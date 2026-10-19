---
title: 質問Patternの分析結果をモデル抽出検知へ渡す
versioned_id: v1.0-C11.3.1
requirement_id: C11.3.1
verification_level: 1
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

# 質問Patternの分析結果をモデル抽出検知へ渡す

AISVS Verification Level: 1

[C11.3 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.3-model-extraction-defense.md)

## Upstream basis

AISVS `v1.0-C11.3.1`は、Query-pattern Analysisが抽出試行の検知器へ入力される。
対応Researchは実経路での検出・制御・識別の試験と、誤検知・見逃しの限界を補足する。特定製品・研究値・手法の全採用を一律のNormative条件にしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

質問の内容・順序・類似性・分布等、対象Modelに関係するPatternを分析し、実際の検知器が消費する。回数CounterやLog保存だけで分析と検知の接続を示したとはしない。複数主体の相関が必要なThreat Modelなら、その観測範囲とPrivacy制約を明示する。

## Security objective

Query-pattern Analysisが抽出試行の検知器へ入力される。

## Applicability

対象Modelと公開API、外部入力、または安全性改善Feedbackの実使用経路に適用する。対象・能力・責任分界を以下のSPに合わせて特定する。

### Non-applicability

対象APIや外部観測面が存在しない場合は到達可能性と責任分界を示す。非公開Providerの内部が見えないことは、対象外やPassの根拠ではなく未立証として記録する。

## Scope and assumptions

対象Model版、入力・出力・Feedback経路、攻撃者の操作・観測範囲を先に定める。無害な模擬Data・Traceを隔離環境で使い、結果と実動作を対応付ける。誤検知・見逃し・未観測の範囲を明記し、Model自身の説明を強制や証拠の代わりにしない。

## Assets, actors, identities, and trust boundaries

API質問からPattern分析、検知器への境界。資産はModel能力と利用記録。API運用者、分析者、検知器、質問可能な攻撃者。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 対象の抽出Threat Modelに対応したQuery-pattern特徴を定義し分析する。 |
| SP-2 | 分析結果を抽出試行の検知器が実際に使う。 |
| SP-3 | 模擬Patternと正常利用で検知結果を観測し、未入力・欠測を正常と誤認しない。 |

## Scope calibration and adjacent assurance

C11.2.2は質問量の制限、C11.3.4は検知後の対応。本要件の検知から措置の実行までを自動的に保証しない。

## Threat and failure-mode rationale

攻撃者が計画的な質問と応答を収集して模倣Modelを作り、汎用利用量監視だけを迂回する。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

質問の内容・順序・類似性・分布等、対象Modelに関係するPatternを分析し、実際の検知器が消費する。回数CounterやLog保存だけで分析と検知の接続を示したとはしない。複数主体の相関が必要なThreat Modelなら、その観測範囲とPrivacy制約を明示する。 対象版、実際の呼出し順、結果と実消費・措置を照合する。

### Positive verification

無害な通常質問列と模擬抽出質問列を入力し、特徴生成から検知器の結果までTraceする。単純な高負荷の正常例も用いて誤検出を記録する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 同数Requestで順序・類似性だけを変える | 定義したPattern特徴が検知器へ渡ることを確認する。SP-1、SP-2。 |
| N-2 | 特徴生成を切り離しLogだけ残す | 検知器への未接続を検出する。SP-2。 |
| N-3 | 分析Jobの欠測・障害を模擬する | 正常Patternと区別し、検知実行済みとしない。SP-3。 |

### Failure conditions

Pattern分析がない、検知器が結果を使わない、Request数だけを抽出分析と呼ぶ場合はFail。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象Flowと検知・制御・識別の設定 | Model・API・改善基盤担当者 | 本文の対象版・資産と実境界 | 対象・Policy・方式変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの条件と実経路を対応付ける |
| 正例・負例と結果・実行Trace | 検証担当者 | 本文の正常・攻撃・障害経路 | 初回と実装・Model変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 宣言だけでなく成功・拒否・未実効を観測する |

## Related requirements

[C11.2.2](../../../../controls/control-records/c11-adversarial-robustness/v1.0-c11.2.2-principal-and-global-inference-limits-for-extraction-threat/README.md)は質問量の制限、[C11.3.4](../../../../controls/control-records/c11-adversarial-robustness/v1.0-c11.3.4-suspected-extraction-detection-triggers-response/README.md)は検知後の対応。本要件の検知から措置の実行までを自動的に保証しない。
[C11 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

低速・分散・正常質問に似た抽出を見逃し得る。相関のための識別Dataも最小化し、検知精度と誤検出を記録する。
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
