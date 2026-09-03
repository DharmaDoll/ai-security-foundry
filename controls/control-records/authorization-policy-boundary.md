---
title: "Agent Authorization Policy Decision Isolation"
versioned_id: "v1.0-C5.2.5"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-02-AI-Resource-Authorization-Classification.md"
last_verified: "2026-09-03"
maturity: "verifiable"
review_status: "unreviewed"
last_reviewed: null
reviewed_by: []
review_scope: null
review_evidence: null
mapping_assessment_refs: []
---

# Agent Authorization Policy Decision Isolation

## Upstream basis

This Control interprets OWASP AISVS `v1.0-C5.2.5`, a Level 2 requirement in
C5.2, AI Resource Authorization & Classification. The normative source and its
corresponding AISVS Research page were inspected at the immutable AISVS revision
recorded in the front matter.

The normative requirement establishes the isolation outcome but does not define a
specific process, container, network, or hosting mechanism. The Research page has
the same requirement identity and verification level and provides supporting threat,
verification, implementation, and limitation material. It was marked "Last
Researched: 2026-07-14" in the reviewed snapshot.

No conflict was found between the normative requirement and Research material. The
Research material's examples of separate services, sidecars, workload identity, and
policy products are implementation options, not additional normative requirements.
This repository therefore interprets isolation by effective compromise boundaries
rather than by deployment labels.

## Interpretation

The Policy Decision Point (PDP) used to authorize an Agent action must be outside the
Agent execution environment's effective control. Compromise of that environment
must not allow the Agent to modify the PDP, its Policy or trusted attributes, its
administrative path, or the integrity of the decision returned to the enforcement
path.

For this Control:

- **Agent execution environment** means the processes, containers, hosts, files,
  runtime configuration, credentials, and control interfaces that the Agent can
  directly influence under the assessed threat model.
- **PDP** means the component that evaluates trusted identity and request context
  against applicable Policy and returns an authorization decision.
- **Policy Enforcement Point (PEP)** means the component that applies the PDP's
  decision before access to the protected action or resource.
- **isolated** means that the Agent runtime lacks an effective path to read or write
  PDP internals, administer Policy, impersonate trusted PDP callers, forge or alter
  decisions, redirect the trusted decision channel, control PDP lifecycle, or alter
  authoritative decision evidence.

A library loaded into the Agent process does not satisfy this interpretation. A
separate process, container, sidecar, host, or managed service satisfies it only when
its actual identity, privilege, administration, communication, storage, and lifecycle
boundaries resist the assessed Agent compromise. Different names, processes, or
containers without distinct effective security boundaries are insufficient.

PDP isolation must be evaluated on a real authorization path. An unused external PDP
does not satisfy the Control merely because it exists. Verification of that path is
not, however, a claim that this Control alone proves complete mediation, correct
Policy semantics, fine-grained action authorization, or continuous re-authorization.

## Security objective

Preserve the integrity and independent auditability of authorization decisions when
an Agent is manipulated, compromised, or simply behaves incorrectly. The Agent may
request an action, but it must not control the authority that decides whether the
action is allowed.

The intended outcome is blast-radius reduction: compromise of the Agent execution
environment does not automatically become compromise of the authorization control
plane.

## Applicability

This Control applies when an autonomous or semi-autonomous Agent can request an
operation governed by authorization, including:

- invoking internal or external Tools and APIs;
- reading protected data or retrieval resources;
- changing records, configuration, infrastructure, or external state;
- delegating work to another Agent, service, or Tool;
- initiating an operation on behalf of a user or workload identity.

It applies to read-only actions when confidentiality or tenant separation depends on
authorization. A human approval step does not remove applicability because approval
and authorization answer different questions.

### Non-applicability

The Control may be not applicable when the assessed system has no Agent execution
environment, or when model output cannot initiate, parameterize, or influence access
to any authorization-controlled action or resource. Examples may include isolated,
offline text generation with no protected data, Tool, network, filesystem, or state
mutation capability.

Non-applicability must be supported by an architecture and capability assessment.
Describing an Agent as "read-only," "internal," or "human supervised" is not by
itself sufficient.

## Scope and assumptions

The assessment must state:

- the exact Agent execution boundary assumed compromised;
- the protected actions and resources whose authorization uses the PDP;
- the identities and trusted attributes used in a decision;
- where Policy is authored, stored, distributed, evaluated, and enforced;
- which administrative and emergency paths can change or bypass Policy;
- whether decisions are cached, delegated, or transformed before enforcement;
- which infrastructure administrators are trusted outside the Agent threat model.

This Control assumes that an authenticated identity and necessary authorization
attributes can be supplied to the PDP through a trusted path. It does not prove that
those inputs are correct. The verifier must record residual dependencies on identity,
attribute, Policy Administration Point (PAP), Policy Information Point (PIP), PEP,
and protected-resource controls.

The word "isolated" is not quantitatively defined by AISVS. This interpretation
therefore uses the required security properties and negative tests below to make the
boundary falsifiable. A higher-assurance threat model may require a separate host,
account, cluster, hardware boundary, or independently administered service even when
process-level isolation passes a lower-assurance assessment.

## Assets, actors, identities, and trust boundaries

| Element | Security relevance |
|---|---|
| Initiating principal | User or workload whose authority and intent constrain the requested action |
| Agent runtime | Potentially compromised requester; must not be trusted to make or self-assert authorization decisions |
| PEP | Applies the authorization outcome before access to the protected action or resource |
| PDP | Evaluates trusted request context and Policy; the primary protected component for this Control |
| PAP and Policy store | Change the rules the PDP evaluates; compromise is equivalent to controlling future decisions |
| PIP or attribute sources | Supply identity, tenant, resource, risk, and contextual attributes used by the PDP |
| Protected Tool or resource | Receives only an action admitted by the trusted enforcement path |
| Decision evidence store | Preserves a record that the Agent runtime cannot rewrite or suppress |

The principal trust boundaries are:

1. Agent runtime to the action-enforcement interface.
2. PEP to PDP authorization request and PDP to PEP decision response.
3. PDP to Policy and trusted attribute sources.
4. Policy administrator to PAP and Policy deployment path.
5. PEP to the protected Tool or resource.
6. PDP and PEP to the independent evidence store.

A reference decision flow is:

```text
Initiating identity and trusted context
                 |
                 v
Agent runtime -> PEP ---- authenticated decision request ----> PDP
                 ^                                           /   \
                 |                                          /     \
                 +----------- bound decision --------------+   Policy / PIP
                 |
                 v
        Protected Tool or resource

PDP / PEP decision evidence ----------> agent-nonwritable evidence store
```

The Agent may propose the action and untrusted parameters. It must not be the source
of truth for identity, tenant, approval, entitlement, Policy version, or the final
allow decision.

## Required security properties

These properties are this repository's testable interpretation of the upstream
isolation outcome.

### SP-1: Separate compromise boundary

The Agent execution identity and accessible runtime privileges cannot read or modify
PDP code, memory, configuration, Policy, trusted attributes, credentials, trust
anchors, or lifecycle controls.

### SP-2: Separate administration

The Agent identity cannot invoke PAP, Policy deployment, debug, maintenance,
impersonation, or emergency interfaces that can change how the PDP decides. Policy
changes use a separately authenticated and auditable administrative path.

### SP-3: Authenticated and integrity-protected decision exchange

The authorization request and response cross the boundary through an authenticated,
integrity-protected interface. The decision is bound to the relevant principal,
action, resource, parameters, tenant, context, Policy version, and validity period as
required by the assessed authorization model.

### SP-4: No Agent-authored authority

The PEP does not treat a model-produced field, Agent-produced claim, local flag, or
unsigned decision object as proof of authorization. Trusted identity and entitlement
attributes are obtained or verified outside the Agent-controlled context.

### SP-5: No effective in-process or local fallback

Production-equivalent paths do not silently fall back to an embedded allow decision,
stale permissive cache, default permit, or Agent-controlled Policy when the isolated
PDP cannot be reached or returns an invalid response.

### SP-6: Bypass resistance sufficient to exercise the isolated PDP

The assessed action path cannot reach the protected Tool or resource while avoiding
the PDP-backed enforcement path. This property establishes that the isolated PDP is
security-relevant; broader complete-mediation assurance remains a related control
concern.

### SP-7: Independent decision evidence

Authorization decision evidence is produced at the PDP or trusted enforcement
boundary and stored where the Agent runtime cannot modify or selectively suppress
it. Evidence correlates the request, decision, Policy version, and resulting action
without exposing unnecessary sensitive content.

### SP-8: Deployment and recovery preserve isolation

Startup, failover, rollback, disaster recovery, maintenance, and test modes preserve
the same trust separation or fail safely. The Agent cannot replace the PDP endpoint,
trust anchor, image, Policy bundle, or recovery configuration with an
Agent-controlled alternative.

## Threat and failure-mode rationale

An Agent may be manipulated through direct or indirect Prompt Injection, poisoned
Tool metadata or output, malicious retrieved content, a vulnerable dependency, or a
logic error. When the PDP shares the Agent's effective compromise boundary, any such
failure can gain access to the authorization logic itself. The attacker can then
change Policy, forge an allow result, suppress denials, redirect the decision path,
or erase evidence.

The following threat links are proposed and remain subject to human review. ATLAS is
a rolling adversary knowledge base; the relationships use the pinned `2026.08`
collection rather than silently inheriting later changes.

| Source snapshot | ID | Relationship | Strength | Rationale |
|---|---|---|---|---|
| MITRE ATLAS `2026.08` | `AML.T0053` AI Agent Tool Invocation | mitigates | partial | An isolated PDP can deny Tool actions outside trusted Policy even when the Agent requests them. It does not by itself constrain Tool capability, guarantee PEP coverage, or prove the Policy correct. |
| MITRE ATLAS `2026.08` | `AML.T0051` LLM Prompt Injection | context | context | Prompt Injection is one way to obtain influence over an Agent runtime. PDP isolation contains authorization impact after that influence; it does not prevent or detect Prompt Injection itself. |

Representative failure modes include:

- Policy evaluation is an Agent-process library whose inputs, code path, or result
  can be patched by the Agent runtime.
- A sidecar has a nominally separate process but shares a writable filesystem,
  process namespace, administrative socket, service account, or unrestricted local
  network path with the Agent.
- The Agent can update Policy or trusted attributes using the same identity used to
  request ordinary actions.
- The PEP accepts an `authorized: true` field, role, tenant, or Policy result produced
  in model context.
- The Agent can call a Tool or downstream resource directly, leaving the isolated PDP
  as a decorative check on only one path.
- A PDP timeout, malformed response, network error, or cold-start race activates a
  permissive fallback.
- The Agent can redirect the PDP endpoint or replace its trust material during
  deployment or recovery.
- Decision logs are written only by the Agent, allowing successful abuse and denied
  attempts to be suppressed.

## Verification

Verification must use a production-equivalent deployment and the Agent's effective
runtime identity. A diagram or separate service name is not sufficient evidence.
Tests that could disrupt service or alter Policy must run in an authorized test
environment with recovery procedures.

### Architecture and configuration review

1. Trace at least one allowed and one denied Agent action from initiating identity
   through Agent, PEP, PDP, Tool or resource, and evidence store.
2. Inventory processes, containers, hosts, namespaces, service accounts, credentials,
   sockets, network paths, mounted storage, environment configuration, and
   administrative interfaces on both sides of the boundary.
3. Verify that the Agent identity has no Policy write, PDP administration, workload
   impersonation, deployment, debug, exec, secret-read, log-delete, or lifecycle
   permission over the PDP boundary.
4. Verify that trusted identity, tenant, entitlement, approval, and resource
   attributes do not originate solely in model or Agent-controlled context.
5. Inspect the decision protocol for peer authentication, integrity protection,
   request and response binding, expiry, replay handling, and Policy version.
6. Enumerate all direct, fallback, maintenance, batch, retry, cache, recovery, and
   emergency paths to the protected action.
7. Confirm that authoritative decision evidence is emitted outside the Agent runtime
   and protected by separate write and deletion permissions.
8. Compare production, staging, test, failover, and recovery configurations for
   weaker embedded or fail-open modes.

### Positive verification

| Test | Procedure | Expected result |
|---|---|---|
| P-1 Allowed action | Submit an action allowed for a known principal, resource, parameters, and tenant | PEP obtains a decision from the isolated PDP, the action succeeds, and independent evidence correlates request, decision, Policy version, and outcome |
| P-2 Policy-controlled denial | Submit the same action as a principal lacking the required entitlement | PDP returns deny, PEP prevents the action, and the protected resource shows no side effect |
| P-3 Authorized Policy change | Change a test Policy through the approved administrative path and repeat the request | The versioned change is attributable, takes effect through the PDP, and cannot be performed with the Agent identity |
| P-4 Recovery path | Exercise an approved PDP restart or failover procedure | Isolation, identity, Policy integrity, decision binding, and evidence continue to hold without an Agent-controlled fallback |

### Negative and abuse-case verification

| Test | Attempt from the Agent compromise boundary | Expected result |
|---|---|---|
| N-1 Policy tampering | Modify mounted Policy, Policy bundle, environment, local cache, or PDP configuration | Write is prevented or has no effect on the authoritative PDP; an alert or audit event is generated where required |
| N-2 Administrative access | Invoke PAP, debug, maintenance, deployment, impersonation, or emergency interfaces with the Agent identity | Authentication or authorization denies access; no Policy or lifecycle state changes |
| N-3 Decision forgery | Supply an Agent-created allow result or alter a legitimate PDP response | PEP rejects the result and the protected action does not occur |
| N-4 Decision replay or substitution | Replay a prior allow for a different principal, action, resource, parameter set, tenant, Policy version, or expired validity period | Binding or freshness checks reject the decision |
| N-5 Trusted-context tampering | Change model-visible identity, role, tenant, approval, or entitlement fields | PDP and PEP use independently verified context; the tampered request is rejected or evaluated under the authentic context |
| N-6 PDP bypass | Call the protected Tool, API, queue, datastore, or alternate protocol directly | Network, resource, or application enforcement blocks the path; no side effect occurs |
| N-7 PDP failure | Cause timeout, connection refusal, malformed response, unavailable Policy, or startup race | The action fails closed; no local or cached default-permit path is selected |
| N-8 Endpoint redirection | Change service discovery, DNS, environment, proxy, certificate trust, or local routing available to the Agent | The decision channel cannot be redirected to an Agent-controlled PDP; peer validation fails safely |
| N-9 Runtime escape attempt | Use the Agent's effective OS or orchestrator privileges to inspect PDP memory, filesystem, secret, namespace, or process control | Isolation prevents access within the stated threat model; any successful access invalidates the claimed boundary |
| N-10 Evidence tampering | Delete, rewrite, suppress, or selectively omit PDP or PEP decision evidence | Agent identity is denied; independent evidence remains complete enough to correlate the test |

### Failure conditions

The Control fails when any of the following is observed within the declared scope:

- the authoritative PDP executes in Agent-controlled process memory;
- the Agent can modify Policy, trusted decision inputs, PDP configuration, code,
  identity, lifecycle, or trust anchors;
- the Agent can forge, alter, substitute, or replay an allow decision successfully;
- the assessed protected action can bypass the PDP-backed enforcement path;
- PDP failure causes default permit or an Agent-controlled fallback;
- an implementation label such as "sidecar" or "separate service" is the only
  evidence of isolation;
- no negative test exercises the Agent's effective runtime privileges;
- authoritative decision evidence exists only in Agent-writable storage;
- the claimed boundary excludes a deployment, recovery, or administrative path that
  gives the Agent equivalent control.

Missing evidence is not automatically evidence of failure in the deployed system,
but it prevents the verifier from concluding that this Control is satisfied.

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Authorization architecture and data-flow record | System architect or reviewed architecture source | Agent, PEP, PDP, PAP/PIP, protected resources, administrative and recovery paths | Current deployed design and after material boundary changes | Version controlled; sensitive endpoints and identities may require restricted storage | Shows the effective compromise boundary and every authorization path, not only component names |
| Runtime identity and privilege inventory | Identity platform, orchestrator, host, or cloud control plane | Agent and PDP workload identities, roles, service accounts, impersonation and admin permissions | Captured from the assessed environment; renewed after IAM or deployment changes | Collected by a principal independent of the Agent; redact secrets | Demonstrates that the Agent cannot administer, impersonate, inspect, or modify the PDP boundary |
| Deployment and isolation configuration | Build/deployment system and runtime control plane | Process, container, host, namespace, mount, network, secret, and lifecycle boundaries | Corresponds to the tested release and environment | Integrity protected and attributable to a reviewed deployment revision | Effective settings support SP-1, SP-2, and SP-8; labels alone are insufficient |
| Decision-channel configuration | PDP/PEP owner or service-mesh/API control plane | Peer identity, trust anchors, authorization request and response protocol | Current configuration and after trust or protocol changes | Protect private keys and sensitive attributes; preserve configuration provenance | Demonstrates authenticated peers, integrity, binding, expiry, and safe error handling |
| Policy administration evidence | PAP, Policy repository, and deployment pipeline | Policy change identities, approvals, versioning, signing, and rollback | Current workflow plus sampled recent change | Agent has no write/delete authority; audit is tamper resistant | Only separately authorized administrators or automation can change authoritative Policy |
| Positive and negative test results | Approved security test harness and protected-resource observer | P-1 through P-4 and applicable N-1 through N-10 | For the assessed release; repeat after material identity, isolation, Policy, PEP, PDP, or recovery changes | Raw results retained outside Agent write control; sanitize sensitive data | Expected decision and resource outcome are both observed; no unauthorized side effect or fail-open path |
| Correlated decision and action records | PDP, PEP, protected resource, and independent logging pipeline | Sampled allowed, denied, failed, and bypass attempts | Runtime evidence from the assessed deployment window | Access controlled, integrity protected, retention defined, minimal necessary sensitive content | Principal, action, resource, context, Policy version, decision, correlation identifier, and outcome can be reconciled |
| Exception and residual-risk record | Named Control owner and risk authority | Untested paths, accepted shared infrastructure, unavailable evidence, compensating controls | Current and reviewed after relevant change or incident | Durable human approval; no production secrets | Every excluded path or weakened boundary has an owner, rationale, expiry or review condition, and stated impact |

Production evidence, credentials, full Policy containing confidential rules, customer
data, and sensitive decision payloads remain outside this public repository. Store
only sanitized examples and evidence expectations here.

## Related requirements

| Requirement | Relationship and distinction |
|---|---|
| `v1.0-C5.2.1` | Establishes access control over AI resources. C5.2.5 asks whether the Agent can control the decision authority used for Agent authorization. |
| `v1.0-C9.5.1` | Requires fine-grained runtime Policy over Tool and parameter use. It addresses decision scope; C5.2.5 addresses the PDP's compromise boundary. |
| `v1.0-C9.5.3` | Keeps access-control decisions in application logic or a Policy engine rather than the model. C5.2.5 is stricter about isolating the PDP from the broader Agent execution environment, not only from model reasoning. |
| `v1.0-C9.5.6` | Requires re-evaluation on privileged actions in long-running sessions. It addresses decision freshness; C5.2.5 addresses decision-authority isolation. |
| `v1.0-C9.6.3` | Requires an isolated out-of-band kill-switch path. It is analogous control-plane separation for shutdown, not ordinary authorization decisions. |

Passing this Control must not be presented as satisfying any related requirement in
full. No Engineering Pattern Mapping has been assessed.

## Known limitations and uncertainty

- PDP isolation does not prove that Policy grants the correct authority or that its
  specification is complete, conflict-free, and current.
- It does not independently prove PEP correctness, complete mediation, trusted
  identity, parameter validation, least privilege, delegation integrity, approval
  integrity, credential isolation, or Tool sandboxing.
- A separate service can share a cloud account, cluster administrator, host kernel,
  service mesh, certificate authority, deployment pipeline, or logging control plane
  with the Agent. The declared threat model must state which shared dependencies are
  trusted and why.
- A sidecar may reduce accidental coupling without resisting a container escape,
  node compromise, shared-volume write, workload-identity theft, or orchestrator
  administration. Deployment topology alone is not an assurance level.
- Fail-closed behavior can reduce availability. Operational design must distinguish
  actions that may safely degrade from actions that must stop, without converting
  an outage into default permit.
- Cached decisions can preserve separation while weakening freshness and binding.
  Their scope, integrity, expiry, invalidation, and replay properties require
  explicit verification.
- Independent logs support detection and investigation but do not prevent the first
  unauthorized attempt.
- No ratified Agent-specific PDP isolation protocol defines interoperable request,
  intent-provenance, and parameter-binding semantics in the reviewed AISVS Research
  snapshot. Product-specific protocols require explicit assumptions and tests.
- The strongest achievable boundary depends on the Agent's effective privilege and
  the protected action's impact. This Control does not assign a universal process,
  container, host, account, or hardware isolation level.

## References

- [OWASP AISVS v1.0 C5 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [OWASP AISVS C5.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-02-AI-Resource-Authorization-Classification.md)
- [OWASP AISVS v1.0 C9 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
- [MITRE ATLAS `2026.08` source snapshot](https://github.com/mitre-atlas/atlas-data/blob/41d4f5ca4112f0e492ffaa3ebff07dc80a75afa5/dist/v6/ATLAS-2026.08.yaml)
- [NIST SP 800-207, Zero Trust Architecture](https://doi.org/10.6028/NIST.SP.800-207)
- [NIST SP 800-192, Verification and Test Methods for Access Control Policies/Models](https://doi.org/10.6028/NIST.SP.800-192)

## Review record and changelog

Human review is required before this Control is mature. `verifiable` records content
depth; it does not grant `reviewed` status.

| Date | Change or review scope | Author or reviewer | Evidence |
|---|---|---|---|
| 2026-09-03 | Initial verifiable draft prepared for human product-security review | Codex authoring agent; not a reviewer | Pending repository commit and human review |
