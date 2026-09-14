---
title: "不要なAuthorityを消し、残る全経路を完全仲介する"
document_kind: "cross-cutting-insight"
status: "draft"
last_updated: "2026-09-14"
---

# 不要なAuthorityを消し、残る全経路を完全仲介する

## 中心となる洞察

最小権限はBlast Radiusを減らすだけではない。安全に許可するためのPolicy、Approval、Monitoring、Testを
設計しなければならない経路そのものを減らす。

> 最も安く説明できるCapabilityは、最初から存在しないCapabilityである。

ただし、必要な経路へPolicyを置くだけでは足りない。Resourceへ到達するすべての経路が、同じSecurity
Decisionを迂回不能な形で通るComplete Mediationが必要である。

## 再利用可能な順序

```text
Inventory
  -> 不要なCapabilityを削除
  -> 必要なCapabilityを対象・Action・Contextへ限定
  -> 全Access PathをPEPへ収束
  -> 障害時はFail closed
  -> 迂回経路をNegative Test
```

Allow Policyは静的な名前Listとは限らない。`Principal x Action x Resource x Context`について、
「この場合だけ許可」をPositive Ruleとして定義する。

## 見かけの境界に注意する

次のLabelや構成名だけでは、実効的な制限を証明しない。

- Container内で動く。
- Private NetworkやCluster内にある。
- Managed Serviceを使う。
- Gateway経由の正規APIだけを制限する。
- Manifestに制約が書かれている。
- Agentが通常WorkflowでAdmin機能を使わない。

Host Mount、管理Socket、直接Database接続、別Port、Batch、Debug、Migration、Fallback、再配置権限等を含め、
実際に到達できる範囲を見る。

## Policy DecisionとEnforcementを分ける

- PDPはAllow／Denyを決める。
- PEPは決定に従って実行を止める。
- Resourceは、迂回した直接Accessも拒否できる必要がある。

正しいPolicyが存在しても、別経路がPolicyを通らなければSecurity Propertyは成立しない。UIやGatewayの拒否を、
Resource側の拒否と混同しない。

## Agentic Systemでの意味

Agentへ「提案を書く」能力は与えても、「有効化する」「再配置する」「Policyを変える」能力は分離できる。
文書変換等の定型処理をAgent化せず、狭い決定論的Toolにすることも、不要なReasoning surfaceとCapabilityを
減らす設計である。

Agentが自分の制限を直接変更できなくても、別Workloadの作成、Credential取得、Queueへの書込み等で同じ結果へ
到達できれば、Capabilityは残っている。

## 設計レビューへの応用

- そのCapabilityは本当に通常業務に必要か。
- Read、Write、Admin、Deploy、Impersonate、Delegateを分けたか。
- UI、API、CLI、Agent、CI/CD、Batch、Debug、Recoveryの全経路を列挙したか。
- Policy取得やSandbox障害時に、広い既定権限へFallbackしないか。
- ToolやAgentを侵害した状態からの実効到達範囲を試したか。
- AllowのPositive Testと、未知・迂回経路のNegative Testを両方持つか。

## 誤用と限界

- 最小権限が常に運用総コストを最小化するとは限らない。必要機能を過度に削れば例外運用が増える。
- 「権限を与えていない」という設計書だけでなく、別経路でも取得できないことを実証する。
- Complete Mediationがあっても、Policy自体が過大・誤りなら危険は残る。
- Availabilityを理由にBroad CredentialへFallbackすると、Security Propertyを失う。

## Slide-ready summary

- 最小権限は、被害だけでなくSecurity reasoning surfaceを減らす。
- 必要な操作だけを狭く表し、例外は保護された管理経路へ分ける。
- Policyが正しいことと、全AccessがPolicyを通ることは別。
- 構成名ではなく、侵害時の実効到達性を見る。

## 起点となった学習記録

- [C5.2.1：Explicit AllowとDefault Deny](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.1-explicit-allow-default-deny-ai-resources/learning.md)
- [C5.2.5：PDP Isolation](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.5-agent-authorization-pdp-isolation/learning.md)
- [C9.2.5：Bounded Self-modification](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.5-bounded-agent-self-modification/learning.md)
- [C9.3.1：Tool Isolation](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.1-least-privilege-tool-execution-isolation/learning.md)
- [C9.3.4：Manifest Runtime Enforcement](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.4-runtime-enforcement-of-tool-manifests/learning.md)

本書は特定製品やFramework項目を必須化せず、複数の学習記録に共通した設計順序を抽出したものである。
