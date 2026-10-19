---
title: GPUメモリを分割しジョブ間で残留情報を消去する
versioned_id: v1.0-C4.2.4
requirement_id: C4.2.4
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

# GPUメモリを分割しジョブ間で残留情報を消去する

AISVS Verification Level: 3

[C4.2 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.2-ai-hardware-security.md)

## Upstream basis

AISVS `v1.0-C4.2.4`は、PartitioningでWorkload間のGPUメモリを隔離し、Job間でメモリをSanitizeする。
対応Researchは機器の名称・機能設定と実際の保護を区別し、対象の機種・状態・時点での検証を重視する。Vendor名、版、製品固有の手法は一律のNormative条件にしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

同時利用者への分離と次利用者への引渡しを独立に確認する。Memory Freeは消去の証明ではなく、PartitionやProcessが変わっても残存Dataを再取得できないことを確かめる。

## Security objective

PartitioningでWorkload間のGPUメモリを隔離し、Job間でメモリをSanitizeする。

## Applicability

対象Accelerator、Driver・Firmware、Workload割当てと保護機能の実構成を評価する。Provider管理の場合は、その責任境界と得られる証拠を明記する。

### Non-applicability

対象のAI Acceleratorを利用しない構成は機器一覧とData Flowを示して対象外とできる。機能非対応のGPUを使うことは要件を満たす根拠や自動的な対象外理由ではない。

## Scope and assumptions

機器・Mode・Firmware・Driver、対象Workloadと管理責任を特定する。証拠の対象と実使用機器を照合し、未観測範囲を記録する。試験は隔離した機器または無害な模擬環境で行い、実Dataを使わない。実機保護を示せない模擬試験だけで製品適合を主張しない。

## Assets, actors, identities, and trust boundaries

Scheduler、GPU Driver、Partition管理、Job実行者。隣接Partition間と前利用者から次利用者への二つの境界。 守る資産はModel・入力・中間状態と実行基盤の信頼性。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 実行中のWorkload間でMemory Partition境界が強制され、他Partitionへアクセスできない。 |
| SP-2 | Job終了・切替時に対象メモリをSanitizeし、次のJobへ前利用者の内容を残さない。 |
| SP-3 | 異常終了・再割当て・再起動経路でも分離と引渡し処理が適用され、消去未完了を再利用可能としない。 |

## Scope calibration and adjacent assurance

C4.2.2の暗号化・完全性とは別の保証。Markerが見つからない一回の結果だけでは全領域の消去を証明せず、Allocator・Deviceの証拠を組み合わせる。

## Threat and failure-mode rationale

隣接Jobが他者メモリを読み、または終了後に前のJobの重みや入力断片を回収する。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

同時利用者への分離と次利用者への引渡しを独立に確認する。Memory Freeは消去の証明ではなく、PartitionやProcessが変わっても残存Dataを再取得できないことを確かめる。 機器・構成・承認基準・実効権限と証拠の作成元を突き合わせる。

### Positive verification

AとBを同時に実行し、別々の合成Markerを使って相互アクセスを拒否する。A終了後にCへ再割当てし、AのMarkerが残っていないことを対象メモリ種別ごとに試す。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 他PartitionのMemoryをPeer／IPC経路から要求する | 定義したPartition境界で拒否する。SP-1。 |
| N-2 | Jobを異常終了させ同じ領域を再割当てする | 次Jobが旧Markerを取得できず、消去手順の実行を確認する。SP-2、SP-3。 |
| N-3 | 消去を遅延・失敗させる | 完了前に次Jobへ領域を引き渡さない。SP-3。 |

### Failure conditions

同時Job間のアクセスが可能、前Jobの内容を次Jobが取得可能、異常終了時に消去を飛ばす場合はFail。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 承認設定と機器の実測・Platform証拠 | Hardware基盤担当者 | 対象機器・版・Mode・強制境界 | 起動・割当て・構成変更等の対象契機 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPに対応する実設定と実状態を追える |
| 正例・負例の実測と判定記録 | 検証担当者 | 本文の対象境界と異常経路 | 初回と機器・保護構成変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 想定した成功・拒否・未評価を区別する |

## Related requirements

[C4.2.2](../../../../controls/control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.2.2-tee-hardware-isolation-encryption-and-integrity/README.md)の暗号化・完全性とは別の保証。Markerが見つからない一回の結果だけでは全領域の消去を証明せず、Allocator・Deviceの証拠を組み合わせる。
[C4 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

機種・Mode・Measurement範囲に依存するため、部分的な証拠を未評価機器や領域へ広げない。C4.2.2の暗号化・完全性とは別の保証。Markerが見つからない一回の結果だけでは全領域の消去を証明せず、Allocator・Deviceの証拠を組み合わせる。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C4 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md)
- [AISVS v1.0 C4.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-02-Hardware-Security.md)
- [C4.2 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.2-ai-hardware-security.md)
- [C4 Family概要](../README.md)

- [関連Insight：共有資源の再利用は、次の利用者への安全な引渡しである](../../../../docs/insights/resource-reuse-is-a-security-handoff.md)（横断的な考察。規範やMappingではない）

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
