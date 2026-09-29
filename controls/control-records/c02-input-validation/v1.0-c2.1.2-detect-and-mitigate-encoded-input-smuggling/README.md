---
title: "入力に隠されたEncoding・表現Smugglingを検出し緩和する"
versioned_id: "v1.0-C2.1.2"
requirement_id: "C2.1.2"
verification_level: 1
family_id: "C2"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md"
last_verified: "2026-09-29"
maturity: "verifiable"
mapping_assessment_refs: []
---

# 入力に隠されたEncoding・表現Smugglingを検出し緩和する

AISVS Verification Level: 1

学習資料：[C2.1 Prompt Injection Defenses](../../../learning/c02-input-validation/v1.0-c2.1-prompt-injection-defenses.md)

## Upstream basis

AISVS `v1.0-C2.1.2`は、入力のEncoding・表現Smugglingを**検出し、緩和する**ことを求める。
Normative本文が示す許容される緩和方法は、Canonicalization、Strict Schema Validation、
Policy-based Rejection、Explicit Markingである。C2.1 Researchは、不可視Unicode、
文字の見た目とCode Pointの差、Base64等で隠した指示、多段変換、復号後の再評価を具体化する。

Researchに列挙された個別Scanner・製品・閾値・攻撃成功率は、この要件の必須実装や
自動的な適合根拠ではない。Researchは出力経路にも言及するが、NormativeのC2.1.2は
**入力**の検出・緩和を対象とする。出力処理は隣接保証として別途評価する。

## Interpretation

入力が別の表現に隠され、検査器や利用者が見た内容と、後段のModel・Parser・Toolが
解釈する内容が異なる場合を識別する。検出した表現に対して、その入力経路と用途に
適した緩和方法を適用し、隠れた内容が未評価のまま新しい権限・指示・操作へ昇格しないようにする。

例えばBase64文書を要約する正当な用途では、Base64の存在だけで一律に拒否する必要はない。
復号結果を新しい非信頼入力として扱い、再評価してから利用する。一方、型の決まった識別子欄では
Strict SchemaでEncodingを拒否できる。Explicit Markingを選ぶなら、印を付けたという記録だけでなく、
後段で元の信頼度・由来を失わず、隠れた指示を権威として扱わないことを確認する。

## Security objective

攻撃者がEncodingや表示・解釈差を使って指示・宛先・引数を隠し、入力側の検査や
信頼区分を迂回する可能性を下げる。検出器の未知攻撃への完全性やModelの忠実な指示追従は保証しない。

## Applicability

Model、Embedding、Agent、Tool、Parserへ進む可能性のある入力を対象にする。
User Messageだけでなく、取得文書、Webページ、Tool／MCP Response、Memory、
Skill／設定ファイル由来のText、OCR／文字起こし結果を、それぞれの入口と変換出口で確認する。
認証されたSourceから取得した内容でも、本文の信頼性は別問題である。

### Non-applicability

Modelや後続の解釈器へ渡らず、復号・変換もされない不透明なBinary保管のみの経路は
直接対象外とできる。将来Textとして抽出・表示・処理する経路があるなら、その出口から対象になる。
「Base64を使っていない」だけでは、Unicode、表示差、別のEncodingを除外できない。

## Scope and assumptions

- Smugglingは、同じ入力が経路の異なる段階で別の意味・表示・Token列として解釈されることを指す。
- 何を異常表現とみなすかは入力型・用途・対応言語ごとに定義する。Flag Emoji、結合文字、
  正当な多言語入力を機械的に攻撃と扱わない。
- 一律の無制限再帰復号は求めない。許容する変換、深さ、サイズ、曖昧さ、失敗時動作を定義する。
- 入力検査で一度Passしたことは、後で復号・連結・レンダリングしてできた新しいTextのPassを意味しない。
- Explicit MarkingはNormativeが列挙する選択肢だが、その安全効果は受け手の解釈と用途に依存する。
  Markingだけで高影響操作を許可したり、認可を代替したりしない。

## Assets, actors, identities, and trust boundaries

保護対象はModelへ入る命令の優先順位、入力内容の完全性、Tool引数や宛先へ流れる値、
下流の機密Dataと操作権限。攻撃者は低信頼入力の一部を編集できる。
ApplicationのParser／Decoder／Normalizer、検査器、Prompt Builder、Model、
Agent Runtime、Toolが異なる解釈をし得る。

Trust Boundaryは、元の低信頼表現から復号・描画・抽出された内容へ移る地点と、
その内容を指示・Tool引数・信頼済みMemoryとして採用する地点にある。
決定論的なEnforcement Pointは、入力種別ごとのParser／Gatewayと変換後の利用前Gate。
検出器自体の意味判断が確率的でも、検知結果に対応する拒否・隔離・Markingの実行は
Application側で強制できる。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 対象入力経路と許容する表現・Encodingを定義し、Smugglingを検出する仕組みが実際の利用経路に適用される。 |
| SP-2 | 検出された入力には、Canonicalization、Strict Schema Validation、Policy-based Rejection、Explicit Markingのうち、その用途で実効性を示せる緩和を適用する。単なるAlertだけで継続しない。 |
| SP-3 | 復号・変換後に新しく得たTextは、元入力の検査結果を無条件に再利用せず、下流の利用前に低信頼として再評価する。 |
| SP-4 | 変換・検出・緩和に失敗した場合、未評価Contentが黙って高信頼の指示・操作入力へFallbackしない。 |
| SP-5 | Markingを選ぶ経路では、Sourceと低信頼区分が後段まで残り、Modelの自己申告だけを根拠に権限を与えない。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 隠蔽を検出し、復号後Textを低信頼として再評価または拒否する | C2.1.2のPositive Evidence。 |
| Unicodeを正規化したが、Base64で隠れた内容を未確認で使う | C2.1.1が成立してもC2.1.2はFail。 |
| 明文のPrompt Injectionを見逃す、検知済みInjectionを遮断しない | 主にC2.1.3。Smugglingの緩和まで失敗していれば本ControlでもFail。 |
| 入力の隠蔽は緩和したがToolが不正な送金を許す | 認可・Action GateはC5／C9の別保証。 |
| 出力Markdownや外部URLのレンダリングで漏えいする | 出力・Egress側の保証も必要。本Controlの入力限定を全体安全性と誤認しない。 |

## Threat and failure-mode rationale

攻撃者は、Base64やHexなどのEncoding、不可視Unicode、双方向表示、複数段の変換を使い、
入力検査器には無害または読めないTextを見せる一方、後段には命令として読ませようとする。
例えばAgentが「このBase64を復号して従え」という文書を処理し、復号後の命令を
新たなUser指示だと誤認すれば、元文書が持たない権威を得る。

ResearchはTokenizer／Renderer／検査器の解釈差を残余リスクとして挙げる。
外部Threat IDは本作業で独立評価していないため、Catalogの`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

User、RAG、Tool、Memory、File、OCR等の入口から、復号・正規化・抽出・Prompt組立て・
Tool実行までのData Flowを追う。入力型別の許容表現、検出条件、緩和方式、変換後の
再評価位置、低信頼Markerの保持先、失敗時の経路を確認する。
Scannerを導入した事実だけでPassにせず、その判定が実際の利用を変えることを確かめる。

### Positive verification

正当なEncoding資料を許容する用途では、復号後の内容が低信頼として扱われ、
定義した再評価を通ってから要約等の許可された利用へ進むことを確認する。
Schemaが厳格な入力欄では、許可値を通常どおり処理できることを確認する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Base64／Hexで隠した指示を取得文書に埋め、後段で復号させる | 復号後Textを低信頼として再評価し、隠れた指示を新しい権威にしない。SP-1〜SP-3 |
| N-2 | 不可視Unicode、双方向制御、表示とCode Pointが異なる表現を混ぜる | 定義した検出・緩和が働き、未評価の解釈差を黙って通さない。SP-1, SP-2 |
| N-3 | 一段目だけ検査して二段目のEncodingを復号する | 後段の新しいTextへ元のPassを流用しない。制限外の変換は拒否・隔離する。SP-3, SP-4 |
| N-4 | Explicit Markingした入力をSummary、Memory、Tool引数へ転送する | Markerと低信頼区分を失わず、Markingのみを認可根拠にしない。SP-5 |
| N-5 | Detector／Decoderの失敗、Timeout、未知Encodingを発生させる | 未評価のまま高信頼経路へFallbackしない。SP-4 |
| N-6 | 正常な多言語Text、Emoji、許可されたEncoded Dataを投入する | 用途Policyどおりに処理し、不要な一律拒否をしない。SP-1, SP-2 |

### Failure conditions

Smugglingのある入力を識別できず、そのまま後段が復号・解釈する、検出しても
実際の利用経路で緩和されない、復号後Textを元のPassで処理する、またはMarkerが
権限を得る前に消える場合はFailを裏付ける。特定の既知Payloadだけを検出した結果を
未知Encodingへの完全な防御と扱わない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 表現・変換Policy | Application／Security Owner | 入力型と変換経路 | Parser／Policy変更時 | Revisionを保持し、実Dataを含めない | 許容Encoding、変換上限、緩和方式、失敗時処理が分かる。 |
| Data FlowとGate配置 | Architecture／Application Owner | 復号前後、Model／Toolへの入口 | Topology変更時 | Revisionとレビュー履歴 | 未評価Contentが強いContextへ昇格しない位置を示せる。 |
| 合成Payload試験 | Test Harness | N-1〜N-6の代表経路 | Release・Model／Parser更新時 | 合成Dataと判定Revisionを保持 | 検出と緩和の双方が観測でき、正常系も成立する。 |
| Marker伝播・判定記録 | Runtime／Gateway | Marking採用経路のみ | 導入・変更時 | Content本体や秘密を最小化 | 後段の信頼区分・拒否／許可の理由を追える。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C2.1.1` | Token化・Embedding前の正規化。正規化だけでSmugglingの検出・緩和は終わらない。 |
| `v1.0-C2.1.3` | Modelを誘導し得る全入力のInjection検査とFlag時の遮断。 |
| `v1.0-C2.1.5` | 入力文字集合のAllowlist。表現Smugglingを減らす一手段だが別要件。 |
| `v1.0-C2.1.7` | 予約特殊TokenがMessage境界を作らない保証。 |
| `v1.0-C8.2.4` | Retrieval操作ContentのVectorization前検査。 |

## Known limitations and uncertainty

見た目とCode Pointの差、Tokenizerの差、暗号化された任意Payload、自然言語の婉曲な指示を
全て検出できるわけではない。合法的な多言語・Encoded Dataとの誤検知もある。
Explicit Markingは低信頼を示す方法としてNormativeにあるが、Modelへ単なるLabelを
書くだけでは遵守を保証しない。高影響操作には独立した認可・能力制限が必要である。

`verifiable`はControl記録の成熟度であり、製品適合や実際の検出率の保証ではない。

## References

- [AISVS v1.0 C2 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md)
- [AISVS v1.0 C2.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md)
- [C2 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-29 | C2.1.2初版。表現隠蔽の検出と緩和をC2.1.1／C2.1.3から分離 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
