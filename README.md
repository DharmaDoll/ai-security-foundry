# AI Security Engineering Patterns

A living engineering knowledge base for building secure AI products.

This repository turns rapidly changing AI-security guidance into practical engineering knowledge that developers, architects, and product-security engineers can use during design, implementation, review, and testing.

## Mission

Prevent security weaknesses from being designed into AI products by making secure patterns easier to find, understand, implement, and verify.

The repository focuses on proactive engineering for systems using technologies such as:

- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- AI agents and tool execution
- Model Context Protocol (MCP)
- Agentic skills
- Agent memory and long-lived context
- AI identity and authorization
- AI data flows and multi-tenant isolation
- AI/model/software supply chains
- AI observability and security monitoring

## What this repository is

This repository has two deliberately separate views.

### 1. Controls view — what must be satisfied?

`controls/` interprets verification requirements and control frameworks. OWASP AISVS is the primary control backbone.

The goal is not to copy standards into this repository. The goal is to connect stable, versioned control requirements to engineering patterns and evidence.

### 2. Engineering view — how should we build it safely?

`engineering/` is organized by relatively stable technology and architecture concepts rather than by the chapter structure of an external framework.

Each substantive engineering pattern must explain:

> Use case → Scope and assumptions → Assets and trust boundaries → Threat and abuse paths → Security invariant → Recommended architecture and control placement → Implementation → Negative and positive tests → Observability and response → Residual risk → Framework mappings

Attack and defense live together. A developer should not need to jump between a separate attack catalog and a separate architecture catalog to understand one engineering problem.

## Framework roles

External frameworks are inputs, not the repository structure.

| Source | Primary role |
|---|---|
| OWASP AISVS | Verification / control backbone |
| MITRE ATLAS | Adversary behavior / TTP backbone |
| OWASP GenAI LLM Top 10 | LLM application risk taxonomy |
| OWASP Top 10 for Agentic Applications | Agent risk taxonomy |
| OWASP MCP Top 10 | MCP-specific risk taxonomy |
| OWASP Agentic Skills Top 10 | Agent-skill / behavior-layer risk taxonomy |
| OWASP AI Exchange | Broad supporting security and privacy knowledge |

See `sources/registry.yaml` for the version and maturity state currently used by this repository.

## Repository structure

```text
.
├── AGENTS.md
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── plan.md
├── controls/
│   └── README.md
├── engineering/
│   ├── README.md
│   ├── llm/
│   ├── rag/
│   ├── agents/
│   ├── mcp/
│   ├── skills/
│   ├── memory/
│   ├── identity-and-authorization/
│   ├── data-security/
│   ├── model-and-supply-chain/
│   └── observability/
├── mappings/
│   └── README.md
├── sources/
│   └── registry.yaml
├── templates/
│   ├── security-pattern.md
│   └── framework-update-review.md
├── docs/
│   ├── repository-design.md
│   └── maintenance.md
└── .github/
    └── pull_request_template.md
```

## Core design principles

1. **Security engineering over framework coverage.** A mapping is useful only if it improves design, implementation, testing, or operations.
2. **Stable repository taxonomy.** Do not reorganize directories simply because a Top 10 or standard changes its taxonomy.
3. **Version-aware evidence.** Use versioned requirement identifiers whenever the source supports them, e.g. `v1.0-C9.4.3` rather than an unversioned AISVS ID.
4. **Threat and mitigation together.** Explain how a pattern fails before prescribing how it should be built.
5. **Defense in depth and containment.** Do not claim prompt filtering or model instructions alone eliminate prompt injection or agent compromise.
6. **Tests are part of the pattern.** A recommended control without an abuse case or verification method is incomplete.
7. **Human-reviewed standard updates.** Agents may detect, diff, classify, and propose updates; they must not silently rewrite security guidance because an upstream source changed.
8. **Primary sources first.** Prefer official OWASP, MITRE, protocol, vendor, and standards sources over secondary summaries.
9. **Explicit maturity.** Stable, draft, public-review, beta, deprecated, superseded, and rolling sources must not be treated as equivalent.
10. **Minimize copied upstream content.** Reference and summarize external material with attribution instead of creating an unmaintainable fork of the source text.

## Adding the first pattern

Start from `templates/security-pattern.md` and place the pattern under the most natural engineering category, for example:

```text
engineering/agents/secure-tool-execution/
├── README.md
├── insecure/
├── secure/
└── tests/
```

The pattern may map to several frameworks at once. That is expected.

New patterns start as `draft`. The `reviewed` and `recommended` states require recorded human review; see the pattern review lifecycle in `AGENTS.md`.

## Initial priority patterns

A practical starting sequence is:

1. Secure agent tool execution
2. Secure multi-tenant RAG
3. Indirect prompt-injection containment
4. Secure MCP server authorization
5. Agent credential and identity isolation
6. Secure agent memory
7. Secure agent-skill onboarding and update
8. AI supply-chain integrity
9. Sensitive-data controls for LLM/RAG flows
10. AI security telemetry and incident evidence

See `plan.md` for the initial build order.

## Status

Early-stage repository design. Framework metadata in `sources/registry.yaml` was initialized on 2026-09-01 and must be re-verified before claims of current compliance or alignment are made.
