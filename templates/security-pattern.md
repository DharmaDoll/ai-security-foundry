---
id: "PATTERN-TBD"
title: "Pattern title"
status: "draft" # draft | reviewed | recommended | deprecated
category: "agents"
created: "YYYY-MM-DD"
last_reviewed: "YYYY-MM-DD"
owners: []
tags: []
framework_mappings: []
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

### Negative / abuse tests

Tests that attempt to bypass the control.

### Positive tests

Tests that show allowed behavior still works.

### Security properties to assert

List deterministic assertions that can be automated.

## Observability and response

Describe security-relevant logs, signals, alerting, provenance, and incident evidence.

Do not log secrets or unnecessary sensitive prompt/content data.

## Residual risk and limitations

State what this pattern does not solve.

Do not claim complete prevention of prompt injection or agent compromise unless a proof-level guarantee genuinely exists.

## Framework mappings

| Source | ID | Strength | Rationale | Last reviewed |
|---|---|---|---|---|
| OWASP AISVS | `vX.Y-C...` | direct/partial/context | TBD | YYYY-MM-DD |
| MITRE ATLAS | TBD | direct/partial/context | TBD | YYYY-MM-DD |
| OWASP GenAI LLM Top 10 | TBD | direct/partial/context | TBD | YYYY-MM-DD |
| OWASP Agentic Top 10 | TBD | direct/partial/context | TBD | YYYY-MM-DD |
| OWASP MCP Top 10 | TBD | direct/partial/context | TBD | YYYY-MM-DD |
| OWASP Agentic Skills Top 10 | TBD | direct/partial/context | TBD | YYYY-MM-DD |

Delete irrelevant rows rather than forcing mappings.

## References

Prefer primary sources. Include source version/date where relevant.

## Change log

| Date | Change | Reason |
|---|---|---|
| YYYY-MM-DD | Initial draft | |
