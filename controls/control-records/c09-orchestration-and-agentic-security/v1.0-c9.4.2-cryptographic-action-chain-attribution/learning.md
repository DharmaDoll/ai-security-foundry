# C9.4.2：操作内容と実行Chainを暗号的に結び付ける

AISVS Verification Level: 2

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.4.2`。採用済みAISVS v1.0の固定Revisionは
`78775233666a2022dcfb82037e5e029116955c00`。

> Verify that agent-initiated actions are cryptographically bound to each step of the execution chain for non-repudiation.

日本語訳：否認防止のため、Agentが開始した操作が実行Chainの各Stepに暗号的に結び付けられていることを確認する。[要件本文][normative]

Normativeはこの要求、Researchは記録の結合・検証例や限界の補足である。
以下の構成と判定条件はRepository interpretation、質疑から得た考え方はDerived insightとして扱う。
Research内の製品・事件・性能・外部Mappingは本ノートで検証・採用していない。
学習完了はControl成熟度や製品適合を変更しない。

## 具体例から理解する

社内Agentが請求書を読み、送金を依頼する。

```text
依頼 → Agent → Planner → Tool Router → MCP Server → 送金API
```

Plannerは実行計画を作るComponent、Tool Routerは呼び出すToolへ要求を振り分けるComponentである。
途中のMCP Serverが侵害され、「A社へ1万円」を「B社へ100万円」に変更したとする。
攻撃者が記録まで差し替えられると、誰がどの操作を依頼し、どこで変わったかを追えなくなる。

C9.4.1は個々のAgent Instanceの身元を扱う。C9.4.2は、その主体と実際の操作内容、実行経路の関係を
検証可能な証拠にする。保護対象は操作記録と主体帰属であり、主なTrust Boundaryは各Component間と記録保存先との間にある。

## 用語と結合対象

- Execution Chain：操作に至る処理の連鎖。分岐や別Agentへの委任も含む。
- Trace ID：同じ処理に属する記録を検索する識別子。単なる文字列は偽造できる。
- Hash：内容から計算する照合用の値。単体では作成者を証明しない。
- HMAC：共有秘密鍵を使う改ざん検出方式。検証者も同じ鍵を持つため、鍵保持者同士の作成者の区別には限界がある。
- 電子署名：秘密鍵で署名し、対応する公開鍵で検証する方式。公開鍵を誰のものとして信頼するかも必要。
- 否認防止：操作を主体へ帰属させる証拠を残すこと。鍵侵害や発行者の虚偽まで排除する絶対的・法的保証ではない。

一例として、StepごとにChain ID、Step ID、前の記録のHash、主体、操作名、送金先・金額のHash、
対象System、時刻を結合して署名する。これは必須Field一覧ではなく、操作と連鎖の意味を保護するための設計例である。
ResearchもPayloadと親記録への結合を補足している。[対応Research][research]

Security Invariantは、操作内容・主体・Chain上の関係を変更した場合に、証拠の検証で検出できること。
決定論的なEnforcement Pointは、記録生成・署名処理と、その記録を照合する検証処理にある。
実行側では署名対象と実際の要求を対応付け、事後監査では実行結果との関係を追跡する。
全体削除や末尾切捨ての検出には、Hash連鎖だけでなく外部Checkpointなど期待する記録範囲の根拠も必要になる。

## 対話と判定の再構成

### 個体認証と平文Trace IDだけで足りるか

問い：各Agentは固有のmTLS証明書で認証するが、Chainは平文Trace IDと自己申告Logだけで、中間記録を変更できる。

学習者：「Fail。具体的にはHMACのような技術で値を検証するイメージでしょうか？」

整理：Fail。通信相手の認証だけでは、保存された操作の連鎖は保護されない。
HMACは改ざん検出の選択肢だが、誰でも共有鍵で記録を作れる構成を、独立した主体帰属の証拠と主張してはいけない。

### 操作ParameterをHashで記録する場合

問い：各Stepに主体・操作・対象・親記録のHash・ParameterのHashを含めて署名し、次のComponentが検証する。
Parameterの生値は監査Logへ保存しない。

学習者：「Fail」

訂正：記録形式だけを理由にFailにはできない。重要な値を漏れなく含め、同じ意味のDataを一定の表現へ整える
正規化を行い、実行内容との照合ができるなら、この結合方式は成立し得る。
問題文にある署名FieldだけでSystem全体の適合を断定できるわけではない。
後日の検証に必要なDataをどこで保持するか、秘密をLogへ残さないかは別途設計する。

> C9.4.2は「全部ログに残せ」ではなく、「実行Chainを改ざん検出可能に結び付けろ」です。

### 操作名だけを署名する場合

問い：署名対象が「送金する」だけで、送金先と金額を書き換えても検証に成功し、そのまま実行される。

学習者：「Fail」

整理：正しい。操作の意味を決める値が保護されていない。

> 署名が有効であることと、実行した操作が署名で保護されていることは別です。

## 運用の疑問：鍵と公開鍵はどう管理するか

学習者：「Agent Instance毎に秘密鍵を持たせて署名するのは鍵管理が煩雑そう。
署名検証する公開鍵はどこで取得するのか。複数Agentだとこれも煩雑になりそう。」

一つの構成は、署名済み記録と一緒に公開鍵を含む証明書を渡す方法である。
認証局（CA）は身元と公開鍵の対応を署名する発行元で、検証側は事前に設定した信頼するCA、
証明書の有効性・用途・期待する主体を確認し、記録の署名を検証する。
相手が持ち込んだ任意の証明書を信頼するわけではない。

SPIFFE/SPIREは身元と資格情報を配る基盤の例である。SPIREは実行環境・Workloadを確認して身元証明を発行し、
SPIFFE Workload APIは証明書・鍵・信頼する発行元の情報を取得する仕組みを提供する。
個々の鍵を手作業で全検証先へ登録する負担を減らせる。
ただし、導入だけでStepへの署名やInstance単位の識別が完成するわけではない。
識別名の割当とInstanceへの対応を設計する。[SPIFFE Concepts][spiffe]、[SPIRE Concepts][spire]

別案は、信頼する実行基盤が各Stepを観測し署名する構成である。
証拠が示すのは「実行基盤がAgent Aの操作として記録した」という事実になる。
基盤が認証済み主体と実際の操作を結び付ける必要があり、自己申告を無条件に署名するだけでは足りない。
Agent個体の鍵による署名とは信頼の置き場所が異なる。

過去の証拠の検証には当時の証明書・信頼情報や検証時刻の根拠も考える。
現在の通信認証と、半年前の操作の検証では必要な情報が異なる。
短命な認証用資格情報を発行できることだけで長期監査の設計を完了としない。

## 保証範囲とNegative Test

署名は発行された記録の真正性・改ざん検出を支えるが、操作の認可、業務上の正しさ、
記録者が事実を述べたことまでは保証しない。人の承認と操作の結合はC9.2.8、資格情報の定期更新はC9.4.3で扱う。
Hashも低Entropy値の推測や業務関係の漏えいを防ぐ保証にはならない。

- 送金先・金額・主体を書き換え、検証が失敗するか。
- 正しい記録を別Chainへ移し、転用を検出できるか。
- 中間Stepを削除・入替えし、不整合を検出できるか。
- 正常なChainでは主体・操作・順序と分岐を復元できるか。
- 未信頼の公開鍵を持ち込んでも、正規Agentの記録として受理されないか。

## 洞察と設計レビューへの問い

> 実行Chainへの署名は、暗号処理の導入だけでは完結しない。
> 誰の操作を、誰の保証で、いつまで検証できるようにするかという運用設計が必要になる。

これは対話から得た設計上の洞察であり、AISVSに特定の鍵管理製品を要求するものではない。

- 証明したい主体はAgent個体か、実行基盤か。誰が証拠を偽造できるか。
- 操作の意味を変える値を全て保護しているか。
- 公開鍵と主体の対応を誰が保証するか。
- 鍵更新後でも必要な期間の証拠を検証できるか。
- 記録の完全性と機密性をどう両立するか。

## References

- [AISVS v1.0 C9要件本文][normative]
- [固定版の対応Research][research]
- [SPIFFE Concepts][spiffe]（補足資料、2026-09-16参照。latestの仕様は今後変わり得る）
- [SPIRE Concepts][spire]（同上）
- [C9 Family overview](../README.md)
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-04-Agent-Identity-and-Audit.md
[spiffe]: https://spiffe.io/docs/latest/spiffe/concepts/
[spire]: https://spiffe.io/docs/latest/spire-about/spire-concepts/
