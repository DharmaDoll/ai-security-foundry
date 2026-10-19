---
title: TEEの隔離・メモリ暗号化・完全性を別々に検証する
versioned_id: v1.0-C4.2.2
requirement_id: C4.2.2
verification_level: 3
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

# TEEの隔離・メモリ暗号化・完全性を別々に検証する

AISVS Verification Level: 3

[C4.2 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.2-ai-hardware-security.md)

## Upstream basis

AISVS `v1.0-C4.2.2`は、TEE内の実行が、ハードウェア強制の隔離、メモリ暗号化、完全性保護を提供する。
対応Researchは機器の名称・機能設定と実際の保護を区別し、対象の機種・状態・時点での検証を重視する。Vendor名、版、製品固有の手法は一律のNormative条件にしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

三つの性質を機種・Mode・設定ごとに確認する。通信Bufferの暗号化をDevice常駐メモリの暗号化と混同せず、Confidential Computingという名称だけで三つすべてを推定しない。

## Security objective

TEE内の実行が、ハードウェア強制の隔離、メモリ暗号化、完全性保護を提供する。

## Applicability

対象Accelerator、Driver・Firmware、Workload割当てと保護機能の実構成を評価する。Provider管理の場合は、その責任境界と得られる証拠を明記する。

### Non-applicability

TEE内で実行しない構成では適用Scopeを明示し、この要件の三性質を満たしたと主張しない。TEE機能名があっても暗号化等が欠ければ本要件のPassにはしない。

## Scope and assumptions

機器・Mode・Firmware・Driver、対象Workloadと管理責任を特定する。証拠の対象と実使用機器を照合し、未観測範囲を記録する。試験は隔離した機器または無害な模擬環境で行い、実Dataを使わない。実機保護を示せない模擬試験だけで製品適合を主張しない。

## Assets, actors, identities, and trust boundaries

Host／Hypervisor、TEE内アプリ、Device、FirmwareとVerifier。外側から保護実行メモリへ進む境界。 守る資産はModel・入力・中間状態と実行基盤の信頼性。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 実行境界がハードウェアによって外側主体から隔離される。 |
| SP-2 | 対象の実行メモリが暗号化され、通信時の暗号化だけで代替しない。 |
| SP-3 | 対象メモリ・実行状態への不正変更に対する完全性保護が有効である。 |

## Scope calibration and adjacent assurance

メモリ消去はC4.2.4の残留対策でありメモリ暗号化の代替ではない。TEE内部の侵害やSide Channelは別に残る。

## Threat and failure-mode rationale

Host管理者や侵害されたHypervisorが、実行中の重み・入力を読んだり変更したりする。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

三つの性質を機種・Mode・設定ごとに確認する。通信Bufferの暗号化をDevice常駐メモリの暗号化と混同せず、Confidential Computingという名称だけで三つすべてを推定しない。 機器・構成・承認基準・実効権限と証拠の作成元を突き合わせる。

### Positive verification

実配備の機種・Mode・設定とPlatform証拠から三つの性質を各々確認する。合成Markerを内部で使い、Scope内の外側主体からの読出し・変更が保護されることを試験する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | メモリ暗号化だけを無効にした構成を評価する | 隔離と完全性があっても本要件は満たさない。SP-2。 |
| N-2 | 通信暗号化の結果だけを提出する | 常駐メモリの暗号化の証拠として不足と判定する。SP-2。 |
| N-3 | Debug Modeや外側からの変更経路を有効にする | 主張する隔離・完全性の欠落を検出する。SP-1、SP-3。 |

### Failure conditions

三性質のいずれかが存在しない・無効・立証不能ならFailまたは証拠不足。TEE名やCC Modeの表示だけではPassにしない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 承認設定と機器の実測・Platform証拠 | Hardware基盤担当者 | 対象機器・版・Mode・強制境界 | 起動・割当て・構成変更等の対象契機 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPに対応する実設定と実状態を追える |
| 正例・負例の実測と判定記録 | 検証担当者 | 本文の対象境界と異常経路 | 初回と機器・保護構成変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 想定した成功・拒否・未評価を区別する |

## Related requirements

メモリ消去はC4.2.4の残留対策でありメモリ暗号化の代替ではない。TEE内部の侵害やSide Channelは別に残る。
[C4 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

機種・Mode・Measurement範囲に依存するため、部分的な証拠を未評価機器や領域へ広げない。メモリ消去はC4.2.4の残留対策でありメモリ暗号化の代替ではない。TEE内部の侵害やSide Channelは別に残る。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C4 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md)
- [AISVS v1.0 C4.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-02-Hardware-Security.md)
- [C4.2 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.2-ai-hardware-security.md)
- [C4 Family概要](../README.md)

- [関連Insight：隔離は、誰から誰を守るかで意味が変わる](../../../../docs/insights/isolation-has-a-direction.md)（横断的な考察。規範やMappingではない）

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
