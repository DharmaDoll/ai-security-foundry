# Controls Knowledge Base Incremental Plan

- Status: proposal
- Scope: `controls/` only
- Primary backbone: OWASP AISVS
- Source state reviewed: 2026-09-01

## 1. Purpose and boundaries

`controls/` is the requirement-oriented entry point for AI product-security assurance. It answers what security property must be assured, why it matters, how it can be verified, and what evidence would demonstrate effective implementation.

The domain should provide:

- version-aware references to authoritative requirements;
- repository-authored interpretations and security objectives;
- threat rationale and applicability boundaries;
- testable security properties;
- verification approaches and evidence expectations;
- explicit threat rationale and optional references to separately maintained
  engineering-pattern mapping assessments;
- historical traceability when an upstream identifier or requirement changes.

The domain should not become:

- a fork or wholesale copy of AISVS or another standard;
- a framework-coverage dashboard optimized for percentage complete;
- an implementation-code library;
- a duplicate of `engineering/`;
- a place where risk lists, adversary techniques, and verification requirements are treated as equivalent;
- a repository for production evidence, secrets, customer data, or organization-confidential identifiers.

Controls and engineering patterns are independent bodies of knowledge. A control defines an assurance expectation; an engineering pattern describes a practical way to design, implement, test, and operate a system. Either may exist before the other, and mappings must not force a one-to-one relationship.

## 2. Current framework landscape

The source state below was checked against `sources/registry.yaml` and the linked primary sources on 2026-09-01.

| Source | State used by this repository | Role in `controls/` | Treatment |
|---|---|---|---|
| OWASP AISVS | `v1.0`, stable; `1.01-dev` is in development | Primary verification/control backbone | Build the catalog and mature controls against stable `v1.0`; monitor but do not silently adopt `1.01-dev` |
| MITRE ATLAS | rolling | Adversary behavior and TTP taxonomy | Use for justified threat links; never treat technique coverage as control completion |
| OWASP GenAI LLM Top 10 | 2026, stable | LLM application risk taxonomy | Use as risk context and mapping evidence, not as control structure |
| OWASP Top 10 for Agentic Applications | 2026, stable | Agentic application risk taxonomy | Use as agentic risk context, particularly for action and delegation controls |
| OWASP MCP Top 10 | beta; published identifiers are labeled 2025 | MCP-specific risk taxonomy | Treat mappings as provisional and status-aware; do not present it as a stable verification standard |
| OWASP Agentic Skills Top 10 | v1 draft/public review | Agent-skill and behavior-layer risk taxonomy | Use as provisional context only; re-review mappings when status changes |
| OWASP AI Exchange | rolling | Supplementary security/privacy knowledge | Use for research and context, not as a normative control backbone |

AISVS states that `v1.0` is its latest stable release, with a locked stable directory and ongoing work in `1.01-dev`. It defines 191 requirements across 12 chapters and assigns verification levels 1–3. Stable, development, beta, public-review, and rolling sources must remain distinguishable in every derived record.

AISVS Appendix B is a useful non-normative, developer-facing reorganization of the requirements. It may inform analysis, but AISVS explicitly identifies chapters C1–C12 as the normative source of truth. The repository should therefore derive requirement identity and meaning from the chapters, not from the appendix alone.

## 3. AISVS v1.0 family inventory

This is a landscape inventory, not an attempt to restate every requirement.

| Family | AISVS chapter | Planning focus for this repository |
|---|---|---|
| C1 | Training Data Integrity & Traceability | Dataset provenance, authorized change, labeling integrity, and traceability |
| C2 | Input Validation | Canonicalization, injection-aware handling, schema and length constraints, and input trust boundaries |
| C3 | Model Lifecycle Management & Change Control | Artifact identity, signing, evaluation gates, promotion, rollback, and change governance |
| C4 | Infrastructure, Configuration & Deployment Security | Serving infrastructure, deployment configuration, isolation, edge deployment, and protected model assets |
| C5 | Access Control & Identity for AI Components & Users | Authentication, AI resource authorization, policy boundaries, delegation context, and tenant isolation |
| C6 | Supply Chain Security for Models | Model and artifact provenance, dependency integrity, acquisition, and supplier trust |
| C7 | Model Behavior, Output Control & Safety Assurance | Output constraints, behavior evaluation, unsafe output handling, and safety assurance |
| C8 | Memory, Embeddings & Vector Database Security | Memory integrity, retrieval authorization, embedding/vector isolation, retention, and poisoning resistance |
| C9 | Orchestration & Agentic Security | Execution budgets, approvals, tool isolation, agent identity, authorization, delegation, and shutdown |
| C10 | Model Context Protocol (MCP) Security | MCP authentication, authorization, token handling, tool/resource integrity, and protocol auditability |
| C11 | Adversarial Robustness | Evaluation against adversarial manipulation, robustness boundaries, and failure handling |
| C12 | Monitoring, Logging & Anomaly Detection | Security telemetry, traceability, detection, incident evidence, and operational response |

The chapter order is not a repository implementation priority or a security ranking. Prioritization should consider cross-cutting value, testability, current engineering demand, threat severity, source stability, and the opportunity to improve the control-development method.

## 4. Proposed machine-readable catalog

### 4.1 Purpose

The catalog should be a compact inventory and traceability layer, not a second copy of the standard. It should answer:

- Which upstream requirement and exact version is being tracked?
- What is its upstream lifecycle state?
- How mature is this repository's interpretation?
- Is human re-review required?
- Where is the detailed control, if one exists?
- Which threat mappings have been justified?
- Which separately maintained engineering-pattern mapping assessments refer to this requirement?

Catalog entries do not require a corresponding Markdown file. Most requirements should initially exist only as catalog metadata; a detailed control document should be created only when that requirement is selected for maturation.

### 4.2 Planned artifacts

After the Golden Control plan is approved, introduce only these artifacts initially:

```text
controls/
├── catalog.yaml
├── schema/
│   └── control-catalog.schema.json
├── templates/
│   └── control.md
└── control-records/
    └── authorization-policy-boundary.md
```

Do not create chapter directories or one file per AISVS requirement during the schema experiment.

### 4.3 Catalog shape

The initial YAML shape should be equivalent to the following proposal:

```yaml
schema_version: 1
catalog:
  source_key: owasp-aisvs
  source_version: "1.0"
  source_status: stable
  last_verified: "YYYY-MM-DD"
  upstream_revision: "<verified upstream commit SHA>"

requirements:
  - versioned_id: v1.0-C5.2.5
    requirement_id: C5.2.5
    family:
      id: C5
      title: Access Control & Identity for AI Components & Users
    section:
      id: C5.2
      title: AI Resource Authorization & Classification
    verification_level: 2
    upstream_status: active
    upstream_url: "<canonical requirement URL>"
    maturity: discovered
    review_status: unreviewed
    development_priority: golden-control
    control_ref: null
    threat_mappings: []
    related_requirements: []
    mapping_assessment_refs: []
    last_reviewed: null
    reviewed_by: []
    review_scope: null
    review_evidence: null
```

This snippet defines a schema proposal; it is not a completed control record.

### 4.4 Field semantics

| Field | Required meaning |
|---|---|
| `source_key` | Exact key from `sources/registry.yaml` |
| `source_version` | Version or rolling state used for the catalog snapshot |
| `source_status` | Source maturity such as stable, beta, public-review, or rolling |
| `upstream_revision` | Immutable upstream revision inspected during ingestion |
| `versioned_id` | Globally unique source/version requirement identifier, such as `v1.0-C5.2.5` |
| `requirement_id` | Identifier within the source version |
| `family` / `section` | Upstream grouping metadata; not a mandate for repository directory structure |
| `verification_level` | AISVS level 1, 2, or 3 where applicable |
| `upstream_status` | `active`, `deprecated`, `superseded`, or `removed`; old rows remain for history |
| `maturity` | Repository interpretation maturity defined in the next section |
| `review_status` | `unreviewed`, `reviewed`, or `re-review-required`; independent of maturity |
| `development_priority` | Planning value such as `golden-control`, `next`, or `backlog`; not a coverage score |
| `control_ref` | Path to a substantive control document, or `null` when none exists |
| `threat_mappings` | Justified threat relationships used in the control rationale |
| `related_requirements` | Related, overlapping, superseding, or superseded requirements |
| `mapping_assessment_refs` | Optional links to canonical assessments under `mappings/`; status and relationship details are not duplicated in the control catalog |
| `last_reviewed` / `reviewed_by` / `review_scope` / `review_evidence` | Date, non-sensitive human reviewer identity, reviewed scope, and durable review record |

### 4.5 Schema invariants

The JSON Schema and catalog validation should enforce at least:

- uniqueness of `versioned_id` within the catalog;
- consistency between source version and versioned identifier;
- enumerated source, requirement, maturity, and review states;
- AISVS verification level limited to 1, 2, or 3;
- no dangling `control_ref` or `mapping_assessment_refs` target;
- preservation of deprecated, superseded, and removed records;
- `review_status: reviewed` only when review date, human reviewer, review scope, and durable review evidence exist;
- `maturity: verifiable` only when a substantive control document exists.

The first schema should be intentionally small. Add fields only when the Golden Control demonstrates a real maintenance or assurance need.

## 5. Control maturity model

Maturity describes the depth of this repository's understanding. It does not describe AISVS verification level and does not prove that a product implements the control.

| Stage | Minimum exit criteria |
|---|---|
| `discovered` | Versioned ID, source/version/status, family/section, verification level, canonical link, and upstream revision are verified |
| `understood` | Repository-authored interpretation, security objective, applicability, assumptions, ambiguity, and known exclusions are documented |
| `threat-linked` | Relevant attacker capability, failure mode, affected assets, and justified threat mappings are documented; absence of a useful mapping is explicit |
| `verifiable` | Testable security properties, positive and negative verification, evidence expectations, limitations, and review metadata are complete |

Progression is ordered: a record should not skip an earlier stage.

Human review is an orthogonal gate:

- `unreviewed`: agent- or author-prepared content;
- `reviewed`: a human product-security reviewer has accepted the stated scope and evidence;
- `re-review-required`: an upstream or repository change may have invalidated the prior review.

A control is considered mature only when `maturity: verifiable` and `review_status: reviewed`. Upstream change detection may set `review_status: re-review-required`; it must not silently rewrite the interpretation or erase prior evidence.

Engineering mapping assessment is maintained separately under `mappings/`. Its
status may be `not-assessed`, `assessed-no-match`, `gap`, `proposed`, `validated`,
or `re-review-required`. A control can reach `verifiable` and `reviewed` without an
assessment or a successful mapping.

## 6. Definition of a complete control

A substantive control is ready for human review when it contains all of the following:

1. Stable repository title and exact versioned upstream requirement ID.
2. Source version, maturity/status, canonical URL, verified revision, and last-verified date.
3. Concise repository-authored interpretation that does not reproduce the normative text wholesale.
4. Security objective and the reason the control exists.
5. Applicability, non-applicability, assumptions, assets, actors, identities, and trust boundaries where relevant.
6. Required security properties expressed independently of a particular product or implementation where possible.
7. Threat and failure-mode rationale with defensible mappings or an explicit statement that no mapping adds value.
8. Verification guidance covering positive behavior, negative/abuse cases, expected results, and failure conditions.
9. Evidence expectations identifying acceptable artifact types, producers, freshness, scope, and acceptance criteria.
10. Related or overlapping requirements that must not be incorrectly collapsed.
11. Known limitations, residual uncertainty, and implementation-dependent assumptions.
12. Primary references, attribution, review metadata, and change history.

The control becomes mature only after human product-security review confirms that these elements are internally consistent and the verification/evidence expectations can evaluate the stated security properties. Documentation existence, compilation, a configuration flag, or a framework mapping alone is insufficient.

Engineering mapping is assessed separately after a Pattern exists independently.
The assessment may validly conclude `assessed-no-match` or `gap`; neither outcome
reduces control maturity.

## 7. First family and Golden Control

### 7.1 Recommended first family: C5 Access Control & Identity

Develop C5 first because it:

- establishes the deterministic authorization boundary that many AI security properties depend on;
- applies across agents, RAG, MCP, model access, training data, and multi-tenant systems;
- exercises identity, delegation, policy enforcement, resource authorization, and isolation concepts without requiring full lifecycle coverage;
- has clear positive and negative verification opportunities;
- produces concrete evidence such as architecture boundaries, policy decisions, denied requests, token scope, and tenant-isolation results;
- is small enough to mature incrementally while still exposing cross-family overlaps with C8, C9, and C10;
- aligns with the repository principle that model reasoning must not be an authorization boundary.

This is a repository development priority, not a claim that C5 is universally more important than every other AISVS chapter.

### 7.2 Initial Golden Control: `v1.0-C5.2.5`

Select AISVS Level 2 requirement `v1.0-C5.2.5` as the first Golden Control. In concise repository terms, it requires the policy decision point for agent authorization to be isolated from the agent execution environment.

It is a strong exemplar because it requires:

- a concrete trust boundary between a potentially compromised agent and deterministic authorization;
- explicit identities, resources, actions, and policy inputs;
- a clear insecure failure mode in which the agent can influence or bypass its own authorization;
- implementation-independent security properties;
- negative tests that attempt to bypass, tamper with, or fail open around the policy decision point;
- multiple evidence types, including architecture review, policy configuration, decision logs, denial tests, and deployment isolation evidence;
- careful relationship analysis with `v1.0-C9.5.3`, without assuming the two requirements are duplicates;
- a stable security boundary that can later be compared with independently
  discovered engineering patterns.

The Golden Control phase should not pre-populate engineering mappings. Threat and
related-requirement analysis belongs to control development; engineering links are
assessed only after an independent Pattern endpoint exists.

## 8. Relationship model

Controls and Patterns have separate origins. Mapping is a third artifact:

```text
Authoritative requirement              Systems / attacks / recurring failures
          |                                           |
          v                                           v
Control security property                  Engineering Pattern
          |                                           |
          +--> verification and evidence              |
          \                                           /
           +---------- mapping assessment -----------+
```

### Threats

- Use MITRE ATLAS for adversary behavior and OWASP risk taxonomies for risk context.
- Record source key, identifier, version/status, relationship, strength, rationale, and review date.
- Map only when the threat explains why the control is needed or what it mitigates/detects.
- Do not infer a mapping from similar words.

### Engineering patterns

- Patterns are discovered from recurring system security problems and attack
  scenarios, not from this control inventory.
- Compare a control with a Pattern only after both are independently understandable
  and reviewable.
- Map by stable repository path and reviewed revision or review date.
- Use `direct`, `partial`, or `context` consistently.
- State which part of the control the pattern addresses and what remains outside it.
- Allow zero, one, or many patterns per control and zero, one, or many controls per pattern.
- If no suitable pattern exists, record an `engineering-gap` instead of creating or modifying engineering content from within the controls task.

### Verification

- Verification evaluates the security property, not the presence of a document or configuration key.
- Distinguish architecture review, configuration inspection, automated tests, abuse tests, runtime checks, and manual review.
- Define both success and failure conditions.
- Keep implementation-specific procedures in the control document or linked engineering pattern, not in the catalog record.

### Evidence

- Define expected evidence classes rather than storing real production evidence in this repository.
- For each class, specify producer, system scope, collection time, freshness, integrity expectations, sensitivity, and acceptance criteria.
- Treat screenshots and configuration exports as point-in-time evidence, not proof of continuous enforcement.
- Prefer repeatable test results and policy-decision records where the security property permits them.

This model keeps `controls/` and `engineering/` independent: controls define the assurance claim and evaluation criteria, while engineering patterns independently describe recurring design problems and reusable solutions. Mapping records the reviewed relationship without rewriting either endpoint.

## 9. Information that remains upstream-only

| Information | Why it stays upstream | Repository treatment |
|---|---|---|
| Full normative requirement text and complete AISVS chapters | AISVS is the source of truth and evolves under its own release process and license | Store versioned IDs, concise original interpretation, source revision, and canonical links |
| Full Appendix B controls inventory | It is non-normative and duplicates every requirement in a different organization | Use it as an analysis aid; do not import it as repository structure |
| AISVS Research Wiki pages and their full tooling/research notes | They are extensive, independently maintained, and may change separately | Link only to the relevant page and summarize material conclusions with attribution when needed |
| Complete OWASP Top 10 risk descriptions and mitigations | They are risk taxonomies, not this repository's control model | Record IDs, version/status, short rationale, and links |
| Complete MITRE ATLAS technique, mitigation, and case-study content | ATLAS is a rolling adversary knowledge base | Record stable identifiers where available, the reviewed state/date, and original mapping rationale |
| Upstream diagrams, tables, logos, and substantial licensed prose | Copying creates licensing and maintenance obligations | Reference the primary source; check license compatibility before any substantial adaptation |
| Upstream change history | Upstream owns the authoritative history | Preserve only repository impact reviews and links to the relevant upstream revisions |

The repository may retain exact identifiers, source/family/section names, verification level, lifecycle status, canonical URLs, immutable revision references, and concise original interpretations. Until the repository license is selected, avoid importing substantial CC BY-SA or other licensed upstream content.

Actual production evidence is not upstream material, but it should also remain outside this public knowledge base. Store only evidence expectations and sanitized examples; keep secrets, sensitive logs, customer data, and organization-confidential artifacts in the appropriate evidence system.

## 10. Incremental roadmap

### Phase 0 — Landscape and decisions

Deliverables:

- approve this purpose, boundary, family inventory, maturity model, and Golden Control selection;
- record open design decisions without creating requirement placeholders.

Exit gate:

- human agreement that the plan is narrow enough to execute and that C5/C5.2.5 is the correct first experiment.

### Phase 1 — Catalog and template experiment

Deliverables:

- create `catalog.yaml` with source metadata and only the Golden Control record;
- create a minimal JSON Schema enforcing the proposed invariants;
- create a control template based on the completeness criteria;
- add validation for schema errors, duplicate IDs, invalid states, and dangling references.

Exit gate:

- the catalog validates deterministically and does not require copied requirement text.

### Phase 2 — Mature the Golden Control

Deliverables:

- develop `v1.0-C5.2.5` through all four control maturity stages;
- validate threat and related-requirement mappings;
- define verification and evidence expectations;
- obtain human product-security review.

Exit gate:

- the control is `verifiable` and `reviewed`, and reviewers agree it is a reusable Golden Control.

### Phase 3 — Refine the method using C5

Deliverables:

- update schema, template, and instructions only from demonstrated Golden Control needs;
- ingest C5 requirement metadata into the catalog without generating one file per requirement;
- select the next two or three C5 requirements based on distinct learning value, not numerical order;
- mature one selected requirement at a time.

Candidate learning areas include end-user authorization context in retrieval, policy-enforced resource access, and multi-tenant isolation. Selection requires a separate review of the exact requirement, assurance value, and threat evidence.

Exit gate:

- at least two additional controls demonstrate that the template works beyond the Golden Control and that overlaps can be represented without duplication.

### Phase 4 — Add adjacent agentic families

Prioritize one representative requirement at a time from:

1. C9 Orchestration & Agentic Security;
2. C10 MCP Security;
3. C8 Memory, Embeddings & Vector Database Security.

This wave tests authorization delegation, tool boundaries, protocol identity, retrieval isolation, and cross-family control relationships. Do not ingest detailed content for all three chapters at once.

Exit gate:

- each selected control adds a distinct verification or evidence approach and is
  mature on its own terms.

### Phase 5 — Expand by assurance and risk need

Use observed product-security demand, threat evidence, assurance gaps, and review
capacity to select representative controls from:

- C2 and C12 for input boundaries and operational detection;
- C1, C3, C4, and C6 for data/model lifecycle, infrastructure, and supply-chain assurance;
- C7 and C11 for behavior/output assurance and adversarial robustness.

The order may change when threat evidence, engineering adoption, incidents, or upstream changes justify it. Record the decision rather than treating chapter order as a backlog.

### Phase 6 — Maintenance automation

Only after the catalog and several controls are stable:

- detect upstream version, identifier, level, and requirement changes;
- compare immutable old/new source snapshots;
- flag affected catalog records, controls, mappings, and evidence expectations;
- set `review_status: re-review-required` where appropriate;
- generate review proposals rather than rewriting controls automatically;
- report stale reviews and mappings.

Exit gate:

- automation preserves history, produces deterministic reports, and cannot promote maturity or approve security-significant changes.

## 11. Progress measures

Do not use percentage of AISVS requirements documented as the primary success metric. Prefer:

- number of `verifiable` and human-reviewed controls;
- percentage of mature controls with executable or repeatable negative verification;
- mapping rationale review quality and stale-mapping count;
- time to identify and triage a relevant upstream change;
- quality and age of separate mapping assessments;
- evidence expectations that engineering teams can actually produce;
- recurring lessons incorporated into schema, template, and guidance.

## 12. Primary references

- [OWASP AISVS repository and current stable-version guidance](https://github.com/OWASP/AISVS)
- [OWASP AISVS v1.0 stable source](https://github.com/OWASP/AISVS/tree/main/1.0)
- [OWASP AISVS release policy](https://github.com/OWASP/AISVS/blob/main/RELEASE.md)
- [AISVS C5 Access Control & Identity](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [AISVS C9 Orchestration & Agentic Security](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
- [AISVS Appendix B: AI Security Controls Inventory](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x91-Appendix-B_AI_Security_Controls_Inventory.md)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/)
- [OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/)
- [OWASP AI Exchange](https://owasp.org/www-project-ai-security-and-privacy-guide/)
