---
title: "ツール単位の資源上限と実行期限"
versioned_id: "v1.0-C9.1.1"
requirement_id: "C9.1.1"
verification_level: 1
family_id: "C9"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-01-Execution-Budgets.md"
last_verified: "2026-09-09"
maturity: "verifiable"
mapping_assessment_refs: []
---

# ツール単位の資源上限と実行期限

AISVS Verification Level: 1

初めて読む方へ：[具体例・用語・対話を含む学習ノート](learning.md)。

## Upstream basis

AISVS `v1.0-C9.1.1`を解釈する。要件本文はツールごとのQuotaとTimeoutを強制することを求める。CPU、Memory、Disk、通信、実行時間は例示である。
採用済みstable v1.0の固定Revisionで本文と対応Researchの要件別検証・限界を確認した。
最新の版・製品への追従を意味しない。

Researchは要求の応答期限と処理自体の終了の違い、資源別の強制・計測、他ツールへの影響を補足する。
以下の具体例・Property・検証条件はRepository interpretationである。
Researchの製品、統計、事件、外部Framework Mappingを未検証のまま転記せず、
例示された実装方式を一律の適合条件にしない。

## Interpretation

各ツールが消費できる資源と実行時間を定め、実際の実行基盤で制限する。モデルへの『長く実行しない』という指示や利用量の通知だけでは上限にならない。

画像変換が30秒でTimeoutを返しても、裏で変換Processが走り続けDiskを書き続けるなら時間制限は不成立。上限内の正常な変換は成功し、期限超過時は対象処理の継続と残る副作用を観測する。数値は説明用である。

## Security objective

異常入力・無限処理による資源占有が他の処理や基盤全体へ波及することを抑える。

## Applicability

Agentから呼ぶローカル・遠隔ツールに適用する。共有Worker、子Process、非同期Jobもツールの実行範囲として確認する。

### Non-applicability

ツール実行のない範囲は対象外。管理できない外部SaaSでも、呼出側が制御する同時実行・時間・通信の範囲は残る。外部側のCPU等は責任分界と取得可能な保証を示す。

## Scope and assumptions

Quotaは量の上限、Timeoutは実行期限。資源種別により抑制・拒否・終了の動作と遅延が異なる。原文の例を全環境へ機械的に適用せず、実際に消費する資源の対象外理由を記録する。

対象構成・採用Policy・許容する動作と評価境界を検証前に固定する。
不明な構成を安全と仮定せず、未確認範囲をEvidenceの不足として残す。

## Assets, actors, identities, and trust boundaries

保護対象は計算・記憶・通信資源と他Workload。入力を与えるAgent／攻撃者、ツールWorker、資源管理者を区別する。強制点は実行Scheduler、OS等の制限、または遠隔Jobの実行制御に置き、呼出元の待機だけを止める境界と分ける。

## Required security properties

Security Invariantは守るべき性質、Enforcement Pointはそれを実際に強制する場所を指す。

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | ツールごとに対象資源・上限・超過時動作を特定できる。 |
| SP-2 | 負荷を増やしても設定した制限が実際に働き、計測可能な境界を越えて無制限に消費しない。 |
| SP-3 | 期限後の子処理・背景処理の継続を制御し、Callerの応答終了だけで成功扱いしない。 |

## Scope calibration and adjacent assurance

実行回数の上限だけではCPUやDisk制限を示せない。通信量上限は宛先認可とは別。実行全体の累積予算はC9.1.2で扱う。

## Threat and failure-mode rationale

攻撃者は大きい入力や処理ループを作る入力を与えられる。上限のないツールがMemoryやDiskを使い切り、Timeout後も処理が残ることで他の利用者へ障害を起こす。

この保証の分析では外部脅威IDを付与する追加価値を確定していない。
攻撃者能力・失敗経路を具体化し、`threat_mappings`は空とする。
ResearchのMappingを自動採用せず、必要時に一次Sourceの固定版で別途評価する。

## Verification

### Architecture and configuration review

全ツールの起動設定と実測値を照合し、子Process、外部Job、共有資源、期限伝達、終了確認の経路を追う。

### Positive verification

上限未満の入力を完了させ、結果と使用量を確認する。同じ環境の別ツールも正常に利用できることを確かめる。

### Negative and abuse-case verification

許可された試験環境と模擬Dataを用いる。モデルが協力することに依存せず、
必要に応じて実行境界へ試験要求を直接与える。

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | CPU・Memory・Disk・通信の対象資源を一つずつ超過させる | 定義した抑制・拒否・終了が働く。SP-1, SP-2 |
| N-2 | 期限を超えて動く処理を開始する | 呼出の応答だけでなく実処理の停止・制限が確認できる。SP-3 |
| N-3 | 子Processや非同期Jobを作りCallerをTimeoutさせる | 制限の継承または同等の強制があり、子で無制限に継続しない。SP-2, SP-3 |
| N-4 | 制限設定を欠落させて起動する | 未管理の無制限実行を許さず、明示した安全な既定値または起動拒否となる。SP-1, SP-2 |

### Failure conditions

上表の期待結果に反する観測やSPの不成立は、本ControlのFailを裏付ける。
試験未実施、構成不明、結果を追跡できない場合はPassを裏付ける証拠不足であり、
実証された回避と区別する。隣接要件の不備だけで本Controlの意味を広げない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 資源制限Matrixと有効設定 | 基盤管理者 | 全ツール・子実行 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 上限と強制機構が対応する |
| 負荷・期限試験と計測 | 検証者・基盤 | 各資源と他Workload | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 使用量、終了時刻、残処理から強制を示せる |
| 遠隔実行の責任分界 | System Owner | 委託先を含む実行範囲 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 観測できる停止範囲と未保証範囲を明示する |

成功と失敗の両方について、設定だけでなく実際の結果を採用構成へ対応付ける。
本Repositoryには期待値のみを置き、本番Evidence、Secret、顧客情報は保存しない。
特定の監査製品やログ形式は、本Controlが明示する性質を満たすための唯一の方式ではない。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C9.1.2` | 実行全体の累積予算 |
| `v1.0-C9.3.1` | 権限と実行環境の隔離 |
| `v1.0-C9.1.3` | Agent群全体の停止 |

## Known limitations and uncertainty

共有基盤の競合や外部Jobの取消不能が残る。遅延を測らずに厳密な瞬時停止を主張しない。資源上限が守られても許可内の情報漏えい等は別問題。

`verifiable`は本Artifactに解釈・脅威・検証・証拠期待値が揃った状態を表す。
製品試験の実施・製品適合・学習完了を意味しない。有限の試験で未知の攻撃を全て否定しない。
Engineering PatternとMappingは独立して評価し、その存在を本Controlの成熟条件にしない。

## References

- [AISVS v1.0 C9要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
- [AISVS v1.0 対応Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-01-Execution-Budgets.md)
- [C9全体分析](../../../docs/c09-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-09 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |

