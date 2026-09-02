# Mapping Relationships

Mappings are derived relationship artifacts. They connect independently developed
controls and engineering patterns to each other and to external risks or adversary
techniques without making those sources the repository structure.

Do not use mappings to discover engineering patterns, define control meaning, or
determine the maturity of either endpoint.

## Assessment status

Every mapping assessment should state one of:

- `not-assessed`: the endpoints have not been compared;
- `assessed-no-match`: no meaningful relationship was found;
- `gap`: a useful relationship is expected, but an adequate endpoint is absent;
- `proposed`: a relationship has been argued but not reviewed;
- `validated`: the relationship and its scope have been reviewed;
- `re-review-required`: an endpoint or upstream source changed materially.

Only `proposed` and `validated` assert that a mapping exists.

## Mapping strength

Every mapping should state one of:

- `direct`: the pattern materially implements/verifies the mapped item.
- `partial`: the pattern addresses part of the mapped item.
- `context`: the source explains relevant risk/context but should not be claimed as coverage.

## Required metadata

Every assessment record should include:

- a stable mapping assessment ID;
- assessment status;
- the subject or candidate endpoints considered;
- rationale for `assessed-no-match` or `gap`;
- last reviewed date.

An asserted mapping with `proposed` or `validated` status should additionally
include:

- relationship type;
- stable identifiers for both endpoints;
- source key from `sources/registry.yaml`;
- exact identifier when one exists;
- source version/status;
- mapping strength;
- short rationale/evidence;
- relationship scope and limitations.

Illustrative shape (not a mapping assertion):

```yaml
- mapping_id: MAP-TBD
  relationship: control-pattern
  status: proposed
  control_ref: controls/catalog.yaml#<versioned-control-id>
  pattern_ref: engineering/<domain>/<pattern>#<pattern-id>
  source: owasp-aisvs
  strength: partial
  rationale: "<technical comparison of the endpoints>"
  limitations: "<uncovered scope>"
  last_reviewed: "YYYY-MM-DD"
```

## Rules

- Prefer versioned AISVS identifiers.
- Develop and review each endpoint independently before mapping it.
- Do not map based only on similar wording.
- Do not maximize mapping count as a KPI.
- Record `assessed-no-match` or `gap` instead of forcing a relationship.
- Re-review mappings after relevant upstream changes.
- Preserve historical traceability for superseded identifiers where useful.
