# Agents

## Scope

Planning, autonomous/semi-autonomous action, tool execution, delegation, approval, sandboxing, blast radius, inter-agent behavior, and action integrity.

## Pattern rule

Add a Pattern only for a security design problem or attack scenario that recurs
across systems or credibly reusable contexts. Start from the system and threat, not
from a control inventory. Develop the Pattern independently; any mapping is assessed
later as a separate artifact under `mappings/`.

Use `templates/security-pattern.md` for new patterns.

## Patterns

- [Agentのツール実行を、利用者の権限内に閉じ込める](secure-tool-execution/README.md) — `draft`（構成選択を改訂し、再レビュー待ち）。照会・提案で足りるかを選び、必要な場合だけ実行権限を追加する設計ガイド。
  [Negative testチェックシート](secure-tool-execution/negative-tests.md)で、越境・改ざん・失効・障害・迂回を確認する。
