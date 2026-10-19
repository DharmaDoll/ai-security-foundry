---
title: 端末保存の重みと機密パラメータをハードウェア鍵で暗号化する
versioned_id: v1.0-C4.3.4
requirement_id: C4.3.4
verification_level: 3
family_id: C4
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-03-Edge-Distributed-Security.md
last_verified: '2026-10-18'
maturity: verifiable
mapping_assessment_refs: []
---

# 端末保存の重みと機密パラメータをハードウェア鍵で暗号化する

AISVS Verification Level: 3

[C4.3 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3-edge-and-distributed-ai-security.md)

## Upstream basis

AISVS `v1.0-C4.3.4`は、ローカル保存のModel重みと機密Parameterを、Hardware-backed Key StoreまたはSecure Enclaveを用いて暗号化する。
対応Researchは実際の端末接続・使用前検証・鍵保護と復号後の経路を点検する。特定製品・端末認証方式・追加の推奨を一律のNormative条件にはしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

保存対象と鍵の保護場所を追い、Key Store API名だけでHardware保護を推定しない。大きなModel本体をHardware内へ丸ごと保存する必要はなく、Data鍵をHardware保護鍵でWrapする構成もあり得る。

## Security objective

ローカル保存のModel重みと機密Parameterを、Hardware-backed Key StoreまたはSecure Enclaveを用いて暗号化する。

## Applicability

Edge・Mobile・IoT・組込みでの対象Deviceと中央基盤・Package・Runtimeの実構成に適用する。各SPの対象資産と未観測範囲を明記する。

### Non-applicability

重みと機密Parameterを端末に保存しない構成では保存経路を示して対象外にできる。Cache・更新Staging等にも残らないことを確認する。

## Scope and assumptions

機種・OS・Model版・Packageと通信・保存・実行経路を先に特定する。信頼する主体と攻撃者の権限、物理アクセスのScopeを明示する。試験は合成Markerと隔離端末で行い、実機の保護を示せない模擬試験だけで製品適合を主張しない。

## Assets, actors, identities, and trust boundaries

端末Storage、鍵Store、Enclave、アプリとBackup管理者。保存された暗号文から鍵利用・復号への境界。 守る資産は端末Identity、Model、入力と隣接Data。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | ローカルに保存する全重みと機密Parameterを特定し、平文保存を残さず暗号化する。 |
| SP-2 | 鍵をHardware-backed Key StoreまたはEnclaveの保護へ結び付け、Modelと一緒に取得できる平文鍵だけへ依存しない。 |
| SP-3 | Hardware保護が実端末で有効と確認し、Software-only FallbackやExport・Backupへ平文鍵・対象物を残さない。 |

## Scope calibration and adjacent assurance

保存時保護は復号後の平文が安全なことを保証しない。C4.3.5はその復号境界を別に問う。認可済みアプリによる鍵の不正利用、物理・Side Channel攻撃も残る。

## Threat and failure-mode rationale

PackageからModelとソフトウェアに埋め込んだ鍵を一緒に抜き出し、暗号化を迂回する。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

保存対象と鍵の保護場所を追い、Key Store API名だけでHardware保護を推定しない。大きなModel本体をHardware内へ丸ごと保存する必要はなく、Data鍵をHardware保護鍵でWrapする構成もあり得る。 実機種・OS・Modeと構成を確認し、設定宣言と実際の経路を照合する。

### Positive verification

合成重みとParameterを暗号化し、実端末の鍵保護Level等の証拠を確認する。正当な利用は可能で、Package・通常File・Backupから平文鍵と重みを取得できないことを試験する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | Key StoreをSoftware-onlyへFallbackさせる | Hardware保護の欠落として検出する。SP-2、SP-3。 |
| N-2 | 重みは暗号化するがParameterや鍵をAssetへ平文同梱する | 対象漏れ・鍵露出を検出し、Passにしない。SP-1、SP-2。 |
| N-3 | 保存物と通常の鍵Metadataだけを外部へCopyする | 元のHardware鍵保護を迂回して復号できないか確認する。意図した鍵共有があれば別途Scopeを記録する。SP-2。 |

### Failure conditions

対象物の平文保存、通常Fileに取り出せる鍵のみの保護、実端末でHardware保護が有効でない場合はFail。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象Deviceと保護設定・実構成 | 端末基盤担当者 | Identity・Package・Runtimeと保護境界 | 機種・OS・構成変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの対象と実効機能を対応付ける |
| 正例・負例の実機試験記録 | 検証担当者 | 通常・更新・障害の対象経路 | 初回と保護実装変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 成功・拒否・未立証を実測で区別する |

## Related requirements

保存時保護は復号後の平文が安全なことを保証しない。[C4.3.5](../../../../controls/control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3.5-packaged-model-encryption-and-trusted-runtime-decryption/README.md)はその復号境界を別に問う。認可済みアプリによる鍵の不正利用、物理・Side Channel攻撃も残る。
[C4 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

保存時保護は復号後の平文が安全なことを保証しない。C4.3.5はその復号境界を別に問う。認可済みアプリによる鍵の不正利用、物理・Side Channel攻撃も残る。 端末を物理的に管理する攻撃者への完全防御は主張しない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C4 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md)
- [AISVS v1.0 C4.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-03-Edge-Distributed-Security.md)
- [C4.3 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3-edge-and-distributed-ai-security.md)
- [C4 Family概要](../README.md)

- [関連Insight：Dataは形を変えてもProtectionを失わない](../../../../docs/insights/protected-data-survives-transformation.md)（横断的な考察。規範やMappingではない）

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
