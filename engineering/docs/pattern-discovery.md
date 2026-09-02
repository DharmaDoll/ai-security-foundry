# Engineering Pattern Discovery Method

## Purpose

This document defines the repository-wide method for discovering engineering
Pattern candidates. The method is independent of any control framework, threat
taxonomy, product, or AI technology.

A Pattern captures either:

- a security design problem that recurs across systems; or
- a real attack or failure scenario that can be generalized beyond one product;

together with reusable Security Invariants, deterministic Enforcement Points,
verification, and limitations.

Pattern discovery is not Pattern development. A candidate recorded in the Landscape
is not a lifecycle `draft`, and no Pattern directory should be created until the
candidate passes the promotion gate.

## Discovery sources and their roles

Use multiple evidence types. Their roles are different.

| Evidence source | Use in discovery | Do not infer |
| --- | --- | --- |
| Real system archetypes and data flows | Identify assets, identities, Trust Boundaries, and side effects | That one product-specific implementation is universally reusable |
| Incidents and postmortems | Establish realized attack paths, impacts, and failed assumptions | That the reported remediation is complete or generally correct |
| Security research and red-team exercises | Establish demonstrated abuse paths and test ideas | That laboratory preconditions always apply in production |
| Threat taxonomies such as MITRE ATLAS | Find attacker behaviors, procedures, case studies, and recurring attack-path components | One Pattern per tactic or Technique ID |
| Risk taxonomies | Check whether important failure modes were omitted | That a risk category defines a Pattern boundary |
| Protocol and platform specifications | Establish normative behavior and concrete security boundaries | That the protocol structure should become the repository taxonomy |
| Controls and verification standards | Later corroborate assurance properties and verification expectations | Pattern candidates derived from control inventory or coverage gaps |

Threat-taxonomy content may therefore be a primary discovery input. Its identifiers
become Mapping metadata only after the Pattern and the source item are independently
understood.

## Evidence snapshot

Before extracting observations from a changing source, record:

- authoritative source and URL;
- source version or rolling state;
- immutable revision when available;
- publication or retrieval date;
- upstream maturity labels;
- scope inspected;
- known gaps or source limitations.

Do not silently combine observations from incompatible source versions. Do not treat
an upstream maturity label as this repository's Pattern maturity.

## Discovery workflow

### 1. Define the engineering scope

State which kinds of systems and security outcomes are in scope. Exclude adversary
activity that does not reveal a defensible AI-system design problem for this
repository.

### 2. Extract observations

Normalize each system, incident, research result, or threat record into an
observation containing:

- source and immutable source state;
- system archetype and use case;
- assets and sensitive side effects;
- actors, identities, and attacker capability;
- preconditions and entry point;
- Trust Boundaries crossed;
- attack or failure steps;
- security outcome and impact;
- upstream evidence or maturity classification;
- uncertainty and missing information.

An observation describes evidence. It is not yet a Pattern candidate.

### 3. Reconstruct the abuse path

Express the observation without source-specific labels:

```text
Attacker capability
  -> entry point
  -> trusted or untrusted data/control transition
  -> missing or bypassed Enforcement Point
  -> privileged interpretation or action
  -> affected asset and security outcome
```

Preserve relevant timing, persistence, delegation, tenant, and audience boundaries.
These frequently determine whether apparently similar observations belong to
different Patterns.

### 4. Derive the Security Invariant

Ask what must remain true even if the model, agent, retrieved content, Tool,
dependency, or external service behaves incorrectly or maliciously.

A useful invariant is:

- tied to a specific security outcome;
- testable where practical;
- independent of one vendor or syntax;
- enforceable outside probabilistic model reasoning when it protects a security
  boundary;
- precise about identity, resource, tenant, audience, provenance, time, or side
  effect when relevant.

Do not begin with an upstream mitigation and rewrite it as an invariant.

### 5. Locate deterministic Enforcement Points

Identify where the invariant can be enforced using trusted state and deterministic
logic. Examples include:

- authorization gateway or policy engine;
- retrieval or storage layer;
- credential broker or token service;
- admission controller or artifact resolver;
- sandbox, operating-system boundary, or network proxy;
- context assembler or typed state gateway;
- output encoder, parser, or constrained interpreter;
- workflow state machine, quota service, or scheduler.

If no credible Enforcement Point exists, retain the item as an open engineering
problem rather than claiming a Pattern.

### 6. Define a falsifying Negative Test

Write at least one test that attempts to violate the invariant at the identified
boundary. The expected result must be an observable security outcome, such as
denial, isolation, bounded consumption, non-disclosure, or safe degradation.

A test that only checks an internal function call is insufficient.

### 7. Cluster observations

Cluster by the combination of:

- recurring design problem;
- relevant Trust Boundaries;
- Security Invariant;
- deterministic Enforcement Point;
- Negative Test outcome.

Do not cluster only because observations share words such as "prompt injection",
"poisoning", "agent", or "supply chain".

### 8. Merge, split, and challenge the cluster

Merge observations when they have materially the same invariant, enforcement
location, and verification strategy.

Split a cluster when it introduces one or more of:

- a new principal, tenant, audience, or delegation hop;
- a persistence or lifecycle boundary;
- a different interpreter or execution boundary;
- a different security outcome;
- an independent Enforcement Point;
- Negative Tests that cannot be expressed coherently in the same Pattern.

Reject or hold a cluster when it is only a product incident, framework label,
generic security principle, mitigation name, or broad problem family without a
coherent Enforcement Point.

### 9. Validate reuse

A candidate should normally have one of the following:

- evidence from at least two independent system archetypes;
- multiple independent incidents or demonstrated exercises; or
- one realized incident plus a defensible demonstration that the same invariant and
  Enforcement Point apply to another independent system context.

Technique-only or feasibility-only evidence may justify a hypothesis, but not
selection as a Golden Pattern. Record counterexamples and contexts where the
candidate does not apply.

### 10. Record the candidate

The candidate Landscape should record:

- provisional name and primary engineering domain;
- recurring design problem;
- supporting observations and their source state;
- Trust Boundaries;
- Abuse Cases;
- Security Invariants;
- deterministic Enforcement Points;
- falsifying Negative Tests;
- reuse evidence and counterexamples;
- nearest existing candidates or Patterns;
- merge, split, or non-integration rationale;
- evidence gaps and promotion status.

Keep candidates in one Landscape. Do not create a directory or Pattern document for
every candidate.

### 11. Select one candidate for development

Prioritize by:

- realistic security impact;
- strength of evidence;
- reuse across system archetypes;
- clarity and testability of the invariant;
- availability of deterministic enforcement;
- ability to keep the first scope reviewable;
- reviewer and long-term owner availability.

Framework coverage is not a selection criterion.

### 12. Develop the Pattern, then assess Mappings

After selection, create one `draft` Pattern using the Pattern lifecycle and template.
Develop it from the use case through verification and residual risk.

Only after the Pattern and another endpoint are independently understandable should
`mappings/` record a Mapping assessment. Discovery evidence IDs may later become
Mapping candidates, but their presence in research notes does not assert a Mapping.

## Candidate decision outcomes

Candidate comparison should end with one of:

- `retain`: coherent candidate, but not yet selected;
- `select`: approved for development as the next Pattern;
- `merge`: represented by another candidate or existing Pattern;
- `split`: contains distinct invariants or Enforcement Points;
- `hold`: plausible but lacks reuse evidence or an enforceable solution;
- `reject`: outside repository scope or not a reusable Pattern.

These are Landscape decisions, not Pattern review lifecycle states.

## Common discovery mistakes

- Creating one Pattern per Control, Technique, risk, product, or framework chapter.
- Treating source co-occurrence as proof that observations share an engineering
  solution.
- Starting from a mitigation name instead of deriving the invariant.
- Calling a principle such as least privilege a Pattern without a concrete boundary.
- Combining ingestion, retrieval, execution, persistence, and operations merely
  because they occur in one product.
- Splitting candidates by vendor when the invariant and enforcement are the same.
- Claiming reuse without an independent system context or evidence.
- Treating prompt instructions, model alignment, or a classifier as the sole
  Enforcement Point for high-impact operations.
- Performing Control or Framework Mapping before the Pattern boundary is stable.

## Applying the method to MITRE ATLAS

For an ATLAS discovery pass:

1. pin the official ATLAS data release and immutable revision;
2. inspect Techniques, sub-techniques, maturity, platforms, Mitigations, Case
   Studies, and `employs` relationships;
3. reconstruct multi-step case-study paths using `step-id` and `leads-to` where
   available;
4. distinguish realized incidents from exercises and feasible Techniques;
5. exclude generic Enterprise activity unless it exposes an AI-specific boundary;
6. group attack paths by boundary, invariant, enforcement, and Negative Test;
7. use ATLAS Mitigations as design prompts, not automatically accepted solutions;
8. record ATLAS IDs as discovery evidence without asserting Mapping coverage;
9. preserve the inspected release in the research record;
10. re-run the discovery diff when a later ATLAS release adds or materially changes
    Techniques or Case Studies.

The current applied analysis is documented in
[`mitre-atlas-pattern-discovery-2026-08.md`](mitre-atlas-pattern-discovery-2026-08.md).
