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

- [MCPの接続構成と、下流APIを呼ぶ主体を選ぶ](audience-bound-downstream-delegation/README.md) — `PATTERN-MCP-001`、`draft`。Oktaのローカル直接認証を主例に、実行場所・権限の主体・資格の保持を選ぶ。[正常系・Negative testチェックシート](audience-bound-downstream-delegation/negative-tests.md)付き。
