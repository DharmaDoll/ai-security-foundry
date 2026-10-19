---
title: モデル構成物のすべてへ権限ある主体が署名する
versioned_id: v1.0-C3.1.2
requirement_id: C3.1.2
verification_level: 2
family_id: C3
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-01-Model-Authorization-Integrity.md
last_verified: '2026-10-18'
maturity: verifiable
mapping_assessment_refs: []
---

# モデル構成物のすべてへ権限ある主体が署名する

AISVS Verification Level: 2

[C3.1 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.1-model-authorization-and-integrity.md)

## Upstream basis

AISVS `v1.0-C3.1.2`は、重み・設定・Tokenizer・基盤Model・Fine-tune・Adapter・安全性／Policy Model等の全Artifactへ、権限ある主体による暗号署名を付ける。
Researchは、重み以外の設定やCheckpoint付属物も対象に含めること、数学的に有効な署名とそのReleaseを署名する権限を区別することを強調する。OMSやSigstore等は手段の例であり、特定製品は必須ではない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

本番でModelを構成する実体の集合を確定し、全構成物の内容に結び付いた暗号署名を持たせる。一つの署名済みManifestで全Fileを束ねる方式でもよいが、Fileパス・内容・版が署名範囲へ含まれ、対象を抜いたり別物へ置換したりできないことが必要である。署名者が対象ReleaseやArtifact種別を署名してよい主体かを確認する。

## Security objective

無署名の付属物や権限のない署名者の成果物を、承認されたModel一式だと誤認しないようにする。

## Applicability

本番用Modelを構成する全Artifactと、そのReleaseへ署名する主体・Workflowを対象とする。読み込む補助状態や実行Codeも構成物なら漏らさない。外部API型ではProvider側の署名Scopeと証拠を確認する。

### Non-applicability

対象境界でModel Artifactを管理・配備しない場合は責任分界を明示する。
外部Providerで内部が見えないことは、Provider側で要件が存在しない理由にはならない。
利用者が確認できない範囲は証拠不足として残し、対象外やPassへ読み替えない。

## Scope and assumptions

対象Deployment、Model一式、版、Provider、Registryと実際の読込み経路を評価開始時に特定する。
名前やAliasが可変なら実体の識別方法を明示する。試験は隔離環境の無害な模擬Artifactで行い、
本番Dataや実行可能な不正Payloadを持ち込まない。証拠の対象版と現在の配備が一致するか確認する。

## Assets, actors, identities, and trust boundaries

Model作者・提供者・Build処理から、Release一式への署名と配布へ移る境界。資産はModel内容と署名、対象集合、署名権限Policyと鍵／署名Identity。攻撃者は未署名Sidecarを追加する、署名対象を一部へ狭める、別の署名Identityで正規品に見せることを試みる。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 実際にModelを構成する全Artifactの内容が暗号署名へ結び付き、対象集合と版を確認できる。 |
| SP-2 | 署名者が当該Artifact・Releaseへ権限を持つと確認できる。単に任意の有効な証明書や署名を受け入れない。 |
| SP-3 | 重み以外の変更・追加も対象集合と署名へ反映され、旧署名を別内容へ流用できない。 |

## Scope calibration and adjacent assurance

C3.1.1は配備物と出所の台帳、C3.1.3は投入・読込み時の実際の署名検証。署名が存在しても検証が実行される保証はなく、C3.1.3を別に試す。安全性の評価はC3.2の保証。

## Threat and failure-mode rationale

重みは署名済みでも、署名対象外の設定や補助Fileを攻撃者が置き換えれば、読込み先やModelの挙動を変更できる。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

Registryと読込み構成から署名対象を列挙する。署名Workflow、ManifestのInclude／Exclude、署名Identity・Issuer・鍵と権限Policyを確認する。配布Bundleと署名範囲が一致するか点検する。

### Positive verification

模擬Model一式に権限を持つ主体が署名し、全Fileとその内容が署名に結び付くことを独立した検証で確認する。正当な設定変更時は新しい内容へ署名が付くことも確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 重みだけ署名し設定またはTokenizerを対象外にする | 署名範囲の欠落を検出し、全Artifact署名済みと判定しない。SP-1。 |
| N-2 | 無権限のIdentityで有効な署名を作る | 暗号検証が通っても署名者の権限条件を満たさないと判定する。SP-2。 |
| N-3 | 署名後にAdapterや付属状態を変更・追加する | 署名対象との不一致または未署名物を検出する。SP-1、SP-3。 |

### Failure conditions

構成物の一部に署名がない、署名対象が実内容と結び付かない、署名者の権限が確認できない場合はFailまたは証拠不足。Hashのみを署名と呼ばない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 署名済みBundle・対象Manifest | 権限あるRelease処理 | 全構成物・版・内容Digest | 各Release時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 未署名物がなく実内容へ署名が結び付く |
| 署名権限Policyと検証結果 | Release管理者と検証担当者 | Identity・Issuer／鍵と対象Release | 権限・鍵変更と各Release時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 有効だが権限外の署名を区別できる |

## Related requirements

[C3.1.1](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.1.1-deployed-model-artifact-and-origin-inventory/README.md)は配備物と出所の台帳、[C3.1.3](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.1.3-signature-verification-at-admission-and-load/README.md)は投入・読込み時の実際の署名検証。署名が存在しても検証が実行される保証はなく、[C3.1.3](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.1.3-signature-verification-at-admission-and-load/README.md)を別に試す。安全性の評価はC3.2の保証。
[C3 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

正当に署名された悪意ある内容や署名Identityの侵害は残る。暗号署名はModelの安全性、品質、公平性を保証しない。署名方式の暗号強度や鍵管理の詳細は環境に合わせて評価する。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C3 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [AISVS v1.0 C3.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-01-Model-Authorization-Integrity.md)
- [C3.1 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.1-model-authorization-and-integrity.md)
- [C3 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
