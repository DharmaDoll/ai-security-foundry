---
title: "Remote MCPに認証済み・暗号化済みStreamable HTTPを使う"
versioned_id: "v1.0-C10.3.1"
requirement_id: "C10.3.1"
verification_level: 1
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

# Remote MCPに認証済み・暗号化済みStreamable HTTPを使う

AISVS Verification Level: 1

## Upstream basis

AISVS `v1.0-C10.3.1`は、Remote ServiceのMCP Transportに認証済み・暗号化済みの
Streamable HTTPを使用することを求める。採用済みstable v1.0の固定Revisionで要件本文と
C10.3 Researchを確認した。

Researchは、Remote EndpointのTLS、証明書検証、Request認証、Legacy SSE、Redirect、Proxy境界を
検証対象として補足する。以下の経路InventoryとFail条件はRepository interpretationである。

## Interpretation

Network越しに利用するMCP ServiceはStreamable HTTPを使用し、Clientから実際のMCP Serverまでの
通信路を暗号化するとともに、通信相手とCallerを認証する。TLSはServer Endpointを認証し通信内容を
保護するが、Callerの権限を証明しない。Access Token等のMCP Request認証も別に必要である。

平文区間、暗号化を失うRedirect、証明書検証の無効化、認証されない代替Endpointを許容しない。
GatewayでTLSを終端する場合、Gateway以降のHopも同じ資産を運ぶTransportとして評価する。

## Security objective

Remote MCPのTool Argument、Response、Credential、Session情報が盗聴・改ざんされること、および
未認証のNetwork PeerがMCP操作へ到達することを防ぐ。

## Applicability

別Host、Container、VM、Cluster、Cloud Service、Gateway等へNetwork越しに接続するすべての
Remote MCP Endpointに適用する。Internet公開かPrivate Networkかを問わない。

### Non-applicability

親子Process間のLocal stdioだけで通信し、Network Transportを一切公開・中継しない構成は直接対象外に
できる。その構成はC10.3.2とC10.1.3で別途評価する。Loopback HTTPはstdioではなくHTTP Transportなので、
「localhost」という理由だけでは対象外にしない。

## Scope and assumptions

- 「暗号化」はTLSを使うことだけでなく、信頼Anchor、Hostname、有効期限等を検証することを含む。
- 「認証済み」はServer認証とCaller認証の双方を含み、後者の詳細はC10.2.1／C10.2.2で扱う。
- Reverse ProxyやService Meshがある場合、外部HopだけでなくMCP Dataが通る全Hopを確認する。
- Legacy SSEや独自Transportの存在は、Remote経路をStreamable HTTPとする要件の代替にならない。

## Assets, actors, identities, and trust boundaries

資産はMCP Message、Tool Argument／Response、Access Token、Session情報、Tool Authorityである。Actorは
MCP Client、Gateway／Proxy、MCP Server、TLS／Identity基盤、Network攻撃者である。Trust Boundaryは
各Network Hopと、TransportからMCP Dispatcherへ入る地点にある。Enforcement PointはClientのTLS検証、
Gateway／ServerのTLS設定、全保護RouteのRequest認証である。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Remote MCPはStreamable HTTPを使用し、平文HTTPやRemote stdioへFallbackしない。 |
| SP-2 | MCP Dataを運ぶ各Network Hopを暗号化し、Server証明書の信頼性と接続先名を検証する。 |
| SP-3 | 各Remote Requestを認証し、TLS確立や既存ConnectionだけをCaller認証の代替にしない。 |
| SP-4 | 無効な証明書、認証失敗、暗号化を失うRedirect／Fallback時にCredentialやMCP Messageを送信しない。 |
| SP-5 | 初期化、再接続、Resume、Streaming、代替Routeを含む全Remote経路で同じTransport Policyを強制する。 |

## Scope calibration and adjacent assurance

C10.2.1は各RequestのAccess Token検証、C10.3.3はHTTPのOrigin／Host検証を扱う。それらが正しくても
平文通信なら本ControlはFailであり、本ControlがPassでもTool・Argument認可までは保証しない。
TLS終端Gatewayの存在だけでは、内部HopとMCP Endpointの認証を自動的に保証しない。

## Threat and failure-mode rationale

Network攻撃者または侵害された中継点は、平文・証明書未検証・不正Redirect・認証漏れEndpointを利用して、
CredentialやTool Dataを取得・変更し、ClientまたはServerになりすます。Private Networkでも誤Route、
侵害Workload、内部者により同じ失敗が成立し得る。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Remote MCP Endpoint、DNS名、Redirect、Load Balancer、Gateway、Service Mesh、Serverまでの全Hopと、
Streamable HTTP／Legacy Transport設定を列挙する。TLS Termination、再暗号化、Certificate Validation、
Authentication Middlewareが実際のDispatcher前にあることを追跡する。

### Positive verification

信頼済み証明書と有効な最小権限Credentialで`initialize`、代表的なDiscovery、Tool呼出しが
Streamable HTTP上で成功し、各Hopの暗号化とRequest認証を観測できることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Remote Endpointへ平文HTTP、Remote stdio、Legacy-only Routeで接続 | 接続・Fallbackを拒否する。SP-1, SP-5 |
| N-2 | 期限切れ、未信頼、Hostname不一致の証明書を提示 | Credential送信前に接続を拒否する。SP-2, SP-4 |
| N-3 | HTTPSからHTTPまたは未許可HostへのRedirectを返す | 自動追従せずCredential／Messageを送らない。SP-4 |
| N-4 | TLSは正常だがCredentialなし・無効で各MCP Requestを送る | Dispatcher前に拒否し副作用を起こさない。SP-3 |
| N-5 | Reconnect、Resume、別Replica、代替PathでN-1／N-4を再実行 | 同じPolicyで拒否する。SP-5 |
| N-6 | Gateway外側だけTLSとし、内側Hopを盗聴可能にする | End-to-end Data Flowの証拠不足または平文HopとしてFailを裏付ける。SP-2 |

### Failure conditions

Remote経路が平文・Legacy-only・Remote stdioである、証明書検証を無効化する、認証なしRouteがある、
または失敗時にCredential／Messageを送る場合はFailを裏付ける。Network Flowや全EndpointのInventoryが
ない場合はPassの証拠不足とする。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Transport Data Flow | Platform／MCP Owner | ClientからServerまでの全Hop | Topology変更時 | Revisionを保持し秘密を含めない | Streamable HTTP、暗号化、認証点を特定可能 |
| TLS／Endpoint設定 | Gateway／Server Owner | 全Remote Endpoint | 証明書・設定変更時 | 承認済み設定と有効期間を保持 | 平文・不正証明書・Downgradeを拒否 |
| Transport Negative test | Test Harness | N-1〜N-6 | Release・Transport変更後 | 模擬証明書・Tokenを使用 | Credential送信・Tool副作用前に拒否 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.2.1` | Transport Securityだけに依存せず各RequestのTokenを検証する。 |
| `v1.0-C10.2.2` | Remote Requestで提示されたTokenのClaimを検証する。 |
| `v1.0-C10.3.2` | Local stdioを許可できる環境境界を扱う。 |
| `v1.0-C10.3.3` | HTTP TransportのOriginとHostを独立に検証する。 |

## Known limitations and uncertainty

暗号化・認証済みTransportでも、正規Client、MCP Server、Gateway自体の侵害や、許可範囲内の有害操作は
防げない。TLS終端やService Meshの信頼設計は環境依存であり、経路の論理的な「end-to-end」を具体化する
必要がある。

`verifiable`はArtifactの成熟度であり、製品適合や未知のTransport Bypass不存在を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-03-Secure-Transport.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |
