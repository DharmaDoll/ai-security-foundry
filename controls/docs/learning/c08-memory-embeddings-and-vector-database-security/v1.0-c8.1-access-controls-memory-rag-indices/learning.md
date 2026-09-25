---
title: "AISVS C8.1 Access Controls on Memory & RAG Indices 学習ノート"
document_kind: "section-learning-note"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
section_id: "C8.1"
requirements:
  - "v1.0-C8.1.1"
  - "v1.0-C8.1.2"
  - "v1.0-C8.1.3"
last_updated: "2026-09-25"
---

# C8.1 Access Controls on Memory & RAG Indices

## 1. 文書の役割とSource separation

本書は、AISVS v1.0の固定RevisionにあるC8.1全3 Requirementを、一つのMulti-tenant RAG Scenarioで学ぶ講義である。
製品適合の証拠やControl本文の代替ではない。

- **Normative:** 下表の英語原文とLevel。
- **AISVS Research:** ACL伝播、Query-time Scope、検証例、実装上の注意を補足する。
- **Repository interpretation:** Security ContextをIngestion、Storage、全Retrieval境界で維持するという実務的な翻訳。
- **Derived insight:** 本Sectionの対話から得た、実装責任と破られるSecurity Propertyを分ける考え方。

## 2. Normative Requirements

| ID | Level | AISVS English | 日本語訳 |
|---|---:|---|---|
| `v1.0-C8.1.1` | 1 | Verify that vector identifiers and namespaces enforce uniqueness per tenant and prevent cross-tenant collisions. | Vector識別子とNamespaceがTenantごとの一意性を強制し、Tenant間の衝突を防ぐことを確認する。 |
| `v1.0-C8.1.2` | 2 | Verify that document metadata tags are immutable after the initial write. | Document Metadata Tagが最初の書込み後に不変であることを確認する。 |
| `v1.0-C8.1.3` | 2 | Verify that retrieval operations enforce scope constraints. | Retrieval OperationがScope制約を強制することを確認する。 |

正本は[固定RevisionのC8要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)である。

## 3. C8における位置づけ

C8.1は、Memory／RAG Recordの「所属」と「読める範囲」を扱う。三Requirementの分担は次のとおりである。

1. C8.1.1：Recordの物理的・論理的な所属を混同させない。
2. C8.1.2：所属、出所、信頼性を示すMetadataをSilentに変更させない。
3. C8.1.3：現在の主体とResourceを、検索のたびに照合する。

C8.2は保存前のContent ValidationとTrusted Memoryへの昇格、C8.3はExpiry、Reset、Quarantineを扱う。
C5の一般的なAuthorizationと重なるが、C8.1はChunking、Embedding、Vector／Hybrid Search、Parent Expansion、Cacheを通じて
Security Contextを失わないことへ焦点を置く。

## 4. Concrete Scenario

一つのSaaS RAGがA社とB社のSharePoint文書を取り込む。

```text
Source document
  ├─ tenant and source object ID
  ├─ owner and ACL
  ├─ classification
  └─ content
       ↓ chunking and embedding
Vector／chunk record
       ↓ dense, lexical, hybrid, cache, parent expansion
LLM context
```

A社とB社はともに`document-42`を持ち得る。AliceはA社の開発文書を読めるが、同じA社の役員文書とB社の全文書を読めない。
Vector DatabaseのService Identityは全Recordへ到達できる。この広いService AuthorityをAliceやAgentのAuthorityと取り違えないことが
Scenario全体の課題である。

## 5. 用語

- **Tenant:** SaaS上の顧客・組織の分離単位。
- **Vector ID:** Vector／Chunk Recordを識別する値。
- **Namespace:** Recordを論理的に分離する領域。Collection、Partition、Table等でも実現できる。
- **Metadata Tag:** Tenant、Source、Owner、Classification、ACL参照、Content Hash等、Recordに付随する属性。
- **Immutable:** 正当な変更も含め一切の履歴を失う上書きを許さない性質。変更が必要なら新VersionやAppend-only Eventにする。
- **Retrieval Scope:** 現在のUser、Agent、Task、Tenant、Resource Policyで読めるData範囲。
- **Parent Expansion:** 検索されたChunkから元Documentや前後Chunkを追加取得する処理。
- **PDP／PEP:** PDPはPolicyを評価する地点、PEPはその判断を実際のQueryやAccessへ強制する地点。
- **RLS:** Row-Level Security。Databaseの行単位でRead／Writeを制限する仕組み。

## 6. Threat ModelとAbuse Path

攻撃者は正規の低権限User、別Tenant、侵害されたConnector／Agent、またはRequest Bodyと検索Queryを操作できるCallerを想定する。

```text
Attacker-controlled tenant／namespace input
  → shared ID or default namespace
  → another tenant's vector is overwritten or aliased

Compromised writer
  → protected metadata is relabeled from untrusted／restricted to trusted／public
  → retrieval policy treats poison or confidential content as allowed

Broad service credential
  → initial vector filter or later parent／graph／cache boundary omits user scope
  → unauthorized content enters model context
```

Similarityは関連度であり、Authorizationではない。Agentの認証も、そのAgentがUserの権限を超えてよい証明ではない。

## 7. Security InvariantとEnforcement Point

| Requirement | Security Invariant | 決定論的なEnforcement Point |
|---|---|---|
| C8.1.1 | Tenant Aの主体は、同一IDでもTenant BのRecordを取得、更新、上書き、削除できない。Tenant不明時は拒否する。 | Trusted Identity Mapper、Key Builder、Ingestion Gateway、Namespace／Partition |
| C8.1.2 | Tenant、Source、Owner、Provenance等を同一Record上でSilentに置換できない。 | Trusted Write API、Append-only Version Store、Database Constraint／Trigger、Direct Credential制限 |
| C8.1.3 | 結果へ入る全Recordは、現在のUser、Agent、Task、Resource Policyで許可されている。Scope不明時は拒否する。 | Retrieval Service、PDP、Server-side Filter、RLS、各Expansion／Cache境界 |

Effective Scopeは、User、Agent、Task、Resource Policyの全条件を同時に満たす範囲である。広いService CredentialへFallbackしない。

## 8. 実装の選択肢

### 8.1 TenantとID

`tenant_id + source_document_id + chunk_id`を一意Keyとし、Tenantを検証済みIdentityからServer側で決める。Request Bodyの
`namespace`をAuthorityとして扱わない。Namespace／Collection分離、Database Partition、Shared Index＋Mandatory Filterを
RiskとScaleに応じて組み合わせる。

### 8.2 Immutable／Versioned Metadata

Metadataを分ける。

- Immutable：Tenant、Source ID、Original Writer、Content Hash、Ingestion Batch。
- Versioned：Classification、ACL Reference、Trust Status。
- Mutable operational state：Last Access、Retrieval Count。

Vector StoreをProvenanceの唯一の正本にせず、Append-only Document Version、Content Hash、署名付きManifest、保護Columnへの
Update拒否を使う。Bulk Import、Reindex、SDK Upsertも同じPolicyを通す。

### 8.3 Retrieval Scope

小〜中規模では、OIDC、PostgreSQL＋pgvector、RLS、必要に応じてOPA／OpenFGAを組み合わせると、Vector、Chunk、Parentを
一つのData Boundaryで扱いやすい。Managed Vector StoreではTenant NamespaceとServer-generated Metadata Filterを併用する。

```text
Verified identity
  → Retrieval Service as PEP
  → OPA／OpenFGA／application PDP
  → trusted filter or authorized resource set
  → vector query under RLS／namespace
  → reauthorization at parent, graph, tool, and cache boundaries
```

PostgreSQLのTable Owner、Superuser、`BYPASSRLS` RoleはRLSを迂回し得る。Migration OwnerとRuntime Roleを分け、Applicationを
非Owner・非Bypass Roleで動かす。ANN Engine内部でFilterが候補走査後に適用される性能上の挙動と、未認可行をTrusted Data Layer外へ
出さないSecurity上のPre-filterを混同しない。

## 9. Pass／FailとScope Calibration

| Observation | 判定 | 理由 |
|---|---|---|
| Trusted ServerがTenantを決め、同じDocument IDを別Namespace／Composite Keyで共存させる | C8.1.1 Pass候補 | Cross-tenant衝突と操作を防ぐ |
| Client指定Namespaceが検証済みTokenのTenantを上書きする | C8.1.1 Fail | 攻撃者入力がSecurity Boundaryを選ぶ |
| Security Metadata変更を拒否するか、認可済み新Versionとして旧値と履歴を保持する | C8.1.2 Pass候補 | Silent mutationを防ぐ |
| Reindex Upsertが同じIDのProvenanceを履歴なしで置換する | C8.1.2 Fail | 別Writer Pathから不変性を迂回する |
| Chunk検索、Parent、Graph、Cacheの各境界で現在のScopeを強制する | C8.1.3 Pass候補 | Retrieval composition全体でUnauthorized Dataを除外する |
| 最初のChunkだけPre-filterし、Parent全体をService Identityで取得する | C8.1.3 Fail | Chunk→Parentの新しいRetrieval境界で再認可がない |
| RLS PolicyはあるがApplicationがTable Ownerで通常運用する | C8.1.3 Fail | 実際のRuntime RetrievalがPolicyを迂回できる |

RLS設定不備のOwnerがInfrastructure Teamであっても、未認可RecordがRAGへ返ればC8.1.3のInvariantも破られる。一つのFailureが
複数Controlへ影響することは、責任分界の混同ではない。

## 10. 保証しない範囲

- C8.1.1は同一Tenant内のUser／Document ACLを保証しない。
- C8.1.2はMetadataの内容が最初から真実であることを保証しない。Source Validationが必要である。
- C8.1.3は取得を許可されたContentが安全、正確、Poisonされていないことを保証しない。
- C8.1全体はPrompt Injection、Embedding Poisoning、Expiry、Physical Deletionを単独では解決しない。
- 特定製品、OPA、OpenFGA、RLSの導入だけではPassにならない。Runtime OutcomeをNegative Testで確認する。

## 11. 対話の再構成

### 問い1：Request BodyがTokenのTenantを上書きする

**学習者の判断:** Fail。Tokenから取得したIdentityの範囲へ書くべきで、Request Bodyは改ざん可能。

**整理:** 正しい。さらにToken Claimも署名、Issuer、Audience、有効期限等を検証し、Trusted Serverが内部Tenant IDへMappingする。
本質は、認証済み境界を攻撃者入力で上書きさせないことである。

### 問い2：Reindex JobだけがMetadataを上書きできる

**学習者の判断:** Fail。変更履歴がなく、不正な変更と区別できない。

**整理:** 正しい。第一のFailureはReindex PathがImmutable Metadataを上書きできること、履歴欠落は正規変更、誤操作、攻撃を
区別不能にする第二のFailureである。履歴だけ追加して無制限上書きを残しても十分ではない。

### 問い3：RLSは正しいがApplicationがTable Ownerで接続する

**学習者の判断:** Pass。DB設定の問題なので別Categoryで扱うべき。

**訂正:** C8.1.3としてもFailである。実際のApplication RetrievalがRLSを迂回し、Unauthorized Recordを返せるからである。
Root Causeの技術領域と、破られたSecurity Invariantは別の軸である。Migration Ownerと非Owner Runtime Roleを分離する。

## 12. このセッションから得た洞察

> Failureの技術的な所有者と、破られるSecurity Invariantは一致するとは限らない。

Controlは「どのTeamの設定ミスか」ではなく、最終的に保証すべきOutcomeが成立するかを問う。Database Configuration、Connector、
Cache、Parent Storeの不備であっても、未認可ContentがRAG Contextへ入ればRetrieval Authorizationは破られる。

また、C8.1の三要件は独立した点検項目ではなく、次の連鎖である。

> IngestionでSecurity Contextを保持し、StorageでSilentな書換えを防ぎ、全Retrieval境界で現在の権限を再評価する。

## 13. 設計レビュー項目

- Tenant／Namespaceは検証済みIdentityからServer側で決まるか。
- Create、Update、Delete、Bulk Import、Reindexで同じTenant Boundaryを強制するか。
- Case、Unicode、Delimiter、空値、Default NamespaceでID衝突しないか。
- Security／Provenance MetadataのProtected Fieldと変更方式が明示されているか。
- Direct Vector DB CredentialでProtected Metadataを迂回できないか。
- Dense、Lexical、Hybrid、Direct ID、Parent、Graph、Reranker、Cacheの全経路を列挙したか。
- AgentのEffective ScopeがUserより広くならないか。
- Scope欠落、PDP停止、Policy未定義時にFail Closedするか。
- Runtime DB RoleがOwner、Superuser、`BYPASSRLS`ではないか。
- 別Tenant Canary、Metadata改ざん、Filter omission、Parent Pivot、Cache HitをNegative Testしたか。

## 14. ControlへのLink

- [C8.1.1 TenantごとのVector ID／Namespace](../../../../control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.1.1-tenant-unique-vector-identifiers-and-namespaces/README.md)
- [C8.1.2 Immutable Document Metadata](../../../../control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.1.2-immutable-document-metadata-tags/README.md)
- [C8.1.3 Retrieval Scope Enforcement](../../../../control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.1.3-retrieval-scope-enforcement/README.md)

## 15. References

- [AISVS v1.0 C8 Normative Requirements](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [AISVS v1.0 C8.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-01-Access-Controls-Memory-RAG.md)
- [PostgreSQL Row Security Policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [pgvector Filtering and Multitenancy](https://github.com/pgvector/pgvector#filtering)
- [Open Policy Agent documentation](https://www.openpolicyagent.org/docs)
- [OpenFGA Concepts](https://openfga.dev/docs/concepts)
- [Pinecone Multitenancy](https://docs.pinecone.io/guides/index-data/implement-multitenancy)
