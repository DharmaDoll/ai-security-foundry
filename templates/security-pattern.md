---
id: "PATTERN-TBD"
title: "Pattern title"
status: "draft" # draft | reviewed | recommended | deprecated; see AGENTS.md
category: "agents"
created: "YYYY-MM-DD"
last_reviewed: null # YYYY-MM-DD after human review
owners: []
reviewed_by: [] # Non-sensitive human reviewer handles; required for reviewed/recommended
review_scope: null # Scope covered by the recorded review
review_evidence: null # Durable PR URL or review record
tags: []
---

# Pattern title

## Summary

One paragraph: what problem this pattern solves and when to use it.

## Use case

Describe the developer/system scenario in concrete terms.

## Scope and assumptions

State what is and is not covered.

## Assets

- Asset 1
- Asset 2

## Trust boundaries

Describe where trust changes: user/model, model/tool, retrieval/data store, agent/service, tenant/tenant, external/internal, etc.

## Threat model and abuse cases

For each relevant threat:

- attacker capability;
- entry point;
- abuse path;
- impacted asset;
- expected impact.

Where useful, map to MITRE ATLAS and OWASP risk taxonomies later in this document.

## Security invariants

Write properties that should remain true even when the model is wrong, manipulated, or compromised.

Examples of good invariant style:

- "The model cannot authorize an action outside the authenticated caller's permissions."
- "Retrieved content from tenant A cannot cause retrieval of tenant B data."
- "A tool request cannot reuse a token issued for a different audience."

Avoid vague statements such as "the prompt should be safe."

## Failure-prone / insecure design

Explain the design that fails and why.

> Clearly label intentionally insecure code/configuration.

## Recommended architecture

Describe where deterministic enforcement occurs and why.

Prefer a simple trust-boundary diagram.

```text
Untrusted input
   |
   v
Model / Agent
   |
   v
Deterministic policy / authorization
   |
   v
Scoped capability / tool
```

## Recommended implementation

State language/framework-independent requirements first.

Then add minimal platform/language examples only where they improve implementation clarity.

## Verification

For a guide, provide the concrete checks below. An executable test suite, demo,
or CI integration is an optional extension, not required to complete this section.
Keep document consistency checks separate from product test results.

### Negative / abuse tests

Provide a checklist of attempts to bypass the enforcement boundary:

| Attempt / invariant | Expected result | Evidence and side effects to inspect | Result / evidence reference |
|---|---|---|---|
| Concrete operation | Rejection or bounded behavior | Response, decision record, downstream state | Untested |

Use untested, passed, failed, or not applicable with a reason. Do not pre-fill
success without execution evidence. Model refusal alone does not verify the boundary.

### Positive tests

Describe allowed operations and expected results to pair with the negative cases.

### Security properties to assert

State observable security outcomes. They should be checkable in the reader's
implementation and may later be automated. Record any actual execution with its
version, environment, and evidence; a checklist alone is not a test result.

## Observability and response

Describe security-relevant logs, signals, alerting, provenance, and incident evidence.

Do not log secrets or unnecessary sensitive prompt/content data.

## Residual risk and limitations

State what this pattern does not solve.

Do not claim complete prevention of prompt injection or agent compromise unless a proof-level guarantee genuinely exists.

## Related mapping assessments (optional)

Mapping is a derived relationship, not an input to Pattern discovery and not a
measure of Pattern maturity. Do not record assessment status or relationship details
here. After independently developing both endpoints, create the canonical assessment
under `mappings/` and add a link here only when useful. Follow
`mappings/README.md`; do not add placeholder links. Delete this section when no
assessment link exists.

## References

Prefer primary sources. Include source version/date where relevant.

## Change log

| Date | Change | Reason |
|---|---|---|
| YYYY-MM-DD | Initial draft | |
