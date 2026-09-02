# Initial Plan

Keep the repository small until the pattern format and maintenance workflow are proven.

## Phase 0 — Repository foundation

- [x] Define repository mission and two-entry-point model
- [x] Define engineering taxonomy
- [x] Define external source roles
- [x] Create source registry
- [x] Create Codex/agent operating policy
- [x] Create security-pattern template
- [x] Create upstream-update review template
- [ ] Choose repository license
- [x] Define ownership/reviewer policy for `recommended` status

## Phase 1 — Prove the pattern model

Build a small set of high-value patterns before expanding coverage.

These candidates come from recurring system security problems and attack scenarios,
not from framework or control coverage targets.

- [ ] `agents/secure-tool-execution`
- [ ] `rag/secure-multi-tenant-retrieval`
- [ ] `llm/indirect-prompt-injection-containment`
- [ ] `mcp/secure-server-authorization`
- [ ] `skills/secure-skill-onboarding-and-updates`

For each pattern:

- [ ] Threat model is explicit
- [ ] Security invariants are testable
- [ ] Insecure/failure design is shown
- [ ] Recommended architecture is shown
- [ ] Minimal implementation example exists where useful
- [ ] Negative/abuse test exists
- [ ] Observability guidance exists
- [ ] Source versions/maturity are recorded

## Phase 2 — Maintenance workflow

- [ ] Assess mappings separately after independently developed endpoints are reviewable
- [ ] Asserted mappings have technical rationale, strength, and source-state metadata
- [ ] Preserve explicit no-match and gap outcomes without changing endpoint maturity

- [ ] Validate the source-registry schema after first real framework update
- [ ] Define a machine-readable mapping schema only after pattern metadata stabilizes
- [ ] Add a scheduled upstream-change detector
- [ ] Make the detector create an issue/report rather than directly modifying guidance
- [ ] Add semantic-diff/impact-analysis workflow for standards updates
- [ ] Add stale-review reporting based on `last_reviewed`

## Phase 3 — Expand engineering coverage

- [ ] Agent identity and credentials
- [ ] Memory poisoning and integrity
- [ ] RAG corpus ingestion and poisoning
- [ ] Sensitive-data handling and output controls
- [ ] AI/model/software supply-chain integrity
- [ ] Sandboxing and code execution
- [ ] Inter-agent communication
- [ ] AI security logging and incident evidence
- [ ] Model/provider boundary and fallback behavior

## Phase 4 — Developer adoption

- [ ] Add a concise secure-design checklist
- [ ] Add architecture-review examples
- [ ] Add CI examples for security regression tests
- [ ] Add discoverability index by use case
- [ ] Add discoverability index by framework
- [ ] Track adoption/feedback without turning framework coverage into the primary KPI
