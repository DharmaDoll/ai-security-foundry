---
title: 抽出の疑いを検知したら対応措置を発動する
versioned_id: v1.0-C11.3.4
requirement_id: C11.3.4
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

# 抽出の疑いを検知したら対応措置を発動する

AISVS Verification Level: 3

[C11.3 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.3-model-extraction-defense.md)

## Upstream basis

AISVS `v1.0-C11.3.4`は、抽出の疑いの検知がResponse措置を発動する。
対応Researchは実経路での検出・制御・識別の試験と、誤検知・見逃しの限界を補足する。特定製品・研究値・手法の全採用を一律のNormative条件にしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

検知器のSignalと、制限・追加認証・調査等の対応をつなぎ、定めた対象と範囲で措置が始まることを実測する。Logだけ保存し誰も対応しない状態では足りない。原文は特定の自動Blockや応答劣化、外部への情報共有を一律に求めていない。

## Security objective

抽出の疑いの検知がResponse措置を発動する。

## Applicability

対象Modelと公開API、外部入力、または安全性改善Feedbackの実使用経路に適用する。対象・能力・責任分界を以下のSPに合わせて特定する。

### Non-applicability

対象APIや外部観測面が存在しない場合は到達可能性と責任分界を示す。非公開Providerの内部が見えないことは、対象外やPassの根拠ではなく未立証として記録する。

## Scope and assumptions

対象Model版、入力・出力・Feedback経路、攻撃者の操作・観測範囲を先に定める。無害な模擬Data・Traceを隔離環境で使い、結果と実動作を対応付ける。誤検知・見逃し・未観測の範囲を明記し、Model自身の説明を強制や証拠の代わりにしない。

## Assets, actors, identities, and trust boundaries

検知器からGateway・運用担当者・Incident対応へ進む境界。資産はModel能力、利用者権限と可用性。検知器、Response担当者、利用者。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 抽出疑いのSignalに対応する措置、責任者、対象と発動条件を定義する。 |
| SP-2 | 検知結果から実際の対応へ接続され、通知・調査・制限等が定義どおり開始する。 |
| SP-3 | 誤検知・対応失敗・復帰を区別し、別主体や無関係な利用者へ誤適用しない。 |

## Scope calibration and adjacent assurance

C11.3.1は検知器へのPattern入力。本Controlは検知後の実対応。対応方針の妥当性や情報共有の許可は別に判断する。

## Threat and failure-mode rationale

抽出を検知しても記録だけで終わり、攻撃者が同じ権限・出力で収集を続ける。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

検知器のSignalと、制限・追加認証・調査等の対応をつなぎ、定めた対象と範囲で措置が始まることを実測する。Logだけ保存し誰も対応しない状態では足りない。原文は特定の自動Blockや応答劣化、外部への情報共有を一律に求めていない。 対象版、実際の呼出し順、結果と実消費・措置を照合する。

### Positive verification

模擬検知Signalを実対応経路へ送り、定めた主体に対する措置または担当者の調査が開始することを確認する。正常Signalには不必要な措置が発動しないことも示す。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 検知Logは残すが措置・担当者へ未接続にする | 対応未発動としてFailとする。SP-2。 |
| N-2 | 措置APIや通知先を障害にする | 未完了を検知し、成功と記録しない。SP-2、SP-3。 |
| N-3 | 同じ名前の別Tenantや主体へ誤Bindingする | 対象違いを検出し、不関係な利用者へ措置を適用しない。SP-3。 |

### Failure conditions

抽出疑いの検知が対応を発動しない、記録だけ、失敗を成功扱いする場合はFail。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象Flowと検知・制御・識別の設定 | Model・API・改善基盤担当者 | 本文の対象版・資産と実境界 | 対象・Policy・方式変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの条件と実経路を対応付ける |
| 正例・負例と結果・実行Trace | 検証担当者 | 本文の正常・攻撃・障害経路 | 初回と実装・Model変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 宣言だけでなく成功・拒否・未実効を観測する |

## Related requirements

[C11.3.1](../../../../controls/control-records/c11-adversarial-robustness/v1.0-c11.3.1-query-pattern-analysis-feeds-model-extraction-detector/README.md)は検知器へのPattern入力。本Controlは検知後の実対応。対応方針の妥当性や情報共有の許可は別に判断する。
[C11 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

疑いは攻撃の確定ではない。過剰制限による正規利用の阻害や検知遅延は残り、措置の比例性と解除条件を記録する。
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
