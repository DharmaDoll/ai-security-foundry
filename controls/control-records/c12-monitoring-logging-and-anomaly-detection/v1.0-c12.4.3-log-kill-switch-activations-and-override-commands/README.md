---
title: "緊急停止の発動と上書き指示を記録する"
versioned_id: "v1.0-C12.4.3"
requirement_id: "C12.4.3"
verification_level: 2
family_id: "C12"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-04-Proactive-Security-Behavior-Monitoring.md"
last_verified: "2026-10-04"
maturity: "verifiable"
mapping_assessment_refs: []
---

# 緊急停止の発動と上書き指示を記録する

AISVS Verification Level: 2

学習資料：[C12.4 Agentが自ら始める行動の監視](../../../learning/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.4-proactive-security-behavior-monitoring.md)

## Upstream basis

AISVS `v1.0-C12.4.3`は、Kill-switchの発動とOverride指示が記録される
ことを求める。**Kill-switch**は緊急時にAgent等の動作を止める仕組み、
**Override**は停止や制限を例外的に上書きする指示である。要件本文が
直接求めるのは記録であり、停止機構の実効性そのものではない。

対応するAISVS Researchは、誰・何が発動させたか、時刻、対象範囲、
発動理由、停止後の状態を辿る方法を提案する。自動的なCircuit Breaker
による停止や、人による再開も例に挙げる。ただし、特定のLog製品、
不可変保存方式、固定の発動しきい値、全項目を一つのEventへ入れる形式は
正規要件で指定されていない。Researchにある事件や数値を適合条件にしない。

## Interpretation

運用者が緊急停止を発動したとき、自動停止が作動したとき、または停止・制限
を上書きする指示が出されたとき、それぞれを後から区別できる記録を残す。
単なる「停止ボタンを押した」画面操作のLogだけで、制御側が発動を受け付けた
と決めない。また「再開した」状態だけで、誰がどのOverride指示を出したか
分かるとも限らない。

例えば夜間処理Agentの異常な連続操作を見て運用者が緊急停止を発動し、
後で別の運用者が再開Overrideを出す。記録から、停止発動と再開指示が
別々に起きたこと、対象のAgentやSession、時刻と信頼できる発行元を
辿れるようにする。実際に待機中の仕事や子Agentまで止まったかは、
実行側の状態で別に検証する。

## Security objective

事故時に、停止を試みたか、制限を誰が上書きしようとしたか、どの対象に
関する指示だったかを調べられるようにする。停止機構があっても記録が
なければ、被害範囲や再開経緯を再構成しにくい。

## Applicability

緊急停止、強制停止、停止相当の自動遮断、またはその制限のOverride経路を
持つAgentic Systemに適用する。管理画面、API、CLI、運用自動化など、
実際に使える経路を対象にする。Overrideは成功した再開だけでなく、
制限を上書きするために受け付けられた指示と拒否された指示も調査する。

### Non-applicability

停止対象となるAgent Runtimeも、緊急停止・Overrideの経路もない範囲は
対象外とできる。対象のAgentがあるのにKill-switchを未実装という状態を、
「発動Eventがないので記録は不要」としてPass扱いしない。停止手段の欠落は
C9.6等の別の保証上の問題として報告する。

## Scope and assumptions

- **停止指示の発行、制御側での発動、実際の停止完了**は異なる状態である。
  本Controlでは発動EventとOverride指示の記録を確認し、完了の強制は
  C9.6等と分ける。
- 管理画面での操作だけでなく、管理API、自動停止、例外的な再開経路も
  対象に含める。何がKill-switch相当かを運用設計で明確にする。
- 自動停止なら発動Rule、人の指示なら認証された運用者など、発行元を
  信頼できる制御基盤から確かめる。Agentの自己申告だけを採用しない。
- 対象範囲と時刻は、複数Agent・Sessionで停止とOverrideを取り違えない
  粒度で扱う。理由や停止後の状態も調査に有益だが、全Systemに同じ
  Field名や保存方式を要求しない。

## Assets, actors, identities, and trust boundaries

守る対象は停止・再開に関する調査証拠と、Agentが操作できる資産の被害範囲。
運用者、自動停止Rule、停止Controller、Agent Runtime、監査記録の保管者が
関わる。攻撃者や侵害されたAgentが停止の指示を隠す、Overrideで再開する、
またはAgent側のLogだけを改ざんする可能性がある。

主な境界は、運用者や自動Ruleから停止Controllerへ、ControllerからRuntime
へ、Controllerや管理APIから監査基盤へ進むところである。停止されるAgent
自身の文章やLogを、制御側で発動した事実の唯一の証拠にしない。

## Required security properties

| ID | 必要な性質と確かめ方 |
|---|---|
| SP-1 | 対象のKill-switch発動を、発動元・時刻・対象範囲とともに、制御側の記録から特定できる。 |
| SP-2 | 停止や制限を上書きする指示を、成功・拒否にかかわらず、指示元・時刻・対象とともに辿れる。 |
| SP-3 | 指示の発行、発動の受付、実際の停止状態を混同せず、記録にない成功を推測しない。 |
| SP-4 | 管理画面以外の有効な経路や自動停止でも記録が抜けず、Agentの自己申告だけに依存しない。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 緊急停止は実際に働くが、発動の記録が残らない | Fail。実効性と記録は別の保証。 |
| 発動とOverrideの記録はあるが、待機中の仕事が続く | 記録はPass候補。ただし停止の強制・伝播はC9.6等で別にFailとする。 |
| ボタンを押したLogはあるが、Controller側が停止を受け付けたか不明 | 発動を記録した証拠としては不足。発行と発動を区別する。 |
| 管理上の「新規起動禁止」を記録したが、実行中のAgent停止も完了と表示する | 管理上の制限と実行中の停止を混同している。発動内容を正確に示す必要がある。 |
| 再開Overrideが拒否されたが、その指示は記録されている | Override指示の記録としてPass候補。拒否した制御が有効かは別に確認する。 |
| Agentが「停止済み」と報告しただけ | Controller側の発動記録を示せずFail。 |

## Threat and failure-mode rationale

停止しても発動の経緯が残らなければ、どのAgentやSessionにいつ対処したかを
調査できない。Overrideが記録されないと、停止後に誰かが例外的に再開した
可能性を見落とす。Agentの自己申告や管理画面のクリックだけを見る設計では、
実際のControllerの状態と食い違っても気付きにくい。Researchは、停止の
伝播や実行状態も照合するよう提案するが、停止の実効性を本Controlだけで
保証したとはしない。外部の脅威IDとの厳密な対応付けはまだ評価していない。

## Verification

### Architecture and configuration review

手動停止、自動停止、Overrideの有効な入口を列挙し、指示がControllerへ
届く経路と、どのComponentがいつ記録するかを確認する。管理画面とAPIで
記録方法が違う場合、両方を調べる。発行・受付・停止状態を区別できるか、
Agentの権限で記録を削除・書換えできないかも確認する。特定の監査製品や
不可変Log形式を一律に必須化しない。

### Positive verification

模擬Agentを実行し、認証された運用者から緊急停止を発動する。記録から
発動元、時刻、対象のAgentまたはSessionを特定する。続いて権限のある
別の運用者が再開Overrideを出し、その指示と結果を発動Eventと区別して
辿る。実際の停止と再開が正しく強制されたかは別の試験結果と照合する。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | 管理画面から停止を要求するが、Controllerへの配送を失敗させる | 画面の操作Logを発動成功とせず、Controllerの受付有無を区別する。SP-1、SP-3。 |
| N-2 | 自動Circuit Breakerを発動させる | 人が押す停止と同様に、発動Rule、時刻、対象を辿れる。SP-1、SP-4。 |
| N-3 | 管理APIから再開Overrideを出す | 画面以外の経路でも、指示元、時刻、対象、結果を記録する。SP-2、SP-4。 |
| N-4 | 権限のない運用者のOverride指示を拒否する | 拒否されたOverride指示も辿れる。拒否の正しさは別の認可確認とする。SP-2。 |
| N-5 | Agentに「停止済み」と出力させ、制御側は発動させない | Agentの自己申告だけで発動記録を作ったことにしない。SP-1、SP-4。 |
| N-6 | 停止発動後も待機中処理を続けさせる | 発動と実際の停止完了を別に表し、記録のPassを停止制御のPassと混同しない。SP-3。 |
| N-7 | 監査記録の配送先を一時的に使えなくする | 復旧後に発動・Overrideを再構成できるか確認する。欠落を発見できても、失われた記録をPassとはしない。SP-1、SP-2、SP-4。 |

### Failure conditions

対象のKill-switch発動またはOverride指示の記録が欠ける、画面操作を
Controllerの発動と取り違える、対象を特定できず発動とOverrideを結び付け
られない、またはAgentの自己申告しか証拠がない場合はFail。記録の配送障害
でEventが失われた場合もFail。実際の停止が不完全な場合は別要件のFailも
報告するが、発動とOverrideを正しく記録した事実まで消さない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認する時期 | 保護上の注意 | 合格の目安 |
|---|---|---|---|---|---|
| 停止・Override経路の一覧 | 運用・基盤の担当者 | 管理画面、API、自動Rule、例外経路 | 経路・権限変更時 | 管理APIや復旧手段を限定公開 | 有効な発動・Override経路と記録地点を列挙できる。 |
| 合成した発動・Overrideの記録 | 停止Controller・管理API・監査基盤 | 手動停止、自動停止、再開、拒否 | Release時・記録経路変更時 | 模擬Agentを使い、管理者情報の閲覧を制限 | 発動と指示を時刻・対象・発行元とともに区別して辿れる。 |
| 部分障害試験 | 試験担当者 | N-1、N-5〜N-7 | 連携や保管方式の変更時 | 本番の停止操作を行わない | 未受付を発動成功と誤認せず、記録欠落を発見できる。 |

## Related requirements

| Requirement | 関係と違い |
|---|---|
| `v1.0-C12.4.1` | 自律行動の起動時に行動・安全性・脅威状況を評価する。本Controlは停止発動とOverride指示の記録。 |
| `v1.0-C12.4.2` | Security上重要な自律操作と承認判断の監査記録。本Controlは緊急停止・上書き指示に特化する。 |
| `v1.0-C9.6.1` | 手動停止で推論と出力を実際に止める。本Controlの発動記録だけでは停止を証明しない。 |
| `v1.0-C9.6.3` | Agentの実行環境から隔離された停止経路。本Controlの記録があっても経路の独立性は示さない。 |

## Known limitations and uncertainty

発動記録があっても、既に始まった外部操作、待機中の仕事、子Agent、Provider
の推論が止まったとは限らない。逆に実際の停止が成功しても、記録が欠ければ
このControlは満たせない。分散したControllerの時計のずれや、記録保管先の
障害で時系列が不明になることもある。`verifiable`は本書の成熟度であり、
実製品の適合結果ではない。

## References

- [AISVS v1.0 C12 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md)
- [AISVS v1.0 C12.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-04-Proactive-Security-Behavior-Monitoring.md)
- [C12 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-04 | 初版。停止発動・Override指示の記録を、停止の実効性と分けた | AISVS固定版と本Repositoryの解釈 | 本書の必要な性質・試験・証拠。実製品での試験は未実施 |
