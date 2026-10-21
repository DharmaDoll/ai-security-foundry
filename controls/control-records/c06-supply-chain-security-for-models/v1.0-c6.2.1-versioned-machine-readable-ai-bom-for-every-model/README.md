---
title: 各モデルに版管理された機械可読AI BOMを公開する
versioned_id: v1.0-C6.2.1
requirement_id: C6.2.1
verification_level: 1
family_id: C6
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C06-Supply-Chain.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C06-Supply-Chain/C06-02-AI-BOM-Supply-Chain-Monitoring.md
last_verified: '2026-10-18'
maturity: verifiable
mapping_assessment_refs: []
---

# 各モデルに版管理された機械可読AI BOMを公開する

AISVS Verification Level: 1


## Upstream basis

AISVS `v1.0-C6.2.1`は、すべてのModel Artifactについて、Dataset、重み、License、Data Origin声明を列挙する版管理済みの機械可読AI BOMを提供する。
対応Researchの手法・製品・版・追加対策は参考情報であり、原文の保証を実効的に確かめる条件と区別する。Research内のMappingを自動採用しない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

各Model版と対応するBOM版を結び付け、実際の構成からDataの由来と権利条件まで追えるようにする。Publishは必要な利用者が取得できる提供であり、本要件から機密情報をInternetへ公開する義務を導かない。特定BOM規格は実装例。

## Security objective

すべてのModel Artifactについて、Dataset、重み、License、Data Origin声明を列挙する版管理済みの機械可読AI BOMを提供する。

## Applicability

第三者Modelと関連Artifact、または対象ModelのAI BOMを扱う取得・Import・Build・昇格経路に適用する。対象となる個別資産は下記SPと境界で特定する。

### Non-applicability

Model Artifactを作成・利用しない境界は責任分界を示す。BOMを生成していないことやProviderが非開示であることだけで対象外にせず、証拠不足を残す。

## Scope and assumptions

対象Modelと構成物、版、Source、BOM、処理環境と責任者を特定する。信頼する基準の作成・更新者と権限を明示し、同じ名前から実体の一致を推定しない。試験は合成Dataや無害なFixtureを隔離環境で使用する。実製品での試験結果は本Repositoryへ保存せず期待証拠を定義する。

## Assets, actors, identities, and trust boundaries

学習・取得MetadataからBOM生成、Model版と結び付けた提供の境界。生成者、Source提供者、BOM利用者。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 各Model Artifactへ対応する機械可読BOMが取得可能である。 |
| SP-2 | Dataset、重み、License、Data Origin声明を記載し、対応する実Model版へ辿れる。 |
| SP-3 | BOMを版管理し、Model更新後も旧版との対応を失わない。 |

## Scope calibration and adjacent assurance

C6.2.2はBOM署名、C6.2.3は欠落時のBuild失敗。BOMの存在はどちらも単独では保証しない。

## Threat and failure-mode rationale

Model名だけのSBOMにDatasetや由来情報がなく、供給元問題の影響を追えない。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

各Model版と対応するBOM版を結び付け、実際の構成からDataの由来と権利条件まで追えるようにする。Publishは必要な利用者が取得できる提供であり、本要件から機密情報をInternetへ公開する義務を導かない。特定BOM規格は実装例。 実処理の呼出し順、入力版、結果と許可・拒否の扱いを点検する。

### Positive verification

二つの合成Model版のBOMを生成し、Parserで読み取る。四つの情報区分と対象Model版を照合し、利用者がそれぞれの版を参照できることを示す。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | Model一件のBOMやDataset・由来情報を省く | 対象または記載の欠落と判定する。SP-1、SP-2。 |
| N-2 | 自由文PDFだけを提供する | 機械可読の構造がなければ満たさない。SP-1。 |
| N-3 | Modelを更新してBOMを同じ名前で上書きし履歴を失う | 旧版との対応・版管理の欠落を検出する。SP-3。 |

### Failure conditions

ModelごとのBOMがない、四情報区分が欠落、機械可読でない、版対応が失われる場合はFailまたは証拠不足。不明を記すことと完全な情報があることは分ける。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象一覧・版とPolicy／設定 | Model・供給網基盤担当者 | 本Controlの対象Artifactと強制・確認点 | 対象・Policy・実装変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの範囲と実構成が一致する |
| 正例・負例の結果と処理Trace | 検証担当者 | 通常・代替・障害の対象経路 | 初回と処理経路・依存変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 検査対象・結果・時点を実処理へ結び付けられる |

## Related requirements

[C6.2.2](../../../../controls/control-records/c06-supply-chain-security-for-models/v1.0-c6.2.2-cryptographically-signed-ai-bom-before-deployment/README.md)はBOM署名、[C6.2.3](../../../../controls/control-records/c06-supply-chain-security-for-models/v1.0-c6.2.3-fail-build-on-missing-ai-bom-component-metadata/README.md)は欠落時のBuild失敗。BOMの存在はどちらも単独では保証しない。
[C6 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

BOMは記載の真偽やSourceの無害性を証明しない。Providerが非開示の由来は未立証として扱い、形式を埋めるだけで保証を作らない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [C6.2 Section学習資料](../../../learning/c06-supply-chain-security-for-models/v1.0-c6.2-ai-bom-and-supply-chain-monitoring.md)：講義・想定問答。学習進捗とControl成熟度は独立。
- [AISVS v1.0 C6 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C06-Supply-Chain.md)
- [AISVS v1.0 C6 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C06-Supply-Chain/C06-02-AI-BOM-Supply-Chain-Monitoring.md)
- [C6 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
