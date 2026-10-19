---
title: 外部・非信頼入力を推論前の異常検知へ通す
versioned_id: v1.0-C11.4.1
requirement_id: C11.4.1
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

# 外部・非信頼入力を推論前の異常検知へ通す

AISVS Verification Level: 2

[C11.4 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.4-model-runtime-anomaly-detection.md)

## Upstream basis

AISVS `v1.0-C11.4.1`は、外部または非信頼Sourceの入力をModel推論前にAnomaly Detectionへ通す。
対応Researchは実経路での検出・制御・識別の試験と、誤検知・見逃しの限界を補足する。特定製品・研究値・手法の全採用を一律のNormative条件にしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

User入力だけでなくWeb、RAG、Tool／MCP応答、Memory等の実使用経路を列挙する。加工・再取得後の実Payloadが検査対象と対応するか確認する。異常判定のFlagと、その後の通過制御は別の保証として扱う。

## Security objective

外部または非信頼Sourceの入力をModel推論前にAnomaly Detectionへ通す。

## Applicability

対象Modelと公開API、外部入力、または安全性改善Feedbackの実使用経路に適用する。対象・能力・責任分界を以下のSPに合わせて特定する。

### Non-applicability

対象の外部・非信頼入力経路が存在しない場合はData Flowを示す。取得元が社内であるというだけで信頼済みとしない。

## Scope and assumptions

対象Model版、入力・出力・Feedback経路、攻撃者の操作・観測範囲を先に定める。無害な模擬Data・Traceを隔離環境で使い、結果と実動作を対応付ける。誤検知・見逃し・未観測の範囲を明記し、Model自身の説明を強制や証拠の代わりにしない。

## Assets, actors, identities, and trust boundaries

外部SourceからContext組立て、検知から推論へ進む境界。資産はModel判断と下流権限。取得者、検知器、Context Builder、推論者。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 使用する外部・非信頼入力経路と実Payloadを列挙する。 |
| SP-2 | 各経路の実入力を推論前に異常検知へ通す。 |
| SP-3 | 加工・Retry・Fallback・検知器障害で未検査状態を検査済み正常へ読み替えない。 |

## Scope calibration and adjacent assurance

C11.4.2はFlag後のGate。事前検知が動いていてもFlagを無視して通すならそちらがFail。C2の形式・内容検証ともScopeを分ける。

## Threat and failure-mode rationale

外部文書やTool応答を攻撃者が操作し、未検査の経路からModel Contextへ指示を持ち込む。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

User入力だけでなくWeb、RAG、Tool／MCP応答、Memory等の実使用経路を列挙する。加工・再取得後の実Payloadが検査対象と対応するか確認する。異常判定のFlagと、その後の通過制御は別の保証として扱う。 対象版、実際の呼出し順、結果と実消費・措置を照合する。

### Positive verification

各入力経路の合成正常例と模擬異常例を通し、検知時点が推論より前で、実Payloadに判定が結び付くことをTraceする。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | RAGだけ検査しTool応答を直接Contextへ入れる | 未検査経路を検出しFailとする。SP-1、SP-2。 |
| N-2 | 検査後にChunkや取得結果を差し替える | 対象の不一致を検出する。SP-2、SP-3。 |
| N-3 | 検知器を停止し推論後のLogだけ作る | 未検査・事後検査を事前検査と扱わない。SP-3。 |

### Failure conditions

非信頼経路が一つでも検知を迂回する、推論後だけ検査する、検査不能を正常とする場合はFail。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象Flowと検知・制御・識別の設定 | Model・API・改善基盤担当者 | 本文の対象版・資産と実境界 | 対象・Policy・方式変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの条件と実経路を対応付ける |
| 正例・負例と結果・実行Trace | 検証担当者 | 本文の正常・攻撃・障害経路 | 初回と実装・Model変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 宣言だけでなく成功・拒否・未実効を観測する |

## Related requirements

[C11.4.2](../../../../controls/control-records/c11-adversarial-robustness/v1.0-c11.4.2-anomaly-flags-trigger-effective-input-gating/README.md)はFlag後のGate。事前検知が動いていてもFlagを無視して通すならそちらがFail。C2の形式・内容検証ともScopeを分ける。
[C11 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

異常検知は巧妙なPrompt Injectionの完全検出を保証しない。誤検出や言語・Modality依存の盲点を明記する。
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
