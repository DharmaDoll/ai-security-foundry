# AISVS C9 学習ガイド

C9ではAgentが許可された、意図された、制限された行動を実行するための保証を学ぶ。
[共通学習方針](../README.md)に従い、原則として章の順番に、一度に一要件ずつ進める。
全体の保証範囲・ID・Levelは[章の分析](../../c09-landscape.md)と
[Control一覧](../../../README.md#c9-control-records)を参照する。

## 現在位置

C9.1の全3要件とC9.2.1・C9.2.2の講義・対話を一巡して保存した。現在学習中の要件はなし。
次はC9.2.3（高影響操作の可逆性の分類）。学習進捗はControl成熟度・製品適合とは独立している。

## 一巡のチェックリスト

- [x] [C9.1.1：ツールごとの資源上限と実行期限](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.1-per-tool-resource-quotas-and-timeouts/learning.md)
- [x] [C9.1.2：実行全体の累積予算](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.2-per-execution-cumulative-budgets/learning.md)
- [x] [C9.1.3：Agent群全体の停止](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.3-swarm-wide-agent-halt/learning.md)
- [x] [C9.2.1：高影響操作への人の承認](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.1-human-approval-before-high-impact-actions/learning.md)
- [x] [C9.2.2：承認対象の完全・正確な表示](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.2-complete-canonical-approval-display/learning.md)
- [ ] C9.2.3
- [ ] C9.2.4
- [ ] C9.2.5
- [ ] C9.2.6
- [ ] C9.2.7
- [ ] C9.2.8
- [ ] C9.2.9
- [ ] C9.2.10
- [ ] C9.3.1
- [ ] C9.3.2
- [ ] C9.3.3
- [ ] C9.3.4
- [ ] C9.3.5
- [ ] C9.3.6
- [ ] C9.3.7
- [ ] C9.3.8
- [ ] C9.4.1
- [ ] C9.4.2
- [ ] C9.4.3
- [ ] C9.4.4
- [ ] C9.5.1
- [ ] C9.5.2
- [ ] C9.5.3
- [ ] C9.5.4
- [ ] C9.5.5
- [ ] C9.5.6
- [ ] C9.6.1
- [ ] C9.6.2
- [ ] C9.6.3

## Sources

採用済みAISVS v1.0、固定Revision `78775233666a2022dcfb82037e5e029116955c00`。

- [C9要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
- [C9 Research章概要](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-Orchestration-and-Agents.md)
- [C9.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-01-Execution-Budgets.md)
- [C9.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-02-High-Impact-Action-Approval.md)
