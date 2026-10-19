---
title: 量子化後の実構成物へ同じ安全性試験を再実行する
versioned_id: v1.0-C3.2.2
requirement_id: C3.2.2
verification_level: 2
family_id: C3
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-02-Model-Validation-Testing.md
last_verified: '2026-10-18'
maturity: verifiable
mapping_assessment_refs: []
---

# 量子化後の実構成物へ同じ安全性試験を再実行する

AISVS Verification Level: 2

[C3.2 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.2-model-validation-and-testing.md)

## Upstream basis

AISVS `v1.0-C3.2.2`は、学習後に量子化したModelは、配備前に圧縮後のArtifactへ同じ安全性・Alignment試験一式を再実行する。
Researchは通常精度やPerplexityの維持から安全性を推定できず、影響がModelと設定に依存することを注意する。Pruningや蒸留の議論もあるが、本要件のNormative対象は学習後の量子化である。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

元のModelで実行した安全性・Alignment Suiteを版と設定で特定し、量子化後に実際に使うArtifactへ同じSuiteを実行する。量子化前の結果の引用や回答精度だけの試験では満たせない。FormatやLoader等の差を記録し、元と圧縮後の結果を対応付ける。

## Security objective

別のArtifactへ変換した後も、変換前に獲得した安全性評価結果を無条件に引き継がないようにする。

## Applicability

Post-training Quantizationを施して配備するModelに適用する。量子化条件、対象の重み等、Loader・推論設定と配備する実体を識別する。対象となる量子化を行っていない場合は、その構成を示して対象外にできる。

### Non-applicability

Post-training Quantizationを実施していない対象は、その構成を示して対象外とできる。他の圧縮手法の評価は有益でも本要件へ自動的に拡大しない。量子化を委託したことは対象外の理由ではない。

## Scope and assumptions

対象Deployment、Model一式、版、Provider、Registryと実際の読込み経路を評価開始時に特定する。
名前やAliasが可変なら実体の識別方法を明示する。試験は隔離環境の無害な模擬Artifactで行い、
本番Dataや実行可能な不正Payloadを持ち込まない。証拠の対象版と現在の配備が一致するか確認する。

## Assets, actors, identities, and trust boundaries

評価済みの元Artifactから量子化処理を経て、配備する圧縮Artifactへ進む境界。資産は圧縮後Modelの安全性評価と対象識別。変換担当者、評価者、Release担当者が関わる。攻撃者は特定入力で変換後に崩れた安全境界を利用し得る。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 元Modelの安全性・Alignment Suiteの版と対象を特定できる。 |
| SP-2 | 同じSuiteを配備する量子化後のArtifactへ再実行し、試験結果を実体へ結び付ける。 |
| SP-3 | 再評価を配備前に実施し、比較結果と退行・未評価項目を隠さず記録する。 |

## Scope calibration and adjacent assurance

C3.2.1は三種の一般的な投入前自動試験、C3.2.3はProviderのModel・版・Routing変更。本要件の量子化だけでProvider変更が起きたとみなさない。

## Threat and failure-mode rationale

量子化で通常の回答精度が保たれても拒否や条件別の振る舞いが変わり、旧結果の流用で弱点を見逃す。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

量子化処理、元と圧縮後の識別値、評価Suiteの版・設定、実行時刻、配備先を確認する。一般精度だけの結果や、Suiteを簡略化して同じ試験と呼ぶ箇所を探す。

### Positive verification

模擬Modelの元Artifactと量子化後Artifactに同じ版のSuiteを実行し、カテゴリ別の結果を比較する。実使用Format・Loader・設定、配備時点と圧縮後Artifactの対応を記録する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 圧縮後は一般精度だけを測る | 安全性・Alignment再評価の欠落としてFailにする。SP-2。 |
| N-2 | 元の重みでSuiteを再実行して圧縮後の結果と申告する | 評価対象の識別不一致を検出する。SP-2。 |
| N-3 | Suiteから失敗カテゴリを除外する、または配備後だけ評価する | Suite・時点の差を検出し、同じ投入前再評価と判定しない。SP-1、SP-3。 |

### Failure conditions

量子化後の配備実体へ同じ安全性・Alignment Suiteを実行していない、配備後の実行しかない、旧Artifactの結果を流用する場合はFail。退行発見は再評価未実施とは異なるため、実施結果とRelease判断を分ける。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 元・圧縮後の対応とSuite実行結果 | 変換・評価担当者 | 両Artifact、Suite版と実設定 | 量子化条件・Artifact変更と各投入前 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 同じSuiteが圧縮後の実体に実行される |
| 差分評価と投入判断 | Release担当者 | カテゴリ別の変化・残余Risk | 各投入時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 退行と対象外・未評価を区別する |

## Related requirements

[C3.2.1](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.2.1-automated-input-safety-output-tests-before-deployment/README.md)は三種の一般的な投入前自動試験、[C3.2.3](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.2.3-security-reevaluation-before-provider-route-changes/README.md)はProviderのModel・版・Routing変更。本要件の量子化だけでProvider変更が起きたとみなさない。
[C3 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

元Suiteにない攻撃は引き続き見えず、Sampling等による結果の変動もある。量子化が常に安全性を損なうとも、一般精度維持なら安全とも言わない。具体的な許容閾値は製品のRisk判断として別に定める。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C3 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [AISVS v1.0 C3.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-02-Model-Validation-Testing.md)
- [C3.2 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.2-model-validation-and-testing.md)
- [C3 Family概要](../README.md)

- [関連Insight：検査するのは入口の文字列ではなく、実際に利用される内容である](../../../../docs/insights/validation-must-cover-effective-payload.md)（Repositoryの横断的な考察。規範やMappingではない）

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
