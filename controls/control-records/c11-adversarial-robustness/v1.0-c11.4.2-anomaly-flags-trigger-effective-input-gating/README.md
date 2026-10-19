---
title: 異常Flagを実際の入力通過制御へつなぐ
versioned_id: v1.0-C11.4.2
requirement_id: C11.4.2
verification_level: 2
family_id: C11
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C11-Adversarial-Robustness.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C11-Adversarial-Robustness/C11-04-Model-Runtime-Anomaly-Detection.md
last_verified: '2026-10-19'
maturity: verifiable
mapping_assessment_refs: []
---

# 異常Flagを実際の入力通過制御へつなぐ

AISVS Verification Level: 2

[C11.4 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.4-model-runtime-anomaly-detection.md)

## Upstream basis

AISVS `v1.0-C11.4.2`は、異常とFlagされた入力がGating Actionを発動する。
対応Researchは実経路での検出・制御・識別の試験と、誤検知・見逃しの限界を補足する。特定製品・研究値・手法の全採用を一律のNormative条件にしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

拒否・隔離・保留・追加確認・信頼度に応じた制限等、対象に適した通過制御を定める。単なるTagやLogではなく、Modelや下流処理に渡る扱いが実際に変わることを確認する。特定入力を必ず削除することだけを唯一の方式にはしない。

## Security objective

異常とFlagされた入力がGating Actionを発動する。

## Applicability

対象Modelと公開API、外部入力、または安全性改善Feedbackの実使用経路に適用する。対象・能力・責任分界を以下のSPに合わせて特定する。

### Non-applicability

対象の外部・非信頼入力経路が存在しない場合はData Flowを示す。取得元が社内であるというだけで信頼済みとしない。

## Scope and assumptions

対象Model版、入力・出力・Feedback経路、攻撃者の操作・観測範囲を先に定める。無害な模擬Data・Traceを隔離環境で使い、結果と実動作を対応付ける。誤検知・見逃し・未観測の範囲を明記し、Model自身の説明を強制や証拠の代わりにしない。

## Assets, actors, identities, and trust boundaries

DetectorのFlagからApplication Gate、推論・下流Actionへの境界。資産はContextと実行権限。検知器、Gate、必要に応じたReviewer。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | Flagに対応する対象・条件・Gate措置を定義する。 |
| SP-2 | Flagが実入力と結び付き、定義した措置が実際の通過に作用する。 |
| SP-3 | Retry・Cache・別Routeで制限対象が無処置のまま再投入されず、Gate障害を成功扱いしない。 |

## Scope calibration and adjacent assurance

C11.4.1は検知の配置、本Controlは検知後の制御。Tool操作の最終認可はC5・C9等の決定論的境界で別に評価する。

## Threat and failure-mode rationale

不審文書へFlagを付けても全文を通常どおり投入し、攻撃指示が下流へ到達する。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

拒否・隔離・保留・追加確認・信頼度に応じた制限等、対象に適した通過制御を定める。単なるTagやLogではなく、Modelや下流処理に渡る扱いが実際に変わることを確認する。特定入力を必ず削除することだけを唯一の方式にはしない。 対象版、実際の呼出し順、結果と実消費・措置を照合する。

### Positive verification

正常入力が通常経路を通り、模擬Flag入力は拒否・隔離・確認等の定義した経路へ移ることを実測する。人が確認する経路では判断前の通常投入がないことを確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | Flagだけ付けて元全文を通常経路へ渡す | Gate未実効としてFailにする。SP-2。 |
| N-2 | 同じ入力をRetry・別Routeで再投入する | 対応する制限が継続し迂回しない。SP-3。 |
| N-3 | Gate処理を失敗させる | 措置未完了を記録し正常通過にしない。SP-3。 |

### Failure conditions

Flagが措置を発動しない、記録だけで扱いが変わらない、別経路で迂回する場合はFail。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象Flowと検知・制御・識別の設定 | Model・API・改善基盤担当者 | 本文の対象版・資産と実境界 | 対象・Policy・方式変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの条件と実経路を対応付ける |
| 正例・負例と結果・実行Trace | 検証担当者 | 本文の正常・攻撃・障害経路 | 初回と実装・Model変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 宣言だけでなく成功・拒否・未実効を観測する |

## Related requirements

[C11.4.1](../../../../controls/control-records/c11-adversarial-robustness/v1.0-c11.4.1-anomaly-screening-before-inference-for-untrusted-inputs/README.md)は検知の配置、本Controlは検知後の制御。Tool操作の最終認可はC5・C9等の決定論的境界で別に評価する。
[C11 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

誤Flagは正規利用を妨げる。制限を通過した内容の安全性やすべての攻撃防止を保証せず、誤制限と見逃しを測る。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C11 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C11-Adversarial-Robustness.md)
- [AISVS v1.0 C11.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C11-Adversarial-Robustness/C11-04-Model-Runtime-Anomaly-Detection.md)
- [C11.4 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.4-model-runtime-anomaly-detection.md)
- [C11 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-19 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
