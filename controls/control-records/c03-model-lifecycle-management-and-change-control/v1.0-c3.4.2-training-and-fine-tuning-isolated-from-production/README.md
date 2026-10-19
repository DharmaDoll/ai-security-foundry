---
title: 学習・追加学習環境を本番から分離する
versioned_id: v1.0-C3.4.2
requirement_id: C3.4.2
verification_level: 2
family_id: C3
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-04-Secure-Development-Practices.md
last_verified: '2026-10-18'
maturity: verifiable
mapping_assessment_refs: []
---

# 学習・追加学習環境を本番から分離する

AISVS Verification Level: 2

[C3.4 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.4-secure-development-practices.md)

## Upstream basis

AISVS `v1.0-C3.4.2`は、Modelの学習・Fine-tuning環境を本番環境から分離する。
Researchは別Projectという名称だけでなく、共有Credential、Secret、Network、Data Store、Registryや昇格経路から本番へ到達しないかを見る。SourceやDataset利用の適法性は分離とは別に評価する。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

学習JobやNotebookが侵害された場合でも、本番のDataや配備状態へ無制限に作用できないよう、Compute、Identity、通信、保存・昇格経路を分離する。承認されたDataを本番からExportして学習用Copyを渡す経路はあり得る。必要な受渡しを全禁止するのではなく、学習側が境界や本番への昇格を勝手に拡大できないことを確認する。

## Security objective

学習環境の侵害や誤操作が本番Credentialや配備先へ直接波及する範囲を抑える。

## Applicability

Training・Fine-tuning Cluster、Notebook、関連CI・Tracker・Dataset Store・Registryと、本番環境の間の境界を対象とする。委託先で学習する場合も責任分界と分離の証拠を確認する。

### Non-applicability

学習・Fine-tuningを行わない場合は、そのData FlowとProviderの役割を示して境界内の対象外を判断する。委託先で学習する場合は、その責任境界の分離確認を省かない。

## Scope and assumptions

対象Deployment、Model一式、版、Provider、Registryと実際の読込み経路を評価開始時に特定する。
名前やAliasが可変なら実体の識別方法を明示する。試験は隔離環境の無害な模擬Artifactで行い、
本番Dataや実行可能な不正Payloadを持ち込まない。証拠の対象版と現在の配備が一致するか確認する。

## Assets, actors, identities, and trust boundaries

学習Compute・Identityから本番Service、Data、Secretと配備先へ進む境界、および承認済みDataとModelの受渡し。学習者、Job、Platform管理者、本番運用者、昇格担当Identityが関わる。攻撃者は学習Codeや依存を実行し、Credential取得、直接書込み、Shared Storeや昇格権限経由のPivotを試みる。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 学習・Fine-tuningと本番のCompute・権限・通信・保存先を特定し、分離の強制点を示せる。 |
| SP-2 | 学習側の侵害を想定しても本番Secretや直接の配備書込みを利用できず、共通Credentialや無制限なNetwork経路で境界を迂回できない。 |
| SP-3 | 承認したData受渡しとModel昇格は範囲・方向・担当権限が制限され、学習Job自身が本番反映の審査や境界を変更できない。 |

## Scope calibration and adjacent assurance

C3.4.1は環境間のAI実行部品の非共有。C3.1はArtifactの署名・検証、C3.2は安全性評価であり、隔離した環境で作ったという事実だけでは代替できない。

## Threat and failure-mode rationale

侵害された学習依存やNotebookが本番のTokenを持っていると、分離されたProject内でも本番Registryへ不正Artifactを上書きできる。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

Notebookと実学習JobのIdentity・Secret・Network・Mount・Registry権限を確認する。別Projectでも共有Service Accountや本番へのWrite権限がないか、昇格処理を学習Jobが変更できないかを追う。

### Positive verification

本番相当から承認した合成DataをCopyとして渡し、学習JobはそのCopyのみを利用する。学習が完了しても本番へ直接反映できず、別の許可された昇格経路だけが模擬Artifactを反映できることを確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 学習JobのIdentityで本番SecretやModel配備先へアクセスする | 本番Secret取得や直接書込みが拒否される。SP-2。 |
| N-2 | 別ProjectのJobへ本番Credentialを同梱する | 実効分離の欠落を検出し、Project名の違いをPass証拠にしない。SP-1、SP-2。 |
| N-3 | 学習側から昇格Workflowや受渡しの対象範囲を変更する | 境界や承認を勝手に広げられない。SP-3。 |

### Failure conditions

学習Jobが本番権限を共有し直接配備を変更できる、共通Secretや無制限な接続で環境分離を迂回できる、学習側だけで昇格境界を変えられる場合はFail。承認された一方向のCopy利用だけで直ちにFailとはしない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 学習と本番のIdentity・接続・保存先の一覧 | 基盤・Identity管理者 | Notebook・Job・Registry・昇格 | 権限・構成変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 名称でなく実到達可能性と強制点を説明できる |
| 本番到達拒否と許可受渡し・昇格の試験 | 検証担当者 | 実学習Identityと承認経路 | 初回と境界・Policy変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 直接作用を拒否し、許可された受渡しのみ成功する |

## Related requirements

[C3.4.1](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.4.1-ai-runtime-component-separation-across-environments/README.md)は環境間のAI実行部品の非共有。C3.1はArtifactの署名・検証、C3.2は安全性評価であり、隔離した環境で作ったという事実だけでは代替できない。
[C3 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

分離の強さは共通管理基盤と権限設定へ依存する。本番由来Dataの学習利用の許可・機密性、Model品質や供給元の安全性は別の保証であり、隔離だけで解決しない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C3 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [AISVS v1.0 C3.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-04-Secure-Development-Practices.md)
- [C3.4 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.4-secure-development-practices.md)
- [C3 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
