---
title: "AISVS v1.0-C5.2.6 Just-in-time Privileged Access Learning Note"
document_kind: "requirement-learning-note"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
requirement_id: "C5.2.6"
verification_level: 3
research_last_researched: "2026-07-14"
last_updated: "2026-09-07"
---

# C5.2.6 Just-in-time Privileged Access 学習ノート

[Control本文：解釈・検証・証拠・限界](README.md)


## この文書について

この文書は、AISVS `v1.0-C5.2.6`を題材に行った学習セッションを、後から単独で
参照できる講義として再構成したものである。

これはControl本文、製品の適合判定、またはAISVS原文の代替ではない。次を分離する。

- **Normative:** AISVS v1.0が実際に要求していること。
- **Research:** AISVS Researchが示すThreat、Verification、実装上の注意。
- **Repository interpretation:** 現場のArchitecture Reviewへ適用するための解釈。
- **Derived insight:** 具体例と質疑から得た、Requirement外を含むSecurity上の洞察。

学習の完了によってControl maturityは変更しない。
別途整備した[Control本文](README.md)
では、適用範囲、検証、Evidenceと保証の限界を整理している。

## 1. Normative Requirement

- Versioned ID: `v1.0-C5.2.6`
- AISVS Verification Level: `3`

> Verify that privileged access to model weights, training pipelines, and
> production AI configuration is granted just in time, with a defined maximum
> session duration and automatic expiry. Zero Standing Privilege (ZSP) to these
> resources is encouraged.

意味を崩さない日本語訳:

> Model Weight、Training Pipeline、およびProduction AI Configurationへの特権Accessが、
> 必要な時点で付与され、最大Session時間が定義され、自動的に失効することを検証する。
> これらのResourceに対するZero Standing Privilege（ZSP）が推奨される。

原文が直接要求する中心は次の3点である。

1. Privileged AccessをJust-in-timeで付与する。
2. 最大Session時間を定義する。
3. その時間を過ぎたら自動的に失効させる。

ZSPは`encouraged`であり、AISVS原文は完全なZSPを明示的な必須条件とは表現していない。
一方、JITと呼ぶ以上、通常のPrivileged Accessを恒久的にActiveにしたままにしてはならない。

## 2. C5における位置づけ

C5.2.6は、AI Systemの重要Resourceに対するPrivilege Lifecycleを扱う。

```text
C5.1.1:
  High-risk Operationの直前に、Principalを再確認する

C5.1.2:
  Federated／Multi-system Agentが使うTokenの性質を制限する

C5.2.5:
  Agentが自分を認可するPDPを支配できないようにする

C5.2.6:
  重要なAI Resourceへの特権を、必要な期間だけ存在させる
```

このRequirementを一言で表すなら、次である。

> 強い権限を、普段から持たせたままにしない。

### C5.1.2との違い

C5.1.2とC5.2.6は、同じ短命Token技術を利用することがある。しかし、検証する軸は異なる。

| 観点 | C5.1.2 | C5.2.6 |
|---|---|---|
| 主な対象 | Federated／Multi-system環境のAI Agent | Model Weight、Training Pipeline、本番AI設定へのPrivileged Access |
| 中心的な問い | System間でどのようなCredentialを使うか | Privilegeをいつ与え、いつ消すか |
| 明示された性質 | 短命、最小Scope、暗号学的署名 | JIT付与、最大時間、自動失効 |
| 主なPrincipal | AI Agent | Human、Agent、Service Account等 |
| 評価単位 | CredentialとSystem間Authentication | Privilege Activationから失効までのLifecycle |

短命で署名済みのTokenをAgentへ無条件に再発行できる構成は、C5.1.2には適合し得るが、
C5.2.6にはFailし得る。逆に、Human AdministratorがPIMで一時的にModel Registry Adminに
なる構成はC5.2.6の対象だが、AI AgentのFederated AuthenticationでなければC5.1.2は
対象外になり得る。

## 3. 最初に一つの具体Scenarioを見る

Training Pipelineが、学習済みModelをModel Registryへ登録し、Productionへ昇格させる。

```text
Protected source repository
  -> Training Pipeline
  -> Model Artifact
  -> Model Registry
  -> Production deployment
```

### Failure-proneな構成

Pipeline Service Accountは恒久的なModel Registry Admin Roleを持つ。Jobが使うAccess Tokenは
15分で失効するが、Service Accountはいつでも追加確認なしで新しいTokenを発行できる。

```text
Permanent Admin Role
  -> 15-minute Access Token
  -> Expiry
  -> new 15-minute Access Token
  -> Expiry
  -> new 15-minute Access Token
  -> ...
```

表面上、一つのTokenは短命である。しかし、Service Accountを侵害したAttackerはTokenを
繰り返し取得できる。実効的なPrivileged Accessに終了時刻がなく、Standing Privilegeが
短命Tokenで包まれているだけである。

### 推奨される構成

```text
通常時:
  Pipeline identityにModel Registry Write権限なし

承認されたJob開始:
  Independent policy evaluates:
    - Pipeline identity
    - Job ID
    - Target model
    - Artifact digest
    - Environment
  -> そのJob専用のWriter Credentialを30分だけ発行
  -> Job終了または30分で失効
  -> Job外からの発行とRefreshを拒否
```

この構成では、特権はToken発行時だけでなく、その前提となるJob authorizationへBinding
される。Jobがなければ、同じService AccountでもPrivileged Credentialを取得できない。

## 4. 用語

### Privileged Access

Security上重要なState、Artifact、Configurationを取得または変更できるAccess。AISVS原文は
組織固有のRole名を定義していないため、Repositoryでは、少なくとも次のOperationを
候補としてInventoryする。

- Model WeightのDownload、Export、Replace、Delete。
- Model RegistryへのPublish、Promotion、Rollback。
- Training Data、Job、Pipeline、Evaluation gateの変更。
- Production Model、System Prompt、Tool Permission、Guardrail、Routingの変更。
- Production AI Endpoint、Secret reference、Runtime Configurationの変更。

Role名に`admin`が含まれるかではなく、実際に達成できるSecurity impactで判定する。

### Model Weight

Modelの学習結果を保持するParameter群。漏えいは知的財産やModel capabilityの流出に、
改ざんはBackdoorやModel behaviorの変更につながり得る。

### Training Pipeline

Training Dataの取得、前処理、学習、Evaluation、Artifact生成、署名、Registry登録等を行う
一連のSystem。単一のScript名ではなく、Source、Runner、Artifact Store、Registry、
DeploymentへのTrust chainとして考える。

### Production AI Configuration

ProductionでModelやAI ApplicationのBehavior、権限、接続先を変える設定。例えば使用Model、
System Prompt、Tool Permission、Routing、Guardrail、Endpoint、Feature flagが含まれ得る。

### Just-in-time（JIT）

通常時はPrivilegeをActiveにせず、許可された作業が始まる時点で、一時的に有効化する方式。
AccountやIdentityそのものを毎回作るという意味ではない。

### Maximum Session Duration

一度ActivationしたPrivilegeを連続して利用できる最大時間。HumanのWeb Sessionだけでなく、
Non-human IdentityではTemporary Role、Access Token、Workload Credential、Delegated Grant、
Pipeline executionの有効期間として現れる。

### Automatic Expiry

人が作業後にRoleを外すのではなく、Identity Provider、PAM、STS、Credential Broker、または
Resource側が、定義した時間を超えたAccessを自動的に拒否すること。

### Standing Privilege

作業が存在しない通常時にも、即座に特権Operationを実行できる権限。また、短命Tokenしか
持たなくても、新しいPrivileged Tokenを無条件に発行できるCapabilityが恒久的なら、
Repositoryでは実効的なStanding Privilegeとして評価する。

### Zero Standing Privilege（ZSP）

通常時にActiveなPrivileged Accessを残さず、必要な作業ごとにPolicy評価を行って一時的に
付与する考え方。AISVS C5.2.6では推奨されているが、完全なZSPという製品LabelをRequirementの
必須条件へ読み替えない。

### EligibleとActive

`eligible`は条件を満たせばPrivilegeをActivationできる状態、`active`は今すぐPrivilegeを
行使できる状態を表す。Eligible assignmentであっても、無条件かつ無期限にActivationできる
なら、JITのAssuranceは弱い。Activation条件と最大時間を含めて評価する。

## 5. Threat ModelとTrust Boundary

### Attacker capability

このRequirementは、次のいずれかが侵害または悪用され得ると想定する。

- Human AdministratorのSession、端末、Credential。
- Training PipelineやCI/CD Runner。
- AgentまたはAutomation Service Account。
- Token、Refresh Token、Client Credential、Cloud Role。
- Model Registry、Artifact Store、Production ConfigurationへのAccess path。

Attackerの目的は、Standing Privilegeまたは過剰に長いSessionを利用し、次を達成することで
ある。

- Model Weightの窃取。
- Training Data、Pipeline、Model Artifactの改ざん。
- 悪意あるModelやBackdoorのProduction昇格。
- Guardrail、Tool Permission、Routing等の無効化。
- Production AI Configurationの永続的な変更。

C5.2.6はCredential theftやPipeline compromiseそのものを防止しない。侵害されたPrincipalが
特権を使える時間と条件を制限し、Blast radiusを下げる。

### 主なTrust Boundary

1. Human／Workload IdentityとJIT Activation Service。
2. Activation PolicyとCredential発行を行うIdP、PAM、STS、Credential Broker。
3. 発行されたCredentialとModel Registry、Pipeline、Production Configuration API。
4. Training JobのControl planeと、特権を受け入れるData plane。
5. CredentialのRefresh／Reissue経路と、新しいAuthorizationを要求する境界。
6. Normal pathとBreak-glass、Recovery、Manual operation等の例外経路。

## 6. Security Invariant

平易な言葉で表す。

> 許可された作業の開始前と、定義した最大時間の終了後には、過去のActivationやCredentialを
> 使って重要なAI Resourceへ特権Operationを実行できない。

具体的には、次が成立する必要がある。

- Privilegeは許可されたPrincipal、Task、Resource、EnvironmentへBindingされる。
- Privilegeの最大時間は明示される。
- Expiry後は対象ResourceまたはTrusted PEPがOperationを拒否する。
- Refresh、Reissue、Assume-role、Background Jobによって最大時間を無期限に延長できない。
- JIT pathを迂回するStatic CredentialやPermanent Admin Roleがない、または明示した例外として
  別途Risk評価される。

ResearchはTask completion時の自動Revocationも推奨する。これは最大時間までの不要なAccessを
減らす有用な追加保証である。ただし、AISVS原文の明示表現はDefined maximum durationと
Automatic expiryであり、Task終了即時Revocationを暗黙の絶対条件へ追加しない。

## 7. Lifecycle全体で評価する

JITの実装方法は多様だが、Architecture Reviewは次の6点に限定できる。

1. **対象Resource:** どのModel Weight、Pipeline、Production Configurationを守るか。
2. **Privileged Operation:** Download、Deploy、Publish、Delete、設定変更等の何を特権とするか。
3. **Activation:** どの作業EventとPolicyによってPrivilegeが有効になるか。
4. **Credential発行:** Principal、Resource、Action、Environment、時間が限定されるか。
5. **RenewalとExpiry:** RefreshやReissueによって最大時間を迂回できないか。
6. **Resource側の強制:** 期限後に対象Resourceが実際に拒否するか。

```text
Resource
  -> Privileged operation
  -> Activation condition
  -> Temporary credential
  -> Renewal ceiling
  -> Automatic expiry
  -> Resource-side denial
```

「実装は無限にあり得る」と考える代わりに、特権Access pathごとにこのLifecycleを追う。
Technologyが異なっても、検証するSecurity Outcomeは有限である。

## 8. 決定論的なEnforcement Point

Enforcementは単一製品ではなく、Lifecycleの複数地点で行われる。

```text
Principal／Workload
  -> Activation policy
  -> IdP／PAM／STS／Credential Broker
  -> Time-bound Role／Credential
  -> Trusted PEP
  -> Model Registry／Pipeline／Production Configuration API
```

### Activation側

- PrincipalまたはWorkload Identityを検証する。
- Task、Job、Approval、Artifact、Target Environment等のActivation条件を評価する。
- 許可されていない通常時のActivationを拒否する。
- 最大DurationをPolicyとして強制する。

### Credential発行側

- Principal、Audience、Resource、Action、Environmentを限定する。
- Expiryを最大Session時間より長くしない。
- RefreshまたはReissueでActivation windowを越えさせない。
- Static secretや別のCredentialによるBypassを残さない。

### Resource／PEP側

- Expiry、Audience、Scope、Principal、Resource bindingを検証する。
- Expiry後の既存Connection、Queued Job、Retryも新しい特権Operationとして再評価する。
- JIT System障害時にPermanent Admin Credentialへ自動Fallbackしない。

## 9. 短命TokenとJITを混同しない

最初の講義では、次の抽象表現を用いた。

> Token TTLが短いことと、特権がJITであることは同じではない。

学習者には分かりにくかったため、具体的な表現へ置き換える。

> 15分Tokenを無条件に何度でも再発行できるなら、管理権限は15分ではなく常時有効である。

さらに一般化した設計原則は次である。

> Credentialの有効期限だけでなく、特権を取得、更新、終了できるLifecycle全体を評価する。

UI Sessionを60分で終了させても、そこで取得したCLI TokenをResourceが24時間受け入れるなら、
実効的な最大時間は24時間である。最大Session時間は設定画面の値ではなく、対象Resourceが
特権Operationを拒否し始める時刻で測る。

## 10. Pass／FailとScope Calibration

| Scenario | C5.2.6 | 理由 |
|---|---|---|
| Admin Sessionは60分だが、CLI Tokenを24時間利用できる | Fail | 定義した最大時間と実効的なAccess時間が一致しない |
| 15分TokenをPermanent Admin Service Accountが無条件に再発行できる | Fail | Tokenは短命でも、Privilege取得Capabilityに終了時刻がない |
| 承認Job中だけ、JobとArtifactへBindingした30分Credentialを発行し、Job外の発行とRefreshを拒否する | Passし得る | Privilege ActivationとExpiryがTaskへ限定される |
| 最大時間を24時間と定義し、24時間後に自動失効する | Context依存 | 数値だけでは判定できない。TaskとRiskに対するJITの妥当性が必要 |
| 作業後に担当者が手動でRoleを外す | Fail | Automatic expiryがなく、忘却や妨害でPrivilegeが残る |
| JITは成立するがCredentialが別Environmentでも使える | C5.2.6単独ではPassし得る | Audience／Environment bindingは重要な隣接Propertyであり、SystemはFailし得る |
| 最大時間で自動失効するが、Task終了後も最大時間までは有効 | Passし得る | 原文の明示条件を満たし得る。Task終了即時Revocationはより強い追加保証 |
| Break-glass AccountだけPermanent Adminである | 自動的にPass／Failとしない | 原文との緊張を明記し、Scope、保護、監視、期限、例外理由を評価する |

AISVSは15分、60分、24時間等の一律な最大値を定めていない。したがって、時間の評価は
二段階に分ける。

1. 定義した最大時間が、すべてのCredential、Refresh、Role、Resourceで実際に強制されるか。
2. その最大時間が、Task duration、Resource sensitivity、攻撃可能時間、運用要件に対して
   説明できるか。

一段目にFailした場合、時間の長短を議論する前にC5.2.6はFailする。二段目では、単に
「業界標準だから」ではなく、対象OperationとImpactに基づく根拠を求める。

## 11. VerificationとNegative Test

### Architecture review

1. Model Weight、Training Pipeline、Production AI ConfigurationをInventoryする。
2. 各ResourceのPrivileged Operationを列挙する。
3. Human、Agent、Service Account、CI/CD、Emergency AccountのAccess pathを描く。
4. Activation、Credential issuance、Refresh、Reissue、Expiry、Revocationを追跡する。
5. Resourceが実際に拒否する時刻と条件を確認する。
6. Normal pathだけでなくBreak-glass、Rollback、Recovery、Maintenance pathを確認する。

### Positive verification

- 許可されたTask開始後だけ、期待したPrincipalへ限定Credentialが発行される。
- Credentialで許可されたResourceとOperationだけを実行できる。
- Long-running Jobが必要な場合も、承認した最大時間とRenewal Policyに従う。
- ExpiryまたはTask終了後、新たなActivationによってのみ特権を再取得できる。

### Negative verification

- TaskやJobが存在しない状態でPrivileged Credentialを要求する。
- Job ID、Artifact digest、Target Model、Environmentを改ざんする。
- Credentialを別Model、別Pipeline、別Environmentへ転用する。
- 最大時間後に同じCredentialでOperationを行う。
- Refresh、Token exchange、Assume-role、Reissueによって最大時間を延長する。
- Credentialを別Workloadへコピーして使用する。
- Expiry前に開始したConnection、Job、RetryからExpiry後に新しい特権Operationを行う。
- JIT ServiceをUnavailableにし、Static Admin CredentialへのFallbackを試す。
- Break-glassまたはRecovery pathから無期限のPrivileged Accessを取得する。

最も重要なNegative Testは次である。

> 定義した最大時間の後に、Resourceが特権Operationを拒否することを、実際のAccess pathで
> 確認する。

## 12. Refresh TokenとService Account

Refresh Tokenは、Access Tokenの失効後に新しいAccess Tokenを取得するためのCredentialで
ある。OAuthではConfidential ClientがToken Endpointを利用するときClient Authenticationを
行うが、すべてのClientがClient Secretを安全に保持できるわけではない。

OAuth Security Best Current Practiceは、Refresh TokenのScopeとResource ServerへのBinding、
Public Clientに対するSender ConstraintまたはRefresh Token Rotation等を求める。これらは
Refresh Token theftやReplayのRiskを下げる。

しかし、強いClient Authenticationや安全な保管は、JIT Authorizationを自動的には作らない。

```text
Client Authentication:
  Tokenを要求しているClientは誰か

JIT Authorization:
  そのClientへ、今このTaskのためにPrivilegeを与えてよいか
```

今回のFailure scenarioは厳密にはRefresh Token Flowとは限らない。Permanent Client
CredentialまたはCloud Roleを使って新しいAccess Tokenを繰り返し取得する場合も同じFailureに
なる。OAuth Client Credentials Flowでは、Refresh Tokenを原則として発行しないことが
推奨されているが、Permanent Client CredentialがPrivileged Tokenの無条件な再発行を許せば、
C5.2.6上の問題は残る。

## 13. AISVS Level 3について

AISVSは、C5.2.6をLevel 3とした個別理由をNormative chapterまたはC5.2 Researchで説明して
いない。次はRepository上の推論である。

- HumanだけでなくCI/CD、Agent、Service AccountのPrivilege Lifecycleを扱う。
- Token TTLだけでなくActivation、Refresh、Delegation、Background Jobまで追跡する。
- Model Registry、Pipeline、Cloud IAM等の複数Systemをまたいで強制する。
- ExpiryがLong-running TrainingやProduction Operationを壊さない設計が必要になる。
- Break-glass、Rollback、Disaster recoveryとJITを両立させる必要がある。

このSystem横断的で運用依存の性質は、AISVSが示すLevel 3の一般的な「実装が難しい、適用が
状況依存、または高度なDefense in Depth」という説明と整合する。

Level 3であることは、High-impactなAI ResourceでStanding Privilegeを放置してよいという
意味ではない。Riskに応じてArchitectureの初期段階から検討する。

## 14. このRequirementだけでは保証しないこと

C5.2.6にPassしても、次は別途評価する。

- PrincipalまたはWorkload Identityが正しいこと。
- Activation PolicyとApprovalが正しいこと。
- Tokenの署名、Audience、Scope、Sender Constraintが安全であること。
- Model Artifact、Pipeline Source、Dependency、Container ImageのIntegrity。
- Credential Broker、PDP、PAM、STS自体のIsolationとSecurity。
- Resource側のAuthorizationとComplete Mediation。
- Model WeightやTraining DataのConfidentiality、Encryption、Provenance。
- Production Configuration変更のReview、Rollback、Auditability。
- Prompt Injection、Agent compromise、Credential theftそのものの防止。

> Privilegeが短時間であることと、そのPrivilegeを与える判断が正しいことは別である。

## 15. 質疑の再構成

### 問い1: UI Sessionは60分だがCLI Tokenは24時間使える

**Scenario:** EngineerはStep-up Authentication後、Model Registry Adminを60分間Activateする。
管理画面のSessionは60分で終了するが、その間に取得したCLI Tokenは24時間有効であり、
8時間後にもModel登録を実行できる。

**学習者の判断:** Fail。60分という期限に現実的な意味はなく、実効時間は24時間である。
24時間という長さの妥当性もPass／Fail評価に関わる。

**整理:** 正しい。まず定義した60分と実効的な24時間が不一致であるため明確にFailする。
仮に24時間を最大時間として定義しても、それだけで自動的にPassにはならない。TaskとRiskに
対してJITと説明できる長さかを別途評価する。

### 問い2: Permanent Adminが15分Tokenを繰り返し発行する

**Scenario:** Training Pipeline Service AccountはPermanent Model Registry Admin Roleを持つ。
各Access Tokenは15分で失効するが、追加のApprovalやJob単位のPolicy評価なしに、いつでも
新しいTokenを発行できる。

**学習者の最初の判断:** Pass。Refresh Tokenの利用例に似ており、Refresh Tokenは限定環境や
Client Secret等でAccess Tokenより厳しく保護されることが多い。Systemの重要性によっては
追加評価が必要だが、対象外にできると考えた。

**訂正:** C5.2.6ではFailする。15分Tokenの外側にあるAdmin RoleまたはToken発行Capabilityが
恒久的だからである。Client Secretや限定環境はCredential theftの可能性を下げるが、
PrivilegeをTask単位かつ時限的にActivationするものではない。また、Refresh Tokenが必ず
Client Secretを必要とするわけではなく、今回の構成はClient CredentialsやCloud Roleからの
再発行である可能性もある。

この訂正から、短命CredentialとJIT Privilegeの違いが明確になった。

### 問い3: JobへBindingした30分Credential

**Scenario:** Pipelineは通常Model RegistryへのWrite権限を持たない。保護されたMain Branchの
署名済みJobが始まったときだけ、独立したCredential BrokerがPipeline Identity、Job ID、
Target Model、Artifact digest、Environmentを検証し、30分Credentialを発行する。Refreshは
できず、Job終了または30分で失効し、Job外からの発行は拒否される。

**学習者の判断:** Pass。

**整理:** 正しい。短命Tokenだけでなく、Activation条件、Task binding、Scope、Renewal ceiling、
Automatic expiry、Resource-side enforcementが一つのLifecycleとして成立している。

### 学習後の所感

学習者は、C5.2.6が対象Resourceを変えたC5.1.2と重なるように感じた。比較した結果、同じ
技術を利用しても、C5.1.2はAgent Credentialの性質、C5.2.6は重要AI Resourceに対する
Privilege Lifecycleを評価するという違いが明確になった。

また、「Token TTLが短いことと、特権がJITであることは同じではない」という抽象表現より、
「Credential単体ではなくLifecycle全体を評価する」という説明で理解が進んだ。局所的な
短命化では足りず、ActivationからResource-side denialまで広く追うため、解釈と実装が
無限に見えるという所感があった。

これに対し、実装方式を網羅するのではなく、対象Resource、Privileged Operation、Activation、
Credential発行、Renewal／Expiry、Resource-side enforcementの6点へ分解すれば、レビューを
有限かつ再利用可能にできると整理した。

## 16. このセッションから得られた洞察

1. **短命TokenはJITの一部であり、JIT全体ではない。** 無条件に再発行できる短命Tokenは
   Standing Privilegeを隠すことがある。
2. **最大時間はResource-side denialで測る。** UIやIdPの表示値ではなく、特権Operationが
   実際に拒否される時刻がSecurity上の終了時刻である。
3. **CredentialではなくPrivilege Lifecycleを見る。** Activation、Issuance、Refresh、
   Reissue、Expiry、Resource enforcementを一つのAccess pathとして評価する。
4. **AuthenticationとJIT Authorizationを分ける。** Clientを強く認証することと、そのClientへ
   今Privilegeを付与してよいことは別の判断である。
5. **C5.1.2とC5.2.6は技術が重なっても保証軸が違う。** Credential propertyとPrivilege
   lifecycleを別々に検証する。
6. **広い問題は6点へ分解できる。** 実装方法を網羅せず、特権Access pathのLifecycleを
   決められた順序で追う。
7. **JITへのPassはPrivilege decisionの正しさを保証しない。** 誤ったPolicyで短時間のAdmin
   Accessを発行してもSystemは安全ではない。

## 17. 設計レビュー項目

- Model Weight、Training Pipeline、Production AI ConfigurationをInventoryしたか。
- 各ResourceについてSecurity impactのあるPrivileged Operationを列挙したか。
- Human、Agent、Service Account、CI/CD、Emergency Accountを含むPrincipalを列挙したか。
- 通常時にActiveなPrivileged Accessが残っていないか。
- Eligible PrincipalのActivation条件がTask、Job、Approval等へBindingされているか。
- Maximum Session Durationが明示され、RiskとTask durationから説明できるか。
- 発行CredentialのExpiryが最大時間を超えていないか。
- Refresh、Reissue、Token exchange、Assume-roleで最大時間を迂回できないか。
- Long-running JobとBackground ProcessがExpiry後も新しい特権Operationを続けないか。
- Model Registry、Pipeline、Configuration APIが期限後のAccessを実際に拒否するか。
- Credentialを別Resource、別Model、別Environment、別Workloadへ転用できないか。
- Task終了時の早期Revocationを追加保証として検討したか。
- Break-glass、Maintenance、Rollback、Recovery pathを例外として放置していないか。
- JIT System障害時にPermanent CredentialへFail openしないか。
- C5.1.2のToken propertyとC5.2.6のPrivilege Lifecycleを混同していないか。
- JITにPassしたことを、Identity、Policy、Artifact、Pipeline全体の安全と表現していないか。

## 18. References

### Normative／Research

- [OWASP AISVS v1.0 C5 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [OWASP AISVS v1.0 C5.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-02-AI-Resource-Authorization-Classification.md)
- [OWASP AISVS v1.0 Verification Levels](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x03-Using-AISVS.md)

### Supporting protocol references

- [RFC 6749: The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749)
- [RFC 9700: Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700)

Supporting referencesはCredential、Refresh、Client Authenticationの理解を補うものである。
OAuthの使用をC5.2.6の唯一の実装方法またはPass条件とはしない。
