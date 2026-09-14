---
title: "ControlはSystem安全性の合否ではなく、Failureを切り分ける診断軸である"
document_kind: "cross-cutting-insight"
status: "draft"
last_updated: "2026-09-14"
---

# ControlはSystem安全性の合否ではなく、Failureを切り分ける診断軸である

## 中心となる洞察

一つのControlにPassしても、System全体が安全とは限らない。反対に重大な事故経路があっても、関係する
すべてのControlがFailするわけではない。Controlは総合点ではなく、どのSecurity Propertyが成立し、
どこが壊れたかを切り分ける診断軸として使う。

> Systemの危険性と、個別Controlの評価を分ける。Scopeを守るほど、直すべき境界が明確になる。

## 具体例

| 観測 | 個別評価の考え方 |
|---|---|
| 正しい署名Tokenで未認可送金が行われた | Credential検証はPassし得るが、Action AuthorizationはFailする |
| Reviewer AIが誘導されたが、Policyが送金を阻止した | Reviewer保護はFail、決定論的Policyは成功として別々に記録する |
| Freshな追加認証後に送信先が差し替えられた | AuthenticationはPassし得るが、Transaction BindingにGapがある |
| Default Denyは動くが、必要なAllow Ruleがない | 拒否のNegative Testは成功しても、Control全体のPassとは限らない |

Defense in Depthでは、一つの層が別の層の失敗を食い止めることがある。被害が出なかったという理由で、途中の
失敗した層まで成功扱いすると、次回は同じ防御が残っていると誤認する。

## 評価状態を混同しない

- `Pass`：定義したScopeでPropertyを裏付けるEvidenceがある。
- `Fail`：Propertyを破る動作または構成を確認した。
- `Insufficient evidence`：Passを裏付けられないが、回避を実証したわけでもない。
- `N/A`：対象となる機能・Data・Trust Boundaryが存在しないと説明できる。
- `Partial mitigation`：Riskを下げるが、RequirementのFailure pathが残る。

未確認をFailと断定せず、未確認をPassにも使わない。部分的MitigationをControl Passへ昇格させない。

AISVS Verification Levelも、実装優先順位、Control maturity、学習難易度、他StandardのAssurance Levelと
同義ではない。Level 2や3でも、Failureの不可逆性や製品のThreat Modelに応じてBaselineへ前倒しできる。

## 実務への応用

設計レビューや脆弱性診断では、Findingごとに次を分ける。

1. Systemとして何が危険か。
2. どのSecurity Propertyが破れたか。
3. どのEnforcement Pointが不足したか。
4. どの防御層は機能したか。
5. 何が未検証か。
6. 隣接Controlへ何を押し出したか。

この分解により、一つの万能対策を求めるのではなく、認証、認可、承認、完全性、隔離、監視等を適切な場所で
修正できる。

## 誤用と限界

- Scopeを狭く守ることは、重大なSystem Riskを小さく報告する理由ではない。
- 個別Controlの評価と併せて、End-to-endのAttack PathとBusiness Impactを報告する。
- Frameworkの粒度が常に理想的とは限らない。重複やGapは隠さず記録する。
- Control数やPass率を、Security outcomeの代替指標にしない。

## Slide-ready summary

- 一ControlのPassはSystem Securityを意味しない。
- 被害を止めた層の成功で、別の層の失敗を隠さない。
- Pass、Fail、未検証、N/A、部分的Mitigationを分ける。
- Verification Levelを、そのまま実装順やSecurity重要度にしない。
- Controlは点数表ではなく、修正すべきSecurity Boundaryを示す診断軸である。

## 起点となった学習記録

- [C5.1.1：Step-up Authentication](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.1.1-step-up-authentication/learning.md)
- [C5.1.2：Agent Token](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.1.2-short-lived-minimal-scoped-signed-agent-tokens/learning.md)
- [C5.2.5：PDP Isolation](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.5-agent-authorization-pdp-isolation/learning.md)
- [C9.2.7：Reviewer保護](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.7-protect-ai-action-review-from-manipulation/learning.md)

本書は上記RequirementのNormativeな統合ではなく、評価時に繰り返し現れたRepository interpretationである。
