---
title: GPU間接続を承認済み構成と認証した機器へ制限する
versioned_id: v1.0-C4.2.5
requirement_id: C4.2.5
verification_level: 3
family_id: C4
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-02-Hardware-Security.md
last_verified: '2026-10-18'
maturity: verifiable
mapping_assessment_refs: []
---

# GPU間接続を承認済み構成と認証した機器へ制限する

AISVS Verification Level: 3

[C4.2 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.2-ai-hardware-security.md)

## Upstream basis

AISVS `v1.0-C4.2.5`は、Accelerator間の接続を承認Topologyと認証されたEndpointへ制限する。
対応Researchは機器の名称・機能設定と実際の保護を区別し、対象の機種・状態・時点での検証を重視する。Vendor名、版、製品固有の手法は一律のNormative条件にしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

実際の機器・Switch・Routeと承認構成を照合し、接続相手のIdentityを認証する。暗号化Linkの存在だけでは相手の正当性やTopologyの承認を証明しない。

## Security objective

Accelerator間の接続を承認Topologyと認証されたEndpointへ制限する。

## Applicability

対象Accelerator、Driver・Firmware、Workload割当てと保護機能の実構成を評価する。Provider管理の場合は、その責任境界と得られる証拠を明記する。

### Non-applicability

機器間Interconnectを利用しない構成は、Peer・Switch・仮想Routeを含む実構成から対象外を判断する。外部管理で構成が見えない場合は証拠不足を残す。

## Scope and assumptions

機器・Mode・Firmware・Driver、対象Workloadと管理責任を特定する。証拠の対象と実使用機器を照合し、未観測範囲を記録する。試験は隔離した機器または無害な模擬環境で行い、実Dataを使わない。実機保護を示せない模擬試験だけで製品適合を主張しない。

## Assets, actors, identities, and trust boundaries

Accelerator、Switch、Fabric管理者とEndpoint Identity管理。機器間の接続・認証と管理PlaneからRouteを作る境界。 守る資産はModel・入力・中間状態と実行基盤の信頼性。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 許可した機器・接続・Topologyを定義し、実際の接続状態が一致する。 |
| SP-2 | 通信Endpointを認証し、未認証・信頼しない機器へ接続を許さない。 |
| SP-3 | 新規接続・再構成でもTopologyと認証を強制し、管理経路から未承認Routeを作れない。 |

## Scope calibration and adjacent assurance

接続制限はメモリ分離やLink全体の暗号化・完全性の完全な保証ではない。特定ProtocolのOptionを他Fabricへ一般化しない。

## Threat and failure-mode rationale

不正GPUやSwitch、未承認RouteがFabricへ入り、ModelやActivationを取得・変更したり他Partitionへ接続したりする。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

実際の機器・Switch・Routeと承認構成を照合し、接続相手のIdentityを認証する。暗号化Linkの存在だけでは相手の正当性やTopologyの承認を証明しない。 機器・構成・承認基準・実効権限と証拠の作成元を突き合わせる。

### Positive verification

承認した模擬Endpoint同士を許可Topologyで接続し、IdentityとRouteを実測する。再接続や承認変更時にもPolicyが適用されることを確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 承認リスト外のLinkやPeer Routeを作る | 拒否するか無効化され、承認外構成で通信しない。SP-1、SP-3。 |
| N-2 | 信頼しないIdentity・無効証明書のEndpointを接続する | Endpoint認証で拒否する。SP-2。 |
| N-3 | 管理APIから別Partitionを繋ぐRouteを追加する | 管理権限とTopology Policyにより迂回できない。SP-3。 |

### Failure conditions

Topologyが未定義・未強制、Endpointが未認証、許可外Peer接続が通る場合はFail。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 承認設定と機器の実測・Platform証拠 | Hardware基盤担当者 | 対象機器・版・Mode・強制境界 | 起動・割当て・構成変更等の対象契機 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPに対応する実設定と実状態を追える |
| 正例・負例の実測と判定記録 | 検証担当者 | 本文の対象境界と異常経路 | 初回と機器・保護構成変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 想定した成功・拒否・未評価を区別する |

## Related requirements

接続制限はメモリ分離やLink全体の暗号化・完全性の完全な保証ではない。特定ProtocolのOptionを他Fabricへ一般化しない。
[C4 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

機種・Mode・Measurement範囲に依存するため、部分的な証拠を未評価機器や領域へ広げない。接続制限はメモリ分離やLink全体の暗号化・完全性の完全な保証ではない。特定ProtocolのOptionを他Fabricへ一般化しない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C4 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md)
- [AISVS v1.0 C4.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-02-Hardware-Security.md)
- [C4.2 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.2-ai-hardware-security.md)
- [C4 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
