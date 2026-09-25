# Controls Domain Instructions

## Working scope

- This directory is the primary scope of the current task.
- Limit changes to this directory unless the task explicitly requires otherwise.
- Before modifying files outside this directory, explain why they are required.
- Follow the testing, architecture, and security requirements documented here.

## Mission

The `controls/` domain maintains structured, traceable, and version-aware security control knowledge for AI systems.

Its purpose is to answer:

* What security property should be assured?
* Why is the control necessary?
* What threats or failure modes justify it?
* How can the control be verified?
* Which engineering patterns may help satisfy it?
* What evidence demonstrates that it is implemented effectively?

The objective is not to maximize framework coverage.

Prefer depth, correctness, traceability, and maintainability over the number of documented controls.

---

## Primary Control Backbone

Use OWASP AISVS as the primary verification and control backbone unless repository documentation states otherwise.

Other sources may supplement AISVS, including:

* MITRE ATLAS
* OWASP GenAI LLM Top 10
* OWASP Agentic Top 10
* OWASP MCP Top 10
* OWASP Agentic Skills Top 10
* OWASP AI Exchange
* relevant vendor-neutral standards and primary technical specifications

These sources have different purposes.

Do not treat threat taxonomies, risk lists, implementation guidance, and verification standards as interchangeable.

---

## Control Record Organization

Organize substantive AISVS Control records by AISVS family and versioned Requirement:

```text
control-records/
└── cNN-family-slug/
    ├── README.md  # family overview; create with substantive family content
    └── vX.Y-cN.N.N-descriptive-control-name/
        └── README.md
```

Use a zero-padded, lowercase family prefix such as
`c05-access-control-and-identity/`. Begin the Requirement directory with the lowercase,
versioned Requirement ID, followed by a stable descriptive slug.

Each Requirement-level `README.md` is the authoritative Control interpretation,
verification, evidence, and limitations. Catalog `control_ref` must point to that
Control `README.md`.

New learning content is organized separately by AISVS Section, not by Requirement:

```text
docs/learning/
└── cNN-family-slug/
    ├── README.md
    └── vX.Y-cN.N-section-slug/
        └── learning.md
```

One Section note teaches every Requirement in that Section as a coherent unit.
Include the Source version in the directory name so a future upstream revision does
not silently overwrite historical learning. Link each relevant Control to the
Section note once it exists, and link the Section note back to the individual
Controls. Keep learning progress and Control maturity independent.

Requirement-level learning notes created before this convention are retained as
historical learning artifacts. Do not move or combine them as an incidental part
of another task; consolidate them only in an explicit migration that preserves
links and substantive dialogue-derived insights.

The family-level `README.md` is the GitHub-friendly navigation entry point. It
summarizes the Category, Sections, and Requirements as concise assurance questions
and prohibited failure states, then links to the individual Control records. It is
not a substitute for the upstream standard, an individual Control, or a product
conformance checklist. Keep learning progress in `docs/learning/`, not in the
family overview.

Use this location for every future Family map. Do not create
`docs/learning/<family>/map.md`; create or update
`control-records/<family>/README.md` instead.

Do not create Section directories under `control-records/` or empty family
placeholders. Create a Control family or Requirement directory only when its first
substantive Control artifact is added. Under `docs/learning/`, create a versioned
Section directory only when its substantive `learning.md` is written. Learning may
precede a Control: do not create a placeholder Control README or catalog entry.

The directory layout supports navigation and AISVS traceability; `catalog.yaml`
remains authoritative for versions, lifecycle, maturity, and
relationships. Preserve historical paths when upstream content is renamed,
renumbered, deprecated, or superseded. Do not move or overwrite a historical
Control solely to mirror a newer AISVS release.

---

## Source Accuracy

Every substantive AISVS Control record must include an integer
`verification_level` matching `catalog.yaml` in its YAML front matter and
`AISVS Verification Level: N` as the first non-empty line after its title.
Use `templates/control.md`; validate both representations against the catalog.
Verification Level is upstream metadata, not Control maturity or product conformance.

Before interpreting or modifying a control:

1. Identify the authoritative upstream source.
2. Confirm its version or publication status.
3. Distinguish stable, draft, public-review, beta, rolling, deprecated, and superseded content.
4. Prefer versioned requirement identifiers when available.
5. Do not silently replace historical identifiers or mappings.

Do not copy large portions of upstream standards into this repository when a reference and original interpretation are sufficient.

---

## Interpretation and Practical Translation

AISVS is the primary assurance backbone, but it is not assumed to be a complete or
perfect product-security design guide. The purpose of this domain is not to perform
a line-by-line critique of AISVS or to paraphrase it into local files.

For each selected Control:

1. read the normative requirement and its corresponding AISVS Research material;
2. distinguish upstream statements from this repository's interpretation;
3. extract the essential assurance property and the failure it is intended to
   prevent;
4. translate that property into concrete trust boundaries, security invariants,
   deterministic enforcement points, verification, and evidence expectations;
5. review every Requirement and relevant case within the agreed learning or
   development scope rather than skipping difficult or ambiguous cases for speed;
6. record uncertainty, disagreement, and repository-specific judgment explicitly.

AISVS Research material is required supporting input for developing an AISVS
Control, but its examples and recommendations do not become normative requirements
automatically.

During a structured family-learning pass, record observations as learning evidence
first. After the full selected scope has been traversed, consolidate reusable
insights into the appropriate Control, template, AGENTS.md, or durable guidance.

---

## Learning Documentation

Use `docs/learning/README.md` as the common learning and persistence method for
every AISVS Category or Family.

- Teach one AISVS Section per learning content. Cover every Requirement in the
  Section; do not reduce the scope merely to reduce the number of files.
- Begin the Section lecture with its ID and title, followed by every included
  Requirement's versioned ID, AISVS Verification Level, exact English text, and a
  faithful Japanese translation.
- Teach from a senior product-security perspective: identify attacker capability,
  assets, Trust Boundaries, Security Invariants, deterministic Enforcement Points,
  observable Pass/Fail conditions, and the assurance boundary.
- Explain unfamiliar terms without removing security nuance.
- Separate Normative text, AISVS Research, repository interpretation, and insights
  derived from discussion.
- Persist a meaningful session as a standalone lecture plus a faithful
  reconstruction of important questions, uncertainty, corrections, and insights;
  do not preserve raw chat noise merely for completeness.
- Keep common policy, lightweight Family progress guides, and versioned Section
  notes in `docs/learning/`. Store each new `learning.md` under a versioned Section
  directory. Do not create empty placeholders.
- Never use learning completion to change Control maturity, Mapping status, or a
  product conformance result.

The legacy C5.1.1 Requirement note linked from `docs/learning/README.md` remains a
reference for depth and teaching stance. It is not the current storage granularity
or a template whose topic-specific sections must be copied mechanically.

---

## Control Development Workflow

Develop controls in the following order:

Control requirement
→ Interpretation
→ Security objective
→ Threat rationale
→ Applicability
→ Required security properties
→ Verification approach
→ Evidence expectations
→ Known limitations

Do not begin from implementation code.

Do not infer that a specific implementation is mandatory merely because it is one possible way to satisfy a control.

Assess engineering mappings separately and only after an engineering pattern has
been developed independently. Mapping success is not a control maturity stage.
Prioritize control development by assurance need, threat evidence, and verification
value—not by planned Pattern coverage.

---

## Controls and Engineering Are Independent Domains

`controls/` defines and interprets security expectations.

`engineering/` develops practical security architectures, patterns, implementations, and tests.

Neither domain is subordinate to the other.

When a defensible relationship exists, connect them through explicit mappings.

Mappings are derived after both endpoints are understood. Do not use a control
inventory to generate engineering pattern candidates, and do not define control
meaning from a particular pattern.

A control may map to:

* multiple engineering patterns;
* no existing engineering pattern;
* a partially applicable engineering pattern.

If no suitable engineering pattern exists, record the gap rather than inventing a weak mapping.

Do not reorganize or modify `engineering/` merely to improve control coverage.

---

## Threat Mapping

Controls should explain why they exist.

Use threat sources such as MITRE ATLAS and OWASP risk taxonomies when they improve understanding.

Do not create mappings based only on similar terminology.

Every non-obvious mapping should have a defensible rationale.

---

## Verification

A mature control should eventually explain how its effectiveness can be evaluated.

Verification may include:

* architecture review;
* configuration review;
* automated tests;
* negative tests;
* abuse-case testing;
* runtime evidence;
* audit logs;
* policy inspection;
* manual review.

Do not confuse the existence of a configuration or document with evidence that the control is effective.

---

## Incremental Development

Do not generate placeholder content for every framework requirement.

Use an AISVS Section (`C.x`) as the default planning and delivery batch when
expanding a Family. Within that batch, keep one canonical Control record, Catalog
entry, maturity value, scope, and verification boundary per Requirement (`C.x.y`).
Do not replace several Requirements with one Section-level Control. A Section is
complete only when every Requirement in its agreed scope has independently reached
the target maturity and the distinctions between adjacent Requirements have been
reviewed.

Work incrementally:

1. understand the overall control landscape;
2. select one control family;
3. understand that family;
4. select one representative requirement;
5. mature it deeply;
6. improve the control template and guidance based on lessons learned;
7. then expand to additional requirements.

The first mature requirement should act as a Golden Control for future work.

---

## Maturity

Use the control maturity model defined in `plan.md`:

* discovered;
* understood;
* threat-linked;
* verifiable.

`verifiable` is the current maturity target for a substantive Control. Do not add a
separate reviewer-status lifecycle or mandatory reviewer identity/evidence fields
unless future repository collaboration demonstrates a concrete need.

Control maturity describes the quality and completeness of the repository artifact.
Learning progress describes a person's understanding. Never advance, block, or
complete either one based on the state of the other.

Do not mark a Control `verifiable` merely because documentation exists.

Mapping assessment has its own status defined in `../mappings/README.md`. A control
may be mature with no matching pattern or with an explicit engineering gap.

---

## Framework Updates

When an upstream framework changes:

1. detect the change;
2. identify old and new versions;
3. perform a semantic diff;
4. assess security significance;
5. identify affected controls and mappings;
6. propose repository changes;
7. preserve useful historical traceability.

Do not automatically rewrite controls solely to mirror the latest upstream structure.

Security-significant changes require human review.

---

## Decision Principles

Prefer:

* security assurance over compliance appearance;
* primary sources over secondary summaries;
* explicit uncertainty over unsupported conclusions;
* traceability over convenience;
* stable engineering concepts over temporary taxonomy structure;
* meaningful mappings over coverage metrics.

Never invent framework requirements, identifiers, citations, mappings, or verification evidence.

---

## Scope Discipline

When working under `controls/`:

* do not modify unrelated repository areas;
* do not generate implementation code unless explicitly requested;
* do not restructure `engineering/`;
* do not attempt full-framework coverage in one task;
* keep changes small enough to review meaningfully.

If a task reveals a broader architectural issue, document it as a recommendation or follow-up rather than expanding the current task without need.
