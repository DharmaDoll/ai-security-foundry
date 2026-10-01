# AISVS C7 Model Behavior, Output Control & Safety Assurance

対象はAISVS v1.0の固定Revision `78775233666a2022dcfb82037e5e029116955c00`。
この一覧は[正規要件][normative]の代替ではなく、保証境界を辿るためのRepository interpretation。
[Section単位の学習資料](../../learning/c07-model-behavior-output-control-and-safety-assurance/README.md)は
講義と対話を扱い、Controlの成熟度とは独立する。正規Metadataは[Catalog](../../catalog.yaml)を参照する。

## この章で保証したいこと

Model出力は、Userへ表示する文章もToolへ渡す引数も、未検証のDataである。
形式、長さ、信頼性、有害性、出典をそれぞれ確認し、該当する境界を越える前に
Applicationが扱いを決める。形式に合うことだけで内容の安全性、事実性、
権限、出典の真正性を保証したとしない。

## Categoryで問うこと

| 問うこと | できてはいけないこと |
|---|---|
| Modelが生成した内容を、用途に応じて検証・制限したうえで公開・利用するか。 | Model応答を完成済みの信頼できる命令・事実・証拠として直接扱う。 |

## Section

| Section | 問うこと | できてはいけないこと |
|---|---|---|
| C7.1 Output Format Enforcement | 出力の形式・長さ・終了状態を、利用前に制御できるか。 | 不正な構造や未完了の出力を完成済みとして下流へ渡す。 |
| C7.2 Hallucination Detection & Mitigation | 回答の信頼性を評価し、低信頼・高リスク時の追加処理を行うか。 | 推測や架空の内容を、検証済みの事実として扱う。 |
| C7.3 Output Safety | 危険な内容・内部情報・外向き要求・隠蔽を公開前に扱えるか。 | 出力に紛れた危険な内容がUserや下流へそのまま届く。 |
| C7.4 Source Attribution & Citation Integrity | RAGの出典と主張を追跡でき、必要な生成Mediaの表示を行うか。 | Modelが作った引用表示だけを根拠とみなす。 |

## Requirement

個別Controlが未作成の行は、未成熟の保証上の問いであり、Catalog登録済みControlではない。
Levelは上流のVerification Levelであって、開発優先度や製品の適合度ではない。

C7.1では「その出力を受け入れてよい形か」（C7.1.1）と、
「生成は制限内で終わり、完成した出力か」（C7.1.2）を別々に確認する。
正常終了だけではSchema適合を示せず、Schema適合の断片だけでも正常終了を示せない。

C7.2では、信頼性を推定する（C7.2.1）、低Confidenceを自動で遮断・代替する
（C7.2.2）、誤答時のImpactが高い回答を追加検証する（C7.2.3）を分ける。
高ConfidenceはHigh-riskの追加検証を省略する理由にならない。

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C7.1.1](v1.0-c7.1.1-validate-and-reject-model-outputs-by-schema/README.md) | 1 | 全Model出力を定義済みSchemaで検証し、不一致を拒否するか。 | JSONとして読めたことや生成時の形式指定だけで下流へ渡す。 |
| [C7.1.2](v1.0-c7.1.2-bound-model-output-length-and-termination/README.md) | 1 | 出力の長さと終了を制御するか。 | 上限到達・中断で終わった断片を完成済みとして使う。 |
| [C7.2.1](v1.0-c7.2.1-estimate-generated-answer-reliability/README.md) | 2 | 生成回答の信頼性をConfidence推定で評価するか。 | 回答の流暢さやModel自身の自信表現を信頼性の証拠とする。 |
| [C7.2.2](v1.0-c7.2.2-block-or-fallback-below-confidence-threshold/README.md) | 2 | 閾値未満の低Confidence回答を自動で遮断・Fallbackへ移すか。 | 低信頼と判定してもWarningだけで元回答を返す。 |
| [C7.2.3](v1.0-c7.2.3-additional-verification-for-high-risk-responses/README.md) | 3 | Policy上High-riskの回答へ追加検証を行うか。 | 高Confidenceを理由に高Impact回答の追加確認を省く。 |
| [C7.3.1](v1.0-c7.3.1-classify-and-block-harmful-responses/README.md) | 1 | 全Responseを有害内容Classifierで検査し、該当内容を遮断するか。 | 検知しても公開・送信を続ける。 |
| C7.3.2 | 2 | System PromptやBackend Dataの漏えいを検出・遮断するか。 | 内部情報をUser向け出力へ混入させる。 |
| C7.3.3 | 2 | Model生成出力が外向きRequestを起動しないか。 | 未信頼出力から外部通信が自動的に発生する。 |
| C7.3.4 | 3 | 文字・形式・Metadata等で隠れた／誤認を誘う内容を検査するか。 | 見た目だけで安全と判定する。 |
| C7.4.1 | 1 | RAG利用回答に元文書へのAttributionがあるか。 | 根拠を辿れない回答を出典付きと表示する。 |
| C7.4.2 | 1 | AttributionをModel生成TextではなくRetrieval Metadataから得るか。 | Modelが架空の出典を作れる。 |
| C7.4.3 | 2 | RAG回答の主張を取得Chunkへ辿れるか。 | 文書名だけで個々の主張の裏付けが不明になる。 |
| C7.4.4 | 3 | 生成MediaへAI生成を証明するWatermarkを付けるか。 | 生成物の由来を確認できない。 |

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md

開発順序は[Controls計画](../../plan.md)を参照する。Control本文では対象Requirementと
対応する[AISVS C7.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-01-Output-Format-Enforcement.md)等を確認する。
