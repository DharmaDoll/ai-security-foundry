# Engineering Instructions

## Working scope

- This directory is the primary scope of the current task.
- Limit changes to this directory unless the task explicitly requires otherwise.
- Before modifying files outside this directory, explain why they are required.
- Follow the testing, architecture, and security requirements documented here.

## Mission

Build practical security engineering patterns for secure AI systems.

Optimize for secure-by-default architecture, testability, and real engineering value rather than framework coverage.

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
→ Framework mappings
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

Connect them through mappings. Do not reorganize engineering content to maximize control coverage.

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
* justified mappings and references.

## Domain instructions

Before working in a subdomain, read its local `AGENTS.md` when present.

Domain-specific files may add requirements for areas such as:

* agents;
* MCP;
* RAG;
* skills;
* memory.

## Detailed guidance

Read the relevant document when the task requires it:

* `docs/security-principles.md`
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
