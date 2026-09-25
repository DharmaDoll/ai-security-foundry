---
title: "Tool Responseへ署名・Nonce・Timestampを付けReplayを検出する"
versioned_id: "v1.0-C10.4.6"
requirement_id: "C10.4.6"
verification_level: 2
family_id: "C10"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-04-Schema-Message-Validation.md"
last_verified: "2026-09-24"
maturity: "verifiable"
mapping_assessment_refs: []
---

# Tool Responseへ署名・Nonce・Timestampを付けReplayを検出する

AISVS Verification Level: 2

## Upstream basis

AISVS `v1.0-C10.4.6`は、MCP ServerがTool Responseを一意なNonceとTimestampとともに署名し、ClientがReplay Attemptを
検出できることを求める。固定Revisionの要件本文とC10.4 Researchを確認した。

ResearchはCanonical Payload、Signer、Tool／Request Context、Freshness Window、Nonce Store、Cross-context Swapを試験対象として
補足し、Core MCPの成熟した標準機能ではない点も示す。

## Interpretation

Serverは各Tool Responseについて、CanonicalなResponse内容、一意Nonce、Timestamp、Signer Identity、およびResponseを
元Request／Tool／Principalへ結び付けるContextを署名対象にする。ClientはModelやBusiness Logicへ渡す前に署名、信頼Key、
Freshness、Nonce未使用、Context一致を検証し、検証成功とNonce消費を一体で扱う。

## Security objective

過去に正当だったResponseのReplay、Payload改ざん、別Tool／User／RequestへのResponse差替えにより、古い状態や偽の実行結果を
Clientへ信じさせることを防ぐ。

## Applicability

Tool Responseを返すMCP Serverと、そのResponseを利用するClient／Gatewayに適用する。TLS終端や複数中継がある構成も含む。

### Non-applicability

Tool機能を提供しないServerのみ対象外にできる。TLSがある、同一Process、監査Hashがあるという理由では署名要件を対象外にしない。

## Scope and assumptions

- 署名対象のCanonical Representation、Algorithm、Key ID、Rotation、Trust Anchorを定義する。
- NonceはSigner／Context内で一意とし、Timestampは許容Clock SkewとFreshness Windowを持つ。
- Streaming ResponseではChunk／Aggregateのどこを署名するかを明示し、未検証ChunkをModelへ渡さない。
- Gateway ReceiptやAudit HashはEnd-to-end Response署名と同等とは限らず、代替時はPartial Evidenceとして扱う。

## Assets, actors, identities, and trust boundaries

資産はTool ResultのIntegrity／Freshness、Client判断、後続Actionである。ActorはMCP Server、Client、Gateway、Key Authority、
Replay攻撃者である。Trust BoundaryはServer署名KeyからMessageへ、MessageからClient Verification／Contextへ移る地点にある。
Enforcement PointはServer Response SignerとClientのPre-context Signature／Replay Gateである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 各Tool Responseを信頼されたServer Keyで署名する。 |
| SP-2 | Payload、Nonce、Timestamp、Signer、Tool／Request／Principal Contextを署名へBindingする。 |
| SP-3 | Clientは署名、Key Trust、Context、Freshness、Nonce未使用を利用前に検証する。 |
| SP-4 | Nonce確認と使用済み記録を競合なく一体で行い、再利用を拒否する。 |
| SP-5 | Payload／Context変更、別Signer、期限外、Replay、検証不能をFail-closedにする。 |
| SP-6 | Replica、Concurrent Request、Retry、Streaming、Key Rotationで同じ保証を維持する。 |

## Scope calibration and adjacent assurance

署名は「誰が・何を・いつ返したか」とReplayを扱い、内容の安全性・正確性を保証しない。署名されたPrompt Injectionは
C10.4.2で別途扱う。C9.5.6等のMessage Integrityと重なるが、本ControlはMCP Tool ResponseのNonce／Timestampに焦点を置く。

## Threat and failure-mode rationale

攻撃者または中継点は、過去の成功Responseを再送し、失敗した現在のActionを成功に見せる、別User／ToolのResponseを差し替える、
Payloadを改ざんする。TLSだけでは終端後・Log・Cache由来のApplication-layer Replayを検出できない。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

署名Envelope、Canonicalization、Key配布／Rotation、Nonce生成／Store、Clock Source、Context Binding、Streaming／Gateway経路を確認する。

### Positive verification

正規Responseの署名とContextが検証され、Nonceが一度だけ消費されてからModel／Callerへ渡ることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 同一署名Response／Nonceを再送 | 2回目を利用前に拒否する。SP-3, SP-4 |
| N-2 | Payload、Timestamp、Nonceを1 Byte変更 | 署名不一致として拒否する。SP-1〜SP-3 |
| N-3 | 別Tool／Request／Userへ正規ResponseをSwap | Context Binding不一致で拒否する。SP-2, SP-5 |
| N-4 | Freshness Window外、未来過大Timestampを提示 | 拒否する。SP-3, SP-5 |
| N-5 | 同一NonceをConcurrent／別Replicaで競合利用 | 一つだけ受理し再利用を拒否する。SP-4, SP-6 |
| N-6 | Unknown／Revoked Key、Replay Store障害、Streaming未署名Chunkを使う | Model／副作用へFail-openしない。SP-5, SP-6 |

### Failure conditions

署名がない、Nonce／Timestamp／Contextが署名範囲外、Clientが利用後に検証、Nonce CheckとRecordが分離して競合可能、または
検証不能時にUnsigned ResponseへFallbackする場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Signing／Trust architecture | Crypto・MCP Owner | ServerからClientまで | Algorithm／Key変更時 | Key Materialを含めずRevision保持 | Signed FieldとTrust Anchorを特定可能 |
| Nonce／Freshness Policy | Client／Platform Owner | Replica・Region・Stream | Store／Clock変更時 | 承認済み設定を保持 | Atomic ConsumeとWindowを説明可能 |
| Tamper／Replay test | Test Harness | N-1〜N-6 | Release・Crypto変更後 | Test Keyを使用 | 利用前に全不正Responseを拒否 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.4.1` | 署名検証後もResponse構造をSchema検証する。 |
| `v1.0-C10.4.2` | 正しく署名された悪意ある内容をInjection観点で検査する。 |
| `v1.0-C9.5.6` | Agent MessageのIntegrity／Authenticity／Replayという広い保証を扱う。 |

## Known limitations and uncertainty

AISVSはAlgorithm、Canonicalization、Key Distribution、Streaming方式を規定せず、相互運用性と運用コストが大きい。Server Keyが
侵害されれば悪意あるResponseも正当に署名できる。Clock／Nonce Store障害への可用性設計も必要である。

`verifiable`はArtifactの成熟度であり、Response内容の真実性や製品適合を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-04-Schema-Message-Validation.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
