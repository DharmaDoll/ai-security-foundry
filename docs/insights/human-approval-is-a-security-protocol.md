---
title: "Human ApprovalはButtonではなくSecurity Protocolである"
document_kind: "cross-cutting-insight"
status: "draft"
last_updated: "2026-09-14"
---

# Human ApprovalはButtonではなくSecurity Protocolである

## 中心となる洞察

Human Approvalは、画面にButtonを置くことでも、起動時に包括同意を得ることでもない。具体的な操作を正確に
提示し、権限のある人の判断を、その操作とContextへ結び付け、差替え・再利用を防ぎながら実行時まで保つ
Security Protocolである。

> 「操作できる」と「今回その操作をするのが妥当」は別である。

## Deterministic ControlとJudgmentを分ける

| 層 | 問うこと |
|---|---|
| Authorization Policy | このPrincipalがこのAction・Resource・値を操作できるか |
| Risk／Reversibility classification | 操作の影響と復旧条件は何か |
| Review | 今回の計画に異常、矛盾、Business上の不自然さがないか |
| Human Approval | 権限のある人が今回の具体的操作を認めたか |

AIによる追加Reviewは、人間のDouble Checkと似た役割を補助できる。しかしAI ReviewのAllowがPolicyのDenyを
上書きしたり、必要なHuman Approvalを代替したりしてはならない。

## Approval Protocol

```text
実行要求をCanonical化
  -> PolicyとImpactを評価
  -> 完全な対象・値・差分を表示
  -> HumanをFreshにAuthentication
  -> 具体的要求をApproval
  -> Approval Serviceが保存済み要求へ署名
  -> Action / Requester / Context / NonceへBinding
  -> 未使用確認と使用済み更新を原子的に実行
  -> 同じ内容だけを下流で実行
```

Canonical表示はModelの要約ではなく、実際に実行する要求から作る。省略、Truncation、Alias、制御文字等で、
見える対象と実対象が食い違わないようにする。

## Approvalを発行するAuthorityを隔離する

KeyをKMS等へ置いてAgentから読めなくしても、Agentが任意内容へ署名を要求できれば隔離にならない。Agentには
申請だけを許し、Approval ServiceはAgentが変更できないHuman Approval recordとPolicyを確認して、保存済みの
内容だけへ署名する。

> Keyを隠すだけでなく、承認を発行する力をAgentから隔離する。

## Replayと変更への対応

Approvalを一回限りにするには、Nonceを付けるだけでなく、未使用確認と使用済み更新を原子的に行う。外部APIの
結果が不明な場合も、安易に未使用へ戻さず、Transaction IDと冪等性を含めて復旧する。

計画が承認後に変わり、より高いImpactの操作が追加されたら、古いApprovalを流用しない。親Task、子Agent、
Tool呼出しを一つのChainとして追い、最大ImpactへApproval条件を引き上げる。個々に低Riskな操作の組合せが
新しい高Impactを生まないかも見る。

## Reviewerも攻撃対象である

Reviewer AIを追加しただけでは独立Reviewにならない。操作側と同じ非信頼文書、同じModel Failure、同じContextを
共有すると、両者が同じ誘導を受ける。偽のReview結果を拒否できても、正規Reviewer自身が騙される経路は残る。

被害を最終Policyが防いでも、Reviewerへの操作が成功した事実を成功扱いしない。

## 設計レビューへの応用

- Approval対象はTool名ではなく、実Action、対象、値、Scopeか。
- 表示は実行要求から作られ、完全な内容へ到達できるか。
- Authentication、Authorization、Review、Approval、Bindingを分けているか。
- AgentがApproval record、Signer、Key、Routing、Deploymentを支配できないか。
- Approval後のParameter差替えと再利用をNegative Testしたか。
- Plan変更、子Agent、再試行、非同期処理で旧Approvalを流用しないか。
- Humanの誤判断とApproval fatigueを運用上監視・軽減するか。

## 誤用と限界

- Approvalは通常のAuthorizationやLeast Privilegeを置き換えない。
- 完全な表示は、人が読み理解し正しく判断することまでは保証しない。
- SignatureはHuman Judgmentの存在を自動的に証明しない。
- 可逆性の正しい分類は、そのRiskを受容してよいという結論ではない。
- Human Approvalが多すぎると、形骸化や自動承認を招き得る。

## Slide-ready summary

- ApprovalはButtonではなく、具体的Transactionを守るProtocolである。
- 権限と今回の妥当性判断を分ける。
- 見せた内容、承認した内容、実行した内容を同一にする。
- Approval発行AuthorityをAgentから隔離する。
- Nonce消費、Plan変更、Action Chainまで扱う。

## 起点となった学習記録

- [C9.2.1：Human Approval](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.1-human-approval-before-high-impact-actions/learning.md)
- [C9.2.2：Canonical Approval Display](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.2-complete-canonical-approval-display/learning.md)
- [C9.2.6：AI-augmented Review](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.6-additive-ai-review-before-high-risk-actions/learning.md)
- [C9.2.7：Reviewer Protection](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.7-protect-ai-action-review-from-manipulation/learning.md)
- [C9.2.8：Single-use Approval](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.8-cryptographically-bound-single-use-approvals/learning.md)
- [C9.2.9：Approval Issuer Isolation](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.9-approval-issuing-key-and-credential-isolation/learning.md)
- [C9.2.10：Chain-wide Approval](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.10-chain-wide-highest-impact-approval/learning.md)

本書はC9.2を新しい単一Controlへまとめるものではなく、実装時に一つのProtocolとして考えるための洞察である。
