# Engineering Pattern Lifecycle

## Engineering Development Workflow

For every substantial engineering pattern, reason in the following order:

```text
Use case
→ Assets
→ Actors and identities
→ Trust boundaries
→ Data flows
→ Threats and abuse cases
→ Security invariants
→ Recommended architecture
→ Vulnerable implementation
→ Secure implementation
→ Security tests
→ Operational considerations
→ Framework mappings
→ Known limitations
```

Do not skip directly from a framework requirement to implementation code.

Do not start by asking how to maximize framework coverage.

## Known Limitations

Every mature pattern should document relevant limitations.

Examples:

* the mitigation reduces but does not eliminate prompt injection risk;
* sandbox escape remains possible under certain assumptions;
* human approval can be vulnerable to approval fatigue;
* authorization depends on upstream identity correctness;
* runtime monitoring cannot prevent all first-use abuse;
* a model upgrade may change behavior.

Do not make absolute security claims without strong evidence.

Prefer precise statements such as:

"reduces the blast radius"

over:

"prevents prompt injection."

## Incremental Development

Do not attempt to populate every engineering category at once.

Develop one high-quality pattern at a time.

Recommended lifecycle:

1. select a concrete problem;
2. research the domain;
3. define threats and invariants;
4. review the proposed architecture;
5. implement a minimal pattern;
6. implement security tests;
7. document limitations;
8. add framework mappings;
9. review the result;
10. improve templates or AGENTS.md based on lessons learned.

A completed pattern should improve the repository's ability to produce the next pattern.

## Domain-Specific AGENTS.md

Subdirectories may define additional instructions.

Examples:

* `engineering/agents/AGENTS.md`
* `engineering/mcp/AGENTS.md`
* `engineering/rag/AGENTS.md`
* `engineering/skills/AGENTS.md`

Use domain-specific instructions when the domain has:

* unique threat models;
* important security invariants;
* authoritative specifications;
* specialized test expectations;
* recurring implementation mistakes.

Do not duplicate repository-wide guidance unnecessarily.

The nearest applicable AGENTS.md should contain only the additional knowledge required for that domain.

## Definition of Done

A mature engineering pattern should usually contain:

* a clearly defined use case;
* relevant assets and actors;
* trust boundaries;
* threats and abuse cases;
* explicit security invariants;
* recommended architecture;
* secure implementation guidance;
* insecure patterns to avoid where useful;
* verification or security tests;
* operational considerations;
* known limitations;
* justified framework mappings;
* authoritative references.

Not every pattern requires executable code.

Architecture and configuration guidance may be the correct implementation artifact when application code is not the relevant security boundary.

## Scope Discipline

When working within `engineering/`:

* modify only the domain relevant to the current task;
* keep changes reviewable;
* avoid unrelated refactoring;
* do not populate placeholder content across unrelated domains;
* do not modify `controls/` merely to make mappings convenient;
* do not introduce dependencies without a clear engineering need;
* do not weaken an existing security property for implementation convenience.

When a broader issue is discovered, record it as follow-up work rather than expanding the current task without need.

## Learning Loop

Treat recurring Codex mistakes and human review findings as repository knowledge.

When a review identifies a reusable lesson:

1. determine whether it is domain-specific or repository-wide;
2. update the appropriate AGENTS.md, template, test, or guideline;
3. avoid solving the same class of mistake only through one-off prompt instructions.

The repository should become better at producing secure engineering guidance over time.
