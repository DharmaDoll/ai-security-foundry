---
title: "AI InteractionをSession ContextとAI固有Telemetryに結び付けて記録する"
versioned_id: "v1.0-C12.1.1"
requirement_id: "C12.1.1"
verification_level: 1
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

# AI InteractionをSession ContextとAI固有Telemetryに結び付けて記録する

AISVS Verification Level: 1

学習資料：[C12.1 Request & Response Logging](../../../learning/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.1-request-response-logging.md)

## Upstream basis

AISVS `v1.0-C12.1.1`は、AIとのやり取りをSession ContextとAI固有の
Telemetryとともに記録することを求める。対応Researchは、推論Eventと実際の
Session／会話、複数のHop、Agentと人間の主体の結合が欠けると事後調査が
難しくなる点を補足し、OpenTelemetry等を例示する。Normative本文は特定の
Telemetry製品、Field名、Raw PromptやResponseの全量保存を指定しない。

## Interpretation

製品の対象となるAI Interactionごとに、後から該当するSessionまたは同等の
一連の実行Contextへ辿れるEventを記録する。Eventには通常のHTTP成功／失敗
だけでなく、そのInteractionがどのAI処理であったか分かるTelemetryを含める。
例えば、Request IDだけを残してSessionとの接続を失った場合や、Model呼出しを
単なる汎用API呼出しとして記録するだけの場合は不十分である。

ここでの「Session」は必ずしもBrowserのCookie Sessionではない。Batch、
Schedule、Agentによる処理ではJob／Run／Conversation等の継続Contextでよいが、
任意に生成した孤立Event IDだけで複数Stepの関係を再構成できるとは扱わない。
AI固有TelemetryのField群は対象Systemに合わせて定義し、C12.1.3が列挙する
推論Eventの最低Fieldを本Controlへ無条件に前倒ししない。

## Security objective

AIが何を処理したか、どの一連のSessionで起きたかを追える基礎的な監査証跡を
作り、攻撃調査・障害解析・影響範囲の特定に必要なContextの欠落を防ぐ。

## Applicability

会話型LLM、RAG、Agent、MCP経由の推論、Batch推論等、SystemがAI
Interactionを処理する経路に適用する。Frontend、Gateway、直接SDK呼出し、
非同期Job等、実際に使われる経路を対象にする。

### Non-applicability

対象SystemがAI Interactionを一切行わない場合には適用しない。人間との
対話がないBatch処理や、Browser Sessionを使わないAgent実行はそれだけで
N/Aにせず、同等の実行Contextで評価する。

## Scope and assumptions

- 「Interaction」の粒度は、調査時に個々のAI処理を区別できるよう定める。
  一つのUser Turnが複数のModel呼出しを生む場合、それらを同じSession内の
  別Eventとして辿れる必要がある。
- Session Contextの正本はApplication／Gateway等の信頼できる処理Context。
  Modelが生成したSession名や、Userが自由に指定できる識別子だけに頼らない。
- AI固有Telemetryは少なくともAI操作の種類や対象を、汎用Request Logと
  区別できる情報である。具体的なField、相互運用Schema、Token集計は
  C12.1.3等の別の要件で追加評価する。
- Logへの機密情報集積と閲覧権限は別の重大なSecurity Propertyである。
  Raw Prompt／Responseの一律保存を本ControlのPass条件にしない。

## Assets, actors, identities, and trust boundaries

保護対象はAI処理の追跡可能性と、調査時に必要な因果関係。Actorsは
利用者、Agent、Application／Gateway、Model Provider、Telemetry Collector、
調査者である。攻撃者は異常な入力を送ったり、侵害した一部の実行経路で
Eventを欠落させたり、User入力に偽のSession情報を混ぜたりし得る。

Trust Boundaryは、User／AgentからApplication Context、Applicationから
ProviderやTool、各ComponentからTelemetry Store、Storeから調査者への
間にある。Session・Trace識別子は信頼できる境界で発行・伝播し、
未信頼入力をそのまま監査上の正本にしない。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 対象のAI Interactionを、実際のSession／会話／Job等のContextへ結び付けるEventとして記録する。 |
| SP-2 | そのEventに、当該処理を汎用API呼出しと区別して調査できるAI固有Telemetryを含める。 |
| SP-3 | 複数Step・非同期処理・Retry等でも、Eventと元のSession／実行Contextとの関係を再構成できる。 |
| SP-4 | 記録Eventが想定するTelemetry Storeへ到達し、必要な期間・権限の範囲で検索可能であることを実測で確認できる。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| AI呼出しの件数だけあるが、Sessionと操作の対応がない | SP-1／SP-2が不足しFail。 |
| 一件ごとのRequest IDはあるが、一連の会話・Jobへ結合できない | Session Contextを示せずFail。 |
| SessionとAI操作を追えるが、Safety FilterのRuleや判断理由はない | 本ControlのPass候補。判断Eventの詳細はC12.1.2で別評価。 |
| Sessionを追えるが、Providerや入出力Token数がない | 本Controlだけでは直ちにFailとはしない。C12.1.3の最低Fieldは別途評価。 |
| RAG検索の文書IDやQueryがない | 本ControlとC12.1.4は分けて評価する。 |
| LogにRaw Promptがない | それだけでFailではない。調査目的に必要なContentの保管は別途設計する。 |
| Logに秘密情報が複製され、広いRoleから閲覧できる | Session記録の存在は漏えいを打ち消さない。Log保護・Privacyを別の重大問題として扱う。 |

## Threat and failure-mode rationale

SessionやAI処理のContextがないと、複数Turnにまたがる攻撃、異常な再試行、
Agentの連鎖行動、Provider切替後の不具合を関連付けられない。Logを出力する
設定だけあっても、Collectorへ届かない、相関IDを途中で失う、直接SDK経路だけ
欠落する場合は調査能力が成立しない。外部Threat IDへの厳密なMappingは
未評価とする。

## Verification

### Architecture and configuration review

対象AI経路を列挙し、Session／Runの発行、Context伝播、Event生成、
Collector、保管、検索までのData Flowを追う。非同期Task、Retry、
Gateway迂回、Toolからの再推論を含め、どの境界でContextが失われ得るかを
確認する。Telemetry Fieldの意味と、Log閲覧・保存Policyも確認するが、
後者を本RequirementのField条件と混同しない。

### Positive verification

合成の二つのSessionでそれぞれ複数AI呼出しを行い、各EventのAI操作と
正しいSessionへの結合を保管先で再構成する。非同期StepやRetryを含む
代表経路でも同じ結果になることを確認する。Event発行の設定ではなく、
実際に検索できる保管Eventを証拠にする。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 同じUserが二つのSessionで推論し、一方のEventからSession情報を落とす | 混同・欠落を検知し、全対象Eventが正しいSessionに属することを確認する。SP-1, SP-3 |
| N-2 | Gatewayを迂回する直接SDK呼出しや非同期Jobを追加する | AI Interactionの未記録経路を発見する。SP-1, SP-2 |
| N-3 | HTTP状態・時刻だけの汎用Access Logを残す | AI操作を識別できず、SP-2の証拠にならない。 |
| N-4 | Retry／複数Agent StepでTrace Contextを切る | Sessionとの結合が壊れたEventを発見する。SP-3 |
| N-5 | Eventの送信だけ成功させ、Collector側で破棄・Samplingする | 保管先の検索で欠落を発見する。SP-4 |
| N-6 | Userが偽のSession IDをRequest Bodyに含める | 信頼できるSession Contextの正本を上書きできない。SP-1, SP-3 |

### Failure conditions

対象のAI Interactionが記録されない、Session／実行Contextと結び付かない、
AI処理と分かるTelemetryがない、またはEventが発行側にしか存在せず
保管先で確認できない場合はFail。個々のEventに全Prompt・Response本文が
ないことや、C12.1.2〜.4固有のFieldがないことだけを本ControlのFailとしない。
Telemetry障害時の推論停止を本要件の一律条件とはしない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| AI InteractionとEventのData Flow | Application／Telemetry Owner | 全推論・Agent・Batch経路 | 経路・SDK変更時 | 具体的User IDや秘密を含めない | Session ContextとAI Fieldの生成・伝播・保管先が明確。 |
| 合成SessionのEnd-to-end Trace | Test Harness／Collector | N-1〜N-6、複数Stepと迂回経路 | Release・Instrumentation変更時 | 合成IDのみ使用 | 保管Eventを検索し、正しいSessionとAI操作へ辿れる。 |
| Telemetry欠落の監視結果 | Telemetry Owner | Collector、Sampling、検索可能期間 | 運用の代表期間 | Log閲覧者を制限 | 記録欠落や保管失敗を判別できる。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C12.1.2` | Safety／Policy判断の監査可能な詳細。Session Contextだけでは代替しない。 |
| `v1.0-C12.1.3` | 推論Eventの相互運用Schemaと指定Field。本ControlのAI固有Telemetryより具体的。 |
| `v1.0-C12.1.4` | RAG検索のQuery・取得文書・Knowledge Sourceの記録。一般的なAI Interaction Eventでは代替しない。 |
| `v1.0-C12.2.2` | 行動異常を見つける検知。記録は入力となるが、Logの存在だけで検知できない。 |

## Known limitations and uncertainty

Session相関ができても、Contentを保管しなければ後から詳細なPrompt／Responseを
再現できない場合がある。一方、内容の全量収集は機密情報の集中を招く。
ResearchはAgentと人間の二重帰属や特定のTelemetry Fieldを提案するが、
Normativeの短い文面はField集合や匿名・Batch処理でのIdentity表現を定義
していない。本ControlはSession／実行ContextとAI操作の対応を直接の
保証とし、Actor帰属や詳細Schema、内容記録、Logの改ざん耐性は隣接保証として
別途評価する。`verifiable`は本Artifactの成熟度であり、実製品の証拠ではない。

## References

- [AISVS v1.0 C12 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md)
- [AISVS v1.0 C12.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-01-Request-Response-Logging.md)
- [C12 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-10-03 | C12.1.1初版。Session相関とAI固有Telemetryの基礎保証を分離して検証 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
