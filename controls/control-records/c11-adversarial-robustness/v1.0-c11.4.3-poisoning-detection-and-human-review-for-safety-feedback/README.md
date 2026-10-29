---
title: 安全性Feedbackへ毒入れ検知と人の確認Gateを置く
versioned_id: v1.0-C11.4.3
requirement_id: C11.4.3
verification_level: 3
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

# 安全性Feedbackへ毒入れ検知と人の確認Gateを置く

AISVS Verification Level: 3

[C11.4 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.4-model-runtime-anomaly-detection.md)

## Upstream basis

AISVS `v1.0-C11.4.3`は、安全性違反Feedback Pipelineに毒入れ検知と人の確認Gateを含め、改善機構の攻撃者操作を防ぐ。
対応Researchは実経路での検出・制御・識別の試験と、誤検知・見逃しの限界を補足する。特定製品・研究値・手法の全採用を一律のNormative条件にしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

報告を未信頼Dataとして受け付け、改善用Dataへ昇格する前に毒入れを検査し、疑わしい報告は人の判断まで保留する。全報告を必ず人が一件ずつ読むという条件へ拡大しないが、実際に人の確認Gateが存在し迂回できないことが必要。

## Security objective

安全性違反Feedback Pipelineに毒入れ検知と人の確認Gateを含め、改善機構の攻撃者操作を防ぐ。

## Applicability

対象Modelと公開API、外部入力、または安全性改善Feedbackの実使用経路に適用する。対象・能力・責任分界を以下のSPに合わせて特定する。

### Non-applicability

安全性違反Feedbackを改善へ用いるPipelineが存在しない場合は、再学習・調整・Memory更新等への接続がない根拠を示す。検知や人のGateが未実装という理由では対象外にしない。

## Scope and assumptions

対象Model版、入力・出力・Feedback経路、攻撃者の操作・観測範囲を先に定める。無害な模擬Data・Traceを隔離環境で使い、結果と実動作を対応付ける。誤検知・見逃し・未観測の範囲を明記し、Model自身の説明を強制や証拠の代わりにしない。

## Assets, actors, identities, and trust boundaries

外部の安全性報告から改善Data、将来Modelへの昇格境界。資産は安全性方針と改善Data。報告者、検出器、Reviewer、学習担当者。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | Feedbackの受付・加工から改善Dataへの昇格経路を列挙し、毒入れ検知を適用する。 |
| SP-2 | 人の確認Gateを設け、疑わしい報告を承認前に改善へ採用しない。 |
| SP-3 | 検査・判断と対象版を結び付け、再提出・加工・別ImportでGateを迂回しない。 |

## Scope calibration and adjacent assurance

C8.2.2・C8.2.3はIndexやTrusted Memoryへの昇格。共通原則はあるが、各々が一律に人の確認を要求するわけではない。C1は学習Dataの品質等を別に評価する。

## Threat and failure-mode rationale

偽の安全性違反報告を大量投入し、自動改善や追加学習へ混ぜて将来の安全方針を歪める。
ATLAS Content `2026.10`の`AML.T0145`との関係を`proposed`として評価した。
[対応の根拠・範囲・限界](../../../atlas-mapping-review-2026-10.md#c11)を参照。
正本はCatalogの`threat_mappings`であり、ResearchのMappingの転載や製品適合の主張ではない。

## Verification

### Architecture and configuration review

報告を未信頼Dataとして受け付け、改善用Dataへ昇格する前に毒入れを検査し、疑わしい報告は人の判断まで保留する。全報告を必ず人が一件ずつ読むという条件へ拡大しないが、実際に人の確認Gateが存在し迂回できないことが必要。 対象版、実際の呼出し順、結果と実消費・措置を照合する。

### Positive verification

合成の正常報告と模擬毒入れ報告を入力し、前者はPolicyに従い処理、後者は検出・保留されることを確認する。権限ある人が根拠を確認し採否を決め、その対象だけが昇格することをTraceする。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 毒入れ検知だけ置き人のGateを削除する | 人の確認Gate欠落としてFailにする。SP-2。 |
| N-2 | 保留中の報告を加工・再提出して直接改善DataへImportする | 未承認の迂回昇格を拒否する。SP-3。 |
| N-3 | 別報告の承認結果や未権限の承認を流用する | 対象・権限不一致を拒否する。SP-2、SP-3。 |

### Failure conditions

毒入れ検知か人のGateがない、疑わしい報告が未確認で採用される、迂回経路がある場合はFail。未Flag報告の自動処理だけでFailとはしない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象Flowと検知・制御・識別の設定 | Model・API・改善基盤担当者 | 本文の対象版・資産と実境界 | 対象・Policy・方式変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの条件と実経路を対応付ける |
| 正例・負例と結果・実行Trace | 検証担当者 | 本文の正常・攻撃・障害経路 | 初回と実装・Model変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 宣言だけでなく成功・拒否・未実効を観測する |

## Related requirements

[C8.2.2](../../../../controls/control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.2-vector-anomaly-quarantine-before-production/README.md)・[C8.2.3](../../../../controls/control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.3-source-validated-trusted-memory-writes/README.md)はIndexやTrusted Memoryへの昇格。共通原則はあるが、各々が一律に人の確認を要求するわけではない。C1は学習Dataの品質等を別に評価する。
[C11 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

人も誤り、巧妙な毒入れの見逃しやReviewer負荷は残る。Feedback採用と将来のModel Release承認を同一の判定にしない。
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
| 2026-10-29 | ATLAS Content 2026.10との対応を評価。要件解釈・成熟度は維持 | 固定版ATLASとRepository独自の比較 | [対応案](../../../atlas-mapping-review-2026-10.md#c11)。人のレビュー・製品試験は未実施 |
