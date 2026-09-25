---
title: "HTTP MCPでOriginとHostを独立に検証する"
versioned_id: "v1.0-C10.3.3"
requirement_id: "C10.3.3"
verification_level: 2
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

# HTTP MCPでOriginとHostを独立に検証する

AISVS Verification Level: 2

## Upstream basis

AISVS `v1.0-C10.3.3`は、DNS Rebinding攻撃を防ぐため、すべてのHTTP-based MCP Transportで
Origin HeaderとHost Headerの双方を独立に検証することを求める。採用済みstable v1.0の固定Revisionで
要件本文とC10.3 Researchを確認した。

Researchは、OriginとHostの片方だけを検証する失敗、Loopback Server、Reverse ProxyでのHeader書換え、
欠落・重複・IPv4／IPv6等の試験を補足する。以下のCanonicalizationと欠落時PolicyはRepository interpretationである。

## Interpretation

HTTP RequestをMCP処理へ渡す前に、要求元を表すOriginと要求先を表すHostを、それぞれ別のAllow Policyで検証する。
片方の成功から他方の信頼を推論せず、許可された組合せだけを受理する。CORS設定、Loopback Bind、TLS、Caller認証は
重要だが、二つのHeader検証を代替しない。

ProxyがHeaderを終端・再構成する場合、どのHopの値をAuthoritativeとするかを定義し、外部Callerが内部用Headerを
注入できないようにする。Originが存在しない非Browser Clientの扱いも明示し、欠落を暗黙の信頼として扱わない。

## Security objective

攻撃者のWeb Originから、DNS RebindingやHeader混同を用いてVictimのLoopback／Private MCP Serverへ到達し、
Victimの権限でToolやResourceを操作することを防ぐ。

## Applicability

Streamable HTTP、Legacy HTTP／SSE、Loopback HTTP、Gateway配下等、HTTPを使うすべてのMCP Endpointに適用する。
Browserから直接利用する設計でなくても、Victim Browserが到達可能なら対象となる。

### Non-applicability

HTTP Endpointを一切持たない純粋なLocal stdio構成は直接対象外にできる。Private Network、Loopback、認証必須、
CORS無効という理由だけではHTTP Endpointを対象外にしない。

## Scope and assumptions

- OriginはRequest InitiatorのWeb Origin、HostはRequest Targetを表し、同じ値・同じ保証ではない。
- 許可値はScheme、Hostname、Port、IPv4／IPv6表記をCanonicalizeした上で完全一致または明示Policyで評価する。
- HTTP VersionやGatewayによりRequest Targetが`:authority`等で表現される場合も、最終的なAuthorityをHost Policyで評価する。
- Origin欠落を許容するClient Classがある場合、Route、Authentication、Content Type等でBrowser Requestと区別し、
  設計判断と試験を残す。欠落を一律許可するだけでは独立検証の証拠にならない。
- Forwarded Headerを信頼できるProxyのIdentityとHop数を固定する。

## Assets, actors, identities, and trust boundaries

資産はLocal／Private MCP Tool、Resource、User Credential、Host権限である。ActorはBrowser User、悪意あるWeb Site、
DNS／Network攻撃者、MCP Client、Proxy、MCP Serverである。Trust BoundaryはBrowser／NetworkからHTTP Edgeへ、
ProxyからApplicationへ入る地点にある。Enforcement Pointは最初の信頼HTTP Edgeと、Bypass不能なServer側Request Gateである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | すべてのHTTP MCP RequestでCanonical Hostを明示Allow Policyと照合する。 |
| SP-2 | OriginをHostとは独立した明示Policyで検証し、未許可Originを拒否する。 |
| SP-3 | Hostが許可でもOrigin不許可、Originが許可でもHost不許可なら拒否する。 |
| SP-4 | 欠落、重複、競合、Malformed、Encoding差、Port・IPv4・IPv6表記をFail-safeに扱う。 |
| SP-5 | Proxy／Gateway経路で外部入力と信頼Headerを分離し、直接接続や代替Routeで迂回させない。 |
| SP-6 | Header検証失敗時はMCP Parse、Credential利用、Tool／Resource Dispatch前に拒否する。 |

## Scope calibration and adjacent assurance

C10.3.1のTLSとAuthenticationがPassでも、Victim Browserが正規TLS Endpointへ送るDNS Rebinding Requestは成立し得る。
C10.2のCaller認証、CSRF対策、Content-Type制約はDefense in Depthだが、本ControlのHost／Origin二重Gateを代替しない。
逆に本Controlは、許可Origin自体の侵害や正規Client Credentialの悪用を防がない。

## Threat and failure-mode rationale

攻撃者は自分のDomainをVictimの`127.0.0.1`やPrivate Addressへ再解決し、BrowserにLocal MCP EndpointへRequestを
送らせる。ServerがHostまたはOriginの片方しか検証しない、Proxyの値を誤って信頼する、表記差でAllowlistを
迂回できる場合、Local ToolがCross-originに操作され得る。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

全HTTP Listener、Route、Proxy Hop、Direct Backend到達性、Host／Origin Allowlist、Canonicalization、欠落時Policy、
Forwarded Header Trustを確認する。ApplicationとEdgeのどちらが最終拒否責任を持つか明示する。

### Positive verification

許可されたHostとOriginの組合せで正規Requestが成功し、双方の判定結果を同一Requestへ対応付けられることを示す。
明示的に許可した非Browser Client経路は、その識別条件と代替保護も確認する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 許可Host＋未許可Origin | Dispatch前に拒否する。SP-2, SP-3, SP-6 |
| N-2 | 未許可Host＋許可Origin | Dispatch前に拒否する。SP-1, SP-3, SP-6 |
| N-3 | 未許可Host＋未許可OriginでBrowser DNS Rebindingを再現 | Local／Private Toolへ到達しない。SP-1〜SP-3 |
| N-4 | Origin／Host／`:authority`の欠落、重複、競合、Case、Trailing dot、Port、IPv6差を送る | Canonical Policy外を安全に拒否する。SP-4 |
| N-5 | `X-Forwarded-Host`等を外部から注入し、信頼Proxyを迂回 | 外部値をAuthoritativeとせず拒否する。SP-5 |
| N-6 | Backendへ直接接続、別Transport Route、Proxy設定差でN-1／N-2を再実行 | 同じ二重Gateで拒否する。SP-5, SP-6 |

### Failure conditions

OriginかHostの一方しか評価しない、片方の成功で両方を許可する、Wildcard／Substring Matchで未許可値を通す、
Proxy Bypassがある、または拒否前にMCP副作用が起きる場合はFailを裏付ける。欠落時Policyと全HTTP Routeの
証拠がなければPassの根拠不足とする。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Header Trust／Allow Policy | Edge・MCP Owner | 全HTTP Transport・Proxy | DNS／Route／Proxy変更時 | Revision・承認を保持 | HostとOriginの独立Policyを説明可能 |
| Route／Proxy Data Flow | Platform Owner | External EdgeからBackendまで | Topology変更時 | 信頼Hopを明示 | Direct Routeを含めGateを迂回不能 |
| DNS Rebinding／Header test | Security Test Harness | N-1〜N-6 | Release・HTTP Stack変更後 | 試験Domainと模擬Dataを使用 | MCP Dispatch前に一貫して拒否 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.2.1` | Header検証とは別に各RequestのTokenを検証する。 |
| `v1.0-C10.3.1` | Remote HTTPの暗号化・Endpoint／Caller認証を扱う。 |
| `v1.0-C10.3.2` | Local stdioはHTTP Headerを使わず、Local実行境界で制約する。 |
| `v1.0-C10.4.3` | MCP Function CallのParameter制限であり、HTTP Request Targetの検証とは異なる。 |

## Known limitations and uncertainty

正規OriginのXSS／侵害、Browser以外のClient Credential窃取、許可Host上のSSRFは本Controlだけでは防げない。
Proxy製品ごとにHost／Forwarded Headerの挙動が異なり、欠落Originを許容すべきClient ClassもDeployment依存である。

`verifiable`はArtifactの成熟度であり、製品適合やDNS／Browser攻撃の完全防止を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-03-Secure-Transport.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |
