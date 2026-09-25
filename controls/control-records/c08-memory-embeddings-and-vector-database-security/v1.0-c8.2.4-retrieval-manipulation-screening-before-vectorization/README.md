---
title: "Retrieval操作用ContentをVectorization前に検出・拒否・検疫する"
versioned_id: "v1.0-C8.2.4"
requirement_id: "C8.2.4"
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

# Retrieval操作用ContentをVectorization前に検出・拒否・検疫する

AISVS Verification Level: 3

学習資料：[C8.2 Embedding Sanitization & Validation](../../../docs/learning/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2-embedding-sanitization-validation/learning.md)

## Upstream basis

AISVS `v1.0-C8.2.4`は、Retrieval Resultを操作するためにCraftされたContentをVectorization前に検出し、拒否またはQuarantineすることを求める。
固定Revisionの要件本文とC8.2 Researchを確認した。

## Interpretation

Raw File、Rendered View、Extracted Text、OCR、Metadata、Link、Hidden Layerを比較し、Hidden Instruction、Query-term Stuffing、Unicode／Layout Obfuscation、
Retrieval-optimized Poison等のSignalをEmbedding前に検査する。検出／判定不能ContentはProductionへ入れずReview可能なQuarantineへ置く。

## Security objective

少数のCrafted Documentが標的Queryで過度にRetrieveされ、Model Answer、Tool選択、Policy判断を攻撃者の意図へ誘導するRiskを低減する。

## Applicability

PDF、DOCX、HTML、Image、Web、Email、Code等の外部ContentをVectorizeする全Loader／Ingestion Pathに適用する。

### Non-applicability

外部ContentをVectorizeしないSystemのみ対象外にできる。Trusted Publisherや署名はContentの無害性を保証しない。

## Scope and assumptions

- LoaderごとのRaw／Rendered／Extracted差を試験する。
- Detectionは完全でなく、Provenance、Quarantine、Retrieval時防御を併用する。
- Hidden Instructionだけでなく、正しそうなContentによるRanking Manipulationも対象とする。
- Quarantine ReleaseはHuman／Policy ReviewとArtifact HashへBindingする。

## Assets, actors, identities, and trust boundaries

資産はCorpus Integrity、Retrieval Ranking、Model Contextである。ActorはPublisher、Connector、Loader、Scanner、Reviewer、Embedding Service、攻撃者である。
Trust BoundaryはRaw ContentからExtracted Chunk／Vectorへ移る地点にある。Enforcement PointはPre-vectorization Security Transformation Gateである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 全Loader／FormatでVectorization前にRetrieval-manipulation Screeningを行う。 |
| SP-2 | Raw、Rendered、Extracted、OCR、Metadata／Hidden Layerの不一致とObfuscationを評価する。 |
| SP-3 | 検出・判定不能Contentを拒否またはProduction外へQuarantineする。 |
| SP-4 | Quarantine ReleaseをReview、根拠、Artifact Hash、ApproverへBindingする。 |
| SP-5 | Alternate Loader、Reingestion、Bulk／Direct UpsertでGateを迂回させない。 |
| SP-6 | Adversarial Fixtureと実IncidentからDetector／Policyを継続評価する。 |

## Scope calibration and adjacent assurance

C8.2.2はVector Geometry異常、本ControlはVectorization前Contentの操作意図／構造を扱う。C10.4.2のRuntime Tool Response Screeningとも時点が異なる。

## Threat and failure-mode rationale

攻撃者はWhite Text、Comment、OCR Layer、Homoglyph、Keyword反復、自然なPoison Documentを作り、Loaderが抽出した内容だけを将来Queryへ強く一致させる。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

全Format／Loader、Normalization、Scanner、Quarantine、Release、Embedding／Direct Upsert経路を確認する。

### Positive verification

正規Contentが意味を保って通過し、Scan VersionとArtifact Hashを追跡できることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Hidden Text、Comment、OCR／Metadata Instructionを埋め込む | Production前に検出／Quarantineする。SP-1〜SP-3 |
| N-2 | Unicode、Encoding、Base64-like、LayoutでObfuscate | Normalize／Multi-view比較で検査する。SP-2 |
| N-3 | Target Query語を不自然に反復、自然文Poisonを投入 | Retrieval Manipulation SignalでFlagする。SP-1, SP-6 |
| N-4 | Alternate Loader／Bulk／Direct Upsertを使う | Gateを迂回できない。SP-5 |
| N-5 | Scan後にArtifactを差し替え | Hash不一致でRelease／Embeddingを拒否する。SP-4 |

### Failure conditions

Embedding後にだけ検査、単一Plaintext Viewのみ、検出してもProductionへ投入、無承認Release、または別Loaderで迂回できる場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Loader／Screening inventory | Ingestion・Security Owner | 全Format／Path | Loader変更時 | Versionを保持 | 各FormatのGateを特定可能 |
| Quarantine／Release record | Review System | 各Artifact | 各Decision時 | Hash・Approverを保護 | 未承認ContentがProduction非表示 |
| Adversarial loader test | Test Harness | N-1〜N-5 | Release時 | Fixtureを隔離 | 操作用Contentを拒否／検疫 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C8.2.2` | Vector Geometry／Clustering異常をProduction投入前に検疫する。 |
| `v1.0-C8.2.3` | Tool／Agent OutputのTrusted Memory Promotionを制御する。 |
| `v1.0-C10.4.2` | RuntimeのMCP Tool ResponseをInjection観点でScreeningする。 |

## Known limitations and uncertainty

自然なPoison、真実だが偏ったContent、Adaptive Attackは検出困難で、False Positiveも避けられない。人のReviewも完全ではなく、Retrieval時Containmentが必要である。

`verifiable`はArtifactの成熟度であり、Poison完全防止や製品適合を意味しない。

## References

- [AISVS v1.0 C8要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [AISVS v1.0 C8.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-02-Embedding-Sanitization-Validation.md)
- [C8全体分析](../../../docs/c08-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
