# C9.5.2：仲介をまたいでも利用者の委任範囲を失わない

AISVS Verification Level: 2

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.5.2`。採用済みAISVS v1.0、固定Revision
`78775233666a2022dcfb82037e5e029116955c00`を使用する。

> Verify that when an agent acts on a user's behalf, the runtime propagates an integrity-protected, scope-limited token that carries the user's authorization context and is enforced at every downstream call.

日本語訳：Agentが利用者の代理で動く場合、実行基盤が、利用者の認可Contextを含む完全性保護されたScope限定Tokenを
伝播し、その制限が全ての下流呼出しで強制されることを確認する。[要件本文][normative]

Normativeは利用者の認可Contextの保護・伝播・各下流での強制を要求する。
Researchは同じTokenの転送とContextの維持の違い、受理先・主体・Scopeの検証を補足する。[対応Research][research]
以下の文書例はRepository interpretation、持ち帰る言葉は対話からの洞察である。
ResearchのDraft・製品・外部Mappingを適合条件にしていない。学習完了はControl成熟度や製品適合を変更しない。

## 文書要約の具体例

Aliceが「文書Aを要約して」と依頼する。Aliceは文書Aだけを読める。

```text
Alice → Agent → MCP Server → 文書API
```

MCP Server自身はサービス運用のため文書A・B・Cを読める資格情報を持つ。
しかしAliceの代理処理でその広い権限を使い、文書Bまで取得できてはいけない。
攻撃者がAgentへ文書Bを要求させたとき、仲介者の権限で利用者の制限を越える経路を防ぐ。

- 認可Context：利用者、所属Tenant、委任された範囲など、許可判断に必要な情報。
- Scope：委任された操作範囲。readという文字列だけで文書単位の権限が決まるわけではない。
- Audience：Tokenの受理先として指定されたサービス。
- 完全性保護：主体やScopeなどの不正変更を検出・阻止すること。
- 下流呼出し：Agentから仲介、仲介から文書APIという、先のサービスへの要求。

保護対象はAliceの権限範囲と文書。主なTrust BoundaryはAgent、MCP Server、文書APIの各境界にある。
Security Invariantは、仲介・Token交換・再試行で利用者の委任範囲が消失・拡大しないこと。
Enforcement Pointは各受取側のToken検証と認可処理である。
Agentや仲介自身の権限も別の制約として残り、利用者の権限があれば無条件に使えるわけではない。

## 対話：名前をLogへ残すだけの場合

問い：入口でAliceを認証するが、文書APIへは全社文書を読める共通サービス資格情報だけを提示する。
Aliceの名前はLogに記録するが認可には使わず、文書Bも取得できる。

学習者：「Fail」

整理：正しい。入口の認証があっても、下流では利用者の制限が失われている。
名前の記録は監査の手掛かりになっても、利用者の権限を強制することを代替しない。

## 対話：受取先に合わせてTokenを交換する場合

問い：MCP Serverが信頼する発行基盤から文書API専用Tokenを取得する。
Aliceの識別情報と限定された委任範囲が保護され、文書APIが発行者・宛先・期限を検証する。
さらにAliceの文書権限と委任範囲を確認し、Aは許可、Bは拒否する。入口でも認可し途中で権限は広がらない。
入口と別のTokenに交換していても成立するか。

学習者：「Yes」

整理：成立する。Tokenの同一性ではなく、必要なContextと制限の維持を確認する。
宛先ごとに適切な資格情報を取得し、各サービスが検証・認可する構成が取れる。
特定の交換ProtocolやClaim名を一律の必須条件にはしない。

> 引き継ぐべきなのは、Tokenそのものではなく、利用者から委任された権限の範囲です。

## 検証・限界・隣接要件

Positive Testは、文書Aが全経路を通って取得でき、最終APIでもAliceの委任範囲で処理されたと確認できること。
Negative Testでは次を確かめる。

- Agent自身の権限が広くても、Aliceの範囲外の文書Bは取得できない。
- 主体・Scope・必要なTenant情報を欠落・変更させても無制限なサービス権限へ切り替わらない。
- 別サービス向けTokenを受理しない。
- 交換時に広いScopeを要求しても、元の委任を越えた権限を発行・行使できない。

Tokenの署名が正しくても、発行PolicyやResource側の認可が誤っていれば安全ではない。
Token交換の採用自体はScope縮小の保証にならず、発行側と利用側のPolicyを確認する。
利用者の代理ではないサービス固有の処理は適用範囲を分けるが、ユーザ起点の要求を便宜的にサービス処理へ
呼び替えて除外しない。

C9.5.1はToolと引数の許可範囲、C9.5.2は仲介をまたぐ利用者Contextの維持を問う。
C5.2.2の検索・組立時の利用者認可とも関係するが、今回の対象は検索に限定されない。
短命性や現在Policyの継続評価は、それぞれ別の保証として確認する。

## 設計レビューへの問い

- 最終APIは誰のどの委任範囲で処理しているか。
- 仲介者の広い資格情報によって利用者の制限が消えないか。
- 各Tokenの発行元・受取先・主体・Scopeを経路ごとに追えるか。
- Contextが欠落した場合、拒否せず共通サービス権限へFallbackしていないか。

## References

- [AISVS v1.0 C9要件本文][normative]
- [対応Research][research]
- [C9 Family overview](../README.md)
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-05-Agent-Authorization-Delegation.md
