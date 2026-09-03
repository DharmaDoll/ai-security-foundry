# Engineering Patterns

## Scope

Engineering-facing entry point. Organize Pattern content under [`domains/`](domains/)
by relatively stable technologies and trust boundaries, not external Top 10 chapter
order. Threat and defense belong together inside each concrete Pattern.

## Pattern rule

A Pattern captures either a security design problem that recurs across systems or a
real attack/failure scenario that generalizes beyond one product, together with
reusable security invariants and solution principles.

Discover Pattern candidates from concrete system archetypes, assets, identities,
trust boundaries, data flows, incidents, attack paths, and recurring failure modes.
Do not generate them from a control inventory or add a document that merely restates
a framework item.

A concrete Pattern should define testable security invariants, recommend an
architecture and implementation approach, and provide verification. Mapping is a
later assessment between independently developed artifacts; an assessed no-match or
gap is valid. The canonical assessment belongs under `mappings/` and is not a
Pattern maturity requirement.

Use `templates/security-pattern.md` for new patterns.

## Navigation

- 横断的なEngineering資料と調査記録: [`docs/README.md`](docs/README.md)
- Patternを配置するEngineering Domain: [`domains/README.md`](domains/README.md)
- 段階的な開発計画とDomainの責務: [`plan.md`](plan.md)
- Pattern化前の候補比較: [`docs/pattern-landscape.md`](docs/pattern-landscape.md)
- 普遍的な候補発見手法: [`docs/pattern-discovery.md`](docs/pattern-discovery.md)
