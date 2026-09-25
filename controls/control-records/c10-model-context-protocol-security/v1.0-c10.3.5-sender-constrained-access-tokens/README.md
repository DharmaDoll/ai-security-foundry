---
title: "MCP Access Tokenを送信Clientへ暗号的に拘束する"
versioned_id: "v1.0-C10.3.5"
requirement_id: "C10.3.5"
verification_level: 3
family_id: "C10"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-03-Secure-Transport.md"
last_verified: "2026-09-24"
maturity: "verifiable"
mapping_assessment_refs: []
---

# MCP Access Tokenを送信Clientへ暗号的に拘束する

AISVS Verification Level: 3

## Upstream basis

AISVS `v1.0-C10.3.5`は、MCP ClientとServer間のAccess TokenをmTLSまたはDPoPでSender-constrainedに
することを求める。採用済みstable v1.0の固定Revisionで要件本文とC10.3 Researchを確認した。

Researchは、mTLSのCertificate-bound TokenとDPoPのKey-bound Token、盗難Bearer TokenのReplay、TLS終端Proxy、
DPoP ProofのMethod／URI／Token Hash／Freshness／Replay試験を補足する。方式固有の項目は各RFCに基づく実装例であり、
AISVSが両方式を同時に要求しているとは解釈しない。

## Interpretation

Access Tokenを所持するだけではMCP Serverで利用できないようにし、Token発行時にClientが保持するKeyまたはCertificateへ
Tokenを結び付ける。Resource Serverは各提示時に、Token内のBindingと、Clientがその秘密鍵を現在保有している証明を
同一Requestで検証する。

mTLSでは単にTLS Client Certificateを要求するだけでなく、そのCertificateとTokenのConfirmation情報を一致させる。
DPoPではToken Bindingに加え、RequestごとのProofの署名、HTTP Method、Target URI、Token Hash、Freshness、Replayを
検証する。失敗時に通常のBearer TokenへFallbackしない。

## Security objective

Log、Client Storage、Proxy、Memory、別Hop等からAccess Tokenだけを取得した攻撃者が、別のClientからMCP Serverへ
ReplayしてTool／Resource権限を行使することを防ぐ。

## Applicability

Access Tokenで保護する高AssuranceなMCP Client–Server通信に適用する。AISVS Level 3であり、鍵配布、Client Identity、
Proxy、可用性を含む運用能力が求められる。

### Non-applicability

Access Tokenを一切使わない純粋なLocal stdio構成には直接適用しない。Bearer Tokenを使うが実装コストが高いという理由は
Non-applicabilityではなく、Level 3への未適合または対象Assurance Levelの判断として扱う。

## Scope and assumptions

- mTLSとDPoPのいずれかを選択できるが、Token発行者、Client、Resource Serverが同じBindingをEnd-to-endで維持する。
- Audience制限はTokenの利用先を狭めるが、提示者が正規Clientであることを証明しない。
- 通常のTLSは通信路を保護するが、通信路外で盗まれたBearer TokenのReplayを防がない。
- DPoP Replay Window、Nonce、`jti` Cache、Clock Skew、mTLS Certificate Rotationは明示的に設計する。
- Gatewayで検証を終端する場合、Backendが偽造不能な検証結果を受け取り、Direct Routeを持たないことを確認する。

## Assets, actors, identities, and trust boundaries

資産はAccess Token、Client秘密鍵／Certificate、MCP Tool Authority、User Delegationである。ActorはOAuth Authorization
Server、MCP Client、Gateway、MCP Resource Server、PKI／Key Store、Token窃取者である。Trust BoundaryはToken発行、
Client Key保持、TLS／DPoP Proof提示、GatewayからBackendへの検証結果伝播にある。Enforcement PointはAuthorization
ServerのToken Bindingと、各MCP Requestを受けるResource Server／GatewayのProof-of-possession検証である。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Access Tokenは発行時に特定Client Key／Certificateへ暗号的にBindingされる。 |
| SP-2 | Resource Serverは各RequestでToken Bindingと提示者のKey所持証明を一致検証する。 |
| SP-3 | mTLSではTokenのCertificate Thumbprintと実際のClient Certificateを一致させる。 |
| SP-4 | DPoPでは署名、Key Binding、Method、Target URI、Token Hash、Freshness、Unique IDを検証する。 |
| SP-5 | Token単体、別Key／Certificate、再利用Proof、Bearer SchemeへのDowngradeを拒否する。 |
| SP-6 | Proxy、Replica、Retry、Reconnect、Certificate／Key Rotationを含む全経路でBindingを維持する。 |
| SP-7 | 検証不能・Replay State障害時はTool／Resource副作用前に安全に失敗する。 |

## Scope calibration and adjacent assurance

C10.2.2のIssuer、Audience、Expiration、Scope検証が正しくても、Bearer Tokenを盗んだ別Senderは利用できるため、
本Controlが独立する。C10.3.1のTLSもTokenの通信路外盗難を防げない。Sender ConstraintがPassでも、Token Scopeが
過大、Client自体が侵害、認可Argumentが不正なら別のFailureが残る。

## Threat and failure-mode rationale

攻撃者はAccess TokenをLog、Storage、Crash Dump、Proxy、侵害Client等から取得し、自分のConnectionでReplayする。
Bearer Tokenでは所持が権限になる。Tokenと正規Clientだけが保持するKey／Certificateを結び付け、Request固有の
Proofを要求すれば、Tokenだけの窃取による権限行使を制限できる。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Token発行からMCP Resource ServerまでのBinding Flow、Key／Certificate保管、Authorization Server Metadata、Gateway
Termination、Backend Header、Replay Store、Rotation、Failure Policyを確認する。mTLSまたはDPoPの選択と全Clientの
適用範囲を明示する。

### Positive verification

正規ClientがBindingされたTokenと対応Key／Certificateを用いたときだけ代表MCP Requestが成功し、Token Identifier、
Binding、Proof検証結果をSecretなしで対応付けられることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 正規Tokenを盗み、対応Key／Certificateなしで提示 | 認可前に拒否する。SP-1, SP-2, SP-5 |
| N-2 | mTLS TokenをCertificateなし／別Certificateで提示 | Binding不一致として拒否する。SP-3, SP-5 |
| N-3 | DPoP Proofを別Keyで署名、または`htm`／`htu`／Token Hashを変更 | Proof不一致として拒否する。SP-4, SP-5 |
| N-4 | 同一DPoP Proof／`jti`を再利用、期限外Proofを提示 | Replay／Freshness違反として拒否する。SP-4, SP-5 |
| N-5 | Sender-constrained TokenをBearer Schemeまたは非対応Routeへ送る | Downgradeせず拒否する。SP-5, SP-6 |
| N-6 | TLS終端Proxyへ偽のCertificate／DPoP検証Headerを注入、Backendへ直接接続 | 信頼境界で除去・再生成し、迂回を拒否する。SP-6 |
| N-7 | Replay Store／Key Resolution／Certificate検証をUnavailableにする | AllowへFallbackせず副作用前に失敗する。SP-7 |
| N-8 | Key／Certificate Rotation前後に旧BindingをReplay | 定義したOverlap外では拒否し、新Bindingだけを受理する。SP-6 |

### Failure conditions

TokenにBindingがない、Resource Serverが所持証明を検証しない、mTLS CertificateとTokenを照合しない、DPoP Proofの
Request Binding／Replayを検証しない、または失敗時にBearerへFallbackする場合はFailを裏付ける。Gateway以外の
Direct Routeや全ReplicaでのReplay検出を試験していなければPassの証拠不足とする。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Sender-constraint architecture | Identity／MCP Owner | Issuer、Client、Gateway、Server | 方式・Topology変更時 | Key値を含めずRevisionを保持 | Bindingと各検証点を追跡可能 |
| Issuer／Resource設定 | Authorization・Resource Server | 全Client／Audience | Key・Certificate Policy変更時 | 承認済み設定を保護 | mTLSまたはDPoPをEnd-to-endで強制 |
| Stolen-token／Replay test | Security Test Harness | N-1〜N-8 | Release・Crypto変更後 | 模擬Token／Keyを使用 | Token単体とReplayを副作用前に拒否 |
| Proof validation telemetry | Gateway／Resource Server | 代表正常・拒否Request | 運用中 | Token／Proof／Key Materialを保存しない | Binding結果と拒否理由を監査可能 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.2.1` | Sender-constrained Tokenも各Requestで検証する。 |
| `v1.0-C10.2.2` | TokenのIssuer、Audience、Expiration、Scopeを別途検証する。 |
| `v1.0-C10.2.3` | Binding済みでもToken／User Credentialを永続化しない。 |
| `v1.0-C10.3.1` | DPoPを含むRemote通信をTLS上のStreamable HTTPで行う。 |
| `v1.0-C5.1.2` | Agent Tokenの短命・最小Scope・署名という別のCredential性質を扱う。 |

## Known limitations and uncertainty

正規Clientと秘密鍵が同時に侵害された場合、Sender Constraintだけでは防げない。mTLSはCertificate LifecycleとProxy
Termination、DPoPはProof生成、Clock、Replay State、URI Canonicalizationの運用コストが高い。Availabilityとの
Trade-offを理由に検証をFail-openにしてはならないが、適切な冗長化が必要となる。

`verifiable`はArtifactの成熟度であり、製品適合、Key非侵害、OAuth Flow全体の安全性を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-03-Secure-Transport.md)
- [RFC 8705: OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705)
- [RFC 9449: OAuth 2.0 Demonstrating Proof of Possession](https://www.rfc-editor.org/rfc/rfc9449)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |
