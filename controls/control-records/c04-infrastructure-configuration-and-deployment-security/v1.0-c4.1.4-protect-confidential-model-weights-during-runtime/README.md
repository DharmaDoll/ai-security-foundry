---
title: 機密推論中の重みを隔離環境で保護する
versioned_id: v1.0-C4.1.4
requirement_id: C4.1.4
verification_level: 3
family_id: C4
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-01-Workload-Sandboxing-Validation.md
last_verified: '2026-10-18'
maturity: verifiable
mapping_assessment_refs: []
---

# 機密推論中の重みを隔離環境で保護する

AISVS Verification Level: 3

[C4.1 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1-ai-workload-sandboxing-and-validation.md)

## Upstream basis

AISVS `v1.0-C4.1.4`は、機密推論Serviceで、隔離実行環境によりRuntime中のModel重みを保護する。
Researchはホスト・管理者・隣接処理からの実行中メモリ読出しと、Dump・一時File等の迂回を扱う。CPU保護だけでGPU側の重みも保護したと主張しない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

誰から重みを守るServiceかを定義し、実行中に平文が存在する場所と保護境界を追う。通常のContainerだけではホスト管理者からのメモリ保護にならない。CPU、GPU、転送、Swap、Dump、Support用出力を含め、想定する外側の主体が平文重みへアクセスできないことを確認する。特定の機種の内部保護を他の機種や全メモリ暗号化へ一般化しない。

## Security objective

保存時暗号化だけに依存せず、機密推論で使われる重みが実行中に保護境界外へ露出することを減らす。

## Applicability

重みの機密性を保護するConfidential Inference Serviceの実行環境。全AI推論へ機密推論というScopeを暗黙に広げない。Host管理者等を対象外にする場合は、その制限がServiceのClaimと一致するかを確認する。

### Non-applicability

機密推論Serviceを提供・利用せず、実行中の重みの機密性を主張しない構成は本要件の対象外とできる。保存時暗号化があるという理由だけで対象内の実行中保護を省略しない。

## Scope and assumptions

対象Model、Loader、Runtime、権限、Device、Providerの責任分界を特定する。
主張する保護対象・攻撃者能力・観測できない部分を明示し、設定の存在と実効性を区別する。
試験は隔離環境の合成Markerや無害な模擬Artifactで行い、実Secretや実攻撃Codeを持ち込まない。

## Assets, actors, identities, and trust boundaries

保護された実行環境からホスト、Hypervisor、管理・監視・Support経路、Deviceや通信へ進む境界。資産は平文の重みと鍵。Service提供者、Host運用者、TEE内アプリ、GPU基盤、鍵管理者が関わる。外側の侵害や管理権限からメモリ・Dumpを読む攻撃を想定する。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 機密性を主張する主体・実行環境のScopeを定義し、CPU・GPU等の平文の重みの経路を列挙する。 |
| SP-2 | 想定する境界外の主体からRuntime中の平文重みを読めない隔離が実際に有効である。 |
| SP-3 | Dump・Swap・Log・一時File・Device転送等が重みを境界外へ迂回して露出しない。 |

## Scope calibration and adjacent assurance

C4.1.1はModelから外へ作用する方向の隔離。C4.2.2はTEEのハードウェア隔離・メモリ暗号化・完全性という具体的な性質を別に問う。C4.1.3の環境証拠も、それ単体ではRuntime経路の非露出を保証しない。

## Threat and failure-mode rationale

暗号化した重みも推論で復号される。Host管理者がそのメモリやDumpを読めるなら、保存時暗号化は実行中の窃取を防がない。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

CPU／GPUと通信の保護機能・Production／Debug状態、鍵の受渡し、Dump・Swap・監視機能を確認する。Vendor証拠と実配備の機種・設定を照合し、保護されない領域を明示する。

### Positive verification

合成重みMarkerを保護環境内で使って推論する。許可された内部処理は使える一方、主張Scopeの外側にあるホスト・管理経路からは平文が見えず、出力Artifactにも残らないことを証拠と試験で確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | Host相当権限からメモリ、Dump、Swapを読む | Scopeに含む外側主体へ平文が露出しない。SP-2、SP-3。 |
| N-2 | CPUだけ保護しGPUや転送経路を未保護にする | 未保護の経路を検出し、全実行中保護のPassにしない。SP-1、SP-2。 |
| N-3 | Supportや障害処理でTensorを一時Fileへ出力する | 保護境界外への平文露出を検出・防止する。SP-3。 |

### Failure conditions

保存時しか保護しない、想定した外側主体が実行中の平文を読める、Dump等へ平文が漏れる場合はFail。Platform名だけを証拠にしない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 機密実行構成とPlatform証拠 | Service・基盤担当者 | 機種・設定・保護対象主体・CPU／GPU経路 | 構成・Firmware・Runtime変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 実配備で主張Scopeの隔離が有効 |
| 外側読出しと障害出力の試験 | 検証担当者 | メモリ・Dump・File・転送・Support | 初回と出力経路変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 平文重みが主張Scope外へ出ない |

## Related requirements

[C4.1.1](../../../../controls/control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1.1-isolated-sandbox-for-model-execution/README.md)はModelから外へ作用する方向の隔離。[C4.2.2](../../../../controls/control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.2.2-tee-hardware-isolation-encryption-and-integrity/README.md)はTEEのハードウェア隔離・メモリ暗号化・完全性という具体的な性質を別に問う。[C4.1.3](../../../../controls/control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1.3-workload-attestation-before-model-loading/README.md)の環境証拠も、それ単体ではRuntime経路の非露出を保証しない。
[C4 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

保護環境内の侵害で重みを正規出力へ流す攻撃やAPI経由の模倣、Side Channelは残る。単一の読出し試験の失敗だけで全攻撃への保護を証明しない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C4 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md)
- [AISVS v1.0 C4.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-01-Workload-Sandboxing-Validation.md)
- [C4.1 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1-ai-workload-sandboxing-and-validation.md)
- [C4 Family概要](../README.md)

- [関連Insight：隔離は、誰から誰を守るかで意味が変わる](../../../../docs/insights/isolation-has-a-direction.md)（横断的な考察。規範やMappingではない）

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
