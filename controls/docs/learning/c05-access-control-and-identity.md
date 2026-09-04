---
title: "AISVS C5 Access Control and Identity Learning Plan"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
overall_status: "in-progress"
current_module: "M4"
last_updated: "2026-09-04"
---

# AISVS C5 Access Control and Identity 学習計画

## 目的

AISVS C5のRequirementを暗記するのではなく、AI SystemにおけるIdentity、
Authorization、Resource protection、Multi-tenant isolationを設計・レビュー・
検証できる状態を目指す。

修了時には、具体的なSystemについて次を説明できなければならない。

- 誰のAuthorityが行使されるか。
- User、Application、Agent、Model、Tool、Service identityをどう区別するか。
- 重要なTrust Boundaryがどこにあるか。
- Authorizationをどこで決定し、どこで強制するか。
- RAG、Tool invocation、Shared infrastructureでAuthorityやTenant境界が失われる
  経路は何か。
- Security InvariantをどのNegative testとEvidenceで検証するか。
- C5だけでは保証できない残存Riskは何か。

## 対象範囲

この計画は、固定したAISVS v1.0 snapshotのC5を対象とする。C5には次の3 Section、
11 Requirementがある。

- C5.1 Authentication: 2 Requirement
- C5.2 AI Resource Authorization & Classification: 7 Requirement
- C5.3 Multi-Tenant Isolation: 2 Requirement

AISVSのNormative chapterをRequirementのSource of Truthとし、対応するAISVS
Research資料を必須の補助教材として読む。ResearchのImplementation例を、そのまま
Normative requirementとして扱ってはならない。

## 進め方

- 標準期間: 6週間
- 標準学習時間: 週3〜5時間
- 進行単位: 一度に1 Module
- 学習順序: 原則としてM1からM6
- 評価方法: 説明、Architecture分析、Negative test、Evidence設計

各Moduleでは、最初に前回内容を自分の言葉で説明し、その後に新しい概念、具体的な
Use case、Abuse case、検証課題へ進む。読了や会話への参加だけではModuleを完了と
しない。

## M1 — IdentityとAuthorizationの基礎

### 学習項目

- Human identityとWorkload identity
- AuthenticationとAuthorization
- Principal、Resource、Action、Context
- RBAC、ABAC、ReBAC
- PDP、PEP、PAP、PIP
- Least privilegeとDefault deny
- Delegation、Impersonation、Credential forwarding
- Scoped、Audience-bound、Short-lived credential

### 演習

`User → Agent → Tool → Internal API`について、各HopのIdentity、Authority、
Authentication、Authorization decision、Enforcement pointを図示する。

### 完了条件

- Agent identityの存在がActionのAuthorizationを意味しない理由を説明できる。
- End userとAgent、Application、Downstream serviceのAuthorityを区別できる。
- 一つのUse caseについてPDPとPEPを特定できる。

## M2 — C5.1 Authentication

### 対象Requirement

- `v1.0-C5.1.1`: High-risk AI operationのStep-up authentication
- `v1.0-C5.1.2`: Federated／Multi-system AgentのToken security

### 学習項目

- Model deployment、Weight export、Training data accessなどのHigh-risk operation
- Human authenticationとAgent authenticationの分離
- Token scope、Audience、Expiry、Signature
- Long-lived service credentialとExcessive privilege

### 演習

High-risk operationごとに、Initiating principal、必要なAuthentication strength、
Token constraint、Expiry、Approval、Audit evidenceを表にする。

### 完了条件

- 通常SessionだけでHigh-risk operationを許可しない理由を説明できる。
- Expired token、Wrong-audience token、Over-scoped tokenのNegative testを定義できる。
- Step-up authenticationとAuthorizationを混同せず説明できる。

## M3 — C5.2前半: Resource authorizationとRetrieval

### 対象Requirement

- `v1.0-C5.2.1`: AI ResourceのAccess controlとDefault deny
- `v1.0-C5.2.2`: Retrieval／Assembly各段階のEnd-user authorization
- `v1.0-C5.2.3`: Sensitive dataとRetrieval architecture
- `v1.0-C5.2.4`: Unauthorized dataのPost-inference filtering

### 学習項目

- Similarity is not authorization
- Service accountのAuthorityとEnd-user authority
- Retrieval前のAuthorizationと出力後Filteringの役割
- TenantやRoleをModel contextだけから取得する危険性
- RAGを使用すること自体はConfidentialityの保証にならないこと

### 演習

Multi-tenant RAGのData flowを、`User → Application → Query construction →
Retrieval → Document assembly → Model → Output filtering → Response`の順に描き、
各段階へPrincipal、Tenant context、Trust Boundary、Enforcement pointを配置する。

### 完了条件

- Tenant AがTenant BのDocumentを取得できないNegative testを設計できる。
- RetrievalとAssemblyの両方でAuthorization contextが必要な理由を説明できる。
- Post-inference filteringを唯一のAuthorization boundaryにできない理由を説明できる。

## M4 — C5.2後半: Agent PDP、JIT access、Classification

### 対象Requirement

- `v1.0-C5.2.5`: Agent authorization PDPの隔離
- `v1.0-C5.2.6`: Privileged AI Resource accessのJIT付与と自動失効
- `v1.0-C5.2.7`: Data classification labelのDownstream伝播

### 中心教材

- [Golden Control](../../control-records/c05-access-control-and-identity/v1.0-c5.2.5-agent-authorization-pdp-isolation.md)

### 学習項目

- AgentにAuthorization decisionを委ねない理由
- 別Processと別Trust Boundaryの違い
- Decision forgery、Replay、PDP bypass、Fail-open
- Just-in-time privilegeとStanding privilege
- Source dataからEmbedding、Cache、OutputへのClassification伝播

### 演習

Golden ControlのSP-1〜SP-8について、各Propertyを破るFailure-prone designと、
それを検出するNegative testを一つずつ作る。

### 完了条件

- PDPを別ServiceにしただけではC5.2.5を満たさない理由を説明できる。
- Agent compromise boundaryからPDPを攻撃するNegative testを設計できる。
- JIT accessとClassification propagationがPDP isolationとは別のSecurity property
  であることを説明できる。

## M5 — C5.3 Multi-Tenant Isolation

### 対象Requirement

- `v1.0-C5.3.1`: Shared model servingにおけるTenant分離
- `v1.0-C5.3.2`: Shared computeを通じた観測・干渉の防止

### 学習項目

- Prompt、Embedding、Fine-tuning、Cache、BatchingのTenant境界
- KV／Prefix cacheの共有
- Shared GPU、Memory、Filesystem、Queue
- Cross-tenant information leakageとResource interference
- Logical isolationとInfrastructure isolation

### 演習

Vector database、Prompt cache、Model server、GPU、Logging pipeline、Evaluation
datasetについて、Cross-tenant failure mode、Security invariant、Negative test、
必要なEvidenceを整理する。

### 完了条件

- Shared serviceのTenant isolationをComponent別に分析できる。
- Application-level Authorizationだけでは防げないInfrastructure boundaryを
  特定できる。
- Tenant分離の成功を、設定値ではなく観測可能な結果で検証できる。

## M6 — 総合演習

Multi-tenant RAG Agent、または同等にC5の複数Sectionを横断するSystemを一つ選ぶ。

### 成果物

1. Use caseとScope
2. Asset、Actor、Identity一覧
3. Trust BoundaryとData flow
4. Resource／Action／PrincipalのAuthorization matrix
5. Security invariant
6. Deterministic enforcement point
7. Positive test
8. Negative／Abuse-case test
9. Evidence expectation
10. Known limitationとResidual risk
11. 関連するC5 Requirementと、その関係の根拠

### 完了条件

- Requirementの言い換えではなく、Failure modeとEnforcement pointを説明できる。
- Security invariantごとに少なくとも一つのNegative testがある。
- EvidenceのProducer、Scope、Freshness、Integrity、Acceptance criteriaが明確である。
- C5だけでは保証できない範囲を明記できる。
- 総合成果物が本人による振り返りを完了している。

## Progress tracker

Statusは`not-started`、`in-progress`、`completed`、`blocked`のいずれかを使う。
`completed`は完了条件を満たす説明または成果物が確認できた場合だけ記録する。

| Module | Subject | Status | Completion evidence | Last updated | Next action |
|---|---|---|---|---|---|
| M1 | IdentityとAuthorizationの基礎 | not-started | — | 2026-09-03 | C5.2.5 Review後にIdentity chain演習を開始する |
| M2 | C5.1 Authentication | not-started | — | 2026-09-03 | M1完了後に開始する |
| M3 | C5.2.1〜C5.2.4 | not-started | — | 2026-09-03 | M2完了後に開始する |
| M4 | C5.2.5〜C5.2.7 | in-progress | Shared identityによるPDP再配置を隔離失敗と正しく判定 | 2026-09-04 | C5.2.5の適用範囲をReviewする |
| M5 | C5.3 Multi-Tenant Isolation | not-started | — | 2026-09-03 | M4完了後に開始する |
| M6 | 総合演習 | not-started | — | 2026-09-03 | M1〜M5完了後に開始する |

## 学習Log

各Sessionの終了時に、実施内容、確認できたEvidence、不明点、次のActionを追記する。
機密情報、実環境のCredential、Customer dataは記録しない。

| Date | Module | Topics and exercises | Evidence or outcome | Open questions | Next action |
|---|---|---|---|---|---|
| 2026-09-03 | Planning | 6 Moduleの学習計画と進捗管理方法を作成 | 学習計画をRepositoryへ保存 | — | M1のIdentity chain演習を開始する |
| 2026-09-04 | M4 | C5.2.5の平易な解釈とPass／Fail境界 | AgentとPDPが同じ再配置権限を共有する構成を、実効的な隔離がないためFailと正しく説明 | ApplicabilityとNon-applicabilityの確認が未完了 | C5.2.5の適用範囲をReviewする |

## 進捗更新手順

今後この計画に沿って学習を支援するAgentは、各Sessionで次を行う。

1. Session開始時にfront matter、Progress tracker、直近の学習Logを確認する。
2. `current_module`の完了条件に沿って、一つのModuleだけを進める。
3. 説明を読むだけでなく、Scenarioへの適用または成果物作成を含める。
4. Session終了時にStatus、Completion evidence、Last updated、Next actionを更新する。
5. `completed`へ変更する前に、すべての完了条件を確認する。
6. Blockerがある場合は`blocked`とし、解除条件を学習Logへ記録する。
7. 全Module完了時に`overall_status: completed`へ更新する。

## Primary references

- [OWASP AISVS v1.0 C5 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [OWASP AISVS v1.0 Research hub](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/README.md)
- [AISVS C5.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-02-AI-Resource-Authorization-Classification.md)
