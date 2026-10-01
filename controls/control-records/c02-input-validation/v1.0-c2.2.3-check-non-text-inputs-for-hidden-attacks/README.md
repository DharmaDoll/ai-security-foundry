---
title: "非テキスト入力に隠れた攻撃を検査する"
versioned_id: "v1.0-C2.2.3"
requirement_id: "C2.2.3"
verification_level: 2
family_id: "C2"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-02-Content-Policy-Screening.md"
last_verified: "2026-09-30"
maturity: "verifiable"
mapping_assessment_refs: []
---

# 非テキスト入力に隠れた攻撃を検査する

AISVS Verification Level: 2

学習資料：[C2.2 Content & Policy Screening](../../../learning/c02-input-validation/v1.0-c2.2-content-policy-screening.md)

## Upstream basis

AISVS `v1.0-C2.2.3`は、画像・動画・音声等の非テキスト入力について、
敵対的な攪乱、ステガノグラフィによる隠蔽、隠れた／埋め込まれた内容、
既知の攻撃パターンを検査することを求める。対応Researchは、画像内の文字、
縮小後に現れる内容、低コントラストの指示、音声に隠れた命令等を論じる。
OCR、文字起こし、再エンコード、マルチモーダル分類等は検討手段であり、
特定製品・ツール・手法の採用をNormative本文は要求しない。

## Interpretation

Modelが実際に受け取る非テキスト入力について、受け付ける形式と変換経路を把握し、
その形式で成立し得る隠蔽・攪乱・既知攻撃を検査する。アップロード時の元Fileだけでなく、
Resize、Frame抽出、音声変換、OCR／文字起こし等の後にModelへ渡る表現も確認する。
元Fileを調べても、変換後にだけ見える攻撃を見逃すなら十分な検査ではない。

検査は「すべての隠し情報がない」という証明ではない。対象形式、検出できる攻撃族、
検査できない成分とその扱いを明示し、既知の代表的な攻撃を再現可能な試験で確認する。
Normative本文はC2.2.4と異なり、一律の遮断結果を明記しない。発見後の拒否・隔離・
確認等は製品のPolicyで決めるが、検査の存在だけで危険な内容の利用を無条件に許してよい
という意味ではない。下流のAction認可は別の保証である。

## Security objective

Text欄だけを検査し、画像・動画・音声の隠れた内容をModelが解釈してしまう
抜け道を減らす。非テキストInputを信頼済みInstructionに昇格させないための
入力側の観測能力を確立する。

## Applicability

画像・動画・音声その他の非テキストDataを、Model Context、Embedding、検索Index、
Tool処理、またはAgentの判断材料へ取り込むApplicationに適用する。
User添付だけでなく、RAG文書、Web取得、Tool出力、MCP Resource等から
非テキストが入る経路も対象にする。製品が受け付けない形式は対象外とできるが、
実際のDecoder、Fallback、埋め込みFile経由で入らないことを確認する。

### Non-applicability

非テキストInputを一切受け付けず、派生する画像・音声・動画もModelや後続処理に
届かないことを経路で示せるApplicationには直接適用しない。
UIで添付を禁止しただけでは、APIや検索資料からの到達を除外できない。

## Scope and assumptions

- 「検査」は形式ごとのRelevantな攻撃に対する観測・判定を意味し、任意の
  ステガノグラフィを完全発見できるとの主張ではない。
- OCRは視認可能・抽出可能なTextに、文字起こしは認識できる発話に有効だが、
  Pixelの攪乱、Metadata、非可聴域、Frame間の変化等を網羅しない。
- Metadata除去や再エンコードは一部の隠蔽経路を減らし得るが、
  画像・音響Signal中の攻撃不存在を証明しない。
- 変換後にModelへ入る表現が元Fileと異なる場合、検査対象と実Payloadの対応を記録する。
- 未対応形式やSize超過等で検査できない場合、その入力を「検査済み」と記録しない。

## Assets, actors, identities, and trust boundaries

保護対象はModel Contextの指示境界、利用者の作業意図、非テキスト由来の
判断・Actionの完全性。攻撃者はFile内容、画素、音響Signal、Metadata、
埋め込みObject等を操作し得る。Trust Boundaryは、外部MediaがDecoder・
前処理を通ってModelまたは後続Componentの解釈対象になる地点。
検査器が見たRepresentationと、Modelが見たRepresentationの差が重要な攻撃面になる。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 到達可能な非テキスト形式・入力経路・前処理と、Model等が実際に消費する表現を特定できる。 |
| SP-2 | 各Relevant形式で、敵対的攪乱、隠蔽・埋め込み内容、既知の攻撃パターンに対する検査対象と手段を説明できる。 |
| SP-3 | 代表的な既知攻撃と正常例を実際の処理経路に通し、検査結果・見逃し・誤検知を観測できる。 |
| SP-4 | 前処理、Fallback、未対応形式で未検査の内容を「検査済み」と誤認せず、検査結果を対象Payloadに結び付ける。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 画像をOCRし、抽出Textだけを検査する | 一部の可視Textを調べられる。Pixel変化、Metadata、縮小後の別像等まで検査した証拠ではない。 |
| 音声を文字起こしし、Transcriptだけを分類する | 認識した発話の検査にはなる。文字化されない音響成分は別に評価する。 |
| 元画像を検査した後、Model側で縮小して別の文字が現れる | Modelが見た表現とのGapがあり、SP-4の失敗。 |
| 画像のMetadataを削除した | 一つの緩和手段。画像内容の隠蔽攻撃がない証明ではない。 |
| Textと画像を個別に検査したが、組合せで攻撃が成立する | C2.2.4の複合形式攻撃として別途評価する。 |
| 検査器が不審な指示を見つけたが、Action認可がない | 入力検査の所見とAction認可失敗を分けて扱う。 |

## Threat and failure-mode rationale

画像中の小さな文字や低コントラストの指示、変換によって現れる内容、
動画の短いFrame、音声の聞き取りにくい成分等は、Textだけの検査を迂回し得る。
File FormatやMetadataに埋め込まれた内容も、抽出・変換過程で後続へ流れる可能性がある。
攻撃者が複数形式を連携させる場合はC2.2.4で別に評価する。
特定の外部Threat IDへのMappingは未評価であり、Catalogには追加しない。

## Verification

### Architecture and configuration review

各Input経路の許可形式、Decoder、Size制約、Media変換、Modelへ渡す最終Payload、
検査器のPlacementと観測範囲を図示する。Image、Video、Audioごとに
どの攻撃族をどの段階で検査するか確認し、Provider内で暗黙に行う変換も
可能な範囲で把握する。検査不能時の記録と下流処理を確認する。

### Positive verification

正常な画像・動画・音声を用途別に投入し、受け入れ可能なFormatや品質が
不当に破壊されないこと、検査結果が最終Payloadへ結び付くことを確認する。
字幕、画面内Text、環境音など正当な要素を誤検知した場合の影響も測る。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 画像中に細字・低コントラストの指示を配置する | 対象Image経路の検査で観測・判定できる範囲を測り、OCRのみのCoverageを過大表示しない。SP-2, SP-3 |
| N-2 | Resize／Crop等の後にだけ意味が現れる画像を投入する | Modelへ渡す変換後Representationを検査し、元Fileの判定を流用しない。SP-1, SP-4 |
| N-3 | Metadata、埋め込みObject、既知のSteganography手法を含むFileを投入する | 実際に後続へ残るChannelと検査・除去の効果を観測し、未知手法への完全性を主張しない。SP-2, SP-3 |
| N-4 | 動画の一部Frame、字幕、音声の一部に攻撃内容を埋める | Frame抽出・音声処理・Model入力のどこで見えるかを測定し、未観測部分を明示する。SP-1〜SP-3 |
| N-5 | 文字起こしで欠落する音響成分や変形音声を投入する | Transcript検査のみを全音声検査とせず、対象攻撃への検査能力と限界を記録する。SP-2, SP-3 |
| N-6 | 未対応Format、Size超過、検査器Timeoutを発生させる | 未検査を安全・検査済みと扱わず、Policyで定めた経路へ送る。SP-4 |
| N-7 | User添付以外のRAG・Tool・MCP Resourceから同じMediaを渡す | 実際に到達する経路を検査対象に含め、UIだけの検査で済ませない。SP-1, SP-4 |

### Failure conditions

到達可能な非テキスト形式を棚卸ししていない、Text抽出だけで元Media全体を
検査したと主張する、既知の代表的攻撃を実経路で試していない、または
前処理・Fallback後の未検査内容を検査済みとしてModelへ渡す場合はFail。
検査できる範囲を明示したうえで、対応できない攻撃族を残余Riskとして
扱うことと、検査が存在しないことは区別する。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Media Flowと変換一覧 | Application Owner | 許可Format、Decoder、Input経路、Model最終Payload | 経路・Model変更時 | 機密Mediaを含めずRevision保持 | 検査対象とModelが見る表現の対応を追える。 |
| Version付き試験Corpus | Security／Test Owner | 正常例、形式別の隠蔽・攪乱・既知攻撃 | Threat・Provider変更時 | 合成Fileを使用し期待結果を保持 | 検査能力と未観測Channelを再現できる。 |
| 実経路の試験結果 | Test Harness | N-1〜N-7、変換後Payload、検査結果 | Release・検査器変更時 | 原文やMediaの保持を最小化 | 各検査結果と実際に消費したPayloadが対応する。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C2.1.3` | Model誘導を狙う入力のPrompt Injection検査とFlag時遮断。本Controlは非テキスト特有の隠蔽・攪乱を扱う。 |
| `v1.0-C2.2.1` | Promptの四区分Content Screening。Media由来Textの分類だけでは、元Mediaの隠蔽検査を満たさない。 |
| `v1.0-C2.2.2` | 非対応言語の分類評価。画像内・音声内Textの言語問題も起き得るが、Media検査の代替ではない。 |
| `v1.0-C2.2.4` | 複数形式を組み合わせた攻撃の検出・遮断。個別Mediaの検査だけでは足りない。 |

## Known limitations and uncertainty

未知のSteganographyや適応的な敵対的攪乱を全件検知する実用的な保証はない。
OCR・文字起こし・再エンコードはそれぞれ異なる成分を失う可能性がある。
Provider内部の前処理を完全に観測できない場合、実Payloadとの一致に不確実性が残る。
その範囲を明示し、危険なActionは入力検査以外の境界でも制限する。
`verifiable`は本Artifactの成熟度であり、実製品の非テキスト安全性を保証しない。

## References

- [AISVS v1.0 C2 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md)
- [AISVS v1.0 C2.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-02-Content-Policy-Screening.md)
- [C2 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-30 | C2.2.3初版。非テキストの検査能力とModelが消費する変換後表現の境界を整理 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
