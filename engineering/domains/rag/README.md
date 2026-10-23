# RAG

## Scope

Retrieval ingestion, corpus trust, authorization-aware retrieval, provenance, poisoning resistance, tenant isolation, and retrieval/output security.

## Pattern rule

Add a Pattern only for a security design problem or attack scenario that recurs
across systems or credibly reusable contexts. Start from the system and threat, not
from a control inventory. Develop the Pattern independently; any mapping is assessed
later as a separate artifact under `mappings/`.

Use `templates/security-pattern.md` for new patterns.

## Patterns

- [RAG検索で、利用者に許可された文書だけを渡す](secure-multi-tenant-retrieval/README.md) — `draft`。異なる会社と会社内の文書権限を、検索・断片・引用・キャッシュで強制する設計ガイド。
  [正常系・Negative testチェックシート](secure-multi-tenant-retrieval/negative-tests.md)で、越境・条件欠落・失効・経路の迂回を確認する。
  [実装ノート](secure-multi-tenant-retrieval/implementation-notes.md)では、本文と同じ①〜⑤をPostgreSQLで実装する流れを追える。
  [構成の選び方](secure-multi-tenant-retrieval/access-control-options.md)では、権限の管理元・強制箇所・格納先の分離を順に決める。
