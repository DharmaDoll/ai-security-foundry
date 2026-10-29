# Memory

## Scope

Persistent/long-lived agent memory and context: write authorization, provenance, poisoning, tenant isolation, retention, recovery, and safe retrieval.

## Patterns

- [PATTERN-MEMORY-001：本人の回答設定を保存し、次の会話へ安全に渡す](authorized-memory-lifecycle/README.md) — `draft`。既存プロフィールAPIを主例に、保存・再読込み・取消しの境界を扱う。[実装例](authorized-memory-lifecycle/implementation-notes.md)・[確認用チェックシート](authorized-memory-lifecycle/negative-tests.md)。
- [PATTERN-MEMORY-002：案件の引継ぎメモを、翌日の指示や承認にしない](persistent-context-poisoning-containment/README.md) — `draft`。自由文要約の全出所・元資料の版・現在の権限を確認して再利用する。[実装例](persistent-context-poisoning-containment/implementation-notes.md)・[確認用チェックシート](persistent-context-poisoning-containment/negative-tests.md)。

## 選定と進捗

P5の型付き本人設定とP6の自由文要約は適用範囲を分ける。選定理由は[P5](../../docs/pattern-landscape.md#p5-scope-proposal)・[P6](../../docs/pattern-landscape.md#p6-scope-proposal)、成果物の状態は[P5計画](../../plan.md#p5-implementation-plan)・[P6計画](../../plan.md#p6-implementation-plan)を参照。本文はいずれも人の技術レビュー待ち。

## Pattern rule

Add a Pattern only for a security design problem or attack scenario that recurs
across systems or credibly reusable contexts. Start from the system and threat, not
from a control inventory. Develop the Pattern independently; any mapping is assessed
later as a separate artifact under `mappings/`.

Use `templates/security-pattern.md` for new patterns.
