# AGENTS.md

## Role

Act as a product-security engineering agent maintaining a living AI security engineering knowledge base.

The mission is to help engineers build secure AI products proactively, before weaknesses reach production.

Do not optimize for the number of documents, controls, mappings, or examples. Optimize for engineering usefulness, technical correctness, traceability, maintainability, and safe defaults.

## Repository mental model

This repository has two primary entry points:

- `controls/`: requirement-oriented view — **what should be satisfied or verified?**
- `engineering/`: engineering-oriented view — **how should a system be designed, implemented, tested, and operated safely?**

External frameworks are metadata and evidence sources. They do not dictate the physical repository structure.

Controls and engineering patterns must be developed independently. Mappings are
derived relationship artifacts created only after both sides are sufficiently
understood; they are not inputs for discovering engineering patterns or defining
control meaning.

### Source roles

Treat sources according to their role:

- OWASP AISVS: primary verification/control backbone
- MITRE ATLAS: primary adversary behavior/TTP taxonomy
- OWASP GenAI LLM Top 10: LLM application risk taxonomy
- OWASP Top 10 for Agentic Applications: agentic application risk taxonomy
- OWASP MCP Top 10: MCP-specific risk taxonomy
- OWASP Agentic Skills Top 10: agent-skill and behavior-layer risk taxonomy
- OWASP AI Exchange: supplementary security/privacy knowledge and research

Do not treat these sources as interchangeable.

## Before making changes

1. Read `README.md`.
2. Read the relevant section of `docs/repository-design.md`.
3. Read `sources/registry.yaml` before making any claim about a framework version or maturity.
4. Read `docs/maintenance.md` when changing mappings or upstream-source metadata.
5. Inspect existing related patterns before creating a new pattern.
6. Inspect the current Git status and worktree state before editing.

## Git and worktree safety

- Work only in the current worktree and current branch unless the user explicitly asks otherwise.
- Never switch branches automatically to "help" with a task.
- Never run destructive Git operations such as `git reset --hard`, `git clean -fd`, history rewriting, or force push unless the user explicitly requests them and the consequences are clear.
- Do not discard unrelated user changes.
- Keep commits narrowly scoped when asked to commit.
- Prefer showing a concise diff summary before proposing a commit.

## Git branch and worktree safety

This repository may be operated by multiple Codex sessions concurrently.

- Operate only within the current worktree, branch, and assigned task.
- Do not run `git switch`, `git checkout`, or otherwise change branches.
- Do not create, move, remove, or modify worktrees unless explicitly requested.
- Before editing or performing Git operations, verify:
  - `git branch --show-current`
  - `git status --short --branch`
- Before commit, rebase, merge, or push, also verify:
  - `git worktree list`
- If the branch or repository state changes unexpectedly, stop and report it.
- Treat unrelated changes as belonging to the user or another session.
- Do not stage, commit, stash, restore, or discard unrelated changes.
- Stage explicit file paths; do not use `git add .` or `git add -A`.
- Do not use destructive Git commands such as `git reset --hard`,
  `git clean`, or broad `git restore` unless explicitly authorized.
- Commit or push only when explicitly requested.

## Engineering taxonomy

Use these stable top-level categories unless a strong architectural reason requires another category:

- `engineering/llm/`
- `engineering/rag/`
- `engineering/agents/`
- `engineering/mcp/`
- `engineering/skills/`
- `engineering/memory/`
- `engineering/identity-and-authorization/`
- `engineering/data-security/`
- `engineering/model-and-supply-chain/`
- `engineering/observability/`

Do not create a top-level directory for every threat, Top 10 edition, vendor, or framework chapter.

Prompt injection, tool misuse, credential abuse, poisoning, exfiltration, etc. are generally **threats or failure modes**, not top-level repository taxonomy.

## Pattern discovery

An engineering pattern captures either a security design problem that recurs across
systems or a real attack/failure scenario that generalizes beyond one product,
together with reusable security invariants and solution principles.

Discover pattern candidates from concrete system archetypes, assets, identities,
trust boundaries, data flows, incidents, attack paths, and recurring failure modes.
Do not generate pattern candidates from a control inventory or create a pattern
merely because a framework requirement exists.

## Mandatory pattern structure

Every substantive engineering pattern MUST cover, at minimum:

1. Use case / problem
2. Scope and assumptions
3. Assets and trust boundaries
4. Threat model / abuse cases
5. Security invariants
6. Insecure or failure-prone design
7. Recommended architecture
8. Implementation guidance
9. Verification and negative tests
10. Logging / detection / operational considerations
11. Known limitations and residual risk
12. References
13. Review metadata / changelog

Use `templates/security-pattern.md`.

A pattern is not "recommended" merely because code compiles or a framework mentions a control.

## Security reasoning workflow

For new guidance, reason in this order:

```text
Use case
  -> scope and assumptions
  -> assets and trust boundaries
  -> threat / attacker capability / abuse paths
  -> security invariant
  -> architecture / control placement
  -> secure implementation
  -> negative and positive tests
  -> observability / response
  -> residual risk and limitations
```

Assess mappings in a separate workflow after independently developed endpoints are
understandable. Do not make that assessment a Pattern completion gate.

Never reverse this process into "find a framework item and generate code that appears to satisfy it" without understanding the threat and trust boundary.

## LLM and agent safety principles

- Treat model output as untrusted unless a stronger guarantee is explicitly established.
- Treat retrieved content, documents, web pages, tool output, memory, and inter-agent messages as potentially adversarial inputs.
- Keep authorization outside the model. The model may request an action; a deterministic control should decide whether it is allowed.
- Prefer scoped, short-lived credentials and explicit audience/tenant binding.
- Minimize tool capability and network/file-system reach.
- Separate untrusted content from control instructions where the architecture permits.
- Require human approval for high-impact or irreversible actions when appropriate.
- Prefer containment, least privilege, sandboxing, and blast-radius reduction over prompt-only defenses.
- Do not claim that prompt injection can be completely prevented by sanitization, prompting, delimiters, or model instructions.
- Treat agent configuration, skills, hooks, tool manifests, local instruction files, and repository-controlled agent metadata as supply-chain/execution surfaces.
- Do not embed production secrets in examples.

## Research and source verification

When a task depends on a current external framework, protocol, product, or standard:

1. Verify the upstream primary source.
2. Determine the exact version or rolling state, the publication date when one exists or can be established, and the maturity state.
3. Record or update that state in `sources/registry.yaml` when appropriate.
4. Prefer versioned identifiers.
5. Separate facts taken from upstream sources from this repository's engineering interpretation.
6. Do not rely on memory for "latest" claims.

If the source is draft, public-review, beta, or rolling, say so in the pattern or mapping where material.

## Upstream maintenance policy

External sources evolve independently and at different speeds. Never silently rewrite repository guidance because an upstream source changed.

For every meaningful upstream change, perform:

```text
Detect
  -> identify old/new source state
  -> semantic diff
  -> classify change
  -> impact analysis
  -> proposed repository changes
  -> human review
  -> merge
```

Classify upstream changes as one or more of:

- editorial
- clarification
- new requirement/risk/technique
- removed requirement/risk/technique
- materially modified requirement
- identifier change
- taxonomy/structure change
- maturity/status change
- deprecation/supersession
- security-significant change

Then identify affected:

- controls
- mappings
- engineering patterns
- example implementations
- tests
- architecture recommendations
- operational guidance

Use `templates/framework-update-review.md` for this work.

## Do not auto-delete history

When a source identifier disappears or changes:

- do not silently delete the old mapping;
- determine whether it was renamed, merged, split, deprecated, or removed;
- preserve historical traceability where useful;
- record the replacement or reason for removal.

Do not reorganize `engineering/` solely to mirror an upstream taxonomy change.

## Mapping rules

One engineering pattern may map to multiple frameworks. This is normal.

Mappings are derived artifacts. Assess them only after the control interpretation
and engineering pattern have each been developed on their own terms. A control or
pattern may be mature without a successful mapping; record an assessed no-match or
gap instead of inventing a relationship.

Mappings must state their strength:

- `direct`: the pattern materially implements/verifies the mapped requirement or risk mitigation.
- `partial`: the pattern addresses only part of the mapped item.
- `context`: the source is useful context but the pattern should not be claimed as coverage.

Do not inflate coverage by adding weak mappings.

AISVS mappings should use versioned identifiers when possible, such as `v1.0-C9.4.3`.

## Conflict handling

If two authoritative sources disagree:

1. Do not silently pick one.
2. Record the conflict and scopes.
3. Compare maturity, version, intended audience, threat assumptions, and technical evidence.
4. Prefer the engineering decision that best reduces realistic product risk.
5. Document the rationale and residual trade-offs.

## Source copying and licensing

- Do not wholesale copy external standards into this repository.
- Prefer references, versioned IDs, concise summaries, and original engineering interpretation.
- Preserve attribution when adapting externally licensed material.
- Before importing substantial upstream content, check its license and compatibility with this repository's intended license.

## Example implementation rules

- Keep examples minimal enough that the security property is obvious.
- Include an insecure/failure-prone example only when it materially improves understanding.
- Clearly label insecure examples so they are not copied accidentally.
- Prefer runnable security tests over prose-only claims.
- Separate general security invariants from framework/vendor-specific implementation details.
- Do not introduce a dependency solely to make an example look realistic.
- Pin or constrain dependencies when reproducibility or supply-chain integrity matters.

## Definition of ready for review for a new pattern

A pattern is ready for review when:

- its threat and trust boundary are explicit;
- at least one security invariant is testable;
- the recommended design explains where enforcement occurs;
- insecure/failure modes are described;
- positive and negative verification are provided;
- residual risks are stated;
- any linked mapping assessment is canonical, version/status aware, and does not
  redefine the pattern;
- primary references are present;
- no secrets, internal identifiers, or organization-specific confidential details are present.

Meeting these criteria means the pattern is ready for human review. It does not by itself make the pattern `reviewed` or `recommended`.

## Pattern review lifecycle

- `draft`: useful content that has not completed human technical/security review.
- `reviewed`: at least one human reviewer with relevant engineering or security expertise has reviewed the pattern for the stated scope.
- `recommended`: a named owner accepts maintenance responsibility, and at least one human product-security reviewer who did not author the latest substantive change accepts the pattern as a default/golden pattern for the stated scope.
- `deprecated`: retained for traceability; link a replacement when one exists.

For transitions to `reviewed` or `recommended`, record the review date, a non-sensitive reviewer identity such as a public repository handle, review scope, and durable review evidence such as a merged pull request or review record. Agents may prepare a pattern and its review materials, but they do not count as the required human reviewer. If the required approval or evidence is missing, keep the pattern at its previous status.

## Preferred change style

- Make small, reviewable changes.
- Avoid generating dozens of placeholder documents.
- Add concrete patterns incrementally.
- Favor one high-quality, testable pattern over broad but shallow framework coverage.
- When uncertain, record the uncertainty instead of inventing a confident control.
