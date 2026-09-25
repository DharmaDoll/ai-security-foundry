---
title: "定義したMemory範囲を完全にResetできるようにする"
versioned_id: "v1.0-C8.3.2"
requirement_id: "C8.3.2"
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

# 定義したMemory範囲を完全にResetできるようにする

AISVS Verification Level: 2

学習資料：[C8.3 Memory Expiry & Revocation](../../../docs/learning/c08-memory-embeddings-and-vector-database-security/v1.0-c8.3-memory-expiry-revocation/learning.md)

## Upstream basis

AISVS `v1.0-C8.3.2`は、MemoryをResetできることを求める。固定Revisionの要件本文とC8.3 Researchを確認した。
本文はResetの粒度や物理削除を定義していない。ResearchはSessionだけでなくDerived Summary、Cache、Background Writer、
Shared Memory等を含むIncident Response Operationとして、再利用停止をEnd-to-endで確認する。

## Interpretation

製品が宣言したMemory Scopeについて、認可された主体がResetを開始でき、Primary Recordと検索可能な派生状態を定義済みの
完了条件まで無効化できるようにする。Reset中のBackground Write、Retry、Replica、Restoreが古いMemoryを再生成しないよう、
状態遷移をOrchestrateし、完了／部分失敗を観測可能にする。

## Security objective

Memory Poisoning、誤学習したPreference、Stale Context、User要求、Incident対応後に、過去の状態が将来の応答やActionへ残留・再出現する
ことを防ぎ、信頼できる状態から処理を再開できるようにする。

## Applicability

Conversation Memory、Long-term Memory、Trajectory、Summary、RAG Memory、Semantic Cache等をRequest／Sessionを越えて再利用するSystemへ適用する。

### Non-applicability

Request終了後に再利用可能な状態を一切保持せず、Cache、Summary、Tool Stateを含むDerived Memoryも存在しないStateless Systemは
対象外にできる。UI上の履歴削除だけを備えることは対象外理由にならない。

## Scope and assumptions

- Reset ScopeをTenant、User、Agent、Session、Task、Memory Class等で定義し、対象外状態も明記する。
- Resetは通常のRetention期限を待たずに実行できるOperationとする。
- Logical Reset、Forensic Retention、Physical Erasure、Model Unlearningを別の結果として扱う。
- Selective Resetは有用だが、上流本文が要求する粒度は曖昧であるため、製品がClaimする粒度ごとに完全性を検証する。
- Reset Authorityと対象ScopeはModel OutputではなくTrusted Identity／Policyから決める。

## Assets, actors, identities, and trust boundaries

資産はUser／Tenant Memory、Trajectory、Summary、Cache、Trust State、Reset Evidenceである。ActorはUser、Tenant Admin、Incident Responder、
Memory Service、Background Agent、Indexer、Backup Operatorである。Trust BoundaryはReset Commandから各Memory Store／Derived Writerへ移る
地点にある。Enforcement PointはReset Orchestrator、Write Fence、Store／Index／Cache Adapterである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Reset対象と権限をTrusted Identity／Policyで決め、ModelやClient指定Scopeだけを信頼しない。 |
| SP-2 | 宣言したScope内のPrimary Memory、Vector、Summary、Cache、TrajectoryをReset対象として列挙する。 |
| SP-3 | Reset開始後のBackground Write、Retry、Compaction、Replicationが旧世代Memoryを再投入しない。 |
| SP-4 | 完了後、旧Memoryを全Production Retrieval／Context Assemblyから利用できない。 |
| SP-5 | Partial Failureを成功として返さず、未完了経路を隔離して再試行または安全に停止する。 |
| SP-6 | Restart、Failover、Restore後もReset世代／Tombstoneを適用し、旧Memoryを復活させない。 |
| SP-7 | Initiator、Scope、開始／完了時刻、各経路の結果を監査可能にする。 |

## Scope calibration and adjacent assurance

本Controlは「Resetできる」というLifecycle Capabilityを扱い、常にMemoryを消去することや、疑わしい証拠を即時破棄することを求めない。
C8.3.3はForensic保持を伴うQuarantine、C8.3.1はExpiry時刻に基づく除外を扱う。Reset後に新しいClean Memoryを保存できることと、
過去のModel Weightから情報をUnlearnすることも別の保証である。

## Threat and failure-mode rationale

Session Storeだけを消しても、Summary、Semantic Cache、Tool Cache、Shared Memory、Background Heartbeatが残れば、Poisonや誤ったPreferenceは
次のSessionへ戻る。Resetと並行するWriterや古いSnapshotが、完了直後に旧状態を再投入する競合もある。

外部脅威IDは独立したMapping評価を実施していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Memory Inventory、Scope Model、Reset Authority、Orchestrator、Generation／Tombstone、Background Writer、Cache、Replica、Restoreを確認する。

### Positive verification

対象ScopeだけをResetし、対象外Tenant／UserのMemoryと、Reset後に明示的に作成した新世代Memoryが正常に利用できることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Poison MarkerをPrimary Memory、Summary、Vector、Cacheへ保存してReset | 完了後、全Production経路でMarkerを取得・利用できない。SP-2、SP-4 |
| N-2 | Reset中にBackground Agent、Retry Queue、Compactionから旧Recordを書き戻す | Write Fence／Generation Checkが拒否する。SP-3 |
| N-3 | 別Tenant／UserまたはModel OutputがReset Scopeを拡大する | Trusted Authorizationが拒否し、他Scopeを変更しない。SP-1 |
| N-4 | 一つのStore／Cache Adapterを失敗させる | Partial Failureとして報告し、未Reset経路をProductionから隔離する。SP-5、SP-7 |
| N-5 | Service Restart、Replica Failover、Reset前Snapshot Restoreを行う | 現行Reset Stateを再適用し、旧Memoryが再出現しない。SP-6 |
| N-6 | 同じReset Requestを再実行する | Idempotentに収束し、他世代／他Scopeを破壊しない。SP-1、SP-5 |
| N-7 | Reset後に元のPoison Triggerと通常Queryを再実行する | Original／Derived Memoryの影響なしに処理する。SP-4 |

### Failure conditions

UI／Session履歴だけを消す、対象Scopeが不明、派生状態やWriterを漏らす、Partial Failureを成功扱いする、またはRestart／Restore後に
旧Memoryが再出現する場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Memory／writer inventory | Architecture Owner | Primary、Derived、Background、Shared State | Architecture変更時 | Review記録を保持 | Reset対象／対象外とOwnerが明確 |
| Reset state-machine specification | Memory Platform Owner | Authority、Scope、Generation、Failure処理 | Reset設計変更時 | Versionと承認を保持 | 完了／失敗条件を機械的に説明可能 |
| Reset drill result | Test／Incident Response | N-1〜N-7 | Release後および定期 | Synthetic Poisonを使用 | 全対象経路で再取得・再発がない |
| Reset audit ledger | Trusted Orchestrator | Initiator、Scope、各Adapter結果 | Event時 | Agentから変更不能 | Partial Failureを含め追跡可能 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C8.2.3` | Trusted Memoryへ昇格する前のSource Validationを扱う。Resetは昇格後の回復手段である。 |
| `v1.0-C8.2.5` | 矛盾を検出しAlertする。Reset対象の決定や実行を代替しない。 |
| `v1.0-C8.3.1` | 時刻／Retentionに基づき期限切れRecordを除外する。 |
| `v1.0-C8.3.3` | 調査対象を保持しつつProduction Retrievalから隔離する。 |
| `v1.0-C9.6.1` | Shutdown時の安全なMemory／State処理を扱い、Reset Operationそのものとは異なる。 |

## Known limitations and uncertainty

Logical ResetはPhysical Erasure、Backup破棄、外部Provider Copyの削除、既に生成されたOutputの回収、Model Unlearningを保証しない。
共有Memoryでは一主体のReset権限と他主体の正当なRetentionが衝突し得る。AISVS本文はResetの粒度、Latency、Selective／Fullの区別を
定義しないため、製品のClaimとThreat Modelに基づくScope宣言が必要である。

`verifiable`はArtifactの成熟度であり、Reset Runbookが製品で実装・訓練済みであることを意味しない。

## References

- [AISVS v1.0 C8要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [AISVS v1.0 C8.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-03-Memory-Expiry-Revocation-Leakage-Prevention.md)
- [C8全体分析](../../../docs/c08-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
