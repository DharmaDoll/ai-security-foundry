---
title: 生の出力をBackend内に保ち公開応答を抽出Riskへ調整する
versioned_id: v1.0-C11.3.2
requirement_id: C11.3.2
verification_level: 2
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

# 生の出力をBackend内に保ち公開応答を抽出Riskへ調整する

AISVS Verification Level: 2

[C11.3 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.3-model-extraction-defense.md)

## Upstream basis

AISVS `v1.0-C11.3.2`は、生のModel出力をApplication Backend外へ直接公開せず、外部応答を抽出Riskに合わせる。
対応Researchは実経路での検出・制御・識別の試験と、誤検知・見逃しの限界を補足する。特定製品・研究値・手法の全採用を一律のNormative条件にしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

生のScore・確率分布・内部Field等をそのままProxyせず、製品が必要とする応答をBackendで構成する。JSONに包むだけでは情報量は変わらない。何を公開し何を抑えるかの根拠を抽出Riskと有用性から定める。ここでの調整はC11.2.3の確信度較正とは別である。

## Security objective

生のModel出力をApplication Backend外へ直接公開せず、外部応答を抽出Riskに合わせる。

## Applicability

対象Modelと公開API、外部入力、または安全性改善Feedbackの実使用経路に適用する。対象・能力・責任分界を以下のSPに合わせて特定する。

### Non-applicability

対象APIや外部観測面が存在しない場合は到達可能性と責任分界を示す。非公開Providerの内部が見えないことは、対象外やPassの根拠ではなく未立証として記録する。

## Scope and assumptions

対象Model版、入力・出力・Feedback経路、攻撃者の操作・観測範囲を先に定める。無害な模擬Data・Traceを隔離環境で使い、結果と実動作を対応付ける。誤検知・見逃し・未観測の範囲を明記し、Model自身の説明を強制や証拠の代わりにしない。

## Assets, actors, identities, and trust boundaries

生出力からBackendの公開Responseへ進む境界。資産はModelの内部情報と能力。Provider、Backend、外部Client。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | Modelの生出力と外部へ公開するField・Surfaceを区別して列挙する。 |
| SP-2 | Backend境界で公開Responseを構成し、生出力を直接外へ流さない。 |
| SP-3 | 公開情報を抽出Riskに合わせて選び、Stream・Debug・説明API等の代替経路にも同じ境界を保つ。 |

## Scope calibration and adjacent assurance

C11.2.3の較正とは目的が異なる。C7の出力安全性・Schema処理も抽出Riskに応じた公開情報選択を単独では代替しない。

## Threat and failure-mode rationale

詳細なScoreや内部Traceを質問と組み合わせて教師Dataとし、Modelの能力・構造を模倣する。
ATLAS Content `2026.10`の`AML.T0005.001`との関係を`proposed`として評価した。
[対応の根拠・範囲・限界](../../../atlas-mapping-review-2026-10.md#c11)を参照。
正本はCatalogの`threat_mappings`であり、ResearchのMappingの転載や製品適合の主張ではない。

## Verification

### Architecture and configuration review

生のScore・確率分布・内部Field等をそのままProxyせず、製品が必要とする応答をBackendで構成する。JSONに包むだけでは情報量は変わらない。何を公開し何を抑えるかの根拠を抽出Riskと有用性から定める。ここでの調整はC11.2.3の確信度較正とは別である。 対象版、実際の呼出し順、結果と実消費・措置を照合する。

### Positive verification

合成Score・内部Markerを含むModel出力をBackendへ渡す。公開Responseが定義したFieldだけで、許可した正規結果は利用できることを全出力経路で確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 生の確率分布をJSONへ包んで返す | 形式変更だけの直接公開としてFailとする。SP-2。 |
| N-2 | Debug・Stream・説明Fieldに内部Markerを入れる | 公開Policy外の漏れを検出する。SP-1、SP-3。 |
| N-3 | Model出力の新Fieldを追加する | 既定の全Field転送で公開されないことを確認する。SP-2、SP-3。 |

### Failure conditions

生出力を直接外へ出す、公開情報が抽出Riskと対応しない、代替経路が境界を迂回する場合はFailまたは根拠不足。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象Flowと検知・制御・識別の設定 | Model・API・改善基盤担当者 | 本文の対象版・資産と実境界 | 対象・Policy・方式変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの条件と実経路を対応付ける |
| 正例・負例と結果・実行Trace | 検証担当者 | 本文の正常・攻撃・障害経路 | 初回と実装・Model変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 宣言だけでなく成功・拒否・未実効を観測する |

## Related requirements

[C11.2.3](../../../../controls/control-records/c11-adversarial-robustness/v1.0-c11.2.3-calibrate-model-outputs-to-reduce-overconfidence/README.md)の較正とは目的が異なる。C7の出力安全性・Schema処理も抽出Riskに応じた公開情報選択を単独では代替しない。
[C11 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

通常の回答にも模倣に使える情報は残る。出力を減らすと正規利用にも影響し、全抽出を防ぐとは言えない。
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
| 2026-10-29 | ATLAS Content 2026.10との対応を評価。要件解釈・成熟度は維持 | 固定版ATLASとRepository独自の比較 | [対応案](../../../atlas-mapping-review-2026-10.md#c11)。人のレビュー・製品試験は未実施 |
