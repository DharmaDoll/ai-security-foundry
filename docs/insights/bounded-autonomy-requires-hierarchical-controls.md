---
title: "Bounded Autonomyには階層ごとの上限と停止意味論が必要である"
document_kind: "cross-cutting-insight"
status: "draft"
last_updated: "2026-09-14"
---

# Bounded Autonomyには階層ごとの上限と停止意味論が必要である

## 中心となる洞察

一回のTool呼出しが小さくても、再試行、並列、子Agent、長時間実行を合算すると、費用・資源・副作用は無制限に
拡大し得る。Agentic Systemでは、Tool、Execution、Swarmの階層ごとに別の上限と停止を設計する。

```text
Per-tool limit
  -> 一つのTool異常を閉じ込める
Per-execution budget
  -> 一連の仕事の再試行・子・並列を合算する
Swarm-wide halt
  -> 動的に増えた全Agentの活動を止め、再開を防ぐ
```

## Timeoutには複数の状態がある

「待つのをやめた」「終了を要求した」「Processが終了した」「下流副作用も止まった」は別である。Clientへ
Timeout Responseを返しても、Server Process、子Process、Queue上のJob、外部API処理が継続すれば、消費と副作用は
残る。

検証では設定値だけでなく、実Process終了、子処理、停止遅延、外部Jobの状態を観測する。

## 一実行の境界を守る

Execution IDやBudgetをModelが書き換え、再試行・子Agent・再開を別の仕事として扱うと上限をResetできる。
親子関係と消費をTrusted Runtimeが管理し、並列処理による同一残額の二重使用を防ぐ。

予算管理が故障したことはN/Aの理由にならない。残額を確認できない場合は新しい消費を拒否する、または
事前予約済みの範囲だけ継続するなど、Fail closedの動作を決める。

## 停止と復旧の衝突

可用性のための自動復旧が、Security上の意図的な停止を解除することがある。Kill-switchでは、停止Request、
各Agentの実停止、群全体の停止完了、停止状態の維持を分ける。Queue再配信、Replica、子Agent、自動再起動で
勝手に復活させない。

> StopはUndoではない。

停止前に送信済みのEmailや完了済み取引は、Agentを止めても元に戻らない。進行中の外部Job、取消可能性、
不可逆な副作用は別の保証として扱う。

## 設計レビューへの応用

- ToolごとにCPU、Memory、Disk、Egress、時間をどの単位で制限するか。
- 一Executionの開始・終了・親子・再試行・再開を定義したか。
- 累積費用、Token、回数、再帰、並列数をどこで合算するか。
- Budgetの確認と消費予約を競合なく行えるか。
- Agent群の全構成員を動的に把握し、停止できるか。
- 停止後の自動復旧、Queue再配信、外部Jobを追ったか。
- 設定上の上限と実測された停止結果を対応付けたか。

## 誤用と限界

- Resource Limitは情報漏えい、認可、不正操作を防ぐ代替策ではない。
- Budget内でも一回の高Impact操作は実行できる。
- Swarm停止は完了済み操作を巻き戻さない。
- 一ExecutionのBudgetは、全User・全SystemのCapacityを保証しない。
- Network分断下の瞬時停止等、保証できない範囲と停止遅延を明記する。

## Slide-ready summary

- 一回が小さいことは、一連の仕事が小さいことを保証しない。
- Tool、Execution、Swarmで異なる上限を持つ。
- Timeout ResponseとProcess終了を分ける。
- 自動復旧にSecurity停止を解除させない。
- StopとUndoを混同しない。

## 起点となった学習記録

- [C9.1.1：Per-tool Quotas](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.1-per-tool-resource-quotas-and-timeouts/learning.md)
- [C9.1.2：Per-execution Budgets](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.2-per-execution-cumulative-budgets/learning.md)
- [C9.1.3：Swarm-wide Halt](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.3-swarm-wide-agent-halt/learning.md)

本書はDoS対策だけでなく、誤動作、費用暴走、再試行、停止後の復活を一つの階層Modelで捉える洞察である。
