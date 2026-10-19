---
title: モデルをImportする前に悪意あるコードを検査する
versioned_id: v1.0-C6.1.1
requirement_id: C6.1.1
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

# モデルをImportする前に悪意あるコードを検査する

AISVS Verification Level: 1


## Upstream basis

AISVS `v1.0-C6.1.1`は、ModelをImportする前に悪意あるCodeをScanする。
対応Researchの手法・製品・版・追加対策は参考情報であり、原文の保証を実効的に確かめる条件と区別する。Research内のMappingを自動採用しない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

Modelの実体と補助Code・設定等の対象範囲を明確にし、危険なLoaderを起動するより前に検査する。検査対象とImport対象を一致させ、未対応形式やScanner障害を陰性と扱わない。複数ScannerやSandboxはResearchの補強策であり、原文が特定のTool数を要求するわけではない。

## Security objective

ModelをImportする前に悪意あるCodeをScanする。

## Applicability

第三者Modelと関連Artifact、または対象ModelのAI BOMを扱う取得・Import・Build・昇格経路に適用する。対象となる個別資産は下記SPと境界で特定する。

### Non-applicability

対象のThird-party ModelやArtifactを取得・Import・昇格しない境界は、Data Flowと責任分界を示して対象外を判断する。外部Providerで内部が見えないことは未立証として記録する。

## Scope and assumptions

対象Modelと構成物、版、Source、BOM、処理環境と責任者を特定する。信頼する基準の作成・更新者と権限を明示し、同じ名前から実体の一致を推定しない。試験は合成Dataや無害なFixtureを隔離環境で使用する。実製品での試験結果は本Repositoryへ保存せず期待証拠を定義する。

## Assets, actors, identities, and trust boundaries

取得隔離領域、Scanner、Cache、LoaderのImport境界。Model作者、取得者、検査者、Import実行者。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | Importする実Modelに対して悪意あるCodeのScanを実施する。 |
| SP-2 | ScanはImport前に完了し、検査した版とImportする版・構成物が対応する。 |
| SP-3 | 検出・陰性・未対応・障害を区別し、検査が成立していない対象をScan済み陰性として通さない。 |

## Scope calibration and adjacent assurance

C4.1.2の形式AllowlistやC4.1.1のSandboxと異なる。C6.1.4の振る舞い試験も悪意あるCodeの静的検査の代替ではない。

## Threat and failure-mode rationale

未信頼ModelがLoaderや補助Scriptを通してCodeを実行し、Import時点でCredentialやホストを侵害する。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

Modelの実体と補助Code・設定等の対象範囲を明確にし、危険なLoaderを起動するより前に検査する。検査対象とImport対象を一致させ、未対応形式やScanner障害を陰性と扱わない。複数ScannerやSandboxはResearchの補強策であり、原文が特定のTool数を要求するわけではない。 実処理の呼出し順、入力版、結果と許可・拒否の扱いを点検する。

### Positive verification

無害なClean Model Fixtureと検査用Markerを含むFixtureを隔離した取得経路へ渡し、Import前に結果が判定されることをTraceする。実Codeの検知精度は承認済み安全な検証Corpusで別に評価する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 検査後にModelや補助Fileを差し替える | 対象不一致を検出し、Scan済みとしてImportしない。SP-2。 |
| N-2 | ScannerをTimeout・未対応形式にする | 陰性へ読み替えない。SP-3。 |
| N-3 | Loader呼出しの後だけScanする | Import前検査の欠落と判定する。SP-1、SP-2。 |

### Failure conditions

Import前のScanがない、対象が一致しない、検査不能を陰性とする場合はFail。検知後に拒否するPolicyは重要な運用設計だが、本要件のScan実施と同一視しない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象一覧・版とPolicy／設定 | Model・供給網基盤担当者 | 本Controlの対象Artifactと強制・確認点 | 対象・Policy・実装変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの範囲と実構成が一致する |
| 正例・負例の結果と処理Trace | 検証担当者 | 通常・代替・障害の対象経路 | 初回と処理経路・依存変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 検査対象・結果・時点を実処理へ結び付けられる |

## Related requirements

[C4.1.2](../../../../controls/control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1.2-safe-serialization-format-allowlist-at-model-loading/README.md)の形式AllowlistやC4.1.1のSandboxと異なる。[C6.1.4](../../../../controls/control-records/c06-supply-chain-security-for-models/v1.0-c6.1.4-behavioral-acceptance-before-any-nondevelopment-promotion/README.md)の振る舞い試験も悪意あるCodeの静的検査の代替ではない。
[C6 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

Scannerの偽陰性・偽陽性、許可された操作を使う悪意あるCode、Scanner自身の脆弱性は残る。陰性は無害性の証明ではない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C6 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C06-Supply-Chain.md)
- [AISVS v1.0 C6 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C06-Supply-Chain/C06-01-Model-Artifact-Integrity.md)
- [C6 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
