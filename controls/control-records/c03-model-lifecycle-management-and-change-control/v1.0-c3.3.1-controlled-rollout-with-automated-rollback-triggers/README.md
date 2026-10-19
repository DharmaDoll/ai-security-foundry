---
title: 本番への展開を制御し自動ロールバックを発動する
versioned_id: v1.0-C3.3.1
requirement_id: C3.3.1
verification_level: 2
family_id: C3
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-03-Controlled-Deployment-Rollback.md
last_verified: '2026-10-18'
maturity: verifiable
mapping_assessment_refs: []
---

# 本番への展開を制御し自動ロールバックを発動する

AISVS Verification Level: 2

[C3.3 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.3-controlled-deployment-and-rollback.md)

## Upstream basis

AISVS `v1.0-C3.3.1`は、本番配備にRolloutの仕組みと自動Rollbackの発動条件を実装する。
ResearchはController設定の存在ではなく、実際のTrafficの切替と異常時の自動復帰を試すことを重視する。特定のControllerや初期配分率・監視指標を一律の必須条件にはしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

本番への展開範囲と切替を制御し、定義した失敗条件が成立すると人のボタン操作を待たずにRollbackする。CanaryやBlue-green等の方式は構成に合わせて選ぶ。失敗条件はHTTP正常だけで安全と誤認しないよう用途のRiskへ対応させるが、特定のModel安全性指標を原文の追加義務として固定しない。

## Security objective

問題のある新版への展開を無制御に拡大せず、検知後の人手待ちによる影響継続を減らす。

## Applicability

本番へModelまたは関連構成を展開し、旧構成から切り替えるDeploymentを対象とする。Controllerが別Serviceでも、切替とRollbackの実際の経路を評価する。

### Non-applicability

本番配備を管理しない境界では、対象Deploymentと責任分界を明示する。Provider委託で内部が見えない場合は、それだけで保証不要とせず証拠不足を残す。

## Scope and assumptions

対象Deployment、Model一式、版、Provider、Registryと実際の読込み経路を評価開始時に特定する。
名前やAliasが可変なら実体の識別方法を明示する。試験は隔離環境の無害な模擬Artifactで行い、
本番Dataや実行可能な不正Payloadを持ち込まない。証拠の対象版と現在の配備が一致するか確認する。

## Assets, actors, identities, and trust boundaries

Release候補から本番Trafficの割当てへ、観測SignalからRollback決定とRoute変更へ進む境界。資産は利用者への応答と配備状態。Release管理者、Controller、Metric提供者、Routerが関わる。誤ったMetricや無効な設定、攻撃者による問題入力から新版の影響が拡大することを想定する。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 本番へのRollout方式・対象・切替条件を定義し、実際の配備とTrafficへ反映する。 |
| SP-2 | 定義した失敗条件が自動Rollbackを起動し、人手の追加操作を待たない。 |
| SP-3 | Rollbackが実際のRoute・配備先へ反映されたことを確認でき、通知や宣言だけで成功扱いしない。 |

## Scope calibration and adjacent assurance

C3.3.2は戻した状態の完全性、C3.3.3は並行版のRuntime状態分離。本Controlの自動復帰だけでは両方を保証しない。C9の停止制御とも目的・対象が異なる。

## Threat and failure-mode rationale

Canaryを展開してAlertは届いても人手まで戻らなければ、問題応答が継続する。Controller設定が実Routeに効かない場合も、制御された展開という前提が崩れる。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

対象Controller、Route、監視入力、条件式、Rollback先と実行Identityを追う。利用Modeで設定が有効か、失敗扱いと判定不能の扱いが定義されるかを確認する。

### Positive verification

模擬新版を本番相当の限定範囲へ展開し、正常条件では予定の切替が進むことを観測する。無害な模擬失敗Signalを発生させ、自動で旧構成へ戻り、新版へのTrafficが停止することを実測する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 異常通知だけを送り手動復帰に設定する | 自動Rollbackの欠落としてFailにする。SP-2。 |
| N-2 | Controllerが無視するModeでRollout設定だけを置く | 実Trafficに反映しないことを検出し、設定の存在を証拠にしない。SP-1、SP-3。 |
| N-3 | 条件成立後のRoute更新を権限不足で失敗させる | Rollback未完了を検知し、Job起動だけで復帰済みとしない。SP-3。 |

### Failure conditions

Rolloutの仕組みがない、自動Rollback条件がない、条件成立時に手動操作を必要とする、実際には戻らない場合はFail。用途と無関係なSignalしか見ない場合は保証Scopeの不足を別途記録する。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| RolloutとRollback設定・Route実測 | 配備基盤担当者 | Controller・失敗条件・実配備先 | 各方式変更とRelease時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 宣言した切替が実際のTrafficへ反映する |
| 自動Rollbackの演習結果 | 検証担当者 | Signal成立から旧版復帰まで | 初回とController・監視変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 人手なしの復帰と未完了検知を観測する |

## Related requirements

[C3.3.2](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.3.2-rollback-restores-complete-model-state/README.md)は戻した状態の完全性、[C3.3.3](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.3.3-parallel-model-version-runtime-state-isolation/README.md)は並行版のRuntime状態分離。本Controlの自動復帰だけでは両方を保証しない。C9の停止制御とも目的・対象が異なる。
[C3 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

自動Rollbackは未知の危険や監視に表れない退行を必ず検知するものではない。旧版も現在の入力で安全とは限らず、検知・伝播・復帰の遅延も残る。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C3 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [AISVS v1.0 C3.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-03-Controlled-Deployment-Rollback.md)
- [C3.3 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.3-controlled-deployment-and-rollback.md)
- [C3 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
