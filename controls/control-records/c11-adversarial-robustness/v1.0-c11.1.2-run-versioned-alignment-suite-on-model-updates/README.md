---
title: "モデル更新ごとに版管理された安全性試験を実行する"
versioned_id: "v1.0-C11.1.2"
requirement_id: "C11.1.2"
verification_level: 1
family_id: "C11"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C11-Adversarial-Robustness.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C11-Adversarial-Robustness/C11-01-Model-Alignment-Safety.md"
last_verified: "2026-10-05"
maturity: "verifiable"
mapping_assessment_refs: []
---

# モデル更新ごとに版管理された安全性試験を実行する

AISVS Verification Level: 1

[C11.1 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.1-model-alignment-safety-and-robustness.md)

## Upstream basis

AISVS `v1.0-C11.1.2`は、版管理されたAlignment試験Suiteを、Modelの
更新またはReleaseのたびに実行することを求める。ここでのAlignment試験は、
Modelが定めた安全方針に沿って応答するかを確かめる試験である。
対応するAISVS Researchは、CI/CDへの組込み、試験範囲の点検、Modelと
試験のVersionを残す再現可能な結果を例示する。また、固定された試験だけでは
新しい攻撃や複数Turnの失敗を十分に捉えられないと注意する。

正規要件は特定の試験Tool、CI/CD、全攻撃形式の網羅、固定の合格しきい値、
自動Release Gateまでは指定していない。Researchの例をそのまま必須条件に
変えず、実行したか、結果が良好だったか、Releaseを認めるかを区別する。

## Interpretation

対象Modelを変更するたびに、どの試験Suiteのどの版を、どのModel Versionと
設定に対して実行したかを後から確かめられるようにする。Suiteの試験入力、
期待する安全上の判定基準、採点方法を変更した場合も、その時点の内容を
特定できる状態で版管理する。Gitは一つの方法だが必須ではない。

例えば、社内AssistantのModelを旧Versionから新Versionに替えるとき、
旧Versionの合格記録を流用せず、新Versionを対象として同じ版の試験を
実行し、結果をModel変更と結び付ける。試験に失敗しても「実行した」事実は
残るが、その失敗を無視して安全なReleaseだとは言えない。

## Security objective

Fine-tuning、Provider Modelの切替、更新されたModel Artifactの配備で、
以前は守れていた安全方針からの逸脱を見逃しにくくする。試験Suiteと実行対象の
両方を識別することで、「前回は大丈夫だった」という説明を新Versionの証拠に
しない。有限の試験でModelの安全性を完全に保証するものではない。

## Applicability

安全方針に沿ったModelの応答を必要とし、Model VersionやArtifactを更新・
Releaseする製品に適用する。自社開発、Fine-tuning、Open-weight Model、
外部Provider Modelの切替を含む。FallbackやRouting変更で実効的に使う
Modelが変わる経路も対象として確認する。

### Non-applicability

評価対象となるModelを利用せず、Model更新・Releaseの事象が存在しない
境界には適用しない。Infrastructureだけの変更でModelとその実効的な
振る舞いの設定が変わらない場合は、本要件の更新事象とは限らない。
Providerが内部更新を公開しないことだけで対象外にはしない。識別・試験
できない範囲は共有責任と証拠上の制約として明示する。

## Scope and assumptions

- **Model更新・Release**は、新しいModel Artifact、Fine-tuning後の版、
  Providerの版切替、FallbackやRoutingの変更で利用Modelが変わる事象を含む。
  製品ごとのRelease境界と対象Endpointを先に定義する。
- ApplicationのPromptやGuardrailだけを変えるReleaseは、正規要件の
  「Model更新」に必ず含まれるとは断定しない。安全性の再試験は有益でも、
  本Controlの直接のPass条件とは区別する。
- **版管理**は、過去のSuiteの内容と判定基準を一意に取り出せることをいう。
  現在の試験画面や可変なDashboardだけでは過去版を証明できない。
- ProviderがRolling Modelを提供する場合、利用者が観測できる版識別子、
  更新通知、実行時のModel情報を確認する。変化を識別できないなら、
  「全更新で実行」を証明できるとは扱わない。
- 試験結果は非決定的になり得る。再現に必要な設定、反復条件、判定方法を
  記録し、単発の成功だけで広い安全性を主張しない。

## Assets, actors, identities, and trust boundaries

守る対象は、製品の安全方針に沿ったModel応答と、変更時にRegressionを
発見できる能力である。Model開発者・Provider、Release担当者、試験担当者、
製品利用者が関わる。境界は、候補Model・Providerの版から試験実行環境へ、
さらに実際の推論Endpointへと進む経路にある。古いModelや試験Suiteの
結果を、異なる組合せに引き継ぐと保証の根拠が切れる。

## Required security properties

| ID | 必要な性質と確かめ方 |
|---|---|
| SP-1 | Safety/Alignment試験Suiteの内容と判定基準をVersionで特定し、過去版を確認できる。 |
| SP-2 | 定義したModel更新・Releaseの各事象について、対象VersionにSuiteを実行した記録がある。 |
| SP-3 | 各実行のModel Version・対象Endpoint/設定・Suite版・実行日時・結果を対応付けられる。 |
| SP-4 | Fallback、手動切替、Provider切替等の別経路も更新事象の記録に含み、旧Versionの結果を流用しない。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 全更新事象に対し、版管理されたSuiteの対象Versionでの実行と結果を追える | Pass候補。結果がすべて良好とは限らない。 |
| Suiteは版管理されているが、新Versionで実行していない | Fail。版管理だけでは足りない。 |
| 毎回試験しているが、Suiteの過去版や判定基準を特定できない | Fail。版管理を確認できない。 |
| 新Versionで試験を実行し、失敗を記録した | 実行という狭い要件は満たし得る。失敗を無視したReleaseの妥当性は別途評価する。 |
| 固定Suiteは成功したが、未収録の攻撃で失敗する | 本Controlの限界。C11.1.3・C11.1.4等で試験範囲と耐性を別に評価する。 |
| Releaseを止める自動Gateがない | それだけで本ControlのFailとはしない。ただし結果の扱いと承認は別のRelease保証で確かめる。 |

## Threat and failure-mode rationale

Model更新やFine-tuningで安全な拒否の振る舞いが変わっても、旧版の試験結果を
使い回すとRegressionを見落とす。試験Suiteが可変で履歴がなければ、
過去の「合格」が何を試した結果か分からない。手動切替やFallbackが試験
手順を迂回すれば、配備中Versionには評価がないままになる。
外部脅威IDへの厳密なMappingはまだ評価していない。

## Verification

### Architecture and configuration review

Model Inventory、変更・Release手順、FallbackとRouting、試験Suiteの
保管場所、版履歴、実行環境、結果保管場所を確認する。CI/CDがあれば連携を
見てもよいが、手動運用も更新漏れの有無と記録で評価する。試験の入力・
判定基準・採点設定が同じSuite版に含まれるか確かめる。

### Positive verification

直近の複数のModel更新・Release事象を選び、それぞれの変更記録から
対象Model Version、試験Suite版、実行ID、結果まで辿る。必要なら安全な
合成入力でSuiteを再実行し、記録したVersionと設定で同じ判定を再現
できるか確かめる。試験に失敗した場合も結果が欠落せず残ることを見る。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | 新Modelへ切り替え、旧Modelの試験結果だけを示す | 新Versionの実行記録がないと分かり、SP-2・SP-3のPassにしない。 |
| N-2 | Suiteの判定基準を変更し、古い合格結果を現在のSuiteの結果として示す | Suite版の不一致を検出し、過去の判定を再解釈しない。SP-1・SP-3。 |
| N-3 | Fallbackや手動切替を通して未試験Modelを利用する | その変更事象に実行記録がないと分かる。SP-2・SP-4。 |
| N-4 | 実行が途中で止まった結果を完了済みとして示す | 完了状態と試験範囲の欠落を見分け、不完全なRunを実行証拠としない。SP-2・SP-3。 |
| N-5 | Provider切替後に実行対象のModel識別子を記録しない | 実際の対象版を確かめられず、証拠不足とする。SP-3。 |

### Failure conditions

対象Model更新・ReleaseのいずれかでSuite未実行、試験Suiteの版履歴が
確認できない、実行対象と結果の紐付けができない、または旧Versionの結果を
流用した場合は本ControlをPassにしない。実行が中断・欠落した場合も
完了した試験として扱わない。試験結果の安全水準、合格しきい値、
Release Gateの不備は重要だが、本要件の「実行したか」と分けて報告する。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認する時期 | 保護上の注意 | 合格の目安 |
|---|---|---|---|---|---|
| Model変更台帳 | Model/Release担当者 | Model Version、Endpoint、Fallback、変更日時 | 各更新・Release時 | 内部Endpointや構成詳細を公開しない | 評価対象の変更事象を漏れなく列挙できる。 |
| 試験Suiteの版履歴 | 試験Suite管理者 | 入力、期待判定、採点設定 | Suite変更時 | 有害な実例や機密Dataを公開しない | 実行当時の内容を一意に取り出せる。 |
| 試験実行結果 | 試験実行者または自動化基盤 | 対象Model、Suite版、実行ID、完了状態、結果 | 各更新・Release時 | Raw出力の機密性と改ざん対策を考慮する | 変更台帳の各事象に対応し、失敗と中断も見える。 |

## Related requirements

| Requirement | 関係と違い |
|---|---|
| `v1.0-C11.1.1` | Modelが安全性の訓練・調整を受けたか。本Controlはその後の変更ごとの試験実行。 |
| `v1.0-C11.1.3` | 実際のModalityに関係する既知の攻撃で評価する。Suiteの版管理・実行だけでは試験範囲は保証できない。 |
| `v1.0-C11.1.5` | 有害出力率の自動評価とRegressionしきい値。結果を測り、悪化を検知する保証は別。 |

## Known limitations and uncertainty

版管理した固定Suiteは未知の攻撃や新しい言い換えを網羅できず、過学習や
試験環境と本番環境の差も残る。Researchの多Turn・多言語・多Modalityの
例は試験設計の助けになるが、一律の網羅条件ではない。Providerの
Silent Updateでは正確な変更事象を利用者が観測できない場合があり、
その場合は「全更新で実行」を無条件に主張できない。試験を実行したことは
安全な結果、Releaseの妥当性、製品全体の適合を意味しない。
`verifiable`は本書の成熟度であり、実製品の適合結果ではない。

## References

- [AISVS v1.0 C11 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C11-Adversarial-Robustness.md)
- [AISVS v1.0 C11.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C11-Adversarial-Robustness/C11-01-Model-Alignment-Safety.md)
- [C11 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-05 | 初版。Suite版と各Model更新での実行を分け、結果の良否・Release判断と区別する | AISVS固定版と本Repositoryの解釈 | 本書の必要な性質・試験・証拠。実製品での試験は未実施 |
