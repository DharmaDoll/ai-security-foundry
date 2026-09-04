---
title: "<stable repository title>"
versioned_id: "vX.Y-Cn.n.n"
requirement_id: "Cn.n.n"
family_id: "Cn"
source_key: "owasp-aisvs"
source_version: "X.Y"
source_status: "<stable|development|draft|public-review|beta|rolling|deprecated|superseded>"
upstream_revision: "<immutable revision>"
upstream_url: "<immutable normative requirement URL>"
research_url: "<immutable corresponding AISVS Research URL>"
last_verified: "YYYY-MM-DD"
maturity: "<discovered|understood|threat-linked|verifiable>"
mapping_assessment_refs: []
---

# <Stable repository title>

## Upstream basis

Identify the exact versioned requirement and the corresponding AISVS Research page.
Summarize the relevant source state; do not reproduce the normative requirement or
Research page wholesale.

Record any discrepancy between the normative requirement and Research material.
Treat the versioned requirement as normative and Research as supporting context.

## Interpretation

Explain what must be true in repository-authored, implementation-independent terms.
Separate the assurance expectation from examples of how a product might implement it.

## Security objective

Explain the security outcome and why it matters.

## Applicability

Describe systems, operating modes, data, identities, and impact levels for which the
control applies.

### Non-applicability

State narrow, defensible conditions under which the control does not apply. Do not
use the absence of a particular product or implementation as the sole rationale.

## Scope and assumptions

List the assumptions on which interpretation and verification depend. Identify
ambiguities or undefined upstream terms that require reviewer judgment.

## Assets, actors, identities, and trust boundaries

Identify the protected assets, relevant principals, delegated authority, execution
environments, policy components, and boundaries that affect the assurance claim.

## Required security properties

State testable properties that must remain true. Prefer properties that remain valid
across multiple implementation technologies. Each required property must be
necessary to the upstream assurance claim or to making that claim effective. Do not
silently turn adjacent secure-system properties into pass conditions for this
Control.

## Scope calibration and adjacent assurance

When the boundary is not obvious, distinguish:

- observations that directly pass or fail this Control;
- supporting conditions needed to make the Control meaningful; and
- important failures that belong to a different Control or assurance concern.

State the separate impact of adjacent failures so that a narrow Control pass is not
misrepresented as overall system security.

## Threat and failure-mode rationale

Explain the attacker capability, failure mode, and impact that justify the control.
Use versioned or snapshot-aware threat identifiers only when the technical
relationship is defensible. An explicit no-useful-mapping conclusion is valid.

For each relationship, record the source snapshot, identifier, relationship,
`direct`/`partial`/`context` strength, `proposed`/`validated` status, technical
rationale, and assessment date. Mapping status is independent of Control maturity.

## Verification

### Architecture and configuration review

Describe the boundaries, data flows, identities, policy, and configuration evidence
that must be inspected.

### Positive verification

Describe allowed behavior and the observable result that demonstrates correct
enforcement.

### Negative and abuse-case verification

Describe bypass, tampering, privilege, isolation, stale-state, and failure-mode tests
as applicable. State the expected denial or safe-failure result.

### Failure conditions

State which observations fail the control, including missing evidence and paths that
bypass the intended enforcement point when that enforcement point is part of this
Control's assurance claim. Keep failures belonging to adjacent Controls in a
separate-check section rather than broadening this Control implicitly.

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| `<artifact or repeatable result>` | `<trusted producer>` | `<system boundary>` | `<required age or event>` | `<protection requirements>` | `<observable pass condition>` |

Do not store real production evidence, secrets, customer data, or confidential
identifiers in this repository.

## Related requirements

Record overlaps, dependencies, supersession, and meaningful distinctions. Do not
collapse requirements merely because they use similar terminology.

## Known limitations and uncertainty

State what the control does not assure, implementation-dependent assumptions,
verification blind spots, and unresolved Research questions.

## Related mapping assessments (optional)

Link only to canonical assessments under `mappings/` after both endpoints have been
developed independently. Do not duplicate Mapping status or relationship details.
Delete this section when no assessment exists.

## References

- Normative requirement: `<immutable URL>`
- AISVS Research: `<immutable URL>`
- Additional primary sources: `<URL and reviewed version/date>`

## Changelog

Record material interpretation, scope, source, and verification changes without
creating a separate reviewer lifecycle for the Control.

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| YYYY-MM-DD | Initial draft | `<source or maintainer>` | `<commit or change record>` |
