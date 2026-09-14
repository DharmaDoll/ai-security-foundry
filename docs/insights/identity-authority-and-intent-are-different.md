---
title: "Identity、Authority、Intent、Transaction Integrityを分ける"
document_kind: "cross-cutting-insight"
status: "draft"
last_updated: "2026-09-14"
---

# Identity、Authority、Intent、Transaction Integrityを分ける

## 中心となる洞察

「正しい主体が接続した」「その主体に権限がある」「今回の操作を望んでいる」「承認した内容と同じ操作が
実行された」は、それぞれ別のSecurity Propertyである。一つのToken、署名、確認画面へ意味を詰め込みすぎない。

```text
Authentication
  -> 誰であるか
Authorization
  -> 何をしてよいか
Approval / Intent
  -> 今回の具体的操作を認めたか
Transaction Integrity
  -> 認めた操作と実行した操作が同じか
```

## Human、Agent、Workloadを同一視しない

Workload Identityは「正規に起動されたAgentやService」であることを示せる。しかし、次を自動的には証明しない。

- Human Userが現在もその操作を望んでいる。
- AgentのReasoningが正しい。
- Prompt Injectionの影響を受けていない。
- Toolの対象・金額・宛先が許可範囲内である。

AgentはActionをRequestまたは提案できるが、自分の出力だけでAuthorityやHuman Intentを作ってはならない。

## 署名が保証するものを広げない

正しいSignatureは、対応するKeyでDataが署名され、署名後に改ざんされていないことを示す。署名だけでは、
Policyが正しい、内容が安全、人が承認した、現在も有効、別のResourceで使える、という結論にはならない。

同様に、信頼できるIssuerのTokenであることと、そのAudience、Tenant、Resource、Actionで使用できることは別である。

## 一つのUXで複数Propertyを満たす場合

重要操作の画面で、Security Keyによる再認証と操作承認を同時に行う設計は可能である。ただし内部では、
次を別々に検証・記録する。

1. FreshなAuthenticationが成立したか。
2. Principalに対象操作のAuthorityがあるか。
3. 完全な操作内容を見せ、明示的Approvalを得たか。
4. Approvalを対象・値・実行ContextへBindingしたか。
5. Resourceが同じ内容だけを実行したか。

見た目が一つのButtonでも、保証まで一つになるわけではない。

## 設計レビューへの応用

- Human User、Agent、Application、Tool、Downstream ServiceのIdentityを分けたか。
- 各Hopで誰のAuthorityを誰が行使するか説明できるか。
- Agent-authored User、Role、Tenant、ApprovalをTrusted inputにしていないか。
- Freshnessは新しいToken発行時刻ではなく、実Authentication eventから判断するか。
- Signature、Authentication、Authorization、Approvalを相互の代替にしていないか。
- 実行時の対象・値が、認可・承認された内容と同一か。

## 誤用と限界

- 強いAuthenticationは、過大権限や悪いPolicyを直さない。
- 正しいAuthorizationは、Humanが今回の操作を望むことを証明しない。
- Human Approvalは、本人性、最小権限、操作の正しさを単独では保証しない。
- Transaction Bindingは、Bindingした操作自体が安全であることを保証しない。

## Slide-ready summary

- 「誰か」「何をしてよいか」「今それを望むか」「同じ操作を実行したか」は別。
- Agent IdentityはHuman Intentの代替ではない。
- SignatureはProvenanceとIntegrityを示すが、安全な判断までは示さない。
- 一つの画面で実装しても、Security Propertyは分けて評価する。

## 起点となった学習記録

- [C5.1.1：Step-up Authentication](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.1.1-step-up-authentication/learning.md)
- [C5.1.2：Agent Token](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.1.2-short-lived-minimal-scoped-signed-agent-tokens/learning.md)
- [C9.2.1：Human Approval](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.1-human-approval-before-high-impact-actions/learning.md)
- [C9.2.8：Approval Binding](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.8-cryptographically-bound-single-use-approvals/learning.md)

本書は個別Requirementを統合した新しいControlではなく、複数の保証を混同しないためのRepository interpretationである。
