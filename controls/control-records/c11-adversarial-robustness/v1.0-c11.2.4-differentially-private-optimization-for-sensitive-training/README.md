---
title: 機微データの学習へ差分Privacy最適化を適用する
versioned_id: v1.0-C11.2.4
requirement_id: C11.2.4
verification_level: 2
family_id: C11
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C11-Adversarial-Robustness.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C11-Adversarial-Robustness/C11-02-Membership-Inference-Model-Inversion-Mitigation.md
last_verified: '2026-10-19'
maturity: verifiable
mapping_assessment_refs: []
---

# 機微データの学習へ差分Privacy最適化を適用する

AISVS Verification Level: 2

[C11.2 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.2-membership-inference-and-model-inversion-mitigation.md)

## Upstream basis

AISVS `v1.0-C11.2.4`は、機微Datasetでの学習にDifferentially-private Optimizationを用いる。
対応Researchは攻撃者の観測権限、出力面、学習・評価の前提と限界を補足する。特定製品・方式・数値を一律のNormative条件にせず、以下の具体化はRepositoryの解釈として記す。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

何を一単位として保護するか、隣接Dataの定義、Privacy予算と会計方法を定め、実学習の更新処理へDP最適化を適用する。DP-SGDは例であり唯一の必須手段ではない。LibraryをImportするだけ、通常のNoiseやDropoutだけで差分Privacyの保証と呼ばない。

## Security objective

機微Datasetでの学習にDifferentially-private Optimizationを用いる。

## Applicability

機微Datasetで学習・追加学習する構成。機微Dataを使わない場合は分類と学習Flowを示して対象外を判断する。Provider委託は未確認の理由にしない。

### Non-applicability

対象の能力・出力・学習条件がない場合はApplicabilityに従い、その根拠を明示する。
非公開Providerで観測できないことは対象外やPassの根拠ではない。証拠不足と適用外を区別する。

## Scope and assumptions

対象Model版、Dataの機微性、公開面、攻撃者の観測権限と質問可能量を先に定める。
合成Dataを隔離環境で使用し、公開Repositoryへ実学習記録や機密な攻撃結果を保存しない。
実際の対象条件へ結び付かない設定や結果だけで合格を主張しない。

## Assets, actors, identities, and trust boundaries

機微学習DataからModel、Modelの出力・公開APIから攻撃者の観測へ進む境界。資産は非公開の記録・属性・在籍。Data管理者、Trainer、API運用者、評価者、反復質問可能な攻撃者を区別する。 学習の過適合や記憶から機微な一記録・個人の在籍や内容が出力に強く反映される。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 機微Datasetと保護単位・Privacy予算・会計の前提を明示する。 |
| SP-2 | 実際の最適化へDPの必要処理を適用し、経路の一部で通常最適化へ無断Fallbackしない。 |
| SP-3 | Runの実Parameter・Step・Sampling等から予算を追跡し、主張する保証と一致を確認できる。 |

## Scope calibration and adjacent assurance

C11.2.5は攻撃試験、C1.1.1はData最小化。匿名化や出力FilterだけでDP最適化の代わりにはならない。

## Threat and failure-mode rationale

学習の過適合や記憶から機微な一記録・個人の在籍や内容が出力に強く反映される。
ATLAS Content `2026.10`の`AML.T0137.000`との関係を`proposed`として評価した。
[対応の根拠・範囲・限界](../../../atlas-mapping-review-2026-10.md#c11)を参照。
正本はCatalogの`threat_mappings`であり、ResearchのMappingの転載や製品適合の主張ではない。

## Verification

### Architecture and configuration review

何を一単位として保護するか、隣接Dataの定義、Privacy予算と会計方法を定め、実学習の更新処理へDP最適化を適用する。DP-SGDは例であり唯一の必須手段ではない。LibraryをImportするだけ、通常のNoiseやDropoutだけで差分Privacyの保証と呼ばない。 対象Model版、Data Flow、処理設定と観測点を確認する。

### Positive verification

合成機微Dataの小規模RunでDP最適化が更新へ適用され、独立した会計照合で予算が整合することを確認する。User単位を主張するなら複数記録の扱いも確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | DP設定だけ置いて通常Optimizerを実行する | 実更新の未適用を検出する。SP-2。 |
| N-2 | Noiseや必要なClip処理を無効化したRunを提出する | 採用したDP方式の成立条件不足を検出する。SP-2。 |
| N-3 | 記録単位の会計を個人単位の保証と表示する | 保護単位と保証の不一致を検出する。SP-1、SP-3。 |

### Failure conditions

対象機微学習にDP最適化がない、成立前提や保護単位を説明できない、実Runと会計が不一致の場合はFailまたは証拠不足。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象・設計・設定と根拠 | Model・Privacy担当者 | 本ControlのModel版とData・出力範囲 | 採用時と対象・設定変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの対象と前提を説明できる |
| 正例・負例と独立評価の実測 | 検証担当者 | 本文の対象経路・試験Data・条件 | 初回とModel・方式変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 結果・版・不確実性を対応付ける |

## Related requirements

[C11.2.5](../../../../controls/control-records/c11-adversarial-robustness/v1.0-c11.2.5-membership-inference-simulations-at-random-baseline/README.md)は攻撃試験、[C1.1.1](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.1.1-purpose-bound-training-fields/README.md)はData最小化。匿名化や出力FilterだけでDP最適化の代わりにはならない。
[C11 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

DPは定義した単位と予算の条件付き保証であり、全秘密の非開示やModel品質を保証しない。大きな予算の実務上の弱さ、組成・繰返しRunの影響も説明する。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C11 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C11-Adversarial-Robustness.md)
- [AISVS v1.0 C11.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C11-Adversarial-Robustness/C11-02-Membership-Inference-Model-Inversion-Mitigation.md)
- [C11.2 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.2-membership-inference-and-model-inversion-mitigation.md)
- [C11 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-19 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
| 2026-10-29 | ATLAS Content 2026.10との対応を評価。要件解釈・成熟度は維持 | 固定版ATLASとRepository独自の比較 | [対応案](../../../atlas-mapping-review-2026-10.md#c11)。人のレビュー・製品試験は未実施 |
