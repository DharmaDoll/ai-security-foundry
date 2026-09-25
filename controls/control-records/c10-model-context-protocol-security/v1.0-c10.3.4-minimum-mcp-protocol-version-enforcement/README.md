---
title: "MCP Clientが最低Protocol Versionを強制する"
versioned_id: "v1.0-C10.3.4"
requirement_id: "C10.3.4"
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

# MCP Clientが最低Protocol Versionを強制する

AISVS Verification Level: 2

## Upstream basis

AISVS `v1.0-C10.3.4`は、MCP Clientが許容可能な最低Protocol Versionを強制し、そのVersionを下回る
`initialize` Responseを拒否することを求める。採用済みstable v1.0の固定Revisionで要件本文と
C10.3 Researchを確認した。

Researchは、Clientが技術的には理解できる旧VersionでもSecurity Baseline未満なら拒否すること、Gatewayや
Compatibility Adapterの自動Fallback、日付文字列の単純比較を検証上の注意として補足する。

## Interpretation

MCP Clientは、組織または製品が許可するProtocol Version集合と最低Versionを明示し、Serverが初期化応答で
Baseline未満を提案した場合、運用Requestを一つも送らず接続を終了する。「実装が旧VersionをSupportする」ことと
「そのDeploymentで旧Versionを許可する」ことを分ける。

Versionは既知のProtocol Identifierとして比較し、任意の日付文字列を新しいという理由だけで信頼しない。
Gateway、SDK、Retry、Legacy Adapterも同じFloorを維持する。

## Security objective

悪意ある・侵害・旧式Serverまたは中継点がProtocol Negotiationを下げ、廃止済みのTransport、Authentication、
Session、Message処理へClientをFallbackさせるDowngradeを防ぐ。

## Applicability

Remote／Localを問わず、MCP Protocol VersionをNegotiationするClient、Host、Gateway、Adapterに適用する。
複数Versionを実装するClientでは特に重要である。

### Non-applicability

Protocol Negotiationを行わず、単一の固定Versionしか実装・送受信できない構成でも、そのVersionが承認Baselineで
固定され、異なるVersionのResponseを拒否する証拠が必要である。「旧Versionしか対応しない」は対象外理由ではない。

## Scope and assumptions

- 最低Versionの値自体はRisk、必要機能、脆弱性、互換性を踏まえOwnerが決定し、変更管理する。
- 比較は実装が認識するVersion順序またはAllowlistで行い、文字列・日付の大小だけに依存しない。
- Baseline未満拒否は本Controlの中心であり、未知・Malformed・将来Versionの扱いもFail-safeに定義する。
- Negotiation前に送る必要がある最小Message以外、Credential、Tool List、Resource Dataを露出しない。

## Assets, actors, identities, and trust boundaries

資産はClientのSecurity Baseline、Credential、Tool／Resource Metadata、後続Sessionである。ActorはMCP Client、
MCP Server、Gateway／Adapter、Policy Owner、攻撃者である。Trust BoundaryはServerの`initialize` Responseから
Clientの接続状態へ移る地点にある。Enforcement PointはClientのVersion Negotiation State Machineと全Fallback経路である。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Clientは承認済み最低Protocol Versionと許可Version集合を明示的に持つ。 |
| SP-2 | Server提案Versionを既知Identifierとして解析し、Baseline未満を必ず拒否する。 |
| SP-3 | 拒否後はInitialized状態へ遷移せず、Credential、Discovery、Tool／Resource Requestを送らない。 |
| SP-4 | Gateway、Retry、Reconnect、Compatibility AdapterがFloor未満へ自動Fallbackしない。 |
| SP-5 | 欠落・Malformed・Unknown・競合Versionは明示Policyに従い、安全でない推定をしない。 |
| SP-6 | Version Floor変更はOwner、根拠、影響、Rollback条件を伴う変更管理下に置く。 |

## Scope calibration and adjacent assurance

Version Floorは既知の旧ProtocolへのDowngradeを制限するが、許可Versionの実装脆弱性や悪意あるServerを無害化しない。
C10.3.1のTransport暗号化、C10.1.2のServer Admission、C10.4のMessage検証は別途必要である。

## Threat and failure-mode rationale

Serverまたは中継点はClientがSupportする古いVersionを選び、より弱いTransport／認証／Session Semanticsを使用させる。
Clientが「理解できるから」と受理したり、接続失敗時にLegacy RouteへRetryしたりすると、管理者のSecurity Baselineを
迂回できる。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

ClientのSupported Version、Minimum Version、Negotiation State Machine、Fallback、Gateway／SDK設定、Policy変更経路を
確認する。Version比較が列挙済みIdentifierか、単純文字列比較かを検査する。

### Positive verification

最低Versionとそれより新しい承認済みVersionのServer Responseが正常にNegotiationされ、以後のMessageで同じVersionを
使用することを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | ServerがSupport済みだがFloor未満のVersionを返す | 接続を終了し、Operational Requestを送らない。SP-1〜SP-3 |
| N-2 | Connection失敗後にGateway／AdapterがN-1のVersionで再試行 | Legacy Fallbackせず拒否を維持する。SP-4 |
| N-3 | Versionを欠落、Malformed、Unknown Future値、競合Header／Body値にする | 明示Policyで拒否または安全に処理し、任意日付を自動受理しない。SP-5 |
| N-4 | Negotiation後のRequestで別Versionを提示・注入 | Negotiated Versionとの不一致を拒否する。SP-2, SP-4 |
| N-5 | Floor設定を無権限Userが引き下げる | 変更を拒否し監査可能にする。SP-6 |
| N-6 | Floor未満拒否後にCredential／`tools/list`が送られるか観測 | 一切送信されない。SP-3 |

### Failure conditions

Baseline未満を受理する、旧Versionへ自動Fallbackする、Floorが未定義・無権限変更可能である、または拒否後に
CredentialやOperational Messageを送る場合はFailを裏付ける。Client以外のAdapter経路を試験していなければ
Passの証拠不足とする。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Version Baseline／根拠 | Protocol・Security Owner | Client群・Deployment | Baseline変更時 | 承認・Revisionを保持 | Floor、許可集合、例外を特定可能 |
| Negotiation／Fallback設計 | Client／Gateway Owner | 全Connection経路 | SDK・Adapter変更時 | Revisionを保持 | Floor未満へ遷移するPathがない |
| Downgrade Negative test | Test Harness | N-1〜N-6 | Release・Version追加時 | 模擬Serverを使用 | Operational Message前に拒否 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.1.2` | 許可されたServerかを判定する。許可ServerでもVersion Floorは必要。 |
| `v1.0-C10.3.1` | 許可VersionでRemote Transportを暗号化・認証する。 |
| `v1.0-C10.4.1` | Negotiation後のResponseをSchema検証する。 |

## Known limitations and uncertainty

AISVSは具体的なMinimum Versionを規定せず、環境ごとの判断が必要である。Version番号はSecurity Strengthの完全な
順序ではなく、新Versionにも脆弱性や互換性問題があり得る。緊急例外でFloorを下げる場合、期間・範囲・補完策を
別途管理する必要がある。

`verifiable`はArtifactの成熟度であり、許可Versionの安全性や製品適合を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-03-Secure-Transport.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |
