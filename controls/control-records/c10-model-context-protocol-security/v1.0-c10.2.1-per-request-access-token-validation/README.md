---
title: "MCPの各RequestでAccess Tokenを検証する"
versioned_id: "v1.0-C10.2.1"
requirement_id: "C10.2.1"
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

# MCPの各RequestでAccess Tokenを検証する

AISVS Verification Level: 1

## Upstream basis

AISVS `v1.0-C10.2.1`は、MCP ServerがRequestごとにAccess Tokenを検証し、Transport Security
だけへ依存しないことを求める。採用済みstable v1.0の固定Revisionで要件本文とC10.2 Researchを
確認した。Researchの事件、統計、製品例を適合根拠としてそのまま採用しない。

Researchは、初回接続、TLS、Localhost、Reverse Proxy、Session ID等を後続Requestの認証として
扱う失敗を補足する。以下のEndpoint範囲と試験条件はRepository interpretationである。

## Interpretation

Access Tokenを使用するMCP Transportでは、`initialize`に成功したことや同じConnection／Sessionから
届いたことを認証の代わりにしない。`tools/list`、`tools/call`、`resources/read`等、保護対象へ
到達する各RequestでTokenの存在と有効性を検証し、失敗したRequestをTool dispatchやData取得前に拒否する。

TLSは通信相手と通信路を保護し得るが、「このRequestをどのPrincipalの権限として処理してよいか」を
Requestごとに証明しない。Session IDもRouting・状態対応の識別子であり、Bearer Credentialへ昇格させない。

## Security objective

認証済みConnection、Session ID、Local Network、Proxy通過等だけを利用して、TokenのないRequestや
別PrincipalのRequestがTool・Resourceへ到達することを防ぐ。

## Applicability

Access Tokenで保護するHTTP、Streaming、Gateway-backed等のMCP Server Endpointに適用する。
Reconnect、Resume、Retry、Long-lived StreamのControl Request、複数Replicaを含む。

### Non-applicability

Access Tokenを利用しないLocal stdio専用構成では、このToken検証要件の直接の評価対象がない場合がある。
ただし、stdioを選んだ事実だけでCaller認証、Process権限、Local Server隔離を保証したことにはならない。
一つでもTokenを受理するHTTP／Gateway経路があれば、その経路には適用する。

## Scope and assumptions

- 「各Request」は、保護対象の操作、Data、Session状態へ到達できる全MCP Requestを指す。
- TokenのIssuer、Audience、Expiration、Scopeという個別Claimの正しさはC10.2.2で深める。
- 認証Middlewareの存在ではなく、全RouteでTool／Resource処理より前に実行されることを確認する。
- 無効TokenへのHTTP StatusやChallengeの詳細は採用Protocolに従うが、失敗時に副作用を起こさないことを
  本Controlの中心とする。

## Assets, actors, identities, and trust boundaries

資産はMCP Tool、Resource、Session Data、下流権限である。ActorはClient Principal、MCP Client、
MCP Server、Gateway／Proxy、Session Store、攻撃者である。Trust Boundaryは各RequestがTransportから
ServerのTool／Resource Dispatcherへ入る地点にある。決定論的なEnforcement Pointは全保護Routeに
適用されるToken検証MiddlewareまたはGatewayと、Bypass不能なServer側Dispatch Gateである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 保護対象へ到達する各Requestで、処理前にAccess Tokenを検証する。 |
| SP-2 | Token欠落・不正・検証不能なRequestを、Tool実行・Data返却・状態変更なしで拒否する。 |
| SP-3 | Connection、TLS、Session ID、Localhost、Proxy Header、過去の認証成功をToken検証の代替にしない。 |
| SP-4 | Reconnect、Resume、Retry、Streaming、Replica、代替Routeを含む全経路で検証を迂回できない。 |

## Scope calibration and adjacent assurance

毎RequestでToken検証を呼んでも、Issuer、Audience、Expiration、ScopeのPolicyが誤っていればC10.2.2の
Failureが残る。正しいTokenでもTool・引数の認可を行わなければC10.2.5を満たさない。
Transport暗号化、Origin／Host検証は重要だがC10.3の別保証である。

## Threat and failure-mode rationale

攻撃者は有効なSession ID、既存Connection、Localhost到達性、Reverse Proxy経路を利用し、Tokenを省略・
置換したRequestを送る。初回だけ認証する設計では、Session Hijack、再接続、保護漏れRouteから、別主体の
権限でTool InvocationやData取得が成立し得る。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

全MCP Route、Transport Adapter、Gateway、Streaming／Resume Endpointを列挙し、Token検証とDispatcherの
順序を追う。Authentication Exclusion、Health／Debug Route、Internal／Loopback Routeが保護対象へ到達
しないか確認する。

### Positive verification

各代表Endpointへ有効な試験Tokenを付けて正常操作が成功し、Requestごとの検証Eventが同じRequest IDと
Principalへ対応することを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Tokenなしで各保護Endpointを呼ぶ | Dispatch前に拒否し、Data・副作用がない。SP-1, SP-2 |
| N-2 | 破損・署名不正・検証不能なTokenを送る | 安全に拒否する。SP-2 |
| N-3 | 有効TokenでSession開始後、Tokenを省略または別Tokenへ置換 | Session IDやConnectionを理由に通さず、当該Requestを検証・拒否する。SP-1, SP-3 |
| N-4 | Reconnect、Resume、Retry、別Replica、代替RouteからN-1を再実行 | すべての経路で同じ結果になる。SP-4 |
| N-5 | TLS・Localhost・信頼Proxy経由でTokenなしRequestを送る | Transport上の信頼だけで許可しない。SP-3 |

### Failure conditions

初回だけTokenを検証する、Session IDを認証情報として扱う、保護Routeの一つがMiddlewareを迂回する、
または拒否したRequestでTool／Data副作用が起きる場合はFailを裏付ける。試験未実施やRoute Inventory
不足はPassの証拠不足として扱う。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Route・認証Flow | MCP／Gateway Owner | 全Transport・Endpoint | Route／SDK／Proxy変更時 | Revisionを保持しSecretを含めない | 全保護RouteがDispatch前の検証を通る |
| Request単位検証結果 | Auth Middleware／Gateway | 正常・拒否Request | Deploy後の代表期間、試験時 | Token値を保存せずRequest・Principal・結果を保護 | 各Requestと検証結果を対応可能 |
| Bypass Negative test | Test Harness | N-1〜N-5 | Route・Session機構変更後 | 模擬Tokenと試験IDを使用 | 全経路で副作用前に拒否 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.2.2` | 各Requestで検証するTokenのIssuer、Audience、Expiration、Scopeを定める。 |
| `v1.0-C10.2.5` | 認証済みRequestでも、Toolと具体的引数を認可する。 |
| `v1.0-C10.2.6` | Session終了後の状態・識別子・Artifactを除去する。 |
| `v1.0-C10.3.1` | Remote MCP通信の暗号化・認証Transport。Transport Securityだけでは本Controlを満たさない。 |

## Known limitations and uncertainty

Token検証Service、鍵配布、Introspection、Cacheが誤設定・侵害されれば無効Tokenを受理し得る。本Controlは
RequestごとのMediationを保証するもので、Token発行、Client登録、Authorization Grant全体の安全性を
単独では保証しない。

`verifiable`はArtifactの成熟度であり、製品適合、学習完了、未知のBypass不存在を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-02-Authentication-Authorization.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |
