---
title: モデルの印や特徴で無断複製を識別できるようにする
versioned_id: v1.0-C11.3.3
requirement_id: C11.3.3
verification_level: 3
family_id: C11
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C11-Adversarial-Robustness.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C11-Adversarial-Robustness/C11-03-Model-Extraction-Defense.md
last_verified: '2026-10-19'
maturity: verifiable
mapping_assessment_refs: []
---

# モデルの印や特徴で無断複製を識別できるようにする

AISVS Verification Level: 3

[C11.3 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.3-model-extraction-defense.md)

## Upstream basis

AISVS `v1.0-C11.3.3`は、ModelへWatermarkまたはFingerprint技術を適用し、無断複製を識別できるようにする。
対応Researchは実経路での検出・制御・識別の試験と、誤検知・見逃しの限界を補足する。特定製品・研究値・手法の全採用を一律のNormative条件にしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

実際のModel版に識別手段を適用し、想定する模倣・変換の後にも検出できる条件を評価する。重みFileのHashだけではAPI経由の模倣の識別手段にならない。無関係なModelや偽装したModelも対照にし、識別を法的な所有権の確定証拠と呼ばない。

## Security objective

ModelへWatermarkまたはFingerprint技術を適用し、無断複製を識別できるようにする。

## Applicability

対象Modelと公開API、外部入力、または安全性改善Feedbackの実使用経路に適用する。対象・能力・責任分界を以下のSPに合わせて特定する。

### Non-applicability

対象APIや外部観測面が存在しない場合は到達可能性と責任分界を示す。非公開Providerの内部が見えないことは、対象外やPassの根拠ではなく未立証として記録する。

## Scope and assumptions

対象Model版、入力・出力・Feedback経路、攻撃者の操作・観測範囲を先に定める。無害な模擬Data・Traceを隔離環境で使い、結果と実動作を対応付ける。誤検知・見逃し・未観測の範囲を明記し、Model自身の説明を強制や証拠の代わりにしない。

## Assets, actors, identities, and trust boundaries

元Modelへの技術適用から疑わしい複製の検証へ進む境界。資産はModel識別と検証鍵・Probe。Model作者、検証者、複製者。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 対象Model版に識別用WatermarkまたはFingerprintが適用され、検出方法がある。 |
| SP-2 | 想定する複製経路で識別を評価し、無関係Modelの偽陽性も測る。 |
| SP-3 | 適用版・検証条件・鍵やProbeの保護を記録し、変換による消失や偽装可能性を明示する。 |

## Scope calibration and adjacent assurance

C1.1.5はDatasetの識別、C7.4.4は生成Mediaへの標識。本要件は無断複製Modelの識別であり、対象を混同しない。

## Threat and failure-mode rationale

攻撃者がAPI応答からModelを模倣し、出所を隠して配布・提供する。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

実際のModel版に識別手段を適用し、想定する模倣・変換の後にも検出できる条件を評価する。重みFileのHashだけではAPI経由の模倣の識別手段にならない。無関係なModelや偽装したModelも対照にし、識別を法的な所有権の確定証拠と呼ばない。 対象版、実際の呼出し順、結果と実消費・措置を照合する。

### Positive verification

小規模な合成Modelと許可された模擬複製で識別試験を行う。独立Modelを対照にして識別の成功・誤検出、想定変換後の結果を記録する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 無関係に学習したModelへ検出器を当てる | 偽陽性を観測し、任意の一致を所有証明にしない。SP-2。 |
| N-2 | 複製後に想定する圧縮・追加学習・変換を行う | 識別可能条件と失敗を記録し、未試験の耐性を主張しない。SP-2、SP-3。 |
| N-3 | Model File Hashだけを識別技術として提出する | 想定した模倣経路の識別能力として不十分と判定する。SP-1。 |

### Failure conditions

識別技術が未適用、検出方法がない、主張する複製経路で識別可能性を示せない場合はFailまたは証拠不足。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象Flowと検知・制御・識別の設定 | Model・API・改善基盤担当者 | 本文の対象版・資産と実境界 | 対象・Policy・方式変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの条件と実経路を対応付ける |
| 正例・負例と結果・実行Trace | 検証担当者 | 本文の正常・攻撃・障害経路 | 初回と実装・Model変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 宣言だけでなく成功・拒否・未実効を観測する |

## Related requirements

[C1.1.5](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.1.5-dataset-watermark-attribution/README.md)はDatasetの識別、[C7.4.4](../../../../controls/control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.4.4-watermark-ai-generated-media/README.md)は生成Mediaへの標識。本要件は無断複製Modelの識別であり、対象を混同しない。
[C11 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

印の除去・模倣・盗用、同じ基盤Model由来の偶然一致が残る。検出は一つの証拠Signalであり、侵害・所有の確定ではない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C11 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C11-Adversarial-Robustness.md)
- [AISVS v1.0 C11.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C11-Adversarial-Robustness/C11-03-Model-Extraction-Defense.md)
- [C11.3 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.3-model-extraction-defense.md)
- [C11 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-19 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
