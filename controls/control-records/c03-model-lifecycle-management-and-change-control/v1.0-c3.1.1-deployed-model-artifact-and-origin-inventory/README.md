---
title: 本番モデルの全構成物と出所を台帳で把握する
versioned_id: v1.0-C3.1.1
requirement_id: C3.1.1
verification_level: 1
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

# 本番モデルの全構成物と出所を台帳で把握する

AISVS Verification Level: 1

[C3.1 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.1-model-authorization-and-integrity.md)

## Upstream basis

AISVS `v1.0-C3.1.1`は、Model Registryで配備済みの全Model Artifactとその出所の台帳を維持する。
Researchは、台帳と実際のServing環境を照合し、名前だけの登録でShadow Deploymentを見逃さないことを重視する。BOM出力やScanner結果の登録も例示するが、特定のBOM形式、Scannerや配備拒否の仕組みは本要件の直接の必須条件ではない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

配備中のModelについて、重みだけでなく挙動を形作る設定、Tokenizer、Adapter、安全性・Policy Model等を列挙し、識別可能な版と出所をRegistryへ記録する。本番の実体から記録へ、記録から実体へ照合できることが重要である。Registry製品が導入済みでも、実際に読み込まれるArtifactが一覧の外にあれば十分ではない。

## Security objective

未把握のModel構成物を減らし、問題が判明したSourceや版を使う配備先を特定できるようにする。

## Applicability

本番で使う基盤Model、Fine-tune、Adapter、Tokenizer、設定、安全性・Policy Model等を対象とする。API提供型の場合はProvider、Model識別子、契約・Routingと得られる内部台帳の証拠を整理し、利用者側のEndpoint一覧だけでProvider内部の全Artifactを把握したとは言わない。

### Non-applicability

対象境界でModel Artifactを管理・配備しない場合は責任分界を明示する。
外部Providerで内部が見えないことは、Provider側で要件が存在しない理由にはならない。
利用者が確認できない範囲は証拠不足として残し、対象外やPassへ読み替えない。

## Scope and assumptions

対象Deployment、Model一式、版、Provider、Registryと実際の読込み経路を評価開始時に特定する。
名前やAliasが可変なら実体の識別方法を明示する。試験は隔離環境の無害な模擬Artifactで行い、
本番Dataや実行可能な不正Payloadを持ち込まない。証拠の対象版と現在の配備が一致するか確認する。

## Assets, actors, identities, and trust boundaries

外部Source・Buildや学習処理で作られたArtifactから、Registryの登録対象へ、そこから実際の本番配備・読込みへ進む境界。資産は構成物の識別と来歴、配備状態との対応。Model提供者、登録者、配備者、Serving Workerが関わる。攻撃者や誤操作がRegistryを経ない配備、補助Fileの追加、可変Aliasの差替えを行う経路を想定する。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 配備中の全ArtifactをRegistryで識別し、出所へ辿れる。重み以外の実際に使う構成物も範囲に含む。 |
| SP-2 | 登録した版と本番で解決・読込みされる実体が対応する。単なる可変の名前やURLだけで同一性を推定しない。 |
| SP-3 | 配備追加・切替・撤去とSource変更を台帳へ反映し、本番との照合で欠落・不一致を発見できる。 |

## Scope calibration and adjacent assurance

C3.1.2は全Artifactへの権限ある主体の署名、C3.1.3は署名の検証点。本要件の台帳は正当性や安全性を単独で証明しない。C6の供給元評価やAI BOMは関連資料だが、Registryと配備の照合を自動的に代替しない。

## Threat and failure-mode rationale

重みだけを登録し、後から追加したAdapterや安全性Modelが台帳外で動くと、侵害されたSourceの影響範囲や復旧対象を特定できない。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

全Serving Endpoint・WorkerとFallbackを列挙し、起動設定・解決先・実際に読むFile一覧をRegistryへ突き合わせる。登録されたArtifactの出所資料と作成・取得記録を標本照合する。

### Positive verification

基盤Model、Adapter、設定、Tokenizer、安全性Modelを含む模擬配備を作る。各構成物の版・出所をRegistryへ登録し、実際の配備一覧と双方から一致を確認する。版の切替と撤去を行い記録も追従することを確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 台帳外の安全性ModelやFallbackを追加する | 本番との照合で未登録物を検出し、台帳完全とは判定しない。SP-1、SP-3。 |
| N-2 | Model名を保ったまま設定やAdapterの版を変える | 実体と台帳の差を観測し、同じ名前を同一版の根拠にしない。SP-2。 |
| N-3 | 出所を削除する、または不明なSource名だけを記録する | 追跡性の欠落として検出し、全Artifactの出所を把握したとは判定しない。SP-1。 |

### Failure conditions

配備済みArtifactの欠落、版・実体の不一致、出所を辿れない登録がある場合はFailまたは証拠不足。台帳の存在や担当者の「把握している」という説明だけではPassにしない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| Registry Exportと出所資料 | Model管理者 | 全配備Artifactと版・Source | 配備・変更ごと | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 記載が実体と一致し、Sourceを追える |
| 双方向の照合記録 | Serving運用者と検証担当者 | Endpoint・Fallback・補助構成物 | 採用時と配備変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 未登録・不一致を検出する負例も含む |

## Related requirements

[C3.1.2](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.1.2-authorized-signatures-for-all-model-artifacts/README.md)は全Artifactへの権限ある主体の署名、[C3.1.3](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.1.3-signature-verification-at-admission-and-load/README.md)は署名の検証点。本要件の台帳は正当性や安全性を単独で証明しない。C6の供給元評価やAI BOMは関連資料だが、Registryと配備の照合を自動的に代替しない。
[C3 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

内部Artifactを開示しないProviderでは確認可能性が限られる。台帳が正確でも、正規Sourceに悪意ある内容が含まれる可能性は残る。BOMを出力できることは完全性の証明ではない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C3 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [AISVS v1.0 C3.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-01-Model-Authorization-Integrity.md)
- [C3.1 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.1-model-authorization-and-integrity.md)
- [C3 Family概要](../README.md)

- [関連Insight：復旧するのはファイルではなく、整合したシステムの状態](../../../../docs/insights/recovery-restores-a-consistent-configuration.md)（Repositoryの横断的な考察。規範やMappingではない）

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
