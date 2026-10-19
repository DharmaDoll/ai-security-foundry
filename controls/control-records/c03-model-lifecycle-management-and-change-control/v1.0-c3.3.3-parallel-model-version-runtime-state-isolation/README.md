---
title: 並行稼働するモデル版の実行状態を分離する
versioned_id: v1.0-C3.3.3
requirement_id: C3.3.3
verification_level: 2
family_id: C3
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-03-Controlled-Deployment-Rollback.md
last_verified: '2026-10-18'
maturity: verifiable
mapping_assessment_refs: []
---

# 並行稼働するモデル版の実行状態を分離する

AISVS Verification Level: 2

[C3.3 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.3-controlled-deployment-and-rollback.md)

## Upstream basis

AISVS `v1.0-C3.3.3`は、並行稼働するModel版はRuntime Stateを分離し、AI固有の共有資源をDeployment間で共用しないようにする。
ResearchはKV Cache、Prompt Cache、Session、Retrieval状態等の版間混入を扱う。同じ物理Serviceでも状態とアクセスが強制分離される構成はあり得るが、Namespace名やRoutingのStickinessだけでは分離の証拠にならない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

Stable・Canary・Shadow等の版を同時に動かすとき、片方の会話・中間計算結果・版固有の検索状態を他方が取得・変更・再利用できないようにする。共有Storeを使うなら、版Identityで強制される分離を実測する。共通のKey接頭辞を付けるだけで、Workerが他版の状態を自由に読める設計は十分でない。

## Security objective

版間の情報混入とCanary評価の汚染を防ぎ、ある版の状態を別版が誤って信頼しないようにする。

## Applicability

複数Model版が並行して稼働するDeploymentと、その会話・Session・KV／Prompt Cache・版固有Retrieval状態を対象とする。単一版しか稼働しないなら、更新時に旧版が残る期間も確認したうえで対象外を判断する。

### Non-applicability

並行稼働する版がない場合は、その構成と更新時の移行期間を示して対象外にできる。CanaryやShadowも並行版に含め、同じService名かどうかだけで対象外を判断しない。

## Scope and assumptions

対象Deployment、Model一式、版、Provider、Registryと実際の読込み経路を評価開始時に特定する。
名前やAliasが可変なら実体の識別方法を明示する。試験は隔離環境の無害な模擬Artifactで行い、
本番Dataや実行可能な不正Payloadを持ち込まない。証拠の対象版と現在の配備が一致するか確認する。

## Assets, actors, identities, and trust boundaries

Stable、Canary、Shadowの各Runtime Identityと状態領域の間の境界。資産は要求・会話Data、推論中間結果、版固有の検索・Cache状態と評価の独立性。各Worker、Cache／Store、Routerが関わる。攻撃者や誤実装はKey衝突、他版ID指定、共有Credentialで越境し得る。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 並行DeploymentのRuntime状態とAI固有資源を列挙し、各版の境界を定義する。 |
| SP-2 | 他版の状態の読出し・書込み・再利用を実際のWorker経路で防ぎ、版名の自己申告だけに依存しない。 |
| SP-3 | 再起動・Scale・Cache Hit・階層化した保存先でも分離を保ち、意図しない越境を観測できる。 |

## Scope calibration and adjacent assurance

C3.3.1のTraffic制御とC3.3.2の復元とは別。本Controlの版間分離だけでC5のTenant間認可が成立するわけではない。C3.4.1は開発・検証・本番という環境間の分離を扱う。

## Threat and failure-mode rationale

CanaryがStableのKV Cacheや会話を再利用すると、情報混入に加え、候補版の評価が旧版の状態で歪む。逆方向の共有はStableへ未承認状態を持ち込む。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

並行版のIdentity、Cache Key、権限、保存Prefix、メモリとOffload先を追う。Routing固定と状態分離を区別し、同じCredentialやKeyを用いた越境経路がないか点検する。

### Positive verification

A版とB版で別々の無害なMarkerをSessionやCacheに保存し、それぞれは自己の状態を使えることを確認する。同じ問い合わせでも他版のMarkerや中間状態が再利用されず、実際のWorker権限で分離されることを観測する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | BのWorkerからAのSession IDやCache Keyを指定する | Aの状態を取得・変更・再利用できない。SP-2。 |
| N-2 | 同じ入力で両版へ要求しCache Hitを誘発する | 他版の中間状態にHitしないことを内容・Cache Trace等で確認する。SP-2。 |
| N-3 | Scaleや再起動後に二次保存先から状態を復元する | Prefix・権限・版の対応を保ち、旧版や他版の状態を取り込まない。SP-3。 |

### Failure conditions

並行版が同じRuntime状態を読書き・再利用できる、版IDや接頭辞を変えるだけで越境できる、二次保存先や再起動経路で分離が崩れる場合はFail。物理Service共用だけを根拠に即Failとはしない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 版と状態資源・権限の対応表 | Serving基盤担当者 | 並行版・Cache・Session・Offload先 | 配備・構成変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 全状態の版境界と実際の強制点を説明できる |
| 越境・Cache再利用・再起動試験 | 検証担当者 | 実Worker Identityと全状態経路 | 初回とStore・Runtime変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 自己状態の利用成功と他版への越境拒否を示す |

## Related requirements

[C3.3.1](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.3.1-controlled-rollout-with-automated-rollback-triggers/README.md)のTraffic制御とC3.3.2の復元とは別。本Controlの版間分離だけでC5のTenant間認可が成立するわけではない。[C3.4.1](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.4.1-ai-runtime-component-separation-across-environments/README.md)は開発・検証・本番という環境間の分離を扱う。
[C3 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

論理分離はStore・Runtime自体が侵害された場合の防御を保証しない。共有GPU等の残余情報やSide Channelは構成別に評価し、Namespaceだけで全漏えいを排除したとは言わない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C3 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [AISVS v1.0 C3.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-03-Controlled-Deployment-Rollback.md)
- [C3.3 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.3-controlled-deployment-and-rollback.md)
- [C3 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
