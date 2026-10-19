---
title: アプリ同梱モデルを暗号化し信頼境界内だけで復号する
versioned_id: v1.0-C4.3.5
requirement_id: C4.3.5
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

# アプリ同梱モデルを暗号化し信頼境界内だけで復号する

AISVS Verification Level: 3

[C4.3 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3-edge-and-distributed-ai-security.md)

## Upstream basis

AISVS `v1.0-C4.3.5`は、Mobile・IoT・組込みアプリへ同梱するModelを保存時に暗号化し、Trusted RuntimeまたはSecure Enclave内だけで復号してPackageやFilesystemからの直接抽出を防ぐ。
対応Researchは実際の端末接続・使用前検証・鍵保護と復号後の経路を点検する。特定製品・端末認証方式・追加の推奨を一律のNormative条件にはしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

復号後のModelがどこに現れるかをTraceする。Hardwareに鍵を置くだけでは、通常の一時Fileへ平文を書き出す経路を守れない。Trusted Runtimeの保護対象主体と範囲を具体化する。

## Security objective

Mobile・IoT・組込みアプリへ同梱するModelを保存時に暗号化し、Trusted RuntimeまたはSecure Enclave内だけで復号してPackageやFilesystemからの直接抽出を防ぐ。

## Applicability

Edge・Mobile・IoT・組込みでの対象Deviceと中央基盤・Package・Runtimeの実構成に適用する。各SPの対象資産と未観測範囲を明記する。

### Non-applicability

Modelをアプリに同梱しない構成は配布・保存経路を示して対象外を判断する。別Downloadで保存する場合の保護はC4.3.2・C4.3.4等で別に評価する。

## Scope and assumptions

機種・OS・Model版・Packageと通信・保存・実行経路を先に特定する。信頼する主体と攻撃者の権限、物理アクセスのScopeを明示する。試験は合成Markerと隔離端末で行い、実機の保護を示せない模擬試験だけで製品適合を主張しない。

## Assets, actors, identities, and trust boundaries

アプリPackage、Updater、Loader、Trusted Runtime／Enclave、Hostと隣接アプリ。暗号文から境界内の平文使用、境界外出力への経路。 守る資産は端末Identity、Model、入力と隣接Data。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 同梱ModelがPackageと保存領域で暗号化され、部分的な平文の重みや構成物を残さない。 |
| SP-2 | 復号は定義したTrusted Runtime／Enclave内だけで行われ、外側のProcessや通常Fileへ平文を引き渡さない。 |
| SP-3 | 更新、起動、障害処理、Cacheや一時保存でも同じ保護を保ち、直接抽出可能な平文を残さない。 |

## Scope calibration and adjacent assurance

Hardware鍵StoreがそのままModel推論全体を実行できるとは限らない。保護環境内の侵害、物理攻撃、APIからの模倣は残る。C4.3.4の保存時鍵保護と本要件の復号場所を区別する。

## Threat and failure-mode rationale

暗号鍵は保護されていても、Loaderが復号した平文ModelをCacheや一時Fileへ出し、端末所有者や隣接Processに盗まれる。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

復号後のModelがどこに現れるかをTraceする。Hardwareに鍵を置くだけでは、通常の一時Fileへ平文を書き出す経路を守れない。Trusted Runtimeの保護対象主体と範囲を具体化する。 実機種・OS・Modeと構成を確認し、設定宣言と実際の経路を照合する。

### Positive verification

合成Modelを含むPackageを展開し、保存中に平文がないことを確認する。起動・推論・停止時のFileとMemory経路をTraceし、平文が指定した信頼境界内だけに現れることを示す。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | Loaderを通常Processで実行し平文を受け取らせる | 信頼境界外の復号・露出を検出し、許可しない。SP-2。 |
| N-2 | 復号後のModelを一時FileやCacheへ書き出す | 直接抽出できる状態を検出し、保護済みと判定しない。SP-3。 |
| N-3 | 更新失敗・Crash後にStagingやDumpを調べる | 平文の同梱Modelが残っていないことを確認する。SP-1、SP-3。 |

### Failure conditions

同梱Modelが平文、復号が信頼境界外で行われる、通常のFile等へ平文が残り直接抽出できる場合はFail。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象Deviceと保護設定・実構成 | 端末基盤担当者 | Identity・Package・Runtimeと保護境界 | 機種・OS・構成変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの対象と実効機能を対応付ける |
| 正例・負例の実機試験記録 | 検証担当者 | 通常・更新・障害の対象経路 | 初回と保護実装変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 成功・拒否・未立証を実測で区別する |

## Related requirements

Hardware鍵StoreがそのままModel推論全体を実行できるとは限らない。保護環境内の侵害、物理攻撃、APIからの模倣は残る。[C4.3.4](../../../../controls/control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3.4-hardware-backed-encryption-for-locally-stored-models/README.md)の保存時鍵保護と本要件の復号場所を区別する。
[C4 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

Hardware鍵StoreがそのままModel推論全体を実行できるとは限らない。保護環境内の侵害、物理攻撃、APIからの模倣は残る。C4.3.4の保存時鍵保護と本要件の復号場所を区別する。 端末を物理的に管理する攻撃者への完全防御は主張しない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C4 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md)
- [AISVS v1.0 C4.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-03-Edge-Distributed-Security.md)
- [C4.3 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3-edge-and-distributed-ai-security.md)
- [C4 Family概要](../README.md)

- [関連Insight：Dataは形を変えてもProtectionを失わない](../../../../docs/insights/protected-data-survives-transformation.md)（横断的な考察。規範やMappingではない）

- [関連Insight：端末で推論できることと、重要操作を許可できることは別である](../../../../docs/insights/local-inference-is-not-action-authority.md)（横断的な考察。規範やMappingではない）

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
