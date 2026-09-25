---
title: "Access TokenのIssuer・Audience・Expiration・Scopeを検証する"
versioned_id: "v1.0-C10.2.2"
requirement_id: "C10.2.2"
verification_level: 1
family_id: "C10"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-02-Authentication-Authorization.md"
last_verified: "2026-09-24"
maturity: "verifiable"
mapping_assessment_refs: []
---

# Access TokenのIssuer・Audience・Expiration・Scopeを検証する

AISVS Verification Level: 1

## Upstream basis

AISVS `v1.0-C10.2.2`は、提示されたAccess TokenのIssuer、Audience、Expiration、Scope Claimを
OAuth 2.1に従ってMCP Serverが検証することを求める。採用済みstable v1.0の固定Revisionで
要件本文とC10.2 Researchを確認した。特定IdP、JWT Library、Scope名を一律に要求しない。

Researchは、別Issuer・別Resource向けToken、期限切れToken、Scope不足を主要なNegative Caseとして
示す。以下のClaim Policyと観測条件はRepository interpretationである。

## Interpretation

Tokenの署名が暗号的に正しいだけでは許可しない。MCP Serverは、信頼するIssuerから発行され、
自ServerというResourceをAudienceとし、評価時点で有効期限内で、要求操作に必要なScopeを持つことを
検証する。いずれかが欠落・不一致・検証不能なら、Tool／Resource処理前に拒否する。

## Security objective

別IdP、別MCP Server、別API、期限切れ、権限不足のTokenを、正規Access TokenとしてReplay・流用し、
本来許可されないToolやResourceへAccessすることを防ぐ。

## Applicability

OAuth Access TokenをResource Serverとして受理するMCP Server／Gatewayに適用する。JWT等の自己完結型、
Introspectionを用いる参照型Tokenの双方を含む。

### Non-applicability

OAuth Access Tokenを一切受理しない構成では直接対象外になり得る。Token形式がJWTでないことは対象外理由に
ならず、Issuer、Audience／Resource、Expiration、Scopeに相当するPolicyを信頼できる方法で検証する。

## Scope and assumptions

- `Issuer`はToken発行者、`Audience`はTokenを受理してよいResource、`Expiration`は有効期限、
  `Scope`は委任された操作範囲である。
- 許可Issuer、正規Audience／Resource URI、操作別Required Scope、Clock Skew、検証失敗時動作を明示する。
- Key取得やIntrospection先を任意Token Claimだけから無制限に決めない。信頼するIssuer Policyへ拘束する。
- `nbf`、Subject、Tenant等の追加ClaimはSystem上重要になり得るが、AISVS本文が列挙する4 Claimと区別する。

## Assets, actors, identities, and trust boundaries

資産はMCP Tool、Resource、利用者の委任範囲、Tenant Dataである。ActorはAuthorization Server、Client、
MCP Server／Gateway、Resource Owner、攻撃者である。Trust BoundaryはToken発行者→Client、Client→MCP
Resource Server、検証鍵／Introspection→Verifierにある。Enforcement Pointは各RequestのToken Verifierと、
操作別Scopeを評価するDispatch前のPolicy Gateである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | TokenのIssuerが明示的に信頼する発行者と一致し、Issuerに対応する検証方法を使う。 |
| SP-2 | Audience／Resourceが当該MCP Serverを対象とし、別Resource向けTokenを受理しない。 |
| SP-3 | Tokenが評価時点で有効期限内であり、期限切れ・期限欠落を許可しない。 |
| SP-4 | Request対象のTool／Resource／操作に必要なScopeをTokenが満たす。 |
| SP-5 | Claim欠落、不一致、曖昧、鍵・Introspection取得不能時は安全に拒否する。 |

## Scope calibration and adjacent assurance

Claim検証はTokenが意図された発行者・Resource・時間・Scopeに属することを示すが、個別ArgumentやObjectを
利用者が操作してよいことまでは示さない。それはC10.2.5やResource側認可の対象である。Scope名が
`documents:read`でも、Tenant Bの文書を読めるとは限らない。

毎Requestでこの検証を実行することはC10.2.1、Token盗難後のReplay耐性はC10.3.5等の別保証である。

## Threat and failure-mode rationale

攻撃者は自分のIssuerが発行したToken、別Service向けToken、期限切れToken、低Scope Tokenを提示する。
Verifierが署名だけ、またはScope文字列の存在だけを確認すると、Audience Confusion、Issuer Confusion、
Stale Credential、Scope Escalationが成立する。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

許可Issuer、検証鍵／Introspection、Audience／Resource、Clock、Required Scope Map、Claim欠落時動作、
GatewayとServerの責任分界を確認する。Gateway検証後にServerへ渡すIdentity Contextの完全性と、
Serverへの直接Bypass経路も確認する。

### Positive verification

正規Issuer、当該MCP Audience、有効期限、必要最小Scopeを持つ試験Tokenで許可操作が成功することを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 未承認Issuerが正しく署名したToken、またはIssuer Claim欠落 | 拒否する。SP-1, SP-5 |
| N-2 | 別MCP Server／API向けAudience、Audience欠落・曖昧 | 拒否する。SP-2, SP-5 |
| N-3 | 期限切れ、Expiration欠落、許容外Clock差 | 拒否する。SP-3, SP-5 |
| N-4 | 必要Scope欠落、似たScope、広さを誤解しやすいScope | 対象操作を拒否する。SP-4 |
| N-5 | 検証鍵・Introspection・Clockを利用不能にする | 検証省略やAllowへFallbackしない。SP-5 |
| N-6 | Gateway検証を迂回してServerへ直接Request | 同等検証なしに処理しない。SP-1〜SP-5 |

### Failure conditions

署名成功だけで許可する、Issuer／Audienceを文字列部分一致する、期限・Scope欠落をDefault Allowする、
別Resource向けTokenを受理する、または検証基盤障害時に処理する場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Token validation policy | Identity／MCP Owner | Issuer、Audience、Time、Scope | IdP・Resource・Tool変更時 | Revision・承認を保持 | 4 Claimの期待値と失敗動作が明示 |
| Operation-Scope map | Resource Owner | Tool／Resource／Operation | 権限Model変更時 | Policy正本として保護 | 各操作のRequired Scopeを一意に評価可能 |
| Claim Negative test | Test Harness | N-1〜N-6 | Verifier／Gateway変更後 | 模擬Tokenのみ使用 | 各不一致を副作用前に拒否 |
| 検証監査Event | Token Verifier | 許可・拒否Request | 継続 | Token Raw値を保存せずClaim最小化 | Request、Policy Revision、拒否理由を追跡可能 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.2.1` | Claim検証を各Requestで実施する。 |
| `v1.0-C10.2.4` | Scopeに基づき`tools/list`の表示対象を限定する。 |
| `v1.0-C10.2.5` | Scopeに加えてToolと具体的Argumentを認可する。 |
| `v1.0-C10.3.5` | 有効TokenをSenderへ暗号的に拘束する。 |
| `v1.0-C5.1.2` | Agent Tokenの短命・最小Scope・署名という広い保証を扱う。 |

## Known limitations and uncertainty

正しいClaimを持つTokenでも盗難・誤発行・過大Scope・古いBackend権限により危険になり得る。Scope taxonomyは
実装依存であり、AISVS本文だけから適切な粒度を決められない。TokenのValid期間中に権限が取り消された場合の
反映は、Introspection、短命Token、継続的認可等の設計に依存する。

`verifiable`はArtifactの成熟度であり、製品適合、学習完了、全OAuth Flowの安全性を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-02-Authentication-Authorization.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |
