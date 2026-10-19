---
title: すべての外部モデル構成物の完全性を検証可能にする
versioned_id: v1.0-C6.1.3
requirement_id: C6.1.3
verification_level: 2
family_id: C6
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C06-Supply-Chain.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C06-Supply-Chain/C06-01-Model-Artifact-Integrity.md
last_verified: '2026-10-18'
maturity: verifiable
mapping_assessment_refs: []
---

# すべての外部モデル構成物の完全性を検証可能にする

AISVS Verification Level: 2


## Upstream basis

AISVS `v1.0-C6.1.3`は、すべてのThird-party Model Artifactが完全性検証できる状態である。
対応Researchの手法・製品・版・追加対策は参考情報であり、原文の保証を実効的に確かめる条件と区別する。Research内のMappingを自動採用しない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

外部から採用する構成物と版を特定し、信頼できる期待Digestや署名等へ結び付ける。実際に照合できることを改変試験で示す。内部で初回取込み時にHashを作る場合、それは以後の不変性の基準であって元Publisher由来や初回の無害性を証明しない。

## Security objective

すべてのThird-party Model Artifactが完全性検証できる状態である。

## Applicability

第三者Modelと関連Artifact、または対象ModelのAI BOMを扱う取得・Import・Build・昇格経路に適用する。対象となる個別資産は下記SPと境界で特定する。

### Non-applicability

対象のThird-party ModelやArtifactを取得・Import・昇格しない境界は、Data Flowと責任分界を示して対象外を判断する。外部Providerで内部が見えないことは未立証として記録する。

## Scope and assumptions

対象Modelと構成物、版、Source、BOM、処理環境と責任者を特定する。信頼する基準の作成・更新者と権限を明示し、同じ名前から実体の一致を推定しない。試験は合成Dataや無害なFixtureを隔離環境で使用する。実製品での試験結果は本Repositoryへ保存せず期待証拠を定義する。

## Assets, actors, identities, and trust boundaries

Publisher・Mirror・保管から期待基準との照合へ移る境界。Source提供者、基準管理者、取得者、Verifier。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 外部Modelを構成する全対象と版を列挙し、検証可能な照合情報がある。 |
| SP-2 | 照合基準の信頼根拠を示し、Artifactと基準を同時に無断置換できない。 |
| SP-3 | 再取得・改変Fixtureで照合の成功と不一致を確認し、単なるHashの存在に留まらない。 |

## Scope calibration and adjacent assurance

C3.1.3は投入時と読込み時の実検証、C3.1.2は署名。本Controlの「検証できる」能力と、それぞれの実行点での強制を混同しない。

## Threat and failure-mode rationale

外部Artifactが転送・Mirror・Cacheで置換されても、期待する実体へ照合できずに使用される。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

外部から採用する構成物と版を特定し、信頼できる期待Digestや署名等へ結び付ける。実際に照合できることを改変試験で示す。内部で初回取込み時にHashを作る場合、それは以後の不変性の基準であって元Publisher由来や初回の無害性を証明しない。 実処理の呼出し順、入力版、結果と許可・拒否の扱いを点検する。

### Positive verification

合成Model一式の各構成物を期待基準へ照合する。未変更物は一致し、一つ変更した構成物は不一致と判定できることを示す。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 設定やTokenizerだけの照合情報を欠落させる | 全Artifactを検証可能とは判定しない。SP-1。 |
| N-2 | Artifactと付属Hashを同時に置換する | 信頼する基準との不一致または基準保護不足を検出する。SP-2。 |
| N-3 | 可変Aliasだけを記録し期待内容を保持しない | 同一性の検証根拠がないと判定する。SP-1、SP-3。 |

### Failure conditions

一つでも検証手段・期待基準がない、基準も同時に無断置換可能、変更を識別できない場合はFailまたは証拠不足。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象一覧・版とPolicy／設定 | Model・供給網基盤担当者 | 本Controlの対象Artifactと強制・確認点 | 対象・Policy・実装変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの範囲と実構成が一致する |
| 正例・負例の結果と処理Trace | 検証担当者 | 通常・代替・障害の対象経路 | 初回と処理経路・依存変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 検査対象・結果・時点を実処理へ結び付けられる |

## Related requirements

[C3.1.3](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.1.3-signature-verification-at-admission-and-load/README.md)は投入時と読込み時の実検証、[C3.1.2](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.1.2-authorized-signatures-for-all-model-artifacts/README.md)は署名。本Controlの「検証できる」能力と、それぞれの実行点での強制を混同しない。
[C6 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

正規に照合できるModelにも毒入れや脆弱性がある。署名や内部HashのScopeと信頼Assumptionを明示する。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C6 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C06-Supply-Chain.md)
- [AISVS v1.0 C6 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C06-Supply-Chain/C06-01-Model-Artifact-Integrity.md)
- [C6 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
