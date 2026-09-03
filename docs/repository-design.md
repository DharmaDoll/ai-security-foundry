# Repository Design

## Why the repository is not organized by a Top 10

External risk taxonomies change faster than engineering concepts. A Top 10 edition may rename, merge, split, or reorder risks without changing the underlying system architecture.

Therefore the physical structure under `engineering/domains/` is based on relatively
stable technology and trust-boundary concepts:

- LLM
- RAG
- agents
- MCP
- agentic skills
- memory
- identity and authorization
- data security
- model and supply chain
- observability

Threats and frameworks are attached as metadata/mappings.

## Two independent views and a derived mapping layer

### Controls view

The controls view answers:

> What requirement or assurance objective should be satisfied?

OWASP AISVS is the primary control backbone because it is designed as a verification standard with versionable requirements.

This repository should not fork AISVS as its primary working model. Forking and modifying the standard directly would couple internal engineering content to upstream document structure and make maintenance, attribution, and version tracking harder.

Instead, controls are developed independently from engineering patterns:

```text
AISVS / other standards
        |
        v
     controls
```

### Engineering view

The engineering view answers:

> How can this system fail, and how should we build it safely?

Attack scenarios and recommended design live in the same pattern.

A pattern represents either a security design problem that recurs across systems or
a real attack/failure scenario that generalizes beyond one product, plus reusable
security invariants and solution principles. Discover patterns from systems, trust
boundaries, incidents, attack paths, and repeated failure modes—not from a control
inventory.

```text
Use case
  |
Scope and assumptions
  |
Assets and trust boundaries
  |
Threat / attacker capability / abuse path
  |
Security invariant
  |
Recommended architecture / control placement
  |
Implementation
  |
Negative and positive tests
  |
Observability / response
  |
Residual risk and limitations
```

This avoids a common failure mode where an attack catalog and a reference-architecture catalog become disconnected.

### Mapping view

Mappings are a third, derived body of knowledge:

```text
Authoritative requirements         Systems / incidents / attack paths
            |                                      |
            v                                      v
         Controls                    Engineering patterns
            \                                      /
             \                                    /
              +------ mapping assessments ------+
```

A mapping must not define either endpoint. A control or pattern can mature without
a successful mapping. Record an assessed no-match or a gap when no defensible
relationship exists.

## Source roles

A useful conceptual model is:

```text
OWASP AISVS ------------------------> control interpretation and verification
MITRE ATLAS / risk taxonomies ------> threat and risk context
Systems / incidents / specifications -> engineering pattern discovery

Controls + engineering patterns + threat context
                    |
                    v
            mapping assessments
```

These inputs overlap, but they are not a hierarchy and must not be treated as
interchangeable.

## Category boundaries

### `llm/`

Model interaction and LLM-specific control surfaces that do not require RAG or autonomous tools.

Examples: output trust, prompt/data separation, model routing, unsafe structured output, prompt-injection containment.

### `rag/`

Retrieval pipeline, corpus ingestion, authorization-aware retrieval, retrieval poisoning, provenance, and tenant isolation.

### `agents/`

Autonomous/semi-autonomous planning, tool invocation, multi-step action, delegation, approval, and blast-radius controls.

### `mcp/`

MCP-specific client/server authorization, tool discovery, protocol trust, server/tool provenance, and boundary design.

### `skills/`

Reusable agent behaviors/instructions/configuration that orchestrate capabilities. Includes installation, provenance, permissions, external instructions, isolation, scanning, update drift, and governance.

### `memory/`

Persistent or long-lived memory/context, poisoning, provenance, write authorization, isolation, retention, and recovery.

### `identity-and-authorization/`

Human, agent, workload, tool, and service identity; authorization; token audience; credential scope; delegation; tenant binding.

### `data-security/`

Sensitive data, prompts, retrieved data, model outputs, privacy/security boundaries, multi-tenant data handling, egress controls.

### `model-and-supply-chain/`

Models, adapters, dependencies, images, plugins/skills, datasets, artifacts, provenance, signing, pinning, and dependency integrity.

### `observability/`

Security-relevant telemetry, decision/action audit, tool invocation logs, provenance, detection, incident evidence, and response hooks.

## Cross-cutting patterns

A pattern should live where a developer is most likely to look first. Cross-cutting relationships belong in mappings and links, not duplicated content.

Example:

`engineering/domains/agents/secure-tool-execution` may map to identity, MCP, supply
chain, observability, AISVS, ATLAS, Agentic Top 10, MCP Top 10, and Agentic Skills
Top 10 without being duplicated under each directory.

## Pattern quality model

The repository should distinguish:

- `draft`: useful but not yet security-reviewed
- `reviewed`: reviewed for technical/security correctness
- `recommended`: accepted as a default/golden pattern for the intended scope
- `deprecated`: retained for historical traceability; replacement should be linked

Framework alignment alone is never sufficient to mark a pattern `recommended`.

Transitions to `reviewed` and `recommended` require recorded human review as defined in `AGENTS.md`. A `recommended` pattern must also have a named owner and independent human product-security approval for its stated scope. The review metadata belongs in the pattern front matter defined by `templates/security-pattern.md`.
