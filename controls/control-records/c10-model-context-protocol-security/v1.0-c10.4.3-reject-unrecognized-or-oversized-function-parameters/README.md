---
title: "未知または過大なFunction Parameterを拒否する"
versioned_id: "v1.0-C10.4.3"
requirement_id: "C10.4.3"
verification_level: 1
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

# 未知または過大なFunction Parameterを拒否する

AISVS Verification Level: 1

## Upstream basis

AISVS `v1.0-C10.4.3`は、MCP ServerがFunction Callの未認識Parameterまたは過大Parameterを拒否することを求める。
固定Revisionの要件本文とC10.4 Researchを確認した。ResearchはExtra Field、巨大String／Array／Nested Object、
Path／URL等の境界値を試験例として示す。

## Interpretation

各Toolは受理するParameter名とValue Size／Collection Size／Nesting等の上限をServer側で明示し、宣言外Fieldまたは
上限超過をBusiness Logicや下流Sinkへ渡す前に拒否する。Client UIやModelが正しいArgumentを生成するという前提に
依存しない。

## Security objective

Parameter Smuggling、Mass Assignment、Parser負荷、Memory／Compute枯渇、および予期しないFieldが下流Command、Query、
File、HTTP Requestへ伝播することを防ぐ。

## Applicability

Argumentを受け取るすべてのMCP Tool／Function Call Endpointに適用する。Read-only、Internal、Local Toolも含む。

### Non-applicability

Argumentを一切受け取らないToolでも空Object以外を拒否する必要があるため、Tool提供自体がない場合に限り対象外にできる。

## Scope and assumptions

- Unknown Fieldは無視・保存・転送せず拒否する。
- Size LimitはByte、Character、Item、Property、Depth等、Parserと下流資源に適した単位で定義する。
- Transport全体のPayload上限はC10.4.5、本Controlは個々のFunction Parameterを扱う。
- Path TraversalやSQL／Command Injectionの意味的検査は隣接保証だが、上限／未知Field拒否だけで代替しない。

## Assets, actors, identities, and trust boundaries

資産はTool Business Logic、Memory／CPU、下流System、対象Dataである。ActorはModel、MCP Client、Server、Tool Handler、
攻撃者である。Trust Boundaryは`tools/call` ArgumentからTool Handlerへ入る地点にある。Enforcement PointはServer側の
Parameter Parser／Validatorである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Toolごとに受理するParameter名を閉じた集合として定義する。 |
| SP-2 | 宣言外、重複、曖昧なParameterを無視せず拒否する。 |
| SP-3 | String、Array、Object、Property、Nesting等へ明示上限を設ける。 |
| SP-4 | 拒否はBusiness Logic、Downstream Call、File／Command操作より前に行う。 |
| SP-5 | Alias、Batch、Retry、Direct Handler等の全Invocation経路で同じ制限を強制する。 |

## Scope calibration and adjacent assurance

C10.4.4は型、Required、Range、Pattern等を含むStrict Schema全体を扱う。C10.4.5はTransport Body総量を扱う。
未知・過大Parameterを拒否しても、許可Size内のSQL InjectionやPath Traversalは防げない。

## Threat and failure-mode rationale

侵害Modelや直接Callerは、隠れField、巨大Input、深いObject、重複Keyを送り、HandlerのMass Assignment、Parser差、
Resource Exhaustion、下流Sinkへの未検証値伝播を狙う。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

全ToolのParameter一覧、Unknown-field Policy、Size／Depth Limit、Validation順序、下流Sink、代替Invocation経路を確認する。

### Positive verification

許可Parameterを各境界値以内で送信し、正しいTool処理だけが実行されることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 未宣言Field、Case違い、Duplicate Keyを追加 | Handler前にRequest全体を拒否する。SP-1, SP-2 |
| N-2 | 上限超過String、Array、Object Propertyを送る | 安全に拒否し資源使用を制限する。SP-3, SP-4 |
| N-3 | 深くNestedしたObjectや巨大Unicode Inputを送る | Parser／ValidatorでBoundedに拒否する。SP-3 |
| N-4 | 未知FieldにCommand、Path、URL等を入れる | 無視・転送せず拒否する。SP-2, SP-4 |
| N-5 | Batch、Alias、Retry、Internal RouteでN-1／N-2を再実行 | 全経路で同じ結果になる。SP-5 |

### Failure conditions

Unknown Fieldを黙って受理・破棄・下流転送する、上限がない、またはValidation前に副作用／高負荷処理が始まる場合はFailを
裏付ける。全Tool InventoryがなければPassの証拠不足とする。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Parameter Contract | Tool Owner | 全Tool | Tool変更時 | Versionを保持 | NameとSize Limitを特定可能 |
| Validation Flow | MCP Server Owner | ParserからHandlerまで | SDK／Handler変更時 | Revisionを保持 | 副作用前の拒否を追跡可能 |
| Boundary／Oversize test | Test Harness | N-1〜N-5 | Release時 | 合成Dataを使用 | 全Toolで一貫して拒否 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.4.4` | 型・Range・Pattern等を含むStrict Schema Validationを全Serverで強制する。 |
| `v1.0-C10.4.5` | Transport単位の総Payload SizeをParse前に制限する。 |
| `v1.0-C10.2.5` | Valid Parameterでも、その具体値が認可範囲内かを確認する。 |

## Known limitations and uncertainty

適切な上限はToolと下流Resourceに依存する。小さいPayloadを大量送信するDoS、許可Field内のInjection、Algorithmic Complexityは
追加のRate／Resource Controlを要する。

`verifiable`はArtifactの成熟度であり、全Input Attack防止や製品適合を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-04-Schema-Message-Validation.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
