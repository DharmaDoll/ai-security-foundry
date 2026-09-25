---
title: "すべてのMCP ServerでStrict Schema Validationを強制する"
versioned_id: "v1.0-C10.4.4"
requirement_id: "C10.4.4"
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

# すべてのMCP ServerでStrict Schema Validationを強制する

AISVS Verification Level: 2

## Upstream basis

AISVS `v1.0-C10.4.4`は、すべてのMCP ServerがStrict Schema Validationを強制することを求める。
固定Revisionの要件本文とC10.4 Researchを確認した。ResearchはWrong Type、Out-of-range、Extra Field、Nested Value、
URL／Path／Command Sink等を検証例として示す。

## Interpretation

各MCP Serverは、宣言SchemaをDocumentationではなくRuntime Contractとして、すべてのTool InputへServer側で強制する。
Type、Required、Enum、Range、Length、Pattern、Object Shape、Unknown Fieldを明示し、Canonicalization後の値をBusiness
Logicへ渡す。Schemaに通ったことだけで下流Sinkに安全とはせず、URL、Path、Query、Command等はDomain制約も評価する。

## Security objective

Modelまたは攻撃者が型混同、Injection、Path Traversal、SSRF、Mass Assignment等を引き起こすArgumentを下流Systemへ
到達させることを防ぐ。

## Applicability

Toolを公開するすべてのMCP Server、Server Adapter、Gateway変換経路に適用する。

### Non-applicability

MCP Server機能を一切提供しないComponentのみ対象外にできる。Clientが事前検証する、内部専用、生成AIだけがCallerという
理由では対象外にならない。

## Scope and assumptions

- Runtime Validatorと公開Schemaの差をなくし、変更を同時に管理する。
- `additionalProperties`、型Coercion、Default挿入、Unknown Format等のValidator Optionを明示する。
- CanonicalizationやTemplate展開を行う場合、展開後の実値にもPolicyを適用し、Secret展開をValidationより先にしない。
- SchemaはSyntax Boundaryであり、認可・Business Rule・Safe API利用は別途必要である。

## Assets, actors, identities, and trust boundaries

資産はTool Authority、File／Database／Cloud API、Secret、Server Processである。ActorはModel、MCP Client、Server、
Validator、Downstream System、攻撃者である。Trust BoundaryはMCP ArgumentからRuntime Object、Runtime ObjectからSinkへ
移る地点にある。Enforcement Pointは全Handler前のServer-side ValidatorとDomain-specific Sink Adapterである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 全Tool InputへRuntimeで宣言Schemaを強制する。 |
| SP-2 | Type、Required、Enum／Range、Length／Pattern、Object Shape、Unknown FieldをStrictに評価する。 |
| SP-3 | Coercion、Default、Canonicalization後の実行値が同じContractを満たす。 |
| SP-4 | URL、Path、Query、Command等はAllowlist／Canonical Root／構造化API等のDomain制約へ接続する。 |
| SP-5 | Validation失敗時はBusiness Logic・Secret展開・Downstream Call・副作用前に拒否する。 |
| SP-6 | 全Server、Tool、Version、Alias、Direct Routeで同じ保証を維持する。 |

## Scope calibration and adjacent assurance

C10.4.3はUnknown／Oversized Parameterの最低保証、C10.4.4はSchema全体と全Server適用を扱う。Strict Schemaでも
`query: string`のように広すぎるContractはInjectionを防がず、C10.2.5の認可やSafe Sink APIも必要である。

## Threat and failure-mode rationale

攻撃者はPrompt Injectionまたは直接Requestで、Wrong Type、Out-of-range、Path、URL、Query、Shell Metacharacterを生成する。
SchemaがDocumentationだけ、Client側だけ、Coercionで緩和される場合、下流Interpreterへ危険値が到達する。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

全Server／ToolのPublished Schema、Runtime Validator、Option、Canonicalization、Domain Policy、Sink API、Bypass Routeを対応付ける。

### Positive verification

最小限の正規InputがCanonicalなRuntime Objectとなり、構造化された下流APIで意図した処理だけを行うことを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Wrong Type、Missing Required、Out-of-range、Invalid Enumを送る | Handler前に拒否する。SP-1, SP-2, SP-5 |
| N-2 | Extra Field、Nested Object、Coercion可能な異型値を送る | Strict Contract外として拒否する。SP-2, SP-3 |
| N-3 | Path Traversal、未許可URL、Query／Command Metacharacterを送る | Canonical／Domain Policyで拒否する。SP-4 |
| N-4 | Environment Placeholder等がValidation後にSecretへ展開される値を送る | 展開前漏えいを起こさず、実値Policy違反を拒否する。SP-3〜SP-5 |
| N-5 | Alias、旧Version、Direct HandlerでN-1を再実行 | 全経路で拒否する。SP-6 |

### Failure conditions

公開SchemaとRuntimeが不一致、Client-sideだけ、型CoercionでContract外を通す、Validation前にTemplate／Secret展開や副作用を
行う、または一つでもServer／Toolが未強制ならFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Schema／Runtime inventory | MCP Owner | 全Server・Tool・Version | Tool変更時 | Version／Hashを保持 | 宣言とRuntime Validatorを対応可能 |
| Validator／Sink Flow | Server Owner | InputからDownstreamまで | 実装変更時 | Revisionを保持 | Validationが副作用前にある |
| Adversarial Schema test | Test Harness | N-1〜N-5 | Release時 | 合成Inputを使用 | Contract外とDomain違反を拒否 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.4.3` | Unknown／Oversized Parameterを明示的に拒否する。 |
| `v1.0-C10.2.5` | Schema-validなTool／Argumentの認可を行う。 |
| `v1.0-C10.4.1` | Server ResponseをClient側Schemaで検証する。 |

## Known limitations and uncertainty

Schema設計が広すぎる場合、Strictに強制しても意味的Attackは残る。Validator差異、Regex DoS、Unicode／Path Canonicalization、
Downstream Interpreter固有の脆弱性も別途評価が必要である。

`verifiable`はArtifactの成熟度であり、Injection完全防止や製品適合を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-04-Schema-Message-Validation.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
