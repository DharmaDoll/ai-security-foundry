---
title: "期限切れVectorをRetrieval結果から除外する"
versioned_id: "v1.0-C8.3.1"
requirement_id: "C8.3.1"
verification_level: 2
family_id: "C8"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-03-Memory-Expiry-Revocation-Leakage-Prevention.md"
last_verified: "2026-09-24"
maturity: "verifiable"
mapping_assessment_refs: []
---

# 期限切れVectorをRetrieval結果から除外する

AISVS Verification Level: 2

学習資料：[C8.3 Memory Expiry & Revocation](../../../docs/learning/c08-memory-embeddings-and-vector-database-security/v1.0-c8.3-memory-expiry-revocation/learning.md)

## Upstream basis

AISVS `v1.0-C8.3.1`は、期限切れVectorがRetrieval結果から除外されることを求める。固定Revisionの要件本文と
C8.3 Researchを確認した。ResearchはDense Vectorだけでなく、Lexical／Hybrid Index、Cache、Replica、Restore後の
Snapshot等、同じContentを返し得る経路を検証対象としている。

## Interpretation

各Vector／Chunkに対する信頼できるExpiry Stateを、結果返却後の後処理ではなく各Retrieval Enforcement Pointで強制する。
Expiryが有効になったRecordは、定義済みPropagation SLOの後、どのProduction Retrieval経路からもCandidate、Score、
Metadata、Contextとして観測できてはならない。

## Security objective

Retention期限、Consent、契約、Access権、Source Validityを失ったContentが、残存IndexやCacheから将来のModel判断へ再流入し、
Stale Guidance、Sensitive Data Disclosure、Poisonの継続を引き起こすことを防ぐ。

## Applicability

TTL、Retention、Consent期限、Source失効等によりVector／Chunkが期限切れになり得るRAG、Memory、Semantic Cacheへ適用する。

### Non-applicability

評価対象に永続・再利用されるVector／Embeddingがなく、Request終了後に検索可能な派生状態も残らない場合は対象外にできる。
Expiry機能を実装していないこと自体は、対象外理由にならない。

## Scope and assumptions

- Expiry Authority、基準Clock、適用時刻、Propagation SLOを明示する。
- Logical ExclusionとStorage／Replica／BackupからのPhysical Deletionを別のMilestoneとして扱う。
- Vector以外の同一Contentを返すIndex／Cacheも、実効的なRetrieval Pathとして数える。
- Client指定FilterにExpiry Enforcementを委ねず、Trusted Server-side Policyとして合成する。
- Eventual Consistencyを理由に無期限の露出を許容しない。

## Assets, actors, identities, and trust boundaries

資産は期限付きContent、Vector、Chunk Metadata、Retention／Revocation Stateである。ActorはSource Owner、Retention Service、
Indexer、Retriever、Cache、Backup／Restore Operator、Callerである。Trust BoundaryはExpiry Stateから各Retrieval Candidate Setへ
移る地点にある。Enforcement PointはDense、Lexical、Hybrid、Graph、Direct-ID、Cacheを含むServer-side Retrieval Gateである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Vector／ChunkへTrusted Expiry Stateを結び付け、Callerが延長・解除できない。 |
| SP-2 | Expiryを全Production Retrieval PathでCandidate選択前または同等に強制する。 |
| SP-3 | 期限切れRecordをContentだけでなくID、Metadata、Score、件数、Contextからも観測させない。 |
| SP-4 | Cache、Replica、Derived Summary等へExpiry／Invalidationを定義済みSLO内で伝播する。 |
| SP-5 | Expiry Stateが欠落、不正、または確認不能な保護対象RecordをFail-openで返さない。 |
| SP-6 | Restart、Failover、Reindex、Snapshot Restore後もExpiry Stateと除外を維持する。 |

## Scope calibration and adjacent assurance

本ControlのPass条件はRetrievalからのLogical Exclusionであり、記憶媒体からの即時Physical Erasureではない。C8.3.3は疑わしい
ContentのForensic保持を伴うQuarantine、C8.1.3はCaller ScopeによるAuthorizationを扱う。期限内でもUnauthorizedなRecordは
C8.1.3で拒否され、期限切れならAuthorized Callerに対しても本Controlで除外される。

## Threat and failure-mode rationale

Primary Vector Storeで削除しても、BM25 Index、Semantic Cache、Replica、Derived Summary、復元Snapshotが同じContentを返せば、
期限切れは実効性を持たない。結果受領後のApplication FilterではScore、件数、Cache Key、Traceへ情報を残すこともある。

外部脅威IDは独立したMapping評価を実施していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Expiry AuthorityからVector／Chunk、各Index、Cache、Replica、Context AssemblyまでのState伝播と、Clock、SLO、Restore手順を追跡する。

### Positive verification

期限内Canaryが許可されたScopeで取得でき、無関係なRecordがExpiry処理の影響を受けないことを確認する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Unique Markerを持つVectorを期限切れにしてDense／Lexical／Hybrid検索 | SLO後は全経路でZero Result。SP-2〜SP-4 |
| N-2 | Direct-ID、Metadata Filter、Graph Expansion、Reranker、Semantic Cacheから取得 | ID、Score、Metadataを含め返らない。SP-2、SP-3 |
| N-3 | ClientがExpiry Filterを削除、未来時刻へ上書き、Clockをずらす | Trusted Policyが除外し、Caller変更を拒否する。SP-1、SP-5 |
| N-4 | Replica Failover、Service Restart、Reindexを行う | Expired Recordが再出現しない。SP-6 |
| N-5 | Expiry前Snapshotを隔離環境へRestoreし昇格判定を実行 | 現行Expiry Stateを再適用するまでProductionへ接続しない。SP-6 |
| N-6 | Cache InvalidationやIndex更新を遅延・失敗させる | SLO違反を検出し、影響経路を閉じるか安全に劣化する。SP-4、SP-5 |

### Failure conditions

期限切れRecordがいずれかのProduction Retrievalから返る、Application後処理だけで隠す、SLOがない、CallerがExpiryを解除できる、
またはRestart／Restoreで再出現する場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Expiry policy／state schema | Data／Security Owner | Expiry Authority、Clock、SLO、Record Class | Retention変更時 | Versionと承認を保持 | 誰がいつ何を期限切れにできるか明確 |
| Retrieval path inventory | Architecture Owner | 全Index、Cache、Replica、Restore経路 | Architecture変更時 | Review記録を保持 | Enforcement漏れがない |
| Expiry canary test | Test Harness | N-1〜N-6 | Retrieval／Storage変更後 | Synthetic Markerを使用 | SLO内Zero Resultと再出現防止を再現 |
| Expiry operation log | Trusted Lifecycle Service | Expiry Eventと各Path適用状態 | Event時 | Agentから変更不能 | 対象、時刻、完了／失敗経路を追跡可能 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C8.1.3` | Expiryとは独立して、CallerのRetrieval Scopeを全経路で強制する。 |
| `v1.0-C8.2.1` | Sensitive Fieldを保存前に削減する。Expiryは既に保存された状態の再利用を止める。 |
| `v1.0-C8.3.2` | IncidentやUser操作により、期限を待たずMemory範囲をResetする。 |
| `v1.0-C8.3.3` | Suspect Contentを保持したままProduction Retrievalから除外する。 |

## Known limitations and uncertainty

Logical ExclusionはRaw Storage、Backup、Provider内部Copyからの消去やModel Weightへの影響除去を保証しない。Distributed Systemでは
短い伝播遅延が残るため、SLOと安全なDegradationが必要である。AISVS本文は「Vector」の範囲や許容伝播時間を定義しないため、
製品ArchitectureとRiskに基づき明示する。

`verifiable`はArtifactの成熟度であり、製品適合やデータ消去法令への適合を意味しない。

## References

- [AISVS v1.0 C8要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [AISVS v1.0 C8.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-03-Memory-Expiry-Revocation-Leakage-Prevention.md)
- [C8全体分析](../../../docs/c08-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
