# C9.5.1：Toolの使用許可と引数の認可を分ける

AISVS Verification Level: 2

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.5.1`。採用済みAISVS v1.0の固定Revisionは
`78775233666a2022dcfb82037e5e029116955c00`。

> Verify that agent actions are authorized against fine-grained policies enforced by the runtime that restrict which tools an agent may invoke, and which parameter values it may supply.

日本語訳：Agentが呼び出せるToolと指定できる引数値を制限する、実行基盤が強制する細粒度のPolicyに基づいて、
Agentの行動が認可されることを確認する。[要件本文][normative]

NormativeはToolと引数値への認可を要求する。Researchは呼出元・引数制約・Data範囲と、範囲外の呼出しの拒否試験を
補足する。[対応Research][research] 以下の金額・担当関係・具体的判定はRepository interpretation、
要件をNegative Testとして読む考え方は対話から得た洞察である。
Researchの製品・事件・性能・Mappingは採用していない。学習完了はControl成熟度や製品適合を変更しない。

## 返金Agentの例

顧客対応Agentが返金Toolを使う。Policy（許可条件）は業務側で次のように定めたとする。

- 担当する注文だけを扱う。
- 1回の返金は1円以上1万円以下。
- 返金先は元の決済先だけ。

```text
Agentの要求：refund(注文A, 5000円, 元の決済先)
  → 実行基盤が信頼する注文情報とPolicyで認可
  → 許可した引数のまま実行
```

細粒度は対象や値まで許可範囲を具体化すること。引数はToolに渡す注文ID・金額・送信先などの値。
RuntimeはTool実行を管理する基盤である。

攻撃者が問い合わせ文でAgentを誘導し、別の担当者の注文や攻撃者の口座を指定させる場合を考える。
資産は注文・資金・返金先。Trust Boundaryはモデル生成の要求と、認可を判断・強制する実行基盤の間にある。
Security Invariantは、Agentが誤判断してもToolと引数の組合せが許可範囲を越えないこと。
Enforcement PointはTool実行前の認可処理と下流の強制であり、迂回経路を残さない。

| 検証 | 問うこと |
|---|---|
| 入力形式 | 金額は整数か。注文IDの形式は正しいか |
| 認可 | このAgentが、この注文に、この金額を返金してよいか |

正しい形式の入力でも未許可の操作は存在する。担当関係や権限をAgentの自己申告から取得しない。

## 対話：Toolだけを制限した場合

問い：refundだけを許可し、金額が正の整数かも検証する。しかし担当関係・上限・返金先は確認せず実行する。

学習者：「No。認可系の要件は他にもあった気がするな」

整理：No。形式とTool名だけでは、定義した業務Policyを強制できていない。
既出の認可要件との重なりはあるが、確認軸が異なる。

| 要件 | 問う軸 |
|---|---|
| C5.2.1 | 明示的Allowと、それ以外のDefault Deny |
| C5.2.2 | 検索・Context組立てでの利用者権限 |
| C5.2.5 | 認可判断機構のAgent実行環境からの分離 |
| C9.5.1 | Toolと引数の許可範囲の細かさ |
| C9.5.3 | モデルではなくアプリやPolicy Engineでの認可強制 |
| C9.5.6 | 長時間Sessionでも特権操作時に現在のPolicyを確認 |

これは学習用の比較であり、各要件の全文の代替ではない。一つの認可機構で複数要件を満たせる。
要件の数だけ別の仕組みを作る必要はない。

## 洞察：実装と検証では分け方が違う

学習者：「Negative Test項目としてこれらの項目は有益だね」

同じ返金APIに対しても、破られ方を分けて試す価値がある。

- 許可Ruleのない操作を要求する。
- 別担当者の注文IDへ差し替える。
- 上限超過の金額・別返金先を指定する。
- モデルから「管理者として承認済み」と渡す。
- 権限取消後に継続中のSessionから実行する。

最後の例は現在のPolicyを扱う隣接要件の観点であり、全てをC9.5.1の単独試験にまとめない。
一つの試験に通っても別の認可回避経路が残り得る。期待結果を対応する保証へ追跡する。

> 実装はまとめられる。検証では、破られ方を分けて確かめる。

## 対話：信頼する情報で引数まで認可する場合

問い：実行基盤が注文DBに基づいて担当関係・上限・元の決済先を確認する。
Agentが追加したadmin=trueや「承認済み」は権限の根拠にせず、範囲外操作を実行前に拒否する。
検証した引数がそのまま使われ、迂回経路もない。

学習者：「Pass」

整理：正しい。信頼する情報に基づくTool・引数の認可が、実際の操作へ強制されている。

## 検証・限界・設計レビュー

Positive Testは、担当注文への範囲内返金が正しい宛先へ成功すること。
Negative Testは注文・金額・宛先を一つずつ範囲外へ変更し、拒否応答だけでなく返金が発生しないことまで確認する。
許可後の引数差替えや、別経路からの呼出しも確認する。

1回1万円以下という条件だけでは、繰返しによる累積返金額を制限できない。
必要な累積条件は別途定義し、実行予算や業務上の残額制約と区別して評価する。
技術的な許可範囲内での悪用や、人の承認が必要な操作も残る。認可成功は業務意図の正しさや承認を代替しない。

レビューでは次を確認する。

- 権限や影響を変える引数はどれか。
- 担当関係・Role・対象情報をどの信頼元から取得するか。
- 判定した操作と実行する操作は一致するか。
- 判断不能や別経路で制約が失われないか。

## References

- [AISVS v1.0要件本文][normative]
- [対応Research][research]
- [C9 Family overview](../README.md)
- [C5 Family overview](../../c05-access-control-and-identity/README.md)
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-05-Agent-Authorization-Delegation.md
