---
title: 開発以外へ昇格する前に振る舞いの受入試験へ合格させる
versioned_id: v1.0-C6.1.4
requirement_id: C6.1.4
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

# 開発以外へ昇格する前に振る舞いの受入試験へ合格させる

AISVS Verification Level: 2


## Upstream basis

AISVS `v1.0-C6.1.4`は、Modelが開発環境以外のいずれかへ昇格する前に、Behavioral Acceptance Test Suiteへ合格する。
対応Researchの手法・製品・版・追加対策は参考情報であり、原文の保証を実効的に確かめる条件と区別する。Research内のMappingを自動採用しない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

用途に対応する安全性・望ましい動作・能力の境界と合否条件を先に定義し、実際に昇格するModel・設定へ適用する。対象は本番だけでなくStaging等も含む。原文は自動化方式や一律の数値基準を指定しない。

## Security objective

Modelが開発環境以外のいずれかへ昇格する前に、Behavioral Acceptance Test Suiteへ合格する。

## Applicability

第三者Modelと関連Artifact、または対象ModelのAI BOMを扱う取得・Import・Build・昇格経路に適用する。対象となる個別資産は下記SPと境界で特定する。

### Non-applicability

開発環境内の実験だけで、非開発環境への昇格がない場合はその構成を示す。Staging・検証用環境を開発と呼び替えてGateを省かない。

## Scope and assumptions

対象Modelと構成物、版、Source、BOM、処理環境と責任者を特定する。信頼する基準の作成・更新者と権限を明示し、同じ名前から実体の一致を推定しない。試験は合成Dataや無害なFixtureを隔離環境で使用する。実製品での試験結果は本Repositoryへ保存せず期待証拠を定義する。

## Assets, actors, identities, and trust boundaries

開発からStaging・本番等の昇格境界。Model管理者、評価担当者、Release Controllerと承認基準管理者。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 用途とScopeに対応した版管理された振る舞い受入試験・合否基準を持つ。 |
| SP-2 | 昇格対象の実Modelと設定でSuiteへ合格し、結果を対象へ結び付ける。 |
| SP-3 | すべての非開発環境への昇格で、合格前・失敗・未評価の昇格を防ぐ。 |

## Scope calibration and adjacent assurance

C3.2.1は配備前の三種の自動試験。本Controlは非開発環境への昇格前の振る舞い受入合格であり、自動化・時点・対象の違いを保つ。

## Threat and failure-mode rationale

署名とCode Scanが成功したModelに危険な癖があっても、Stagingや検証先へ無試験で昇格する。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

用途に対応する安全性・望ましい動作・能力の境界と合否条件を先に定義し、実際に昇格するModel・設定へ適用する。対象は本番だけでなくStaging等も含む。原文は自動化方式や一律の数値基準を指定しない。 実処理の呼出し順、入力版、結果と許可・拒否の扱いを点検する。

### Positive verification

無害な通常質問と用途別の境界試験を対象Modelへ行い、合格した版だけが開発から模擬Stagingへ昇格できることを確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 不合格または未実行の結果で昇格する | Staging等でも拒否する。SP-3。 |
| N-2 | 別Model版の合格結果を提出する | 対象不一致で拒否する。SP-2。 |
| N-3 | 本番Gateを迂回して検証環境へ直接登録する | 非開発環境の昇格経路として同じ合格条件を要求する。SP-3。 |

### Failure conditions

Suiteや基準がない、対象Modelが未合格、非開発環境への昇格に未評価経路がある場合はFail。試験を実施しただけでは足りない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象一覧・版とPolicy／設定 | Model・供給網基盤担当者 | 本Controlの対象Artifactと強制・確認点 | 対象・Policy・実装変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの範囲と実構成が一致する |
| 正例・負例の結果と処理Trace | 検証担当者 | 通常・代替・障害の対象経路 | 初回と処理経路・依存変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 検査対象・結果・時点を実処理へ結び付けられる |

## Related requirements

[C3.2.1](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.2.1-automated-input-safety-output-tests-before-deployment/README.md)は配備前の三種の自動試験。本Controlは非開発環境への昇格前の振る舞い受入合格であり、自動化・時点・対象の違いを保つ。
[C6 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

有限Suite、評価条件への過適応、評価環境と実環境の差が残る。合格は無条件の安全性認定ではない。
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
