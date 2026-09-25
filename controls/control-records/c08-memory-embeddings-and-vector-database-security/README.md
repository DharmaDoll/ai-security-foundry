# AISVS C8 Memory, Embeddings & Vector Database Security

対象はAISVS v1.0、固定Revision `78775233666a2022dcfb82037e5e029116955c00`。
以下は原文の代替や製品適合チェックリストではなく、C8の保証境界と整備済みControlへの入口である。
全11要件の分析と段階的な着手順序は[C8全体分析](../../docs/c08-landscape.md)を参照する。

## Category：C8 Memory, Embeddings & Vector Database Security

| 問うこと | できてはいけないこと |
|---|---|
| 将来のModel判断へ再利用されるMemory／Vectorを、正しい主体・出所・期限・信頼状態に基づいて書込み、検索、除外できるか。 | Similarity、同じTenant、過去の成功、Agent生成という理由だけで、未認可・汚染・期限切れ・検疫中DataをTrusted Contextへ戻す。 |

## Sectionの見取り図

| Section | 問うこと | できてはいけないこと |
|---|---|---|
| C8.1 Access Controls on Memory & RAG Indices | Tenant Identity、Metadata、Caller Scopeを全Write／Retrieval Pathで維持できるか。 | ID衝突、Metadata改ざん、Filter omission、Cache／Graph Pivotで別ScopeのRecordへ到達する。 |
| C8.2 Embedding Sanitization & Validation | Embedding／Trusted Memoryへ入れる前にSensitive Data、異常、Source、操作目的、矛盾を検査できるか。 | Agent／Tool Outputや検索操作用Contentを未検証のまま永続的なTrusted Memoryへ昇格する。 |
| C8.3 Memory Expiry & Revocation | Expiry、Reset、Quarantineを全Index／Cache／Replicaへ強制し、状態を検証できるか。 | TombstoneやFlagを付けただけで、別検索経路・Backup Restore・Background Writerから再出現させる。 |

## 整備済みRequirement

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C8.1.1](v1.0-c8.1.1-tenant-unique-vector-identifiers-and-namespaces/README.md) | 1 | Vector ID／NamespaceをTenantごとに一意・衝突不能にしているか。 | Client指定Tenant、Default Namespace、正規化差により別Tenant Recordを上書き・検索する。 |
| [C8.1.2](v1.0-c8.1.2-immutable-document-metadata-tags/README.md) | 2 | Security／Provenance Metadata Tagを初回Write後に不変としているか。 | Restricted／Poisoned RecordのOwner、Classification、SourceをSilentにTrusted値へ書き換える。 |
| [C8.1.3](v1.0-c8.1.3-retrieval-scope-enforcement/README.md) | 2 | 全Retrieval／Cache／ExpansionでTrusted Scopeを強制しているか。 | SimilarityやBroad Service AuthorityだけでUnauthorized Candidateを取得・展開・再利用する。 |
| [C8.2.1](v1.0-c8.2.1-sensitive-field-handling-before-embedding/README.md) | 1 | Sensitive FieldをEmbedding前に検出し、Policyに従って変換または除外しているか。 | Raw値をEmbedding Provider、Vector、Metadata、Logへ流す。 |
| [C8.2.2](v1.0-c8.2.2-vector-anomaly-quarantine-before-production/README.md) | 2 | 通常Clusterから外れるVectorをProduction Index投入前に検出・検疫しているか。 | Productionで検索可能になった後に検出する、またはFlagだけで利用を継続する。 |
| [C8.2.3](v1.0-c8.2.3-source-validated-trusted-memory-writes/README.md) | 2 | Agent／Tool OutputのSourceを検証してからTrusted Memoryへ昇格しているか。 | 生成結果やTool Outputを、その生成主体自身の判断だけで自動昇格する。 |
| [C8.2.4](v1.0-c8.2.4-retrieval-manipulation-screening-before-vectorization/README.md) | 3 | Retrieval操作用に細工されたContentをVectorization前に検出し、拒否または検疫しているか。 | 単一の整形済みTextだけを検査し、別Loader、Hidden Layer、OCR、Metadata経路を迂回させる。 |
| [C8.2.5](v1.0-c8.2.5-memory-contradiction-detection-and-alerting/README.md) | 3 | 新規Memoryと関連する既存Memoryの矛盾を検出し、調査可能なAlertを発生させているか。 | 矛盾する値をSilentに上書き、破棄、または区別なしで共存させる。 |
| [C8.3.1](v1.0-c8.3.1-expired-vector-retrieval-exclusion/README.md) | 2 | 期限切れVectorを全Production Retrieval経路から除外しているか。 | Primary Vector Storeだけ更新し、Lexical Index、Cache、Replica、Restore後の経路から再出現させる。 |
| [C8.3.2](v1.0-c8.3.2-complete-memory-reset/README.md) | 2 | 宣言したMemory範囲を完全かつ観測可能にResetできるか。 | Session履歴だけを消し、Summary、Cache、Background Writer、旧SnapshotからMemoryを復活させる。 |
| [C8.3.3](v1.0-c8.3.3-quarantine-retention-and-retrieval-exclusion/README.md) | 3 | Quarantine Contentを調査用に保持しつつ、全Production Retrievalから除外しているか。 | Filter漏れで再取得させる、または即時削除してForensic Evidenceを失う。 |

未整備Requirementの行やPlaceholderは作らない。個別Controlが`verifiable`になった時点で追加する。
学習進捗とControl maturityは独立している。

## Source

- [AISVS v1.0 C8要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [AISVS v1.0 C8 Research概要](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-Memory-and-Embeddings.md)
- [AISVS v1.0 C8.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-01-Access-Controls-Memory-RAG.md)
- [AISVS v1.0 C8.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-02-Embedding-Sanitization-Validation.md)
- [AISVS v1.0 C8.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-03-Memory-Expiry-Revocation-Leakage-Prevention.md)
