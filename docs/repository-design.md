# Repository Design

## Why the repository is not organized by a Top 10

External risk taxonomies change faster than engineering concepts. A Top 10 edition may rename, merge, split, or reorder risks without changing the underlying system architecture.

Therefore the physical structure is based on relatively stable technology and trust-boundary concepts:

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

## Two views, one body of engineering knowledge

### Controls view

The controls view answers:

> What requirement or assurance objective should be satisfied?

OWASP AISVS is the primary control backbone because it is designed as a verification standard with versionable requirements.

This repository should not fork AISVS as its primary working model. Forking and modifying the standard directly would couple internal engineering content to upstream document structure and make maintenance, attribution, and version tracking harder.

Instead:

```text
AISVS / other standards
        |
        v
controls + mappings
        |
        v
engineering patterns
```

### Engineering view

The engineering view answers:

> How can this system fail, and how should we build it safely?

Attack scenarios and recommended design live in the same pattern.

```text
Use case
  |
Threat / abuse path
  |
Security invariant
  |
Recommended architecture
  |
Implementation
  |
Security tests
```

This avoids a common failure mode where an attack catalog and a reference-architecture catalog become disconnected.

## Framework layers

A useful conceptual stack is:

```text
MITRE ATLAS
  adversary behavior / TTP
        |
OWASP risk taxonomies
  LLM / Agentic / MCP / Agentic Skills
        |
OWASP AISVS
  verifiable control requirements
        |
This repository
  concrete architecture, implementation, tests, operations
```

The layers overlap; they are not a strict hierarchy. Their roles are deliberately different.

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

`engineering/agents/secure-tool-execution` may map to identity, MCP, supply chain, observability, AISVS, ATLAS, Agentic Top 10, MCP Top 10, and Agentic Skills Top 10 without being duplicated under each directory.

## Pattern quality model

The repository should distinguish:

- `draft`: useful but not yet security-reviewed
- `reviewed`: reviewed for technical/security correctness
- `recommended`: accepted as a default/golden pattern for the intended scope
- `deprecated`: retained for historical traceability; replacement should be linked

Framework alignment alone is never sufficient to mark a pattern `recommended`.
