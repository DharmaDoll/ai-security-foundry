# Framework Mappings

Mappings connect engineering patterns to external controls, risks, and adversary techniques without making those external taxonomies the repository structure.

## Mapping strength

Every mapping should state one of:

- `direct`: the pattern materially implements/verifies the mapped item.
- `partial`: the pattern addresses part of the mapped item.
- `context`: the source explains relevant risk/context but should not be claimed as coverage.

## Required metadata

A mapping should include:

- source key from `sources/registry.yaml`;
- exact identifier when one exists;
- source version/status;
- mapping strength;
- short rationale/evidence;
- last reviewed date.

Example:

```yaml
- source: owasp-aisvs
  id: v1.0-C9.4.3
  strength: partial
  rationale: "The pattern covers credential rotation but not the full identity lifecycle."
  last_reviewed: "YYYY-MM-DD"
```

## Rules

- Prefer versioned AISVS identifiers.
- Do not map based only on similar wording.
- Do not maximize mapping count as a KPI.
- Re-review mappings after relevant upstream changes.
- Preserve historical traceability for superseded identifiers where useful.
