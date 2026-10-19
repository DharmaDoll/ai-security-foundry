---
title: モデル読込みで安全な保存形式の許可リストを強制する
versioned_id: v1.0-C4.1.2
requirement_id: C4.1.2
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

# モデル読込みで安全な保存形式の許可リストを強制する

AISVS Verification Level: 1

[C4.1 Section講義](../../../learning/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1-ai-workload-sandboxing-and-validation.md)

## Upstream basis

AISVS `v1.0-C4.1.2`は、Model Artifactの読込みで、復元時に任意Code実行を許さないSerialization形式の明示的Allowlistを強制する。
Researchは拡張子ではなく実際の形式と復元経路を評価し、重みが安全な形式でも設定やTemplate等が実行面になると注意する。Scannerで危険物を探すだけでは形式Allowlistの代替にならない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

許可する形式を明示し、それぞれのParser・設定・Custom Operator等が復元時の任意Codeを許さない条件を定義する。形式判定と拒否を危険なDeserializerより前に行い、未知形式や別のLoaderへの自動Fallbackを許可しない。信頼された署名があるという理由だけでCode実行可能な形式を本要件のAllowlistへ入れない。

## Security objective

数値Dataの読込みだと信頼して、攻撃者指定のCodeやCallableを復元処理で実行することを防ぐ。

## Applicability

重み・設定・付属物等を復元するModel読込み経路。Artifact内の動的Code、Template、Custom Operatorが利用されるなら、それを含めて許可条件を検証する。

### Non-applicability

対象境界でModelを読み込まず実行もしない場合は、Providerとの責任分界を示す。Provider内部が見えないことは隔離・検証が不要である根拠ではなく、未立証として記録する。

## Scope and assumptions

対象Model、Loader、Runtime、権限、Device、Providerの責任分界を特定する。
主張する保護対象・攻撃者能力・観測できない部分を明示し、設定の存在と実効性を区別する。
試験は隔離環境の合成Markerや無害な模擬Artifactで行い、実Secretや実攻撃Codeを持ち込まない。

## Assets, actors, identities, and trust boundaries

未信頼Artifactから形式識別・Allowlist判定を経てDeserializerへ進む境界。資産はLoaderと推論環境の実行権限。Artifact作者、形式Policy管理者、Parser、Loaderが関わる。攻撃者が拡張子、Metadata、圧縮やFallbackを利用してCode実行可能な復元を誘うことを想定する。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 許可する形式と復元条件が明示され、任意Codeを実行できる形式や設定を許可しない。 |
| SP-2 | 実内容と読込み経路をAllowlistへ照合し、許可外・不明形式を危険な復元処理の前に拒否する。 |
| SP-3 | 自動Fallback、補助File、TemplateやCustom Operatorの処理が形式制限を迂回しない。 |

## Scope calibration and adjacent assurance

C4.1.1は実行後の到達範囲、C3.1は署名・同一性。本要件は読込み形式の性質であり、署名済み・Scanner陰性だけでは満たせない。Runtime RPCのSerializationは関連する別の確認境界。

## Threat and failure-mode rationale

安全な重み形式を名乗るFileでも、中身や補助Configが汎用Object復元やTemplate実行へ渡ると、読込み時に攻撃者Codeが動く。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

形式Policy、実内容識別、LoaderのDispatch、環境変数、Custom CodeとFallbackを調べる。危険Deserializerを先に実行してから判定していないか確認する。

### Positive verification

許可したData形式の模擬Modelを、実際の本番相当Loaderで読む。許可したParser・設定だけが選ばれ、未許可Deserializerへ処理が渡らないことをTraceで確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 許可外の形式へ許可済みの拡張子を付ける | 復元前に拒否する。実行Payloadではなく無害な形式Fixtureと呼出しTraceを使う。SP-2。 |
| N-2 | 同梱TemplateやConfigで動的Callableの起動を要求する | 任意Code実行を許す読込みへ入らない。SP-1、SP-3。 |
| N-3 | 形式判定を失敗させ汎用DeserializerへFallbackさせる | Allowlist外の復元を拒否する。SP-2、SP-3。 |

### Failure conditions

明示的Allowlistがない、任意Code実行可能な復元形式・条件を許可する、拡張子だけで判定する、許可外処理へFallbackする場合はFail。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 形式AllowlistとParser条件 | Model基盤担当者 | 形式・Parser・設定・補助物 | 形式・Loader変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 各許可条件で任意Code復元を許さない根拠がある |
| Dispatchと形式拒否試験 | 検証担当者 | 実LoaderとFallback・補助物 | 初回と依存・設定変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 禁止Deserializer呼出し前に拒否する |

## Related requirements

[C4.1.1](../../../../controls/control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1.1-isolated-sandbox-for-model-execution/README.md)は実行後の到達範囲、C3.1は署名・同一性。本要件は読込み形式の性質であり、署名済み・Scanner陰性だけでは満たせない。Runtime RPCのSerializationは関連する別の確認境界。
[C4 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

許可形式にもParserのメモリ破壊等の脆弱性はあり得る。形式設計がCode実行を許さないことと、実装に脆弱性がないことは別で、Parser更新とSandboxも必要。
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
