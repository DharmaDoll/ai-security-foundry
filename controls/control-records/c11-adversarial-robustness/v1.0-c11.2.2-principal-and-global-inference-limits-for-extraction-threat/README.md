---
title: 推測攻撃の質問量に合わせ主体別・全体の上限を強制する
versioned_id: v1.0-C11.2.2
requirement_id: C11.2.2
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

# 推測攻撃の質問量に合わせ主体別・全体の上限を強制する

AISVS Verification Level: 1

[C11.2 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.2-membership-inference-and-model-inversion-mitigation.md)

## Upstream basis

AISVS `v1.0-C11.2.2`は、推論Endpointへ、抽出Threat Modelに合わせた主体別と全体のRate Limitを強制し、汎用API制限だけで済ませない。
対応Researchは攻撃者の観測権限、出力面、学習・評価の前提と限界を補足する。特定製品・方式・数値を一律のNormative条件にせず、以下の具体化はRepositoryの解釈として記す。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

攻撃者が得られる出力と必要質問量、複数主体、Burst・低速反復を考えて上限と集計窓を定める。API Keyを替えるたび上限がリセットされ全体が無制限な構成では満たせない。制限値は用途ごとのRisk判断であり、一律の安全な質問数はない。

## Security objective

推論Endpointへ、抽出Threat Modelに合わせた主体別と全体のRate Limitを強制し、汎用API制限だけで済ませない。

## Applicability

外部に観測可能な推論Endpoint。非公開内部処理だけの場合は攻撃者到達性と責任境界を示す。

### Non-applicability

対象の能力・出力・学習条件がない場合はApplicabilityに従い、その根拠を明示する。
非公開Providerで観測できないことは対象外やPassの根拠ではない。証拠不足と適用外を区別する。

## Scope and assumptions

対象Model版、Dataの機微性、公開面、攻撃者の観測権限と質問可能量を先に定める。
合成Dataを隔離環境で使用し、公開Repositoryへ実学習記録や機密な攻撃結果を保存しない。
実際の対象条件へ結び付かない設定や結果だけで合格を主張しない。

## Assets, actors, identities, and trust boundaries

機微学習DataからModel、Modelの出力・公開APIから攻撃者の観測へ進む境界。資産は非公開の記録・属性・在籍。Data管理者、Trainer、API運用者、評価者、反復質問可能な攻撃者を区別する。 主体ごとの上限を複数AccountやEndpointで分散し、学習Dataの在籍・内容を推測する観測を集める。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 抽出・推測の攻撃予算に対応した主体識別、対象Endpoint、集計窓と上限の根拠を定義する。 |
| SP-2 | 主体別上限を実APIで強制する。 |
| SP-3 | 複数主体を横断する全体上限も強制し、別Endpoint・Replica等で集計を迂回できない。 |

## Scope calibration and adjacent assurance

C11.3.1は抽出らしい質問Patternの検知。Rate Limitは検知器の代替ではなく、主体横断の制限だけで全攻撃を止めるわけでもない。

## Threat and failure-mode rationale

主体ごとの上限を複数AccountやEndpointで分散し、学習Dataの在籍・内容を推測する観測を集める。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

攻撃者が得られる出力と必要質問量、複数主体、Burst・低速反復を考えて上限と集計窓を定める。API Keyを替えるたび上限がリセットされ全体が無制限な構成では満たせない。制限値は用途ごとのRisk判断であり、一律の安全な質問数はない。 対象Model版、Data Flow、処理設定と観測点を確認する。

### Positive verification

上限内の正常質問が成功し、合成負荷で主体上限と全体上限をそれぞれ超えると制限されることを実APIで確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 同一主体でKeyやSessionを替えて連続質問する | 定義した主体Bindingで上限を維持する。SP-2。 |
| N-2 | 複数主体から同時に質問する | 全体上限が働き総量無制限にしない。SP-3。 |
| N-3 | 別Replica・説明API・低速反復へ分散する | 対象範囲と窓に従い制限が適用される。SP-1、SP-3。 |

### Failure conditions

主体別か全体の一方がない、実際に強制しない、上限が抽出Threat Modelと無関係な汎用値のみの場合はFailまたは根拠不足。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象・設計・設定と根拠 | Model・Privacy担当者 | 本ControlのModel版とData・出力範囲 | 採用時と対象・設定変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの対象と前提を説明できる |
| 正例・負例と独立評価の実測 | 検証担当者 | 本文の対象経路・試験Data・条件 | 初回とModel・方式変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 結果・版・不確実性を対応付ける |

## Related requirements

[C11.3.1](../../../../controls/control-records/c11-adversarial-robustness/v1.0-c11.3.1-query-pattern-analysis-feeds-model-extraction-detector/README.md)は抽出らしい質問Patternの検知。Rate Limitは検知器の代替ではなく、主体横断の制限だけで全攻撃を止めるわけでもない。
[C11 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

少数質問で成立する攻撃や多数主体の識別限界、正規利用の誤制限が残る。WindowのResetやCounter障害時の扱いも記録する。
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
