# MITRE ATLAS v2026.08 Pattern Discovery

## Research record

- Analysis date: 2026-09-03
- Source role: adversary behavior, Technique, procedure, and Case Study evidence
- Authoritative source: MITRE ATLAS official `atlas-data` repository
- ATLAS collection version: `2026.08`
- Data format: `6.0.0`
- Immutable revision: `41d4f5ca4112f0e492ffaa3ebff07dc80a75afa5`
- Reviewed file: `dist/v6/ATLAS-2026.08.yaml`
- SHA-256: `a8d32f676854cc57721c217ec5b39f07db518076dee4a6c1335df0a7bc8271a2`
- Reviewed scope: 16 tactics, 114 Techniques, 83 sub-techniques, 39 Mitigations,
  72 Case Studies, and their relationships
- Case Study types: 22 `Incident`, 50 `Exercise`

ATLAS is a rolling source. This record pins one release so that later changes can be
diffed. ATLAS IDs below are discovery evidence, not asserted Framework Mappings.

## Method and filters

The analysis applies [`pattern-discovery.md`](pattern-discovery.md). It inspected the
full release, then clustered AI-product attack paths by Trust Boundary, Security
Invariant, deterministic Enforcement Point, and Negative Test.

The following were not promoted directly into Pattern candidates:

- tactics or Technique names without an AI-product Enforcement Point;
- generic Enterprise intrusion activity that merely used AI as an attacker tool;
- impact categories such as financial or reputational harm;
- Mitigation names without independently derived invariants;
- one-to-one translations of Prompt Injection, Jailbreak, Poisoning, or Supply Chain
  Technique IDs;
- broad problem families whose enforcement and verification differ by modality.

An ATLAS `Realized`, `Demonstrated`, or `Feasible` maturity value is preserved as
upstream context. It does not determine whether a repository candidate is reusable,
selected, or mature. Likewise, an ATLAS `Incident` is stronger realization evidence
than an `Exercise`, but the repository still has to establish generalizability.

## Existing Landscape candidates strengthened by ATLAS

### P1: Deterministically Authorized Tool Execution

ATLAS repeatedly connects Prompt Injection or compromised agent context to Tool
Invocation, data exfiltration, and destructive actions.

- Discovery evidence: `AML.T0053`, `AML.T0086`, `AML.T0101`; Case Studies
  `AML.CS0037`, `AML.CS0045`, `AML.CS0046`, `AML.CS0054`, `AML.CS0063`,
  `AML.CS0067`.
- Comparison result: retain P1. The evidence strengthens the need for authorization
  outside the model, constrained Tool capabilities, and denial tests at the action
  boundary.
- Limitation: shared Technique IDs do not prove that P1 covers every attack step or
  that a Mapping should be `direct`.

### P4: Untrusted Content-to-Action Containment

Indirect and triggered Prompt Injection appears across email, RAG, Web content,
MCP output, documents, and calendar content, followed by Tool use or exfiltration.

- Discovery evidence: `AML.T0051.001`, `AML.T0051.002`, `AML.T0066`, `AML.T0093`,
  `AML.T0094`; Case Studies `AML.CS0020`, `AML.CS0035`, `AML.CS0038`,
  `AML.CS0039`, `AML.CS0045`, `AML.CS0046`, `AML.CS0059`, `AML.CS0063`,
  `AML.CS0066`.
- Comparison result: retain P4 and prefer a Content-to-Action boundary over a
  generic "prevent Prompt Injection" Pattern.
- Limitation: prompt classification and model guardrails may be useful layers, but
  the ATLAS cases do not support treating them as the sole high-impact Enforcement
  Point.

### P6: Persistent Context Poisoning Containment

ATLAS distinguishes poisoning of memory, conversation threads, delayed
instructions, and agent configuration, supporting a persistence-specific candidate.

- Discovery evidence: `AML.T0080`, `AML.T0080.000`, `AML.T0080.001`, `AML.T0092`,
  `AML.T0094`; Case Studies `AML.CS0038`, `AML.CS0040`, `AML.CS0051`,
  `AML.CS0063`, `AML.CS0066`.
- Comparison result: retain P6 separately from single-turn content containment.
- Limitation: authorization and retention requirements remain in P5; persistence
  alone does not combine semantic poisoning and lifecycle access control into one
  Pattern.

## New candidates extracted from ATLAS

### P7: Provenance-Bound RAG Ingestion

- Provisional domain: `rag/`
- Discovery evidence: `AML.T0066`, `AML.T0070`, `AML.T0071`; Case Studies
  `AML.CS0026`, `AML.CS0035`, `AML.CS0059`.
- Repeating design problem: content enters a RAG corpus from a source whose owner,
  authorization, integrity, or change history is not enforced, and is later treated
  as trusted context.
- Main Trust Boundaries: content producer to ingestion pipeline; ingestion pipeline
  to index; document metadata to retrieval policy; retrieved content to model
  context.
- Security Invariant: only authorized, provenance-bound content may enter a corpus,
  and ingestion must not elevate content into instructions or trusted policy.
- Deterministic Enforcement Point: authenticated ingestion API, source allowlist,
  provenance and ownership validation, immutable document identity, review or
  quarantine workflow, and index update policy.
- Negative Test: submit content through an unauthorized source, forge owner or
  tenant metadata, replace content behind a previously trusted URL, and inject an
  instruction into an approved document; verify rejection, quarantine, or preserved
  untrusted provenance.
- Reuse: enterprise search, support knowledge bases, email indexing, document
  assistants, Web ingestion, and memory import.
- Non-integration rationale: P2 protects authorization at query time. P7 protects
  integrity and provenance at ingestion time; the security outcome and Enforcement
  Point are different.
- Decision: `retain`.

### P8: Provenance-Bound Training Data Pipeline

- Provisional domain: `model-and-supply-chain/`
- Discovery evidence: `AML.T0010.002`, `AML.T0020`, `AML.T0059`, `AML.T0115.000`;
  Case Studies `AML.CS0002`, `AML.CS0009`, `AML.CS0025`; design prompts
  `AML.M0007`, `AML.M0025`.
- Repeating design problem: mutable, externally hosted, weakly attributed, or
  attacker-influenced data enters training or fine-tuning and persistently changes
  model behavior.
- Main Trust Boundaries: data source to collection pipeline; collected object to
  curated dataset; dataset version to training job; trained model to promotion.
- Security Invariant: every training item and transformation must remain attributable
  to an approved immutable source state, and unreviewed changes must not enter a
  promoted model.
- Deterministic Enforcement Point: dataset manifest and digest verification,
  provenance store, source snapshotting, admission policy, transformation lineage,
  and model promotion gate.
- Negative Test: replace content at a retained URL, reclaim a source domain, inject
  unauthorized examples, alter data after review, or omit a transformation from
  lineage; verify that training or promotion fails.
- Reuse: pre-training, fine-tuning, evaluation datasets, feedback pipelines, active
  learning, and synthetic-data generation.
- Non-integration rationale: P7 protects runtime retrieval content. Training changes
  a durable model artifact and requires lineage through training and promotion, so
  its recovery and verification boundary is different.
- Decision: `retain`.

### P9: Immutable AI Artifact Resolution and Promotion

- Provisional domain: `model-and-supply-chain/`
- Discovery evidence: `AML.T0010`, `AML.T0074`, `AML.T0109`, `AML.T0111`,
  `AML.T0115`; Case Studies `AML.CS0015`, `AML.CS0027`, `AML.CS0031`,
  `AML.CS0049`, `AML.CS0053`, `AML.CS0065`; design prompts `AML.M0013`,
  `AML.M0014`, `AML.M0023`.
- Repeating design problem: mutable names, tags, namespaces, redirects, reputation,
  or automatic updates resolve to an artifact different from the one reviewed.
- Main Trust Boundaries: repository publisher to registry; registry namespace to
  resolver; dependency or model reference to build; build artifact to deployment.
- Security Invariant: a deployed artifact must be bound to the exact immutable
  identity and provenance that was reviewed; publisher, namespace, content, or
  dependency changes require a new decision.
- Deterministic Enforcement Point: resolver policy, digest and signature verification,
  lockfile, approved publisher identity, provenance attestation, and deployment
  admission controller.
- Negative Test: reclaim a namespace, mutate a tag, redirect an owner path, perform a
  rug pull, publish a dependency-confusion package, or substitute an unsigned
  artifact; verify that resolution or promotion stops.
- Reuse: models, datasets, adapters, packages, containers, MCP Servers, Tools, and
  agent skills.
- Non-integration rationale: P10 assumes an artifact has resolved and addresses what
  happens when it is processed. P9 prevents identity substitution before processing;
  a correct digest does not prove an artifact is safe.
- Decision: `retain`.

### P10: Safe AI Artifact Loading and Processing

- Provisional domain: `model-and-supply-chain/`
- Discovery evidence: `AML.T0011.000`, `AML.T0018.002`, `AML.T0018.003`,
  `AML.T0119`; Case Studies `AML.CS0031`, `AML.CS0064`, `AML.CS0068`; design
  prompts `AML.M0011`, `AML.M0016`, `AML.M0032`.
- Repeating design problem: model files, templates, serialized objects, metadata, or
  automated processing hooks are treated as passive data but execute code or alter
  privileged prompt construction during load.
- Main Trust Boundaries: artifact to parser or loader; parser to host process;
  artifact metadata to prompt/control plane; automated processing job to production
  infrastructure.
- Security Invariant: loading an untrusted artifact must not execute code, escape its
  processing environment, access production credentials, or modify control logic
  outside an approved policy.
- Deterministic Enforcement Point: safe format parser, disabled dynamic loaders,
  static scanning, isolated conversion sandbox, restricted filesystem and network,
  and promotion after behavioral validation.
- Negative Test: load a serialized code payload, malicious template, unsafe library
  reference, archive traversal, network callback, or sandbox escape attempt; verify
  rejection or containment without credential access.
- Reuse: model formats, dataset archives, notebook imports, plugins, generated code,
  evaluation artifacts, and document conversion.
- Non-integration rationale: P9 establishes artifact identity and provenance. A
  legitimately published or correctly pinned artifact may still contain unsafe
  active content, so load-time isolation needs an independent Pattern.
- Decision: `retain`.

### P11: Capability-Bounded Agent Extension Admission

- Provisional domain: `skills/`, with `mcp/` and `agents/` as consumers
- Discovery evidence: `AML.T0010.005`, `AML.T0011.002`, `AML.T0099`, `AML.T0110`,
  `AML.T0115.002`; Case Studies `AML.CS0049`, `AML.CS0053`, `AML.CS0054`; design
  prompts `AML.M0028`, `AML.M0032`, `AML.M0033`.
- Repeating design problem: an agent extension combines executable implementation,
  natural-language instructions, Tool metadata, external dependencies, and requested
  permissions, while installation treats only one of those surfaces as security
  significant.
- Main Trust Boundaries: extension publisher to registry; registry to installer;
  definition or instructions to model context; implementation to runtime; requested
  permission to effective capability.
- Security Invariant: installing or updating an extension must not grant capabilities
  beyond reviewed intent, and every behavior-influencing and executable component
  must remain bound to the reviewed version.
- Deterministic Enforcement Point: extension admission controller, publisher and
  artifact verification, manifest and permission policy, dependency lock, isolated
  runtime, explicit update review, and revocation mechanism.
- Negative Test: change only a Tool description, implementation, runtime response,
  transitive dependency, or permission request; verify that the review binding is
  invalidated and the extension cannot gain undeclared filesystem, network, secret,
  or Tool access.
- Reuse: MCP Tools, agent skills, plugins, coding-agent rules, browser extensions,
  and Tool marketplaces.
- Non-integration rationale: P9 supplies generic artifact identity, while P11 must
  compare declared behavior and permissions with effective runtime capabilities.
  P12 protects locally selected control configuration rather than extension
  admission as a package lifecycle.
- Decision: `retain`.

### P12: Agent Control-Plane Configuration Integrity

- Provisional domain: `agents/`, with `skills/` as an adjacent domain
- Discovery evidence: `AML.T0018.003`, `AML.T0081`, `AML.T0084`, `AML.T0084.001`,
  `AML.T0084.002`, `AML.T0084.003`; Case Studies `AML.CS0041`, `AML.CS0064`,
  `AML.CS0067`.
- Repeating design problem: repository files, prompt templates, Tool definitions,
  activation triggers, hooks, and call chains silently alter high-precedence agent
  behavior or expose capabilities.
- Main Trust Boundaries: project content to agent configuration loader; configuration
  to system instruction; Tool definition to capability registry; CI event content to
  agent activation.
- Security Invariant: untrusted project or event content must not modify trusted
  instruction precedence, Tool availability, activation conditions, or secret access
  without an explicit policy decision.
- Deterministic Enforcement Point: configuration precedence engine, trusted-path
  policy, schema and Unicode normalization checks, reviewed configuration manifest,
  CI trigger policy, and protected branch or signature enforcement.
- Negative Test: add hidden instructions, confusable characters, a new Tool, broad
  glob, unsafe hook, or untrusted event trigger; verify that the agent rejects,
  isolates, or requires explicit review before activation.
- Reuse: coding agents, repository instruction files, system prompts, CI agents,
  desktop agents, Tool manifests, and skills.
- Non-integration rationale: P11 governs installation and update of an extension.
  P12 governs precedence and trust of configuration already present in a project or
  execution context; provenance alone does not make tenant-controlled configuration
  trusted.
- Decision: `retain`.

### P13: Agent Runtime Host and Network Isolation

- Provisional domain: `agents/`
- Discovery evidence: `AML.T0053`, `AML.T0097`, `AML.T0105`, `AML.T0112.000`;
  Case Studies `AML.CS0016`, `AML.CS0045`, `AML.CS0046`, `AML.CS0048`,
  `AML.CS0050`, `AML.CS0052`, `AML.CS0067`, `AML.CS0068`; design prompt
  `AML.M0032`.
- Repeating design problem: even when named Tools are authorized, an agent runtime
  can directly reach host files, environment secrets, shells, sockets, cloud
  metadata, or unrelated networks outside the Tool boundary.
- Main Trust Boundaries: agent process to host; sandbox to kernel; process to
  filesystem, secret store, and network; ephemeral job to production environment.
- Security Invariant: compromise of the model or agent process must not grant access
  beyond the explicitly mounted data, allowed network destinations, resource budget,
  and isolated execution identity.
- Deterministic Enforcement Point: operating-system or virtual-machine sandbox,
  container policy, minimal mounts, secretless workload identity, network proxy,
  syscall policy, and clean per-task environment.
- Negative Test: attempt host escape, direct shell or syscall use, environment-secret
  reads, cloud-metadata access, localhost service access, undeclared network egress,
  and cross-task persistence; verify denial and cleanup.
- Reuse: coding agents, computer-use agents, evaluation agents, notebook execution,
  generated-code runners, and local assistants.
- Non-integration rationale: P1 mediates intended Tool calls. P13 assumes the runtime
  is compromised and prevents direct paths that bypass the Tool broker entirely.
- Decision: `retain`.

### P14: Mediated AI Credential Use

- Provisional domain: `identity-and-authorization/`
- Discovery evidence: `AML.T0055`, `AML.T0082`, `AML.T0083`, `AML.T0098`,
  `AML.T0086`; Case Studies `AML.CS0035`, `AML.CS0045`, `AML.CS0048`,
  `AML.CS0054`, `AML.CS0067`.
- Repeating design problem: broad or long-lived credentials are exposed to model
  context, Tool metadata, RAG content, process environment, or an agent runtime that
  can disclose or reuse them.
- Main Trust Boundaries: secret store to workload; workload to model context;
  credential to Tool; Tool to downstream resource; secret-bearing result to egress.
- Security Invariant: models and untrusted content must not receive reusable raw
  credentials; each operation receives only audience-, tenant-, action-, and
  lifetime-bound authority required for that operation.
- Deterministic Enforcement Point: credential broker, workload identity, token
  exchange, secretless Tool adapter, audience and scope enforcement, result
  filtering, and egress policy.
- Negative Test: instruct an agent to read environment variables, configuration,
  RAG credentials, Tool secrets, or token caches and send them externally; attempt
  token reuse for another audience or tenant; verify non-disclosure and rejection.
- Reuse: agents, MCP Servers, RAG connectors, CI assistants, database Tools, Cloud
  APIs, and browser automation.
- Non-integration rationale: P1 decides whether an action is allowed, and P3 governs
  delegation across an MCP downstream hop. P14 governs whether credential material
  becomes observable or reusable at all, including outside authorized Tool calls.
- Decision: `retain`.

### P15: Bounded Autonomous Objective and Resource Execution

- Provisional domain: `agents/`
- Discovery evidence: `AML.T0034.002`, `AML.T0116`, `AML.T0117`, `AML.T0124`;
  Case Studies `AML.CS0068`, `AML.CS0069`, `AML.CS0070`, `AML.CS0071`; design
  prompts `AML.M0036`, `AML.M0037`, `AML.M0038`.
- Repeating design problem: a long-running agent discovers new resources, creates
  subgoals, retries, delegates, or adapts its attack path until its effective scope,
  authority, and resource use exceed the initiating objective.
- Main Trust Boundaries: initiating objective to generated plan; plan step to next
  step; discovered resource to authorized target set; parent agent to sub-agent;
  workflow to compute, time, and Tool budget.
- Security Invariant: runtime discoveries and generated subgoals must not expand the
  pre-authorized objective, target set, identities, capabilities, delegation depth,
  or resource budget.
- Deterministic Enforcement Point: workflow state machine, objective and target
  policy, per-step authorization, capability ledger, iteration and delegation limits,
  scheduler quotas, and emergency termination control.
- Negative Test: give an impossible or ambiguous task and induce scanning of adjacent
  systems, account creation, new Tool acquisition, sub-agent fan-out, repeated
  retries, or target expansion; verify bounded termination or renewed authorization.
- Reuse: research and evaluation agents, cyber agents, Web agents, workflow
  automation, incident-response agents, and multi-agent systems.
- Non-integration rationale: P1 evaluates individual actions. P15 preserves authority
  and objective continuity over time and across an adaptive multi-step workflow;
  every isolated action can appear valid while the aggregate path violates scope.
- Decision: `retain`, with the limitation that several ATLAS cases describe
  intentionally malicious operators rather than accidental product scope drift.

### P16: Authenticated and Bounded Inter-Agent Delegation

- Provisional domain: `agents/`
- Discovery evidence: `AML.T0118`, `AML.T0118.000`, `AML.T0118.001`, `AML.T0124`;
  Case Studies `AML.CS0068`, `AML.CS0071`; related design prompt `AML.M0032`.
- Repeating design problem: direct messages or shared artifacts are treated as
  trusted instructions between agents without preserving sender identity,
  provenance, delegated authority, or task scope.
- Main Trust Boundaries: agent to agent; parent to child agent; agent to shared
  workspace; message broker to recipient; delegated capability to downstream Tool.
- Security Invariant: an inter-agent message or shared artifact cannot confer more
  authority than the authenticated sender can delegate, and cannot silently change
  the recipient's authorized objective.
- Deterministic Enforcement Point: authenticated message broker, signed or
  integrity-protected task envelope, delegation policy, capability token, shared
  artifact ACL, replay protection, and recipient-side authorization.
- Negative Test: spoof a parent, alter a shared plan, replay a delegation, inject an
  instruction through a shared artifact, exceed delegation depth, or request a Tool
  outside the sender's scope; verify rejection and attributable audit evidence.
- Reuse: planner-worker systems, agent swarms, background agents, shared workspaces,
  queue-driven agents, and cross-service automation.
- Non-integration rationale: P15 limits objective drift within an orchestrated
  workflow. P16 protects identity, integrity, replay, and delegated authority across
  communication boundaries, including when each agent's local objective is stable.
- Decision: `hold`. ATLAS demonstrates adversary-owned multi-agent communication,
  but more evidence is needed that the same failure recurs as a victim-system trust
  vulnerability rather than only as attacker infrastructure.

### P17: Untrusted Model Output at Active Interpreter Boundaries

- Provisional domain: `llm/`, with sink-specific consumers
- Discovery evidence: `AML.T0050`, `AML.T0067`, `AML.T0077`, `AML.T0102`; Case
  Studies `AML.CS0016`, `AML.CS0044`, `AML.CS0060`, `AML.CS0062`.
- Repeating design problem: model output is interpreted as executable code, shell,
  HTML, URL, query, template, or Tool argument instead of untrusted data.
- Main Trust Boundaries: model output to renderer; model output to parser or
  interpreter; generated argument to Tool adapter; stored output to later human or
  system consumer.
- Security Invariant: model output must not cross into an active sink unless a
  deterministic, sink-specific contract constrains its syntax, semantics, authority,
  and output context.
- Deterministic Enforcement Point: typed schema validator, contextual output encoder,
  allowlisted command or query builder, constrained interpreter, URL and egress
  policy, and isolated execution environment.
- Negative Test: generate stored and reflected HTML, shell metacharacters, unsafe
  URLs, path traversal, query injection, template directives, and malformed
  structured output; verify inert rendering, rejection, or containment.
- Reuse: chat UI, support consoles, code generation, database assistants, report
  generation, Tool adapters, and generated workflow steps.
- Non-integration rationale: P4 protects how untrusted input influences a model and
  later action; P17 protects the output-to-interpreter boundary regardless of why the
  model produced the value. P1 authorization does not make an argument safe for an
  interpreter.
- Decision: `retain`, but split by sink if a single Pattern cannot provide coherent
  Enforcement Points and tests.

### P18: Abuse-Resistant AI Service Resource Budgets

- Provisional domain: unresolved cross-domain concern, likely `observability/` plus
  the owning service domain
- Discovery evidence: `AML.T0029`, `AML.T0034`, `AML.T0034.000`, `AML.T0034.001`,
  `AML.T0034.002`; design prompts `AML.M0004`, `AML.M0036`.
- Repeating design problem: authenticated or anonymous requests can trigger
  unbounded inference, context, retries, parallelism, Tool calls, or downstream cost.
- Main Trust Boundaries: client to AI service; request to scheduler; model to Tool
  loop; tenant to shared compute and financial budget.
- Security Invariant: each principal, tenant, request, and workflow has enforceable
  bounds on time, compute, tokens, concurrency, retries, Tool calls, delegation, and
  downstream spend.
- Deterministic Enforcement Point: API gateway, quota service, scheduler, workflow
  budget ledger, rate and concurrency limiter, timeout, and circuit breaker.
- Negative Test: submit burst, long-context, high-complexity, recursive, retrying,
  parallel, and Tool-loop workloads; verify bounded consumption, fair isolation, and
  safe termination.
- Reuse: inference APIs, batch jobs, RAG, agents, evaluation systems, multimodal
  processing, and shared model platforms.
- Non-integration rationale: P15 protects objective and authority continuity in
  autonomous workflows. P18 also covers non-agent inference and shared-service
  availability and cost isolation at scheduler and quota boundaries.
- Decision: `retain`, but production workload evidence is needed because ATLAS marks
  Cost Harvesting sub-techniques as `Feasible`.

### P19: Minimum-Disclosure Inference API

- Provisional domain: `data-security/`
- Discovery evidence: `AML.T0024`, `AML.T0024.000`, `AML.T0024.001`,
  `AML.T0024.002`, `AML.T0040`, `AML.T0056`, `AML.T0057`; Case Studies
  `AML.CS0007`, `AML.CS0021`, `AML.CS0029`, `AML.CS0056`, `AML.CS0058`;
  design prompts `AML.M0002`, `AML.M0004`, `AML.M0019`.
- Repeating design problem: an inference interface returns more detail or permits
  enough adaptive queries to expose model behavior, training membership, sensitive
  content, system instructions, or a replicable substitute.
- Main Trust Boundaries: client to inference API; model state or training data to
  response; internal confidence and metadata to public contract; one tenant's query
  history to shared abuse detection.
- Security Invariant: an inference endpoint returns only information required by its
  product contract, and adaptive use cannot bypass identity, query, disclosure, and
  export policies without detection or limits.
- Deterministic Enforcement Point: authenticated API gateway, response minimization,
  confidence and metadata policy, per-principal query controls, behavioral abuse
  detection, privacy mechanism where justified, and export approval.
- Negative Test: perform adaptive extraction, membership inference, prompt probing,
  high-volume replication, confidence harvesting, and cross-account limit evasion;
  verify contract-limited output, enforced budgets, and actionable detection.
- Reuse: predictive model APIs, hosted LLMs, embeddings, classifiers, ranking APIs,
  and model evaluation endpoints.
- Non-integration rationale: P18 protects availability and cost. P19 protects model,
  data, and instruction confidentiality; identical query limits have different
  acceptance criteria and cannot alone prove non-disclosure.
- Decision: `retain`, with an explicit residual-risk requirement because model
  extraction or inference leakage generally cannot be claimed as completely
  prevented.

## Problem cluster held for further split

### Adversarially Robust Predictive-AI Decision Boundaries

`AML.T0015`, `AML.T0043` and its sub-techniques, together with numerous Case Studies
covering malware detection, biometrics, physical sensors, translation, and identity
verification, clearly expose a recurring problem: a high-impact decision relies on
a model or sensor input that an adversary can manipulate.

This is not yet one coherent Pattern candidate. Digital perturbation, physical
presentation attacks, deepfakes, malware-feature manipulation, and multi-sensor
systems require different Trust Boundaries, Enforcement Points, and Negative Tests.
The current top-level engineering taxonomy also lacks an obvious primary home for
predictive-AI runtime robustness.

- Decision: `split` and hold outside the canonical candidate list until modality- or
  decision-specific clusters are analyzed.
- Follow-up question: whether stable cross-modal invariants justify a new domain or
  should remain in system-specific Patterns.

## Observations merged rather than promoted

- Generic Prompt Injection and Jailbreak are attack methods, not standalone Pattern
  boundaries. Their consequences are represented by P4, P6, P12, P14, P15, and P17.
- Hallucinated package names (`AML.T0060`, `AML.T0062`, `AML.CS0022`) become Negative
  Tests for P9 and P17 unless further evidence demonstrates a separate Enforcement
  Point.
- AI telemetry logging (`AML.M0024`) is a cross-cutting operational requirement, not
  a Pattern without a concrete detection or evidence boundary.
- Generic Valid Accounts, Phishing, remote-service exploitation, data staging, and
  other Enterprise TTPs are not promoted merely because an AI agent used them.
- Guardrails, model alignment, user guidance, and human approval may be defense
  layers, but their ATLAS Mitigation entries do not by themselves define reusable
  deterministic Patterns.

## Result

- ATLAS strengthens existing candidates P1, P4, and P6.
- New retained candidates: P7 through P15, P17, P18, and P19.
- New held candidate: P16.
- Predictive-AI robustness remains a split-required problem cluster rather than one
  Pattern candidate.
- No Control or Framework Mapping is asserted by this analysis.

The canonical candidate summary is maintained in
[`../pattern-landscape.md`](../pattern-landscape.md).

## Primary references

- [MITRE ATLAS](https://atlas.mitre.org/)
- [Official MITRE ATLAS data repository](https://github.com/mitre-atlas/atlas-data)
- [ATLAS data release v2026.08](https://github.com/mitre-atlas/atlas-data/releases/tag/v2026.08)
- [Immutable analyzed revision](https://github.com/mitre-atlas/atlas-data/commit/41d4f5ca4112f0e492ffaa3ebff07dc80a75afa5)
- [Analyzed ATLAS v2026.08 YAML](https://github.com/mitre-atlas/atlas-data/blob/41d4f5ca4112f0e492ffaa3ebff07dc80a75afa5/dist/v6/ATLAS-2026.08.yaml)

Technique and Case Study identifiers resolve under the official ATLAS site using
`/techniques/<ID>` and `/studies/<ID>` respectively.
