# C9.3.8：Policy違反時にToolを自動的に封じ込める

AISVS Verification Level: 3

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.3.8`。採用済み固定Revisionは
`78775233666a2022dcfb82037e5e029116955c00`。

> Verify that policy violations trigger automated tool containment.

日本語訳：Policy違反が発生した場合に、Toolの自動的な封じ込めが起動することを確認する。
[要件本文][normative]

Normativeは要件本文、Researchは補足である。段階的な封じ込め、残存Capability、Level 3の理由は
Repository interpretation、対話からの整理は学習上の洞察である。学習完了はControl成熟度や製品適合を変更しない。

## 平易な説明

Toolが禁止された操作を試みたとき、該当Requestを拒否してLogへ残すだけでは、侵害されたToolが別経路、別Job、
再試行によって被害を続けられる。Runtimeは定義した違反条件に応じ、Toolの追加行動を自動的に制限・停止する。

```text
Policy違反を検出
  ↓
改ざんされにくい違反Signal
  ↓
Toolの実行・通信・Credential・Job受付を制限
  ↓
調査と安全な復旧
```

**危険なToolを発見できることではなく、発見後に行動を続けられないことを保証する。**

## Policy EnforcementとContainmentを分ける

一回の禁止Requestを拒否することはPolicy Enforcementである。C9.3.8は、それに加えて違反したToolの残存Capabilityを
自動的に縮小することを問う。

```text
Policy Enforcement
  今回の禁止操作を通さない

Automated containment
  違反後の追加操作・再試行・再起動・Credential利用を制限する
```

AlertやSIEMへの通知だけもContainmentではない。通知から自動Responseが起動し、Process、Network、Credential、
Queue、Registry等へ実制御が到達する必要がある。

## 対象はToolである

C9.3.8の直接の対象は、違反したToolの封じ込めであり、Agent全体や正常なToolの停止ではない。正常なToolまで
無条件に停止すると、Blast RadiusではなくAvailabilityへの影響を広げる。

```text
Agent
  ├─ 正常Tool A      → 継続可能
  ├─ 違反Tool B      → 隔離・停止
  └─ 正常Tool C      → 継続可能
```

ただしAgentが同じToolを再起動、再登録、別Instanceとして複製できるなら、その経路は封じ込め対象に含める。
Agent全体を停止しなくても、Tool ID、Version／Digest、Instance、Credential、新規Job、再登録・再起動を必要な粒度で
拒否する。

## Trust BoundaryとSecurity Invariant

```text
Agent／Tool
  ↓ 操作要求
Policy Enforcement Point
  ├─ Allow → Tool実行
  └─ Deny＋違反判定
          ↓
Containment Controller
  ↓
Process・Network・Credential・Registry・Queueを制限
```

Tool自身に停止を任せない。侵害されたToolは自己申告を止め、停止要求を無視できる。Security Invariantは、
ToolがPolicyに違反した場合、Tool自身の協力なしに、追加の副作用を起こせる能力を定義時間内に遮断できることである。

決定論的なEnforcement Pointには、Process／Container Supervisor、MCP／API Gateway、Egress Proxy、Credential Broker、
Orchestrator、Tool Registry等がある。製品名ではなく、実際に能力を止められるかで評価する。

## 違反に応じた段階的Response

全ての軽微なDenyでToolを永久停止すると、攻撃者が意図的に違反を発生させて可用性を奪える。そのため、対象Policy、
違反の重大度、回数、封じ込め処置、解除条件を事前に対応付ける。

```text
軽微な単発違反
  Request拒否、記録、監視強化

反復・疑わしい違反
  Rate limit、権限降格、新規Job停止、一時隔離

重大な違反
  Process停止、Network遮断、Credential失効、再起動禁止

復旧
  調査、再承認、既知の安全なVersionへの交換
```

単発の通常Denyと「侵害を疑いContainmentを起動するPolicy違反」の境界を明示する。重大な違反をAlertだけで済ませない。

## 残存Capabilityを回収する

Containerを終了しても、次が残れば封じ込めは迂回される。

- 長寿命CredentialとSession
- 非同期Queueに残るJob
- 進行中の外部処理
- Retry、Fallback、別Worker
- 同じToolの新Instance
- 再登録・自動復旧機構
- 共有File、Database、Cacheに置かれた実行要求

停止対象はProcess名ではなく、違反Toolが副作用を起こすためのCapability graphで考える。

## 実装コストとLevel 3

この要件は単一のPolicy Engineだけでは完成しない。

```text
違反検出
  -> 信頼できるSignal伝達
  -> 分散したCapabilityの封じ込め
  -> 復活経路の遮断
  -> 調査
  -> 安全な解除
```

実装・運用上の難所は次のとおりである。

- 誤検知によるAvailability Risk
- 分散Systemで封じ込めが完了するまでのRace
- Process停止後にも残るCredential、Session、Job
- ToolのLogや自己申告を信頼できないこと
- 自動復旧が攻撃者の再起動経路になること
- 高権限なContainment Controller自体の保護
- 実際の停止範囲と遅延を継続的に試験する必要

このようにDetection、Runtime Control、Credential、Orchestration、Incident Responseを横断する成熟が必要であることは、
Verification Level 3を理解する実務的な理由になる。ただしLevelの正式な決定理由をRepositoryが断定するものではない。

> Toolの自動封じ込めは、一つのSecurity機能ではなく、Runtime全体にまたがるIncident Responseである。

## 隣接Requirementとの違い

- C9.1は、時間、回数、費用等のBudget超過を防ぐ。
- C9.3.8は、ToolのPolicy違反を契機に該当ToolのCapabilityを自動的に封じる。
- C9.6は、人がSystemやModelを停止できる経路と安全な停止を扱う。

同じCircuit BreakerやOrchestratorを利用できても、保証する失敗条件は異なる。

## 検証と対話の再構成

**問い：Toolが許可外Domainへ通信した。Egress Proxyは通信を拒否しAlertを出したが、ToolはFile読取り、別Job、
再試行を継続できる。適合するか。**

学習者：「Yes」

整理：Failである。一回の通信拒否はPolicy Enforcementであり、残存Capabilityの自動的な縮小がない。Alertも
実制御へ到達しなければContainmentにならない。

**問い：許可外通信を三回検出すると、新規Job停止、Egress全面遮断、Credential失効、Process終了、再承認までの
再起動禁止を自動実行する。正常な他Toolは継続する。適合するか。**

学習者：「Pass。Toolの実行は縮小している。この要件はAgentには言及していない。実装Costは高い」

整理：そのとおり。違反Toolを実効的に封じ、正常Toolを不必要に止めない。Agent全体の停止は直接要件ではない。
ただし同じToolをAgentが再生成できるなら、その復活経路も拒否する必要がある。

**問い：違反後にTool Containerだけを終了するが、24時間有効なCredential、非同期Job、即時再起動経路が残り、
新Instanceが同じCredentialを利用できる。適合するか。**

学習者：「Fail」

整理：そのとおり。Processを止めてもCapabilityは残っている。Credential、Queue、再起動等を含む実際の副作用経路を
遮断しなければならない。

## Negative Test

- 模擬Policy違反を発生させ、人の介入前に定義したContainmentが起動することを確認する。
- 封じ込め後に同じTool、別Instance、別Workerから再試行し、隔離が維持されることを確認する。
- Container停止後にCredential、Session、非同期Job、共有Queueを利用し、副作用を継続できないことを確認する。
- 自動再起動・再登録・Fallbackで未確認の正常状態へ戻れないことを確認する。
- Containment APIの遅延・障害時に成功と偽らず、安全な代替制限を適用することを確認する。
- 軽微な違反を意図的に発生させ、過剰な全体停止によるDoSを起こせないことを確認する。

## 洞察と設計レビューへの問い

- 通常のDenyとContainmentを起動するPolicy違反をどう区別するか。
- AlertからProcess、Network、Credential、Queueへの実制御が本当に接続されているか。
- Tool停止後に残るCapabilityと進行中の副作用は何か。
- Agentが同じToolを別Instanceとして復活させられないか。
- 正常Toolまで止める範囲過大と、危険なCapabilityを残す範囲不足をどう避けるか。
- 解除を誰が承認し、どのEvidenceで安全性を確認するか。
- Containment Controller自体の権限と可用性をどう保護するか。

## References

- [AISVS v1.0 C9.3.8][normative]
- [対応Research][research]
- [C9 Family overview](../README.md)
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-03-Tool-and-Plugin-Isolation.md
