---
title: "Document Metadata Tagを初回Write後に不変にする"
versioned_id: "v1.0-C8.1.2"
requirement_id: "C8.1.2"
verification_level: 2
family_id: "C8"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-01-Access-Controls-Memory-RAG.md"
last_verified: "2026-09-24"
maturity: "verifiable"
mapping_assessment_refs: []
---

# Document Metadata Tagを初回Write後に不変にする

AISVS Verification Level: 2

学習資料：[C8.1 Access Controls on Memory & RAG Indices](../../../docs/learning/c08-memory-embeddings-and-vector-database-security/v1.0-c8.1-access-controls-memory-rag-indices/learning.md)

## Upstream basis

AISVS `v1.0-C8.1.2`は、Document Metadata Tagを初回Write後にImmutableとすることを求める。固定Revisionの要件本文と
C8.1 Researchを確認した。ResearchはSource、Owner、Tenant、Classification、Timestamp、Batch、Content Hash、Embedding Model等の
Provenance／Security Metadataの改ざんを中心に扱う。

## Interpretation

Chunk／Vectorを信頼・認可・追跡する根拠となるMetadata Tagは、初回Commit後に同一Record上で上書きできないようにする。
Source側のACL、Classification、Content、Embedding Model等が正当に変わる場合は、既存事実を改変せず、新しいVersion／Recordと
変更関係をAppendする。Current Viewは新Versionを指せるが、過去のTagをSilentに書き換えない。

## Security objective

攻撃者または誤動作Jobが、Poisoned／Restricted ContentをTrusted、Public、別Tenant所有へ再Labelし、Authorization、Quarantine、
Revocation、Incident Tracebackを迂回することを防ぐ。

## Applicability

RAG Document、Chunk、Embedding、Agent MemoryへSource／Owner／Tenant／ACL／Classification／Provenance Tagを保存するSystemに適用する。

### Non-applicability

Security／Provenance判断に一切使わないTransient Metric等は、このRequirementの中心的なMetadata Tagから除外できる。ただし
何をImmutable対象としたかをData Contractで明示する。Vector／Memoryを持たないSystemのみ全体を対象外にできる。

## Scope and assumptions

- Upstreamの「document metadata tags」は範囲が広いため、本RepositoryはAuthorization、Classification、Provenance、Traceabilityへ
  影響するTagを最低対象と解釈する。
- Source Object ID、Tenant、Owner、ACL／Policy Snapshot、Classification、Writer、Ingestion Batch／Time、Content Hash、
  Embedding Model／Chunking VersionをData Contractで選定する。
- Vector StoreがMetadata Updateを許す場合、Application PolicyとAppend-only Store／Signed Manifest等で補う。
- ImmutabilityはMetadataの真実性を保証せず、初回Write前のSource Validationが別途必要である。

## Assets, actors, identities, and trust boundaries

資産はProvenance、Authorization Tag、Classification、Incident Evidenceである。ActorはSource Connector、Ingestion Job、Writer Principal、
Vector Store、Reindex Job、Administrator、攻撃者である。Trust BoundaryはSource MetadataからInitial Commitへ、変更Requestから
Versioned Updateへ移る地点にある。Enforcement PointはIngestion Contract、Metadata Store、Update／Upsert Policyである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 各Chunk／Vectorへ必須Security／Provenance Tagを初回Write時に結び付ける。 |
| SP-2 | Commit済みTagをUpdate／Upsert／Bulk Job／Direct APIで同一Record上書きできない。 |
| SP-3 | 正当な変更を新VersionとしてAppendし、旧値・変更者・時刻・理由との関係を保持する。 |
| SP-4 | Chunk Body／EmbeddingとMetadata TagをContent Hash／Manifest等で対応付け、別Recordへの差替えを検出する。 |
| SP-5 | Reindex、Migration、Restoreでも元TagとVersion Historyを保持する。 |
| SP-6 | Mutation AttemptをSecurity Eventとして監査可能にする。 |

## Scope calibration and adjacent assurance

C8.1.3はTagを使ってRetrieval Scopeを強制し、本Controlはその判断材料の事後改ざんを防ぐ。C5.2.7のClassification Label伝播と
重なるが、本ControlはVector／Chunk Record上の初回Write後不変性に焦点を置く。Source ACL変更の反映は旧Snapshot改変ではなく
新Version／Revocationとして扱う。

## Threat and failure-mode rationale

Write権限を得た攻撃者は、`classification=restricted`を`public`へ、Tenant／Ownerを自分へ、Source／Timestampを正規値へ変更し、Poisonや
不正取得を隠す。通常のVector DB UpsertがPayloadをSilent更新すると、監査・Quarantine・権限判定の根拠が失われる。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

必須Tag、Initial Writer、Commit境界、Update／Upsert／Bulk／Admin API、Versioning、Manifest／Hash、Reindex／Restoreを追う。

### Positive verification

初回Writeで必須Tagが保存され、正当なReclassificationが旧Recordを保持した新Versionとして反映されることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 必須Tagを欠落してInitial Write | Commit前に拒否する。SP-1 |
| N-2 | Tenant、Owner、ACL、Classification、Source、Hashを直接Update | 拒否または新Version Workflowへ限定する。SP-2, SP-3 |
| N-3 | SDK Upsert、Bulk Reindex、Admin APIでN-2を再実行 | 同じ不変性を維持する。SP-2 |
| N-4 | Chunk Bodyだけ差し替えMetadataを再利用 | Binding不一致として拒否・検出する。SP-4 |
| N-5 | Migration／Backup RestoreでTag／Historyを欠落 | Production昇格を拒否する。SP-5 |
| N-6 | Metadata Mutationを試行 | 値を変えずSecurity Eventを生成する。SP-6 |

### Failure conditions

Commit後のTagをSilent更新できる、正当変更で旧値を失う、BodyとTagがBindingされない、またはBulk／Admin経路が不変性を迂回する場合は
Failを裏付ける。Immutable対象TagのContractがなければPassの証拠不足とする。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Metadata Data Contract | Data・Security Owner | 全Source／Collection | Tag変更時 | Version・承認を保持 | 必須・Immutable Tagを特定可能 |
| Append-only／Binding design | Ingestion／Storage Owner | Commit・Update・Restore | Architecture変更時 | Revision・Hashを保持 | 旧値とBody対応を検証可能 |
| Mutation／Version test | Test Harness | N-1〜N-6 | Release・Migration後 | 合成Documentを使用 | Silent Mutationがゼロ |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C8.1.3` | Immutable TagをQuery-time Scopeへ使用する。 |
| `v1.0-C5.2.7` | Classification LabelをDownstream処理へ伝播する。 |
| `v1.0-C8.3.3` | Quarantine StateとForensic Evidenceの保持にMetadataが必要となる。 |

## Known limitations and uncertainty

初回Write時に偽Metadataを受け入れればImmutableに偽情報を固定する。Append-only設計はStorage／Privacyコストを増やし、Erasure Requirementと
衝突し得る。どのOperational MetadataまでImmutableにするかはData Contractで明示的に決める必要がある。

`verifiable`はArtifactの成熟度であり、Metadataの真実性や製品適合を意味しない。

## References

- [AISVS v1.0 C8要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [AISVS v1.0 C8.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-01-Access-Controls-Memory-RAG.md)
- [C8全体分析](../../../docs/c08-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
