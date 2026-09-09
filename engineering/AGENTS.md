# Engineering Instructions

## Working scope

- This directory is the primary scope of the current task.
- Limit changes to this directory unless the task explicitly requires otherwise.
- Before modifying files outside this directory, explain why they are required.
- Follow the testing, architecture, and security requirements documented here.

## Mission

Build practical security engineering patterns for secure AI systems.

Optimize for secure-by-default architecture, testability, and real engineering value rather than framework coverage.

An engineering pattern captures either a security design problem that recurs across
systems or a real attack/failure scenario that generalizes beyond one product,
together with reusable security invariants and solution principles. Discover
patterns from systems and failures, not from control catalogs.

Threat-taxonomy Techniques, procedures, and case studies—especially MITRE ATLAS—may
be Pattern discovery evidence when their technical attack paths are analyzed. Do
not create one Pattern per identifier; identifier Mapping remains a later step.

## Required reasoning

For substantial patterns, reason in this order:

Use case
→ Assets and identities
→ Trust boundaries
→ Threats and abuse cases
→ Security invariants
→ Architecture
→ Implementation
→ Security tests
→ Operational considerations
→ Known limitations

Do not jump directly from a framework requirement to code.

## Core principles

* Assume LLMs and agents can behave incorrectly.
* Prefer containment and blast-radius reduction over assumptions of perfect prevention.
* Do not use LLM reasoning as an authorization boundary.
* Prefer deterministic authorization, least privilege, scoped credentials, and narrow capabilities.
* Treat model output, retrieved content, tool output, skills, and external instructions as untrusted across security boundaries.
* Similarity is not authorization.
* Avoid uncontrolled credential forwarding.
* Do not claim that prompt injection or agent compromise is completely prevented without strong evidence.

## Controls relationship

`engineering/` and `controls/` are independent domains.

Engineering answers:

"How should this be designed, implemented, and tested securely?"

Controls answers:

"What security property should be assured?"

When a defensible relationship exists, connect them through mappings only after
both sides have been developed independently. Do not generate Pattern candidates
from controls, define a Pattern to fit a requirement, or reorganize engineering
content to maximize control coverage.

Mapping assessment is orthogonal to Pattern maturity. A mature Pattern may have an
assessed no-match or expose a control gap.

## Incremental development

Develop one high-quality pattern at a time.

Do not generate placeholders across all domains.

A mature pattern should normally include:

* use case;
* trust boundaries;
* threats;
* security invariants;
* recommended architecture;
* implementation guidance;
* security tests;
* operational considerations;
* known limitations;
* authoritative references.

Mapping assessments live under `../mappings/` and are not part of Pattern maturity.
Patterns may link to canonical assessments when they exist.

## Domain instructions

Engineering domain content lives under `domains/`. Keep cross-domain methods,
research records, and candidate comparisons under `docs/` instead of mixing them
with Pattern categories.

Before working in a subdomain, read its local `AGENTS.md` when present.

Domain-specific files may add requirements for areas such as:

* agents;
* MCP;
* RAG;
* skills;
* memory.

## Detailed guidance

GenAI LLM Top 10, Agentic Top 10, MCP Top 10, Agentic Skills Top 10, ACS, and Secure Agent Playbook
are supplementary sources for Pattern development. Use risk taxonomies for failure
and abuse perspectives, ACS for runtime-control design insights, and Playbook for
analysis, review, and negative-test questions. Preserve independent reasoning;
none is a dependency, mandatory conformance target, or maturity gate. Do not create
one Pattern per taxonomy item. Follow `docs/source-policy.md` when using them.

Read the relevant document when the task requires it:

* `docs/security-principles.md`
* `docs/pattern-discovery.md`
* `docs/pattern-lifecycle.md`
* `docs/testing-guidance.md`
* `docs/source-policy.md`

Do not load or modify unrelated guidance unless needed for the task.

## Scope discipline

* Keep changes small and reviewable.
* Avoid unrelated refactoring.
* Do not modify `controls/` merely to simplify mappings.
* Record broader issues as follow-up work.
* Promote recurring review findings into the appropriate AGENTS.md, test, template, or guidance document.
