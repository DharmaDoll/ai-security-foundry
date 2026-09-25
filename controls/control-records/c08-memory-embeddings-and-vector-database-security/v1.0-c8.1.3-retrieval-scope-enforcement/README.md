---
title: "すべてのRetrieval OperationでScopeを強制する"
versioned_id: "v1.0-C8.1.3"
requirement_id: "C8.1.3"
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

# すべてのRetrieval OperationでScopeを強制する

AISVS Verification Level: 2

学習資料：[C8.1 Access Controls on Memory & RAG Indices](../../../docs/learning/c08-memory-embeddings-and-vector-database-security/v1.0-c8.1-access-controls-memory-rag-indices/learning.md)

## Upstream basis

AISVS `v1.0-C8.1.3`は、Retrieval OperationがScope Constraintを強制することを求める。固定Revisionの要件本文とC8.1 Researchを
確認した。ResearchはTenant、User、Role、Classification、Source ACL、Task ScopeをTrusted Server側でQueryへ注入し、Dense／Lexical／
Hybrid、Cache、Graph／Multi-hopの各境界で評価するよう補足する。

## Interpretation

Retrievalは「似ているRecordを探す処理」ではなく、認可されたRecordの中から関連Recordを選ぶ処理として実装する。認証済みCaller、
End-user Delegation、Tenant、Role／Group、Classification Clearance、Task Purpose、現在のSource ACLからEffective ScopeをServer側で計算し、
Unauthorized CandidateがRanking、Context Assembly、Citation、Cache Hitへ入る前に強制する。

AgentがUserの代理で検索する場合、AgentのService AuthorityだけでなくEnd-user／Delegationの制約を維持する。

## Security objective

Similarity、Broad Service Principal、Filter omission、Multi-hop Expansion、Semantic Cacheを通じて、Callerが受け取る権限のないDocument／Memoryが
Model Context、Score、Citation、応答へ露出することを防ぐ。

## Applicability

Vector Search、RAG、Long-term Memory、Semantic Cache、Hybrid／Federated Retrieval、Graph Expansion、Rerankingを行うSystemに適用する。

### Non-applicability

公開情報のみで、全Callerが全Recordへ同じ権限を持ち、非公開・Tenant／User差が存在しないCollectionは細粒度Scopeを対象外にできる。
その分類と公開性を継続して保証する必要がある。一つでもRestricted Recordが混在すれば適用する。

## Scope and assumptions

- ScopeはClient／Modelから渡されたFilterではなく、Trusted Identity／Policy／Source Dataから導出する。
- Pre-filterまたはEquivalentなIn-engine Authorizationを基本とし、Post-filterだけをPrimary Boundaryにしない。
- Dense、Lexical、Hybrid、Reranker、Graph、Tool、Cache、Fallbackの全PathをInventory化する。
- Authorization Service Unavailable、Empty Scope、Stale ACL時はRetrieve-allへFallbackしない。
- Revocation反映には測定可能なFreshness Objectiveを持つ。

## Assets, actors, identities, and trust boundaries

資産はDocument、Chunk、Memory、Score／Candidate Metadata、Citation、Source ACLである。ActorはEnd User、Agent、Service Principal、Retriever、
Policy Engine、Vector／Search Store、Cache、攻撃者である。Trust BoundaryはIdentity／DelegationからEffective Scopeへ、QueryからCandidate Setへ、
Retriever間のExpansionへ移る地点にある。Enforcement PointはServer-side Scope Resolver、Store Query Filter／Policy、各Expansion Boundaryである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Effective ScopeをTrusted Identity、Delegation、Tenant、Role／ACL、Classification、Task Contextから計算する。 |
| SP-2 | Unauthorized RecordをRanking／Reranking／Context Assembly／Citation前に候補から除外する。 |
| SP-3 | Dense、Lexical、Hybrid、Cache、Graph、Federated、Recursive、Tool経路ごとにScopeを強制・再評価する。 |
| SP-4 | Agent／Service Principalの権限でEnd-user／Delegation Scopeを拡張しない。 |
| SP-5 | Missing／Empty Scope、Policy障害、Stale State時にRetrieve-allへFail-openしない。 |
| SP-6 | Permission Revocationを定義SLO内に全Index／Cacheへ反映し、旧Scopeの結果を返さない。 |
| SP-7 | Authorized／UnauthorizedのCandidate Count、Score、Latency等からSensitive Recordの存在を不要に露出しない。 |

## Scope calibration and adjacent assurance

C5.2.2はEnd-user認可をRetrieval／Assemblyに維持する広いControlであり、本ControlはVector／Memory Retrievalの全PathとQuery-time Scopeへ焦点を
置く。C8.1.1のTenant分離だけではTenant内のUser差を扱えず、C8.1.2のMetadataが改ざん可能ならScope判断も信頼できない。

## Threat and failure-mode rationale

攻撃者またはPrompt-injected Agentは別Tenant／UserのDocumentに似たQueryを送り、Client Filterを省略・変更する。Broad Service Credential、
Post-filter、Graph Expansion、Semantic Cache Hit、Fallback Searchの一つでもScopeを再評価しなければUnauthorized Dataへ到達する。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Identity／Delegation、Policy、Metadata、Query Builder、Vector／Lexical／Hybrid Store、Reranker、Graph／Tool Expansion、Cache、Context Assemblyを追い、
各BoundaryのScope SourceとFailure Policyを確認する。

### Positive verification

異なるUser／Role／Tenantの試験Principalが、それぞれ許可されたRecordだけをDense／Hybrid／Cache経路で取得できることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Client／ModelがFilterを欠落、別Tenant／Userへ変更 | Trusted Scopeを強制しUnauthorized Recordを返さない。SP-1, SP-2 |
| N-2 | Broad Agent／Service Credentialで狭いEnd-userを代理 | Effective Scopeを拡張せず拒否する。SP-4 |
| N-3 | Authorized Vector SeedからUnauthorized Graph／Secondary Indexへ展開 | 各Hopで再認可し除外する。SP-3 |
| N-4 | 別PrincipalがSemantic Cache／Reranker CacheをHit | Scope-bound Cache Key／ResultでCross-scope Hitを防ぐ。SP-3 |
| N-5 | Authorization ServiceをUnavailable／Empty Scopeにする | Retrieve-allせずFail-closedにする。SP-5 |
| N-6 | Source権限をDirect／Group／Inherited経路でRevocation | 定義SLO内に全Pathから消える。SP-6 |
| N-7 | Post-filter前後の件数、Score、Latency、Empty Answerを比較 | Unauthorized Corpusの存在を不要に推測できない。SP-2, SP-7 |

### Failure conditions

ScopeをClient値へ依存する、Unauthorized Candidateを取得後にだけ捨てる、AgentのBroad AuthorityでUser Scopeを失う、一つでもRetrieval／Cache／
Expansion Pathが未認可、またはPolicy障害時に全件検索する場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Retrieval／Scope Data Flow | RAG・Security Owner | 全Retriever／Cache／Expansion | Topology変更時 | Revisionを保持 | 各BoundaryのScopeとPEPを特定可能 |
| Identity-to-filter contract | Identity・Data Owner | Tenant／User／Role／ACL | Policy変更時 | Version・承認を保持 | Trusted ContextからQuery条件を再現可能 |
| Cross-scope／Pivot test | Test Harness | N-1〜N-7 | Release・ACL変更後 | Canary Documentを使用 | Unauthorized結果・副Channelが許容範囲内 |
| Revocation freshness result | Connector／Index Owner | 全Index／Cache | 定期・Connector変更後 | 時刻とDecisionを保護 | 定義SLO内に検索除外 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C8.1.1` | TenantごとのVector Identity／Namespace衝突を防ぐ。 |
| `v1.0-C8.1.2` | Scope判断に用いるMetadata Tagの事後改ざんを防ぐ。 |
| `v1.0-C5.2.2` | End-user認可をRetrieval／Assemblyへ維持する。 |
| `v1.0-C8.3.1` | Expired Recordを全Retrieval結果から除外する。 |

## Known limitations and uncertainty

Filterable ANN、Post-filter、In-database Authorizationの能力は製品により異なる。Strong Pre-filterがRecall／Latencyへ影響する場合も、Security Scopeを
広げるFallbackは許容しない。Source ACLの正しさ、Connector Freshness、Authorization Policyの正しさは本Controlの前提となる。

`verifiable`はArtifactの成熟度であり、製品適合やSide Channelの完全排除を意味しない。

## References

- [AISVS v1.0 C8要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [AISVS v1.0 C8.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-01-Access-Controls-Memory-RAG.md)
- [C8全体分析](../../../docs/c08-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
