---
title: "新規Memoryと既存Memoryの矛盾を検出しAlertする"
versioned_id: "v1.0-C8.2.5"
requirement_id: "C8.2.5"
verification_level: 3
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

# 新規Memoryと既存Memoryの矛盾を検出しAlertする

AISVS Verification Level: 3

学習資料：[C8.2 Embedding Sanitization & Validation](../../../docs/learning/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2-embedding-sanitization-validation/learning.md)

## Upstream basis

AISVS `v1.0-C8.2.5`は、新規Memory Contentを既存MemoryとのContradictionについて検査し、Conflict時にAlertすることを求める。
固定Revisionの要件本文とC8.2 Researchを確認した。

## Interpretation

Memory Commit前に、CandidateのEntity、Scope、Time、Claimを正規化し、関連する既存Record／Golden Sourceと比較する。矛盾を検出した場合、
Silent overwrite／Silent drop／無印併存ではなく、双方のProvenance、Trust Tier、影響範囲を含むAlertとReview Workflowを起動する。

## Security objective

Poisoned、Stale、Forged Claimが既存のTrusted FactやPolicyを静かに置換し、将来のAgent判断を変えることを防ぐ。

## Applicability

Fact、Policy、Preference、Entitlement、Vendor、Deadline、Trajectory等を長期Memoryへ追加・更新・要約するSystemに適用する。

### Non-applicability

永続Memoryへ書かず、互いにFactとして比較できないTransient Eventだけを扱う経路は対象外にできる。

## Scope and assumptions

- ContradictionはEntity、Tenant／User Scope、Temporal Validity、Source Authorityを揃えて評価する。
- Alertは自動的なTruth判定ではなく、人／PolicyによるResolutionを起動する。
- Newerは常に正しい、High ConfidenceはTrustedというRuleにしない。
- Summary／Compaction／ImportもCandidate Writeとして評価する。

## Assets, actors, identities, and trust boundaries

資産はTrusted Fact、Policy、Memory Ledger、Decision Consistencyである。ActorはWriter、Agent、Tool、Source Owner、Detector、Reviewer、攻撃者である。
Trust BoundaryはCandidate ClaimからExisting Memory／Golden Sourceへ移る地点にある。Enforcement PointはPre-commit Conflict DetectorとAlert／Review Gateである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Candidateを関連Entity／Scope／Timeの既存MemoryとCommit前に比較する。 |
| SP-2 | Explicit、Paraphrased、Temporal、Scope-dependent Conflictを評価する。 |
| SP-3 | Conflict時に双方のClaim、Provenance、Trust Tier、影響を含むAlertを生成する。 |
| SP-4 | Resolution前にHigh-trust RecordをSilent overwrite／降格しない。 |
| SP-5 | Reviewer Decision、Supersession、Quarantine、Rollbackを監査可能にする。 |
| SP-6 | Detector障害・判定不能時にHigh-impact Memoryを無条件Commitしない。 |

## Scope calibration and adjacent assurance

C8.2.3はSource ValidationとPromotion、本Controlは内容間Conflictの可視化を扱う。矛盾しないFalse Claim、同じ誤りの反復、未知Factは検出できない。

## Threat and failure-mode rationale

攻撃者は「承認Vendorが変更された」「Policy Ownerは別人」等の低Trust ClaimをTool／Summary経由で保存し、Compaction時にGolden Recordを置換させる。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Entity Resolution、Neighbor Retrieval、Trust／Temporal Model、Conflict Detector、Alert、Review、Commit／Rollbackを確認する。

### Positive verification

整合する更新と正当なTemporal Supersessionが適切に記録され、不要なAlertだけで運用不能にならないことを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Golden Policy／Owner／Entitlementと反対の低Trust Claimを投入 | Commit前にAlertしSilent overwriteしない。SP-1〜SP-4 |
| N-2 | Paraphrase、否定、別時点、別ScopeとしてConflictを表現 | Entity／Temporal／Scopeを考慮して評価する。SP-2 |
| N-3 | Summary／CompactionでConflictを隠す | Derived Writeにも同じGateを適用する。SP-1 |
| N-4 | DetectorをUnavailableにする | High-impact Candidateを保留／Quarantineする。SP-6 |
| N-5 | ReviewerがResolution後Rollback | Claim HistoryとDecisionを復元・監査できる。SP-5 |

### Failure conditions

比較なしCommit、ConflictをSilent overwrite／drop、AlertにProvenanceがない、Derived Writerが迂回、またはDetector障害時にAllowする場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Claim／Trust model | Memory・Domain Owner | Entity／Scope／Time／Source | Domain変更時 | Versionを保持 | 比較対象と優先Ruleを説明可能 |
| Conflict／Resolution ledger | Detector／Review System | 各Alert | Event時 | 改ざん防止 | 双方のClaimとDecisionを追跡可能 |
| Contradiction test | Test Harness | N-1〜N-5 | Detector変更後 | Synthetic Claimsを使用 | Conflict AlertとNon-overwriteを確認 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C8.2.3` | Candidate MemoryのSource ValidationとPromotionを行う。 |
| `v1.0-C8.1.2` | 比較根拠となるProvenance Metadataを不変にする。 |
| `v1.0-C8.3.2` | Poison判明後にMemoryをResetできるようにする。 |

## Known limitations and uncertainty

NLI／Similarityは暗黙・Temporal・Scope別Conflictを見逃し、False Positiveも多い。Alert Fatigue、Golden Sourceの誤り、Truthの変化を扱うDomain Governanceが必要である。

`verifiable`はArtifactの成熟度であり、Memoryの真実性や製品適合を意味しない。

## References

- [AISVS v1.0 C8要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [AISVS v1.0 C8.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-02-Embedding-Sanitization-Validation.md)
- [C8全体分析](../../../docs/c08-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
