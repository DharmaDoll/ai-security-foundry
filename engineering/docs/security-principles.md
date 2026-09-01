# Engineering Security Principles

## Mission

The `engineering/` domain develops practical security engineering knowledge for building and operating secure AI systems.

Its purpose is to answer:

* What can go wrong in this architecture or use case?
* Where are the important trust boundaries?
* What security properties must always hold?
* What architecture reduces the likelihood and impact of compromise?
* What implementation patterns should engineers prefer or avoid?
* How can the security properties be tested and verified?
* What limitations remain after the mitigation is applied?

The primary objective is not framework compliance.

The objective is to help engineers build secure systems by default.

## Engineering Scope

The `engineering/` domain may contain guidance and implementation patterns related to areas such as:

* LLM applications;
* RAG;
* autonomous and semi-autonomous agents;
* MCP clients and servers;
* agent skills;
* memory and context management;
* identity and authorization;
* sensitive data handling;
* model and dependency supply chains;
* observability and incident detection;
* sandboxing and isolation;
* human approval and operational controls.

Organize content primarily around stable engineering concepts, system boundaries, and practical use cases.

Do not reorganize the repository merely to mirror an external framework or Top 10 taxonomy.

## Use Cases First

Start with the actual engineering problem.

Examples:

* an agent invokes internal tools;
* an MCP server accesses a downstream API;
* a RAG system retrieves tenant-specific documents;
* an agent processes untrusted web content;
* an agent skill installs external dependencies;
* long-term memory stores user-generated content.

Clearly describe:

* who initiates the action;
* which identities exist;
* which systems are trusted or untrusted;
* which resources are sensitive;
* which side effects are possible;
* what happens if the model or agent behaves incorrectly.

Avoid designing controls for an abstract "AI system" without a concrete execution context.

## Threat Modeling

Threat analysis should precede mitigation design.

Consider relevant threats including, where applicable:

* direct prompt injection;
* indirect prompt injection;
* goal hijacking;
* excessive agency;
* confused deputy behavior;
* privilege escalation;
* credential misuse;
* unauthorized tool invocation;
* malicious or compromised tools;
* tool output injection;
* command or code injection;
* context poisoning;
* memory poisoning;
* RAG poisoning;
* cross-tenant data exposure;
* sensitive data exfiltration;
* insecure inter-agent communication;
* supply chain compromise;
* malicious skills or plugins;
* dependency compromise;
* cascading agent failure;
* insecure fallback behavior;
* insufficient auditability.

Use MITRE ATLAS, OWASP risk taxonomies, and other authoritative sources when they improve threat understanding.

Do not force every pattern to map to every threat framework.

## Security Invariants

Every mature engineering pattern should define the security properties that must remain true even when components fail or behave maliciously.

Prefer explicit invariants such as:

* an LLM decision alone must not authorize a privileged action;
* credentials must not grant broader authority than the initiating principal;
* tenant identity must be enforced outside of model-generated context;
* untrusted content must not directly determine privileged tool execution;
* credentials intended for one audience must not be reused for another;
* high-impact actions must be subject to deterministic authorization;
* compromise of one tool should not automatically compromise unrelated tools;
* model output must be treated as untrusted when it crosses a security boundary.

Security invariants should be:

* understandable;
* testable where practical;
* implementation-independent when possible;
* tied to specific threats.

## Prefer Containment Over Perfect Prevention

Assume that probabilistic AI components can fail.

Do not design systems around the assumption that:

* prompt injection can be completely eliminated;
* an LLM will always follow system instructions;
* a classifier will always correctly identify malicious content;
* an agent will always reason correctly;
* model-generated plans are trustworthy authorization decisions.

Prefer layered defenses that limit blast radius.

Typical controls may include:

* least privilege;
* capability restriction;
* deterministic authorization;
* scoped credentials;
* audience restriction;
* sandboxing;
* isolation;
* allowlists;
* schema validation;
* human approval;
* rate limits;
* transaction limits;
* output encoding;
* security monitoring;
* audit logging;
* safe failure behavior.

Prompt-based defenses may be useful as one layer but must not be treated as the sole security boundary for high-impact operations.

## Identity and Authorization

Always identify the principal whose authority is being exercised.

Distinguish between:

* the end user;
* the application;
* the agent;
* the model;
* the MCP client;
* the MCP server;
* the tool;
* the downstream resource;
* service identities.

Do not treat an agent identity as proof that an action is authorized.

Prefer authorization decisions based on deterministic policy and trusted identity context.

When delegation is involved, analyze:

* who delegated authority;
* what scope was delegated;
* for how long;
* for which resource;
* under which conditions.

Avoid uncontrolled credential forwarding and implicit privilege inheritance.

## Tool and Agent Execution

For systems that can perform actions:

* enumerate available tools and capabilities;
* classify tool impact;
* identify destructive and irreversible actions;
* identify required privileges;
* identify external side effects;
* identify which actions require user or human approval.

Do not expose broad capabilities to an agent when narrower tools can satisfy the use case.

Prefer tools that represent constrained business operations over generic execution interfaces.

Example:

Prefer:

`create_support_ticket()`

over:

`execute_arbitrary_http_request()`

when the narrower capability satisfies the requirement.

## RAG and Data Retrieval

For retrieval systems, explicitly consider:

* authorization before retrieval;
* tenant boundaries;
* document ownership;
* metadata integrity;
* poisoning of indexed content;
* malicious instructions embedded in retrieved content;
* sensitive data exposure;
* stale or revoked access;
* provenance;
* retrieval scope.

Similarity is not authorization.

Do not rely solely on metadata supplied through model context to enforce data access boundaries.

Prefer enforcement at the retrieval, database, or trusted policy layer.

## MCP

When working with MCP, explicitly model:

```text
Client
→ MCP Server
→ Tool or Resource
→ Downstream System
```

Identify identity and authorization boundaries at every hop.

Consider:

* MCP server authentication;
* client authorization;
* token audience;
* scope;
* token passthrough;
* confused deputy risks;
* malicious MCP servers;
* tool poisoning;
* unsafe tool metadata;
* dynamic capability discovery;
* context over-sharing;
* command injection;
* auditability.

Do not assume that credentials received by an MCP server are automatically appropriate for downstream resources.

## Agent Skills

Treat agent skills as executable or behavior-influencing supply chain components.

Consider:

* source authenticity;
* malicious instructions;
* excessive requested permissions;
* dependency integrity;
* external resources referenced by the skill;
* update behavior;
* version pinning;
* provenance;
* scanning;
* review;
* isolation.

Do not automatically trust a skill because it is expressed as Markdown, configuration, or natural language.

Changes to skills may represent security-significant code changes.

## Operational Security

Do not stop at development-time protections.

Consider runtime concerns including:

* telemetry;
* audit logging;
* anomaly detection;
* incident investigation;
* revocation;
* emergency disabling of tools or agents;
* credential rotation;
* model or dependency rollback;
* rate limiting;
* blast-radius reduction;
* safe degradation.

A pattern should explain significant operational dependencies when they affect its security properties.

## Decision Principles

Prefer:

* secure defaults over optional hardening;
* deterministic enforcement over probabilistic enforcement for authorization;
* least privilege over broad capability;
* containment over assumptions of perfect model behavior;
* narrow tools over generic execution;
* explicit trust boundaries over implicit trust;
* security invariants over implementation-specific rules;
* automated verification over documentation-only assurance;
* primary evidence over security folklore;
* practical engineering value over framework coverage.
