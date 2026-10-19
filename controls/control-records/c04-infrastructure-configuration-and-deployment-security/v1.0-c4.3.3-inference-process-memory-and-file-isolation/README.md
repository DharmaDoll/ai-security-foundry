---
title: 端末推論のプロセス・メモリ・ファイルアクセスを隔離する
versioned_id: v1.0-C4.3.3
requirement_id: C4.3.3
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

# 端末推論のプロセス・メモリ・ファイルアクセスを隔離する

AISVS Verification Level: 3

[C4.3 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3-edge-and-distributed-ai-security.md)

## Upstream basis

AISVS `v1.0-C4.3.3`は、Inference RuntimeがProcess・Memory・File Accessの隔離を強制する。
対応Researchは実際の端末接続・使用前検証・鍵保護と復号後の経路を点検する。特定製品・端末認証方式・追加の推奨を一律のNormative条件にはしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

別Processという名前だけでなく、他ProcessやFileへ到達できない権限・境界を確認する。端末OS、Sandbox、Mandatory Access Control等は実装例であり、Server用Container設定を全端末へ一律に要求しない。

## Security objective

Inference RuntimeがProcess・Memory・File Accessの隔離を強制する。

## Applicability

Edge・Mobile・IoT・組込みでの対象Deviceと中央基盤・Package・Runtimeの実構成に適用する。各SPの対象資産と未観測範囲を明記する。

### Non-applicability

推論Runtimeが端末・Edge上に存在しない境界では、その実行責任を示す。単に隔離非対応のOSであることは対象外の理由にしない。

## Scope and assumptions

機種・OS・Model版・Packageと通信・保存・実行経路を先に特定する。信頼する主体と攻撃者の権限、物理アクセスのScopeを明示する。試験は合成Markerと隔離端末で行い、実機の保護を示せない模擬試験だけで製品適合を主張しない。

## Assets, actors, identities, and trust boundaries

推論Runtime、OS、隣接アプリ、Device Driver。Process・MemoryとFileのアクセス境界。 守る資産は端末Identity、Model、入力と隣接Data。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 推論Runtimeと隣接Process・Memory・Fileの許可範囲を明示する。 |
| SP-2 | 三つのアクセス境界を実Runtime権限で強制し、任意の他Process・Memory・Fileへの自由なアクセスを防ぐ。 |
| SP-3 | 起動・再起動・子Process・共有Device等の経路でも隔離を維持する。 |

## Scope calibration and adjacent assurance

端末OSやKernelの侵害、物理攻撃への耐性は方式に依存する。Runtimeの隔離だけでHost管理者からのModel機密性やAPI出力の安全性を保証しない。

## Threat and failure-mode rationale

侵害された推論Runtimeが他アプリのDataを読み、または隣接アプリが推論のメモリ・Model Fileへアクセスする。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

別Processという名前だけでなく、他ProcessやFileへ到達できない権限・境界を確認する。端末OS、Sandbox、Mandatory Access Control等は実装例であり、Server用Container設定を全端末へ一律に要求しない。 実機種・OS・Modeと構成を確認し、設定宣言と実際の経路を照合する。

### Positive verification

模擬端末の推論処理が許可されたModelと作業領域だけを使えることを確認する。別Processの合成Markerと保護Fileへのアクセスを両方向から試し、定義した隔離を示す。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 推論Processから他アプリのFile・Memoryを読む | 境界外アクセスが拒否される。SP-2。 |
| N-2 | 隣接アプリから推論Memoryや保護Model Fileを読む | 定義した保護対象へのアクセスが拒否される。SP-1、SP-2。 |
| N-3 | 子Processや再起動経路で権限を増やす | 同じ境界が維持され、未隔離ProcessへFallbackしない。SP-3。 |

### Failure conditions

三つの隔離の一つでも欠け、任意の他Process・Memory・Fileへ自由にアクセスできる場合はFail。Model署名・暗号化だけでは満たせない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象Deviceと保護設定・実構成 | 端末基盤担当者 | Identity・Package・Runtimeと保護境界 | 機種・OS・構成変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの対象と実効機能を対応付ける |
| 正例・負例の実機試験記録 | 検証担当者 | 通常・更新・障害の対象経路 | 初回と保護実装変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 成功・拒否・未立証を実測で区別する |

## Related requirements

端末OSやKernelの侵害、物理攻撃への耐性は方式に依存する。Runtimeの隔離だけでHost管理者からのModel機密性やAPI出力の安全性を保証しない。
[C4 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

端末OSやKernelの侵害、物理攻撃への耐性は方式に依存する。Runtimeの隔離だけでHost管理者からのModel機密性やAPI出力の安全性を保証しない。 端末を物理的に管理する攻撃者への完全防御は主張しない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C4 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md)
- [AISVS v1.0 C4.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-03-Edge-Distributed-Security.md)
- [C4.3 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3-edge-and-distributed-ai-security.md)
- [C4 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
