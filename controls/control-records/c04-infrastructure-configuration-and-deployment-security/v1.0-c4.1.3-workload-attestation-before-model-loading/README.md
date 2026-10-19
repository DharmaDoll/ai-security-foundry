---
title: モデル読込み前に実行環境のアテステーションを検証する
versioned_id: v1.0-C4.1.3
requirement_id: C4.1.3
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

# モデル読込み前に実行環境のアテステーションを検証する

AISVS Verification Level: 3

[C4.1 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1-ai-workload-sandboxing-and-validation.md)

## Upstream basis

AISVS `v1.0-C4.1.3`は、Model読込み前にWorkload Attestationを行い、実行環境が改ざんされていない証拠を得る。
Researchは期待するMeasurement、信頼根、鮮度と鍵配布の順序を例示する。モデル署名と環境の証拠を区別し、特定TEEや鍵Brokerを唯一の方法とはしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

実際にModelを読む環境について証拠を取得し、承認した基準と照合してから読み込む。署名されたReportの存在だけでなく、対象環境と鮮度、期待する状態を検証する。失敗した証拠を正常環境の根拠にしない。失敗・不明時に読込みや鍵配布を止めるのは、保証を実効的にするResearchに基づくRepository解釈である。

## Security objective

改ざんされた環境を正規環境と誤認して、Modelや復号鍵を渡すことを防ぐ。

## Applicability

Modelを読むWorkloadと、その環境証拠を信頼するVerifier・Policy・必要な鍵配布経路。CPUとGPU等に環境が跨る場合は証拠で保証する範囲と対象外を明記する。

### Non-applicability

対象境界でModelを読み込まず実行もしない場合は、Providerとの責任分界を示す。Provider内部が見えないことは隔離・検証が不要である根拠ではなく、未立証として記録する。

## Scope and assumptions

対象Model、Loader、Runtime、権限、Device、Providerの責任分界を特定する。
主張する保護対象・攻撃者能力・観測できない部分を明示し、設定の存在と実効性を区別する。
試験は隔離環境の合成Markerや無害な模擬Artifactで行い、実Secretや実攻撃Codeを持ち込まない。

## Assets, actors, identities, and trust boundaries

実行環境が生成する証拠からVerifierの判定へ、判定からModel読込みへ進む境界。資産はModel・鍵と承認状態の根拠。Attester、Verifier、基準管理者、Loader、鍵Brokerが関わる。攻撃者は別環境の証拠や過去Reportの再利用、基準の改変を試みる。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | Modelを読む実環境へ結び付いた証拠を、その読込み前に検証する。 |
| SP-2 | 信頼根・Measurement基準・鮮度等を確認し、署名が有効でも不一致・再利用・対象違いを正常とみなさない。 |
| SP-3 | 不合格・検証不能の結果を成功として読み込まず、再起動・再取得でも定義した順序を守る。 |

## Scope calibration and adjacent assurance

C3.1.3はModel Artifact署名、C4.2.3は各Workload前のGPU完全性Attestation。本ControlはModel読込み前のWorkload環境であり、証拠のScopeと実行時点を混同しない。

## Threat and failure-mode rationale

攻撃者が正規Modelの署名を保ったままLoader環境を改変すると、重みや鍵を盗める。過去の正常証拠を再利用する方式も現環境の状態を示さない。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

AttesterからVerifier、Reference値、判定、Loader・鍵配布の順序を追う。基準更新の権限、Reportの対象Binding、Nonceや有効期間等の鮮度管理、例外経路を確認する。

### Positive verification

承認した模擬環境の新しい証拠を検証し、合格後にのみ模擬Model読込みが進む順序を観測する。評価対象と実際の読込み環境が一致することを確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 測定対象のImageや設定を未承認の値へ変える | 基準不一致を検出し、正常な環境証拠として使わない。SP-2、SP-3。 |
| N-2 | 過去Reportや別環境のReportを再利用する | 鮮度・対象Bindingの検証で拒否する。SP-1、SP-2。 |
| N-3 | Verifierを停止する、または失敗を返させる | 失敗結果を無視せず読込みを保留・拒否する。SP-3。 |

### Failure conditions

読込み後しか検証しない、Model署名だけを環境証拠とする、対象違い・不一致・古い証拠を正常と扱う場合はFail。無条件読込みは実効的検証としてのRepository解釈に反する。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 環境証拠とVerifier判定 | AttesterとVerifier | 対象環境・Measurement・信頼根・鮮度 | 各対象読込み前 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 現在の実環境が基準に合うと追える |
| 不一致・Replay・障害試験と読込みTrace | 検証担当者 | 判定とLoader・鍵配布経路 | 初回と基準・Verifier変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 不合格が正常読込みへ進まない |

## Related requirements

[C3.1.3](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.1.3-signature-verification-at-admission-and-load/README.md)はModel Artifact署名、[C4.2.3](../../../../controls/control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.2.3-hardware-attestation-before-each-accelerator-workload/README.md)は各Workload前のGPU完全性Attestation。本ControlはModel読込み前のWorkload環境であり、証拠のScopeと実行時点を混同しない。
[C4 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

Attestationは測定・基準の範囲を越えた正当性を証明しない。測定後の侵害、Verifierや基準管理者の侵害、Side Channelは残る。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C4 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md)
- [AISVS v1.0 C4.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-01-Workload-Sandboxing-Validation.md)
- [C4.1 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1-ai-workload-sandboxing-and-validation.md)
- [C4 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
