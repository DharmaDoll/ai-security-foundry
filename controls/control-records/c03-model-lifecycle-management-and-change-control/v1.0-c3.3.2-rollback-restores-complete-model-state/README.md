---
title: ロールバックでモデルの状態全体を復元する
versioned_id: v1.0-C3.3.2
requirement_id: C3.3.2
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

# ロールバックでモデルの状態全体を復元する

AISVS Verification Level: 2

[C3.3 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.3-controlled-deployment-and-rollback.md)

## Upstream basis

AISVS `v1.0-C3.3.2`は、Rollbackで完全なModel状態を復元できるようにする。
Researchは重みだけでなく設定、Adapter、安全性・Policy Model等の整合した復元を扱う。DeploymentのPod Templateを戻すだけでは、外部保存先や可変Aliasの内容まで戻るとは限らない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

復元対象となる既知のModel状態一式を、構成物と版で定義する。Rollback後にその組合せが実際に読み込まれることを照合する。System Promptや検索Index等が版と強く結び付く構成では、それらを含む整合性も確認する。この追加境界は製品構成に依存するRepository解釈であり、あらゆる外部Dataの巻戻しを一律に義務付けるものではない。

## Security objective

旧重みと新設定の混在等、試験していない組合せを復旧済みと誤認しないようにする。

## Applicability

本番のModel状態を以前の構成へ復元する能力を対象とする。In-place Reload、Adapter切替、Pod再作成等、状態が変わる手段にかかわらず、完全な組合せを戻せるかを確認する。

### Non-applicability

本番配備を管理しない境界では、対象Deploymentと責任分界を明示する。Provider委託で内部が見えない場合は、それだけで保証不要とせず証拠不足を残す。

## Scope and assumptions

対象Deployment、Model一式、版、Provider、Registryと実際の読込み経路を評価開始時に特定する。
名前やAliasが可変なら実体の識別方法を明示する。試験は隔離環境の無害な模擬Artifactで行い、
本番Dataや実行可能な不正Payloadを持ち込まない。証拠の対象版と現在の配備が一致するか確認する。

## Assets, actors, identities, and trust boundaries

問題のある現行状態から既知の復旧状態へ移る境界。資産は重み、Adapterと合成順序、設定、Tokenizer、安全性・Policy Model等の版と依存関係。Release管理者、Store、Registry、Rollback Controller、Loaderが関わる。複数の可変参照や独立した更新経路が部分復旧を生むことを想定する。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 完全なModel状態を構成する対象と版・組合せを特定し、復旧可能な参照または保存物を保持する。 |
| SP-2 | Rollbackが実際の読込み状態を対象の組合せへ戻し、重み以外を新状態のまま残さない。 |
| SP-3 | 途中の混合状態を正常な復旧として供用せず、復元結果の照合が完了するまで状態を区別できる。 |

## Scope calibration and adjacent assurance

C3.3.1は自動発動、C3.3.3は並行状態の分離。本Controlは復元結果の完全性であり、Rollbackが自動かどうかとは別。C3.1.3の読込み時検証は復元経路にも必要な隣接保証。

## Threat and failure-mode rationale

重みを戻してもAdapterや安全性設定が新しいままだと、既知の状態に戻らず、障害・危険応答が続く。複数の独立Storeに状態があるほど、単一のRollout Undoでは不足しやすい。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

復旧Manifest、Registry参照、可変Alias、外部Configと保存物、Reload経路を調べる。何を戻せば完全な状態かを特定し、依存するPromptやIndexの互換性、部分失敗時の挙動を確認する。

### Positive verification

基盤Model・Adapter・設定・安全性Modelを含む模擬構成を新版へ更新してから戻す。復旧後に全構成物の版と組合せを照合し、無害なSmoke試験で対象状態が実際に使われることを確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 重みだけ旧版へ戻し安全性設定を新版に残す | 部分復旧と検出し、完全な復元のPassにしない。SP-2。 |
| N-2 | 外部ConfigやRegistry Aliasの復元を失敗させる | Template復元の成功とModel状態の復元を区別し、混合状態を供用しない。SP-2、SP-3。 |
| N-3 | 旧Artifactを削除した状態でRollbackを発動する | 復元不能を観測し、旧版名の宣言だけで成功にしない。SP-1。 |

### Failure conditions

対象状態一式を特定・保持できない、構成物の一部が新状態のまま、または復元結果を照合できない場合はFailまたは証拠不足。Controllerの完了表示だけを完全復旧の証明としない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 復旧対象Manifestと保持記録 | Release管理者 | 全構成物・版・依存関係 | Releaseと保持方針変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 既知の組合せを取得・復元できる |
| 復元演習と復旧後の照合 | 配備・検証担当者 | 全状態の実読込みと部分失敗 | 初回と復旧経路・構成変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 全構成物が一致し、部分復旧を成功にしない |

## Related requirements

[C3.3.1](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.3.1-controlled-rollout-with-automated-rollback-triggers/README.md)は自動発動、[C3.3.3](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.3.3-parallel-model-version-runtime-state-isolation/README.md)は並行状態の分離。本Controlは復元結果の完全性であり、Rollbackが自動かどうかとは別。[C3.1.3](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.1.3-signature-verification-at-admission-and-load/README.md)の読込み時検証は復元経路にも必要な隣接保証。
[C3 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

状態の復元は既に行われた送信・外部操作や情報開示を取り消さない。旧版に現在の脆弱性があることもあり、完全復元を現在の安全性と同一視しない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C3 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [AISVS v1.0 C3.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-03-Controlled-Deployment-Rollback.md)
- [C3.3 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.3-controlled-deployment-and-rollback.md)
- [C3 Family概要](../README.md)

- [関連Insight：復旧するのはファイルではなく、整合したシステムの状態](../../../../docs/insights/recovery-restores-a-consistent-configuration.md)（Repositoryの横断的な考察。規範やMappingではない）

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
