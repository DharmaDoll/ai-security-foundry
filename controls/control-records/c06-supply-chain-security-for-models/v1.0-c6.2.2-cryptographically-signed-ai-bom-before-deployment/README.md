---
title: AI BOMへ配備前に暗号署名する
versioned_id: v1.0-C6.2.2
requirement_id: C6.2.2
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

# AI BOMへ配備前に暗号署名する

AISVS Verification Level: 2


## Upstream basis

AISVS `v1.0-C6.2.2`は、AI BOMへ配備前に暗号署名を付ける。
対応Researchの手法・製品・版・追加対策は参考情報であり、原文の保証を実効的に確かめる条件と区別する。Research内のMappingを自動採用しない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

配備対象に対応するBOMの実内容を署名へ結び付ける。署名の存在だけでなく、対象内容・Signerと署名時点を確認して成立を示す。特定Tool・透明性Log・署名封筒形式は必須ではない。

## Security objective

AI BOMへ配備前に暗号署名を付ける。

## Applicability

第三者Modelと関連Artifact、または対象ModelのAI BOMを扱う取得・Import・Build・昇格経路に適用する。対象となる個別資産は下記SPと境界で特定する。

### Non-applicability

Model Artifactを作成・利用しない境界は責任分界を示す。BOMを生成していないことやProviderが非開示であることだけで対象外にせず、証拠不足を残す。

## Scope and assumptions

対象Modelと構成物、版、Source、BOM、処理環境と責任者を特定する。信頼する基準の作成・更新者と権限を明示し、同じ名前から実体の一致を推定しない。試験は合成Dataや無害なFixtureを隔離環境で使用する。実製品での試験結果は本Repositoryへ保存せず期待証拠を定義する。

## Assets, actors, identities, and trust boundaries

生成済みBOMから署名・配備へ進む境界。生成者、署名者、鍵管理者とRelease担当者。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 配備対象のBOM版・内容に結び付く有効な暗号署名がある。 |
| SP-2 | 署名Identityと信頼根拠を確認し、別内容・別BOMの署名を流用しない。 |
| SP-3 | 署名が配備より前に完了し、その後のBOM変更には対応する署名を用意する。 |

## Scope calibration and adjacent assurance

C6.2.1はBOM内容・提供、C6.2.3は完全性チェック。署名済みでも欠落・誤記したBOMはあり得る。配備時Verifierの強制は本要件の署名事実とは分けて運用設計する。

## Threat and failure-mode rationale

生成後のBOMを差し替え、危険な構成や由来を隠して配備する。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

配備対象に対応するBOMの実内容を署名へ結び付ける。署名の存在だけでなく、対象内容・Signerと署名時点を確認して成立を示す。特定Tool・透明性Log・署名封筒形式は必須ではない。 実処理の呼出し順、入力版、結果と許可・拒否の扱いを点検する。

### Positive verification

合成Model版に対応するBOMへ署名し、検証で内容との一致を確認する。署名時点と配備時点、配備に対応するBOM版を追えるよう記録する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 配備後に署名を付ける | 配備前という条件を満たさない。SP-3。 |
| N-2 | 署名済みBOMの内容を変更する | 署名との不一致を検出する。SP-1、SP-2。 |
| N-3 | 別ModelのBOM署名を添付する | 対象不一致として検出する。SP-2。 |

### Failure conditions

未署名、無効署名、別内容への署名、配備後の署名しかない場合はFail。Model本体の署名をBOM署名の代わりにしない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象一覧・版とPolicy／設定 | Model・供給網基盤担当者 | 本Controlの対象Artifactと強制・確認点 | 対象・Policy・実装変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの範囲と実構成が一致する |
| 正例・負例の結果と処理Trace | 検証担当者 | 通常・代替・障害の対象経路 | 初回と処理経路・依存変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 検査対象・結果・時点を実処理へ結び付けられる |

## Related requirements

[C6.2.1](../../../../controls/control-records/c06-supply-chain-security-for-models/v1.0-c6.2.1-versioned-machine-readable-ai-bom-for-every-model/README.md)はBOM内容・提供、[C6.2.3](../../../../controls/control-records/c06-supply-chain-security-for-models/v1.0-c6.2.3-fail-build-on-missing-ai-bom-component-metadata/README.md)は完全性チェック。署名済みでも欠落・誤記したBOMはあり得る。配備時Verifierの強制は本要件の署名事実とは分けて運用設計する。
[C6 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

正当なSignerによる虚偽記載やIdentity侵害は残る。署名は内容が正しいという保証ではない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C6 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C06-Supply-Chain.md)
- [AISVS v1.0 C6 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C06-Supply-Chain/C06-02-AI-BOM-Supply-Chain-Monitoring.md)
- [C6 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
