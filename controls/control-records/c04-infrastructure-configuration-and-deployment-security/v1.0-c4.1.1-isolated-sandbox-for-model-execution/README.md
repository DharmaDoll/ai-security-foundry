---
title: AIモデルを隔離されたサンドボックスで実行する
versioned_id: v1.0-C4.1.1
requirement_id: C4.1.1
verification_level: 1
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

# AIモデルを隔離されたサンドボックスで実行する

AISVS Verification Level: 1

[C4.1 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1-ai-workload-sandboxing-and-validation.md)

## Upstream basis

AISVS `v1.0-C4.1.1`は、AI Modelを隔離されたSandbox内で実行する。
ResearchはModel読込み・実行がCode実行面になり得ることと、Containerを使うだけではホストへの到達を防げないことを扱う。特定製品やMicroVMを全用途へ一律に義務付ける原文ではない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

Modelの読込み・推論が侵害される可能性を前提に、File、Process、通信、Credential、Deviceと管理APIへの到達範囲をSandboxで制限する。必要な推論資源は許可してよいが、Model側からホストや他Workloadへ自由に作用できる構成を隔離とは呼ばない。Modelを読む前段の処理が境界外で危険な処理を行っていないかも確認する。

## Security objective

不正なModelや実行処理の侵害がホストと他Workloadへ広がる範囲を抑える。

## Applicability

Modelの読込み・推論を実行する環境。外部API型ではProviderの実行基盤が責任境界に入り、利用者のClient設定だけでProvider側の隔離を証明しない。

### Non-applicability

対象境界でModelを読み込まず実行もしない場合は、Providerとの責任分界を示す。Provider内部が見えないことは隔離・検証が不要である根拠ではなく、未立証として記録する。

## Scope and assumptions

対象Model、Loader、Runtime、権限、Device、Providerの責任分界を特定する。
主張する保護対象・攻撃者能力・観測できない部分を明示し、設定の存在と実効性を区別する。
試験は隔離環境の合成Markerや無害な模擬Artifactで行い、実Secretや実攻撃Codeを持ち込まない。

## Assets, actors, identities, and trust boundaries

Model／Loader／推論Processからホスト、他Workload、管理機能、Network・Deviceへ進む境界。資産はホストのFile・Secret・管理権限と隣接処理。攻撃者がModelやその補助Fileを操作し、境界内で任意の処理を試みることを想定する。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 実際のModel読込み・実行が定義したSandbox境界内で行われる。 |
| SP-2 | 必要なFile・Process・通信・Deviceの許可範囲が限定され、ホスト管理機能や他Workloadへ自由に作用できない。 |
| SP-3 | 通常起動・再起動・Fallbackでも同じ隔離が適用され、Sandbox起動失敗を境界外実行で代替しない。 |

## Scope calibration and adjacent assurance

C4.1.2は受入れる保存形式、C4.1.3は実行環境の証拠、C4.1.4は実行中の重みを外側から保護する保証。本Controlの方向はModel側から外部への影響の封じ込め。

## Threat and failure-mode rationale

悪意あるModelの読込みがホスト権限で走ると、ホストSecretや他Workloadが侵害される。隔離内からホスト側のFile処理へ不正参照を渡す代理経路も境界を破り得る。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

Runtime設定、実Processの権限・Mount・Device・Socket・Networkを確認する。特権Container、ホスト管理Socket、広いVolume共有やCredential代理が境界を迂回しないか調べる。

### Positive verification

隔離内の無害な推論処理が必要なModelと作業領域を使えることを示す。ホスト相当の模擬Secret、他処理のMarker、管理用Socket、非許可通信先へ実Identityで到達できないことを確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | Sandbox内からホストの保護Fileや他Processへアクセスする | 定義した境界で拒否し、内容や状態を変更できない。SP-2。 |
| N-2 | 出力FileにSymlinkや境界外Pathを作り、ホスト側の後処理に渡す | 後処理を代理にした境界外アクセスを拒否する。SP-2。 |
| N-3 | Sandbox起動を失敗させFallbackを起動する | 未隔離実行に切り替えない。SP-1、SP-3。 |

### Failure conditions

Modelが隔離外で実行される、ホストや他Workloadの重要資源へ自由に作用できる、失敗時に未隔離Fallbackへ移る場合はFail。Container名や設定宣言だけではPassにしない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 実行境界と実効権限の記録 | Runtime運用者 | Loader・推論・Fallback・ホスト資源 | Runtime・権限変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 実Processが宣言した隔離と一致する |
| 許可動作と境界越境の実測 | 検証担当者 | File・Process・通信・Device経路 | 初回と隔離構成変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 必要動作は成功し越境は拒否される |

## Related requirements

[C4.1.2](../../../../controls/control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1.2-safe-serialization-format-allowlist-at-model-loading/README.md)は受入れる保存形式、[C4.1.3](../../../../controls/control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1.3-workload-attestation-before-model-loading/README.md)は実行環境の証拠、[C4.1.4](../../../../controls/control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1.4-protect-confidential-model-weights-during-runtime/README.md)は実行中の重みを外側から保護する保証。本Controlの方向はModel側から外部への影響の封じ込め。
[C4 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

Sandbox自体の脆弱性や許可した通信の悪用は残る。通常のContainer隔離はホスト管理者から重みを守る保証ではない。Modelが安全な回答を返す保証とも区別する。
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
