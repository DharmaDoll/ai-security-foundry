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

## Source Accuracy

Before interpreting or modifying a control:

1. Identify the authoritative upstream source.
2. Confirm its version or publication status.
3. Distinguish stable, draft, public-review, beta, rolling, deprecated, and superseded content.
4. Prefer versioned requirement identifiers when available.
5. Do not silently replace historical identifiers or mappings.

Do not copy large portions of upstream standards into this repository when a reference and original interpretation are sufficient.

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
→ Engineering mappings
→ Evidence expectations
→ Known limitations

Do not begin from implementation code.

Do not infer that a specific implementation is mandatory merely because it is one possible way to satisfy a control.

---

## Controls and Engineering Are Independent Domains

`controls/` defines and interprets security expectations.

`engineering/` develops practical security architectures, patterns, implementations, and tests.

Neither domain is subordinate to the other.

Connect them through explicit mappings.

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
* engineering-linked;
* verifiable.

Treat human review as an independent gate. A control is mature only when it is
`verifiable` and its review status is `reviewed`.

Do not mark a control mature merely because documentation exists.

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
