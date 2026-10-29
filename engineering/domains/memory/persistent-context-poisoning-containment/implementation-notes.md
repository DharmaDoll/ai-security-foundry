# P6の実装例：元資料から作ったメモを、翌日使うまで

[本文](README.md)の①元資料 → ②要約 → ③保存 → ④再利用を追う。SQLはPostgreSQL 18の要点断片で、スキーマ一式や起動可能サービスではない。SQL実行・製品試験は未実施。

中心は、**モデルが返す本文と、サーバーが付ける出所を分け、元資料とメモの版を保存・再利用の両方で比較すること**である。

## 準備：既存の案件・権限と、本人メモを結び付ける

説明中のU1、T-100、S1/S2は表示名。DBでは再割当てしないUUIDを使う。以下はSQLが前提とするデータ契約で、既存アプリのテーブルへ対応付ける。

| テーブル | 主な列・制約 | 更新責任 |
|---|---|---|
| `cases` | `(company_id, case_id)`が一意、`evidence_revision`は非NULL・単調増加 | 業務処理。資料本文・追加・削除・ACL・案件アクセス条件を変えるTransactionで版を進める |
| `company_memberships` / `case_access` | 会社所属の`status`、案件・本人の`can_read`。各Scope内で本人の行は一意 | 既存の所属・案件権限管理 |
| `case_sources` | `(company_id, case_id, source_id)`が一意、`source_revision`、`body`、`active`、`llm_allowed` | 既存の資料管理。`llm_allowed`は今回の固定LLM・用途への送信可否で、本文の自己申告から作らない |
| `source_readers` | `(company_id, case_id, source_id, user_id)`が一意 | この例の資料ACL。行がある本人だけが読める |
| `case_memos` | 主キーは`(company_id, case_id, user_id, purpose)`。`purpose`は`case_handoff`固定。`revision`、`summary_text`、`inputs`、`evidence_revision`、`expires_at`、`job_id` | メモ処理。モデル・ブラウザから直接書かせない |

`case_memos`の空枠は、担当設定・Migration等の管理経路で一度だけ作る。`revision=0`、本文・資料版・期限・処理IDはNULL、`inputs=[]`とする。本人からの保存時に枠を自動作成せず、取消しでも枠や版を削除・初期化しない。既存枠の上書きはしない。

版は非負の整数とし、APIで扱う範囲をDB制約とも一致させる。例では`0..9007199254740991`に制限し、上限到達はエラーにする。本文ありなら出所配列・資料版・期限・処理IDも必須、本文なしならこれらも空という制約を設ける。Scopeの外部キーを設け、別会社の資料へ結び付けない。

DBはPrimary、短いRead Committed Transactionを使う。SQL断片はDriverから一文ずつ発行する。認証・CSRFは既存Web基盤、会社切替時の版と応答の対応は[P5の本人・会社の確認](../authorized-memory-lifecycle/implementation-notes.md#①-本人会社入力を確定する)を使う。

DB・LLM資格は管理されたSecret Store等からサーバーの接続処理だけへ渡す。秘密値をサンプルやモデル入力へ埋め込まない。接続先・TLS証明書を検証し、検証を無効にしない。DB Roleは必要な照会・メモ更新・行ロック取得の権限に絞り、Ownerや管理Roleにしない。

### 全経路で共有する短いDB処理

**元資料の変更、案件権限変更、メモの保存・取消し・読込みが、同じ案件行を最初にロックする。** 一つでも直接更新する経路が残れば、この順序付けの保証は成立しない。業務側の書込処理へも組み込む。

API入口で既存の本人・対象認可を通した後、以下を開始する。ロック用SQLの引数は`$1`会社、`$2`案件。会社は検証済みSessionから、案件はその会社の対象として確定する。

```sql
BEGIN ISOLATION LEVEL READ COMMITTED;
SELECT evidence_revision
FROM cases
WHERE company_id = $1::uuid AND case_id = $2::uuid
FOR UPDATE;
```

案件行がなければ中断する。取得後、**次のSQL文で**所属・案件権限を再確認する。引数は`$1`会社、`$2`案件、`$3`本人。Read Committedの新しい文で、ロック待ちの間に確定した変更も読む。

```sql
SELECT
  EXISTS (
    SELECT 1 FROM company_memberships
    WHERE company_id = $1::uuid AND user_id = $3::uuid AND status = 'active'
  ) AND EXISTS (
    SELECT 1 FROM case_access
    WHERE company_id = $1::uuid AND case_id = $2::uuid
      AND user_id = $3::uuid AND can_read IS TRUE
  ) AS permitted;
```

`permitted`がtrueでなければRollbackし、本文を読み出さない。以下の①・③・④・取消しではこの共通処理を通す。所属やSessionの失効は判定時点で確認するもので、処理中要求の全てを瞬時に止める保証ではない。

ロック待ち・Transactionに短い上限を設け、Timeout時はRollbackする。ロックを保持したままLLMや外部APIを呼ばない。案件内の処理を短時間直列化する設計なので、高頻度更新の案件では待ち時間を評価する。

## ① 元資料の本文と、出所の記録を同じ取得結果から作る

APIの配置例は`/companies/{company_id}/cases/{case_id}/me/handoff-memo`。会社ID・案件IDは認可対象の候補であり、本人IDを本文から受け取らない。

| 操作 | 入力と処理 |
|---|---|
| `GET` | 本人メモの現在版と状態を表示。版はScope確認後に取得し、本文は④の再利用確認を通ったときだけ返す。失効した本文を設定画面から漏らさない |
| `POST /generate` | `expected_revision`だけを受け、①〜③を開始する |
| `POST /clear` | `expected_revision`だけを受け、後述の取消しを行う |
| 既存案件画面の再開API | 今回の依頼を受け、④で確認したメモだけを新しい生成入力へ加える |

ブラウザの作成要求は、認証済みの会社・案件のURLへ送る。入力本文は表示した`expected_revision`だけとし、所有者、出所、信頼ラベル、任意の要約本文を受け付けない。Cookieで状態を変える作成・取消しにはFrameworkのCSRF検証を使う。未知キー・重複キー・型違い・過大な要求は拒否する。

共通DB処理で案件行をロックした後、本人のメモ版と現在読める元資料を取得する。全てDriverの引数バインドを使う。

```sql
SELECT revision
FROM case_memos
WHERE company_id = $1::uuid AND case_id = $2::uuid AND user_id = $3::uuid
  AND purpose = 'case_handoff';

SELECT s.source_id, s.source_revision, s.body
FROM case_sources AS s
JOIN source_readers AS r
  ON r.company_id = s.company_id AND r.case_id = s.case_id
 AND r.source_id = s.source_id AND r.user_id = $3::uuid
WHERE s.company_id = $1::uuid AND s.case_id = $2::uuid
  AND s.active IS TRUE AND s.llm_allowed IS TRUE
ORDER BY s.source_id;
```

枠がない場合は整合性エラー、期待版と違えば競合として止める。元資料が0件なら要約を作らない。資料件数・入力容量の上限を超えたら縮小範囲を明示してやり直し、出所だけを省略しない。

```text
job = サーバーが作る変更不可の生成処理記録
job.scope = 確定済みの会社・本人・案件・用途
job.expected_memo_revision = 取得した本人メモ版（例: 7）
job.evidence_revision = ロックした案件の資料版（例: 41）
job.inputs = 取得行の全(source_id, source_revision)
job.model_input = 同じ取得行の本文。過去の要約・回答・会話履歴は追加しない
job.session_ref / company_context_version / deadline = サーバーで設定
Commitしてロックを解放する
```

本文を実際にLLMへ渡す集合と`job.inputs`を同じ取得結果から作る。ジョブの一時保存先にも閲覧・保持制限を掛ける。生成結果との対応はサーバーの処理IDで結び付け、ブラウザやモデルが返したジョブのMetadataで上書きしない。

## ② 本文だけを要約させる

LLMへは固定の要約依頼と①の本文を新しい要求で渡す。Tool・Connector・ブラウザ実行は有効にしない。期待出力の例：

```json
{"summary_text": "配送遅延についての問い合わせ。最新の配送予定は元資料で確認する。"}
```

返却はこの一項目だけに制限する。JSON構造、重複キー、文字列型、長さを検証する。例えば本文は1〜4000文字とし、上限は製品の用途に合わせる。モデルの`approved`や`sources`を、保存Recordへmergeしない。

正しい形式でも「承認不要」という文章は残り得る。内容検査を追加しても、以降の出所・版・能力の制限は省略しない。

## ③ 全入力の現在の状態を照合し、その版へ保存する

結果はサーバーの元ジョブへ対応付ける。Sessionが有効か、会社選択の版が一致するか、有効期限内かを確認する。共通DB処理を始め、ロック待ちの後にも期限と権限を確認する。

保存する出所配列はモデル出力ではなく`job.inputs`。例は架空のS1/S2である。

```json
[
  {"source_id": "00000000-0000-4000-8000-000000000001", "source_revision": 3},
  {"source_id": "00000000-0000-4000-8000-000000000002", "source_revision": 5}
]
```

配列が非空、項目は二キーだけ、UUIDと非負の整数、IDの重複なしという形を確認する。次のSQLは、利用できない入力を一件でも見つけたら返す。`$1`会社、`$2`案件、`$3`本人、`$4`はサーバー保管の入力配列。

```sql
SELECT i.source_id
FROM jsonb_to_recordset($4::jsonb)
  AS i(source_id uuid, source_revision bigint)
LEFT JOIN case_sources AS s
  ON s.company_id = $1::uuid AND s.case_id = $2::uuid
 AND s.source_id = i.source_id
LEFT JOIN source_readers AS r
  ON r.company_id = s.company_id AND r.case_id = s.case_id
 AND r.source_id = s.source_id AND r.user_id = $3::uuid
WHERE s.source_id IS NULL
   OR s.active IS NOT TRUE OR s.llm_allowed IS NOT TRUE
   OR s.source_revision IS DISTINCT FROM i.source_revision
   OR r.user_id IS NULL
LIMIT 1;
```

一件でも返る、配列が不正、照合が失敗する場合は保存しない。0件でも「文章は安全」ではなく「記録された全入力を現在も利用できる」という確認にすぎない。

同じTransactionで次を実行する。引数`$1..3`は同じScope、`$4`は開始時の資料版、`$5`は開始時のメモ版、`$6`は検査済み本文、`$7`は元ジョブの入力配列、`$8`はサーバーのジョブUUID。

```sql
UPDATE case_memos AS m
SET summary_text = $6,
    inputs = $7::jsonb,
    evidence_revision = $4::bigint,
    revision = m.revision + 1,
    expires_at = statement_timestamp() + interval '7 days',
    job_id = $8::uuid
WHERE m.company_id = $1::uuid AND m.case_id = $2::uuid AND m.user_id = $3::uuid
  AND m.purpose = 'case_handoff' AND m.revision = $5::bigint
  AND EXISTS (
    SELECT 1 FROM cases AS c
    WHERE c.company_id = m.company_id AND c.case_id = m.case_id
      AND c.evidence_revision = $4::bigint
  )
RETURNING m.revision;
```

一行更新してCommitした場合だけ保存成功。0行なら資料変更・取消し・競合等として結果を破棄し、最新の版へ付け替えて再試行しない。エラーはRollbackし、SQL内部情報を応答へ出さない。7日は説明値で、実際の保持方針からサーバーが決める。読取りでは期限を延長しない。

Commitの応答を失った場合は成否不明として現在版を読み直す。未保存と断定して別の版へ再保存しない。取消しの応答喪失も同じ扱いにする。

## ④ 翌日は、出所を確認して新しい入力を組み立てる

現在のWebセッション・会社・案件を確定し、共通DB処理を通す。本人メモを取得する。

```sql
SELECT m.revision, m.summary_text, m.inputs, m.evidence_revision, m.expires_at
FROM case_memos AS m
JOIN cases AS c ON c.company_id = m.company_id AND c.case_id = m.case_id
WHERE m.company_id = $1::uuid AND m.case_id = $2::uuid AND m.user_id = $3::uuid
  AND m.purpose = 'case_handoff' AND m.summary_text IS NOT NULL
  AND m.expires_at > statement_timestamp()
  AND m.evidence_revision = c.evidence_revision;
```

0行ならメモを使わない。1行なら出所配列の形を再確認し、③の全入力の照合SQLを`m.inputs`で実行する。一つでも利用不可ならメモ全体を除外する。Commitしてロックを解放した後、有効だった本文だけを使う。

```text
生成入力 = アプリ管理の固定指示
         ＋ 今回の本人の依頼
         ＋ reference_noteとしてのメモ本文（有効だった場合だけ）
固定指示・Tool定義・権限・承認・宛先をメモから組み立てない
新しいLLM要求を作る。Tool一覧とTool呼出しの実行経路は空
返却がTool要求や業務更新命令でも実行せず、許す文字列応答だけ扱う
```

実際のメッセージはSDKの構造化APIで組み、本文をJSONやSQLのコードへ文字列連結しない。データ欄の区別はモデルへの補助であり、指示無視の保証ではない。保証を担うのは業務操作の経路を持たせないことと、外側の認可・開示判断である。

UIは安全なテキスト表示を使い、HTML・Markdown・外部画像取得・リンクプレビューを動かさない。応答は`Cache-Control: no-store`とし、本人・会社の選択が変わった画面へ遅い応答を混ぜない。

メモだけの失効・取得障害なら、現在読める元記録から調査を再開する。所属や案件権限を確認できない場合は要求停止。古いメモを使ったfallbackはしない。

## 取消し・元資料変更も、同じ順序に組み込む

### 本人メモを取り消す

取消し要求は表示したメモの`expected_revision`だけを受け付け、Session・会社・CSRF・共通DB処理を通す。`$1..3`は会社・案件・本人、`$4`は期待メモ版。

```sql
UPDATE case_memos
SET summary_text = NULL, inputs = '[]'::jsonb,
    evidence_revision = NULL, expires_at = NULL, job_id = NULL,
    revision = revision + 1
WHERE company_id = $1::uuid AND case_id = $2::uuid AND user_id = $3::uuid
  AND purpose = 'case_handoff' AND revision = $4::bigint
RETURNING revision;
```

一行更新とCommit後に完了を返す。保存が先に版を進めた場合、古い版への取消しは0行で未完了。画面を読み直して取り消す。取消しが先なら、古い作成ジョブは③で0行になる。

### 元資料・ACLを変更する

業務側の更新は、その操作の権限を別に確認したうえで同じ案件行をロックする。資料本文・`source_revision`・ACL等の変更と、次の資料版の更新を同じTransactionでCommitする。引数は`$1`会社、`$2`案件。

```sql
UPDATE cases
SET evidence_revision = evidence_revision + 1
WHERE company_id = $1::uuid AND case_id = $2::uuid;
```

削除・復元・ACL変更・案件のアクセス条件変更も対象。古い資料版・メモ版へ巻き戻さない。全経路がこの手順を守ることはDBが自動保証する機能ではなく、アプリ側の実装条件である。直接SQL、管理画面、定期処理も確認する。

| 到着順 | 結果 |
|---|---|
| ジョブ開始：資料41・メモ7 → 取消し7→8 → ジョブ完了 | 期待メモ版7が合わず、保存しない |
| ジョブ開始：資料41 → S2の変更で資料42 → ジョブ完了 | 資料版が合わず、保存しない |
| メモ保存成功 → S2の権限変更・Commit → 新しい再開 | 資料版／全出所の照合で旧メモを除外 |
| 再利用確認完了 → 取消し・資料変更 | 既に読み出した処理は進み得る。以後の新しい読込みは除外する |

## 会話再開と、既にMemory製品を使う場合

主例は毎回新しい生成要求を組み立てる。再開状態に保存するのは案件・メモの識別子や版で、前回の要約本文・回答・System Promptを次の生成要求へ自動復元しない。旧Contextを安全に除けない場合は、新しい会話として再開する。

| 既存の仕組み | 組み込む場所と確認 |
|---|---|
| LangGraph Store / Checkpointer | 要約nodeは本文だけ返し、保存nodeで③を行う。Store取得とCheckpoint再開のどちらも④を経由させる。保存履歴を丸ごとモデルへ渡す構成は主例に含まれない。[公式のMemory構成](https://docs.langchain.com/oss/python/concepts/memory) |
| AgentCore Memory等の外部サービス | 元イベントと派生記録は別に管理され得る。[DeleteEventの注意](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/short-term-delete-event.html)を踏まえ、外部生成・削除の遅延と再利用の確認を設計し直す。同一DBのロック例をそのまま保証として使わない |

レビュー依頼例：

> S1/S2から作ったメモで、モデルがS1しか引用しない結果を返すようにしてください。保存された出所にS2も残ること、S2の権限を取り消した後の入力に旧メモが入らないことを確認したいです。別に、メモを取り消した後で古い要約処理を完了させ、更新0行になることと、会話再開からも復活しないことを示してください。
