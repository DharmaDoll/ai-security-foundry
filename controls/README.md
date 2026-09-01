# Controls View

This directory is the requirement-oriented entry point.

## Primary backbone

OWASP AISVS is the primary verification/control backbone.

Do not copy the entire AISVS standard into this repository. Prefer:

- versioned requirement ID;
- concise interpretation;
- engineering implication;
- links to relevant patterns;
- verification evidence;
- source version/status.

Example conceptual record:

```yaml
source: owasp-aisvs
requirement: v1.0-C9.4.3
interpretation: "...repository-authored interpretation..."
patterns:
  - engineering/agents/example-pattern
mapping_strength: direct
```

## Why controls are separate from engineering patterns

Controls answer "what should be verified?" while engineering patterns answer "how should we build and test it?"

A single pattern can satisfy or partially address many controls, and a single control can require several patterns.

Do not force a one-to-one mapping.
