---
title: "Sensitive FieldをEmbedding前に検出・変換・除外する"
versioned_id: "v1.0-C8.2.1"
requirement_id: "C8.2.1"
verification_level: 1
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

# Sensitive FieldをEmbedding前に検出・変換・除外する

AISVS Verification Level: 1

学習資料：[C8.2 Embedding Sanitization & Validation](../../../docs/learning/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2-embedding-sanitization-validation/learning.md)

## Upstream basis

AISVS `v1.0-C8.2.1`は、Sensitive FieldをEmbedding前に検出し、Mask、Tokenize、またはDropすることを求める。
固定Revisionの要件本文とC8.2 Researchを確認した。Researchは本文だけでなくMetadata、表、OCR、Attachment名等を対象に含める。

## Interpretation

Embedding ProviderまたはVector Storeへ送る前に、抽出済みContentとMetadataをData Classification Policyで検査し、Fieldごとに
Mask／Tokenize／Dropを決定する。変換前の値をEmbedding API、Vector、Metadata、Log、Dead-letter Queueへ流さない。

## Security objective

PII、PHI、Payment Data、Credential、Customer Secret、社内機密等がVectorへ固定され、検索・Store侵害・Embedding Inversion等で
再露出するRiskを低減する。

## Applicability

Document、Image／OCR、Table、Tool Output、Memory等をEmbeddingする全Ingestion Pathに適用する。

### Non-applicability

Policy上公開情報だけを扱い、Sensitive Fieldが入り得ないことをSource Contractと継続検査で保証できるCollectionは対象外にできる。

## Scope and assumptions

- Sensitiveの定義は法令だけでなく、Tenant／Role／Business Context固有のSecretを含む。
- Mask／Tokenize／Dropの選択はRetrieval Utility、Re-identification Risk、利用目的に基づく。
- Detection Toolの存在ではなく、変換後DataだけがEmbedding Boundaryを越えることを確認する。
- Source削除後もDerived Vector、Replica、Cache、Backupが残り得るため、事前処理をPrimary Gateとする。

## Assets, actors, identities, and trust boundaries

資産はSensitive Source Data、Embedding、Metadata、Provider送信Dataである。ActorはConnector、Parser、DLP／Classifier、Embedding Service、
Vector Store、攻撃者である。Trust Boundaryは抽出ContentからEmbedding Requestへ移る地点にある。Enforcement PointはPre-embedding
Inspection／Transformation Gateである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 全Embedding PathでContentとMetadataをSensitive Field検査へ通す。 |
| SP-2 | 検出FieldをPolicyに従いMask、Tokenize、またはDropしてからEmbeddingする。 |
| SP-3 | Raw Sensitive ValueをEmbedding Provider、Vector Store、Log、Error／Retry経路へ送らない。 |
| SP-4 | OCR、Table、Attachment、Hidden Metadata、Chunk境界でも同じPolicyを適用する。 |
| SP-5 | Detector障害・判定不能時にSensitive CollectionへFail-openしない。 |
| SP-6 | Domain固有Detectorを評価用Datasetで継続検証し、False Negativeを管理する。 |

## Scope calibration and adjacent assurance

本Controlの本質はDLP製品導入ではなく、Sensitive ValueがEmbedding Boundaryを越える前のData Flow制約である。C5.2.3はSensitive Dataを
Model Storageへ固定しない広い保証、C8.1.3は保存後のRetrieval Authorizationを扱う。

## Threat and failure-mode rationale

Secretが一度Vector化されると、Raw Storeを直接見なくてもSimilarity QueryやInversionにより情報が漏れる可能性がある。本文だけを検査し、
Metadata／OCR／Error Queueから漏れる経路もある。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Source、Parser、Normalization、Detection、Transformation、Embedding API、Vector Upsert、Log／Error／RetryをEnd-to-endで追う。

### Positive verification

許可Dataと適切にTokenizeされたValueが期待するRetrieval Utilityを保ってEmbeddingされることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | PII、Credential、Domain Secretを本文／Metadataへ配置 | Raw値がEmbedding／Storeへ到達しない。SP-1〜SP-3 |
| N-2 | Table、OCR、Attachment名、Hidden Fieldへ同じ値を配置 | 同じPolicyで変換・除外する。SP-4 |
| N-3 | Sensitive ValueをChunk境界へ分割・Encoding変形 | Normalize／Context検査で検出またはQuarantineする。SP-1, SP-4 |
| N-4 | DetectorをTimeout／Unavailableにする | Raw DataをEmbeddingせず安全に保留する。SP-5 |
| N-5 | Error、Retry、Debug Logを観測 | Raw値を含まない。SP-3 |

### Failure conditions

検査がEmbedding後、本文だけ対象、Raw値をLog／Providerへ送る、Detector障害時に続行、またはPolicy上必須Fieldを未検出の場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Sensitive Data policy | Data／Privacy／Security Owner | Source／Field／Action | Policy変更時 | 承認・Versionを保持 | Sensitive分類とMask／Tokenize／Dropを特定可能 |
| Pre-embedding Data Flow | Ingestion Owner | 全Path | Pipeline変更時 | Revisionを保持 | Raw値がBoundaryを越えない |
| Labeled detection test | Test Harness | N-1〜N-5 | Detector／Source変更時 | Synthetic Dataを使用 | 定義閾値を満たし漏えいなし |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C5.2.3` | Sensitive DataをModel内部へ恒久固定しない。 |
| `v1.0-C8.1.3` | 保存後のVector／Memory Retrieval Scopeを強制する。 |
| `v1.0-C8.3.1` | Expiry後のDerived Vectorを検索結果から除外する。 |

## Known limitations and uncertainty

Context依存Secretや企業固有識別子は自動検出が難しく、MaskingはUtilityを低下させ得る。Embeddingからの復元可能性をゼロにはできず、
Store Access Control、Encryption、Retentionも必要である。

`verifiable`はArtifactの成熟度であり、Sensitive Data不存在や製品適合を意味しない。

## References

- [AISVS v1.0 C8要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [AISVS v1.0 C8.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-02-Embedding-Sanitization-Validation.md)
- [C8全体分析](../../../docs/c08-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
