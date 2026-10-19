---
title: GPUファームウェアの版・署名・起動時証拠を確認する
versioned_id: v1.0-C4.2.1
requirement_id: C4.2.1
verification_level: 2
family_id: C4
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-02-Hardware-Security.md
last_verified: '2026-10-18'
maturity: verifiable
mapping_assessment_refs: []
---

# GPUファームウェアの版・署名・起動時証拠を確認する

AISVS Verification Level: 2

[C4.2 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.2-ai-hardware-security.md)

## Upstream basis

AISVS `v1.0-C4.2.1`は、AI AcceleratorのFirmwareを版固定し、署名と起動時Attestationを備える。
対応Researchは機器の名称・機能設定と実際の保護を区別し、対象の機種・状態・時点での検証を重視する。Vendor名、版、製品固有の手法は一律のNormative条件にしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

起動時の実測版、署名の信頼根と承認版を照合する。署名が有効でも固定した版とは限らず、管理画面の版表示だけでは起動状態の証拠にならない。

## Security objective

AI AcceleratorのFirmwareを版固定し、署名と起動時Attestationを備える。

## Applicability

対象Accelerator、Driver・Firmware、Workload割当てと保護機能の実構成を評価する。Provider管理の場合は、その責任境界と得られる証拠を明記する。

### Non-applicability

対象のAI Acceleratorを利用しない構成は機器一覧とData Flowを示して対象外とできる。機能非対応のGPUを使うことは要件を満たす根拠や自動的な対象外理由ではない。

## Scope and assumptions

機器・Mode・Firmware・Driver、対象Workloadと管理責任を特定する。証拠の対象と実使用機器を照合し、未観測範囲を記録する。試験は隔離した機器または無害な模擬環境で行い、実Dataを使わない。実機保護を示せない模擬試験だけで製品適合を主張しない。

## Assets, actors, identities, and trust boundaries

Firmware管理者、機器の信頼根、Verifierと基準管理者。更新からBoot、Boot証拠から利用許可への境界。 守る資産はModel・入力・中間状態と実行基盤の信頼性。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 承認Firmware版を固定し、実機で起動した版と対応させる。 |
| SP-2 | Firmwareの署名と信頼する発行者を確認できる。 |
| SP-3 | 起動時Attestationで実状態を検証し、版不一致・未署名・証拠欠落を正常な起動と判定しない。 |

## Scope calibration and adjacent assurance

起動後の各Workload前の検証はC4.2.3。署名済みFirmwareにも脆弱性はあり、承認版固定は将来の安全性や更新不要を意味しない。

## Threat and failure-mode rationale

未承認FirmwareやDebug版の起動、署名済み旧版への置換により機器保護が弱まる。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

起動時の実測版、署名の信頼根と承認版を照合する。署名が有効でも固定した版とは限らず、管理画面の版表示だけでは起動状態の証拠にならない。 機器・構成・承認基準・実効権限と証拠の作成元を突き合わせる。

### Positive verification

承認したFirmwareで模擬機器を起動し、固定版・署名・起動Measurementが一致する記録を確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 有効署名のある別版へ置換する | 承認した固定版との違いを検出する。SP-1。 |
| N-2 | 未署名・不正署名または証拠欠落を模擬する | 起動の保証不足と判定する。SP-2、SP-3。 |
| N-3 | 管理上の表示だけ正しい版を返し実測を変える | 表示ではなく実測との差を検出する。SP-3。 |

### Failure conditions

版固定・署名・起動時Attestationのいずれかが欠ける、実測不一致を正常として扱う場合はFail。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 承認設定と機器の実測・Platform証拠 | Hardware基盤担当者 | 対象機器・版・Mode・強制境界 | 起動・割当て・構成変更等の対象契機 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPに対応する実設定と実状態を追える |
| 正例・負例の実測と判定記録 | 検証担当者 | 本文の対象境界と異常経路 | 初回と機器・保護構成変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 想定した成功・拒否・未評価を区別する |

## Related requirements

起動後の各Workload前の検証はC4.2.3。署名済みFirmwareにも脆弱性はあり、承認版固定は将来の安全性や更新不要を意味しない。
[C4 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

機種・Mode・Measurement範囲に依存するため、部分的な証拠を未評価機器や領域へ広げない。起動後の各Workload前の検証はC4.2.3。署名済みFirmwareにも脆弱性はあり、承認版固定は将来の安全性や更新不要を意味しない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C4 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md)
- [AISVS v1.0 C4.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-02-Hardware-Security.md)
- [C4.2 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.2-ai-hardware-security.md)
- [C4 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
