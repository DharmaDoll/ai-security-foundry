---
title: 出力を較正し予測の過信を減らす
versioned_id: v1.0-C11.2.3
requirement_id: C11.2.3
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

# 出力を較正し予測の過信を減らす

AISVS Verification Level: 2

[C11.2 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.2-membership-inference-and-model-inversion-mitigation.md)

## Upstream basis

AISVS `v1.0-C11.2.3`は、Model出力を較正し、過度に自信のある予測を減らす。
対応Researchは攻撃者の観測権限、出力面、学習・評価の前提と限界を補足する。特定製品・方式・数値を一律のNormative条件にせず、以下の具体化はRepositoryの解釈として記す。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

独立評価Dataで表示確信度と実際の正答率等の関係を測り、過信を減らす調整を確認する。数値を単に隠すことや推論Temperatureを変更したという設定だけでは較正の効果を示せない。生成SamplingのTemperatureと確信度較正も同一視しない。

## Security objective

Model出力を較正し、過度に自信のある予測を減らす。

## Applicability

確信度を持つ対象予測・出力。数値確信度を返さない場合も内部・公開出力の評価可能性を確認し、単なる非表示を較正と呼ばない。

### Non-applicability

対象の能力・出力・学習条件がない場合はApplicabilityに従い、その根拠を明示する。
非公開Providerで観測できないことは対象外やPassの根拠ではない。証拠不足と適用外を区別する。

## Scope and assumptions

対象Model版、Dataの機微性、公開面、攻撃者の観測権限と質問可能量を先に定める。
合成Dataを隔離環境で使用し、公開Repositoryへ実学習記録や機密な攻撃結果を保存しない。
実際の対象条件へ結び付かない設定や結果だけで合格を主張しない。

## Assets, actors, identities, and trust boundaries

機微学習DataからModel、Modelの出力・公開APIから攻撃者の観測へ進む境界。資産は非公開の記録・属性・在籍。Data管理者、Trainer、API運用者、評価者、反復質問可能な攻撃者を区別する。 正答率に見合わない高確信Scoreが公開され、機微推測や過大な判断の根拠になる。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 対象出力・確信度の意味と較正の評価方法を特定する。 |
| SP-2 | 学習や較正の調整に流用していない独立Dataで、過信と調整後の効果を測る。 |
| SP-3 | Model版・較正器・対象条件を結果に結び付け、条件別の失敗や過信を平均だけで隠さない。 |

## Scope calibration and adjacent assurance

C11.2.5は在籍推定への耐性。確信度が正確でも在籍推定が成功する場合があり、両要件を別に判定する。

## Threat and failure-mode rationale

正答率に見合わない高確信Scoreが公開され、機微推測や過大な判断の根拠になる。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

独立評価Dataで表示確信度と実際の正答率等の関係を測り、過信を減らす調整を確認する。数値を単に隠すことや推論Temperatureを変更したという設定だけでは較正の効果を示せない。生成SamplingのTemperatureと確信度較正も同一視しない。 対象Model版、Data Flow、処理設定と観測点を確認する。

### Positive verification

合成評価で調整前後のReliability等を比較し、過信が減ることを確認する。Data分割、件数、対象条件、品質への影響も記録する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 99%表示の群で実際の正答率が約60%となる例を評価する | 過信を識別し、較正済みと無条件判定しない。SP-2。 |
| N-2 | 学習・調整用Dataだけで較正効果を測る | 独立評価の不足と判定する。SP-2。 |
| N-3 | 較正器を旧版のままModelだけ変更する | 結果対象の不一致を検出し再評価する。SP-3。 |

### Failure conditions

較正処理または効果の根拠がない、対象出力で過信を減らしていない、独立評価がない場合はFailまたは証拠不足。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象・設計・設定と根拠 | Model・Privacy担当者 | 本ControlのModel版とData・出力範囲 | 採用時と対象・設定変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの対象と前提を説明できる |
| 正例・負例と独立評価の実測 | 検証担当者 | 本文の対象経路・試験Data・条件 | 初回とModel・方式変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 結果・版・不確実性を対応付ける |

## Related requirements

[C11.2.5](../../../../controls/control-records/c11-adversarial-robustness/v1.0-c11.2.5-membership-inference-simulations-at-random-baseline/README.md)は在籍推定への耐性。確信度が正確でも在籍推定が成功する場合があり、両要件を別に判定する。
[C11 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

較正は情報漏えいの完全防止ではない。標本・条件・時間によって誤差があり、形式的な較正指標だけでPrivacyを主張しない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## 関連する洞察

個別要件の理解・設計レビューを助ける参照であり、追加要件や正式なMappingではない。

- [安全性の数字には、比較できる測定条件が必要である](../../../../docs/insights/security-metrics-need-comparable-conditions.md)：安全性の数字と、その数字を作った試験集合・判定条件・対象を併せて評価する。

## References

- [AISVS v1.0 C11 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C11-Adversarial-Robustness.md)
- [AISVS v1.0 C11.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C11-Adversarial-Robustness/C11-02-Membership-Inference-Model-Inversion-Mitigation.md)
- [C11.2 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.2-membership-inference-and-model-inversion-mitigation.md)
- [C11 Family概要](../README.md)


## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-19 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
