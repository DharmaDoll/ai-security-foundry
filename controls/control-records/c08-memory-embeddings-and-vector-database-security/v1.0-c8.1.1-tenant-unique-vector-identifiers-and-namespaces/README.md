---
title: "Vector IDとNamespaceをTenantごとに一意・衝突不能にする"
versioned_id: "v1.0-C8.1.1"
requirement_id: "C8.1.1"
verification_level: 1
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

# Vector IDとNamespaceをTenantごとに一意・衝突不能にする

AISVS Verification Level: 1

学習資料：[C8.1 Access Controls on Memory & RAG Indices](../../../docs/learning/c08-memory-embeddings-and-vector-database-security/v1.0-c8.1-access-controls-memory-rag-indices/learning.md)

## Upstream basis

AISVS `v1.0-C8.1.1`は、Vector IdentifierとNamespaceがTenantごとの一意性を強制し、Cross-tenant Collisionを
防止することを求める。固定Revisionの要件本文とC8.1 Researchを確認した。

Researchは同一Local ID、正規化差、Delimiter、Default Namespace、Update／Delete、Cache経路を試験対象として補足する。

## Interpretation

Vector／ChunkのIdentityは、信頼済み認証Contextから得たTenant IdentityとTenant内IDを結び付けたCanonical Tupleとして扱う。
Tenantが異なれば同じLocal IDを安全に共存でき、あるTenantのCreate／Upsert／Read／Update／Delete／Searchが別TenantのRecordを
上書き、Alias、参照しないようStorageとApplicationの双方で強制する。

Client指定の`tenant_id`、空値、未知値をDefault／Global NamespaceへFallbackさせない。

## Security objective

Identifier／Namespace衝突や誤Routingにより、別TenantのVectorが上書き・改ざん・削除・検索されることを防ぐ。

## Applicability

複数Tenant、Organization、Workspace、User隔離単位を同じVector／Memory基盤で扱うSystemに適用する。Collection分離、Namespace、
Shard、Metadata Partition等の実装方式を問わない。

### Non-applicability

単一の信頼Domainしか持たず、将来も複数隔離単位を共有Storeへ格納しない構成はCross-tenant部分を対象外にできる。ただし
User／Workspace境界が実質的なTenantでないか確認する。

## Scope and assumptions

- Tenant Identityは認証済みPrincipal／Server-side Mappingから導出し、Model／Client入力を信頼しない。
- Unicode、Case、Delimiter、Length／Truncationを含むCanonicalizationを一つに定義する。
- Namespace機能の存在ではなく、全CRUD／Search／Cache／Migration経路でのEnforcementを確認する。
- Vector Store管理面の侵害やBroad Admin Credentialは本Control単独では防げない。

## Assets, actors, identities, and trust boundaries

資産はVector、Chunk、Metadata、Tenant Corpus、Indexである。ActorはEnd User、Agent、Ingestion Service、Retrieval Service、
Vector Store、Administrator、攻撃者である。Trust BoundaryはRequest TenantからCanonical Storage Key／Namespaceへ移る地点にある。
Enforcement PointはServer-side Tenant Resolver、Key Builder、Store Partition／Policy、全CRUD Query Builderである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Tenant Identityを信頼済みContextから導出し、Client／Model指定値をIdentity Sourceにしない。 |
| SP-2 | Canonical TenantとLocal Vector IDの組をStorage上で一意にする。 |
| SP-3 | 異なるTenantの同一Local IDが上書き・Alias・Collisionせず共存する。 |
| SP-4 | Create／Upsert／Read／Update／Delete／Search／Cacheを同じTenant境界で制約する。 |
| SP-5 | Tenant欠落・不正・曖昧・Collision時にGlobal／Default NamespaceへFallbackしない。 |
| SP-6 | Migration、Reindex、Bulk Job、Backup Restore後もTenant Identityと一意性を維持する。 |

## Scope calibration and adjacent assurance

Tenant Namespaceが正しくても、そのTenant内でUser／Role／Task Scopeを強制しなければC8.1.3はFailになり得る。C5.3.1は
共有Model Serving StateのTenant隔離を広く扱い、本ControlはVector Identity／Namespace Collisionへ焦点を置く。

## Threat and failure-mode rationale

攻撃者は別Tenantと同じID、正規化で同値になるTenant名、Delimiterを含む値、空Tenantを用いて、Upsert／Delete対象を衝突させる。
Missing FilterやGlobal Cache KeyによりCross-tenant Retrievalも起こり得る。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Tenant Source、Canonicalization、Key／Namespace生成、Store Constraint、全CRUD／Search／Cache、Bulk／Migration／Restore経路を追う。

### Positive verification

Tenant AとBへ同じLocal Vector IDを書き、両Recordが独立して正しく取得・更新・削除できることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Tenant AのCredentialでTenant Bを自己申告 | 信頼Contextへ固定または拒否する。SP-1 |
| N-2 | 同一IDをA／BへUpsert後、片方を更新・削除 | 他方を変更しない。SP-2〜SP-4 |
| N-3 | Case、Unicode、Delimiter、TruncationでCollisionを狙う | Canonical Keyで分離または曖昧入力を拒否する。SP-2, SP-5 |
| N-4 | Tenantを欠落・空・未知値にする | Default／Globalへ入れず拒否する。SP-5 |
| N-5 | Search、Semantic Cache、Direct Store APIで別Tenant Canaryを探す | 一切返さない。SP-4 |
| N-6 | Reindex／Restore後にN-2／N-5を再実行 | 分離を維持する。SP-6 |

### Failure conditions

TenantをClient値から採用する、異Tenantの同一IDが上書きされる、CRUDの一部がTenant非Scoped、欠落時にGlobalへFallback、
またはMigrationでTenant情報を失う場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Tenant／Key Contract | Data・Security Owner | 全Collection／Memory Store | Schema変更時 | Revisionを保持 | Canonical TupleとConstraintを特定可能 |
| CRUD／Query Data Flow | Retrieval／Ingestion Owner | 全経路 | Topology変更時 | Revisionを保持 | Tenant Gateを迂回不能 |
| Collision／Canary test | Test Harness | N-1〜N-6 | Release・Migration後 | 合成Tenant Dataを使用 | Cross-tenant変更・検索がゼロ |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C8.1.3` | Tenant内のUser／Role／Task Scopeを各Retrievalで強制する。 |
| `v1.0-C5.2.2` | End-user認可をRetrieval／Assemblyへ維持する。 |
| `v1.0-C5.3.1` | 共有Model Serving状態のTenant隔離を扱う。 |

## Known limitations and uncertainty

Namespace分離はVector Store自体の認証Bypass、Admin Credential侵害、Side Channelを防がない。Tenantの定義がOrganization、User、
Workspaceで変わるSystemでは、複合隔離KeyとMigration Semanticsを明示する必要がある。

`verifiable`はArtifactの成熟度であり、製品適合やStore全体の安全性を意味しない。

## References

- [AISVS v1.0 C8要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [AISVS v1.0 C8.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-01-Access-Controls-Memory-RAG.md)
- [C8全体分析](../../../docs/c08-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
