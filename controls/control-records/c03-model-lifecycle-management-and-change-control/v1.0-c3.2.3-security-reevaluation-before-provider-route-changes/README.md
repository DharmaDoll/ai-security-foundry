---
title: 提供者のモデル・版・経路変更後は継続利用前に再評価する
versioned_id: v1.0-C3.2.3
requirement_id: C3.2.3
verification_level: 3
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

# 提供者のモデル・版・経路変更後は継続利用前に再評価する

AISVS Verification Level: 3

[C3.2 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.2-model-validation-and-testing.md)

## Upstream basis

AISVS `v1.0-C3.2.3`は、ProviderのModel・Version・Routing変更を契機に、継続利用前にSecurity再評価を行う。
Researchは可変Alias、RegionやFallbackも実応答先を変え得ること、Provider内部の経路が見えない場合には固定可能な版と変更通知・観測限界を記録することを扱う。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

ProviderのModel名やアプリCodeだけでなく、実際の処理先が変わる契機を把握する。変更後の対象経路でSecurityを再評価してから継続利用を認める。変更通知を受けるだけ、または旧Routeの評価を再掲するだけでは足りない。再評価で使う条件と結果を対象Routeへ結び付ける。

## Security objective

Provider側だけの変更で製品のSecurity境界が変わっても、古い合格結果のまま使い続けることを防ぐ。

## Applicability

外部または内部ProviderがModel、版、振り分け先を変更する構成へ適用する。Alias、Region、障害Fallback等が別Modelへ解決されるなら対象とする。Provider管理の変更経路が存在しなければ、その理由とScopeを記録する。

### Non-applicability

ProviderのModel・Version・Routingの変更対象がない場合は、境界と変更経路がない根拠を記録する。内部が非公開であることは対象外の根拠とせず、変更検知・再評価の未立証範囲を明記する。

## Scope and assumptions

対象Deployment、Model一式、版、Provider、Registryと実際の読込み経路を評価開始時に特定する。
名前やAliasが可変なら実体の識別方法を明示する。試験は隔離環境の無害な模擬Artifactで行い、
本番Dataや実行可能な不正Payloadを持ち込まない。証拠の対象版と現在の配備が一致するか確認する。

## Assets, actors, identities, and trust boundaries

承認されたProvider処理先から変更後のModel・Version・Routeへ移る境界。資産は入出力・Tool等のSecurity特性と変更判定。Provider、Router管理者、Application運用者、評価担当者が関わる。攻撃者は変更後に生じた拒否・出力処理・Tool動作の退行を利用し得る。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | ProviderのModel・Version・Routingの変更契機と現在の評価対象を把握する。把握不能な範囲を明示する。 |
| SP-2 | 変更後の実経路でSecurity再評価を実行し、条件・結果とModel／Routeを対応付ける。 |
| SP-3 | 未評価の変更先を旧結果だけで継続利用しない。変更検知から再評価・利用再開までの判定と実行順を確認できる。 |

## Scope calibration and adjacent assurance

C3.2.2は学習後の量子化への同じSuiteの再実行。本ControlはProvider側のModel・Version・Routing変更であり、量子化だけを理由に同じFailを転記しない。C12のDrift観測は変更検知を補助するが、継続利用前の再評価そのものではない。

## Threat and failure-mode rationale

可変Aliasや障害Fallbackがモデルを変更しても、アプリのReleaseがないため試験を起動せず、旧版にしか対応しない安全性を前提に利用し続ける。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

Provider通知、Alias解決、Route設定、Fallback、変更検知方法と利用再開の判定を追う。対象Route、Prompt・Tool・出力処理等の設定と評価条件を確認する。可変Aliasのまま内部Versionを保証した説明がないか点検する。

### Positive verification

隔離した模擬Providerで旧版から候補版へ変更する。変更を検出し、候補経路へ保持したSecurity試験を実行してから通常利用へ戻る順序を観測する。実Model・Route・設定と試験結果を記録する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 表示名を保ったままAliasの実Versionを変える | アプリCode不変でも再評価契機として検出する。SP-1。 |
| N-2 | 障害時に未評価Fallbackや別RegionのModelへ切り替える | 旧Routeの結果を流用せず、対象経路の再評価前に通常利用を継続しない。SP-2、SP-3。 |
| N-3 | 再評価Jobを停止する、または旧Routeへ誤接続する | 未完了・対象違いを検出し、評価済みとして再開しない。SP-2、SP-3。 |

### Failure conditions

変更後に再評価せず継続利用する、再評価対象が旧Routeのまま、再評価Jobの完了前に通常利用へ戻す場合はFail。Providerの内部Routeを確認できないときは、その範囲を未立証として残す。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| Provider変更・Route解決記録 | ProviderとRouter運用者 | Model・Version・Region・Fallback | 変更検知時と試験・利用時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 実際の変更と対象経路を追える |
| 再評価と利用再開の記録 | 評価・運用担当者 | Suite・設定・対象Route・実行順 | 変更ごと継続利用前 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 未評価期間に旧結果で通常利用しない |

## Related requirements

[C3.2.2](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.2.2-same-safety-suite-on-quantized-artifact/README.md)は学習後の量子化への同じSuiteの再実行。本ControlはProvider側のModel・Version・Routing変更であり、量子化だけを理由に同じFailを転記しない。C12のDrift観測は変更検知を補助するが、継続利用前の再評価そのものではない。
[C3 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

Providerが実体や変更情報を開示しないと完全な変更検知はできない。Behaviorの監視だけで同一版を証明しない。版固定・通知・契約上の責任と残る観測不能範囲を記録し、無条件Passを主張しない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C3 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [AISVS v1.0 C3.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-02-Model-Validation-Testing.md)
- [C3.2 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.2-model-validation-and-testing.md)
- [C3 Family概要](../README.md)

- [関連Insight：検査するのは入口の文字列ではなく、実際に利用される内容である](../../../../docs/insights/validation-must-cover-effective-payload.md)（Repositoryの横断的な考察。規範やMappingではない）

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
