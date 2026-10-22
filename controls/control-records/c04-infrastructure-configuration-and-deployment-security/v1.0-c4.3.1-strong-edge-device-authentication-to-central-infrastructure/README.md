---
title: 端末を中央基盤で強く認証する
versioned_id: v1.0-C4.3.1
requirement_id: C4.3.1
verification_level: 1
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

# 端末を中央基盤で強く認証する

AISVS Verification Level: 1

[C4.3 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3-edge-and-distributed-ai-security.md)

## Upstream basis

AISVS `v1.0-C4.3.1`は、Edge AI Deviceが中央基盤へ接続する際に強い認証を行う。
対応Researchは実際の端末接続・使用前検証・鍵保護と復号後の経路を点検する。特定製品・端末認証方式・追加の推奨を一律のNormative条件にはしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

端末IDやIPの自己申告だけでなく、端末が正当なCredentialを保持することを検証する。Device証明書によるmTLSは一例だが唯一の方式ではない。Credentialの登録・失効・更新を含め、実際の中央接続で認証が強制されるかを見る。

## Security objective

Edge AI Deviceが中央基盤へ接続する際に強い認証を行う。

## Applicability

Edge・Mobile・IoT・組込みでの対象Deviceと中央基盤・Package・Runtimeの実構成に適用する。各SPの対象資産と未観測範囲を明記する。

### Non-applicability

中央基盤へ接続しない端末は、その通信と更新経路を示して対象外を判断する。認証が未実装というだけでは対象外にしない。

## Scope and assumptions

機種・OS・Model版・Packageと通信・保存・実行経路を先に特定する。信頼する主体と攻撃者の権限、物理アクセスのScopeを明示する。試験は合成Markerと隔離端末で行い、実機の保護を示せない模擬試験だけで製品適合を主張しない。

## Assets, actors, identities, and trust boundaries

端末、Credential発行者、中央認証Service、Fleet運用者。端末から中央接続へ参加する境界。 守る資産は端末Identity、Model、入力と隣接Data。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 中央接続で端末IdentityとCredentialを検証する強い認証方式を定義し、自己申告や共通の既定値だけに依存しない。 |
| SP-2 | Model配布・同期等の対象接続と代替経路で認証を強制し、認証不能・無効な端末を受け入れない。 |
| SP-3 | CredentialのProvisioning・失効・更新後も正しい端末Bindingと検証Policyを保つ。 |

## Scope calibration and adjacent assurance

認証は端末の健全性や権限の全体を証明しない。Attestation・Command認可・盗難端末への対応は隣接保証として評価する。

## Threat and failure-mode rationale

偽端末が正規端末IDを名乗り、Model配布やData送信経路へ参加する。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

端末IDやIPの自己申告だけでなく、端末が正当なCredentialを保持することを検証する。Device証明書によるmTLSは一例だが唯一の方式ではない。Credentialの登録・失効・更新を含め、実際の中央接続で認証が強制されるかを見る。 実機種・OS・Modeと構成を確認し、設定宣言と実際の経路を照合する。

### Positive verification

登録済み模擬端末が正当なCredentialで中央基盤へ接続できることを示す。更新後も正当な新Credentialが使え、無効になったものはPolicyに従い拒否される。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 正規端末IDだけを名乗り接続する | Credentialの証明がなく拒否する。SP-1。 |
| N-2 | 無効・期限切れ・信頼しないCredentialを使う | 中央側が拒否し、弱い方式へFallbackしない。SP-2。 |
| N-3 | Credential失効後に旧接続経路を再利用する | 失効Policyが反映され、認証迂回できない。SP-3。 |

### Failure conditions

端末IDやIPだけで信用する、無認証経路を残す、無効Credentialで接続できる場合はFail。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象Deviceと保護設定・実構成 | 端末基盤担当者 | Identity・Package・Runtimeと保護境界 | 機種・OS・構成変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの対象と実効機能を対応付ける |
| 正例・負例の実機試験記録 | 検証担当者 | 通常・更新・障害の対象経路 | 初回と保護実装変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 成功・拒否・未立証を実測で区別する |

## Related requirements

認証は端末の健全性や権限の全体を証明しない。Attestation・Command認可・盗難端末への対応は隣接保証として評価する。
[C4 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

認証は端末の健全性や権限の全体を証明しない。Attestation・Command認可・盗難端末への対応は隣接保証として評価する。 端末を物理的に管理する攻撃者への完全防御は主張しない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## 関連する洞察

個別要件の理解・設計レビューを助ける参照であり、追加要件や正式なMappingではない。

- [端末で推論できることと、重要操作を許可できることは別である](../../../../docs/insights/local-inference-is-not-action-authority.md)：端末上の推論・モデル保護と、重要操作を許す側の判断を分ける。

## References

- [AISVS v1.0 C4 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md)
- [AISVS v1.0 C4.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-03-Edge-Distributed-Security.md)
- [C4.3 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3-edge-and-distributed-ai-security.md)
- [C4 Family概要](../README.md)


## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
