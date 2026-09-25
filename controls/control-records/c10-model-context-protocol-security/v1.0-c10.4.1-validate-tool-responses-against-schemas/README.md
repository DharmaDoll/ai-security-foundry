---
title: "Tool Responseを宣言Schemaで検証してからModel Contextへ入れる"
versioned_id: "v1.0-C10.4.1"
requirement_id: "C10.4.1"
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

# Tool Responseを宣言Schemaで検証してからModel Contextへ入れる

AISVS Verification Level: 1

## Upstream basis

AISVS `v1.0-C10.4.1`は、MCP `tools/list`と`tools/call`のResponseを、Model Contextへ注入する前に
宣言Schemaへ照合することを求める。採用済みstable v1.0の固定Revisionで要件本文とC10.4 Researchを確認した。
Researchは、Malformed JSON-RPC、Unexpected Content、`outputSchema`不一致、Duplicate Key等を試験例として示す。

## Interpretation

MCP Clientまたは信頼Gatewayは、Serverから届いたTool MetadataとResultをUntrusted Inputとして扱い、Protocol Schemaと
Toolが宣言したOutput Schemaの双方へ照合する。検証に成功したFieldだけをModel Contextへ渡し、失敗したResponse、
Validatorが扱えない形式、Schemaなしで構造を仮定するResponseを暗黙に通さない。

Schema Validationは構造・型・制約への適合を示すが、内容が安全・正確・善意であることは示さない。

## Security objective

MalformedまたはSchema外のTool Metadata／ResultがParser差異、隠れField、型混同を通じてModel Contextや後続処理へ
入り、意図しないTool選択・Action・Data解釈を起こすことを防ぐ。

## Applicability

`tools/list`または`tools/call` Responseを受け取り、Model Context、Planner、UI、他Toolへ渡すMCP Client／Gatewayに適用する。

### Non-applicability

Tool機能を一切利用しないMCP Clientは対象外にできる。ResponseがTextだけ、信頼Server、Local Serverという理由では
対象外にならない。

## Scope and assumptions

- Protocol Envelope、Tool Definition、Content Block、`structuredContent`、宣言済み`outputSchema`を区別して検証する。
- Optional SchemaがないDataは「検証済み構造」と表現せず、制限されたUnstructured Dataとして別扱いする。
- ParserとValidatorのDuplicate Key、Case、Number、Unicode挙動を揃える。
- Error ResponseもModelへ戻すなら同じTrust Boundaryを通す。

## Assets, actors, identities, and trust boundaries

資産はModel Context、Tool Catalog、後続Action、Client Parser状態である。ActorはMCP Server、Client、Gateway、Model、
攻撃者である。Trust BoundaryはServer ResponseからClient Parser／Model Contextへ移る地点にある。Enforcement Pointは
Model Context組立前のProtocol／Schema Validatorである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | `tools/list` ResponseをMCP Protocol Schemaへ照合してから利用する。 |
| SP-2 | `tools/call` Envelope、Content Block、宣言済みStructured Outputを対応Schemaへ照合する。 |
| SP-3 | Validation失敗、Ambiguous Parse、Unsupported ContentをModel Contextへ入れない。 |
| SP-4 | Validation対象と、実際にContextへ渡すCanonical Dataを一致させる。 |
| SP-5 | Success、Error、Streaming、Gateway、Cache等の全Response経路で検証を迂回させない。 |

## Scope calibration and adjacent assurance

C10.4.2はSchema上正しい自然言語に含まれるIndirect Prompt Injectionを扱う。C10.4.8はTool Definitionの承認後変更を
検出する。本ControlのPassはResponse内容の正確性、Provenance、無害性を保証しない。

## Threat and failure-mode rationale

侵害ServerはSchema外Field、型差、Duplicate Key、不正Content Block、宣言と異なるStructured Outputを返し、Clientと
Gateway／Modelの解釈差を利用する。検証後にRaw Responseを渡す設計でも同様にBypassが成立する。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

`tools/list`／`tools/call`受信からContext組立までのParser、Schema Source、Validator設定、Error／Streaming／Cache経路を追う。

### Positive verification

正しいTool DefinitionとResultが検証され、Canonicalな許可FieldだけがModel Contextへ渡ることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 必須Field欠落、型違い、未知Content Typeを返す | Context投入前に拒否する。SP-1〜SP-3 |
| N-2 | `structuredContent`を`outputSchema`違反にする | 拒否しUnstructured Textへ自動降格しない。SP-2, SP-3 |
| N-3 | Duplicate JSON Key、Case差、Malformed JSON-RPC Errorを返す | Ambiguous Dataを拒否する。SP-3 |
| N-4 | Validator通過後にRaw Responseへ差し替える | 検証済みCanonical Dataだけを使用する。SP-4 |
| N-5 | Error、Streaming、Cache、Gateway経由でN-1を再実行 | 全経路で拒否する。SP-5 |

### Failure conditions

Responseを検証前にModelへ渡す、ProtocolだけでTool Output Schemaを見ない、失敗時にRaw TextへFallbackする、または
検証値と利用値が異なる場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Response Validation Flow | Client／Gateway Owner | 全Tool Response経路 | Parser／SDK変更時 | Revisionを保持 | Context前のSchema Gateを追跡可能 |
| Schema Source／Policy | Tool・Client Owner | Protocol／Tool Schema | Tool定義変更時 | VersionとHashを保持 | 使用SchemaとResponseを対応可能 |
| Invalid-response test | Test Harness | N-1〜N-5 | Release時 | 模擬Serverを使用 | Schema外DataがContextへ入らない |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.4.2` | Schema適合後の内容をIndirect Prompt Injection観点で検査する。 |
| `v1.0-C10.4.4` | Server側のTool Input Schema強制を扱う。 |
| `v1.0-C10.4.8` | 承認済みTool Definitionの変更を検出し再承認する。 |

## Known limitations and uncertainty

Optional `outputSchema`やUnstructured Textでは構造保証が限定される。Schema自体が過度に広い、悪意ある、古い場合も
Validationは成功し得る。内容検査と後続Action制約が別途必要である。

`verifiable`はArtifactの成熟度であり、製品適合やResponseの意味的安全性を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-04-Schema-Message-Validation.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
