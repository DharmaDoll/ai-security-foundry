---
title: "Tool ResponseをIndirect Prompt Injection観点で検査する"
versioned_id: "v1.0-C10.4.2"
requirement_id: "C10.4.2"
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

# Tool ResponseをIndirect Prompt Injection観点で検査する

AISVS Verification Level: 1

## Upstream basis

AISVS `v1.0-C10.4.2`は、MCP `tools/list`と`tools/call`のResponseをModel Contextへ注入する前に、
Indirect Prompt InjectionについてScreeningすることを求める。固定Revisionの要件本文とC10.4 Researchを確認した。

ResearchはTool Description、Schema Field、Success Result、Error Resultに埋め込まれたInstructionを扱い、単一Filterでの
完全防止は困難と明記する。以下の処理区分とFail-safeはRepository interpretationである。

## Interpretation

Tool DefinitionとResultを、Modelへの命令ではなく外部Server由来のUntrusted Dataとして識別し、Context投入前に
検査する。検出時の処理をBlock、Quarantine、構造化抽出、User確認、Capability縮小等へ明示的に結び付ける。

ScreeningはPrompt Injectionを完全に判定できる保証ではない。High-impact ActionはScreening結果にかかわらず、
Model外の認可、引数制約、承認、Sandboxで制限する。

## Security objective

悪意あるTool Description／Output／ErrorがSystem・Developer Instructionのように扱われ、秘密取得、別Tool呼出し、
Data送信、Policy無視等へModelを誘導するRiskを低減する。

## Applicability

`tools/list`／`tools/call` ResponseをLLM／Agent Contextへ入れるすべてのMCP Client、Host、Gatewayに適用する。

### Non-applicability

Tool ResponseがModelへ一切渡らず、決定論的Parserが必要Dataだけを抽出し、自然言語を破棄する経路は直接のInjection
Screening対象を縮小できる。ただし実際に別ContextやError Retryへ流れない証拠が必要である。

## Scope and assumptions

- Success、Error、Description、Schema、Annotation、Link、Embedded Resourceを対象Inventoryに含める。
- 「Sanitize」「Delimiter」「Model Instruction」だけを完全なSecurity Boundaryとみなさない。
- Detection精度、False Positive／Negative、更新、Bypass試験を管理する。
- Screening後もData由来とProvenanceを保持し、Control Instructionと混同させない。

## Assets, actors, identities, and trust boundaries

資産はSystem／Developer Intent、Secret、Tool Authority、Model Context、User Dataである。ActorはMCP Server、Content提供者、
Client、Model、Screening Component、攻撃者である。Trust BoundaryはServer ResponseからContextへ移る地点と、Model Output
からTool Actionへ移る地点にある。Enforcement PointはContext組立前のInspection／Transformationと後続Action Gateである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | `tools/list`と`tools/call`の全Model-visible ContentをUntrustedとしてScreeningする。 |
| SP-2 | Injection検出結果をBlock、Quarantine、縮小、Escalation等の明示処理へ結び付ける。 |
| SP-3 | Tool DataのProvenanceとRoleを保持し、System／Developer Instructionへ昇格させない。 |
| SP-4 | Error、Retry、Streaming、Encoded／Obfuscated Contentでも検査経路を迂回させない。 |
| SP-5 | Screening失敗・Unavailable時にHigh-impact Actionを無条件許可しない。 |
| SP-6 | Screeningを認可・承認・Sandboxの代替にしない。 |

## Scope calibration and adjacent assurance

C10.4.1のSchema Validationは内容が命令的かを判定しない。本ControlもInjectionの不存在を証明せず、C10.2.5やC9.5.3の
決定論的認可を代替しない。許可範囲内のModel操作や意味上の欺瞞には追加設計が必要である。

## Threat and failure-mode rationale

攻撃者はTool Description、Result、Errorへ「Secretを読み別Toolへ送れ」等のInstructionを埋め込む。ModelがDataと命令を
厳密に分離できない場合、正規MCP Responseを介してCross-tool ActionやExfiltrationが成立する。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

全Model-visible Field、Context Role、Screening Engine、Transformation、検出時Action、後続Authorization／Approvalを追う。

### Positive verification

通常のTool Metadata／Resultが意味を保って利用でき、Data ProvenanceとScreening結果を追跡できることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Tool Description／Schemaへ命令・Secret要求を埋め込む | 検出Policyを適用し無条件Context投入しない。SP-1〜SP-3 |
| N-2 | Success Resultと`isError` Resultへ同じPayloadを入れる | 双方を同じBoundaryで検査する。SP-1, SP-4 |
| N-3 | Encoding、Unicode、分割Streaming、Link先でPayloadを変形 | 正規化後に検査し、未対応形式を安全に扱う。SP-4 |
| N-4 | Screening ServiceをTimeout／Unavailableにする | High-impact ActionへFail-openしない。SP-5 |
| N-5 | 検出を回避したPayloadで未許可Tool／Argumentを要求 | 決定論的Action Gateが拒否する。SP-6 |

### Failure conditions

Tool Responseを信頼Instructionとして直接連結する、Error経路だけ未検査、検出結果に処理がない、Screening停止時に
無条件Allow、またはScreeningだけを認可Boundaryとする場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Context／Screening Flow | Client・Security Owner | 全Model-visible Field | Context構成変更時 | Revisionを保持 | 検査と処理点を追跡可能 |
| Detection／Handling Policy | Security Owner | Block・Quarantine・Escalation | Rule／Model変更時 | Versionと承認を保持 | 結果が具体Actionへ接続 |
| Injection Abuse Corpus結果 | Test Harness | N-1〜N-5 | Release・Detector変更後 | Test Dataを隔離 | Bypassと残存Riskを記録 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.4.1` | 内容検査前にResponse構造をSchema検証する。 |
| `v1.0-C10.2.5` | Injectionで生成されたTool／Argumentも決定論的に認可する。 |
| `v1.0-C10.4.8` | Tool Definition変更時に再承認し、Rug-pullを制限する。 |

## Known limitations and uncertainty

自然言語に対する完全なInjection検出は期待できず、False Positive／Negativeが残る。正当なInstructionを含むTool Outputも
あり、構造化抽出できないUse CaseではRiskとUsabilityのTrade-offがある。したがって「prevents prompt injection」とは
表現しない。

`verifiable`はArtifactの成熟度であり、Injection完全防止や製品適合を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-04-Schema-Message-Validation.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
