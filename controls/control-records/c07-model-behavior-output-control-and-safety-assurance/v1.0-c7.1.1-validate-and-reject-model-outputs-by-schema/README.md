---
title: "全Model出力を定義済みSchemaで検証し、不一致を拒否する"
versioned_id: "v1.0-C7.1.1"
requirement_id: "C7.1.1"
verification_level: 1
family_id: "C7"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-01-Output-Format-Enforcement.md"
last_verified: "2026-09-30"
maturity: "verifiable"
mapping_assessment_refs: []
---

# 全Model出力を定義済みSchemaで検証し、不一致を拒否する

AISVS Verification Level: 1

学習資料：[C7.1 Output Format Enforcement](../../../learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.1-output-format-enforcement.md)

## Upstream basis

AISVS `v1.0-C7.1.1`は、Applicationが全Model出力を定義済みSchemaで検証し、
不一致を拒否することを求める。対応Researchは、Model出力を非信頼Dataとして
扱う理由と、不正な構造が後続ParserやWorkflowへ入る失敗を説明する。
JSON Mode、Structured Output、制約付き生成は補助になり得るが、
特定の生成方式やLibraryをNormative本文は指定しない。

## Interpretation

Modelが生成した値をApplicationが受け取る各経路について、下流が受け入れる
**出力契約**を事前に定義し、実際の出力をその契約へ照合する。不一致なら
User表示、Tool呼出し、保存、後続Agent Step等の利用へ進めない。
「JSONとしてParseできた」「Providerに形式を指定した」「Modelが従うはず」は、
ApplicationによるSchema検証と拒否の証拠にならない。

Schemaは用途に合わせて、必要なField、型、許可値、入れ子構造、追加Fieldの扱い等を
定義する。自由記述Textの経路も「任意文字列なら常に合格」と暗黙に扱わず、
その経路で検証可能な形式契約と公開・利用単位を明示する。ただし、文意の正確性や
危険性はSchemaだけで判定できず、C7.2／C7.3等の別保証となる。

ModelのRetry／再生成／Fallbackで新しい出力が得られた場合も、その出力を検証する。
Streamingは方式だけでFailとしないが、断片を公開・実行する時点までに
必要な契約を検証できているかを確認する。全文を待たないと検証できない契約なら、
未検証の断片を取り消せない下流へ渡してから最後に拒否しても、この境界は守れない。

## Security objective

Model由来の予想外の構造・値が、Applicationの解釈を変えたり、後続処理へ
未検証で流れたりすることを防ぐ。Schema適合は形式契約の保証であり、
正しい判断、無害なContent、適切な権限を保証しない。

## Applicability

Model出力をUserへ表示する、Tool／API引数へ使う、Data Storeへ保存する、
次のPromptやAgentへ渡す、外部Systemへ送るApplicationに適用する。
Tool Call引数、Structured Response、自由記述の表示Contentなど、
実際に利用する出力経路を棚卸しする。

### Non-applicability

Model出力を受け取らず利用しない決定論的処理は対象外。
ある出力経路が人間向けの自由記述であることだけでは対象外にしない。
ただしSchemaで意味の正しさまで保証するような拡張はしない。

## Scope and assumptions

- 「全Model出力」は、製品が利用する各Model出力経路を指す。Reasoningの非公開内部状態等、
  Applicationが取得も利用もしないDataまで検証したと主張する必要はない。
- Schemaは出力の受け入れContractに一致する必要がある。形式上あらゆる値を
  許すSchemaは、このControlの保証価値を乏しくする。
- 検証はModel／Providerの設定だけに依存せず、Applicationの受け入れ境界で
  観測する。生成時の形式制約と受け入れ検証は併用できる。
- Schemaに合うScript文字列やURLでも、描画時のEncoding、外部通信、認可、
  Content Safety等は別の保証として評価する。

## Assets, actors, identities, and trust boundaries

保護対象は後続API／Toolの入力契約、保存Dataの完全性、Userへ公開する
出力の整合性。攻撃者はPromptや取得資料を通じて予想外のField・値・構造を
Modelに生成させ得る。Model自体も誤った形式を返し得る。
Trust Boundaryは、Modelの非信頼出力がApplicationに入り、そこから
User表示、Tool実行、保存、次Stepへ移る地点。受け入れ判断はModelの自己申告でなく
Application側に置く。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 利用する各Model出力経路に、下流の受け入れ条件を表す定義済みSchemaがある。 |
| SP-2 | Applicationが実際の出力を、その経路に適用するSchemaと照合する。Parse成功や生成時制約だけを代替としない。 |
| SP-3 | Schema不一致の出力は、公開・保存・実行・後続Stepへの利用前に拒否される。 |
| SP-4 | Retry、Fallback、Streaming等でも、利用された値と検証された値・Versionの対応を失わない。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| JSONをParseできるが必須Fieldがない／型や許可値が違う | Schema不一致なら拒否する。Parse成功だけではFail。 |
| ProviderのStructured Output機能で生成する | 有効な補助。Applicationの受け入れ検証と拒否を確認する。 |
| Schemaに適合するTextに悪意あるHTMLやURLが入る | 本Controlだけでは安全性を保証しない。描画・外向き通信・Content Safetyを別途評価する。 |
| Schema適合のTool引数で無権限Resourceを指定する | 認可はC5／C9等の別境界。Schema適合は許可の証拠ではない。 |
| 長さ上限で出力が途切れる | 終了・長さ制御はC7.1.2。不完全出力がSchema不一致なら本Controlでは拒否する。 |
| 全文検証前のStreaming断片をUserへ表示する | その断片を公開する時点の契約が未検証なら、後から拒否しても公開済み部分は戻せない。 |

## Threat and failure-mode rationale

Model出力を直接ParserやWorkflowへ渡すと、余分なField、欠損、型違い、
想定外のネストが処理を誤らせ得る。ResearchはInjectionやData Pipelineの
破損等を例に挙げるが、Schema検証だけでScript実行やSQL Injectionを
すべて防ぐという主張にはしない。重要なのは、非信頼出力を
Applicationの契約に照らし、合わないものを下流へ渡さないことである。
外部Threat IDへの厳密なMappingは未評価とする。

## Verification

### Architecture and configuration review

Model出力が届く全経路とSinkを列挙し、適用Schema、Validator、拒否時の挙動、
生成時の形式制約、再生成・Fallback、Streaming公開時点を追う。
Schemaが実際の下流Contractを表すか、許可しない追加Field等の扱いが
明示されているか確認する。Provider側の設定画面だけでPassとしない。

### Positive verification

定義された必須Field、型、許可値、正当な追加Field、境界長等に合う出力を
通し、正当な値が不当に拒否されないことを確認する。利用されたPayloadと
検証されたPayloadが同一であることを観測する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 必須Field欠損、型違い、許可外Enum、許可しない追加Fieldを生成する | 各経路のSchema不一致をApplicationが拒否し、下流へ渡さない。SP-1〜SP-3 |
| N-2 | JSONとしては読めるが、入れ子構造や配列要素が契約と違う出力を渡す | Parse成功にかかわらずSchemaで拒否する。SP-2, SP-3 |
| N-3 | Tool引数や保存Dataに余分な操作Fieldを含める | 下流Contractで禁止したFieldを拒否し、Tool／Storeへ送らない。SP-1〜SP-3 |
| N-4 | Validator失敗後に再生成・Fallbackで別の出力を得る | 新しい出力を改めて検証し、旧判定を流用しない。SP-2〜SP-4 |
| N-5 | Streamingの途中で不正なFieldや未完了構造を送る | 検証前に不可逆な公開・副作用を生じさせず、宣言した単位で拒否する。SP-3, SP-4 |
| N-6 | Schema適合の無権限Action、危険なURL、誤情報を生成する | 本Controlの形式判定と別の認可・出力安全・信頼性の検査を混同しない。SP-1, SP-2 |

### Failure conditions

利用する出力経路にSchemaがない、生成時の形式指定やJSON Parseだけで
受け入れる、Schema不一致をLogだけに残して下流へ渡す、または
検証済み値と利用値が異なる場合はFail。Schemaが形式上存在しても、
下流が解釈するField・型・構造をほぼ無制限に許すなら、契約の妥当性を
レビューする。Schemaに合った悪意ある内容は、本Control単独のFailではなく
別の保証として評価する。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 出力経路とSchema一覧 | Application Owner | User表示、Tool、Store、後続Step | 経路・Schema変更時 | 機密Payloadを含めずRevision保持 | 全利用経路のContractとValidatorを辿れる。 |
| SchemaとValidator設定 | Application／Policy Owner | Field、型、許可値、追加Field、Version | Schema変更時 | 変更履歴を保持 | 下流Contractに対応する条件と拒否動作が定義される。 |
| 回帰試験結果 | Test Harness | N-1〜N-6、Retry・Streamingを含む | Release・Model／Provider変更時 | 合成Dataと期待結果を保持 | 不一致が利用前に拒否され、正常出力が利用される。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C7.1.2` | 出力の長さ・終了制御。本Controlは利用値のSchema適合と不一致拒否を問う。 |
| `v1.0-C7.2.1`／`v1.0-C7.2.2` | 回答の信頼性評価と低Confidence時の処理。Schema適合は事実性を示さない。 |
| `v1.0-C7.3.1`〜`v1.0-C7.3.4` | 有害性、機密漏えい、外向きRequest、隠蔽の検査。形式だけでは扱えない。 |
| `v1.0-C9.5.1` | Toolと引数の認可。Schemaに合うActionでも権限を別途確認する。 |

## Known limitations and uncertainty

Schemaが緩すぎれば不正な意味内容を通す。厳しすぎれば正当な回答を
過剰に拒否する。自由記述Textで何をSchemaとして定義し得るかは
利用先のContractに依存し、形式検証だけで文意の安全性を担保できない。
Streamingは公開単位により検証時点が異なるため、経路ごとに説明が必要。
`verifiable`は本Artifactの成熟度であり、製品のSchema適合や安全性を保証しない。

## References

- [AISVS v1.0 C7 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md)
- [AISVS v1.0 C7.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-01-Output-Format-Enforcement.md)
- [C7 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-30 | C7.1.1初版。Schema不一致拒否と別保証の境界を定義 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
