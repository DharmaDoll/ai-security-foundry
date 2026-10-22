---
title: 在籍推定試験で偶然を超える攻撃成功がないか確かめる
versioned_id: v1.0-C11.2.5
requirement_id: C11.2.5
verification_level: 3
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

# 在籍推定試験で偶然を超える攻撃成功がないか確かめる

AISVS Verification Level: 3

[C11.2 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.2-membership-inference-and-model-inversion-mitigation.md)

## Upstream basis

AISVS `v1.0-C11.2.5`は、Membership-inference攻撃Simulationで、評価Data上の攻撃正答率がRandom Guessingを超えないことを示す。
対応Researchは攻撃者の観測権限、出力面、学習・評価の前提と限界を補足する。特定製品・方式・数値を一律のNormative条件にせず、以下の具体化はRepositoryの解釈として記す。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

MemberとNon-memberの構成、攻撃者の観測権限、攻撃調整Dataと評価Data、偶然の基準を先に固定する。均衡二群では50%だが、不均衡Dataへ機械的に50%を使わない。観測正答率、件数、不確実性、対象集団ごとの結果を示す。ResearchのAUC許容例を原文のAccuracy条件の緩和として使わない。

## Security objective

Membership-inference攻撃Simulationで、評価Data上の攻撃正答率がRandom Guessingを超えないことを示す。

## Applicability

学習済みModelとその学習Dataの在籍Privacy。API型で学習Membershipが分からない場合は評価不能を明記し、対象外やPassへ置き換えない。

### Non-applicability

対象の能力・出力・学習条件がない場合はApplicabilityに従い、その根拠を明示する。
非公開Providerで観測できないことは対象外やPassの根拠ではない。証拠不足と適用外を区別する。

## Scope and assumptions

対象Model版、Dataの機微性、公開面、攻撃者の観測権限と質問可能量を先に定める。
合成Dataを隔離環境で使用し、公開Repositoryへ実学習記録や機密な攻撃結果を保存しない。
実際の対象条件へ結び付かない設定や結果だけで合格を主張しない。

## Assets, actors, identities, and trust boundaries

機微学習DataからModel、Modelの出力・公開APIから攻撃者の観測へ進む境界。資産は非公開の記録・属性・在籍。Data管理者、Trainer、API運用者、評価者、反復質問可能な攻撃者を区別する。 Modelの応答差から特定記録が学習に入ったかを攻撃者が判別し、非公開の在籍自体を漏えいさせる。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 評価DataのMember／Non-member、分割、攻撃権限とRandom基準を明示する。 |
| SP-2 | 対象Modelで現実的な在籍推定Simulationを実行し、攻撃調整と独立した評価で正答率を測る。 |
| SP-3 | 評価対象で基準を超えない結果を示し、上回る攻撃・集団や統計的不確実性を隠さない。 |

## Scope calibration and adjacent assurance

C11.2.3の較正やC11.2.4のDPは試験結果の代替ではない。AUCや低FPRでの検出率は補足として記録し、原文の正答率と混同しない。

## Threat and failure-mode rationale

Modelの応答差から特定記録が学習に入ったかを攻撃者が判別し、非公開の在籍自体を漏えいさせる。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

MemberとNon-memberの構成、攻撃者の観測権限、攻撃調整Dataと評価Data、偶然の基準を先に固定する。均衡二群では50%だが、不均衡Dataへ機械的に50%を使わない。観測正答率、件数、不確実性、対象集団ごとの結果を示す。ResearchのAUC許容例を原文のAccuracy条件の緩和として使わない。 対象Model版、Data Flow、処理設定と観測点を確認する。

### Positive verification

合成学習記録と同じ生成分布の非学習記録を用意し、攻撃を調整用と評価用に分ける。対象APIへの攻撃結果を偶然基準と比較し、評価済み範囲と不確実性を記録する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 均衡二群で攻撃正答率78%を得る | 50%基準を超えるためFailとする。SP-3。 |
| N-2 | Memberだけ出所の違うDataを使う | 分布差を当てる試験と在籍推定を区別し、盲検対照で評価の歪みを検出する。SP-1、SP-2。 |
| N-3 | 弱い攻撃一件の結果で他攻撃の超過や標本不足を隠す | 主張範囲の不足を検出し、普遍的なPassにしない。SP-2、SP-3。 |

### Failure conditions

評価Data上の攻撃正答率が定義したRandom基準を超える、試験未実施、分割漏えいや根拠のない基準で結果を主張する場合はFailまたは未立証。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象・設計・設定と根拠 | Model・Privacy担当者 | 本ControlのModel版とData・出力範囲 | 採用時と対象・設定変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの対象と前提を説明できる |
| 正例・負例と独立評価の実測 | 検証担当者 | 本文の対象経路・試験Data・条件 | 初回とModel・方式変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 結果・版・不確実性を対応付ける |

## Related requirements

[C11.2.3](../../../../controls/control-records/c11-adversarial-robustness/v1.0-c11.2.3-calibrate-model-outputs-to-reduce-overconfidence/README.md)の較正やC11.2.4のDPは試験結果の代替ではない。AUCや低FPRでの検出率は補足として記録し、原文の正答率と混同しない。
[C11 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

有限試験は未知攻撃や母集団全体での完全な非識別性を証明しない。偶然以下の観測値でも、件数・信頼区間・攻撃の強さが不足すれば保証は限定的。
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
