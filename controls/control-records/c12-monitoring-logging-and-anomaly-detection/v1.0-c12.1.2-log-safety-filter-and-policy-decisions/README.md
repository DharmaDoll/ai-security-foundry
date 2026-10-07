---
title: "Safety FilterとPolicy判断を監査・調査できる詳細で記録する"
versioned_id: "v1.0-C12.1.2"
requirement_id: "C12.1.2"
verification_level: 2
family_id: "C12"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-01-Request-Response-Logging.md"
last_verified: "2026-10-03"
maturity: "verifiable"
mapping_assessment_refs: []
---

# Safety FilterとPolicy判断を監査・調査できる詳細で記録する

AISVS Verification Level: 2

学習資料：[C12.1 Request & Response Logging](../../../learning/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.1-request-response-logging.md)

## Upstream basis

AISVS `v1.0-C12.1.2`は、Safety FilteringとPolicy判断を、Content Moderation
Systemの監査・Debug・Forensic Analysisに十分な詳細で記録することを求める。
対応Researchは、適用したPolicy／Rule、判断結果、カテゴリ、入力か出力かという
Stage、対象Requestとの相関、Scoreが存在する場合の意味を確認例とする。
一方、Provider間でScoreの形式が異なり、全製品が数値Scoreを出すわけではない。
Researchの特定Field名、製品、Hash方式を規範の一律必須条件にしない。

## Interpretation

Safety FilterやContent Moderation Policyが評価を行った際に、対象となる
処理、適用したPolicy、何を判断したか、結果として何をしたかを、後から
区別・再構成できるEventとして残す。許可、拒否、削除／伏せ字、代替応答、
判定不能やFilter Errorも、その経路で実際に生じた扱いを追えるようにする。

例えば「blocked=true」だけでは、入力と出力のどちらを、どのPolicyで、
何のカテゴリとして拒否したか分からない。逆に、Full Promptや認証Headerを
丸ごとLogへ複製しなくても、識別子・Policy版・Stage・結果と、必要に応じた
保護されたContentへの参照で調査可能性を設計できる。

## Security objective

Moderationの判断と実際の適用結果を監査し、誤遮断、見逃し、設定変更や
Filterの失敗を調べられるようにする。Modelの「拒否しました」という応答文を
Policy実行の証拠と取り違えない。

## Applicability

AI入力・出力にSafety Filter、Guardrail、Content Moderation Policyを
適用する経路に適用する。複数Provider、Local Filter、Fallback、Streaming、
Batch、Agent経路がある場合、それぞれの実際の判断地点を確認する。

### Non-applicability

対象となるSafety／Moderation判断が存在しないSystemでは、この記録対象は
存在しない。ただし、Filterを導入していない事実は、C2やC7等の必要な
安全制御を満たしていることを意味しない。Content Moderationと関係のない
すべての業務認可Policyを、本Requirementの対象へ無制限には広げない。

## Scope and assumptions

- 「十分な詳細」は、監査・Debug・Forensicの問いに答えられることとして
  評価する。固定のVendor Schemaや全Contentの保存を意味しない。
- Policy ID／Version、入力・出力等のStage、カテゴリ、判断、実際の処理、
  時刻、相関IDは有用な例。Systemが判定に使用する値を再現できるようにし、
  存在しないScoreを捏造しない。
- 判断を行うTrusted ComponentがEventを生成する。Modelの自己申告や
  Userが付けたLabelだけを正本にしない。
- Filterが評価されなかった場合、単に拒否文がないことを「許可判断の記録」
  とみなさない。Filter失敗・迂回を調べるには期待Eventとの突合が必要。
- LogはPrompt、Response、Header、Token等の秘密を集め得る。収集内容、
  閲覧権限、保存期間は必要性に合わせて別途制限する。

## Assets, actors, identities, and trust boundaries

保護対象はSafety／Policy判断の監査可能性、誤遮断や回避の原因究明、Log内の
機密情報。Actorsは利用者、Model／Agent、Filter・Policy Engine、Application、
Telemetry Collector、調査者。攻撃者は入力・取得Contentを操作して判断を
回避したり、侵害した経路でLogを欠落・改ざんしたりし得る。

Trust Boundaryは、非信頼ContentからFilter、FilterからApplicationの
実際の扱い、判断ComponentからLog Store、Storeから調査者への間にある。
AI出力と安全判断を同じ信頼度に置かず、またLog Storeを無制限なRaw
Contentの複製先にしない。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 対象経路で実行されたSafety Filter／Content Moderation Policyの判断を、Trustedな判断地点からEvent化し、対象Request・Sessionへ結び付ける。 |
| SP-2 | 各Eventで、適用Policy／Ruleまたは同等の判断根拠、入力／出力等のStage、分類・理由、判断結果と実際の処理を再構成できる。 |
| SP-3 | Allow、Block、Redact、Fallback、Error等、対象経路で起きる判断・失敗状態がLogから区別できる。成功した拒否だけを記録しない。 |
| SP-4 | 生成したEventが必要な期間保管・検索可能で、監査・Debug・事後調査に使える。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| Filterが入力を拒否したが「拒否」だけを記録する | Policy・Stage・理由・対象処理が不明ならFail。 |
| Filterが許可した場合は一切記録せず、拒否だけ残る | 判断全体や回避経路を再構成できずFail。 |
| Providerが数値Confidenceを提供せず、カテゴリ・判断・理由は追える | 数値Scoreの欠落だけでFailとしない。判定の根拠と限界は示す。 |
| Logは十分だが、危険な出力を実際には遮断しない | 本Controlの記録とC7の遮断は別保証。Logだけで安全な出力とは言えない。 |
| Modelの拒否文だけ残り、Filter／Policy判断Eventはない | Model応答は判断Componentの証拠を代替せずFail。 |
| Ruleと結果はあるが、全Raw Promptがない | 直ちにFailではない。詳細なContent調査が必要なら保護された参照等を別途評価する。 |
| 認可PDPの判断を記録しているがContent Moderationは記録しない | 他DomainのLogで本Controlを代替できない。 |

## Threat and failure-mode rationale

判断Eventがない、またはStage・Rule・Outcomeが欠落すると、攻撃を見逃したのか、
Filterが呼ばれていないのか、呼ばれたがErrorだったのかを区別できない。
逆にFilterの実行Contextを丸ごとLogへSerialiseすると、認証Headerや
個人情報を広いTelemetry Storeへ漏らす。外部Threat IDの厳密なMappingは
未評価とする。

## Verification

### Architecture and configuration review

入力・出力それぞれのSafety／Policy判断地点を列挙し、判断、Applicationでの
適用、Event生成、Collector、保管先のData Flowを追う。Allow／Block以外の
Redact、Fallback、Timeout、Errorも確認する。Policy版、カテゴリ、Stage、
Request／Session相関、Logの閲覧・保持Policyを点検し、Raw Contentや
Secretの複製範囲を明示する。

### Positive verification

合成Input／Outputで許可・拒否・伏せ字等の代表判断を発生させる。保管された
Eventから、何に、どのPolicyが、どのStageで、どの結果を出し、Applicationが
どう扱ったかを再構成する。対象ResponseやRequestとの結合も確認する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 同じContentを入力Stageと出力Stageで検査し、両EventからStageを消す | 異なる判断地点を区別できず、SP-2の欠落として検出する。 |
| N-2 | Policy変更前後で同じカテゴリを評価し、版／Ruleを記録しない | どのPolicyが効いたか再構成できず、SP-2の欠落を発見する。 |
| N-3 | 許可、遮断、伏せ字、判定Errorを発生させる | それぞれの判断と実際の扱いを区別できる。SP-2, SP-3 |
| N-4 | Output Filterを迂回する経路やExporterで捨てられるEventを作る | 期待した判断Eventとの突合と保管先検索で欠落を検出する。SP-1, SP-4 |
| N-5 | Guardrailが受け取ったHeader・Token・Raw ContentをEventへ混入させる | 必要性のないSecret複製を検出し、収集・閲覧範囲を是正する。隣接するLog保護の確認。 |

### Failure conditions

対象のSafety／Moderation判断が記録されない、対象処理・Policy・Stage・結果を
実質的に辿れない、成功した拒否しか記録せず許可やErrorを区別できない、
またはEventが保管先で見つからない場合はFail。Score、Token数、特定Schema、
全文保存、暗号学的な改ざん検知の欠如だけを、このRequirementの一律Fail
条件にはしない。Logの機密漏えいは別の重大な問題として報告する。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 判断Eventの設計・Data Flow | Safety／Policy Owner | 全入力・出力・Fallback経路 | Policy／Provider変更時 | Raw Prompt・Secretを含めない | Policy、Stage、カテゴリ、判断、適用、相関のFieldと正本が分かる。 |
| 合成判断のEnd-to-end試験 | Test Harness／Telemetry Owner | N-1〜N-4、Allow／Block／Error | Release・Policy変更時 | 合成Content・IDを使用 | 保管Eventから判断と実際の扱いを再構成できる。 |
| Log内容と閲覧境界の点検 | Security／Privacy Owner | N-5、Collector・Store | Exporter／Guardrail変更時 | 記録例も機密情報として制限 | 不要なSecretが複製されず、調査者権限が明確。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C12.1.1` | InteractionのSession相関とAI固有Telemetry。Policy判断の詳細は本Controlが扱う。 |
| `v1.0-C12.1.3` | 推論Eventの構造化・相互運用Schemaと指定Field。Safety判断Eventの内容とは別。 |
| `v1.0-C12.2.1` | 攻撃の検知・Alert。Policy判断Logは調査材料だが、検知を代替しない。 |
| `v1.0-C7.3.1` | 有害Contentの分類・遮断。正しいLogだけでは出力遮断は保証されない。 |

## Known limitations and uncertainty

Contentを抑制したLogは調査時に全文を再生できないことがあるが、全Contentの
無制限保存は別のRiskを作る。Policy IDや分類だけでは、誤分類の根本原因を
完全には説明できない。Provider Scoreは相互比較可能とは限らず、Scoreを
持たない製品もある。「sufficient detail」の線引きは製品の判断種類と
調査目的に依存する。Researchが挙げる特定Field、Hash、Telemetry製品を
Normativeとして扱わない。`verifiable`は本Artifactの成熟度であり、
製品のModerationやLog保護の実証ではない。

## References

- [AISVS v1.0 C12 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md)
- [AISVS v1.0 C12.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-01-Request-Response-Logging.md)
- [C12 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-10-03 | C12.1.2初版。Moderation判断の記録と実際の遮断を分離して検証 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
