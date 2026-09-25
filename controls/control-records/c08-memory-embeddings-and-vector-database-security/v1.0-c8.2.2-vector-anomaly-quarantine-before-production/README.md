---
title: "異常なVectorをProduction Index投入前に検疫する"
versioned_id: "v1.0-C8.2.2"
requirement_id: "C8.2.2"
verification_level: 2
family_id: "C8"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-02-Embedding-Sanitization-Validation.md"
last_verified: "2026-09-24"
maturity: "verifiable"
mapping_assessment_refs: []
---

# 異常なVectorをProduction Index投入前に検疫する

AISVS Verification Level: 2

学習資料：[C8.2 Embedding Sanitization & Validation](../../../docs/learning/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2-embedding-sanitization-validation/learning.md)

## Upstream basis

AISVS `v1.0-C8.2.2`は、通常のClustering Pattern外のVectorをFlagし、Production Indexへ入れる前にQuarantineすることを求める。
固定Revisionの要件本文とC8.2 Researchを確認した。ResearchはOutlierだけでなく、多数Queryへ近いHigh-centrality／Hub Vectorも注意対象とする。

## Interpretation

Candidate VectorをTenant、Corpus、Source Type、Language、Media、Embedding Model VersionごとのBaselineと比較し、異常Signalを検出したRecordを
Productionから分離されたStaging／Quarantineへ移す。検疫解除には根拠と承認を要し、直接Store APIでGateを迂回させない。

## Security objective

Adversarial Vector、Collision、Hubness、異常Metadata／Multimodal不整合により、Poison Recordが多数・標的Queryで優先RetrievalされるRiskを低減する。

## Applicability

Embeddingを生成・受領してProduction Vector／Graph Indexへ投入するPipelineに適用する。

### Non-applicability

Vectorを生成・保存しないSystemは対象外にできる。小規模、信頼Source、Single Tenantは異常検査を不要とする理由にならない。

## Scope and assumptions

- BaselineをCorpus／Tenant／Model Version等でSegmentし、Version管理する。
- Far-out Outlierだけでなく、過度なCentrality、Duplicate、Reverse-neighbor頻度、Metadata Drift等を複合評価する。
- FlagはPoisonの証明ではなく、QuarantineとReviewを起動するSignalである。
- Production StoreへのWrite PathをSanctioned Pipelineへ限定する。

## Assets, actors, identities, and trust boundaries

資産はProduction Index、Retrieval Ranking、Corpus Integrityである。ActorはSource Writer、Embedding Service、Detector、Reviewer、Vector Store、
攻撃者である。Trust BoundaryはCandidate VectorからProduction Indexへ昇格する地点にある。Enforcement PointはPre-commit DetectorとAdmission Gateである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Candidate VectorをVersioned Baselineに対してProduction Commit前に評価する。 |
| SP-2 | Outlier、Hubness／Centrality、Duplicate、Source／Metadata不整合等の複数Signalを扱う。 |
| SP-3 | Threshold違反・判定不能RecordをProduction外へFlag／Quarantineする。 |
| SP-4 | Quarantine解除をReview、理由、Approver、対象VersionへBindingする。 |
| SP-5 | Direct API、Bulk Import、Reindex、Replica経路でAdmission Gateを迂回させない。 |
| SP-6 | Baseline／Threshold変更とFalse Positive／Negativeを監視・再評価する。 |

## Scope calibration and adjacent assurance

C8.2.4はContent自体がRetrieval操作目的にCraftされているかを扱う。本ControlのCluster異常検出は正常Cluster内のPoisonを見逃し得るため、
Provenance、Content Screening、Contradiction Reviewを代替しない。

## Threat and failure-mode rationale

攻撃者は標的Query近傍またはEmbedding Space中心へVectorを配置し、少数Recordを広範囲にRetrieveさせる。単一Global BaselineやDistance Outlierだけでは
Corpus固有・中心的Poisonを見逃す。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Baseline作成、Feature、Threshold、Staging／Quarantine、Review、Production Commit、Direct／Bulk Write Pathを確認する。

### Positive verification

代表Corpusの正規Vectorが許容範囲で投入され、判定とBaseline Versionを追跡できることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 遠方Outlier、Duplicate、Metadata不整合Vectorを投入 | Production前にFlag／Quarantineする。SP-1〜SP-3 |
| N-2 | 多数の無関係QueryへHitするHub／Centroid近傍Vectorを投入 | Centrality Signalで検出対象にする。SP-2 |
| N-3 | 別Tenant／Language／Model Version Baselineを混用 | Segment不一致を拒否し正しいBaselineを使う。SP-1 |
| N-4 | Direct Store API／Bulk／ReindexでDetectorを迂回 | Production Writeを拒否する。SP-5 |
| N-5 | 無承認でQuarantine解除 | Releaseを拒否し監査Eventを残す。SP-4 |

### Failure conditions

検査がProduction投入後、異常をFlagだけして検索可能、単一Global／Outlier Signalのみ、Direct Writeで迂回、または無承認解除できる場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Baseline／Threshold record | ML・Security Owner | Corpus／Tenant／Model | Corpus／Model変更時 | Version・承認を保持 | SegmentとSignalを特定可能 |
| Admission／Quarantine Flow | Ingestion Owner | 全Write Path | Pipeline変更時 | Revisionを保持 | Production前Gateを迂回不能 |
| Poison／Hub test | Test Harness | N-1〜N-5 | Detector変更後 | Synthetic Vectorを使用 | 異常RecordがProduction非表示 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C8.2.4` | Retrieval操作用にCraftされたContentをVectorization前に検査する。 |
| `v1.0-C8.2.5` | 新Memoryと既存Memoryの矛盾を検出する。 |
| `v1.0-C8.3.3` | Quarantined Contentを保持しつつ全Retrievalから除外する。 |

## Known limitations and uncertainty

正常な新Topic／Languageも異常に見え、Adaptive Poisonは正常Clusterへ紛れる。Detection Model自体のPoison、Embedding Model変更、Threshold Driftもあり、
本ControlだけでPoison不存在は保証できない。

`verifiable`はArtifactの成熟度であり、Poison完全検出や製品適合を意味しない。

## References

- [AISVS v1.0 C8要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [AISVS v1.0 C8.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-02-Embedding-Sanitization-Validation.md)
- [C8全体分析](../../../docs/c08-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
