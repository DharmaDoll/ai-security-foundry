---
title: "Quarantine Contentを保持しつつ全Retrieval結果から除外する"
versioned_id: "v1.0-C8.3.3"
requirement_id: "C8.3.3"
verification_level: 3
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

# Quarantine Contentを保持しつつ全Retrieval結果から除外する

AISVS Verification Level: 3

学習資料：[C8.3 Memory Expiry & Revocation](../../../docs/learning/c08-memory-embeddings-and-vector-database-security/v1.0-c8.3-memory-expiry-revocation/learning.md)

## Upstream basis

AISVS `v1.0-C8.3.3`は、QuarantineされたContentを保持しながら、すべてのRetrieval結果から除外することを求める。
固定Revisionの要件本文とC8.3 Researchを確認した。ResearchはProduction Retrievalと制限されたForensic Accessを分離し、
Dense、Lexical、Hybrid、Cache、Agent Memory、Replica、Restore後の経路へ同一Quarantine Stateを適用する。

## Interpretation

Suspect Contentを`active`から`quarantined`へ遷移させ、原本、Provenance、検出理由、Integrityを調査用に保持する。一方、
ProductionのCandidate Selection、Direct Lookup、Cache、Context Assemblyからは一貫して除外する。Forensic Interfaceは通常のRetrieval
経路から分離し、明示的な調査権限と監査を要求する。

## Security objective

Poisoned、改ざん疑い、Policy違反のContentが調査中もModel／Agentへ影響し続けることを止めながら、原因分析、影響範囲特定、
Rollback判断、説明責任に必要な証拠を失わないようにする。

## Applicability

RAG、Vector Store、Long-term Memory、Semantic Cache、Shared Agent Memory等で、疑わしいContentを調査・復旧するSystemへ適用する。

### Non-applicability

評価対象に永続・検索可能なContentがなく、したがって保持または隔離すべき状態が存在しないSystemは対象外にできる。
Quarantine機能を持たず常にHard Deleteする設計は、本Requirementの対象外ではなく、保持要件を満たさない。

## Scope and assumptions

- Quarantine、Release、Purgeを別の認可された状態遷移として扱う。
- 「保持」はProductionで検索可能にすることを意味せず、Forensic Store／Interfaceへ厳格に限定できる。
- Quarantine StateはDocument、Chunk、Vector、Derived Summary、Cache Entry等の関連Artifactへ伝播する。
- Privacy Erasure、Legal Hold、Incident Evidence Retentionが衝突する場合は、Policy OwnerとLegal Reviewで解決する。
- Filter Flagだけに依存する場合、そのFilterを省略・改ざん・Injectionできないことを別途検証する。

## Assets, actors, identities, and trust boundaries

資産はSuspect Content、Provenance、Forensic Evidence、Production Retrieval Integrityである。ActorはDetector、Responder、Data Owner、
Forensic Reviewer、Retriever、Cache、Backup Operator、攻撃者である。Trust BoundaryはQuarantine DecisionからProduction／Forensicの
二つのRead Planeへ分岐する地点にある。Enforcement PointはLifecycle State Store、全Production Retrieval Gate、独立Forensic Authorizationである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Quarantine StateをTrusted Lifecycle Serviceが設定し、Content自身やModelが解除できない。 |
| SP-2 | Quarantined Contentを全Production RetrievalのCandidate、Result、Score、Metadata、Contextから除外する。 |
| SP-3 | 原本、Provenance、検出理由、Quarantine時刻、Integrityを調査可能な形で保持する。 |
| SP-4 | Forensic AccessをProduction Retrievalから分離し、明示的権限、目的、監査を要求する。 |
| SP-5 | Document／Chunk／Vector／Summary／Cache／Shared MemoryへQuarantine Stateを一貫して伝播する。 |
| SP-6 | Restart、Failover、Reindex、Backup Restore後もQuarantine Stateを優先し、再出現させない。 |
| SP-7 | Release／PurgeはQuarantine設定とは別に認可・記録し、対象と影響を検証してから実行する。 |

## Scope calibration and adjacent assurance

本Controlは「保持」と「全Production Retrievalからの除外」を同時に要求する。Hard DeleteだけではForensic保持を、別CollectionへのCopyだけで
元Indexを除外しなければ隔離を満たさない。C8.2.2／C8.2.4は疑わしいContentの検出と投入前検疫、本Controlは保存後を含むLifecycle
Stateの継続強制を扱う。Quarantine対象が真に悪性かを本Controlは保証しない。

## Threat and failure-mode rationale

攻撃者は一つでもFilterを省略するDense／Keyword／Direct-ID／Cache経路を使い、Quarantined Poisonを再取得させられる。一方、即時削除すると
近接Chunk、Query履歴、Source Provenanceを用いたImpact Analysisができず、再発防止やUnquarantine判断を誤る。

外部脅威IDは独立したMapping評価を実施していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

DetectionからState遷移、Artifact関連付け、全Production Read Path、Forensic Plane、Release／Purge、Backup／Restoreまでを追跡する。

### Positive verification

Active Contentが通常検索で利用でき、認可されたResponderだけがQuarantine RecordをForensic Interfaceから完全性検証付きで閲覧できることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Unique Marker付きDocument／ChunkをQuarantineしDense／Lexical／Hybrid検索 | 全Production結果がZero、Forensic Recordは保持。SP-2、SP-3 |
| N-2 | Direct-ID、Metadata Filter、Reranker、Graph Expansion、Semantic／Application Cacheを利用 | ID、Score、Metadataを含め返らない。SP-2、SP-5 |
| N-3 | Agent／Content Metadata／一般UserがFlag解除またはFilter省略 | Trusted Stateが優先され、解除・取得を拒否する。SP-1、SP-2 |
| N-4 | Production CredentialでForensic InterfaceへAccess | Denyし、Attemptを監査する。SP-4 |
| N-5 | Restart、Replica Failover、Reindex、Quarantine前Snapshot Restore | 現行Stateを再適用するまで接続せず、再出現しない。SP-6 |
| N-6 | Documentの一部Chunk、Summary、CacheだけをQuarantine対象から外す | Related Artifactを列挙し、一貫したStateへ収束する。SP-5 |
| N-7 | Quarantineと同時にRelease／Purge RequestをReplay | 独立AuthorizationとIdempotencyで意図しない復帰・消去を防ぐ。SP-7 |
| N-8 | Forensic Recordを改ざんする | Integrity検証に失敗し、証拠として利用せずAlertする。SP-3 |

### Failure conditions

いずれかのProduction Retrievalで返る、Flag省略で迂回できる、証拠が消える、Production IdentityでForensic Accessできる、または
Restart／RestoreでActiveへ戻る場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Quarantine state-machine／policy | Security／Data Owner | Set、Retain、Release、Purge | Policy変更時 | Versionと承認を保持 | 各TransitionのAuthorityと完了条件が明確 |
| Retrieval／artifact inventory | Architecture Owner | 全Read PathとDerived Artifact | Architecture変更時 | Review記録を保持 | 除外と伝播の漏れがない |
| Quarantine isolation test | Test Harness | N-1〜N-8 | Retrieval／Lifecycle変更後 | Synthetic Markerを使用 | Production Zero ResultとForensic保持を同時確認 |
| Forensic custody record | Trusted Lifecycle／Forensic System | Content、Hash、Provenance、Access | Event／Access時 | 改ざん検知、機密保護 | IntegrityとChain of Custodyを追跡可能 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C8.1.2` | Quarantine判定に必要なSecurity／Provenance Metadataの不変性を扱う。 |
| `v1.0-C8.1.3` | Production RetrievalでTrusted Scopeを強制する。Quarantineは許可Scope内でも優先される。 |
| `v1.0-C8.2.2` | Vector異常をProduction投入前に検出・検疫する。 |
| `v1.0-C8.2.4` | Retrieval操作用ContentをVectorization前に拒否・検疫する。 |
| `v1.0-C8.3.1` | 期限切れRecordのLogical Exclusionを扱い、Forensic保持は要求しない。 |
| `v1.0-C8.3.2` | 定義したMemory Scope全体をResetするRecovery Operationを扱う。 |

## Known limitations and uncertainty

Quarantineは未検出Poison、既に生成・送信されたOutput、外部Systemへ複製済みDataを回収しない。Metadata Filter方式はQuery Injectionや
Filter Omissionへ弱く、物理分離方式は移動のAtomicityと運用Costを伴う。Forensic RetentionとPrivacy Erasureの優先関係は技術だけでは
決められない。

`verifiable`はArtifactの成熟度であり、特定製品のQuarantine機能や法的保持義務への適合を意味しない。

## References

- [AISVS v1.0 C8要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [AISVS v1.0 C8.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-03-Memory-Expiry-Revocation-Leakage-Prevention.md)
- [C8全体分析](../../../docs/c08-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
