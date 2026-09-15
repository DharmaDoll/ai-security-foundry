# C9.4.1：Agent Instanceを一意な暗号的Identityとして認証する

AISVS Verification Level: 2

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.4.1`。採用済み固定Revisionは
`78775233666a2022dcfb82037e5e029116955c00`。

> Verify that each agent instance has a unique cryptographic identity and authenticates as a first-class principal to downstream systems.

日本語訳：各Agent Instanceが一意な暗号的Identityを持ち、下流Systemに対して独立したPrincipalとして認証される
ことを確認する。[要件本文][normative]

Normativeは要件本文、Researchは補足である。Instance境界、Identity伝達、Userとの関係に関する具体化は
Repository interpretation、対話からの整理は学習上の洞察である。学習完了はControl成熟度や製品適合を変更しない。

## 平易な説明

複数のAgent WorkerがApplication共通のAPI Keyを使うと、下流Systemからは全て同じ主体に見える。

```text
Agent Instance A ─┐
Agent Instance B ─┼─ 共通API Key ─→ Downstream API
Agent Instance C ─┘
```

この構成では、どのInstanceが操作したかを信頼できる形で区別できず、侵害された一体だけを失効・拒否することも
難しい。C9.4.1は各Agent InstanceをApplication内部の単なる処理番号ではなく、下流が認証できる独立した主体として
扱う。

**Agent Instanceの名前を記録することではなく、そのInstanceであることを暗号的に証明する。**

## 用語

### Agent Instance

同じAgent定義から生成されても、実行単位が異なれば別Instanceになり得る。

```text
Support Agentという定義
  ├─ Instance A：AliceのTask
  ├─ Instance B：BobのTask
  └─ Instance C：定期Batch
```

Instance境界は、Task、Session、Worker、Process、Container、長期稼働Agent等、Architectureに応じて定義する。
生成、再起動、置換、終了、ID再利用の境界を曖昧にしない。

### Principal

Principalは認証・認可・監査の対象となる主体である。Userだけでなく、Application、Workload、Agent、MCP Server、
ToolもPrincipalになり得る。`first-class principal`とは、下流SystemがAgent Instanceを独立した主体として認識し、
必要に応じて認可・監査・失効の単位として扱えることを意味する。

### 暗号的Identity

自己申告の名前ではなく、信頼するIssuerの署名、証明書、鍵の保有等によって検証できるIdentityである。

- Instance固有の短命なmTLS Client Certificate
- SPIFFE IDとSVID
- Instance固有のWorkload Identity
- InstanceをSubjectに持つ署名付きJWT
- Cloud IAMのWorkload Credential
- Instance固有鍵による署名と証明書

例えば、次のような署名付きTokenを下流がIssuer、Signature、Audience、有効期限とともに検証する。

```json
{
  "iss": "trusted-agent-runtime",
  "sub": "agent-instance:8b7c",
  "aud": "document-api",
  "exp": 1789400000
}
```

Agentが自分で任意の`sub`やHeaderを書くことは、暗号的なIdentity証明にならない。

## 推奨するArchitecture

```text
Agent Orchestrator
  ↓ Instance生成
Trusted Identity Issuer
  ↓ Instance固有Credential
Agent Instance
  ↓ 認証
Gateway／Downstream API
  - Credentialを検証
  - 個体Identityを保持
  - First-class principalとして識別
```

主なTrust Boundaryは、Identity IssuerとInstance、InstanceとGateway、Gatewayと下流Systemの間である。
決定論的なEnforcement Pointは、Credential発行、InstanceへのBinding、下流の認証Middleware、失効・終了処理にある。

Security Invariantは、一つのAgent Instanceを侵害しても別Instanceとして認証できず、下流Systemが各操作を検証済みの
Instanceへ帰属できることである。

## Identityを仲介で潰さない

入口でInstance固有のmTLS証明書を検証しても、Gatewayが全てを共通Service Accountへ変換し、個体Identityを信頼できる
形で下流へ伝えなければ、下流から見たFirst-class principalではない。

```text
Instance固有Identity
  ↓ Gatewayで消失
共通Service Account
  ↓
Downstream API
```

証明書自体をEnd-to-Endで転送する必要はない。信頼するGatewayが検証結果を署名付きTokenへ再発行し、下流が個体を
認証できる方式も成立し得る。

```json
{
  "iss": "trusted-agent-gateway",
  "sub": "agent-instance:8b7c",
  "aud": "document-api",
  "act": {
    "sub": "agent-platform"
  }
}
```

重要なのはCredentialの形式ではなく、下流で受理されたPrincipalと実際のInstanceとの信頼可能な対応が失われない
ことである。

## User、Application、Agent Instanceを分ける

Userを認証しても、Agent InstanceのIdentityを代替しない。Userの代理で動く場合、少なくとも次を区別する。

```text
委譲元：Alice
実行主体：Agent Instance 8b7c
対象：Document X
許可操作：Read
```

Aliceだけを`sub`として認証し、Agent Instance IDを監査用属性として付けるだけでは、C9.4.1の個体認証にならない。
一方、Agent Instanceを認証できてもAliceの権限を自動的に持つわけではない。Userの委譲Contextは主にC9.5.2、
操作の認可はC9.5で扱う。

**Agent Identityは認証の根拠であり、操作の認可そのものではない。**

## 検証と対話の再構成

**問い：十個のAgent Workerが共通API Keyを使い、各自が自由に指定できる`X-Agent-Instance-ID`をLogへ残す。
適合するか。**

学習者：「Fail」

整理：そのとおり。暗号的に認証されるのは共通Service Accountだけである。自己申告HeaderやTrace IDは、
Instance Identityの証明にならない。

**問い：Orchestratorは各WorkerへInstance固有の短命mTLS証明書とSPIFFE IDを発行する。Document APIはCA署名、
有効期限、SPIFFE IDを検証し、Instance単位で監査・失効できる。適合するか。**

学習者：「Pass」

整理：そのとおり。Instance固有の暗号的Identityと、下流におけるFirst-class principalの両方が成立している。

**問い：各Instanceは異なるmTLS証明書を持つが、Gatewayが全てを共通Service Accountへ変換し、下流は個体単位の
認証・監査・失効ができない。適合するか。**

学習者：「Fail」

整理：そのとおり。入口で認証しても、下流へ到達する前にIdentityを潰している。Gatewayが検証済みIdentityを
改ざんできない形式へ再発行し、下流が個体を認証できるなら別である。

**問い：Aliceを`sub`とする署名付きTokenに`agent_instance_id`属性を付けるが、下流が認証するPrincipalはAliceだけで、
Instance単位の認証・失効・拒否はできない。適合するか。**

学習者：「Fail」

整理：そのとおり。User IdentityはAgent Instance Identityを代替しない。委譲元と実行主体を別の信頼可能なIdentityとして
扱う必要がある。

## Negative Test

- 別Instanceの名前をHeader、Claim、Log Fieldへ設定し、認証済みPrincipalを変更できないことを確認する。
- 二つのInstanceへ異なるCredentialを発行し、下流が異なるPrincipalとして識別することを確認する。
- 異なる鍵でも同じPrincipalへ解決される構成を検出する。
- Gateway通過後に個体Identityが共通Service Accountへ潰れないことを確認する。
- 未信頼Issuer、不正Signature、異なるAudience、期限切れCredentialを個体Identityとして受理しないことを確認する。
- 一つのInstanceを失効し、他Instanceへ影響せず該当Instanceだけが拒否されることを確認する。
- User Identityだけを提示し、Agent Instance認証を省略できないことを確認する。

## 洞察と設計レビューへの問い

- このSystemでは何を一つのAgent Instanceと定義するか。
- Instance生成、再起動、置換、終了時にIDをどう扱うか。
- 自己申告のInstance IDと、暗号的に検証されたPrincipalを混同していないか。
- GatewayやService Meshで個体Identityを共通Service Accountへ潰していないか。
- 下流が受理したPrincipalを、Issuerの発行記録と実際のInstanceへ追跡できるか。
- 一体だけを失効・拒否できるか。
- User、Application、Agent InstanceのIdentityとAuthorization Contextを区別しているか。

## References

- [AISVS v1.0 C9.4.1][normative]
- [対応Research][research]
- [C9 Family overview](../README.md)
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-04-Agent-Identity-and-Audit.md
