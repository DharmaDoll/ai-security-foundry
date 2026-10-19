---
title: モデルが推測した機微属性を出力へ直接返さない
versioned_id: v1.0-C11.2.1
requirement_id: C11.2.1
verification_level: 1
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

# モデルが推測した機微属性を出力へ直接返さない

AISVS Verification Level: 1

[C11.2 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.2-membership-inference-and-model-inversion-mitigation.md)

## Upstream basis

AISVS `v1.0-C11.2.1`は、Modelが推測した機微属性を出力で直接返さない。
対応Researchは攻撃者の観測権限、出力面、学習・評価の前提と限界を補足する。特定製品・方式・数値を一律のNormative条件にせず、以下の具体化はRepositoryの解釈として記す。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

機微属性と公開可能範囲を先に定義し、回答本文だけでなく構造化Field、Score、説明API、Stream等の外部出力を確認する。属性名を削除しても特定属性を直接表す数値を返せば保護したことにならない。Promptで返さないよう頼むだけでなく、出力境界の実動作を評価する。

## Security objective

Modelが推測した機微属性を出力で直接返さない。

## Applicability

機微属性を推測できるModelの出力とその公開経路。属性推測のないModelは能力・出力Scopeを示して適用外を判断する。

### Non-applicability

対象の能力・出力・学習条件がない場合はApplicabilityに従い、その根拠を明示する。
非公開Providerで観測できないことは対象外やPassの根拠ではない。証拠不足と適用外を区別する。

## Scope and assumptions

対象Model版、Dataの機微性、公開面、攻撃者の観測権限と質問可能量を先に定める。
合成Dataを隔離環境で使用し、公開Repositoryへ実学習記録や機密な攻撃結果を保存しない。
実際の対象条件へ結び付かない設定や結果だけで合格を主張しない。

## Assets, actors, identities, and trust boundaries

機微学習DataからModel、Modelの出力・公開APIから攻撃者の観測へ進む境界。資産は非公開の記録・属性・在籍。Data管理者、Trainer、API運用者、評価者、反復質問可能な攻撃者を区別する。 攻撃者が正規APIを繰返し利用し、非公開の病歴や属性をModelの推測出力から直接取得する。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 対象となるModel推測の機微属性と外部出力面を列挙する。 |
| SP-2 | 対象属性が本文・構造化Field・直接その属性を表すScore等へ返らない。 |
| SP-3 | Stream、説明、Export等の代替経路にも非開示を適用する。 |

## Scope calibration and adjacent assurance

C11.2.5は間接的な在籍推定の成功率。本Controlで直接開示を抑えても、出力傾向からの推測耐性は示せない。

## Threat and failure-mode rationale

攻撃者が正規APIを繰返し利用し、非公開の病歴や属性をModelの推測出力から直接取得する。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

機微属性と公開可能範囲を先に定義し、回答本文だけでなく構造化Field、Score、説明API、Stream等の外部出力を確認する。属性名を削除しても特定属性を直接表す数値を返せば保護したことにならない。Promptで返さないよう頼むだけでなく、出力境界の実動作を評価する。 対象Model版、Data Flow、処理設定と観測点を確認する。

### Positive verification

合成した機微属性と非機微属性の質問を用い、前者を直接返さず後者の許可結果を使えることを全出力面で観測する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 本文を隠し同じ属性を説明FieldやScoreへ入れる | 直接開示の残存として検出する。SP-2。 |
| N-2 | Streamの初期Chunkだけに属性を出す | 最終回答だけでなく公開済みChunkでFailを検出する。SP-3。 |
| N-3 | 説明・Export経路を呼ぶ | 同じ非開示境界を確認する。SP-1、SP-3。 |

### Failure conditions

対象の推測機微属性を一つでも外部へ直接返す場合はFail。本文の検査だけでは全出力面の保証にならない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象・設計・設定と根拠 | Model・Privacy担当者 | 本ControlのModel版とData・出力範囲 | 採用時と対象・設定変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの対象と前提を説明できる |
| 正例・負例と独立評価の実測 | 検証担当者 | 本文の対象経路・試験Data・条件 | 初回とModel・方式変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 結果・版・不確実性を対応付ける |

## Related requirements

[C11.2.5](../../../../controls/control-records/c11-adversarial-robustness/v1.0-c11.2.5-membership-inference-simulations-at-random-baseline/README.md)は間接的な在籍推定の成功率。本Controlで直接開示を抑えても、出力傾向からの推測耐性は示せない。
[C11 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

機微属性の定義漏れ、言い換えや反復質問による推測は残る。一般的な個人情報Scannerだけで対象属性を尽くしたとしない。
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
