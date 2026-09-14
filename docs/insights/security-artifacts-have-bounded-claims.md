---
title: "Security Artifactは証明できる範囲を越えて信頼しない"
document_kind: "cross-cutting-insight"
status: "draft"
last_updated: "2026-09-14"
---

# Security Artifactは証明できる範囲を越えて信頼しない

## 中心となる洞察

Signature、Schema、Manifest、Policy、Log、Classification Label等はSecurityを支える重要なArtifactである。
しかし、それぞれが証明するPropertyは限定される。一つのArtifactが正しいことから、内容・判断・実行・System
全体の安全まで推論しない。

> Artifactの存在ではなく、何を誰に対してどこまで証明するかを見る。

## 代表的な保証境界

| Artifact／Mechanism | 主に証明・支援すること | それだけでは証明しないこと |
|---|---|---|
| Digital Signature | Issuer、Integrity、Key possession | 内容の安全性、Policyの正しさ、Human Intent |
| Schema Validation | 型、必須Field、許容値、構造 | 値の権限、真実性、Prompt Injection耐性 |
| Tool Manifest | 必要能力と制約の宣言 | 宣言の最小性、真実性、Runtimeでの強制 |
| Authorization Policy | 定義された条件でのDecision | 全Access PathがDecisionを通ること |
| Log／Alert | Eventの観測と記録 | 違反や副作用を阻止したこと |
| DLP Detection | 定義Patternとの一致 | Requester固有の受領権限、言い換えた情報の安全性 |
| Classification Label | Protection stateや取扱条件 | PolicyがLabelを実際に強制すること |
| Deployment名・製品機能 | 意図したArchitectureの手掛かり | 実構成と攻撃時の実効的なIsolation |

## よくある誤った推論

```text
署名が正しい
  -> 内容も安全である              # 誤り

JSON Schemaに適合した
  -> 実行してよい                  # 誤り

PolicyにDenyが書かれている
  -> Resourceは必ず守られる         # 誤り

違反をLogへ記録した
  -> 違反をEnforceした              # 誤り

ManifestにNetwork禁止と書いた
  -> ToolはNetworkへ接続できない    # 誤り
```

必要なのは、隣接するPropertyを別のEnforcement PointとEvidenceでつなぐことである。

```text
宣言
  -> 妥当性Review
  -> Trusted Configuration
  -> Runtime Enforcement
  -> Negative Test
  -> Operational Evidence
```

## 「正しい」と「安全」の間

過大権限を正直に宣言した署名済みManifestは、署名・宣言としては正しいが安全ではない。悪意ある宛先を正しい型で
表したJSONはSchemaに適合する。誤ったPolicy Decisionを正規Keyで署名することもできる。

したがって、Artifactごとに次を明示する。

- Producerと信頼根拠。
- 対象Version、Resource、Audience、Context。
- 保証するProperty。
- 保証しないProperty。
- 実行へ反映するEnforcement Point。
- Failureを実証するNegative Test。

## 設計レビューへの応用

- 「導入済み」「署名済み」「検証済み」という言葉の対象Propertyを確認する。
- ArtifactのProducerを、ModelやAgentの自己申告にしていないか。
- Versionと実行物、PolicyとPEP、ManifestとRuntimeが対応しているか。
- 検出、判断、阻止を別々に観測できるか。
- 一つの成功Evidenceで隣接PropertyをPassにしていないか。
- 正しい形式の悪意ある値、正規署名された危険な内容をNegative Testへ含めるか。

## 誤用と限界

- Artifactの限界を強調して、署名、Schema、Policy等を不要と結論しない。それらはDefense in Depthの構成要素である。
- 個別Propertyを分けても、End-to-endの攻撃経路とBusiness Impactを併せて評価する。
- Artifactの意味は利用ContextとVersionで変わる。一般的な製品名だけで保証範囲を固定しない。

## Slide-ready summary

- SignatureはSafetyを証明しない。
- SchemaはAuthorizationを証明しない。
- ManifestはEnforcementを証明しない。
- PolicyはComplete Mediationを証明しない。
- LogはPreventionを証明しない。

## 起点となった学習記録

- [C5.1.2：Agent Token](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.1.2-short-lived-minimal-scoped-signed-agent-tokens/learning.md)
- [C5.2.4：Post-inference Authorization](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.4-post-inference-authorization-filtering/learning.md)
- [C5.2.7：Classification Label Propagation](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.7-downstream-classification-label-propagation/learning.md)
- [C9.3.2：Tool Output Schema](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.2-tool-output-schema-validation/learning.md)
- [C9.3.3：Tool Manifest](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.3-explicit-tool-manifest-security-requirements/learning.md)
- [C9.3.4：Runtime Enforcement](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.4-runtime-enforcement-of-tool-manifests/learning.md)

本書は各Artifactを弱いと評価するのではなく、保証Claimを正しい境界へ保つためのRepository interpretationである。
