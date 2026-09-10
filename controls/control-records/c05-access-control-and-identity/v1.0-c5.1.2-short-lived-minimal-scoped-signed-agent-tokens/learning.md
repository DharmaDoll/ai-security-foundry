---
title: "AISVS v1.0-C5.1.2 Agent Token Learning Note"
document_kind: "requirement-learning-note"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
requirement_id: "C5.1.2"
verification_level: 3
research_last_researched: "2026-07-14"
last_updated: "2026-09-05"
---

# C5.1.2 Short-lived、Minimal-scoped、Signed Agent Token 学習ノート

[Control本文：解釈・検証・証拠・限界](README.md)


## この文書について

この文書は、AISVS `v1.0-C5.1.2`を題材に行った学習セッションを、後から単独で
参照できる講義として再構成したものである。

これはControl本文、製品の適合判定、またはAISVS原文の代替ではない。次の情報を
意識して分離する。

- **Normative:** AISVS v1.0が実際に要求していること。
- **Research:** AISVS Researchや一次仕様が与える脅威・検証上の補足。
- **Repository interpretation:** 現場のArchitecture Reviewへ適用するための解釈。
- **Derived insight:** 学習中の問いから得られた、隣接するSecurity上の洞察。

## 1. Normative Requirement

- Versioned ID: `v1.0-C5.1.2`
- AISVS Verification Level: `3`

> Verify that AI agents in federated or multi-system deployments authenticate
> using short-lived, minimal-scoped, cryptographically signed tokens.

意味を崩さない日本語訳:

> Federatedまたは複数Systemにまたがる環境のAI Agentが、短命で、必要最小限の
> Scopeに制限され、暗号学的に署名されたTokenを使用して認証することを検証する。

AISVSが明示する必須要素は次の四つである。

1. 対象がFederatedまたはMulti-system DeploymentのAI Agentである。
2. TokenがShort-livedである。
3. TokenがMinimal-scopedである。
4. TokenがCryptographically signedである。

Requirement本文は、具体的なToken形式、最大Lifetime、署名Algorithm、OAuth Grant、
Audience Claim、Sender Constraining、Token Exchange、Human Delegation表現、または
Certificate方式までは指定していない。

## 2. C5における位置づけ

C5.1はHuman、Service、AgentのAuthenticationを扱う。

- C5.1.1はHigh-risk AI Operationの直前にHuman等のAuthenticationをStep-upする。
- C5.1.2はAgentがSystem間で提示するMachine CredentialのLifetime、Authority、
  Authenticityを制約する。

このRequirementはAuthenticationを主題とするが、`minimal-scoped`という表現により
Authorizationとも接している。ただし、次までは保証しない。

- AgentがそのActionを実行すべきかというRuntime Authorization。
- Agentの判断がHuman Intentと一致するか。
- High-impact ActionにHuman Approvalがあるか。
- ModelまたはAgent RuntimeがPrompt Injectionを受けていないか。
- Agent Processが安全にTokenとPrivate Keyを扱うか。

## 3. Security Objective

一言で表すと、C5.1.2の目的は次である。

> AgentのCredentialが盗まれたりAgent自身が侵害されたりしても、そのAuthorityを
> 長時間、別System、または別Actionへ使い回せないようにする。

Short lifetimeは時間的なBlast Radiusを、Minimal scopeはAuthority上のBlast Radiusを
縮小する。Cryptographic signatureはTokenの偽造とClaim改ざんを検出可能にする。

ただし、これらは相互の代替ではない。正しく署名された長期・広範囲Tokenも危険であり、
短命なTokenでも署名やIssuer検証がなければ偽造できる。

## 4. 講義用Scenario

調達Agentが社内MCP Serverを経由して購買APIへ見積情報を取得する。

```text
Human User
    |
    v
Procurement Agent
    |
    | Token A: aud=procurement-mcp, scope=quotation.request
    v
Procurement MCP Server
    |
    | Token B: aud=purchasing-api, scope=quotation.read
    v
Purchasing API
```

危険な設計では、AgentまたはMCP Serverが一つの長期Credentialをすべての接続先へ
提示する。

```text
Lifetime: 90 days
Audience: all-internal-services
Scope: read write approve delete
```

AgentがPrompt Injection、Command Injection、Log漏えい、またはRuntime侵害を受けて
Tokenが盗まれた場合、攻撃者は本来のTaskと無関係なSystemやActionへAuthorityを
転用できる。

望ましい設計では、各Trust Boundaryに対して対象とAuthorityを限定した短命Tokenを
取得し、受信側が独立して検証する。Token Aを下流APIへそのまま転送しない。

## 5. 用語

### Agent IdentityとWorkload Identity

LLMそのものではなく、Agentを実行するService、Process、Pod、VM、Job等へBinding
されたIdentity。Authenticationが証明するのは、登録されたWorkloadが対応するKeyを
現在Controlしていることまでであり、AgentのReasoningやHuman Intentではない。

### Federated Deployment

異なるIdentity Domain、Issuer、組織、Cloud、または管理境界がTrust関係を結び、
Identity AssertionやTokenを受け入れる構成。

### Multi-system Deployment

Agent、Orchestrator、MCP Server、Tool、Downstream API等、複数SystemとTrust Boundaryを
またいでActionを実行する構成。必ずしも異なる組織である必要はない。

### Access Token

ClientがResource Serverへ提示し、許可されたAccessを得るCredential。Tokenを持つだけで
使えるものはBearer Tokenと呼ばれる。

### Short-lived

TaskとRiskに応じた短い有効期間を持ち、自動的に失効すること。単に定期Rotateする
Static Keyではなく、各Tokenに検証可能なExpiryが必要である。

### Scope

Tokenで実行できるActionや対象Resourceの範囲。Claim名が`scope`であることより、
実際に行使できるAuthorityが必要最小限かが重要である。

### Audience (`aud`)

Tokenを受理してよい対象ServiceまたはResource Server。Signatureが正しくても、
自分向けでないAudienceのTokenをResource Serverは拒否する。

### Issuer (`iss`)

Tokenを発行し、Token内のIdentity、Scope、Audience等をAssertionする主体。Verifierは
Signatureだけでなく、想定するIssuerとKeyの組み合わせを検証する。

### Cryptographic Signature

IssuerがPrivate KeyでTokenへ署名し、Verifierが対応するPublic Keyで、Issuer由来で
あることと署名後に改ざんされていないことを確認する仕組み。署名は暗号化ではない。

### Sender-constrained Token

Tokenだけでなく、特定のPrivate KeyをControlしているClientだけが利用できるように
BindingされたToken。mTLS-bound Access TokenやDPoP-bound Access Tokenが代表例である。

## 6. Threat ModelとAbuse Path

### Long-lived Tokenの窃取

```text
AgentのLog、Trace、Environment、Memory等からTokenを窃取
  -> 攻撃者が別HostからBearer TokenをReplay
  -> 長い有効期間にわたりAPIを操作
```

Short lifetimeは窃取を防がない。窃取後に利用できる時間を制限する。

### Broad Scopeの転用

```text
quotation.readに必要なAgentがadmin相当Tokenを保持
  -> Agent Runtimeを侵害
  -> write、approve、deleteへ権限を転用
```

Minimal scopeは、侵害された正規Agentが行使できるAuthorityも縮小する。

### Cross-service Token Passthrough

```text
Token AをMCP Server向けに発行
  -> MCP ServerがToken AをDocument APIへそのまま転送
  -> Document APIがAudienceを検証せず受理
```

「信頼できるIssuerが発行したToken」と「このAPIで使用してよいToken」は別物である。

### Token Claimの改ざん

```text
scope=documents.readをscope=payments.writeへ変更
  -> Resource ServerがSignatureを検証しない
  -> 攻撃者がAuthorityを自己申告
```

Signatureが存在するだけでなく、Resource Serverでの検証が必要である。

### 正規Agent Contextの悪用

```text
悪意あるWeb PageがAgentをPrompt Injection
  -> 正規Agent Processが正規Keyを使用
  -> 有効なTokenとProofで許可範囲内の送金を要求
```

これはToken窃取やAgent Impersonationではない。C5.1.2にPassしても発生し得るため、
Runtime Authorization、Tool分離、Approval等の別Propertyで扱う。

## 7. Security InvariantとEnforcement

### Security Invariant

> Agentが一つの接続先で取得したCredentialによって、信頼されたIssuerが許可した
> 短い時間、対象System、Resource、Actionを超えて操作できてはならない。

### Enforcement flow

```text
Agent / Workload
    |
    | Workload IdentityまたはDelegation Evidence
    v
Authorization Server / STS
    |
    | short exp + narrow aud + narrow scope + issuer signature
    v
Agent / Workload
    |
    | Access Token
    v
Resource Server / API Gateway
    |
    | signature + issuer + audience + expiry + scopeを検証
    v
許可されたActionだけを実行
```

### 決定論的なEnforcement Point

**Authorization ServerまたはSecurity Token Service:**

- Agent／Workload Identityを確認する。
- Taskに必要なAudience、Resource、Actionだけを付与する。
- Riskに応じた短いExpiryを設定する。
- 許可したAlgorithmとKeyでTokenへ署名する。

**Resource ServerまたはAPI Gateway:**

- 想定したIssuerとSigning Keyを検証する。
- Algorithm confusionやUnsigned Tokenを拒否する。
- 自分向けのAudience、Tenant、Expiry、Not-before、Scopeを検証する。
- Claim不足、検証不能、Token Service障害時にFail closedする。

**Token BrokerまたはExchange Point:**

- Hopごとに対象Resource専用Tokenを取得する。
- Upstream Tokenの無制御なPassthroughを防ぐ。
- Delegationする場合も元のAuthorityより広げない。

ModelやAgentがIssuer、Audience、Scope、Trust Anchor、またはAllow/Deny Policyを決める
構成は決定論的Enforcementにならない。

## 8. Pass／FailとScope Calibration

| Scenario | C5.1.2評価 | 理由または別の問題 |
|---|---|---|
| 5分、`aud=purchasing-api`、`scope=quotation.read`のSigned TokenをAPIが全Claim検証する | Pass候補 | 実際のUse Caseに対してScopeが最小で、全経路で同じ検証があることが条件 |
| 正しく署名されているが24時間有効で`scope=*`である | Fail | Short-livedでもMinimal-scopedでもない |
| MCP Server向けTokenをDocument APIへ転送し、Document APIがAudienceを見ずに受理する | Fail | HopごとのAuthentication Boundaryがなく、別AudienceへCredentialを転用できる |
| 3分、Narrow Audience／Scope、正しいSignatureのBearer TokenがDebug Logから盗まれ、有効時間内にReplayされる | C5.1.2はPassし得る | Sender ConstrainingとSecret Handlingに別のGapがある |
| Token内に固定`nonce`を追加したが、Tokenと一緒にReplayできる | C5.1.2はPassし得る | 単なるNonce ClaimはHolderを証明しない。Replay防止の追加保証になっていない |
| Agentが正規TokenとDPoP Keyを使い、Prompt Injectionに従って許可Scope内で不正送金する | C5.1.2はPassし得る | Runtime Authorization、Human Approval、Transaction Integrity等の別Failure |
| Signed Tokenは`scope=payments.create`だが、任意送金先・任意金額を許す | 要Use Case確認 | Claim名ではなく、実際に行使できるAuthorityが最小かで判断する |
| Opaque Tokenと認証済みIntrospectionにより同等のIssuer、Expiry、Audience、Scopeを検証する | 原文への厳密適合は困難 | Security上は強い設計になり得るが、AISVS本文はSigned Tokenを明示する |

Configurationの存在だけではEvidenceにならない。少なくとも次をNegative Testする。

- ExpiredまたはNot-yet-valid Tokenを拒否する。
- Signatureを改ざんしたTokenを拒否する。
- Unknown Issuer、Unexpected Algorithm、Unknown KeyのTokenを拒否する。
- 別Audience、別Tenant、過剰ScopeのTokenを拒否する。
- MCP向けTokenをDownstream APIへ提示して拒否される。
- CertificateまたはDPoP Keyが異なるSenderからのReplayを、Sender Constraining採用時に
  拒否する。
- Token発行Service障害時にStaticまたはBroad CredentialへFallbackしない。

## 9. mTLS-bound Access Token

### 通常のTLSとmTLS

通常のHTTPSでは、主としてServerがCertificateを提示し、ClientがServerを認証する。

```text
Client  -- Server Certificate --> ServerのIdentityを確認
```

Mutual TLSでは、ClientもX.509 Certificateを提示し、対応するPrivate Keyを現在Control
していることをTLS Handshake中に証明する。

```text
Client Certificate + CertificateVerify
Client ---------------------------------> Server
       Private Keyは送信しない
```

ClientはHandshake Transcriptに対するSignatureを作る。ServerはCertificate内のPublic
Keyで検証する。この署名はAccess Token自体や送金Request Bodyへの署名ではない。

### OAuthにおける二つのmTLS用途

RFC 8705は、次の二つを区別している。

1. **mTLS Client Authentication:** Authorization ServerのToken EndpointでOAuth Clientを
   認証する。
2. **Certificate-bound Access Token:** 発行したAccess Tokenを、Clientが提示した
   CertificateへBindingする。

両者は補完的だが、同じ機能ではなく、必ず同時利用する必要もない。C5.1.2のToken
Replay対策として中心になるのは二つ目である。

### 発行からAPI利用まで

```text
1. AgentがKey PairとClient Certificateを持つ

2. Agent -- mTLS --> Authorization Server / Token Endpoint
   TLS HandshakeでAgentがPrivate Keyの所持を証明

3. Authorization ServerがCertificate ThumbprintをTokenへBinding

   {
     "aud": "document-api",
     "scope": "documents.read",
     "exp": 1234567890,
     "cnf": {
       "x5t#S256": "SHA-256 thumbprint of client certificate"
     }
   }

4. Agent -- 同じCertificateによるmTLS + Access Token --> Document API

5. Document APIが二つを検証
   a. Access TokenのIssuer Signature、Audience、Expiry、Scope
   b. TLSで提示されたCertificateのThumbprint == Tokenのcnf.x5t#S256

6. 一致しなければ401 invalid_token
```

ここでは異なる二つのSignatureが存在する。

- **Issuer Signature:** Authorization ServerがAccess Tokenへ署名する。Token Claimの
  AuthenticityとIntegrityを守る。
- **TLS Client Signature:** AgentがTLS HandshakeでPrivate Keyの所持を証明する。
  Tokenを提示しているSenderをCertificateへBindingする。

TokenがLogから盗まれても、攻撃者がClient Private Keyを持たなければ対応するmTLS
Connectionを確立できない。別Certificateを提示するとThumbprintが一致せず拒否される。

### Certificateは何を保証するか

X.509 CertificateはPublic KeyとIdentityまたは登録情報を結び付けるContainerである。
Private KeyはCertificateの中には含まれない。

PKI型mTLS Client Authenticationでは、ServerはCertificate Chain、SAN／Subject、期限、
必要に応じてRevocation等を検証してClient Identityを確立する。一方、Certificate-bound
TokenのProof of Possessionだけに使う場合、RFC 8705ではResource ServerがCA Chainを
Identity目的で再検証せず、TokenにBindingされたCertificateとの一致を確認する構成も
認めている。

### 運用上の難所

- Certificate発行、Secure Key Storage、Rotation、失効、Trust Bundle配布が必要。
- Access Tokenは特定CertificateへBindingされるため、Certificate Rotation後は新しい
  Tokenを取り直す必要がある。
- Load BalancerやService MeshでTLSを終端する場合、Client Certificate情報をBackendへ
  改ざん不能な経路で伝える必要がある。
- Internetから届く`X-Forwarded-Client-Cert`等を無条件に信頼してはならない。
- mTLSを要求するEndpointと通常Endpointを分離しないと、Browser等へCertificate選択UIを
  出すなどUXへ影響することがある。
- Clock Skew、CA／Bundle更新、Token Service障害、Rotation順序、Retry設計を誤ると、
  認証Failureが広範囲なService障害になる。

## 10. DPoPとの関係

mTLS-bound TokenとDPoPは概念的には重なる。どちらも次を実現する。

> Access Tokenだけを盗んだ攻撃者が、正規ClientとしてReplayできないようにする。

違いはPrivate Keyの所持を証明するLayerと単位である。

| 観点 | mTLS-bound Token | DPoP-bound Token |
|---|---|---|
| ProofのLayer | TLS Transport Layer | HTTP Application Layer |
| Proofの単位 | TLS Connection／Session | 原則としてHTTP Requestごと |
| Key表現 | X.509 Certificate | JWK Public Key |
| Token Binding | `cnf.x5t#S256` Certificate Thumbprint | `cnf.jkt` JWK Thumbprint |
| SenderのProof | TLS `CertificateVerify` | `DPoP` HeaderのSigned JWT |
| RequestとのBinding | TLS ChannelへBinding | `htm`、`htu`、`iat`、`jti`、`ath`等へBinding |
| PKI | Client Identity用途では必要になり得る | CA発行Client Certificateは不要 |
| Proxy／TLS終端 | Certificate情報の安全な伝達が難所 | HTTP Headerで運べるが、ProxyによるURI正規化等に注意 |
| Browser／Public Client | Certificate UXや配布が難しい | 比較的導入しやすい用途がある |

DPoPではClientがRequestごとにDPoP Proof JWTを作り、自身のPrivate Keyで署名する。
Resource Serverは次を確認する。

- Proof SignatureとPublic Key。
- HTTP Methodを表す`htm`。
- Target URIを表す`htu`。
- 発行時刻`iat`と一意な`jti`。
- Access Token Hashを表す`ath`。
- Access Tokenの`cnf.jkt`とProof Keyの一致。
- Serverが要求した場合は`nonce`。

このため、以前の対話で挙げたNonceは、Tokenへ固定値として置くのではなく、Serverが
発行し、ClientがPrivate Keyで署名するDPoP Proofへ含めて初めて意味を持つ。ただし
NonceだけがProof of Possessionを作るわけではなく、Private Key SignatureとToken／
Request Binding全体が中心である。

### 両方式の限界

- Agent Runtime自身が侵害され、正規Keyを署名Oracleとして使える場合は防げない。
- Access TokenのScope内で正規Agentが行う不適切なActionは防げない。
- mTLSはBusiness Request BodyやTransaction内容を直接署名しない。
- DPoPも標準ではHTTP MethodとURI等を中心にBindingし、Request Body全体のIntegrityや
  Human Intentを保証しない。
- Private KeyがExport可能なら、TokenとKeyを一緒に盗まれる可能性がある。

したがってNon-exportable Key、Process Isolation、Transaction Authorization、Human
Approval、Parameter Binding等は別のDefenseとして必要になる。

## 11. Prompt Injectionによる不正送金のControl Scope

次のScenarioを考える。

```text
Token: 5分、aud=payments-api、scope=payments.create、Signed、DPoP-bound
攻撃: Web PageのPrompt Injectionに正規Agentが従い、攻撃者宛て送金を作成
```

TokenのLifetime、Audience、Scope、Signature、Sender Constrainingが設計どおりなら、
この事象だけでC5.1.2はFailしない。DPoPも、正規Agent Processが正規KeyでProofを作る
ため阻止できない。

System全体には重大なFailureがあり、原因に応じて次を評価する。

| Failure | 主に評価するAISVS Requirement |
|---|---|
| Untrusted Web Dataを処理するComponentからPayment Tool実行へ到達できた | C9.3.5 |
| Agentが任意の送金先や金額を指定できた | C9.5.1 |
| Modelの判断だけでAllow／Denyを決めた | C9.5.3 |
| End-userのAuthorityがDownstreamへ維持されなかった | C9.5.2 |
| High-impact送金にExplicit Human Approvalがなかった | C9.2.1 |
| Approvalで完全な送金先、金額等を表示しなかった | C9.2.2 |
| ApprovalをParameter、Requester、Context、Single-use NonceへBindingしなかった | C9.2.8 |
| Untrusted InputのAnomaly DetectionとGatingがなかった | C11.4.1／C11.4.2（補助） |

最も直接的なPrimary Findingは観測した失敗で決める。BroadなPrompt Injectionという
ラベルだけで複数RequirementへCoverageを膨らませない。

Input Schema Validationは必要だが、正しい形式の攻撃者口座番号を拒否できない。
自然言語から悪意あるInstructionを完全に判別する決定論的Boundaryにもならない。

> AgentはTransactionを提案できるが、Agentの判断だけでHigh-impact Transactionを
> 認可してはならない。

## 12. AISVS Level 3と導入難易度

AISVSはC5.1.2をLevel 3にした個別理由をNormative Chapterで説明していない。次は
Requirementの性質と一般的なIdentity ArchitectureからのRepository上の推論である。

C5.1.2の原則自体は、OAuth、Workload Identity、Zero Trust、Service-to-service Security
等で以前から繰り返されてきた普遍的なものである。AI専用のCryptographic Primitive
ではない。

AI Agentで重要性が増す理由は次である。

- Agentが多くのTool、API、Tenant、Identity Domainを動的にまたぐ。
- Untrusted ContentがAgentのAction選択へ影響する。
- CredentialがPrompt、Context、Trace、Tool Parameter、Local Configへ露出しやすい。
- AgentがHumanより高速・連続的にAuthorityを行使する。
- Delegated Human AuthorityとAgent／Workload Authorityを区別する必要がある。

実装上は次の調整が難しい。

- Token LifetimeとTask完了時間、Retry、Queue、Long-running Jobの整合。
- Scope、Audience、Tenant、Delegation Chainの設計とDownstreamでの検証。
- Refresh、Token Exchange、Key／Certificate Rotationの失敗時動作。
- IdP／STS障害時のAvailabilityと、Fail closedの両立。
- mTLS終端、Service Mesh、Gateway、Multi-cloud Trustの一貫性。
- Observabilityを確保しつつTokenをLogへ残さない設計。
- Human Interactionがある場合のReauthenticationやCertificate UIによるUX低下。

Short-lived Tokenを自動更新できればHuman UXを抑えられるが、Refresh CredentialやSTSへ
新しいRiskとAvailability依存を移す。長期Tokenへ戻すFallbackはSecurity Propertyを
失わせる。

このように「言うは易いが、全Hopで正しく運用すると障害やUXへ影響しやすい」点は、
Level 3と整合する有力な説明である。ただし、AISVSが示した公式な個別理由ではない。

## 13. 対話の再構成

### Q1: MCP向けTokenをDownstream APIへ転送できるか

**問い:** 5分、Signed、`scope=documents.read`、`aud=knowledge-mcp`のTokenをMCP Serverが
Document APIへ転送する。Document APIはAudienceを確認しない。適合するか。

**学習者の判断:** 不適合。MCPとDocument APIの認可制御は分ける必要がある。

**整理:** 正しい。Authorizationに加え、Authentication CredentialのTrust Boundaryも
Hopごとに分ける。Signatureが正しくても自分向けTokenとは限らない。Document API専用
Tokenを取得し、Audienceを検証する。

### Q2: Short-lived Tokenが盗まれた場合

**問い:** 3分、Signed、Narrow Scope／AudienceのTokenがDebug Logへ出て、攻撃者が
有効期限内に別端末からReplayした。C5.1.2はFailか。何を追加するか。

**学習者の判断:** C5.1.2には適合する。Nonceを付与しDocument API側で検証する。

**整理:** C5.1.2にはPassし得るという判断は正しい。Token内の固定NonceだけではTokenと
一緒にReplayされる。DPoPやmTLS-bound Token等でSenderへBindingする。Nonceを使うなら、
Server発行Challengeを署名Proofへ含め、Replay管理と組み合わせる。

### Q3: 正規AgentがPrompt Injectionで不正送金した場合

**問い:** Short-lived、Narrow、Signed、DPoP-boundなTokenを正規Agentが使い、Prompt
Injectionに従って許可Scope内で不正送金した。C5.1.2はFailか。何が不足するか。

**学習者の判断:** C5.1.2の対象外。入力値検証が不足している。他に何があるか。

**整理:** C5.1.2にはPassし得る。Schema Validationは必要だが、正しい形式の悪意ある
送金を止めない。Tool分離、Fine-grained Runtime Policy、Model外のAuthorization、
Human Approval、Transaction Binding、送金先／金額制限が必要である。

### Q4: どのControlで不正送金を扱うか

**問い:** Prompt Injectionによる不正送金はどのControlで扱うべきか。

**整理:** 単一の「Prompt Injection Control」へ押し込まず、Failureを分解する。Untrusted
DataからTool実行への直結はC9.3.5、ToolとParameterのAuthorityはC9.5.1、Modelを
Authorization BoundaryにしたFailureはC9.5.3、High-impact ApprovalはC9.2系をPrimary
またはRelatedとして評価する。C11.4のDetectionは補助であり最終Boundaryではない。

### Q5: mTLS-bound TokenとDPoPは重複しないか

**学習者の疑問:** CertificateとPrivate Keyを使ってSignatureを検証するなら、DPoPと
同じではないか。

**整理:** 目的は重なるがLayerが異なる。mTLSはTLS HandshakeでCertificateに対応する
Private Keyの所持をConnection単位で証明し、Tokenの`cnf.x5t#S256`へBindingする。
DPoPはHTTP RequestごとにProof JWTへ署名し、Tokenの`cnf.jkt`へBindingする。どちらも
正規Agent Process自体の悪用や、許可Scope内の不適切なActionは防がない。

### 学習者の所感

1. C5.1.2のShort-lived、Least Privilege、Signature Validationは、多くのFrameworkや
   Guidanceで言われている普遍的な内容である。
2. 原則は容易に説明できるが、実装ではUX低下や障害につながり得るため難易度が高く、
   それがLevel 3の理由ではないか。

**整理:** いずれも重要な理解である。AI固有Primitiveではなく、既存のIdentity Security
原則をAgentの多Hop・動的実行へ適用している。Level 3理由は公式説明ではないが、
Credential LifecycleとAvailabilityを全Hopで安全に成立させる難しさと整合する。

## 14. このセッションから得られた洞察

1. **C5.1.2は普遍的なIdentity原則のAgent適用である。** AI専用方式ではないが、Agentの
   多Hop、動的Tool、Untrusted Contextにより重要性と運用難易度が増す。
2. **Short-livedは侵害防止ではない。** 侵害後の時間的なBlast Radiusを縮小する。
3. **Claim名ではなく実Authorityを見る。** `payments.create`がMinimal Scopeかは、
   許可される送金先、金額、Account、Contextによる。
4. **署名が正しいことと安全なActionであることは別である。** SignatureはIssuer由来の
   ClaimとIntegrityを証明するが、Policyの正しさやHuman Intentを証明しない。
5. **信頼できるIssuerのTokenと、このAPIで使用できるTokenは別物である。** Audience、
   Tenant、Scopeを受信側が検証する。
6. **HopごとにCredential Boundaryを置く。** MCP向けTokenをDownstreamへPassthroughせず、
   対象Resource用の狭いTokenへ交換する。
7. **Tokenを盗んだだけではAgentになりすませないことが追加保証になる。** mTLSまたは
   DPoP等のSender Constrainingを使う。
8. **Nonce単体はReplay Defenseではない。** Server Challenge、Private Key Signature、
   Request／Token Binding、Replay管理と組み合わせる。
9. **Input ValidationはAuthorization Boundaryではない。** Well-formedな悪意ある値を、
   Schema Validationだけでは拒否できない。
10. **AgentはTransactionを提案できるが、その判断だけでHigh-impact Actionを認可しては
    ならない。** Runtime Policy、Approval、Transaction Bindingが別途必要である。
11. **DPoPとmTLSは同じ目的を異なるLayerで実現する。** Application Request単位のProofと
    Transport Connection単位のProofという違いがある。
12. **Sender Constrainingは侵害済み正規Processを止めない。** 正規Keyを署名Oracleとして
    使用できるため、Process IsolationとAction Authorizationが必要である。
13. **重大なSystem Failureでも全ControlをFailにしない。** C5.1.2のCredential保証と、
    C9のTool Authorization／Approval保証を分離して評価する。
14. **Level 3は原則の珍しさではなく、End-to-end運用の難しさと解釈できる。** Token、
    Certificate、Key、Trust Bundle、Rotation、Gateway、Failure Modeを整合させる必要が
    ある。ただしこれはRepository Interpretationである。
15. **SecurityとAvailabilityをFallbackで交換しない。** STSやCertificate障害時にLong-lived
    Broad Tokenへ戻すと、C5.1.2のSecurity Propertyを失う。

## 15. 後から設計レビューするときの確認事項

- Agent／Workload Identityの単位とCredential所有者を説明できるか。
- 各Agent、MCP Server、Tool、Downstream API間のTrust Boundaryを列挙したか。
- Token LifetimeはRiskとTask durationに対して十分短いか。
- Retry、Queue、Long-running JobがExpiryを迂回していないか。
- Scopeの名前ではなく、実際に実行できるResourceとActionを確認したか。
- Resource ServerがIssuer、Signature、Algorithm、Key、Audience、Tenant、Expiry、Scopeを
  検証するか。
- Upstream Tokenを別AudienceへPassthroughしていないか。
- Downstream Token ExchangeでAuthorityが拡大していないか。
- Token、Refresh Token、Certificate、Private KeyがPrompt、Log、Trace、Tool Parameter、
  Error、Memoryへ露出しないか。
- Bearer Token ReplayをThreat Modelに含めたか。
- mTLSまたはDPoP採用時、Tokenと提示KeyのBindingをNegative Testしたか。
- mTLS終端ProxyからBackendへのCertificate情報を改ざん不能にしたか。
- Certificate Rotation時にBound Tokenを再発行できるか。
- Rotation、STS、CA、Trust Bundle障害時にBroad Static CredentialへFallbackしないか。
- Agent Runtime侵害時にKeyを使われる前提でAction Authorityを限定したか。
- C5.1.2のPassと、Prompt Injection、Tool Authorization、Human Approval、Transaction
  Integrityの評価を分けたか。
- Opaque Token等の代替Architectureを使う場合、AISVS原文との差を明示したか。

## References

### Normative and AISVS sources

- [OWASP AISVS v1.0 C5 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [OWASP AISVS v1.0 C5.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-01-Identity-Management-Authentication.md)
- [OWASP AISVS v1.0 C9 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
- [OWASP AISVS v1.0 C11 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C11-Adversarial-Robustness.md)

### Token and sender-constraining specifications

- [RFC 9700: Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/info/rfc9700/)
- [RFC 8705: OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/info/rfc8705/)
- [RFC 9449: OAuth 2.0 Demonstrating Proof of Possession](https://www.rfc-editor.org/info/rfc9449/)
- [RFC 8693: OAuth 2.0 Token Exchange](https://www.rfc-editor.org/info/rfc8693/)
