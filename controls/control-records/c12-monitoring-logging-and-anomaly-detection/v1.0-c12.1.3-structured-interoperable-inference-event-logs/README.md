---
title: "AI推論Eventを指定Fieldを持つ構造化Schemaで記録する"
versioned_id: "v1.0-C12.1.3"
requirement_id: "C12.1.3"
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

# AI推論Eventを指定Fieldを持つ構造化Schemaで記録する

AISVS Verification Level: 2

学習資料：[C12.1 Request & Response Logging](../../../learning/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.1-request-response-logging.md)

## Upstream basis

AISVS `v1.0-C12.1.3`は、AI推論EventのLogが構造化・相互運用可能な
Schemaに従い、少なくともModel Identifier、入力と出力のToken使用量、
Provider Name、Operation Typeを含むことを求める。対応Researchは
OpenTelemetry GenAIのFieldや、要求したModel Aliasと実際にServingされた
Modelを区別する検証例を挙げる。ただしNormative本文はOTel採用、
要求Modelと実際のModelの二Field、特定Schema Versionを指定しない。

ResearchにはContentを既定で記録しないというPrivacy上の提案もあるが、
NormativeのC12.1.3自体はその禁止を明記していない。Raw Contentの
収集制限は重要な別の設計判断として扱い、四つの最低Fieldと混同しない。

## Interpretation

実際の推論処理から得たEventを、ProviderやInstrumentationが異なっても
同じ意味で読み取れるField構造へ正規化して保管・Exportする。各Eventから
どのModelを対象に、どのProviderで、どの種類の推論を、入出力それぞれ
何Token使って行ったかを取り出せるようにする。単一の自由文Messageや
Vendor固有の不透明Payloadへ全情報を押し込み、利用側が共通Fieldとして
読めない状態は「構造化・相互運用可能」とは扱わない。

例えば複数Providerを束ねるGatewayが、全てを`provider=gateway`、
`model=default`として記録するだけでは、実際のProviderとModelを識別
できない。要求Aliasしか分からない場合はその値と「Serving先は不明」
という限界を明示する。Providerが実際のServing Model IDを返すなら、
Researchに従って要求値と区別して記録するのが有用だが、この二重記録
そのものをNormativeの一律必須Fieldとはしない。

## Security objective

推論EventをBackendやTool間で比較・集計・調査できるようにし、Model／
Provider変更、異常なToken消費、Operationの違いを曖昧なLog表現で
見落とさないようにする。

## Applicability

Systemが行うAI推論のEventに適用する。直接SDK呼出し、Gateway、
Multi-provider Routing、Streaming、Agentの反復推論、Batch推論等、
本番で利用する各経路を含める。

### Non-applicability

対象SystemがAI推論を実行しない場合には適用しない。推論を外部Providerへ
委ねるだけでN/Aとはならず、自Systemが利用した推論EventをどのFieldで
取得・記録できるかを評価する。RAG検索だけでModel推論がないEventは、
この要件の推論Eventと区別する。

## Scope and assumptions

- Model Identifierは、Eventで観測できる要求先・実際のServing先の区別を
  明示する。単なる`unknown`や全Model共通の固定値を識別子として数えない。
- 入力Token数と出力Token数は別Fieldとして意味・単位を定める。成功Eventの
  値が欠落した場合に`0`で埋めず、Errorや中断で未取得ならその状態を示す。
- Provider NameはGatewayの製品名だけでなく、推論を提供した先を
  識別できる値とする。経路によって実際のProviderが見えないときは
  観測可能な値と限界を分けて記録する。
- 「相互運用可能」は単一Vendor専用Parserを前提にしないこと。Field名、
  型、単位、Operationの語彙、Versionを説明・Exportできれば、特定の
  業界Schemaを採用しなくても評価できる。
- Query／Prompt／Responseの全文収集は本要件の最低Fieldではない。
  Metadataも個人や利用状況を示し得るため、保護不要とはみなさない。

## Assets, actors, identities, and trust boundaries

保護対象は推論Eventの比較可能性、調査時のModel／Provider／利用量の
再構成。ActorsはApplication、Gateway／Inference Adapter、Provider、
Telemetry Pipeline、調査者。攻撃者は一部の入力や経路を変えてLogの
欠落・不正なField値を誘発したり、広く閲覧可能なLogから利用情報を得たり
し得る。

Trust Boundaryは、Provider ResponseからAdapter、Adapterから共通Schema、
Collectorから保管先、保管先から調査者への間にある。User／Modelが書いた
自由形式の文字列を、ProviderやToken使用量の正本にしない。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 対象の推論Eventに、Model Identifier、入力Token使用量、出力Token使用量、Provider Name、Operation Typeが区別可能な構造化Fieldとして存在する。 |
| SP-2 | Fieldの型・単位・値の意味が経路間で定義され、Providerごとの値を共通形式へExport・検索できる。 |
| SP-3 | 記録値が実際の推論処理または信頼できる計測結果に由来し、未知・未取得・中断と有効な`0`を混同しない。 |
| SP-4 | 全対象推論経路のEventが保管先で確認でき、代表Eventから最低Fieldを再構成できる。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| Session IDだけを記録し、Model／Provider／Token数等がない | C12.1.1の相関はあり得るが本ControlはFail。 |
| JSON Logだが必要値は全て一つの自由文Messageに埋まる | 構造化Fieldとして利用できずFail。 |
| 入出力Token数を合算した総数だけ記録する | Normativeの両方向を区別できずFail。 |
| 要求Aliasを記録し、実際のServing ModelはProviderから取得できない | `model identifier`の最低Fieldは評価可能だが、実際のServing先の再現性に限界があると明記する。 |
| 複数Providerを束ね、全EventにGateway名だけを書く | 実Providerを識別できないならFail。 |
| OTel準拠でないが、Fieldの意味・型・Exportが共通化される | 特定方式の不採用だけでFailとしない。 |
| Raw Prompt／Responseを記録しない | 最低Fieldの欠落ではない。Content Captureの要否・保護は別途評価する。 |
| Policy判断やRAG取得文書がLogにない | C12.1.2・C12.1.4で別評価する。 |

## Threat and failure-mode rationale

非構造化や経路ごとに異なるField表現は、Model差替え、Provider Routing、
Token急増を横断的に見えなくする。Aliasだけを実Modelと誤認すると、
事後の再現や影響範囲の特定にも限界が出る。逆に、相互運用のためとして
Prompt全文を全Telemetry Storeへ複製すれば、別の機密漏えい経路を作る。
外部Threat IDとの厳密なMappingは未評価とする。

## Verification

### Architecture and configuration review

全推論経路、Adapter／Gateway、Provider Response、Schema変換、Exporter、
保管先を追う。Field名・型・単位・Operation語彙、Unknown／Error表現、
Token数の取得元、Model AliasとServing Modelの区別を確認する。
SchemaまたはInstrumentation変更時の互換性と、Raw Contentが別Event層へ
流れる可能性も確認するが、内容収集の禁止を本要件の直接条件にしない。

### Positive verification

二つのProvider、異なるModel、通常推論と別Operation、Streaming完了を
含む合成実行を行い、保管Eventを共通のQuery／Exportで読む。各Eventに
最低Fieldがあり、入出力Token数が個別に取得できることを確認する。
値がProvider Responseまたは信頼できる計測値に一致することも照合する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 第二ProviderへRoutingし、全EventへGateway名と`default` Modelを書かせる | 実Provider／Modelを識別できずFail。SP-1, SP-3 |
| N-2 | Token総数だけを残す、または出力Token欄を常に`0`で埋める | 入出力の分離・値の意味の欠落を検出する。SP-1, SP-3 |
| N-3 | ProviderごとにToken単位とOperation値の意味を変え、変換せず同じFieldへ入れる | 比較・Exportの不整合を検出する。SP-2 |
| N-4 | JSONの`message`一Fieldへだけ必要情報を埋め込み、共通Fieldを消す | 構造化された最低Fieldを検索できずFail。SP-1, SP-2 |
| N-5 | Streaming中断・Provider Errorで未取得Token数を有効な`0`として記録する | 中断／未取得状態と実測値を区別する。SP-3 |
| N-6 | Gateway迂回経路やExporter変更後にEventをCollectorで破棄する | 保管先でのField欠落・未記録経路を発見する。SP-4 |

### Failure conditions

成功した推論Eventに指定されたModel、Provider、Operation、入出力別Token
使用量が構造化Fieldとしてなく、またはFieldの意味が経路間で比較不能なら
Fail。推論経路自体が未記録、ダミー値で埋められている場合もFail。
Providerが実際のServing Modelを公開しない場合は、観測できるAliasと
限界を明示して評価する。OTel不採用、Raw Contentを既定で記録しないこと、
二重Model FieldがないことだけをFail条件にしない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 共通Schema定義とFieldの由来 | Telemetry／Inference Owner | 全Provider・Operation | Schema・Provider変更時 | Prompt・秘密を含めない | 最低Fieldの型・意味・単位と取得元が説明できる。 |
| 合成推論のEnd-to-end Event | Test Harness／Collector | N-1〜N-6、複数Provider／Streaming | Release・Instrumentation変更時 | 合成IDを使用 | 保管先で全Eventの最低Fieldを同じ方法で読める。 |
| Provider Responseとの値の照合 | Inference Adapter Owner | Model、Provider、入出力Token数 | SDK・Routing変更時 | Response内の機密値を保護 | ダミー値やAlias誤認がなく、観測不能なFieldは明示される。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C12.1.1` | AI InteractionとSession Contextの相関。本Controlは推論Eventの共通Fieldを要求する。 |
| `v1.0-C12.1.2` | Safety／Policy判断の詳細。推論Eventの共通Schemaだけで判断内容は分からない。 |
| `v1.0-C12.1.4` | RAG検索のQuery・取得文書・Sourceの記録。推論Token数では代替しない。 |
| `v1.0-C12.2.5` | Token使用量をUser・Session・Feature・Team等へ帰属する。推論Eventの入出力数だけでは帰属は完成しない。 |

## Known limitations and uncertainty

「相互運用可能」はNormativeで特定の標準名が示されず、Schemaの統一度は
実際のExport・Queryで評価する必要がある。要求Aliasだけしか得られない
ProviderではServing Snapshotまで再現できない。Tokenの計測定義や
Error時の取得可否もProviderに依存する。Researchは実Serving Modelの
Field、OTelの具体属性、Content既定除外を勧めるが、これらをNormativeの
一律必須条件へ昇格させない。Metadataにも個人の利用状況が含まれ得る。
`verifiable`は本Artifactの成熟度であり、実製品のLog品質を証明しない。

## References

- [AISVS v1.0 C12 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md)
- [AISVS v1.0 C12.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-01-Request-Response-Logging.md)
- [C12 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-10-03 | C12.1.3初版。最低FieldとSchema互換性、観測不能なServing先の限界を分離して検証 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
