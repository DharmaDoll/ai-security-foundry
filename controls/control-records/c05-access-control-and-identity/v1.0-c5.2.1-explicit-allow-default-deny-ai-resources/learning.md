---
title: "AISVS v1.0-C5.2.1 Explicit Allow and Default Deny Learning Note"
document_kind: "requirement-learning-note"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
requirement_id: "C5.2.1"
verification_level: 2
research_last_researched: "2026-07-14"
last_updated: "2026-09-05"
---

# C5.2.1 Explicit AllowとDefault Deny 学習ノート

[Control本文：解釈・検証・証拠・限界](README.md)


## この文書について

この文書は、AISVS `v1.0-C5.2.1`を題材に行った学習セッションを、後から単独で
参照できる講義として再構成したものである。

これはControl本文、製品の適合判定、またはAISVS原文の代替ではない。次の情報を
意識して分離する。

- **Normative:** AISVS v1.0が実際に要求していること。
- **Research:** AISVS Researchが与える脅威・検証上の補足。
- **Repository interpretation:** 現場のArchitecture Reviewへ適用するための解釈。
- **Derived insight:** 学習中の問いから得られた、隣接するSecurity上の洞察。

## 1. Normative Requirement

- Versioned ID: `v1.0-C5.2.1`
- AISVS Verification Level: `2`

> Verify that every AI resource (datasets, endpoints, vector collections,
> embedding indices, compute instances) enforces access controls with explicit
> allow-lists and default-deny policies.

意味を崩さない日本語訳:

> すべてのAI Resource（Dataset、Endpoint、Vector Collection、Embedding Index、
> Compute Instance）が、明示的なAllow-listとDefault-deny PolicyによるAccess Controlを
> 強制していることを検証する。

原文が直接要求する要素は次の三つである。

1. 対象が一部ではなく`every AI resource`である。
2. 許可するAccessが明示されている。
3. 明示的なAllowがないAccessはDefaultで拒否される。

原文のResource一覧は例示である。ResearchはModel Artifact、Prompt Store、Cache、Agent
Tool等も含め、AI Systemに追加されたResourceをInventoryする必要性を補足している。

## 2. C5における位置づけ

C5.1はAuthenticationを扱う。

> Callerは誰か。そのIdentity Evidenceを信頼できるか。

C5.2はAuthorizationを扱う。

> そのPrincipalに、このResourceへ、このActionを行わせてよいか。

C5.2.1はAI Resource Authorizationの基礎である。C5.2.2以降は、End-user Context、
Inference Output、PDP Isolation、JIT Privilege、Classification Label等の、より具体的な
Propertyを扱う。

## 3. Security Objective

C5.2.1の本質は次である。

> AI固有のResourceも、明示的に許可された条件以外では利用できてはならない。

保護すべきResourceを認識していなければPolicyを定義できない。このため最初の
Enforcement Artifactは、しばしばResource Inventoryになる。

AI Resourceの例には次がある。

- Training、Fine-tuning、Evaluation Dataset。
- Model Weights、Model Registry、Artifact Store。
- Inference、Embedding、Administration Endpoint。
- Vector Collection、Embedding Index、Feature Store。
- Prompt Template、System Prompt、Prompt／Response Cache。
- Agent Tool、MCP Endpoint、Tool Manifest。
- Training／Inference Compute、GPU、Job Scheduler。
- Backup、Snapshot、Export Artifact等の代替Access Path。

> 存在を認識していないResourceを、正しく認可することはできない。

## 4. 講義用Scenario

社内RAG Systemに次のResourceがある。

```text
Web Application
    |
    v
RAG Service
    |
    v
Vector Database
    +-- hr-documents
    +-- engineering-documents
    +-- public-documents
```

Web ApplicationにはRole Checkがあるが、Vector Databaseは同じCluster内から認証なしで
接続できるとする。

```text
正規経路:
User -> Web Application -> RAG Service -> Vector Database
          Authorizationあり

迂回経路:
Compromised Workload ------------------> Vector Database
                                          Authorizationなし
```

通常経路が安全でも、Resourceへ一つでも無制御な到達経路があればC5.2.1はFailする。
Private NetworkやCluster Membershipだけでは、PrincipalとActionを判定するAccess
Controlにならない。

## 5. 用語

### AI Resource

AI Systemが読み取り、変更、実行、消費、または管理するSecurity上の保護対象。Dataだけ
でなくEndpoint、Tool、Model Artifact、Compute、Cache、Backupも含む。

### Principal

Accessを要求する主体。Human User、Service Account、Agent、Workload、MCP Server、
Tool、Administrator等が該当する。

### Allow-list

許可する対象または条件を明示するPolicy。旧来「Whitelist」と呼ばれた考え方に近いが、
固定された名前一覧だけを意味しない。

実務では、少なくとも次の組み合わせを表す。

```text
Principal x Action x Resource x Context -> Allow
```

例えば次である。

```text
Principal: rag-query-service
Action:    query
Resource:  production-support-vectors
Context:   environment=production, tenant=tenant-a
Decision:  allow
```

RBAC、ABAC、ReBAC、Capability Token、Policy-as-code等でも、Allow条件が明示されて
いればよい。特定IPやService Account名だけの単純Listへ限定されない。

### Default Deny

適用できる明示的Allow Ruleがない場合、Accessを拒否するPolicy。次の状態もDenyへ
倒す。

- Principal、Tenant、Scope等がMissingまたはUnverifiable。
- ResourceまたはActionがPolicyに未登録。
- Policy Decision PointがUnavailableまたはTimeout。
- Allow-listが空。
- 新しいResourceがInventoryまたはOnboardingを完了していない。

> Deny Ruleが見つからないから許可するのではなく、Allow Ruleが見つかった場合だけ
> 許可する。

### Policy Decision Point (`PDP`)

Policyを評価し、Allow／Denyを判断する場所。

### Policy Enforcement Point (`PEP`)

PDPの判断を実際のResource Accessへ強制する場所。正しいDeny Decisionがあっても、
CallerがPEPを迂回できればResourceは保護されない。

### Complete Mediation

保護対象へのすべてのAccessを、毎回Authorization Checkで仲介するSecurity Principle。
通常のUIやAPIだけでなく、Admin、Batch、Debug、Backup、Migration、別Port等も含む。

## 6. Threat ModelとAbuse Path

### Unmanaged AI Resource

```text
新しいVector Collectionを作成
  -> IAM／Policy Inventoryへ登録しない
  -> Product DefaultがAnonymousまたはBroad Access
  -> Unauthorized Retrieval／Modification
```

### Default Allow

```text
Callerに一致するDeny Ruleがない
  -> ApplicationがAllowと解釈
  -> Unknown Principalまたは新しいActionを許可
```

Empty Allow-listを「制限なし」と解釈する実装も同じFailureである。

### PEP Bypass

```text
通常RequestはGatewayでAuthorization
  -> 攻撃者が内部Endpoint、別Port、Batch Credential等を発見
  -> Gatewayを通らずResourceへ直接Access
```

### Shared Service AccountによるConfused Deputy

```text
End User A
  -> Broad Service Accountを持つRAG Service
  -> User BのDocumentをRetrieval
```

Vector DatabaseがService Accountだけを明示的にAllowし、他をDefault Denyしているなら、
C5.2.1にはPassし得る。End UserのAuthorization Contextを失った根本FailureはC5.2.2で
扱う。ただしService AccountへのGrant自体が意図せずBroadまたは暗黙のDefault Allow
なら、C5.2.1もFailし得る。

## 7. Security InvariantとEnforcement

### Security Invariant

> 明示的に許可されたPrincipal、Action、Resource、Contextの組み合わせ以外では、
> どの到達経路からもAI Resourceを利用できない。

このInvariantは次を含む。

1. 未知または未登録のResourceは自動的に公開されない。
2. Policy不足、評価不能、依存Service障害時はAllowへFallbackしない。
3. Gateway、PEP、Native IAM等のEnforcementを迂回する経路がない。
4. Read、Write、Delete、Execute、Admin等のActionを区別する。

### Enforcement Point

実装方式は一つに限定されない。

- Resource Native IAM／RBAC。
- API GatewayまたはAuthorization Proxy。
- Service Mesh Authorization。
- Cloud IAM、Object Storage Policy、Database Authorization。
- Cluster RBAC、Compute Scheduler、Job／Namespace Policy。
- Resourceへ到達する全経路を強制する外部PEP。

External PEPを使う場合、ResourceへPEP以外から直接到達できないことがPass条件になる。
「通常はGatewayを使う」という運用手順だけではComplete Mediationにならない。

## 8. Pass／FailとScope Calibration

| Scenario | C5.2.1評価 | 理由または別の問題 |
|---|---|---|
| CollectionごとにQuery／Writeを明示し、その他をDefault Denyする | Pass候補 | Explicit AllowとDefault DenyをResource Accessへ強制している |
| Vector DBはPrivate Subnet内だが、そのSubnetからは認証なし | Fail | Network位置だけではPrincipalとActionを認可していない |
| Deny-listに載っていないCallerをすべて許可する | Fail | Default Allowである |
| Empty Allow-listをAllow-allとして処理する | Fail | Policy不足時に危険側へ倒れる |
| UIにはRBACがあるがBackendへ直接接続できる | Fail | PEPを迂回でき、Complete Mediationがない |
| Datasetは保護されているが同じDataを含むBackupは公開されている | Fail | 代替Resource／Pathが無制御である |
| External PEPが全Accessを仲介し、Resourceへの直接到達を拒否する | Pass候補 | Native IAMでなくてもOutcomeを満たせる |
| Resourceは意図的にQuarantineされ、明示的なEmpty Allow Setで全Accessを拒否する | Pass候補 | Deny-allが意図されたPolicy Stateとして管理されている |
| Production ResourceのAllow Ruleを登録し忘れ、正規Callerも全員403になる | Passと断定しない | Default DenyのNegative Testには成功するが、意図されたExplicit Allow PolicyとPositive Testが欠ける |
| Vector DBはBroad Service Accountだけを明示的にAllowするが、RAGがEnd-user権限を無視する | C5.2.1はPassし得る | C5.2.2が直接Failする。Service Account Grant自体の意図とResource粒度は別途確認する |

### Positive TestとNegative Test

C5.2.1はDenyだけ確認して完了しない。

```text
Positive Test:
  Explicitly allowed Principal + Action + Resource + Context -> Allow

Negative Test:
  Unknown Principal、別Action、別Resource、Missing Context -> Deny
```

正規Callerまで拒否する状態はUnauthorized Accessを防ぐ意味では安全側だが、意図した
Access Control Policyが完成した証拠にはならない。

## 9. 保証しない範囲と隣接Property

C5.2.1にPassしても次は保証しない。

- Service Accountの背後にいるEnd UserのAuthorization Contextを維持すること。
- Retrieval、Reranking、Parent Expansion、Assembly等の各段階で認可すること。
- Allow PolicyのBusiness SemanticsやLeast Privilegeが十分であること。
- AgentがPrompt Injectionを受けないこと。
- Inference OutputからUnauthorized Dataを除くこと。
- PDPをAgent Runtimeから隔離すること。
- Tenant間のModel State、Cache、Computeを分離すること。

主な隣接Requirementは次である。

| Requirement | 境界 |
|---|---|
| C5.2.2 | Broad Service Accountへ依存せず、End-user AuthorizationをRetrieval／Assembly全段階へ維持する |
| C5.2.4 | Inference後のResponseからUnauthorized Dataを除外する |
| C5.2.5 | Agent AuthorizationのPDPをAgent Runtimeから隔離する |
| C5.3.1／C5.3.2 | Shared Model StateとComputeにおけるTenant Isolationを守る |
| C9.5.1／C9.5.3 | Agent Tool／Parameter AuthorizationとModel外の決定論的Enforcementを行う |

## 10. 「ホワイトリスト」という理解のCalibration

学習者の次の理解は本質を捉えている。

> 所謂ホワイトリストであり、「この場合だけ許可」を定義することが重要である。

現在の用語ではAllow-listと呼ぶことが多い。Security上重要なのは呼称ではなく、
Positive Authorization Modelであることだ。

ただし、次のようなPrincipal名だけのListでは不十分になり得る。

```text
allowed_principals = ["rag-service"]
```

`rag-service`が全CollectionへRead／Write／Deleteできるなら、条件が粗すぎる可能性が
ある。実務では次まで限定する。

```text
allow only if:
  principal == rag-query-service
  action == query
  resource == tenant-a-support-vectors
  environment == production
  authorization_context is trusted and current
```

さらに、そのRuleが正しくても、迂回経路があればC5.2.1はFailする。

> 「この場合だけ許可」を定義することと、すべてのAccessをその定義で検査することの
> 両方が必要である。

## 11. 対話の再構成

### Q1: Resource AccessとEnd-user Authorizationの境界

**問い:** Vector Databaseは`rag-service`だけを明示的にAllowし、他をDefault Denyする。
RAG Serviceは全Userに同じService Accountを使用し、End-user権限を確認せず別Tenantの
Documentを返した。C5.2.1はPassか。どのRequirementが直接Failするか。

**学習者の判断:** Fail。Authorizationの問題だがRequirementは分からない。

**整理:** System全体がFailという感覚は正しい。ただし、明示的なService Account Grantと
Default DenyがResourceで強制されているならC5.2.1にはPassし得る。Broad Service Account
だけに依存してEnd-user Contextを失ったFailureはC5.2.2が直接扱う。許可された代理人が
誰のためにAuthorityを使っているかは別のPropertyである。

### Q2: Policy未登録で全Requestが403になる場合

**問い:** 新しいProduction Vector CollectionのAllow Ruleを登録し忘れ、すべてのRequestが
403になる。C5.2.1はPassか。

**学習者の判断:** Fail。要件に必要なAllow Ruleを定義していない。

**整理と問いの訂正:** 判断は妥当である。元の問いは、Fail-closedの安全性と完成した
Access ControlのPassを混同させる曖昧さがあった。Default DenyのNegative Testには成功
しているが、意図されたExplicit AllowとPositive Testがないため、そのままC5.2.1 Pass
とは断定しない。意図的QuarantineとしてEmpty Allow Setを明示管理する場合とは分ける。

### Q3: Gatewayを迂回する内部経路

**問い:** Agentからの通常経路ではGatewayがExplicit AllowとDefault Denyを強制するが、
Cluster内Workloadは認証なしでVector Databaseへ直接接続できる。Passか。

**学習者の判断:** Pass。明示的Allow PolicyとDefault Denyを強制すると書かれている。

**整理:** Failである。PolicyはGateway経路にしか適用されず、Resourceへの別経路は
Default Allowである。C5.2.1の主語は通常Requestではなく`every AI resource`であり、
Complete Mediationが必要である。

### Q4: Allow-listの理解

**学習者の所感:** 所謂ホワイトリストであり、「この場合だけ許可」を定義することが
重要である。認識が誤っていれば指摘してほしい。

**整理:** 核は正しい。ただし、静的な名前Listだけでなく、Principal、Action、Resource、
ContextのPositive Ruleとして捉える。さらにPolicy定義だけでなく、すべてのAccess Pathで
そのRuleを強制する必要がある。

## 12. このセッションから得られた洞察

1. **存在を認識していないResourceを正しく認可することはできない。** Resource
   InventoryはC5.2.1の出発点である。
2. **Allow-listの本質は「この場合だけ許可」である。** Deny RuleがないことをAllowの
   根拠にしない。
3. **Allow-listは名前の固定Listとは限らない。** `Principal x Action x Resource x
   Context`のPositive Authorization Policyとして設計する。
4. **Empty Policyは自由を意味しない。** 判断材料がない場合はDenyする。
5. **Default Denyの成功だけでControl全体のPassにはならない。** 意図したAllowの
   Positive Testも必要である。
6. **Fail closedとAvailability Failureを区別する。** 正規Callerの403は運用Failureに
   なり得るが、Unauthorized Accessを許すFailureとは異なる。
7. **Policyが正しいことと、すべてのAccessがPolicyを通ることは別である。** Complete
   Mediationがなければ迂回される。
8. **内部NetworkはIdentityでもAuthorizationでもない。** Cluster内Workloadの侵害を
   想定し、Resourceまたは強制されたPEPで認可する。
9. **Resourceへの入場許可と、代理人が誰のために権限を使うかは別である。** C5.2.1に
   PassしながらC5.2.2のConfused Deputy Failureを持ち得る。
10. **正規経路だけのPassをResource全体のPassと呼ばない。** Admin、Batch、Backup、
    Debug、Migration、別Port等をNegative Testする。
11. **System全体の重大Failureと個別Controlの評価を分ける。** Scopeを守ることで、
    修正すべきEnforcement Pointを誤らない。

## 13. 後から設計レビューするときの確認事項

- Dataset、Model、Endpoint、Vector Store、Embedding Index、Tool、MCP、Compute、Cache、
  Backupを含むAI Resource Inventoryがあるか。
- Resource OwnerとAuthoritative Policyを特定できるか。
- Allow RuleはPrincipal、Action、Resource、Contextを十分な粒度で表すか。
- Unknown Principal、Unknown Resource、New Action、Missing ContextをDenyするか。
- Empty Allow-list、PDP Timeout、Policy取得失敗時にDenyするか。
- 意図したAllowに対するPositive Testがあるか。
- Anonymous、Low-privilege、別Tenant、Stale Credentialに対するNegative Testがあるか。
- UI、API、CLI、Admin、Batch、Backup、Debug、Migration、別Portを列挙したか。
- GatewayまたはPEPを迂回してResourceへ直接到達できないか。
- Private NetworkやCluster MembershipだけをAccess Controlと扱っていないか。
- Shared Service Account GrantとEnd-user Authorizationを混同していないか。
- New ResourceがPolicy Onboarding前に公開されないか。
- Default Deny障害時にBroad Static CredentialへFallbackしないか。
- Decision LogでPrincipal、Action、Resource、Decision、Policy Versionを追跡できるか。
- C5.2.1のPassと、C5.2.2、C5.2.5、C5.3、C9の評価を分けたか。

## References

- [OWASP AISVS v1.0 C5 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [OWASP AISVS v1.0 C5.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-02-AI-Resource-Authorization-Classification.md)
- [OWASP AISVS v1.0 C9 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
