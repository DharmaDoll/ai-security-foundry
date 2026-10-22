# 実装の要点：操作提案からOPAの認可判断、業務APIへ

[Pattern本文](README.md)の「担当者Aが注文1001へ3,000円の返金を依頼する」を、データと処理に落とした例。
**モデルが作るのは操作提案だけ。認可に必要な事実は実行サービスが集め、許可した値をAPIへ渡す。**

ここでは`refund.request`だけを具体化する。認証・承認基盤を含む完成したサービスではなく、
JSON、Rego、処理手順から実装時の役割を読み取るためのサンプルである。
`order.lookup`には別の認可ルールを定義し、返金用ルールを通らないことを理由に無条件で許可しない。

## 1. モデルの提案と、認可に使う事実を分ける

Agentが実行サービスへ送れる提案は、次の三項目に絞る。

```json
{
  "action": "refund.request",
  "order_id": "1001",
  "amount_jpy": 3000
}
```

受信時には項目名・必須項目・型・長さ・範囲を検査し、未知の項目や重複JSONキーを拒否する。
`amount_jpy`は正の整数円とし、文字列やbooleanを数値へ暗黙変換しない。
`user_id`、`tenant_id`、`approved`、`url`、`headers`を提案に含めても採用しない。

実行サービスは、次の情報をサーバー側で取得する。

| 情報 | 取得元 | モデルの提案と分ける理由 |
|---|---|---|
| `subject`：担当者Aと現在の権限 | 検証済みセッションと権限の正本 | 自称した利用者や所属では認可できない |
| `task`：今回の注文・操作・上限 | 認証済み画面から確定し、担当者と実行ジョブに結び付けたタスク | モデルがタスクを選び直して権限を拡大することを防ぐ |
| `order`：所属会社、担当、残額、返金可否 | 注文管理の正本 | モデルに渡された古い注文情報を認可の根拠にしない |
| `approval`：承認した対象と金額 | サーバーが保管する承認記録 | メール本文やモデルの「承認済み」を採用しない |
| `now_epoch_s`：判断時刻 | 実行サービスの時計 | モデルに期限判定を任せない |

ジョブと主体・タスクの結び付けも検証する。Agentが送ったタスクIDだけでレコードを切り替えない。
注文情報は認可のためにサービス内で参照し、認可前にはAgentへ返さない。
取得失敗・失効・型不正では止める。ユーザー入力とサーバー情報の汎用的なマージで認可入力を作らない。

### OPAへ渡す入力の形

以下は**実行サービスが組み立てる**リクエスト本文。`proposal`以外の値をAgentから受け取るAPIにはしない。
識別子と時刻は架空の説明値。実装ではサーバーが得た現在値に置き換える。

```json
{
  "input": {
    "proposal": {
      "action": "refund.request", "order_id": "1001", "amount_jpy": 3000
    },
    "subject": {
      "id": "staff-a", "tenant_id": "company-a", "active": true,
      "actions": ["order.lookup", "refund.request"], "refund_limit_jpy": 5000
    },
    "task": {
      "id": "task-1001", "subject_id": "staff-a", "order_id": "1001",
      "active": true, "actions": ["order.lookup", "refund.request"],
      "max_amount_jpy": 3000, "expires_at_epoch_s": 1800000300
    },
    "order": {
      "id": "1001", "tenant_id": "company-a", "assignee_id": "staff-a",
      "refundable": true, "remaining_jpy": 8000
    },
    "approval": {
      "id": "approval-1001", "subject_id": "staff-a", "task_id": "task-1001",
      "action": "refund.request", "order_id": "1001", "amount_jpy": 3000,
      "active": true, "expires_at_epoch_s": 1800000300
    },
    "now_epoch_s": 1800000000
  }
}
```

サーバー由来の情報も、必須項目と型を検証してからOPAへ渡す。
IDは空でない文字列、権限は操作名の配列、金額・期限は整数、状態はbooleanとする。
型不正をRegoの大小比較だけで検出しようとしない。

## 2. 認可ルール：許可条件がすべて揃ったときだけ進める

OPA 1.x / Rego v1の記法で示す。`default allow := false`を起点に、
同じ`allow`本体内の条件をすべて満たした場合だけ許可する。
これは本PJの業務例に対するルールであり、OPAの組み込み返金ポリシーではない。

```rego
package foundry.refund

import rego.v1

default allow := false

allow if {
    p := input.proposal
    s := input.subject
    t := input.task
    o := input.order
    a := input.approval

    # 誰が、どのタスクで、どの注文を扱うか
    s.active == true
    t.active == true
    t.subject_id == s.id
    input.now_epoch_s < t.expires_at_epoch_s
    p.action == "refund.request"
    p.action in s.actions
    p.action in t.actions
    p.order_id == t.order_id
    p.order_id == o.id
    o.tenant_id == s.tenant_id
    o.assignee_id == s.id

    # 利用者・タスク・注文がそれぞれ許す金額か
    o.refundable == true
    is_number(p.amount_jpy)
    p.amount_jpy == floor(p.amount_jpy)
    p.amount_jpy > 0
    p.amount_jpy <= s.refund_limit_jpy
    p.amount_jpy <= t.max_amount_jpy
    p.amount_jpy <= o.remaining_jpy

    # 承認した操作と、今回実行する操作が一致するか
    a.active == true
    a.subject_id == s.id
    a.task_id == t.id
    a.action == p.action
    a.order_id == p.order_id
    a.amount_jpy == p.amount_jpy
    input.now_epoch_s < a.expires_at_epoch_s
}
```

担当者の通常上限が5,000円でも、タスク上限が3,000円なら4,000円は拒否する。
承認した3,000円を2,000円に変えた場合も、この例では承認内容の不一致として再承認を求める。
承認範囲を金額上限として扱う業務では、承認画面とルールの両方でその意味を明示する。

このルールは、入力の出所、業務APIの呼出元、実行時点の残額まで保証しない。
前節の入力構築と、次節の実行境界を合わせて実装する。

## 3. 判断結果を、固定の業務APIへつなぐ

### OPAへの問い合わせ

実行サービスは、前節のJSONを固定の`POST /v1/data/foundry/refund/allow`へ送る。
OPAの接続先と評価パスは配備設定で管理し、モデルに選ばせない。
応答は次のように扱う。

| 応答 | 実行サービスの動作 |
|---|---|
| HTTP 200、JSONオブジェクト、`result`がbooleanの`true` | この認可入力に結び付いた確定操作だけを実行へ渡す |
| `false`、欠落、`null`、文字列の`"true"`、数値の`1` | 拒否する。一般的な「真とみなせる値」の判定を使わない |
| タイムアウト、非200、JSON解析失敗、応答サイズ超過 | 実行しない。拒否・障害の理由を記録する |

OPAの`result`は署名付きの実行許可証ではない。Agentから`{"result": true}`を受け取っても使わない。
実行サービスから認証したOPAへ問い合わせ、同じ処理内で応答と認可入力を対応させる。
OPA自身のAPI認証・認可も設定し、評価を許可したサービスにポリシー更新権限まで与えない。

### API接続部分の処理例

これは言語非依存の処理手順。`命令`は検査したプリミティブ値をコピーした、変更不能な内部データを表す。

```text
提案を検査 → 主体・タスク・注文・承認を正本から取得
  → 命令を確定：操作=refund.request / 注文=1001 / 金額=3000
  → その命令と正本の情報からOPA入力を作る
  → OPAの明示的な許可を確認（それ以外はここで終了）
  → 命令と主体・タスク・承認を、サーバー生成の要求IDに結び付けて保存
  → 実行サービス専用の資格情報で固定の業務APIへ送る
  → 業務APIが呼出元と保存済み命令を照合
  → 実行時の条件を確認して返金依頼を受け付け、要求IDに対応する結果を返す
```

呼出先は、たとえば配備設定にある`https://orders.example.invalid/v1/refund-requests`に固定する。
JSON本文は次のように必要な値だけを組み立てる。汎用的なURL・メソッド・ヘッダーの指定をAgentへ公開しない。

```json
{
  "request_id": "request-1001",
  "order_id": "1001",
  "amount_jpy": 3000
}
```

`request_id`は説明用の値。実際にはサーバーが一意に生成し、保存済みの主体・タスク・承認・確定操作を引く参照とする。
ID自体を認証情報にはしない。業務APIはmTLS等で許可された実行サービスの呼出元を確認し、
要求IDの記録を信頼するストアから取得して、受信した注文・金額との一致も検証する。
記録がない、期限切れ、値が違う、呼出元が違う場合は拒否する。

認可後に元のモデル提案を読み直したり、別タスクの許可結果を使ったりしない。
キューを挟む場合も、受信側が保存済みの命令を取得し、遅延中の失効・状態変化を再確認する。
返金残額の確認と更新は業務API内の同じトランザクションに置く。

HTTPクライアントには証明書検証、接続・読取りのタイムアウト、応答サイズ制限を設定する。
リダイレクトを自動追従せず、資格情報は実行サービスにだけ注入する。
返金受付後に通信が途切れた場合は結果不明として要求IDで照会し、無条件に再送しない。
要求IDがあるだけでは二重受付を防げないため、再送を許すなら業務APIで重複検出を実装する。

## 4. どのチェックで確かめるか

本例を読む際の対応表。実際の操作・証拠欄は[Negative testチェックシート](negative-tests.md)にまとめてある。

| サンプルの要点 | 対応する確認 |
|---|---|
| 主体・タスク・承認をサーバーから取得 | N1 主体偽装、N5 承認流用、N10 情報欠落 |
| 所属・担当・操作・金額の共通範囲だけ許可 | N2 越境、N3 上限、N4 引数逸脱 |
| 確定操作と要求IDを結び付け、業務APIが照合 | N6 差し替え、N7 状態競合 |
| 現在の権限、期限、明示的な許可を確認 | N8 失効、N9 認可障害 |
| 資格情報・通信・ポリシー管理権限を分離 | N11 直接実行、N12 認可ルール変更 |

> 開発者への依頼例：「モデル提案からOPA入力を作る箇所を見せてください。
> `subject`や`approval`がリクエスト本文で上書きされないことと、APIへ渡す注文・金額が
> OPAで確認したものと一致することを確認したいです。」

サーバー由来でも古い権限や承認を使えば誤った許可になる。失効の反映期限と実行時確認は省略しない。
API接続や配備の分離、競合制御をこのサンプルで実行検証したとは扱わない。

## 参照と確認範囲

2026-10-22に以下の公式資料を確認。Rego v1とData APIの記法を参照し、業務ルールは独自に構成した。
公式文書は更新型。OPA 1.xを想定しているが、特定リリースでの評価・製品連携試験は未実施。
ローカルにOPA実行環境はなく、Regoのコンパイル・実行結果は記録していない。

- [OPA Policy Language](https://www.openpolicyagent.org/docs/policy-language)：ルールと構造化入力。
- [OPA default](https://www.openpolicyagent.org/docs/policy-reference/keywords/default)：既定の拒否。
- [OPA v1への移行](https://www.openpolicyagent.org/docs/v0-upgrade)：Rego v1の言語要件。
- [OPA Data API](https://www.openpolicyagent.org/docs/rest-api)：`input`を渡すPOSTと`result`の扱い。
- [OPA APIの保護](https://www.openpolicyagent.org/docs/security)：評価APIと管理操作のアクセス制御。

暗号処理や認証トークンの実装は含めず、秘密値・証明書をサンプルへ埋め込まない。
既存の認証基盤・TLS実装を使い、呼出元の検証を有効にした状態でこの処理を組み込む。
