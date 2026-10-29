# P5の実装例：本人設定の保存から取消しまで

[本文](README.md)と同じ①本人と会社 → ②保存 → ③次回読込み → ④取消しを追う。既存Webアプリに追加する疑似コードとPostgreSQL 18のSQL断片であり、起動可能なサービスではない。SQL・製品連携は未実行。

**中心になる処理は、会社・本人・用途・期待版を含む更新と、毎回の有効性確認。** 任意のMemory書込Toolや新たな認可製品は追加しない。

## 準備するものと、毎回動くもの

| 準備するもの | 要求ごとに動くもの |
|---|---|
| 既存のログイン・CSRF保護、会社選択、所属台帳 | ①本人・現在の所属・画面の会社選択の一致を確認 |
| 会社・利用者ごとの設定枠と、許可する値 | ②表示版に対して保存し、④同じ条件で取消す |
| DB・LLMへ接続するサーバー側の資格 | ③有効設定を読み、固定文へ変換して推論へ渡す |

DBはPrimaryへ短いRead Committed要求でアクセスする。遅延Replica、前の要求から続く長いTransaction、古い設定のアプリCacheをこの例に混ぜない。DB資格・LLM資格は管理されたSecret Store等から接続処理だけへ渡し、コードに値を書かない。通信先とTLS証明書を検証し、検証を無効にしない。

DB実行Roleは必要なSELECTと設定値・版・期限のUPDATEだけを許し、Table OwnerやBYPASSRLSにはしない。設定枠の初期作成と物理削除は別の管理経路で行う。Web利用者の認可は以下のAPI・SQL条件で行う。

## ① 本人・会社・入力を確定する

説明中の会社A・担当者U1は架空の表示名。DBには再割当てしない内部UUIDを使う。`company_memberships(company_id, user_id, status)`は既存の所属台帳で、会社・利用者の組は一意とする。

設定APIの例：

| 操作 | 入力 | 結果 |
|---|---|---|
| `GET /companies/{company_id}/me/answer-preferences` | 会社の候補、画面に結び付く会社選択の版 | 本人の設定、現在版、有効／期限切れ／未設定。`Cache-Control: no-store` |
| `PUT` 同じURL | `expected_revision`、`language`、`detail` | 保存できた版を返す。状態変更なのでCSRF検証必須 |
| `POST` 同じURLの`/clear` | `expected_revision`だけ | 値を消した版を返す。状態変更なのでCSRF検証必須 |

会社選択の版は、既存画面を表示するときにサーバーが渡した`context_version`を要求Headerへ付ける例とする。会社切替でサーバーの版を進める。これはCookieやCSRF tokenの代替ではない。初期画面のBootstrapも認証済みWeb基盤が行う。

```text
s = 既存Web基盤がCookieから検証したサーバー側Session
if Sessionが失効・期限切れ: 401
if route.company_id != s.active_company_id: 409（会社選択を再表示）
if header.context_version != s.company_context_version: 409

company_id = s.active_company_id
user_id = s.internal_user_id
m = 所属台帳を(company_id, user_id)で取得
if mがない or m.status != "active": 403
if 認証・所属を確認できない: 停止

PUTとclearは既存FrameworkのCSRF検証を通す
JSONのサイズを制限し、重複キー・未知のキー・型違いを拒否
expected_revisionは0以上の安全に表現できる整数（真偽値・文字列を受け付けない）
PUT: キーはexpected_revision, language, detailだけ
     languageはja/en、detailはbrief/standardだけ
clear: キーはexpected_revisionだけ

DBパラメータのcompany_id, user_idは上で確定した値
purposeはサーバー固定のanswer_preferences
```

実行中に会社選択が変わっても、取得済みの本人・会社を別の会社へ付け替えない。切替前に受け付けた更新が元の会社で完了することはあり得るが、その応答を切替後の画面へ反映しない。サーバーは返却前にも現在の会社選択の版を確認し、UIも要求時の版と違う応答を破棄して再読込みする。

AgentのToolからこの状態変更APIへ接続する経路はない。人が操作するWeb APIにだけCookie／CSRFで接続する。Agent由来の提案を将来受け付ける場合も、これを本人の保存操作へ自動変換しない。

## 保存の形：値が空でも版は残す

次は管理用Migrationで作るSchemaの例。`company_memberships`の複合一意キーが存在する前提である。

```sql
CREATE TABLE answer_preferences (
    company_id uuid NOT NULL,
    user_id uuid NOT NULL,
    purpose text NOT NULL CHECK (purpose = 'answer_preferences'),
    revision bigint NOT NULL DEFAULT 0
        CHECK (revision BETWEEN 0 AND 9007199254740991),
    language text,
    detail text,
    expires_at timestamptz,
    updated_at timestamptz NOT NULL DEFAULT statement_timestamp(),
    PRIMARY KEY (company_id, user_id, purpose),
    FOREIGN KEY (company_id, user_id)
        REFERENCES company_memberships (company_id, user_id),
    CHECK (
        (language IS NULL AND detail IS NULL AND expires_at IS NULL)
        OR
        (language IS NOT NULL AND detail IS NOT NULL AND expires_at IS NOT NULL
         AND language IN ('ja', 'en') AND detail IN ('brief', 'standard'))
    )
);
```

所属の作成処理で、その本人・会社の空の設定枠を一度だけ作る。これは管理された所属作成Transaction内で行う。既存利用者の枠はMigrationで用意する。

```sql
INSERT INTO answer_preferences (company_id, user_id, purpose)
VALUES ($1::uuid, $2::uuid, 'answer_preferences')
ON CONFLICT (company_id, user_id, purpose) DO NOTHING;
```

利用者向けPUTで欠けた枠を自動作成しない。取消し・期限切れ処理でも枠のDELETE→再作成や版の0への初期化を行わない。空の枠に残す本人・会社・版も管理対象のMetadataであり、無期限保持の推奨ではない。完全なアカウント廃止と物理削除は[本文の運用](README.md#6-運用と限界)に従う。

## ② 表示した版へ保存する

U1が見た版7に対する保存入力：

```json
{"expected_revision": 7, "language": "ja", "detail": "brief"}
```

`$1`は会社、`$2`は本人、`$3`は期待版、`$4`は言語、`$5`は文量。全てDB Driverでバインドし、SQL文字列へ連結しない。`expected_revision`は認可情報ではなく、①で認可した対象への競合チェックに使う。

```sql
UPDATE answer_preferences AS p
SET language = $4,
    detail = $5,
    expires_at = statement_timestamp() + interval '30 days',
    revision = p.revision + 1,
    updated_at = statement_timestamp()
WHERE p.company_id = $1::uuid
  AND p.user_id = $2::uuid
  AND p.purpose = 'answer_preferences'
  AND p.revision = $3::bigint
  AND EXISTS (
      SELECT 1 FROM company_memberships AS m
      WHERE m.company_id = p.company_id AND m.user_id = p.user_id
        AND m.status = 'active'
  )
RETURNING p.revision, p.language, p.detail, p.expires_at;
```

30日はこのガイドの説明値で、実際の保持方針に合わせてサーバー側で固定する。ブラウザが送る任意の期限は受け付けない。期限延長は本人の新しい保存として扱い、読取りだけで延長しない。

一行更新してCommitできたときだけ、版8を保存成功として返す。0行なら変更なしで競合等を返す。現在の所属失効が分かれば403、版不一致なら409。DBエラーは成功に変えず、SQL内部情報を応答に含めない。応答を失った場合は設定を再読込みし、最新の版へ無条件に差し替えて再保存しない。

設定画面のGETは同じ会社・本人・用途とactiveな所属で一行を読み、版と状態を表示する。期限切れの値を新しい有効設定として表示しない。認可済み利用者でも枠が欠落していれば整合性エラーとして扱い、版0の新しい枠だと推測しない。

## ③ 有効な設定だけを次の生成要求へ渡す

生成要求でも①の本人・会社・所属を確認する。既存会話を指定するときは、会話の保存元が持つ`company_id`と`owner_user_id`が確定済みの会社・本人に一致しなければ拒否する。会話ID自体を認可の証拠にしない。

```sql
SELECT p.revision, p.language, p.detail, p.expires_at
FROM answer_preferences AS p
JOIN company_memberships AS m
  ON m.company_id = p.company_id AND m.user_id = p.user_id
WHERE p.company_id = $1::uuid
  AND p.user_id = $2::uuid
  AND p.purpose = 'answer_preferences'
  AND m.status = 'active'
  AND p.expires_at > statement_timestamp();
```

```text
所属の確認済み = ①の判定が成立した状態
pref = 上のSQL結果（0行なら設定なし）
if 設定だけの取得障害: prefなしとして固定の既定値を使用し、障害を記録

language_text = {ja: "日本語で回答する", en: "英語で回答する"}
detail_text = {brief: "簡潔にまとめる", standard: "通常の詳しさで説明する"}
if prefあり:
    言語・文量が各表のキーでなければ設定を使わず、異常を記録
    有効なら表から選んだ二つの固定文だけを生成条件へ追加

毎回、アプリの固定指示＋今回の設定条件＋認可済みの会話入力を組み立てる
前回の設定条件を含むSystem Prompt・生成要求を再利用しない
本人・会社・revision・Cookie・DB/LLM資格はモデルへ渡さない
Toolの認可・対象の確認は別の信頼する情報で行い、設定値を参照しない
```

設定条件は会話履歴・要約へ追記保存しない。モデルが返した文章を保存する場合、その文章が設定の正本になるわけではない。取消し後も以前の日本語の回答や利用者自身の発言がモデルの応答へ影響する可能性はあるため、取消しの試験では「英語で返ったか」でなく、旧設定条件を生成入力へ付けていないかを見る。

PrimaryのRead Committedで、取消しCommit後にこのSELECTを開始すれば取消し後の状態を読む。取消し前に開始したSELECT・要求まで遡って無効にする保証ではない。所属失効・会社切替も判定前後の進行中要求を区別し、現在の会社と異なる会話応答はUIへ出さない。

## ④ 値を消し、古い保存要求を拒否する

取消し入力は`{"expected_revision": 8}`。①の共通チェックを通した後、同じバインド引数`$1`会社、`$2`本人、`$3`期待版を使う。

```sql
UPDATE answer_preferences AS p
SET language = NULL,
    detail = NULL,
    expires_at = NULL,
    revision = p.revision + 1,
    updated_at = statement_timestamp()
WHERE p.company_id = $1::uuid
  AND p.user_id = $2::uuid
  AND p.purpose = 'answer_preferences'
  AND p.revision = $3::bigint
  AND EXISTS (
      SELECT 1 FROM company_memberships AS m
      WHERE m.company_id = p.company_id AND m.user_id = p.user_id
        AND m.status = 'active'
  )
RETURNING p.revision;
```

この更新も一行の更新とCommitを確認してから完了を返す。版8を取り消すと版9になる。設定値と期限は消えるが版は残る。

| 順序 | DBの状態 | 古い保存要求の結果 |
|---|---|---|
| 保存成功 | 版8、日本語・短め | 版7への再送は不一致 |
| 版8の取消し成功 | 版9、値なし | 版8への保存は不一致 |
| 本人が再表示し、改めて保存 | 版10、新しく選んだ値 | 新しい本人操作なので許可できる |

同じ版8に対して保存と取消しが競合した場合、先に更新した側が版を進め、もう一方は0行になる。**保存が先に成功したなら、取消しは未完了。** 画面を再表示して取消し直す。競合した取消しを成功扱いしてはいけない。PostgreSQLのRead Committedでは、競合するUPDATEを待った後に更新後の行へ条件を再評価するため、期待版の条件がこの区別を作る。[公式の説明](https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED)

会話再開、バックアップ復元、アカウント再作成でこの版の扱いを迂回しない。取消しAPIだけ正しくても、別の処理が古い値を戻せば保証は成立しない。

<a id="memory-services"></a>

## 必要な場合だけ追加する仕組み

| 仕組み | 追加する理由と確認点 |
|---|---|
| PostgreSQL RLS | 複数のDBアクセス経路にも行の制限を掛ける場合。会社・本人のContextの設定元、接続プールの残留、Owner／BYPASSRLSの迂回を確認する。アプリの対象条件は維持する。[P2のSQL例](../../rag/secure-multi-tenant-retrieval/implementation-notes.md#shared-db-example)は参考だが、P5の書込み・取消しは別に評価する |
| LangGraph Store / Checkpointer | アプリが会話横断Storeやthreadの状態を実際に必要とする場合。認証済み主体からnamespaceを組み立て、Storeとcheckpointのどちらに設定の複製があるか確認する。[公式概念ガイド](https://docs.langchain.com/oss/python/concepts/memory) |
| AgentCore Memory | 自動抽出・Managed Storeが必要な場合。元イベントの削除は派生Memoryの削除にならない。長期MemoryのTTLは即時の読取除外ではなく、期限切れ後も返り得る。[イベント削除](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/short-term-delete-event.html)・[TTL](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/long-term-record-ttl.html)。利用停止と回収の保証を採用APIで別に確認する |

上記は製品機能の比較であり、主例の依存関係ではない。版・確認日は[本文の参照情報](README.md#7-根拠とレビュー情報)に記録する。

レビュー依頼例：

> 現在のアプリ版で、版8の取消しを完了させた後に、保存しておいた版8の更新要求を送ってください。DBの値と版、更新行数、次のLLMへ渡した設定条件を確認したいです。409を返した記録だけの場合は、別の書込経路やCacheで旧値が復活していないことも示してください。
