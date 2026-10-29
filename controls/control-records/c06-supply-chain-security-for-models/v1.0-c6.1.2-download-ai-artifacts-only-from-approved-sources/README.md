---
title: 重み・データセット・Adapterを承認した取得元へ限定する
versioned_id: v1.0-C6.1.2
requirement_id: C6.1.2
verification_level: 1
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

# 重み・データセット・Adapterを承認した取得元へ限定する

AISVS Verification Level: 1


## Upstream basis

AISVS `v1.0-C6.1.2`は、Model重み、Dataset、Fine-tuning Adapterを承認済みSourceからのみDownloadする。
対応Researchの手法・製品・版・追加対策は参考情報であり、原文の保証を実効的に確かめる条件と区別する。Research内のMappingを自動採用しない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

承認範囲をRegistryのドメインだけでなくPublisher・Repository・Artifact種別等で定義し、実際に解決される取得先へ適用する。推移依存、Redirect、Loaderの暗黙Downloadも対象とし、名前や人気だけを承認の根拠にしない。

## Security objective

Model重み、Dataset、Fine-tuning Adapterを承認済みSourceからのみDownloadする。

## Applicability

第三者Modelと関連Artifact、または対象ModelのAI BOMを扱う取得・Import・Build・昇格経路に適用する。対象となる個別資産は下記SPと境界で特定する。

### Non-applicability

対象のThird-party ModelやArtifactを取得・Import・昇格しない境界は、Data Flowと責任分界を示して対象外を判断する。外部Providerで内部が見えないことは未立証として記録する。

## Scope and assumptions

対象Modelと構成物、版、Source、BOM、処理環境と責任者を特定する。信頼する基準の作成・更新者と権限を明示し、同じ名前から実体の一致を推定しない。試験は合成Dataや無害なFixtureを隔離環境で使用する。実製品での試験結果は本Repositoryへ保存せず期待証拠を定義する。

## Assets, actors, identities, and trust boundaries

Registry・Publisherから取得Client・Loaderへの境界。承認者、Network制御、Proxy、Source管理者。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 三種類の対象Artifactについて承認Sourceと承認責任を明示する。 |
| SP-2 | 実Download先を承認Policyへ照合し、未承認Sourceからの取得を拒否する。 |
| SP-3 | 自動依存取得・Redirect・Fallbackでも同じ制限を保つ。 |

## Scope calibration and adjacent assurance

C6.1.1は悪意あるCode、C6.1.3は内容の完全性。承認Sourceでも侵害され得るため本要件のPassを無害性とみなさない。

## Threat and failure-mode rationale

承認Registryと同じドメイン内の偽Publisherや補助Adapter、Redirectから不正Dataを取得する。
ATLAS Content `2026.10`の`AML.T0010.003`との関係を`proposed`として評価した。
[対応の根拠・範囲・限界](../../../atlas-mapping-review-2026-10.md#c6)を参照。
正本はCatalogの`threat_mappings`であり、ResearchのMappingの転載や製品適合の主張ではない。

## Verification

### Architecture and configuration review

承認範囲をRegistryのドメインだけでなくPublisher・Repository・Artifact種別等で定義し、実際に解決される取得先へ適用する。推移依存、Redirect、Loaderの暗黙Downloadも対象とし、名前や人気だけを承認の根拠にしない。 実処理の呼出し順、入力版、結果と許可・拒否の扱いを点検する。

### Positive verification

承認した模擬Sourceから重み・Dataset・Adapterを取得できることを示し、実解決先と取得版を記録する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 同じRegistryの未承認Publisher・Repositoryを指定する | 拒否する。ドメイン許可だけで承認済みとしない。SP-1、SP-2。 |
| N-2 | 許可先から未承認先へRedirectする | 最終取得先のPolicyで拒否する。SP-3。 |
| N-3 | Loaderが未承認Adapterを暗黙取得する | 通常取得と同じ制限で拒否する。SP-3。 |

### Failure conditions

対象のいずれかを未承認SourceからDownloadできる、暗黙取得経路が迂回する場合はFail。Policy文書だけで実制限がなければ満たせない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象一覧・版とPolicy／設定 | Model・供給網基盤担当者 | 本Controlの対象Artifactと強制・確認点 | 対象・Policy・実装変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの範囲と実構成が一致する |
| 正例・負例の結果と処理Trace | 検証担当者 | 通常・代替・障害の対象経路 | 初回と処理経路・依存変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 検査対象・結果・時点を実処理へ結び付けられる |

## Related requirements

[C6.1.1](../../../../controls/control-records/c06-supply-chain-security-for-models/v1.0-c6.1.1-malicious-code-scan-before-model-import/README.md)は悪意あるCode、[C6.1.3](../../../../controls/control-records/c06-supply-chain-security-for-models/v1.0-c6.1.3-integrity-verifiability-for-every-third-party-model-artifact/README.md)は内容の完全性。承認Sourceでも侵害され得るため本要件のPassを無害性とみなさない。
[C6 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

承認判断の誤りや承認済みPublisherの侵害は残る。版固定は有益な実装例だが、Source承認と安全性の継続評価を分ける。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [C6.1 Section学習資料](../../../learning/c06-supply-chain-security-for-models/v1.0-c6.1-model-artifact-integrity.md)：講義・想定問答。学習進捗とControl成熟度は独立。
- [AISVS v1.0 C6 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C06-Supply-Chain.md)
- [AISVS v1.0 C6 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C06-Supply-Chain/C06-01-Model-Artifact-Integrity.md)
- [C6 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
| 2026-10-29 | ATLAS Content 2026.10との対応を評価。要件解釈・成熟度は維持 | 固定版ATLASとRepository独自の比較 | [対応案](../../../atlas-mapping-review-2026-10.md#c6)。人のレビュー・製品試験は未実施 |
