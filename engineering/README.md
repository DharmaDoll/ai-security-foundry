# Engineering Patterns

## Scope

Engineering-facing entry point. Organize by relatively stable technologies/trust boundaries, not external Top 10 chapter order. Threat and defense belong together inside each concrete pattern.

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

Pattern化前の候補比較は [`pattern-landscape.md`](pattern-landscape.md)、段階的な開発優先順位と
ドメインの責務は [`plan.md`](plan.md) に定義する。普遍的な候補発見手法は
[`docs/pattern-discovery.md`](docs/pattern-discovery.md)を使用する。
