# Controls Knowledge Base Incremental Plan

- Status: active
- Scope: `controls/` only
- Primary backbone: OWASP AISVS
- AISVS source state reviewed: 2026-09-03

### C2 checkpoint — 2026-09-28

C2の[保証範囲](control-records/c02-input-validation/README.md)とSection単位の開発順序を整理した。
学習資料とは独立に、C2.1の最初の[C2.1.1 Control](control-records/c02-input-validation/v1.0-c2.1.1-normalize-input-before-tokenization-or-embedding/README.md)を
正規要件と対応Researchから`verifiable`まで整備した。C2.1は残り7要件、C2.2は4要件が未整備。
次はC2.1.2から、各要件の独立した保証境界とNegative Testを確認して進める。
学習済みのC7・C12もControlとしては未着手であり、C2のSection横断確認後に優先順位を判断する。

2026-09-29：続く[C2.1.2 Control](control-records/c02-input-validation/v1.0-c2.1.2-detect-and-mitigate-encoded-input-smuggling/README.md)も
`verifiable`まで整備した。C2.1の残りは6要件。次はC2.1.3で「入力経路の検査」と
「検知時の遮断」を分けて確認する。C2.1全体は未完了であり、
Catalog・Control本文・Family案内の整合を確認しながら進める。

同日：続けて[C2.1.3 Control](control-records/c02-input-validation/v1.0-c2.1.3-screen-and-block-model-steering-inputs/README.md)を
`verifiable`まで整備した。全入力経路の検査とFlag時の遮断を独立に試験する。
C2.1の残りは5要件。次はC2.1.4でContext上限と黙った切詰めの境界を扱う。

同日：[C2.1.4 Control](control-records/c02-input-validation/v1.0-c2.1.4-reject-over-limit-input-without-truncation/README.md)を
`verifiable`まで整備した。上限超過の拒否を最終Payload・Model切替・SDKの
切詰め挙動まで追い、事前の資料選択と区別した。C2.1の残りは4要件。
次はC2.1.5の文字集合Allowlistを、対応言語を不当に壊さない保証と併せて扱う。

同日：[C2.1.5 Control](control-records/c02-input-validation/v1.0-c2.1.5-allowlist-required-input-characters/README.md)を
`verifiable`まで整備した。Field・用途・対応言語別のAllowlistと、許可外文字の拒否／必要文字の受入れを
対にして検証可能にした。C2.1の残りは3要件。次はC2.1.6の指示階層を、Model内の優先順位と
Application側の決定論的な権限境界を混同せずに扱う。

同日：[C2.1.6 Control](control-records/c02-input-validation/v1.0-c2.1.6-preserve-instruction-hierarchy-across-steps/README.md)を
`verifiable`まで整備した。上位Roleを保つ構造と、User・Tool・RAG・Memoryを経た後続Stepでの
実効的な指示優先を分けて検証する。認可Decisionは別保証とした。C2.1の残りは2要件。
次はC2.1.7の予約特殊TokenがLiteralとして扱われる境界を確認する。

同日：[C2.1.7 Control](control-records/c02-input-validation/v1.0-c2.1.7-render-reserved-tokens-as-literal-content/README.md)を
`verifiable`まで整備した。非信頼Text中の予約表現が実際のRole／Turn境界に変わらないことを
Model・Tokenizer・Template・入力経路ごとに確認する。C2.1の残りはC2.1.8の1要件。
次はMany-shot検出をContext上限や単なる連続投稿制限と区別して扱う。

同日：[C2.1.8 Control](control-records/c02-input-validation/v1.0-c2.1.8-detect-many-shot-jailbreak-patterns/README.md)を
`verifiable`まで整備した。Many-shot検知をContext上限、投稿回数、Modelの拒否応答と区別し、
正常なFew-shotとの誤判定も試験対象にした。C2.1全8要件の初期成熟化が揃った。
次はSection横断で保証境界とCatalogの整合を確認し、その後C2.2の着手を判断する。

同日：C2.1全8件を横断確認し、Catalog・Level・Linkの整合を確認した。
C2.1.7では事前拒否をLiteral EncodingのPass証拠としないよう検証条件を修正した。
C2.1の初期Sectionレビューを終え、次はC2.2の保証範囲を確認する。

同日：C2.2の最初の[C2.2.1 Control](control-records/c02-input-validation/v1.0-c2.2.1-screen-prompts-before-model-context/README.md)を
`verifiable`まで整備した。四つの内容区分と設定可能な閾値による分類に加え、
閾値超過時のModel投入前拒否／無害化を独立して検証する。C2.2の残り3要件は未整備。
次はC2.2.2で非対応言語における分類の評価を扱う。

2026-09-30：[C2.2.2 Control](control-records/c02-input-validation/v1.0-c2.2.2-evaluate-content-classification-for-unsupported-languages/README.md)を
`verifiable`まで整備した。非対応・不明・混在言語での分類評価を、全言語対応や
一律拒否の義務と混同しない。C2.2の残りはC2.2.3・C2.2.4の2要件。
次は非テキスト入力の検査境界を扱う。

同日：[C2.2.3 Control](control-records/c02-input-validation/v1.0-c2.2.3-check-non-text-inputs-for-hidden-attacks/README.md)を
`verifiable`まで整備した。画像・動画・音声の隠蔽／攪乱を、元Fileだけでなく
Modelが消費する変換後表現との関係で検証する。OCRや文字起こしを全成分の
安全性証明としない。C2.2の残りはC2.2.4の1要件。次は複数形式の連携攻撃を扱う。

同日：[C2.2.4 Control](control-records/c02-input-validation/v1.0-c2.2.4-detect-and-block-cross-modal-attacks/README.md)を
`verifiable`まで整備した。個別形式では無害でも、合成後に攻撃となるCaseを検出し、
Logのみではなく下流への伝播を遮断することを試験する。これでC2.2の4要件が揃った。
次はSection横断で隣接要件の保証境界、Catalog・Level・Linkを確認する。

同日：C2.2の4件を横断確認し、内容分類、非対応言語での評価、非テキストの検査、
複合形式攻撃の検出・遮断という保証境界を[Family概要](control-records/c02-input-validation/README.md)に整理した。
固定版のLevel、Catalog、Control参照を照合した。C2全2 Section・12要件の初期成熟化が揃った。
これはControl Artifactの到達点であり、実製品の適合やすべての入力攻撃の防止を意味しない。
次はC7・C12等の未整備Familyを、保証上の必要性と学習資料の蓄積に照らして選ぶ。

### C7 checkpoint — 2026-09-30

C2入力境界の初期成熟化に続き、Model出力を受け入れる境界を先に扱うためC7を選んだ。
[Family概要](control-records/c07-model-behavior-output-control-and-safety-assurance/README.md)で
全4 Section・13要件の保証上の問いを整理した。これは未作成ControlのPlaceholderではない。
最初の[C7.1.1 Control](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.1.1-validate-and-reject-model-outputs-by-schema/README.md)を
正規要件と対応Researchから`verifiable`まで整備した。全Model出力のSchema適合と
不一致拒否を、内容安全性・事実性・認可・長さ／終了制御から分けて確認する。
残る12要件は未整備。次は同SectionのC7.1.2で長さと終了状態の保証を扱う。

同日：[C7.1.2 Control](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.1.2-bound-model-output-length-and-termination/README.md)を
`verifiable`まで整備した。出力上限が実際に働くことと、正常完了・上限到達・中断を
区別して未完了出力を安全に扱うことを分けて検証する。C7.1の2要件が揃ったため、
次はSection横断でSchema検証との境界とCatalog・Level・Linkを確認する。

同日：C7.1の2件を横断確認し、Schemaによる受け入れ判定と出力Bound・終了判定の
違いを[Family概要](control-records/c07-model-behavior-output-control-and-safety-assurance/README.md)に明記した。
固定版のLevel、Catalog、Control参照を照合し、C7.1の初期Sectionレビューを終えた。
次はC7.2の保証範囲を確認し、信頼性評価と低Confidence時の処理を分けて着手する。

同日：[C7.2.1 Control](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.2.1-estimate-generated-answer-reliability/README.md)を
`verifiable`まで整備した。Confidenceの有無ではなく、回答の信頼性という対象、
代表的な正誤との関係、誤った高Confidenceの限界を評価する。
低Confidence時の自動遮断・FallbackはC7.2.2、高Impact回答の追加検証はC7.2.3として分けた。
次はC7.2.2でScoreを実際の公開判定へ結び付ける。

2026-10-01：[C7.2.2 Control](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.2.2-block-or-fallback-below-confidence-threshold/README.md)を
`verifiable`まで整備した。定義済み閾値未満の回答が、Warningのみで公開・利用されず、
自動で遮断または元回答を含まないFallbackへ切り替わることを試験する。
Scoreの校正はC7.2.1、高Impact回答の追加検証はC7.2.3に分ける。
次はC7.2.3でConfidenceと誤答時のImpactを別軸として扱う。

同日：[C7.2.3 Control](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.2.3-additional-verification-for-high-risk-responses/README.md)を
`verifiable`まで整備した。Policy上のHigh-risk回答はConfidenceにかかわらず、
具体的な主張・操作内容を対象にした追加検証を通す。検証方式を一律に固定せず、
人間の承認や別Modelの同意だけで適合としない。C7.2の3要件が揃ったため、
次はSection横断で保証境界とCatalog・Level・Linkを確認する。

同日：C7.2の3件を横断確認し、Confidence推定、閾値未満の自動Gate、
高Impact回答の追加検証を[Family概要](control-records/c07-model-behavior-output-control-and-safety-assurance/README.md)で分離した。
固定版のLevel、Catalog、Control参照を照合し、C7.2の初期Sectionレビューを終えた。
次はC7.3の出力安全性を、内容分類・内部情報・外向きRequest・隠蔽の別保証として扱う。

同日：[C7.3.1 Control](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.3.1-classify-and-block-harmful-responses/README.md)を
`verifiable`まで整備した。全Responseの有害内容分類と、該当時の公開・利用遮断を
接続して検証する。入力分類のC2.2.1、内部情報漏えいのC7.3.2、外向きRequestの
C7.3.3とは保証を分ける。次はC7.3.2の出力側の内部情報漏えい防止を扱う。

2026-10-02：[C7.3.2 Control](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.3.2-block-system-prompt-and-backend-data-disclosure/README.md)を
`verifiable`まで整備した。System PromptとBackend Dataの意図しない出力開示を
検知・遮断する一方、正当に許可されたBackend Dataの利用は一律に拒否しない。
受取権限の決定・取得認可はC5側の独立した保証とし、Filterだけで代替しない。
次はC7.3.3のModel出力を契機とする外向きRequestを扱う。

同日：[C7.3.3 Control](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.3.3-prevent-output-triggered-outbound-requests/README.md)を
`verifiable`まで整備した。URL文字列の表示と、出力だけを契機とする通信を分け、
Browser・Server・Toolでの外向きRequestを観測して検証する。明示操作や
独立したPolicy判断に基づく正当な通信は一律禁止としない。
次はC7.3.4の隠れた・符号化された・誤認を誘う内容の検査を扱う。

同日：[C7.3.4 Control](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.3.4-check-hidden-encoded-and-misleading-outputs/README.md)を
`verifiable`まで整備した。Raw・表示・下流解釈の差をSink別に検査し、
正当な多言語表現の一律削除を要件化しない。C7.3.1〜C7.3.4を横断確認し、
分類／開示／通信／隠蔽の四つを別保証として[Family概要](control-records/c07-model-behavior-output-control-and-safety-assurance/README.md)に整理した。
これでC7.3の初期Sectionレビューを終えた。次はC7.4の出典・引用の保証へ進む。

2026-10-03：[C7.4.1 Control](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.4.1-attribute-rag-responses-to-source-documents/README.md)を
`verifiable`まで整備した。RAG回答に識別可能な参照元文書を示すことと、
出典の生成主体（C7.4.2）、主張とChunkの支持関係（C7.4.3）を分ける。
次はC7.4.2でRetrieval Metadataからの出典構成を扱う。

同日：[C7.4.2 Control](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.4.2-derive-rag-attributions-from-retrieval-metadata/README.md)を
`verifiable`まで整備した。Citationの正本を今回のRetrieval Metadataへ結び付け、
Model生成Textによる出典の追加・上書きを許さない。Metadata自体の汚染、
出典の表示、主張の支持は別の保証として残す。次はC7.4.3のClaimと
取得Chunkの対応を扱う。

同日：[C7.4.3 Control](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.4.3-trace-rag-claims-to-retrieved-chunks/README.md)を
`verifiable`まで整備した。主張から今回取得したChunkの版・該当箇所へ辿れる
ことと、その箇所が主体・数値・条件を支えるかの評価を分ける。NLI等の特定方式は
必須化せず、明白な矛盾・誤主体・旧版の引用をNegative Testへ落とした。
次はC7.4.4の生成MediaのWatermarkを扱う。

同日：[C7.4.4 Control](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.4.4-watermark-ai-generated-media/README.md)を
`verifiable`まで整備した。生成時の付与と最終配布物での検出を分け、
通常の変換で失われる経路を試験する。Watermarkは特定の発行者、非改変、
事実性を一律に証明しない。ResearchのC2PA併用例や法令解説を規範条件へ
昇格させず、Textを含むMediaの範囲は用途ごとの判断として残した。
C7.4の4要件が揃ったので、次はSectionとFamily全体の境界・Level・Linkを
横断確認する。

同日：C7.4の4件を横断確認した。C7.4.1〜C7.4.3はRAG回答の出典表示・
出典の生成主体・主張と取得Chunkの対応という別保証であり、C7.4.4は生成Mediaの
AI生成標識という独立した枝である。[Family概要](control-records/c07-model-behavior-output-control-and-safety-assurance/README.md)、
Catalog、ControlのLevel・参照先を照合し、C7の全13 Requirementの初期整備を
`verifiable`で完了した。これはRepository Artifactの成熟度であって、実製品の
適合や全ての誤出力の検出を保証しない。次の優先Familyは別途計画から選ぶ。

### C12 checkpoint — 2026-10-03

C2・C7の入力／出力境界に続き、その処理を運用中に観測・調査できるかを扱う
C12を選んだ。全5 Section・21 Requirementの学習資料は既にあるが、Controlの
成熟とは独立する。[Family概要](control-records/c12-monitoring-logging-and-anomaly-detection/README.md)へ
各SectionとRequirementの保証上の問いを整理した。初回はC12.1の
[C12.1.1 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.1.1-log-ai-interactions-with-session-context/README.md)を
正規要件と対応Researchから`verifiable`まで整備した。Session／実行Contextと
AI固有Telemetryの結合を直接の保証とし、Policy判断の詳細（C12.1.2）、
推論Schema（C12.1.3）、RAG検索の記録（C12.1.4）を混ぜない。
次はC12.1.2のSafety／Policy判断の監査可能な記録を扱う。

同日：[C12.1.2 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.1.2-log-safety-filter-and-policy-decisions/README.md)を
`verifiable`まで整備した。Safety／ModerationのAllow・Block・Redact・Error等を
対象処理、Policy、Stage、判断と実際の扱いへ結び付ける。記録の存在を
遮断の有効性と混同せず、Researchの特定SchemaやScoreを一律必須としない。
次はC12.1.3の推論Event Schemaと最低Fieldを扱う。

同日：[C12.1.3 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.1.3-structured-interoperable-inference-event-logs/README.md)を
`verifiable`まで整備した。Model ID、入出力別Token数、Provider、Operationを
構造化・比較可能なFieldとして記録し、ダミー値やProvider間の意味のずれを
Negative Testで検出する。OTel固有属性、実Serving Modelの二重Field、
Content既定除外はResearchの補足であり一律のNormative条件にしない。
次はC12.1.4のRAG Retrieval Eventを扱う。

2026-10-04：[C12.1.4 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.1.4-log-rag-retrieval-queries-documents-and-sources/README.md)を
`verifiable`まで整備した。実際にRetrieverへ渡したQuery、取得文書、
Knowledge Sourceを同じEventで辿れるようにする。Queryの復元不能なHashだけ、
件数だけのLog、複数Sourceや旧版文書の取り違えをNegative Testへ落とした。
全文の運用Log複製は必須化せず、保護された別Storeへ置く場合は参照整合性を
試験する。C12.1の4要件が揃ったので、次はSection横断で境界・Level・Linkを
確認する。

同日：C12.1の4件を横断確認した。Session相関（C12.1.1）、Safety／Policy
判断の詳細（C12.1.2）、推論Eventの共通Field（C12.1.3）、Retrievalの
Query・文書・Source（C12.1.4）は、同じ処理を観測する別の保証である。
[Family概要](control-records/c12-monitoring-logging-and-anomaly-detection/README.md)、
Catalog、ControlのLevel・参照先を照合し、C12.1の初期Sectionレビューを
終えた。Logの存在は遮断・認可・検知の有効性を示さず、Contentの過剰収集も
正当化しない。次はC12.2の検知・Alertを、記録から独立した保証として扱う。

同日：[C12.2.1 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.2.1-detect-and-alert-on-known-adversarial-inputs/README.md)を
`verifiable`まで整備した。既知の攻撃的な入力を見つけ、調査につながる通知を
出せるかを試す。入力の記録だけ、遮断だけでは合格としない。利用者の質問に
加え、AIが読む外部文書やToolの返答も、実際にある経路について確認する。
未知の攻撃を必ず見つけるとは主張しない。次はC12.2.2で、会話の流れや
繰り返しから異常を見つける保証を扱う。

同日：[C12.2.2 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.2.2-detect-unusual-conversation-and-probing-behavior/README.md)を
`verifiable`まで整備した。一件ごとの危険な文面ではなく、会話の変化、拒否後の
再試行、少しずつ条件を変える探り行動を見つけられるかを試す。回数が多い
だけの正規利用を攻撃と決め付けず、誤判定も確認する。通知を要件本文の
必須条件へ付け加えず、C12.2.1の通知と区別する。次はC12.2.3で、協調した
攻撃などに合わせた個別の検知ルールを扱う。

同日：[C12.2.3 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.2.3-detect-ai-specific-attacks-with-custom-rules/README.md)を
`verifiable`まで整備した。協調した脱獄、不正な指示の混入、内部指示の引き出しを
対象システム向けのルールで見つけられるか、合成した試行で確かめる。
単発の既知文面の検知（C12.2.1）や一人の行動異常（C12.2.2）だけでは
置き換えない。次はC12.2.4で、抽出に関する通知から問題の質問を調べられるかを扱う。

同日：[C12.2.4 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.2.4-include-offending-query-metadata-in-extraction-alerts/README.md)を
`verifiable`まで整備した。抽出の疑いを知らせる通知から問題の質問へ辿れるかを
合成データで試す。通知名と総利用量だけでは足りない。質問本文の通知への
直接添付や特定の項目名は必須にせず、別の保管先を使うなら参照が解決できる
ことを確認する。次はC12.2.5で、AIの利用量を利用者・会話・機能・組織に
正しく帰属させられるかを扱う。

同日：[C12.2.5 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.2.5-attribute-token-usage-by-user-session-feature-and-team/README.md)を
`verifiable`まで整備した。AIのトークン使用量が利用者・会話・機能・チーム
または作業領域へ正しく結び付くかを、二つの組織にまたがる合成試験で確かめる。
費用の急増を知らせる通知や予算上限は有用だが、この要件の必須条件には
しない。次はC12.2.6で、AI APIを隠れた通信路として悪用する兆候の監視を扱う。

同日：[C12.2.6 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.2.6-monitor-llm-api-traffic-for-covert-c2-activity/README.md)を
`verifiable`まで整備した。管理対象からLLM APIへの経路を確認し、正規の
AI利用に紛れた指令・情報の受け渡しを疑う信号が実際に評価されるかを、
無害な模擬通信で試す。暗号化通信の全文取得や自動遮断は必須としない。
C12.2の6要件が揃ったので、次はSection全体の保証境界、Level、Catalog、
Linkを横断確認する。

同日：C12.2の6件を横断確認した。既知の攻撃的な入力と通知（C12.2.1）、
会話を通した不自然な行動（C12.2.2）、AI特有の攻撃を狙う個別ルール
（C12.2.3）、抽出通知から質問への追跡（C12.2.4）、使用量の四つの
帰属先（C12.2.5）、AI APIを使う隠れた通信の兆候（C12.2.6）は別の
保証である。Levelは順に1・2・2・2・2・3で、Catalogと本文が一致し、
Family一覧とSection学習資料から各Controlへ辿れる。これでC12.2の
初期Sectionレビューを終えた。次はC12.3.1の入力データの変化の監視へ進む。

同日：[C12.3.1 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.3.1-monitor-input-distribution-drift-by-data-type/README.md)を
`verifiable`まで整備した。入力件数が同じでも内容の構成が変わる試験を使い、
データの種類に合う方法で変化を見つけられるか確認する。分布の変化を
攻撃や回答品質低下の証拠とは決め付けない。次はC12.3.2で、個々の
出力の事実誤認・矛盾・捏造を識別できるかを扱う。

同日：[C12.3.2 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.3.2-identify-and-flag-factually-wrong-contradictory-or-fabricated-outputs/README.md)を
`verifiable`まで整備した。既知の誤答・矛盾・架空の情報に印を付けられるか、
正答を一律に疑わないかを合成データで確かめる。検知器の判定は真実の証明
ではなく、回答の自動遮断や印の割合の時系列監視とも分ける。次は
C12.3.3で、印が付いた割合を継続して追えるかを扱う。

同日：[C12.3.3 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.3.3-track-hallucination-rate-over-time/README.md)を
`verifiable`まで整備した。印が付いた件数を検査済み回答数で割り、
同じ条件で複数期間を比べられるかを試す。検知器や抽出対象が変わっただけの
見かけの上昇と、実際の継続的な変化を混同しない。次はC12.3.4で、
説明できない変化と想定内の運用変化を分ける。

同日：[C12.3.4 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.3.4-distinguish-unexplained-behavior-from-expected-drift/README.md)を
`verifiable`まで整備した。変更の時期が一致するだけでは想定内とせず、
変化の範囲・方向・大きさまで説明できるかを合成例で確かめる。根拠が
足りなければ未解決として残す。C12.3の4要件が揃ったので、Section全体の
保証境界、Level、Catalog、Linkを横断確認する。

同日：C12.3の4件を横断確認した。入力分布の変化（C12.3.1）、個々の
誤情報を含む回答のFlag（C12.3.2）、その割合の時系列（C12.3.3）、
想定内と説明不能な変化の区別（C12.3.4）は別の保証である。Levelは順に
1・2・2・3で、Catalogと本文が一致し、Family一覧とSection学習資料から
各Controlへ辿れる。これでC12.3の初期Sectionレビューを終えた。次は
C12.4.1で、自律的な行動を始める際のSecurity評価を扱う。

同日：[C12.4.1 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.4.1-evaluate-autonomous-action-triggers/README.md)を
`verifiable`まで整備した。正規のScheduleやEventでも起動前に、行動の
流れ、安全性、関係する脅威状況の三観点が評価されるかを、模擬した
起動経路で確かめる。ResearchにあるGateway方式や外部Threat Feedを
一律の必須条件にはせず、実行時の承認Gateとも分けた。次はC12.4.2で、
重要な自律操作と承認判断の監査記録を扱う。

同日：[C12.4.2 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.4.2-audit-security-critical-proactive-actions/README.md)を
`verifiable`まで整備した。模擬送金の承認・拒否・Timeout・実行失敗を使い、
承認者、時刻、対象引数、判断結果と実行結果を同じ操作へ辿れるか確かめる。
「送金なし」だけでは拒否・未提案・失敗を区別できない。記録の保証と
実行時の承認Gateは別に評価する。次はC12.4.3で、緊急停止とOverride
指示の記録を扱う。

同日：[C12.4.3 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.4.3-log-kill-switch-activations-and-override-commands/README.md)を
`verifiable`まで整備した。模擬Agentの手動停止、自動停止、再開Overrideで、
発動と指示を管理画面の操作や実際の停止完了から区別して記録できるかを
確かめる。C12.4の3要件が揃ったので、Section全体の保証境界、Level、
Catalog、Linkを横断確認する。

同日：C12.4の3件を横断確認した。自律的な行動の起動時に三つの観点を
評価する（C12.4.1）、重要操作と承認判断を監査する（C12.4.2）、
停止発動とOverride指示を記録する（C12.4.3）は別の保証である。
Levelはいずれも2で、Catalogと本文が一致し、Family一覧とSection学習資料
から各Controlへ辿れる。記録があっても実行時の承認Gateや実停止を
保証しない。これでC12.4の初期Sectionレビューを終えた。次はC12.5.1で、
Datasetと構成要素の来歴を扱う。

同日：[C12.5.1 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.5.1-record-complete-dataset-lineage/README.md)を
`verifiable`まで整備した。二つの元Datasetを変換・増強・結合した合成例で、
構成要素と中間成果物の各版を辿り、Notebookによる未記録の加工も見つける。
来歴を内容の安全性やModel変更監査と混同しない。次はC12.5.2で、
Label付け活動の記録を扱う。

同日：[C12.5.2 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.5.2-log-all-labeling-activities/README.md)を
`verifiable`まで整備した。ラベルの最終値だけでなく、初回付与・付け直し・
削除や、自動処理・まとめて取り込む経路の活動を合成Dataで辿る。
ラベルの正しさやModel変更記録の変更不能性とは分けて評価する。
次はC12.5.3で、Model変更の監査記録を扱う。

同日：[C12.5.3 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.5.3-immutable-audit-records-for-model-changes/README.md)を
`verifiable`まで整備した。Model Artifactや配備先・Alias・管理対象の設定を
変える経路を洗い出し、変更前後の実体と監査記録を結び付ける。記録の欠落と、
変更者が過去の記録を消せる状態を別々に試す。次はC12.5.4で、取込文書の
書込み時Tagを扱う。

同日：[C12.5.4 Control](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.5.4-tag-ingested-documents-at-write-time/README.md)を
`verifiable`まで整備した。文書を書き込む時にSource・Writer Identity・
Timestampを付けることを、Uploadと同期Connectorの合成例で確かめる。
利用者の自己申告と信頼できる書込みContextを分け、Tagの存在だけで
本文の安全性や検索認可まで保証しない。

同日：C12.5の4件を横断確認した。Datasetと加工の来歴（C12.5.1）、
ラベル付け活動の記録（C12.5.2）、変更不能なModel変更監査（C12.5.3）、
取込文書への書込み時Tag（C12.5.4）は、同じ来歴の話でも対象と保証が異なる。
Levelは順に1・1・2・2で、Catalogと本文が一致し、Family一覧とSection
学習資料から各Controlへ辿れる。来歴だけで内容の安全性、変更の承認、
検索認可は保証しない。C12全21件の初期Control整備を終えた。

### C11 checkpoint — 2026-10-04

C2・C7・C12の初期整備後、入力や出力の境界だけでは説明しきれない
Modelの安全性訓練、敵対的な操作への耐性、Privacy推測、Model抽出への
保証を扱うためC11を選んだ。[C11 Family概要](control-records/c11-adversarial-robustness/README.md)に
4 Section・17 Requirementの問いと失敗状態を整理した。これは全要件の
Control本文や学習資料を一括作成したことを意味しない。

最初の[C11.1.1 Control](control-records/c11-adversarial-robustness/v1.0-c11.1.1-model-alignment-and-safety-training/README.md)を
`verifiable`まで整備した。利用するModel Versionが禁止出力カテゴリを
対象とする訓練・調整を受けた根拠と、代表的な合成質問での振る舞いを
分けて確かめる。Promptや出力FilterだけをModel訓練の証拠にはしない。

### C11 checkpoint — 2026-10-05

[C11.1.2 Control](control-records/c11-adversarial-robustness/v1.0-c11.1.2-run-versioned-alignment-suite-on-model-updates/README.md)を
`verifiable`まで整備した。試験Suiteの版管理と、Model更新・Releaseの
たびの実行記録を独立に確かめる。実行した事実、試験結果の良否、Release
判断を混同しない。

[C11.1.3 Control](control-records/c11-adversarial-robustness/v1.0-c11.1.3-evaluate-modality-relevant-adversarial-attacks/README.md)を
`verifiable`まで整備した。製品で有効な形式・変換経路と既知の攻撃手法を
対応させ、前処理での拒否とModelの応答を区別して評価する。結果が悪くても
評価を行った事実と、耐性の不足・修正判断は混同しない。

[C11.1.4 Control](control-records/c11-adversarial-robustness/v1.0-c11.1.4-harden-model-against-adversarial-inputs/README.md)を
`verifiable`まで整備した。対策の存在、実際の推論経路への適用、敵対的な
試験での効果を分けて確かめる。Model自身の強化と外付けの安全層も混同しない。
続いて[C11.1.5 Control](control-records/c11-adversarial-robustness/v1.0-c11.1.5-measure-harmful-content-rate-and-flag-regressions/README.md)を
`verifiable`まで整備した。自動評価器による割合の測定、比較条件、定義した
しきい値を超える悪化の印を別々に確認する。印が付くことと、Release停止や
弱点の修正も混同しない。これでC11.1の5要件の初期Control本文が揃った。

C11.1を横断確認した。訓練の根拠（C11.1.1）、更新ごとの試験実行
（C11.1.2）、形式に合った攻撃評価（C11.1.3）、強化策の効果
（C11.1.4）、有害出力率の悪化検知（C11.1.5）は別の保証である。
Levelは順に1・1・1・2・3で、Catalogと本文が一致し、Family一覧から
各Controlへ辿れる。Controlの初期整備は学習完了を意味しない。

### C5 implementation checkpoint — 2026-09-08

C5全11 RequirementのControlを`verifiable`まで整備した。Phase 1〜3の成果物と
Exit criteriaを満たし、一覧は[README](README.md)、正規Metadataは[catalog](catalog.yaml)を参照する。
各Controlは適用境界、脅威、Positive/Negative Verification、Evidence、限界を持つ。
学習の一巡とは独立したArtifactの完成であり、実製品への適合や全攻撃への完全保証を意味しない。

残る作業は、利用・レビューからの改善と、必要な場合の独立したEngineering Mapping評価である。
Mapping不在を埋めるためにPatternを生成しない。次Familyの候補はPhase 4のC9/C10/C8だが、
このC5作業では着手しない。以下のPhase記述は開発順序と判断根拠として保持する。

### C9 landscape checkpoint — 2026-09-09

Phase 4の次FamilyとしてC9を選び、[Family概要](control-records/c09-orchestration-and-agentic-security/README.md)へ保証範囲を集約した。
採用済みv1.0の固定Revisionで要件本文と対応Researchを確認し、最初の代表要件を
`v1.0-C9.5.1`（Level 2：ツールと引数の細粒度認可）とした。
全体分析に続き、[C9.5.1のControl](control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.1-fine-grained-tool-and-parameter-authorization/README.md)を
解釈・脅威・検証・証拠・限界まで整備し、Catalogに`verifiable`で追加した。
続いてC9全34件を同じ成熟度まで整備した。要件別の適用境界、脅威、正常・拒否試験、
証拠期待値、限界を持つ。全件のID・Levelは固定Sourceと照合し、
一覧は[README](README.md#c9-control-records)、正規Metadataは[Catalog](catalog.yaml)を参照する。
Phase 4のC9作業は完了。残るのは利用・レビューからの改善と必要時の独立したMapping評価。
C10/C8にはこの作業で着手しない。学習進捗とEngineering Mappingは変更しない。

### C10 landscape checkpoint — 2026-09-10

C9完了後、Phase 4の次FamilyとしてC10を選び、
[Family概要](control-records/c10-model-context-protocol-security/README.md)へ保証範囲を集約した。
採用済み固定Revisionの要件本文と対応Researchから、全4節・23件の保証範囲を整理した。
最初の代表要件は`v1.0-C10.2.7`（Level 2：受信Tokenの下流APIへの転送禁止）。
2026-09-23にこの一件を既存Templateで`verifiable`まで整備し、Catalogへ追加した。
Client Tokenの非転送と委任Contextの維持を分け、Credential取得失敗時のFallback、
Proxy・Retry・任意送信先を含むEgress試験と証拠期待値を定義した。この時点のCatalogは46件。
2026-09-24にControl成熟化の作業単位をSectionへ変更し、C10.1の3要件をすべて
`verifiable`まで整備した。Control ArtifactとCatalog行はRequirement単位を維持する。
続いてC10.2の残る6要件も成熟させ、同Sectionの全7要件を`verifiable`とした。
さらにC10.3 Secure Transportの全5要件を成熟させ、Remote／Local Transport、Origin／Host、
Version Downgrade、Sender-constrained Tokenの保証境界を分離した。続いてC10.4の全8要件を成熟させ、
Schema／Content、Parameter／Payload、署名／Replay、Consent／Definition再承認を分離した。
C10全23要件が`verifiable`となり、Catalogは68件。C10の章整合確認をもって同Familyの初期成熟化を完了した。

### C8 landscape checkpoint — 2026-09-24

Phase 4の残るFamilyとしてC8を選び、[Family概要](control-records/c08-memory-embeddings-and-vector-database-security/README.md)へ保証範囲を集約した。
採用済み固定Revisionの要件本文と3つのSection Researchから、全3節・11件の保証範囲を整理した。
最初のSectionはC8.1 Access Controls on Memory & RAG Indicesである。Vector ID／NamespaceのTenant一意性、
Security／Provenance Metadata Tagの不変性、全Retrieval PathでのScope強制という3要件を`verifiable`まで整備した。
続いてC8.2 Embedding Sanitization & Validationの5要件を`verifiable`まで整備した。Sensitive Field、Vector異常、
Trusted MemoryへのSource検証、Retrieval操作Content、Memory間の矛盾を、それぞれ独立して検証可能な保証へ翻訳した。
C8.3 Memory Expiry & Revocationの3要件も`verifiable`まで整備した。Logical ExclusionとPhysical Deletionを分け、
Resetは宣言したMemory Scopeの再利用停止、QuarantineはForensic保持とProduction Retrieval除外の両立として定義した。
C8全3 Section・11要件の初期成熟化を完了し、Catalogは79件となった。次はC8章内の整合確認と、未着手Familyの優先順位見直しを行う。

## 1. Purpose and boundaries

`controls/` is the requirement-oriented entry point for AI product-security assurance. It answers what security property must be assured, why it matters, how it can be verified, and what evidence would demonstrate effective implementation.

The domain should provide:

- version-aware references to authoritative requirements;
- repository-authored interpretations and security objectives;
- threat rationale and applicability boundaries;
- testable security properties;
- verification approaches and evidence expectations;
- explicit threat rationale and optional references to separately maintained
  engineering-pattern mapping assessments;
- historical traceability when an upstream identifier or requirement changes.

The domain should not become:

- a fork or wholesale copy of AISVS or another standard;
- a framework-coverage dashboard optimized for percentage complete;
- an implementation-code library;
- a duplicate of `engineering/`;
- a place where risk lists, adversary techniques, and verification requirements are treated as equivalent;
- a repository for production evidence, secrets, customer data, or organization-confidential identifiers.

Controls and engineering patterns are independent bodies of knowledge. A control defines an assurance expectation; an engineering pattern describes a practical way to design, implement, test, and operate a system. Either may exist before the other, and mappings must not force a one-to-one relationship.

## 2. Current framework landscape

The source state below was checked against `sources/registry.yaml` and the linked primary sources on 2026-09-01.

| Source | State used by this repository | Role in `controls/` | Treatment |
|---|---|---|---|
| OWASP AISVS | `v1.0`, stable; `1.01-dev` is in development | Primary verification/control backbone | Build the catalog and mature controls against stable `v1.0`; monitor but do not silently adopt `1.01-dev` |
| MITRE ATLAS | rolling | Adversary behavior and TTP taxonomy | Use for justified threat links; never treat technique coverage as control completion |
| OWASP GenAI LLM Top 10 | 2026, stable | LLM application risk taxonomy | Use as risk context and mapping evidence, not as control structure |
| OWASP Top 10 for Agentic Applications | 2026, stable | Agentic application risk taxonomy | Use as agentic risk context, particularly for action and delegation controls |
| OWASP MCP Top 10 | beta; published identifiers are labeled 2025 | MCP-specific risk taxonomy | Treat mappings as provisional and status-aware; do not present it as a stable verification standard |
| OWASP Agentic Skills Top 10 | v1 draft/public review | Agent-skill and behavior-layer risk taxonomy | Use as provisional context only; re-review mappings when status changes |
| OWASP AI Exchange | rolling | Supplementary security/privacy knowledge | Use for research and context, not as a normative control backbone |

AISVS states that `v1.0` is its latest stable release, with a locked stable directory and ongoing work in `1.01-dev`. It defines 191 requirements across 12 chapters and assigns verification levels 1–3. Stable, development, beta, public-review, and rolling sources must remain distinguishable in every derived record.

AISVS Appendix B is a useful non-normative, developer-facing reorganization of the requirements. It may inform analysis, but AISVS explicitly identifies chapters C1–C12 as the normative source of truth. The repository should therefore derive requirement identity and meaning from the chapters, not from the appendix alone.

## 3. AISVS v1.0 family inventory

This is a landscape inventory, not an attempt to restate every requirement.

| Family | AISVS chapter | Planning focus for this repository |
|---|---|---|
| C1 | Training Data Integrity & Traceability | Dataset provenance, authorized change, labeling integrity, and traceability |
| C2 | Input Validation | Canonicalization, injection-aware handling, schema and length constraints, and input trust boundaries |
| C3 | Model Lifecycle Management & Change Control | Artifact identity, signing, evaluation gates, promotion, rollback, and change governance |
| C4 | Infrastructure, Configuration & Deployment Security | Serving infrastructure, deployment configuration, isolation, edge deployment, and protected model assets |
| C5 | Access Control & Identity for AI Components & Users | Authentication, AI resource authorization, policy boundaries, delegation context, and tenant isolation |
| C6 | Supply Chain Security for Models | Model and artifact provenance, dependency integrity, acquisition, and supplier trust |
| C7 | Model Behavior, Output Control & Safety Assurance | Output constraints, behavior evaluation, unsafe output handling, and safety assurance |
| C8 | Memory, Embeddings & Vector Database Security | Memory integrity, retrieval authorization, embedding/vector isolation, retention, and poisoning resistance |
| C9 | Orchestration & Agentic Security | Execution budgets, approvals, tool isolation, agent identity, authorization, delegation, and shutdown |
| C10 | Model Context Protocol (MCP) Security | MCP authentication, authorization, token handling, tool/resource integrity, and protocol auditability |
| C11 | Adversarial Robustness | Evaluation against adversarial manipulation, robustness boundaries, and failure handling |
| C12 | Monitoring, Logging & Anomaly Detection | Security telemetry, traceability, detection, incident evidence, and operational response |

The chapter order is not a repository implementation priority or a security ranking. Prioritization should consider cross-cutting value, testability, current engineering demand, threat severity, source stability, and the opportunity to improve the control-development method.

## 4. Proposed machine-readable catalog

### 4.1 Purpose

The catalog should be a compact inventory and traceability layer, not a second copy of the standard. It should answer:

- Which upstream requirement and exact version is being tracked?
- What is its upstream lifecycle state?
- How mature is this repository's interpretation?
- Where is the detailed control, if one exists?
- Which threat mappings have been justified?
- Which separately maintained engineering-pattern mapping assessments refer to this requirement?

Catalog entries do not require a corresponding Markdown file. Most requirements should initially exist only as catalog metadata; a detailed control document should be created only when that requirement is selected for maturation.

### 4.2 Planned artifacts

Phase 1 introduces only these artifacts:

```text
controls/
├── catalog.yaml
├── schema/
│   └── control-catalog.schema.json
├── templates/
│   └── control.md
├── requirements.txt
├── scripts/
│   └── validate_catalog.py
└── tests/
    └── test_validate_catalog.py
```

Phase 2 adds the Golden Control at
`control-records/c05-access-control-and-identity/v1.0-c5.2.5-agent-authorization-pdp-isolation/README.md`.
Do not create empty directories or one file per AISVS requirement during incremental
development.

Use one family directory and one versioned Requirement directory:

```text
control-records/
└── cNN-family-slug/
    ├── README.md  # family assurance overview and navigation
    └── vX.Y-cN.N.N-descriptive-control-name/
        └── README.md

learning/
└── cNN-family-slug/
    ├── README.md  # lightweight family learning navigation
    └── vX.Y-cN.N-section-slug.md  # only when a substantive Section lecture exists
```

The family number makes the primary AISVS backbone directly traceable. The
descriptive family and Control slugs keep paths understandable, while the versioned
Requirement directory prevents historical interpretations from being overwritten.
Do not create Section directories under `control-records/`. Under `learning/`,
create a versioned Section file only with a substantive lecture. Create a
family directory only when the first substantive Control or learning artifact in
that family is added.

The family `README.md` gives GitHub users a default-rendered overview from Category
to Section to Requirement. It links concise assurance questions and prohibited
failure states to the individual Controls; it is not a conformance checklist.

The Requirement-level `README.md` remains the canonical Control artifact referenced by `control_ref`.
New `learning.md` files contain Section-level teaching, dialogue, and insights for
all Requirements in that Section, with reciprocal links when the relevant Controls
also exist. Learning progress remains independent of Control maturity. Shared
learning policy and Family progress guides remain in `learning/`.
Learning may precede a Control; a substantive Section note does not create a
placeholder Control or catalog entry. Requirement-level C5/C9 notes created under
the earlier convention remain historical artifacts until an explicit migration.

This storage convention does not make other frameworks normative and does not apply
to `engineering/`. `catalog.yaml` remains the source of truth for identity,
lifecycle, maturity, and relationships. An upstream rename or
renumbering triggers semantic review and historical traceability; it does not cause
automatic path rewrites.

### 4.3 Catalog shape

The initial YAML shape should be equivalent to the following proposal:

```yaml
schema_version: 2
catalog:
  source_key: owasp-aisvs
  source_version: "1.0"
  source_status: stable
  canonical_url: "<canonical stable-version URL>"
  last_verified: "YYYY-MM-DD"
  upstream_revision: "<verified upstream commit SHA>"

requirements:
  - versioned_id: v1.0-C5.2.5
    requirement_id: C5.2.5
    family:
      id: C5
      title: Access Control & Identity for AI Components & Users
    section:
      id: C5.2
      title: AI Resource Authorization & Classification
    verification_level: 2
    upstream_status: active
    upstream_url: "<canonical requirement URL>"
    research_source:
      url: "<corresponding AISVS Research URL>"
      last_verified: "YYYY-MM-DD"
    maturity: discovered
    development_priority: golden-control
    control_ref: null
    threat_mappings: []
    related_requirements: []
    mapping_assessment_refs: []
```

This snippet defines a schema proposal; it is not a completed control record.

### 4.4 Field semantics

| Field | Required meaning |
|---|---|
| `source_key` | Exact key from `sources/registry.yaml` |
| `source_version` | Version or rolling state used for the catalog snapshot |
| `source_status` | Source maturity such as stable, beta, public-review, or rolling |
| `canonical_url` | Maintainer-owned location for the tracked source version; immutable per-requirement snapshots are recorded separately |
| `upstream_revision` | Immutable upstream revision inspected during ingestion |
| `versioned_id` | Globally unique source/version requirement identifier, such as `v1.0-C5.2.5` |
| `requirement_id` | Identifier within the source version |
| `family` / `section` | Upstream grouping metadata; the family selects the family directory, each versioned Requirement has its own directory, and sections remain metadata without directories |
| `verification_level` | AISVS level 1, 2, or 3 where applicable |
| `upstream_status` | `active`, `deprecated`, `superseded`, or `removed`; old rows remain for history |
| `maturity` | Repository interpretation maturity defined in the next section |
| `development_priority` | Planning value such as `golden-control`, `next`, or `backlog`; not a coverage score |
| `control_ref` | Path to a substantive control document, or `null` when none exists |
| `research_source` | Corresponding AISVS Research page pinned to `upstream_revision`, and the date that supporting material was inspected |
| `threat_mappings` | Justified, snapshot-aware threat relationships used in the control rationale; each records source/version/status/revision, identifier, relationship, strength, rationale, assessment date, and `proposed`/`validated`/`re-review-required` state |
| `related_requirements` | Related, overlapping, superseding, or superseded requirements |
| `mapping_assessment_refs` | Optional links to canonical assessments under `mappings/`; status and relationship details are not duplicated in the control catalog |

### 4.5 Schema invariants

The JSON Schema and catalog validation should enforce at least:

- uniqueness of `versioned_id` within the catalog;
- consistency between source version and versioned identifier;
- enumerated source, requirement, maturity, and mapping states;
- AISVS verification level limited to 1, 2, or 3;
- no dangling `control_ref` or `mapping_assessment_refs` target;
- consistency between catalog lifecycle/source metadata and Control-document front
  matter when `control_ref` exists;
- presence of the corresponding AISVS Research source for every tracked AISVS requirement;
- preservation of deprecated, superseded, and removed records;
- `maturity: verifiable` only when a substantive control document exists;
- threat sources registered in `sources/registry.yaml`, immutable source snapshots,
  unique mapping identities, and consistent `context` relationship/strength.

The first schema should be intentionally small. Add fields only when the Golden Control demonstrates a real maintenance or assurance need.

AISVS Verification Level is upstream metadata. It is not a repository maturity
stage, a learning difficulty rating, or proof that an implementation satisfies the
Requirement.

Catalog schema version 2 deliberately omits a per-Control reviewer lifecycle. The
current single-maintainer workflow does not benefit enough from reviewer identity,
approval evidence, or separate review-state fields to justify their maintenance
cost. These fields can be reconsidered if the collaboration model changes.

## 5. Control maturity model

Maturity describes the depth of this repository's understanding. It does not describe AISVS verification level and does not prove that a product implements the control.

| Stage | Minimum exit criteria |
|---|---|
| `discovered` | Versioned ID, source/version/status, family/section, verification level, canonical link, and upstream revision are verified |
| `understood` | Repository-authored interpretation, security objective, applicability, assumptions, ambiguity, and known exclusions are documented |
| `threat-linked` | Relevant attacker capability, failure mode, affected assets, and justified threat mappings are documented; absence of a useful mapping is explicit |
| `verifiable` | Testable security properties, positive and negative verification, evidence expectations, and limitations are complete |

Progression is ordered: a record should not skip an earlier stage.

`verifiable` is the current target for a mature Control. Peer feedback and later
revisions may improve it, but they are not modeled as a separate approval lifecycle.

Control maturity describes the quality and usability of the repository artifact.
Learning progress describes a person's understanding of the subject. They are
independent: completing a learning step must not promote a Control, and maturing a
Control must not mark a learning step complete.

Engineering mapping assessment is maintained separately under `mappings/`. Its
status may be `not-assessed`, `assessed-no-match`, `gap`, `proposed`, `validated`,
or `re-review-required`. A Control can reach `verifiable` without an assessment or
a successful mapping. Mapping state must not promote or demote Control maturity.

## 6. Definition of a complete control

A substantive Control is mature at `verifiable` when it contains all of the following:

1. Stable repository title and exact versioned upstream requirement ID.
2. Source version, maturity/status, canonical URL, verified revision, and last-verified date.
3. Concise repository-authored interpretation that does not reproduce the normative text wholesale.
4. Security objective and the reason the control exists.
5. Applicability, non-applicability, assumptions, assets, actors, identities, and trust boundaries where relevant.
6. Required security properties expressed independently of a particular product or implementation where possible.
7. Threat and failure-mode rationale with defensible mappings or an explicit statement that no mapping adds value.
8. Verification guidance covering positive behavior, negative/abuse cases, expected results, and failure conditions.
9. Evidence expectations identifying acceptable artifact types, producers, freshness, scope, and acceptance criteria.
10. Related or overlapping requirements that must not be incorrectly collapsed.
11. Known limitations, residual uncertainty, and implementation-dependent assumptions.
12. Primary references, attribution, and material change history.

These criteria—not the mere existence of documentation, a completed learning step,
a configuration flag, or a framework mapping—define maturity. Peer feedback is
useful but is not a separate lifecycle state in the current repository workflow.

Engineering mapping is assessed separately after a Pattern exists independently.
The assessment may validly conclude `assessed-no-match` or `gap`; neither outcome
reduces control maturity.

## 7. First family and Golden Control

### 7.1 Recommended first family: C5 Access Control & Identity

Develop C5 first because it:

- establishes the deterministic authorization boundary that many AI security properties depend on;
- applies across agents, RAG, MCP, model access, training data, and multi-tenant systems;
- exercises identity, delegation, policy enforcement, resource authorization, and isolation concepts without requiring full lifecycle coverage;
- has clear positive and negative verification opportunities;
- produces concrete evidence such as architecture boundaries, policy decisions, denied requests, token scope, and tenant-isolation results;
- is small enough to mature incrementally while still exposing cross-family overlaps with C8, C9, and C10;
- aligns with the repository principle that model reasoning must not be an authorization boundary.

This is a repository development priority, not a claim that C5 is universally more important than every other AISVS chapter.

### 7.2 Initial Golden Control: `v1.0-C5.2.5`

Select AISVS Level 2 requirement `v1.0-C5.2.5` as the first Golden Control. In concise repository terms, it requires the policy decision point for agent authorization to be isolated from the agent execution environment.

It is a strong exemplar because it requires:

- a concrete trust boundary between a potentially compromised agent and deterministic authorization;
- explicit identities, resources, actions, and policy inputs;
- a clear insecure failure mode in which the agent can influence or bypass its own authorization;
- implementation-independent security properties;
- negative tests that attempt to bypass, tamper with, or fail open around the policy decision point;
- multiple evidence types, including architecture review, policy configuration, decision logs, denial tests, and deployment isolation evidence;
- careful relationship analysis with `v1.0-C9.5.3`, without assuming the two requirements are duplicates;
- a stable security boundary that can later be compared with independently
  discovered engineering patterns.

The Golden Control phase should not pre-populate engineering mappings. Threat and
related-requirement analysis belongs to control development; engineering links are
assessed only after an independent Pattern endpoint exists.

## 8. Relationship model

Controls and Patterns have separate origins. Mapping is a third artifact:

```text
Authoritative requirement              Systems / attacks / recurring failures
          |                                           |
          v                                           v
Control security property                  Engineering Pattern
          |                                           |
          +--> verification and evidence              |
          \                                           /
           +---------- mapping assessment -----------+
```

### Threats

- Use MITRE ATLAS for adversary behavior and OWASP risk taxonomies for risk context.
- Record source key, identifier, version/status, relationship, strength, rationale, and assessment date.
- Map only when the threat explains why the control is needed or what it mitigates/detects.
- Do not infer a mapping from similar words.

### Engineering patterns

- Patterns are discovered from recurring system security problems and attack
  scenarios, not from this control inventory.
- Compare a control with a Pattern only after both are independently understandable
  and reviewable.
- Map by stable repository path and endpoint/source revision.
- Use `direct`, `partial`, or `context` consistently.
- State which part of the control the pattern addresses and what remains outside it.
- Allow zero, one, or many patterns per control and zero, one, or many controls per pattern.
- If no suitable pattern exists, record an `engineering-gap` instead of creating or modifying engineering content from within the controls task.

### Verification

- Verification evaluates the security property, not the presence of a document or configuration key.
- Distinguish architecture review, configuration inspection, automated tests, abuse tests, runtime checks, and manual review.
- Define both success and failure conditions.
- Keep implementation-specific procedures in the control document or linked engineering pattern, not in the catalog record.

### Evidence

- Define expected evidence classes rather than storing real production evidence in this repository.
- For each class, specify producer, system scope, collection time, freshness, integrity expectations, sensitivity, and acceptance criteria.
- Treat screenshots and configuration exports as point-in-time evidence, not proof of continuous enforcement.
- Prefer repeatable test results and policy-decision records where the security property permits them.

This model keeps `controls/` and `engineering/` independent: controls define the assurance claim and evaluation criteria, while engineering patterns independently describe recurring design problems and reusable solutions. Mapping records the assessed relationship without rewriting either endpoint.

## 9. Information that remains upstream-only

| Information | Why it stays upstream | Repository treatment |
|---|---|---|
| Full normative requirement text and complete AISVS chapters | AISVS is the source of truth and evolves under its own release process and license | Store versioned IDs, concise original interpretation, source revision, and canonical links |
| Full Appendix B controls inventory | It is non-normative and duplicates every requirement in a different organization | Use it as an analysis aid; do not import it as repository structure |
| AISVS Research Wiki pages and their full tooling/research notes | They are extensive, independently maintained, and may change separately | Link only to the relevant page and summarize material conclusions with attribution when needed |
| Complete OWASP Top 10 risk descriptions and mitigations | They are risk taxonomies, not this repository's control model | Record IDs, version/status, short rationale, and links |
| Complete MITRE ATLAS technique, mitigation, and case-study content | ATLAS is a rolling adversary knowledge base | Record stable identifiers where available, the inspected state/date, and original mapping rationale |
| Upstream diagrams, tables, logos, and substantial licensed prose | Copying creates licensing and maintenance obligations | Reference the primary source; check license compatibility before any substantial adaptation |
| Upstream change history | Upstream owns the authoritative history | Preserve only repository impact reviews and links to the relevant upstream revisions |

The repository may retain exact identifiers, source/family/section names, verification level, lifecycle status, canonical URLs, immutable revision references, and concise original interpretations. Until the repository license is selected, avoid importing substantial CC BY-SA or other licensed upstream content.

Actual production evidence is not upstream material, but it should also remain outside this public knowledge base. Store only evidence expectations and sanitized examples; keep secrets, sensitive logs, customer data, and organization-confidential artifacts in the appropriate evidence system.

## 10. Incremental roadmap

### Phase 0 — Landscape and decisions

Deliverables:

- approve this purpose, boundary, family inventory, maturity model, and Golden Control selection;
- record open design decisions without creating requirement placeholders.

Exit gate:

- maintainer decision that the plan is narrow enough to execute and that C5/C5.2.5 is the correct first experiment.

### Phase 1 — Catalog and template experiment

Deliverables:

- create `catalog.yaml` with source metadata and only the Golden Control record;
- create a minimal JSON Schema enforcing the proposed invariants;
- create a control template based on the completeness criteria;
- add Python validation with a pinned YAML parser for schema errors, duplicate IDs,
  identifier consistency, invalid states, maturity gates, and dangling references;
- add regression tests for the catalog validator.

Exit gate:

- the catalog validates deterministically and does not require copied requirement text.

### Phase 2 — Mature the Golden Control

Deliverables:

- develop `v1.0-C5.2.5` through all four control maturity stages;
- validate threat and related-requirement mappings;
- define verification and evidence expectations.

Exit gate:

- the Control is `verifiable` and demonstrates a reusable Golden Control method.

### Phase 3 — Refine the method using C5

Deliverables:

- update schema, template, and instructions only from demonstrated Golden Control needs;
- ingest C5 requirement metadata into the catalog without generating one file per requirement;
- select the next two or three C5 requirements based on distinct learning value, not numerical order;
- mature one selected requirement at a time.

Candidate learning areas include end-user authorization context in retrieval, policy-enforced resource access, and multi-tenant isolation. Selection requires a separate review of the exact requirement, assurance value, and threat evidence.

Exit gate:

- at least two additional controls demonstrate that the template works beyond the Golden Control and that overlaps can be represented without duplication.

### Phase 4 — Add adjacent agentic families

Prioritize one representative requirement at a time from:

1. C9 Orchestration & Agentic Security;
2. C10 MCP Security;
3. C8 Memory, Embeddings & Vector Database Security.

This wave tests authorization delegation, tool boundaries, protocol identity, retrieval isolation, and cross-family control relationships. Do not ingest detailed content for all three chapters at once.

Exit gate:

- each selected control adds a distinct verification or evidence approach and is
  mature on its own terms.

### Phase 5 — Expand by assurance and risk need

Use observed product-security demand, threat evidence, assurance gaps, and review
capacity to select representative controls from:

- C2 and C12 for input boundaries and operational detection;
- C1, C3, C4, and C6 for data/model lifecycle, infrastructure, and supply-chain assurance;
- C7 and C11 for behavior/output assurance and adversarial robustness.

The order may change when threat evidence, engineering adoption, incidents, or upstream changes justify it. Record the decision rather than treating chapter order as a backlog.

### Phase 6 — Maintenance automation

Only after the catalog and several controls are stable:

- detect upstream version, identifier, level, and requirement changes;
- compare immutable old/new source snapshots;
- flag affected catalog records, controls, mappings, and evidence expectations;
- set Mapping assessments to `re-review-required` where appropriate;
- generate change proposals rather than rewriting Controls automatically;
- report stale source inspections and mappings.

Exit gate:

- automation preserves history, produces deterministic reports, and cannot silently promote Control maturity or validate security-significant Mapping changes.

## 11. Progress measures

Do not use percentage of AISVS requirements documented as the primary success metric. Prefer:

- number of `verifiable` Controls with complete source, scope, verification, evidence, and limitations;
- percentage of mature controls with executable or repeatable negative verification;
- mapping rationale review quality and stale-mapping count;
- time to identify and triage a relevant upstream change;
- quality and age of separate mapping assessments;
- evidence expectations that engineering teams can actually produce;
- recurring lessons incorporated into schema, template, and guidance.

## 12. Primary references

- [OWASP AISVS repository and current stable-version guidance](https://github.com/OWASP/AISVS)
- [OWASP AISVS v1.0 stable source](https://github.com/OWASP/AISVS/tree/main/1.0)
- [OWASP AISVS release policy](https://github.com/OWASP/AISVS/blob/main/RELEASE.md)
- [AISVS C5 Access Control & Identity](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [AISVS C9 Orchestration & Agentic Security](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
- [AISVS Appendix B: AI Security Controls Inventory](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x91-Appendix-B_AI_Security_Controls_Inventory.md)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/)
- [OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/)
- [OWASP AI Exchange](https://owasp.org/www-project-ai-security-and-privacy-guide/)
