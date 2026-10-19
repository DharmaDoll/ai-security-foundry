---
title: モデルを署名して配布し端末の使用前に検証する
versioned_id: v1.0-C4.3.2
requirement_id: C4.3.2
verification_level: 2
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

# モデルを署名して配布し端末の使用前に検証する

AISVS Verification Level: 2

[C4.3 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3-edge-and-distributed-ai-security.md)

## Upstream basis

AISVS `v1.0-C4.3.2`は、Edge・Mobile向けModelをPackaging時に暗号署名し、端末Runtimeが読込み・推論前に署名またはChecksumを検証する。
対応Researchは実際の端末接続・使用前検証・鍵保護と復号後の経路を点検する。特定製品・端末認証方式・追加の推奨を一律のNormative条件にはしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

Packaging時の署名と端末での実検証を別に確かめる。原文は端末側の署名またはChecksum検証を認めるが、期待値を攻撃者がModelと一緒に差し替えられるなら信頼できる検証にはならない。

## Security objective

Edge・Mobile向けModelをPackaging時に暗号署名し、端末Runtimeが読込み・推論前に署名またはChecksumを検証する。

## Applicability

Edge・Mobile・IoT・組込みでの対象Deviceと中央基盤・Package・Runtimeの実構成に適用する。各SPの対象資産と未観測範囲を明記する。

### Non-applicability

端末へModelを配布せず中央APIだけを呼ぶ構成は、そのData Flowを示して本要件の対象外にできる。

## Scope and assumptions

機種・OS・Model版・Packageと通信・保存・実行経路を先に特定する。信頼する主体と攻撃者の権限、物理アクセスのScopeを明示する。試験は合成Markerと隔離端末で行い、実機の保護を示せない模擬試験だけで製品適合を主張しない。

## Assets, actors, identities, and trust boundaries

Package作成者、署名者、配布Service、端末UpdaterとLoader。配布から端末保存、保存から実使用への境界。 守る資産は端末Identity、Model、入力と隣接Data。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 配布する実Model Packageが暗号署名され、署名範囲と版を特定できる。 |
| SP-2 | 端末が実際に使う内容を、読込み・推論前に信頼できる署名または期待Checksumへ照合する。 |
| SP-3 | 改変・未検証・検証不能なPackageを使用せず、再起動・更新・Cache経路でも検証対象と使用対象が一致する。 |

## Scope calibration and adjacent assurance

署名された旧版のReplayや正当な署名者の悪意は別に残る。ResearchのTUF等によるFreshnessやRollback防御は補強であり、この要件の原文へ一律追加しない。

## Threat and failure-mode rationale

配布経路や端末Cacheが置換され、中央で確認したものと違うModelを端末が使う。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

Packaging時の署名と端末での実検証を別に確かめる。原文は端末側の署名またはChecksum検証を認めるが、期待値を攻撃者がModelと一緒に差し替えられるなら信頼できる検証にはならない。 実機種・OS・Modeと構成を確認し、設定宣言と実際の経路を照合する。

### Positive verification

合成Model一式へ署名し、端末相当Runtimeで使用前検証を行う。署名方式またはChecksum方式の信頼基準を記録し、実Packageが推論に使われるまで追跡する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 重みや設定を一つだけ変更する | 端末で不一致を検出し、読込み・推論へ進まない。SP-2、SP-3。 |
| N-2 | Modelと攻撃者が添付したChecksumを共に置換する | 保護された期待値または署名との不一致を検出する。SP-2。 |
| N-3 | 更新失敗後に未検証Cacheや別形式へFallbackする | 同じ使用前検証が適用され、迂回しない。SP-3。 |

### Failure conditions

Packaging署名がない、端末側の使用前検証がない、基準とModelを無断で一緒に置換できる場合はFail。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 対象Deviceと保護設定・実構成 | 端末基盤担当者 | Identity・Package・Runtimeと保護境界 | 機種・OS・構成変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各SPの対象と実効機能を対応付ける |
| 正例・負例の実機試験記録 | 検証担当者 | 通常・更新・障害の対象経路 | 初回と保護実装変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 成功・拒否・未立証を実測で区別する |

## Related requirements

署名された旧版のReplayや正当な署名者の悪意は別に残る。ResearchのTUF等によるFreshnessやRollback防御は補強であり、この要件の原文へ一律追加しない。
[C4 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

署名された旧版のReplayや正当な署名者の悪意は別に残る。ResearchのTUF等によるFreshnessやRollback防御は補強であり、この要件の原文へ一律追加しない。 端末を物理的に管理する攻撃者への完全防御は主張しない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C4 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md)
- [AISVS v1.0 C4.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-03-Edge-Distributed-Security.md)
- [C4.3 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3-edge-and-distributed-ai-security.md)
- [C4 Family概要](../README.md)

- [関連Insight：端末で推論できることと、重要操作を許可できることは別である](../../../../docs/insights/local-inference-is-not-action-authority.md)（横断的な考察。規範やMappingではない）

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
