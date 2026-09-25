---
title: "すべてのMCP TransportでPayload Size上限を強制する"
versioned_id: "v1.0-C10.4.5"
requirement_id: "C10.4.5"
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

# すべてのMCP TransportでPayload Size上限を強制する

AISVS Verification Level: 2

## Upstream basis

AISVS `v1.0-C10.4.5`は、すべてのMCP Transportが最大Payload Sizeを強制することを求める。
固定Revisionの要件本文とC10.4 Researchを確認した。ResearchはOversized／Chunked Body、Malformed／Truncated Frame、
stdio、Streamable HTTP、SSE、ProxyとServer Limit差を検証対象として補足する。

## Interpretation

有効な各Transportと方向ごとに、単一Message／Frame／Bodyおよび必要な累積単位の最大Sizeを定義し、可能な限り
全量BufferingやJSON Parseより前にByte Countで強制する。Gateway Limitだけに依存せず、最終Client／Server Read Loopも
上限を持つ。Chunking、Compression、Streaming、Retryで上限を迂回させない。

## Security objective

巨大・終端しない・分割されたPayloadによるMemory／CPU／Connection枯渇、Parser Desynchronization、部分Message処理を防ぐ。

## Applicability

Streamable HTTP、stdio、SSE互換経路、Gateway／Proxy、Client／Server等、Payloadを送受信するすべての有効MCP Transportに適用する。

### Non-applicability

特定Transportを無効化している場合、そのTransportの試験は対象外にできる。ただし有効Transportに上限が不要となる構成はない。

## Scope and assumptions

- Limitの単位、方向、Message／Frame／Stream／Decompressed Sizeを明示する。
- Proxy、Gateway、SDK、ApplicationのLimitを整合させ、外側だけでなく内側も守る。
- Oversize拒否後に残りを読み続けたり、部分PayloadをDispatchしたりしない。
- Payload SizeはC9.1の実行時間・回数・累積Budgetを代替しない。

## Assets, actors, identities, and trust boundaries

資産はMemory、CPU、Connection、Parser State、Service Availabilityである。ActorはMCP Client、Server、Gateway、Proxy、
攻撃者である。Trust BoundaryはTransport Read LoopからParser／Dispatcherへ入る地点にある。Enforcement Pointは各Hopの
Body／Frame ReaderとApplication Parser前のSize Gateである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 全有効Transport／方向へ明示的な最大Payload Sizeを設定する。 |
| SP-2 | Limitを全量Buffering、Decompression、JSON Parse、Dispatchより前または同時にBoundedに強制する。 |
| SP-3 | Chunking、Compression、Streaming、Frame分割、Retryで総量制限を迂回させない。 |
| SP-4 | Gateway、Proxy、SDK、ApplicationのLimit差が内部Componentを露出させない。 |
| SP-5 | Oversize／Malformed／Truncated Inputを副作用なく拒否し、Connection／Parserを安全な状態へ戻す。 |
| SP-6 | Size Limit自体の変更を負荷試験・資産要件と結び付けて管理する。 |

## Scope calibration and adjacent assurance

C10.4.3はFunction Parameter単位のSize、C10.4.5はTransport Payload全体を扱う。小さいPayloadの大量送信、長時間Tool、
高価な正規RequestはC9.1のRate／Budget等が必要である。

## Threat and failure-mode rationale

攻撃者は巨大Body、Chunked Stream、Compression Bomb、深いJSON、終端しないstdio Line等を送信し、Limit判定前のBufferingや
Parseで資源を枯渇させる。Proxyだけが制限してもDirect Backendや内部HopでBypassできる。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

全Transport／Hop、Limit、Buffering、Compression、Parser、Timeout、Backpressure、Direct Routeを列挙し、実際のRead Loopでの
Enforcement順序を確認する。

### Positive verification

上限直下の正規Messageが各Transportで処理され、通常のStreaming／Backpressureが機能することを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 上限超過Body／stdio Message／Frameを送る | Parse／Dispatch前にBoundedに拒否する。SP-1, SP-2 |
| N-2 | Chunkを分割し累積で上限を超える | 累積Sizeで拒否する。SP-3 |
| N-3 | 圧縮後は小さいが展開後に上限超過するPayloadを送る | Decompressed Limitで拒否する。SP-2, SP-3 |
| N-4 | Malformed、Invalid UTF-8、Truncated／Unterminated Messageを送る | 部分Dispatchせず接続を安全に処理する。SP-5 |
| N-5 | Proxy Limitを迂回しBackend直通、または内側Limit差を突く | 内部Gateでも拒否する。SP-4 |
| N-6 | Oversize Requestを並列送信 | Memory／Connection使用が定義範囲内に留まる。SP-2, SP-5 |

### Failure conditions

Limitが一つでも未定義、全量Buffering後にのみ判定、Chunk／CompressionでBypass、GatewayのみでBackend未防御、または
Oversizeの一部がDispatchされる場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Transport Limit matrix | Platform／MCP Owner | 全Hop・方向・Transport | Topology／Limit変更時 | Revision・承認を保持 | 単位と実効値を特定可能 |
| Read-loop／Parser Flow | SDK／Server Owner | 受信からDispatchまで | SDK変更時 | Revisionを保持 | Bounded Enforcement順序を確認可能 |
| Oversize／Load test | Test Harness | N-1〜N-6 | Release時 | 合成Payloadを使用 | 資源がBoundedで副作用なし |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.4.3` | Tool Parameter単位のUnknown／Oversizeを拒否する。 |
| `v1.0-C9.1.1` | Tool単位のResource／Time Limitを扱う。 |
| `v1.0-C9.1.2` | 実行全体の累積Budgetを扱う。 |

## Known limitations and uncertainty

安全かつ実用的なSizeはUse Caseごとに異なり、大規模Resource転送ではChunk単位と総量の両方が必要になる。Size Limitだけで
Parser Algorithmic Complexityや多数の小Requestは防げない。

`verifiable`はArtifactの成熟度であり、DoS完全防止や製品適合を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-04-Schema-Message-Validation.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
