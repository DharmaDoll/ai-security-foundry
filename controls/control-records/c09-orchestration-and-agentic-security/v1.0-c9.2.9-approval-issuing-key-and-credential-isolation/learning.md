# C9.2.9：承認を発行する力をAgentから隔離する

AISVS Verification Level: 3

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.2.9`。採用済み固定Revisionは
`78775233666a2022dcfb82037e5e029116955c00`。

> Verify that cryptographic key material or credentials used to issue approvals are isolated from the agent runtime.

日本語訳：承認の発行に使用する暗号鍵や資格情報が、Agentの実行環境から隔離されていることを
確認する。[要件本文][normative]

Normativeは要件本文、Researchは補足。承認ServiceとKMSによる構成はRepository interpretation、
対話からの整理は学習上の洞察である。学習完了はControl成熟度や製品適合を変更しない。

## C9.2.8との違い

C9.2.8は、発行済みの承認を別操作へ差し替えたり二度使ったりできないかを問う。
C9.2.9は、Agentが正規の承認そのものを勝手に発行できないかを問う。

返金Agentが承認用秘密鍵を読めると、「10万円の返金を承認済み」というデータを偽造できる。
実行APIが署名を検証しても、正規鍵による署名なので通ってしまう。人の業務に置き換えると、
申請者が承認者の印鑑を自由に使える状態である。

鍵を別Serviceへ保管するだけでも足りない。Agentが任意の内容へ署名を要求できれば、
秘密鍵を盗まずに承認を作れる。保護対象には秘密鍵だけでなく、署名APIを使うCredential、
承認記録、発行Policy、Signerの設定と配置も含まれる。

## 信頼境界と具体構成

| 役割 | 許可すること |
|---|---|
| Agent | 操作の提案、承認申請、状態確認。 |
| 承認Service | 権限のある人による具体的な承認記録を確認し、その内容だけに署名する。 |
| 実行API | 署名、承認内容、実行要求、一回性を検証して実行する。 |

Trust Boundary（信頼境界）はAgentの実行権限と、承認の発行・管理権限の間。
Security Invariant（守るべき性質）は、Agentが鍵を取得できず、Agentの要求だけで任意の承認を
発行できないこと。Enforcement Point（強制点）は、鍵のAccess Control、承認発行APIの認可、
承認記録の更新、Signerの管理・配置である。

承認Serviceは、Agentが渡す`approved=true`を信用しない。自分が管理する承認記録から、
承認者のIdentity・権限・具体的な判断を確認する。Researchも、非Export鍵であっても署名APIを
自由に使えれば隔離にならないことを補足する。[Research][research]

## 実装例と検証

Agentには承認の申請と状態確認だけを許し、承認状態の更新と署名権限を与えない。
承認Serviceだけが正当な記録に基づいて署名を要求する。例えばAWS KMSでは秘密鍵をKMS内で使い、
`Sign` APIの権限を承認ServiceのIdentityに限定できる。KMSが人の承認を判断するわけではなく、
その判断は承認Serviceが担う。この製品例は2026-09-11に公式資料を確認したもので、必須方式や
製品適合を示さない。[AWS KMS Sign][kms-sign] [AWS KMS key policy][kms-policy]

Negative Test（不正や失敗条件を意図的に試す検証）では、Agentの全Credentialを使い、鍵の読取、
承認記録の変更、任意署名、Signerの設定・再配置、LogやTraceからの秘密取得を試す。
「鍵がExport不可」という設定表示だけでなく、未承認内容へ有効な承認を発行できない結果を確認する。

鍵が隔離されても、承認Serviceへ渡る人の判断が偽造可能なら一連の承認は安全ではない。
一つの弱点がC9.2.1とC9.2.9の両方をFailさせる場合もある。Requirementは排他的な分類ではない。

## 対話の再構成

**問い：秘密鍵は外部鍵管理ServiceにありAgentから取得できないが、Agentは任意の内容へ署名を
要求できる。人の承認なしに承認データを作れる。適合するか。**

学習者：「わからん。難しいな」

整理：Fail。鍵を盗むことと、鍵を自由に使わせることは別。承認印を金庫から取り出せなくても、
窓口が内容を確認せず何にでも押印すれば、申請者は自分で承認済みにできる。

**質問：では、どうやって制御するのか。**

整理：Agentには申請だけを許す。人は承認Serviceへ自分のIdentityでアクセスし、具体的な申請を
承認する。承認Serviceは自分が管理する承認記録を確認し、保存済みの内容だけに署名する。
Agent用IdentityにはKMSの署名権限を与えず、承認Service用Identityだけに与える。

**問い：Agentは鍵や署名APIを使えないが、承認記録を`approved`へ変更できる。
承認Serviceはその記録へ自動署名する。適合するか。**

学習者：「No」

整理：Agentは承認状態の改ざんを経由して、実質的に自分の承認を発行できるためFail。
正規署名が作られるので、実行APIだけでは偽の人間判断を見分けられない。この場合、実際の人の
承認を受けていないC9.2.1と、Agentが発行経路を支配するC9.2.9の双方に関係する。

学習者は最後の整理に`OK`と応答し、このRequirementの学習を一巡した。

## 洞察と設計レビューへの問い

**鍵をAgentから隠すだけでなく、承認を発行する力をAgentから隔離する。**

- Agentは鍵、署名Credential、承認記録、発行Policyのどこまで操作できるか。
- 承認Serviceは、人の判断をAgentの自己申告とは別の信頼できる経路で確認するか。
- AgentがSignerを再配置したり、別の鍵・Endpointへ差し替えたりできないか。
- 正規署名の存在から、正規の人間判断があったと追跡できるか。

## References

- [AISVS v1.0 C9.2.9][normative]
- [対応Research][research]
- [AWS KMS Sign API][kms-sign]
- [AWS KMS key policies][kms-policy]
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-02-High-Impact-Action-Approval.md
[kms-sign]: https://docs.aws.amazon.com/kms/latest/APIReference/API_Sign.html
[kms-policy]: https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html
