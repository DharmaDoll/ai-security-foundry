---
title: "隠れた・符号化された・誤認を誘うModel出力を検査する"
versioned_id: "v1.0-C7.3.4"
requirement_id: "C7.3.4"
verification_level: 3
family_id: "C7"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-03-Output-Safety-Privacy-Explainability.md"
last_verified: "2026-10-02"
maturity: "verifiable"
mapping_assessment_refs: []
---

# 隠れた・符号化された・誤認を誘うModel出力を検査する

AISVS Verification Level: 3

学習資料：[C7.3 Output Safety](../../../learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.3-output-safety.md)

## Upstream basis

AISVS `v1.0-C7.3.4`は、Model出力について、類似文字、書式、Metadata、
構造化Field等が作る隠れた・符号化された・誤認を誘う内容を検査することを
求める。原文は「検査する」であり、すべての該当文字を一律削除・拒否する
とは書いていない。対応Researchは、Unicodeの不可視・方向制御文字、
ANSI Escape、表示されないField等と、正常な多言語表現を壊す過剰除去を論じる。
Researchの統計的なToken選択によるSteganographyは追加の研究論点として扱い、
単一Responseでの検出を本Requirementの必須Pass条件にしない。

## Interpretation

Model出力を、表示された見た目だけで安全と判断しない。実際のByte／Code Point、
Parserが解釈するField、Rendererが表示する内容、後続Systemが受け取る内容を
対象Sinkごとに照合し、表現差や隠れたPayloadを検査する。Unicode、Markup、
Metadata、Structured Dataを、一つの文字列の「本文」へ平坦化して終わらせない。

検査が見つけた内容の扱いはSinkのPolicyに結び付ける。例えばTool引数、Code、
Terminal表示では曖昧な識別子・制御文字を拒否または無害化する方針があり得る。
一方、通常のChatで必要な文字を無条件に削除すると言語や意味を壊す。
方式は一律に固定せず、どの表現を許容し、どれを警告・拒否・変換するかを
用途別に示し、その判定が検査後の実際の出力に適用されることを確認する。

## Security objective

人間が見た内容と下流処理が解釈する内容のずれを見逃さず、隠れた指示、
偽装された識別子、非表示の送信先やDataが信頼境界を越える前に発見できる
ようにする。検査自体が、内容の適法性・認可・安全性をすべて保証するわけではない。

## Applicability

Model出力を画面、Terminal、Code／設定File、Markdown／HTML、Tool引数、
Memory、別Agent、構造化API Response、生成Media等へ渡すSystemに適用する。
各形式で意味を持つ非表示Field・Metadataと、変換後の表現を確認する。

### Non-applicability

Model出力を生成・取得・利用しない処理は直接対象外。単に「画面には
Plain Textしか見せない」「Schema検証済み」という理由では、Raw出力や
未知Field、コピー後・再解釈後の意味を確認したことにはならない。

## Scope and assumptions

- まず出力先と、そのParser／Renderer／下流Componentが解釈する形式を特定する。
  Sinkが違えば危険な表現も変わる。
- 検査前のRaw値と、正規化・Sanitize・Decode・Render後に実際に使う値の
  対応を保つ。検査後の変換で新しい意味が生じるなら再検査する。
- UnicodeのZWJ、ZWNJ、Variation Selector、双方向Text等には正当な用途がある。
  一律の文字Category削除を適合条件にしない。
- すべての符号化・隠蔽技法を有限の検査で発見できるとは主張しない。
  検査対象、未対応形式、誤検知と見逃しを明示する。

## Assets, actors, identities, and trust boundaries

保護対象は利用者の判断、Tool／Code実行先、識別子、内部Data、下流Policy。
攻撃者は入力文書やTool結果を通じてModelにPayloadを出力させ得る。
Modelも悪意なしに曖昧な文字やMetadataを出す可能性がある。

Trust BoundaryはRaw Model出力からRenderer／Parserへ、表示された内容から
人間の判断へ、そして下流のTool／File／Agentへ渡る地点にある。
その境界で「見える文字列」と「実際に解釈される値」が異なるなら、
見た目だけのレビューや本文だけのFilterでは検査にならない。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 各Model出力Sinkについて、Raw値、変換、表示、下流利用の経路と検査対象形式を特定できる。 |
| SP-2 | 類似文字・不可視／方向制御文字、書式、Metadata、構造化Fieldに隠れた・符号化された・誤認を誘う内容を、該当Sinkで検査する。 |
| SP-3 | 検査結果を実際に利用されるPayloadへ結び付け、後続変換や別Fieldで未検査の意味が生じないことを確認できる。 |
| SP-4 | 検出時の扱いをSink別Policyで定義し、必要な言語表現を壊す過剰処理と、危険な表現の素通しを試験で識別できる。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| JSON Schemaには合うが未知FieldにURLが入る | Schema適合だけではSP-2を示せない。未知Fieldの扱いと実際のSinkを検査する。 |
| TerminalにANSI Escapeを含む回答をそのまま表示する | 表示変更や偽装の可能性を検査していなければFail。検出後の拒否・無害化はTerminal Policyに従う。 |
| ペルシア語の正当なZWNJや絵文字のZWJを使う | 不可視文字というだけでFailではない。正当例を壊さず、危険な用法との差を評価する。 |
| 見えないField内のURLを検出する | 本Controlの検査。実際の自動外部通信の禁止はC7.3.3の別保証。 |
| Metadataに機密Dataがある | 本Controlで非表示部分を検査する。開示の可否と遮断はC7.3.2等でも評価する。 |
| 入力文書のUnicode隠蔽を検査済み | C2の入力側保証。新たに生成した出力の検査は省けない。 |

## Threat and failure-mode rationale

Unicodeの方向制御でCodeや識別子の見た目を変える、不可視文字へDataを
埋め込む、MarkdownやJSONの非表示Fieldに送信先を置く、といった方法では、
人間のレビュー画面と下流が実際に使う内容が異なる。検査器がRender後の
本文だけを見るとPayloadを失い、Raw値だけを見て下流解釈を知らなければ
危険を評価できない。外部Threat IDへの厳密なMappingは未評価とする。

## Verification

### Architecture and configuration review

Raw出力から各Sinkまでの変換順序、ParserとRendererの仕様、Metadata・
未知Fieldの扱い、検査位置、検査結果後の処理を追う。表示用の値と
Tool／Code／Memoryへ渡す値を比較し、見えないDataがどこに残るか確認する。

### Positive verification

正当な多言語文、絵文字、双方向Text、必要なMetadataを含む出力を試し、
用途に必要な情報が破壊されず、検査結果と実際の表示・下流値が対応する
ことを確認する。正当例を通すことだけで危険例の検出を推定しない。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Unicode Tags、Variation Selector、Zero-width、Bidi制御を含む合成出力を各Sinkへ渡す | Rawと表示／下流値の差を検出し、Sink Policy上の扱いを記録する。SP-1〜SP-4 |
| N-2 | 混在Scriptの類似文字でUser名、Tool名、送金先ID等を偽装する | 対象識別子の見た目と実値の違いを検査し、Policyで定めた扱いになる。SP-2〜SP-4 |
| N-3 | ANSI Escapeを含む出力をTerminal、Markdownの非表示要素をBrowserへ渡す | 画面上の見え方だけで安全と判定せず、制御・非表示部分を検査する。SP-1〜SP-3 |
| N-4 | JSONの未知Field、画像・File Metadata、Alt Textに合成Payloadを置く | 表示本文以外も、利用する形式に応じて検査する。SP-1〜SP-3 |
| N-5 | 検査後にDecode・正規化・Renderを変え、別の意味を生じさせる | 実際に使用する表現への検査の適用を確認し、検査済みと誤認しない。SP-1〜SP-3 |
| N-6 | 正当な多言語文字・絵文字を危険例と同じ検査へ通す | 一律削除で必要な表現を壊さず、誤検知とPolicy上の判断を記録する。SP-4 |

### Failure conditions

表示本文しか検査しない、Metadata・Structured Fieldを対象外とする、
Rawと下流解釈の差を確認しない、または検査後の変換で未検査の意味が生じる
場合はFail。危険な表現を検知しても、その扱いが定義されず、下流Sinkへ
無検討で渡されるならSP-4の実効性を示せない。ただし、特定の文字を
一律に拒否しないことだけでFailとはしない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Sink・変換・Field一覧 | Application／Renderer Owner | Raw出力、表示、Tool、File、Memory | Sink・Parser変更時 | 機密Payloadを含めずVersion保持 | 検査対象と実際の解釈先を辿れる。 |
| 合成表現Corpus | Security／Test Owner | N-1〜N-6、正当な多言語例 | Model・Renderer・Policy変更時 | 合成IDとExpected Resultを保持 | 隠蔽例と正常例の境界を再現できる。 |
| 検査・Sink試験結果 | Test Harness | Raw／表示／下流値の比較 | Release・変換変更時 | Rawの機密化に注意し最小化 | 未検査Field・変換が残らないことを示す。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C2.1.2`／`v1.0-C2.1.7` | 入力側のEncoding隠蔽と予約Token。入力検査は出力検査の代替ではない。 |
| `v1.0-C7.1.1` | Schema適合。許可されたField内の不可視・誤認Contentは別に検査する。 |
| `v1.0-C7.3.1` | 有害Category分類と遮断。隠れた表現の検査は分類器の適用前提になり得るが同一要件ではない。 |
| `v1.0-C7.3.2`／`v1.0-C7.3.3` | 開示と外向きRequestの別保証。検査だけで漏えい遮断・通信禁止を示さない。 |

## Known limitations and uncertainty

未知の符号化、Renderer固有の解釈、統計的なToken選択に潜むChannelは
有限のCorpusで完全には検出できない。Researchが挙げる統計的Steganographyは
反復出力や分布情報を要し、単一出力の検査と成熟度が異なる。
本ControlはC7.3.4の明示する表現・Fieldの検査を中核とし、追加研究を
未検証の必須条件へ昇格させない。`verifiable`は本Artifactの成熟度であり、
製品の出力安全性を保証しない。

## References

- [AISVS v1.0 C7 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md)
- [AISVS v1.0 C7.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-03-Output-Safety-Privacy-Explainability.md)
- [C7 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-10-02 | C7.3.4初版。Raw／表示／下流解釈の差とSink別の検査を定義 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
