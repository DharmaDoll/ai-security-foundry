# MCP

## Scope

MCP-specific client/server/tool trust, authorization, token/audience boundaries, server provenance, tool discovery, protocol and transport security.

## Pattern rule

Add a Pattern only for a security design problem or attack scenario that recurs
across systems or credibly reusable contexts. Start from the system and threat, not
from a control inventory. Develop the Pattern independently; any mapping is assessed
later as a separate artifact under `mappings/`.

Use `templates/security-pattern.md` for new patterns.

## Patterns

- [MCPから下流APIを、利用者本人の権限で呼ぶ](audience-bound-downstream-delegation/README.md) — `PATTERN-MCP-001`、`draft`。注文照会を入口から追い、本人の資格の引継ぎと下流APIでの対象認可を説明する。[正常系・Negative testチェックシート](audience-bound-downstream-delegation/negative-tests.md)付き。
