# Controls View

This directory is the requirement-oriented entry point.

See [`plan.md`](plan.md) for the incremental plan for developing the controls knowledge base.

## Current artifacts

- [`catalog.yaml`](catalog.yaml): machine-readable C5 inventory with AISVS Verification
  Levels and lifecycle metadata; it is not a copy of the standard.
- [`schema/control-catalog.schema.json`](schema/control-catalog.schema.json): catalog
  structure and enumerated lifecycle states.
- [`templates/control.md`](templates/control.md): required structure for a substantive
  Control document.
- [Initial Golden Control](control-records/c05-access-control-and-identity/v1.0-c5.2.5-agent-authorization-pdp-isolation.md):
  first `verifiable` Control demonstrating the repository's Control-development method.
- [End-user Authorization Across Retrieval and Assembly](control-records/c05-access-control-and-identity/v1.0-c5.2.2-end-user-authorization-retrieval-assembly.md):
  second `verifiable` Control, applying the method to authorization-aware retrieval.
- [Shared Model-serving Tenant Isolation](control-records/c05-access-control-and-identity/v1.0-c5.3.1-shared-model-serving-tenant-isolation.md):
  third `verifiable` Control, separating logical serving-state isolation from
  shared-compute assurance.

Validate the catalog and its repository-level invariants with:

```shell
python3 -m pip install -r controls/requirements.txt
python3 controls/scripts/validate_catalog.py
python3 controls/tests/test_validate_catalog.py
```

The current catalog contains metadata for all 11 C5 Requirements and substantive
documents for C5.2.2, C5.2.5, and C5.3.1. `verification_level` records AISVS Level
1, 2, or 3; it is distinct from repository Control maturity. All three substantive
Controls are `verifiable`, the current target for a mature repository Control. This
describes the artifacts, not a maintainer's learning progress or proof that a
product implements them. No Engineering Pattern Mapping is asserted.

## Learning

- [Common Controls learning method](docs/learning/README.md): shared teaching,
  dialogue-reconstruction, insight, storage, and quality rules for every AISVS
  Category.
- [AISVS C5 Access Control and Identity learning guide](docs/learning/c05-access-control-and-identity/README.md):
  C5 Requirement sequence, lightweight progress, and persistent learning notes.

## Control record layout

Store substantive AISVS Control records under one AISVS-family directory:

```text
control-records/
└── cNN-family-slug/
    └── vX.Y-cN.N.N-descriptive-control-name.md
```

For example, the Golden Control is stored under
`c05-access-control-and-identity/`. The family number and versioned Requirement ID
provide direct upstream traceability; the descriptive suffix keeps the security
subject understandable without looking up the identifier.

Use only the family level as a directory boundary. Do not create section-level
directories such as `c05.2/`, and do not create empty family directories. Create a
family directory only with its first substantive Control.

The filesystem layout is a navigation aid. `catalog.yaml` remains authoritative for
source version, lifecycle state, Verification Level, maturity, related Requirements, and
Mappings. When AISVS renames or renumbers content, preserve the historical record
and perform a semantic change review; do not silently rename or overwrite it.

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
