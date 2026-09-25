---
title: "AISVS C8.3 Memory Expiry & Revocation 学習ノート"
document_kind: "section-learning-note"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
section_id: "C8.3"
requirements:
  - "v1.0-C8.3.1"
  - "v1.0-C8.3.2"
  - "v1.0-C8.3.3"
last_updated: "2026-09-25"
---

# C8.3 Memory Expiry & Revocation

## 1. 文書の役割とSource separation

本書は、AISVS v1.0の固定RevisionにあるC8.3全3 Requirementを、Memoryを後から安全に利用停止するLifecycleとして学ぶ講義である。
製品適合の証拠やControl本文の代替ではない。

- **Normative:** 下表の英語原文とLevel。
- **AISVS Research:** 全Retrieval Path、Reset Drill、Forensic保持、Backup／Restore等を補足する。
- **Repository interpretation:** Logical Exclusion、Reset、Quarantine、Physical Deletionを別の完了点として扱う。
- **Derived insight:** 「消す」だけでなく、利用停止、再出現防止、調査可能性をそれぞれ検証する。

## 2. Normative Requirements

| ID | Level | AISVS English | 日本語訳 |
|---|---:|---|---|
| `v1.0-C8.3.1` | 2 | Verify that expired vectors are excluded from retrieval results. | 期限切れVectorがRetrieval結果から除外されることを確認する。 |
| `v1.0-C8.3.2` | 2 | Verify that memory can be reset. | MemoryをResetできることを確認する。 |
| `v1.0-C8.3.3` | 3 | Verify that quarantined content is retained but excluded from all retrieval results. | Quarantine Contentを保持しながら、すべてのRetrieval結果から除外することを確認する。 |

正本は[固定RevisionのC8要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)である。

## 3. C8における位置づけ

C8.1は所属とRetrieval Scope、C8.2は保存前の検査とTrusted Memoryへの昇格を扱う。C8.3は、正しく保存された後でも、
期限、信頼、利用目的、Incident状態が変化したDataを将来の判断から外せるかを扱う。

| Requirement | Lifecycle上の役割 |
|---|---|
| C8.3.1 | 期限に基づくLogical Exclusion |
| C8.3.2 | 指定Scopeを信頼できる初期状態へ戻すRecovery Operation |
| C8.3.3 | 証拠保持とProduction Exclusionを両立するIncident Containment |

## 4. Concrete Scenario

社内Agentは、長期Memory、RAG Vector、Conversation Summary、Semantic Cacheを利用する。三つの事象が起きる。

1. 旧手続Documentが有効期限を迎える。
2. Web経由で保存されたPoisoned MemoryをIncident対応でResetする。
3. 疑わしいSharePoint Documentを原因調査のためQuarantineする。

```text
active memory／vector
  ├─ expiry → productionから除外 → 後で物理削除
  ├─ reset → old generationを無効化 → clean generation
  └─ quarantine → forensic保持 + productionから除外
```

一つのDelete API成功だけでは、Cache、Summary、Retry、Replica、RestoreしたSnapshotから再出現しないことを保証できない。

## 5. 用語

- **Logical Exclusion:** Storage上にDataが残っていても、Production Retrievalへ返さない状態。
- **Physical Deletion:** Storage、Index、Replica等から実体を削除する処理。
- **Propagation SLO:** State変更から全Retrieval経路で効果が出るまでの最大許容時間。
- **Reset Scope:** User、Tenant、Agent、Session、Task、Memory Class等、Reset対象として宣言した範囲。
- **Generation／Epoch:** Reset前後のMemory世代を区別し、旧Writerの再投入を拒否する識別子。
- **Write Fence:** 古いGenerationのBackground WriterやRetryがReset後に書き戻すことを防ぐ境界。
- **Quarantine:** 疑わしいContentを通常利用から隔離し、調査用に保持する状態。
- **Forensic Plane:** Incident Responderだけが証拠へAccessする、Productionとは分離した経路。
- **Integrity:** Contentが正しいという意味ではなく、隔離後に改ざんされていないことを検証できる性質。

## 6. Threat ModelとAbuse Path

攻撃者はMemoryへPoisonを保存できる外部Content提供者、侵害されたWriter、低権限Tenant、またはReset／Quarantine状態の
迂回を狙う主体を想定する。運用事故、非同期処理、古いSnapshotもFailure Sourceである。

```text
Expired record remains in lexical／cache path
  → later query retrieves stale or sensitive content

Reset clears visible session only
  → retry／background summary rewrites poison
  → next session activates it

Quarantine is only a metadata flag
  → one filter-less path retrieves poison

Immediate hard delete
  → incident evidence and impact trace are lost
```

## 7. Security InvariantとEnforcement Point

| Requirement | Security Invariant | 決定論的なEnforcement Point |
|---|---|---|
| C8.3.1 | Expired Recordは、閲覧権限がある主体にも全Production Retrievalから返らない。 | Trusted Expiry State、Server-side Retrieval Gate、Cache／Replica Invalidation |
| C8.3.2 | Reset完了後、宣言したScopeの旧世代MemoryがProductionへ再利用・再投入されない。 | Reset Orchestrator、Generation、Write Fence、各Store Adapter |
| C8.3.3 | Suspect Contentを改ざん検知可能な調査用Evidenceとして残し、通常のUser／Agent／Tool／Cacheへ出さない。 | Lifecycle State Store、全Production Retrieval Gate、独立Forensic Authorization |

## 8. 実装の考え方

### 8.1 Expiry

RecordへTrusted `expires_at`とPolicy／Authorityを結び付ける。Dense、Lexical、Hybrid、Direct ID、Graph、Reranker、Semantic Cache、
Application Cache、Replica、Restore後の経路へ同じStateを強制する。Client指定の`include_expired`へAuthorityを与えない。

Logical Exclusionを先に行い、Compaction等のPhysical Deletionを後で実施できる。全Production経路がZero Resultになるまでの
Propagation SLOを定め、Canaryで測定する。

### 8.2 Reset

Reset ScopeとAuthorityをTrusted Identity／Policyで決める。Background Writerを停止またはFenceし、Generationを更新し、Primary、
Vector、Summary、Cache、Trajectory、Queueを無効化する。Partial Failureを成功として返さず、Restart、Failover、Restore後も
旧Generationを拒否する。

```text
authorize scope
  → fence writers
  → advance generation
  → invalidate all declared state
  → verify zero retrieval
  → resume clean generation
```

### 8.3 Quarantine

平易に言えば、次の設計である。

> 疑わしい情報は、調査用の隔離庫に元の状態で残す。ただし、通常の検索やAgentの判断材料には出さない。

`active → quarantined → released／purged`を別々の認可された状態遷移として扱う。Metadata Flag方式ではFilter omissionや改ざん、
別Namespace／Forensic Store方式では移動のAtomicity、Cache、Replicaを検証する。Original Content、Source、Hash、検出理由、時刻、
関連Artifact、Access履歴を保持する。

## 9. Pass／FailとScope Calibration

| Observation | 判定 | 理由 |
|---|---|---|
| Expiry時に全Production結果から即時除外し、24時間後に物理削除する | C8.3.1 Pass候補 | 直接の保証はRetrievalからのLogical Exclusion |
| Primary Vectorだけ除外しSemantic Cacheから返す | C8.3.1 Fail | 実効的なRetrieval Pathが残る |
| 宣言したScopeのPrimary／Derived Memoryを無効化し、旧WriterをFenceする | C8.3.2 Pass候補 | 旧世代が再利用・再投入されない |
| SessionとVectorを消すがRetry Summaryが新世代へ戻る | C8.3.2 Fail | Reset後に旧Memoryが再出現する |
| Suspect ContentをForensic Storeへ完全性付きで保持し、全Production経路から除外する | C8.3.3 Pass候補 | 保持と利用停止を両立する |
| 全Artifactを即時Hard Deleteし、Content／Provenance／理由を残さない | C8.3.3 Fail | 「保持」を満たさず調査不能になる |

Physical DeletionのLatency、Privacy Erasure、Legal Hold、Model Unlearningは重要だが、各Requirementの直接のPass条件と分けて評価する。

## 10. 保証しない範囲

- C8.3.1のLogical ExclusionはRaw Storage、Backup、Provider Copyからの消去を保証しない。
- C8.3.2は既に外部へ送信されたOutputの回収やModel WeightのUnlearningを保証しない。
- C8.3.3はQuarantine対象が真に悪性か、Forensic Retentionの法的根拠があるかを保証しない。
- Lifecycle Stateが正しくても、列挙されていないRead／Write Pathを自動的に保護しない。
- 特定Vector DBのTTL、Delete、Flag機能があるだけではPassにならない。

## 11. 対話の再構成

### 問い1：Logical ExclusionとPhysical Deletion

**Scenario:** Expiry時に全Production Retrievalから即座に除外するが、Vector本体は24時間後のCompactionで削除する。

**学習者の判断:** C8.3.1 Pass。即座に除外されるため。

**整理:** 正しい。C8.3.1の直接の保証はRetrieval Exclusionである。24時間の物理保持がRetention／Privacy要件を満たすかは別に評価する。

### 問い2：Reset後の再投入

**Scenario:** Conversation、Vector、Cacheは消したが、Retry QueueのAgent SummaryをBackground Workerが10分後に書き戻す。

**学習者の判断:** C8.3.2 Fail。Summaryに残っているため。

**整理:** 正しい。さらに、Summaryの残存だけでなく、旧GenerationのWriterがReset後へ再投入できるWrite PathがFailureである。
対象状態の無効化とWrite Fenceの両方が必要になる。

### 問い3：QuarantineとHard Delete

**Scenario:** Suspect Vector、Document、Cacheを即時Hard Deleteし、Productionから消えるがEvidenceを何も残さない。

**学習者の判断:** C8.3.3 Fail。何も残らず調査できない。

**整理:** 正しい。「完全性を保って存在する」という抽象表現は、疑わしい情報を調査用の隔離庫へ元の状態で残し、Hash等で
隔離後の改ざんを検証できるという意味である。Contentの正しさを保証する意味ではない。

## 12. このセッションから得た洞察

> 「検索から消えた」「Storageから消えた」「再び現れない」は別々の検証対象である。

> Quarantineの本質は、「消す」ではなく、「使わせずに、調査できる状態で隔離する」ことである。

Expiry、Reset、Quarantineを一つのDelete機能へ潰すと、どのSecurity Outcomeを達成したか説明できなくなる。Lifecycle Operationは
State Transition、全Read／Write Path、完了条件、Evidenceを一組として設計する。

## 13. 設計レビュー項目

- Expiry Authority、基準Clock、Propagation SLOが明示されているか。
- Dense、Lexical、Hybrid、Direct ID、Graph、Cache、Replica、Restoreを列挙したか。
- Logical ExclusionとPhysical DeletionのEvidenceを分けているか。
- Reset Scopeと対象外状態を明示したか。
- Background Writer、Retry、Compaction、ReplicationをFenceできるか。
- Partial Resetを成功として返さないか。
- Quarantine、Release、Purgeを別々に認可・監査するか。
- ProductionとForensicのIdentity、Interface、Access Logを分離したか。
- Original Content、Hash、Source、検出理由、関連Artifactを保持するか。
- Restart、Failover、Snapshot Restore後の再出現をNegative Testしたか。
- Privacy Erasure、Legal Hold、Incident Evidence Retentionの衝突をPolicyで扱うか。

## 14. ControlへのLink

- [C8.3.1 Expired Vector Retrieval Exclusion](../../../../control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.3.1-expired-vector-retrieval-exclusion/README.md)
- [C8.3.2 Complete Memory Reset](../../../../control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.3.2-complete-memory-reset/README.md)
- [C8.3.3 Quarantine Retention and Exclusion](../../../../control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.3.3-quarantine-retention-and-retrieval-exclusion/README.md)

## 15. References

- [AISVS v1.0 C8 Normative Requirements](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [AISVS v1.0 C8.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-03-Memory-Expiry-Revocation-Leakage-Prevention.md)
