---
title: 投入前に入力・安全性・出力無害化の自動試験を行う
versioned_id: v1.0-C3.2.1
requirement_id: C3.2.1
verification_level: 1
family_id: C3
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-02-Model-Validation-Testing.md
last_verified: '2026-10-18'
maturity: verifiable
mapping_assessment_refs: []
---

# 投入前に入力・安全性・出力無害化の自動試験を行う

AISVS Verification Level: 1

[C3.2 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.2-model-validation-and-testing.md)

## Upstream basis

AISVS `v1.0-C3.2.1`は、配備前に入力検証、安全性評価、出力無害化の自動試験をModelへ実施する。
Researchは入力だけでなく、出力がRendererやTool等へ渡る境界を自動試験することを強調する。毒性や拒否応答のScoreだけでは出力無害化を示せない。Researchの推奨GateやTool名を普遍的な必須条件へ置き換えない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

本番で利用するModel版と周辺の入出力経路について、三種類の試験を投入前に自動実行する。入力検証は想定外入力の処理、安全性評価は用途で避ける振る舞い、出力無害化は次の解釈・実行先に渡す未信頼出力の扱いを確認する。Model単体にApplicationの無害化機能が内蔵される必要はないが、実際の製品経路を試す。

## Security objective

一種類のBenchmarkだけで入出力境界も安全と誤認し、未試験の構成を配備することを防ぐ。

## Applicability

配備するModelと、その製品で実際に使う入力処理・安全方針・出力の利用先を対象とする。外部API Modelを採用する場合も、製品側で観測できる三種類の経路を自動試験する。

### Non-applicability

投入対象Modelがない境界では適用しない。外部API利用だけで試験不要とはしない。出力がText表示だけでも、その利用先の処理を確認し、三種類の試験の一つを黙って削除しない。

## Scope and assumptions

対象Deployment、Model一式、版、Provider、Registryと実際の読込み経路を評価開始時に特定する。
名前やAliasが可変なら実体の識別方法を明示する。試験は隔離環境の無害な模擬Artifactで行い、
本番Dataや実行可能な不正Payloadを持ち込まない。証拠の対象版と現在の配備が一致するか確認する。

## Assets, actors, identities, and trust boundaries

試験環境から本番のRelease判断へ移る境界と、利用者・取得内容からModelへ、Model出力からRendererやToolへ進む境界。資産は安全な処理と試験結果。Model提供者、Application作者、試験実行者、Release担当者が関わる。攻撃者は未信頼入力・出力で既存制御を迂回しようとする。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 対象Model版へ入力検証、安全性評価、出力無害化の三種類を自動試験する。 |
| SP-2 | 自動試験が本番投入前に実行され、対象版・設定・結果と配備を結び付けられる。 |
| SP-3 | 実際の入出力経路に対する観測可能な期待値があり、通常成功・拒否・無害化・試験不能を区別する。 |

## Scope calibration and adjacent assurance

C2は入力境界、C7は出力境界の性質を扱い、本Controlは三種の投入前自動試験を扱う。C3.2.2・C3.2.3は量子化やProvider変更による再評価。署名成功は試験の代わりにならない。

## Threat and failure-mode rationale

入力と有害回答の試験だけが通っても、出力が別の処理系で命令として解釈される脆弱性を発見できない。旧版の成功結果を新しい構成へ流用する問題もある。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

三種の試験一覧とCI実行順、ModelとApplication設定、RendererやTool等の出力先を照合する。試験が利用しない経路、Mockだけで実経路を通さない試験、Modelの拒否だけを出力無害化と呼ぶ結果がないか点検する。

### Positive verification

通常の許可入力、拒否・制限対象の模擬入力、安全な代替応答を期待する質問、無害な出力Markerを用意する。入力検証・安全性・出力境界の三種で、期待した処理を自動で判定し、投入前の対象版へ結果を結び付ける。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 出力無害化の試験だけを削除して試験済みと申告する | 三種の欠落を検出し、C3.2.1のPassにしない。SP-1。 |
| N-2 | RendererやToolが解釈する形式の模擬出力を強制する | Modelの拒否Scoreとは独立に、境界での拒否・安全な処理または不備を観測する。SP-1、SP-3。 |
| N-3 | 旧Model版の実行結果や配備後の実行のみを提出する | 対象と時点の不一致を検出し、投入前試験の証拠としない。SP-2。 |

### Failure conditions

三種類のいずれかがない、自動でない、配備前に実行しない、または配備対象と試験対象が対応しない場合はFail。試験実施と試験合格、製品Riskの受容は区別する。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 三種の版管理された試験と実行結果 | Applicationと評価担当者 | Model版・実経路・期待値・結果 | 各投入前と試験条件変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 三種類が実行され欠落・不一致を検出できる |
| 配備と評価の対応記録 | Release担当者 | 試験対象・実行時刻・本番構成 | 各配備時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 配備前の対象一致を確認できる |

## Related requirements

C2は入力境界、C7は出力境界の性質を扱い、本Controlは三種の投入前自動試験を扱う。[C3.2.2](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.2.2-same-safety-suite-on-quantized-artifact/README.md)・[C3.2.3](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.2.3-security-reevaluation-before-provider-route-changes/README.md)は量子化やProvider変更による再評価。署名成功は試験の代わりにならない。
[C3 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

有限の自動試験はすべての攻撃やPrompt Injectionの不在を証明しない。試験に合格しても残余Riskはある。危険な結果を把握して投入する判断の妥当性は、本要件の試験実施だけで承認されるものではない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C3 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [AISVS v1.0 C3.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-02-Model-Validation-Testing.md)
- [C3.2 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.2-model-validation-and-testing.md)
- [C3 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
