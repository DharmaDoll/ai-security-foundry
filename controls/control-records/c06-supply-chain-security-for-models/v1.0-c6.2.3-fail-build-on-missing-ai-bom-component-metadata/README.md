---
title: AI BOMの構成Metadata欠落時にBuildを失敗させる
versioned_id: v1.0-C6.2.3
requirement_id: C6.2.3
verification_level: 2
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

# AI BOMの構成Metadata欠落時にBuildを失敗させる

AISVS Verification Level: 2


## Upstream basis

AISVS `v1.0-C6.2.3`は、AI BOM完全性チェックで構成要素のMetadata欠落を見つけたらBuildを失敗させる。
対応Researchの手法・製品・版・追加対策は参考情報であり、原文の保証を実効的に確かめる条件と区別する。Research内のMappingを自動採用しない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

対象Modelの実構成と必要Metadataを定義し、値の欠落・空欄と構成要素そのものの漏れを検出する。Schema適合や生成成功だけを完全性とみなさず、同じ検査を実Buildの失敗へ接続する。外部非開示は自動Passの理由にしない。

## Security objective

AI BOM完全性チェックで構成要素のMetadata欠落を見つけたらBuildを失敗させる。

## Applicability

第三者Modelと関連Artifact、または対象ModelのAI BOMを扱う取得・Import・Build・昇格経路に適用する。対象となる個別資産は下記SPと境界で特定する。

### Non-applicability

Model Artifactを作成・利用しない境界は責任分界を示す。BOMを生成していないことやProviderが非開示であることだけで対象外にせず、証拠不足を残す。

## Scope and assumptions

対象Modelと構成物、版、Source、BOM、処理環境と責任者を特定する。信頼する基準の作成・更新者と権限を明示し、同じ名前から実体の一致を推定しない。試験は合成Dataや無害なFixtureを隔離環境で使用する。実製品での試験結果は本Repositoryへ保存せず期待証拠を定義する。

## Assets, actors, identities, and trust boundaries

BOM生成からCI完全性判定、Build結果とPublishへ進む境界。生成器、Policy管理者、CI実行者。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 実構成に対する構成要素と必要Metadataの完全性Policyを版管理する。 |
| SP-2 | BuildでPolicyを適用し、欠落・空欄や対象成分の未記載を検出する。 |
| SP-3 | 不足を検出したBuildは非成功で停止し、検査未実行・障害をPassへ読み替えない。 |

## Scope calibration and adjacent assurance

C6.2.1は情報を持つBOM、C6.2.2は署名。本ControlのBuild失敗は別に検証する。必要MetadataのScopeを隠して狭めない。

## Threat and failure-mode rationale

BOM生成成功がBuild成功とみなされ、由来・License等が空のまま配布される。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

対象Modelの実構成と必要Metadataを定義し、値の欠落・空欄と構成要素そのものの漏れを検出する。Schema適合や生成成功だけを完全性とみなさず、同じ検査を実Buildの失敗へ接続する。外部非開示は自動Passの理由にしない。 実処理の呼出し順、入力版、結果と許可・拒否の扱いを点検する。

### Positive verification

全必要情報を持つ合成BOMと実構成一覧でBuildが成功することを示す。同じBuild Commandへ欠落Fixtureを渡し、非成功結果と後続Publishが進まないことを観測する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | Dataset Originや重みの必要Metadataを一項目ずつ削除する | 完全性検査で検出しBuildが失敗する。SP-2、SP-3。 |
| N-2 | 成分をBOMから丸ごと削除する | 実構成との照合で漏れを検出する。SP-1、SP-2。 |
| N-3 | 検査Jobを停止・Timeoutさせる、結果を無視する | Build成功へ進まず、未評価を区別する。SP-3。 |

### Failure conditions

欠落を検出しない、WarningだけでBuild成功、検査障害が成功へFallbackする場合はFail。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象一覧・版とPolicy／設定 | Model・供給網基盤担当者 | 本Controlの対象Artifactと強制・確認点 | 対象・Policy・実装変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの範囲と実構成が一致する |
| 正例・負例の結果と処理Trace | 検証担当者 | 通常・代替・障害の対象経路 | 初回と処理経路・依存変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 検査対象・結果・時点を実処理へ結び付けられる |

## Related requirements

[C6.2.1](../../../../controls/control-records/c06-supply-chain-security-for-models/v1.0-c6.2.1-versioned-machine-readable-ai-bom-for-every-model/README.md)は情報を持つBOM、[C6.2.2](../../../../controls/control-records/c06-supply-chain-security-for-models/v1.0-c6.2.2-cryptographically-signed-ai-bom-before-deployment/README.md)は署名。本ControlのBuild失敗は別に検証する。必要MetadataのScopeを隠して狭めない。
[C6 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

Metadataが埋まっていても内容の真偽や正当性は保証しない。検査器と構成一覧が共に侵害されるRisk、未知の成分を見逃すRiskは残る。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## 関連する洞察

個別要件の理解・設計レビューを助ける参照であり、追加要件や正式なMappingではない。

- [AI BOMの技術構造と実構成を確かめるための証拠](../../../../docs/insights/ai-bom-inventory-evidence-and-trust.md)：実構成の記載漏れと必須情報の欠落を検出し、Buildを止める観点を確認する。

## References

- [C6.2 Section学習資料](../../../learning/c06-supply-chain-security-for-models/v1.0-c6.2-ai-bom-and-supply-chain-monitoring.md)：講義・想定問答。学習進捗とControl成熟度は独立。
- [AISVS v1.0 C6 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C06-Supply-Chain.md)
- [AISVS v1.0 C6 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C06-Supply-Chain/C06-02-AI-BOM-Supply-Chain-Monitoring.md)
- [C6 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
