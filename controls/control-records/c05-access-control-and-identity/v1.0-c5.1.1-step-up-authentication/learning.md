---
title: "AISVS v1.0-C5.1.1 Step-up Authentication Learning Note"
document_kind: "requirement-learning-note"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
requirement_id: "C5.1.1"
verification_level: 3
research_last_researched: "2026-07-14"
last_updated: "2026-09-04"
---

# C5.1.1 Step-up Authentication 学習ノート

[Control本文：解釈・検証・証拠・限界](README.md)


## この文書について

この文書は、AISVS `v1.0-C5.1.1`を題材に行った学習セッションを、後から単独で
参照できる講義として再構成したものである。

これはControl本文、製品の適合判定、またはAISVS原文の代替ではない。次の情報を
意識して分離する。

- **Normative:** AISVS v1.0が実際に要求していること。
- **Research:** AISVS Researchや一次仕様が与える脅威・検証上の補足。
- **Repository interpretation:** 現場のArchitecture Reviewへ適用するための解釈。
- **Derived insight:** 学習中の問いから得られた、隣接するSecurity上の洞察。

## 1. Normative Requirement

- Versioned ID: `v1.0-C5.1.1`
- AISVS Verification Level: `3`

> Verify that high-risk AI operations (model deployment, weight export, training
> data access, production configuration changes) require step-up authentication.

意味を崩さない日本語訳:

> ModelのDeploy、WeightsのExport、Training DataへのAccess、本番設定の変更といった
> 高RiskなAI Operationに、Step-up Authenticationが要求されることを検証する。

AISVSが明示している必須要素は次の二つである。

1. 対象がHigh-risk AI Operationであること。
2. そのOperationにStep-up Authenticationが要求されること。

Requirement本文は、特定のAuthenticator、Protocol、認証強度、再認証の有効時間、
Transaction Binding、またはHuman Approval方式までは指定していない。

## 2. C5における位置づけ

C5.1はAuthenticationを扱う。C5.1.1が確認するのは、現在のCallerが高Riskな操作に
必要な強度とFreshnessで認証されているかである。

これは次の問いとは異なる。

- そのCallerに操作を許可すべきかというAuthorization。
- Privilegeが必要な時間だけ付与されたかというJIT Access。
- 操作内容をHumanが承認したかというApproval。
- 承認後に操作内容が変わっていないかというTransaction Integrity。
- 実行した変更が安全かというChange Validation。

C5.1.1にPassしても、これらが欠けていればSystem全体は安全ではない。

## 3. Security Objective

このRequirementが重要になるThreat Modelは、攻撃者が未認証である場合だけでは
ない。むしろ中心となるのは、攻撃者がすでに通常のBase Sessionを取得している場合
である。

攻撃者は、たとえば次のものを持っている可能性がある。

- 盗んだSession Cookie。
- 長期間有効なAccess TokenまたはRefresh Token。
- 放置された管理者Session。
- 侵害した開発者端末上のBrowser Session。
- 正常に認証済みだが、高Risk Operationには古い、または弱い認証状態。

通常のSessionをそのままModel WeightsのExportやProduction Configurationの変更へ
使える場合、Session Hijackingが不可逆または広範囲なAI Asset侵害へ直結する。

C5.1.1のSecurity Objectiveは、Base Sessionの侵害が自動的に高Risk AI Operationの
実行権へ昇格しないよう、操作直前に独立した認証境界を置くことである。

## 4. 講義用Scenario

開発者Aliceは、午前9時に組織のSSOへログインした。その後、攻撃者がAliceのBase
Sessionを奪い、午後3時にModel RegistryからProduction ModelのWeightsをExport
しようとする。

```text
AliceのBase Sessionを窃取
          |
          v
通常の管理画面・APIへAccess
          |
          v
Model Weights Export API  <--- High-risk Operationの境界
          |
          v
回収できないModel Assetの窃取
```

Export APIが「認証済みSessionだから許可する」と判断すれば、Base Sessionの窃取が
そのままModel窃取になる。

望ましい境界では、Export APIが現在の認証では強度またはFreshnessが不足すると判断
し、Base Sessionとは別の新しいAuthentication Eventを要求する。

## 5. 用語

### Base Session

通常のLogin後に継続して利用する認証済みSession。このRequirementでは、Base
Sessionそのものが盗まれた、古い、または高Risk Operationには弱すぎる場合を考える。

### Step-up Authentication

すでに認証済みのCallerへ、RequestのRiskに応じて、より強いAuthenticationまたは
新しいReauthenticationを要求すること。

Step-upは単にLogin画面をもう一度表示することではない。Resource側が要求する認証
強度とFreshnessを満たし、その結果をResource側が検証できなければならない。

### Authentication Freshness

End Userが最後に実際のAuthenticationを行ってから、どれだけ時間が経過したか。

OpenID Connectでは、次のClaimを区別する。

- `auth_time`: End Userが実際にAuthenticationした時刻。
- `iat`: Tokenが発行された時刻。

Refresh Tokenから新しいTokenを発行すると`iat`は新しくなるが、利用者が再認証して
いなければ`auth_time`は元の時刻のままである。新しい`iat`をFresh Authenticationの
証拠にすると、古い認証状態をToken Refreshで洗浄できてしまう。

### Authentication Context Class Reference (`acr`)

どの種類または強度のAuthentication Contextを満たしたかを表すClaim。値の意味は
導入組織やTrust Frameworkが定義するため、単に`acr`が存在するだけでは不十分である。

### Maximum Authentication Age (`max_age`)

最後のActive Authenticationから許容する最大経過時間。これを超えた場合、IdPまたは
OpenID Providerは利用者を再認証する。

### Resource Server

保護対象のAPIまたはService。ScenarioではModel Weights Export APIが該当する。
高Risk Operationの実行直前に、認証強度とFreshnessを最終確認するEnforcement Pointに
なる。

### Phishing-resistant Authentication

利用者の注意力だけに依存せず、Authenticatorの出力を正規のVerifierまたは通信
Channelへ暗号的にBindingし、偽Siteで取得した認証情報を正規Siteへ転用できないように
するAuthentication。

## 6. Threat ModelとAbuse Path

### Base Sessionの窃取

```text
Session CookieまたはTokenを窃取
  -> 通常の認証状態をReplay
  -> High-risk AI Operationへ到達
  -> ReauthenticationなしでModel窃取・Training改ざん・本番設定変更
```

Step-upは、最初のSessionが侵害されても、高Risk Operationまで自動的に侵害されない
ようにするDefense in Depthである。

### Authentication-freshness laundering

```text
古いAuthentication Event
  -> Refresh Tokenを使用
  -> 新しいiatのTokenを取得
  -> ResourceがiatをAuthentication時刻と誤認
  -> ReauthenticationなしでHigh-risk Operationを許可
```

Freshnessは`auth_time`または同等の信頼できるAuthentication Eventから判断する。

### UI-only Step-up bypass

```text
Web UIはStep-upを要求
  -> 攻撃者がAPI、CLI、Agent、CI/CD経路を直接使用
  -> Backendは通常Tokenを受理
  -> High-risk Operationを実行
```

再認証画面の存在ではなく、実際のResource Serverでの強制が必要である。

### 弱いAuthenticatorの繰り返し

Base SessionをPasswordだけで取得でき、そのPasswordもPhishingで取得されている場合、
同じPasswordをもう一度要求しても攻撃者を排除できない。認証強度は少なくともBase
Session取得時と同等とし、操作Riskが高い場合はPhishing-resistantな方式へ引き上げる。

## 7. Security InvariantとEnforcement

### Security Invariant

> Base Sessionを所持するだけではHigh-risk AI Operationを実行できない。Resourceが
> 要求する強度とFreshnessを満たす、新しいAuthentication Eventがなければ、Resource
> Serverは操作を拒否する。

### Enforcement flow

```text
Client / Agent
    |
    | Base TokenでHigh-risk Operationを要求
    v
Resource Server / PEP
    |
    | 認証強度またはFreshness不足として拒否
    v
Authorization Server / IdP
    |
    | Fresh Authenticationを実施
    v
短命なAuthentication EvidenceまたはAccess Token
    |
    | auth_time・acr・issuer・audience・expiry等を検証
    v
Resource Server / PEP
    |
    v
許可されたHigh-risk Operationだけを実行
```

Resource Serverが、少なくとも次を判断できる必要がある。

- どのOperationをHigh-riskとして扱うか。
- 現在のTokenが要求するAuthentication Contextを満たすか。
- 実際のAuthentication Eventが十分に新しいか。
- API、CLI、Agent、CI/CD、Fallbackなど別経路で迂回できないか。
- 不足時に許可ではなくReauthenticationまたはDenyへ進むか。

ModelまたはAgentの「この操作は安全」という判断は、決定論的なAuthentication
Enforcement Pointの代替にならない。

## 8. Pass／FailとScope Calibration

| Scenario | C5.1.1評価 | 理由または別の問題 |
|---|---|---|
| Base TokenでWeights Export APIを呼ぶと拒否され、YubiKeyによるFresh Authentication後だけ成功する | Pass候補 | Backendが強度とFreshnessを検証し、全経路で強制されることが条件 |
| Web UIだけがPassword再入力を要求し、APIはBase Tokenを受理する | Fail | 実際のOperationにStep-upが要求されていない |
| 午前9時の認証から午後3時にRefreshされたTokenの`iat`だけを見てFreshと判断する | Fail | Token発行とUser Authenticationを混同している |
| Base Sessionと同じPasswordを再入力させ、Backendも検証する | 原文上はPass候補 | Step-upではあるが、SessionとPasswordが同時に侵害されるThreatには弱い。High-assurance設計として十分とは限らない |
| YubiKeyでFresh Authenticationした後、攻撃者がExport先を変更できる | C5.1.1はPassし得る | Authenticationは成立している。Transaction Integrity、Operation Authorization、Approvalに別の重大なGapがある |
| Human経路にはStep-upがあるが、常設Service API Keyで同じExportを実行できる | Fail | High-risk OperationにStep-upを要求する境界を迂回できる |
| DeviceがMDM上CompliantであることだけをFresh Authenticationとして扱う | Fail | Device PostureはContextであり、現在のUserによる新しいAuthentication Eventではない |
| High-risk Operationの定義が文書化されず、未分類のAdmin APIが通常Sessionで実行できる | Fail | 対象OperationのInventoryと完全なEnforcementがない |

Configuration画面にMFA Policyが存在するだけではEvidenceにならない。少なくとも次を
確認する。

- Base Tokenによる直接API Requestの拒否結果。
- Step-up前後の`auth_time`と`acr`または同等のEvidence。
- 最大許容時間を超えた後の再拒否。
- Refresh TokenがFreshnessを更新しないこと。
- UI以外の全High-risk Operation経路。
- Authentication Service障害時にFail closedすること。

## 9. CSRFとの関係

C5.1.1とCSRF Preventionには、次の共通した上位原則がある。

> 既存Sessionが付いたRequestであるという事実だけでは、重要なOperationを実行させない。

ただし、脅威とControlは異なる。

| 観点 | CSRF Prevention | C5.1.1 Step-up Authentication |
|---|---|---|
| 主なThreat | BrowserがSession Cookieを自動送信し、別Originから不要なRequestを実行させられる | Base Sessionが盗まれた、古い、またはOperationに対して認証強度が不足している |
| 確認対象 | Requestが正規Originや正規Application flowから送られたか | Userが要求強度で最近Authenticationしたか |
| 代表的なControl | CSRF Token、Origin検証、Fetch Metadata、SameSite | Reauthentication、MFA、`auth_time`、`acr`、`max_age` |
| 主なOutcome | Cross-site Requestの偽造を防ぐ | Session侵害後のHigh-risk Operationを分離する |

Password再入力や別のUser Interactionは、高Sensitiveな操作に対するDefense in Depthに
なる。しかしStep-upはCSRF Token、Origin検証、Fetch Metadata、SameSiteなどの一般的な
CSRF Defenseを置き換えない。逆にCSRF Tokenも、現在のUserをFreshにAuthenticationした
証拠にはならない。

## 10. Phishing-resistant Authentication

### 成立に必要な性質

Phishing-resistant Authenticationは、少なくとも次の性質を持つ。

- 正規のVerifier名または通信ChannelへAuthenticator出力をBindingする。
- ChallengeまたはNonceにより、過去の出力のReplayを防ぐ。
- 秘密鍵そのものをVerifierへ送らない。
- High-assurance用途では、秘密鍵をNon-exportableかつHardware-protectedにする。
- 必要な場合、User PresenceまたはPIN・BiometricによるUser Verificationを要求する。

### 具体例

| 方式 | Phishing Resistanceの根拠 | 注意点 |
|---|---|---|
| YubiKeyのFIDO2／WebAuthn Mode | 正規DomainのChallengeへDevice内の秘密鍵で署名する | YubiKeyのOTP Modeは同じ性質を持たない。TouchだけではTransaction内容の承認までは証明しない |
| Device-bound Passkey | WebAuthnのVerifier名BindingとDevice内の秘密鍵を利用する | すべてのPasskeyがHardware-boundまたはNon-exportableとは限らない。Syncable PasskeyはNIST AAL3と同一ではない |
| Windows Hello等のPlatform Authenticator | TPM等のKeyとLocal PIN／BiometricをWebAuthnで利用できる | 単なるDevice Login確認ではなく、正規ServiceへのWebAuthn Authenticationとして使う |
| PIV／CAC Smart CardとClient-authenticated TLS | Smart Card内のKeyによる署名をTLS ChannelへBindingする | PKI、Certificate lifecycle、Reader、端末管理が必要 |

次の方式は、単独では通常Phishing-resistantとみなさない。

- Password。
- SMSまたはEmail OTP。
- TOTP Authenticator App。
- 秘密の質問。
- 単純なPush Approval。
- Known Device CookieやDevice Fingerprintだけの確認。

手入力できる認証出力は、偽Siteが正規ServiceへRelayできる。Device Posture、Location、
IP ReputationなどはStep-upを要求するRisk Signalにはなるが、それ自体がFresh User
Authenticationになるわけではない。

## 11. HumanとAgentのAuthentication

HumanとAgentでは、Authenticationが証明する対象が異なる。

| Principal | Authenticationで主に証明するもの | Authenticationだけでは証明しないもの |
|---|---|---|
| Human | AccountへBindingされたAuthenticatorを本人が現在Controlしていること | 具体的なOperation内容が安全、正しい、または意図どおりであること |
| Agent／Workload | 登録されたWorkloadが現在対応するKeyをControlしていること | AgentのReasoning、Prompt、Action、Human Intentが正しいこと |

AgentにはYubiKeyを操作するHuman Presenceがない。Machine側の強いAuthenticationには、
次のような構成要素を用いる。

- SPIFFE X.509-SVID等の短命なWorkload Identity。
- mTLSによる秘密鍵のProof of Possession。
- Cloud Workload IdentityによりPod、VM、Job、Service AccountへBindingされたIdentity。
- TPM、HSM、またはTEEに保持されたNon-exportable Key。
- 承認されたRuntime、Image、構成を確認するRemote Attestation。
- Operation時にToken Exchangeで取得する短命・Audience限定・Scope限定Token。
- mTLSまたはDPoPでSender-constrainedされたAccess Token。

DPoPはToken Replayを難しくするProof-of-possession Mechanismであるが、RFC 9449が明示
するように、DPoP単独はClient Authenticationではない。また、Agent Runtime自体が
侵害されていれば、そのRuntimeは正規のKeyを使って署名できる。

AgentがHumanを代理してHigh-risk Operationを行う場合、強い設計は次の要素を分離して
検証する。

```text
HumanのFresh Authentication
  + Agent／Workload Authentication
  + Operationに対する決定論的Authorization
  + 必要に応じたHuman ApprovalとTransaction Binding
```

Agent IdentityはHuman Intentの代替ではない。完全自律Operationを許可する場合は、
どのWorkload、Build、Environment、Action、Resource、Audience、期限を許可するかを
事前PolicyとJIT Credentialで限定する必要がある。この追加設計はC5.1.2、C5.2.6、
Agent Authorization、Approval、およびSupply-chain Assuranceにもまたがる。

## 12. Transaction Bindingは別のSecurity Property

高ImpactなOperationでは、Authentication結果を具体的なTransactionへBindingする
設計が望ましい。

```text
Principal:   Alice
Action:      export
Resource:    model/customer-risk-v4
Destination: approved-artifact-store
Purpose:     release-2026-09
Expiry:      5 minutes
```

これにより、一つのStep-up結果を別Model、別Destination、別Actionへ使い回しにくく
できる。

ただしC5.1.1のNormative Requirementは、Transaction Bindingや具体的なApproval内容
までは要求していない。したがって、YubiKeyでFresh Authenticationした後に攻撃者が
Export先を変更できるSystemは、C5.1.1にはPassし得るが、System全体として重大な
Transaction IntegrityまたはAuthorization Gapを持つ。

良いSecurity Architectureを推奨することと、隣接PropertyをC5.1.1のPass条件へ勝手に
追加することを区別する必要がある。

## 13. AISVS Level 3の意味

AISVSは、C5.1.1をLevel 3にした個別の理由までは説明していない。以下はAISVSのLevel
定義とRequirementの性質からのRepository上の推論である。

AISVS v1.0はLevel 3を、一般に次のようなRequirementとして説明している。

- 実装が比較的難しい。
- 適用がSituationalである。
- Defense in Depthにあたる。
- Niche、Targeted、またはHigh-complexityなAttackへのMitigationである。
- Critical Infrastructure、Life-safety、高Sensitive Data等のHigh-assurance Systemで
  典型的に利用する。

C5.1.1は次の理由でこの特徴に合うと考えられる。

1. Base Authentication後のSession侵害を想定するDefense in Depthである。
2. Model ExportやProduction Pipeline変更等を持たないSystemには適用が限定される。
3. IdP、Authorization Server、Resource Server間で強度とFreshnessを伝達する必要がある。
4. UIだけでなくAPI、CLI、Agent、CI/CD、Admin Endpointを含む全経路を閉じる必要がある。
5. Model WeightsやTraining Pipelineなど、侵害後の回復が困難なAssetを守る。

AISVS Level 3とNIST AAL3は異なる。

- **AISVS Level 3:** AI Systemに対するVerificationの深度と典型的な適用Risk。
- **NIST AAL3:** Human Authenticationに対する非常に高いAssurance Level。

C5.1.1がAISVS Level 3であることは、すべてのStep-upでNIST AAL3を必須にする意味では
ない。逆に、Level 3だから一般のProduction Systemでは後回しにしてよいという意味
でもない。守るAssetとOperation Impactに基づいて採用とAuthentication Policyを決める。

## 14. 対話の再構成

### Q1: RefreshされたTokenはFresh Authenticationか

**問い:** Aliceは午前9時にMFAを完了した。午後3時にRefresh Tokenから新しいAccess
Tokenが発行され、Weights Export APIは`iat=15:00`だけを見て新しいAuthenticationと
判断した。Passか。

**学習者の判断:** Fail。

**整理:** 正しい。`iat`はToken発行時刻であり、Userが実際にAuthenticationした時刻
ではない。`auth_time`または同等のAuthentication Eventを確認する。

### Q2: HumanならYubiKey、Agentなら何を使うか

**問い:** HumanにはYubiKeyのようなPhysical Keyが使える。Agentは何でAuthentication
するのか。

**整理:** AgentではHuman Presenceの代わりに、短命なWorkload Identity、mTLS、
Non-exportable Key、Remote Attestation、Sender-constrained Token等で、正規Workloadが
現在KeyをControlしていることを証明する。ただしAgentの判断やHuman Intentまでは
証明しない。

### Q3: Base Sessionが盗まれているなら何が必要か

**学習者の洞察:** Sessionを奪われているため、多くの対策がBypassされる。Sessionを
取得した際と同等のAuthenticationを設ける必要がある。

**整理:** 核心を捉えている。Base Sessionの所持やToken RefreshをStep-upの証拠にせず、
独立したFresh Authenticationを要求する。認証強度は少なくともBase Session取得時と
同等とし、元のAuthenticationが弱い場合はOperation Riskに応じて強くする。

### Q4: YubiKey後にDestinationを変更できる場合

**問い:** YubiKeyでReauthenticationするが、画面には具体的なExport対象やDestinationが
表示されず、Authentication後に攻撃者がDestinationを変更できる。C5.1.1はFailか。

**学習者の反応:** 判定が分からない。

**整理:** 問いがAuthenticationとTransaction Integrityを混ぜていた。Fresh Step-upが
実際に要求されていればC5.1.1はPassし得る。しかしSystem全体には重大なAuthorization、
Approval、またはTransaction Integrity Gapが残る。ControlのScopeを広げず、別のFinding
として報告する。

### Q5: CSRFと同じ考え方か

**問い:** CSRF対策のように、重要操作の前にPassword入力等を要求する思想と同じか。

**整理:** 「既存Sessionだけを重要操作の十分な証拠にしない」という上位原則は近い。
ただしCSRFはCross-site Requestの偽造、Step-upはAuthentication強度とFreshnessを扱う。
両方必要であり、相互の代替ではない。

### Q6: C5.1.1はなぜLevel 3か

**整理:** AISVSは個別理由を明記していない。Base Session侵害後のDefense in Depth、
AI固有のHigh-value Asset、適用のSituationalさ、全経路への実装複雑性がLevel 3の一般
定義に合うと推論できる。ただしAISVS Level 3はNIST AAL3や実装優先順位と同義ではない。

## 15. このセッションから得られた洞察

1. **C5.1.1は単なるMFA導入要件ではない。** Base SessionのAuthentication Stateを
   High-risk Operationへそのまま流用させないRequirementである。
2. **Token FreshnessとAuthentication Freshnessを区別する。** `iat`が新しくても
   `auth_time`が古ければReauthenticationではない。
3. **Step-upはBase Sessionから独立していなければならない。** 奪われたSession内の
   FlagやCookieを再確認しても境界にならない。
4. **同じAuthenticationの繰り返しは常に十分ではない。** 元の方式が弱ければ、
   Operation Riskに応じてPhishing-resistantな方式へ引き上げる。
5. **Device PostureはAuthenticationではない。** Known Device、MDM Compliance、
   Location等はRisk Signalにはなるが、Fresh User Authenticationを証明しない。
6. **Phishing Resistanceは製品名ではなくProtocol Propertyである。** YubiKeyでも
   FIDO2 ModeとOTP Modeでは保証が異なる。
7. **Enforcement PointはResource側に置く。** UIにReauthentication画面があっても、
   API、CLI、Agent、CI/CD経路で迂回できればFailである。
8. **Agent AuthenticationはHuman Authenticationの代替ではない。** Workload Identity
   は正規Agentを証明しても、Reasoning、Human Intent、操作の安全性を証明しない。
9. **Transaction Bindingは重要だが別のPropertyである。** 良い設計として推奨しても、
   C5.1.1のNormative Pass条件へ暗黙に追加してはならない。
10. **一つのControlへのPassはSystem Securityを意味しない。** C5.1.1へPassしながら、
    Authorization、Approval、Transaction Integrityに重大なGapを持つことがある。
11. **CSRF DefenseとStep-upは隣接するが別物である。** どちらも既存Sessionを無条件に
    信じないが、検証するSecurity Propertyが異なる。
12. **Verification Levelを実装順または認証強度と混同しない。** AISVS Level 3は
    NIST AAL3ではなく、Level 3だから後回しでよいわけでもない。
13. **AISVSをそのまま絶対視しない。** 原文のScopeを守りつつ、実運用上不足する
    Transaction Binding等は独立した追加保証として明示する。

## 16. 後から設計レビューするときの確認事項

- High-risk AI Operationを、実際のAPIとAction単位でInventoryしているか。
- Base Sessionだけで各Operationを直接呼べないか。
- Step-up結果のFreshnessは`iat`ではなく実Authentication Eventから判断しているか。
- 要求するAuthentication強度をOperation Riskごとに定義しているか。
- Password、OTP、PushをPhishing-resistantと誤認していないか。
- UI、API、CLI、Agent、CI/CD、Fallback、Admin経路に同じ境界があるか。
- Resource Serverが認証不足を決定論的に拒否するか。
- IdPまたはAuthentication Service障害時にFail closedするか。
- Agent IdentityとHuman Intentを同一視していないか。
- C5.1.1のPassと、Authorization、Approval、Transaction Integrityの評価を分けたか。
- AISVS Level 3とNIST AAL3を混同していないか。

## References

### Normative and AISVS sources

- [OWASP AISVS v1.0 C5 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [OWASP AISVS v1.0 C5.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-01-Identity-Management-Authentication.md)
- [OWASP AISVS v1.0 verification levels](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x03-Using-AISVS.md)

### Authentication specifications and guidance

- [RFC 9470: OAuth 2.0 Step Up Authentication Challenge Protocol](https://www.rfc-editor.org/info/rfc9470/)
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
- [NIST SP 800-63B: Authentication Assurance Levels](https://pages.nist.gov/800-63-4/sp800-63b/aal/)
- [NIST SP 800-63B: Authenticators and Phishing Resistance](https://pages.nist.gov/800-63-4/sp800-63b/authenticators/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [OWASP Multifactor Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html)

### Workload and Agent authentication context

- [SPIFFE Concepts](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/)
- [SPIFFE X.509-SVID specification](https://spiffe.io/docs/latest/spiffe-specs/x509-svid/)
- [RFC 9449: OAuth 2.0 Demonstrating Proof of Possession](https://www.rfc-editor.org/info/rfc9449/)
