# Contributing

## What belongs here

Contributions should improve the practical security of AI-system design, implementation, verification, or operations.

Good contributions include:

- a new engineering pattern tied to a realistic threat;
- a secure reference implementation;
- an abuse case or regression test;
- a correction to an inaccurate security claim;
- an update caused by an upstream framework change;
- a mapping supported by clear evidence;
- an operational lesson that materially affects security.

Avoid contributions that only restate a framework without adding engineering value.

## Adding a pattern

1. Choose the most stable technology/architecture category under `engineering/`.
2. Copy `templates/security-pattern.md`.
3. Complete the threat model before the framework mapping.
4. Add minimal examples/tests if the pattern depends on implementation behavior.
5. Add primary references.
6. Mark new content as `draft` until reviewed.

## Framework updates

Use `templates/framework-update-review.md`.

Do not update mappings solely from a title or changelog. Review the semantic impact of the upstream change.

## Review expectations

Security review should ask:

- What attacker capability is assumed?
- What asset is protected?
- Where is the trust boundary?
- Which security property is deterministic and which depends on model behavior?
- Can the model bypass the control?
- What happens after model compromise or prompt injection?
- What is the blast radius?
- Can the recommendation be regression-tested?
- Is the mapping stronger than the evidence supports?
- Is the source version/maturity current?

## Content lifecycle

Patterns should move through:

`draft -> reviewed -> recommended -> deprecated`

- `reviewed` requires at least one human reviewer with relevant engineering or security expertise.
- `recommended` additionally requires a named owner and approval from a human product-security reviewer who did not author the latest substantive change.
- Record the review date, reviewer, scope, and durable evidence in the pattern front matter.
- Agents may prepare review materials but do not count as the required human reviewer.

Deprecation should name a replacement when one exists.
