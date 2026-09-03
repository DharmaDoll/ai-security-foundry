# Controls View

This directory is the requirement-oriented entry point.

See [`plan.md`](plan.md) for the incremental plan for developing the controls knowledge base.

## Current artifacts

- [`catalog.yaml`](catalog.yaml): machine-readable inventory containing only selected
  requirements; it is not a copy of the standard.
- [`schema/control-catalog.schema.json`](schema/control-catalog.schema.json): catalog
  structure and enumerated lifecycle states.
- [`templates/control.md`](templates/control.md): required structure for a substantive
  Control document.
- [`control-records/authorization-policy-boundary.md`](control-records/authorization-policy-boundary.md):
  initial Golden Control prepared for human product-security review.

Validate the catalog and its repository-level invariants with:

```shell
python3 -m pip install -r controls/requirements.txt
python3 controls/scripts/validate_catalog.py
python3 controls/tests/test_validate_catalog.py
```

The current catalog contains only the initial Golden Control. Its content maturity is
`verifiable`, but its review status remains `unreviewed`; it is not yet a mature
Control. No Engineering Pattern Mapping is asserted.

## Primary backbone

OWASP AISVS is the primary verification/control backbone.

## AISVS Research documentation

When developing, interpreting, mapping, or reviewing an AISVS control, always read
both:

1. the requirement in the applicable versioned AISVS chapter; and
2. the corresponding chapter or section page in the
   [AISVS Research Wiki](https://github.com/OWASP/AISVS/blob/main/1.0/research/README.md).

Use the Research documentation to investigate threat rationale, verification
approaches, tooling maturity, implementation caveats, open questions, and related
requirements. It is a required research input, but it is supporting material rather
than the normative requirement text.

If the Research documentation and the versioned requirement appear inconsistent,
do not silently choose or merge them. Treat the versioned requirement as the AISVS
normative source, record the discrepancy and uncertainty, and determine whether an
upstream or repository follow-up is required.

Do not copy Research pages wholesale. Record the page URL and reviewed source state,
summarize only the relevant findings with attribution, and independently validate
security-significant claims before using them in control interpretation,
verification, evidence expectations, or mappings.

Do not copy the entire AISVS standard into this repository. Prefer:

- versioned requirement ID;
- concise interpretation;
- security objective and required security properties;
- verification evidence;
- optional references to separately maintained mapping assessments;
- source version/status.

Example conceptual record:

```yaml
source: owasp-aisvs
requirement: v1.0-C9.4.3
interpretation: "...repository-authored interpretation..."
mapping_assessment_refs: []
```

Mapping assessment status and relationship details belong under `mappings/`.
Control records may link to those canonical assessments but must not duplicate them.

## Why controls are separate from engineering patterns

Controls answer "what should be verified?" while engineering patterns answer "how should we build and test it?"

A single pattern can satisfy or partially address many controls, and a single control can require several patterns.

Develop each side independently. Mapping is a later, derived artifact and does not
determine control maturity. Do not force a one-to-one mapping or generate Pattern
candidates from the Control inventory. See [`../mappings/README.md`](../mappings/README.md).
