---
title: "Agent／Tool OutputをSource検証なしにTrusted Memoryへ書かない"
versioned_id: "v1.0-C8.2.3"
requirement_id: "C8.2.3"
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

# Agent／Tool OutputをSource検証なしにTrusted Memoryへ書かない

AISVS Verification Level: 2

学習資料：[C8.2 Embedding Sanitization & Validation](../../../docs/learning/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2-embedding-sanitization-validation/learning.md)

## Upstream basis

AISVS `v1.0-C8.2.3`は、Agent OutputとTool Outputを明示的なSource ValidationなしにTrusted Agent Memoryへ自動Writeしないことを求める。
固定Revisionの要件本文とC8.2 Researchを確認した。

## Interpretation

生成Summary、Tool Result、Model推論はCandidate Memoryとして隔離し、Origin、Author／Tool Identity、Source URI、Invocation、Tenant、Trust Tier、
Sensitivity、Write Authorityを検証してからTrusted MemoryへPromotionする。生成した同じModel Contextを自己検証者にしない。

## Security objective

一度のPrompt Injection、Tool Poisoning、誤推論が長期Memoryへ固定され、将来Sessionで自己強化・再発動することを防ぐ。

## Applicability

Agent／Tool OutputをProfile、Summary、Preference、Trajectory、Long-term Memory、Vector Storeへ保存する全Write Pathに適用する。

### Non-applicability

OutputをSession内のTransient Dataとしてのみ使い永続・共有Memoryへ書かない経路は対象外にできる。

## Scope and assumptions

- User-authored fact、Tool observation、Agent inference、System factを別Source Classとして保持する。
- Promotion PolicyはModel ConfidenceだけでなくSource ProvenanceとWrite Authorizationを使う。
- High-impact MemoryはHumanまたは独立Policy Engineの承認を要求する。
- Derived Summary／Compaction／Background Writerも新しいWriteとして同じGateを通す。

## Assets, actors, identities, and trust boundaries

資産はTrusted Memory、User Profile、Future Agent Behaviorである。ActorはUser、Agent、Tool、Validator、Approver、Memory Service、攻撃者である。
Trust BoundaryはOutputからCandidate Memoryへ、CandidateからTrusted Memoryへ移る地点にある。Enforcement PointはCentral Memory-write Serviceである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 全Memory Write PathがOutputをCandidateとして扱い、直接Trusted Storeへ書かない。 |
| SP-2 | Source Identity、URI／Invocation、Tenant、Trust Tier、Sensitivity、Writerを検証・記録する。 |
| SP-3 | Promotionを独立Policy／Reviewerと明示Write Authorizationへ結び付ける。 |
| SP-4 | Summary、Compaction、Retry、Background／Shared Memory経路も同じGateを通す。 |
| SP-5 | Validation失敗・不明Source時はQuarantineし、Trusted Retrievalから除外する。 |
| SP-6 | Promotion／拒否／Rollbackを監査・取消可能にする。 |

## Scope calibration and adjacent assurance

C8.2.4はEmbedding前のRetrieval操作Content、C8.2.5は既存Memoryとの矛盾を扱う。本Controlは「誰が何を根拠にTrusted Memoryへ昇格させるか」に焦点を置く。

## Threat and failure-mode rationale

悪意あるDocumentやTool Responseが「remember」「trusted source」等を含み、AgentがSummaryとして保存すると、元Injectionが消えても誤ったInstruction／Factが残る。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

全Memory Writer、Source Class、Candidate／Trusted Store、Promotion Policy、Approver、Rollback、Background Jobを列挙する。

### Positive verification

検証済みSourceの許可MemoryだけがProvenance付きでPromotionされ、後からDecisionを再現できることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Tool／Documentが永続化を要求するOutputを返す | 自動PromotionせずCandidate／Quarantineに留める。SP-1, SP-5 |
| N-2 | Source URI、Tool Identity、Invocationを欠落・偽装 | Trusted Writeを拒否する。SP-2 |
| N-3 | Agentが自分のOutputを自分で承認 | 独立Policy／Authorityなしでは拒否する。SP-3 |
| N-4 | Summary、Compaction、Background WriterでGateを迂回 | 同じValidationを強制する。SP-4 |
| N-5 | Session再起動後にPoison Triggerを検索 | 未承認Candidateを取得しない。SP-5 |

### Failure conditions

Outputを直接Trusted Memoryへ保存する、Provenanceなし、同一Modelの自己評価だけ、または一つでもWriterがGateを迂回する場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Memory-write inventory／policy | Memory・Security Owner | 全Writer／Source Class | Feature変更時 | Version・承認を保持 | Promotion条件を特定可能 |
| Promotion／Rollback ledger | Memory Service | 各Decision | 各Write時 | 改ざん防止、Secret最小化 | Source・Approver・対象を追跡可能 |
| Persistent-poison test | Test Harness | N-1〜N-5 | Release時 | Synthetic Payloadを使用 | 未検証MemoryがTrusted Retrievalされない |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C8.2.4` | Vectorization前にRetrieval操作Contentを検査する。 |
| `v1.0-C8.2.5` | Candidateと既存Memoryの矛盾をAlertする。 |
| `v1.0-C9.5.4` | Agent Message／Memoryへ伝播するIdentity Contextを扱う。 |

## Known limitations and uncertainty

Sourceが正規でも内容が誤ることがあり、ValidationはTruthを保証しない。厳しいPromotionはUtility／Latencyを下げ、Trust Tier設計とReviewer Capacityが必要である。

`verifiable`はArtifactの成熟度であり、Memory Poisoning完全防止や製品適合を意味しない。

## References

- [AISVS v1.0 C8要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [AISVS v1.0 C8.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-02-Embedding-Sanitization-Validation.md)
- [C8全体分析](../../../docs/c08-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
