---
title: "複数の入力形式にまたがる連携攻撃を検出・遮断する"
versioned_id: "v1.0-C2.2.4"
requirement_id: "C2.2.4"
verification_level: 3
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

# 複数の入力形式にまたがる連携攻撃を検出・遮断する

AISVS Verification Level: 3

学習資料：[C2.2 Content & Policy Screening](../../../learning/c02-input-validation/v1.0-c2.2-content-policy-screening.md)

## Upstream basis

AISVS `v1.0-C2.2.4`は、複数の入力形式をまたぐ連携攻撃を検出し、遮断することを
求める。正規要件は、画像中の隠しPayloadとTextのPrompt Injectionの組合せを例示する。
対応Researchは、個別形式では無害に見えるFragmentが合成後に攻撃となること、
OCR・文字起こし・複合形式の評価やSession単位の相関を検討することを論じる。
Researchの特定Toolや「すべてのSessionに相関Engineを必須とする」といった
実装案をNormative本文の条件に読み替えない。

## Interpretation

同じModel応答、Agent判断、Tool実行等に使われるText・画像・音声・動画の
**組合せとしての意味**を評価し、単独入力では検出できない連携攻撃を見つけて遮断する。
各形式の検査を置いただけ、または連携攻撃をLogに残すだけでは足りない。

評価単位は、実際に複数形式が統合されるRequest、Model Context、会話履歴、
Agent Step等とする。一つのRequestで完結しない場合も、前段のMediaから抽出した
内容が後続Turnへ残り、そこで別形式と結び付くなら、その合成地点を対象にする。
無関係な全Sessionを一律に連結することは求めない。

「遮断」は攻撃が有効な下流へ届く前に、該当する合成InputのModel投入、
後続Stepへの引継ぎ、またはTool／外部Actionへの伝播を止めることを指す。
どの地点で止めるかはArchitectureによるが、検出後に同じ攻撃をRetryや
Fallbackで再投入する構成をPassとはしない。必要な認可・承認は別保証であり、
検出器だけを高Impact Actionの認可境界にしない。

## Security objective

別々の形式へ分割した指示やPayloadが、合成時に初めて危険な意味を持つ
抜け道を減らす。個別検査の成功を全体の安全性と誤認せず、連携攻撃の
検出結果を実際の遮断へ結び付ける。

## Applicability

複数の入力形式を同じModel判断または下流処理へ渡すApplicationに適用する。
例としてTextと添付画像、音声と画面、動画と字幕、RAG由来の画像とUserのText、
Toolが返したMediaとAgentの後続Promptがある。異なる経路から来ても、
同じ判断に利用されるなら対象となる。

### Non-applicability

単一の入力形式しか受け付けず、他形式の取得・派生・統合もなく、
複数形式が同じ判断へ到達しないことを経路で示せる場合は直接対象外。
UIで画像添付を禁止しただけでは、RAG、Tool、MCP Resource、音声文字起こし等の
経路を除外できない。単一形式内の隠蔽攻撃はC2.2.3等で評価する。

## Scope and assumptions

- 「複数形式」はText、画像、音声、動画等の異なる入力Typeを指す。
  同じTypeのFileが複数あるだけでは、この要件の代表的な連携条件とはしない。
- 検出対象は、適用Productで到達可能な形式・合成順序・実際のContextに基づく。
  すべての未知の組合せを完全検出できるとは主張しない。
- OCR、文字起こし、個別Classifierの結果は材料になり得るが、失われる画素・音響・
  時間的な情報がある。抽出Textだけで複合形式全体を評価したことにはならない。
- 攻撃のFragment、判定、遮断対象の合成Inputを同じRequest／Step／Contextへ
  結び付けられることが検証の前提となる。

## Assets, actors, identities, and trust boundaries

保護対象はModelへの指示境界、Userの正当な目的、Agent／Toolが扱うDataと権限。
攻撃者はTextとMediaの一方または両方、あるいは検索資料・Tool応答へ
分割Payloadを置き得る。Trust Boundaryは、異なる形式の内容がDecoder・抽出器・
Context Builderを経て一つの判断材料になる地点と、その判断がTool等の
副作用へ進む地点。個々のFileの信頼性と、合成された指示の正当性を混同しない。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 同じ判断に寄与する入力形式・経路・合成地点を特定し、関連するFragmentを一つの評価対象へ結び付けられる。 |
| SP-2 | 個別には危険と判定されない場合も含め、形式間の意味の組合せから成立する代表的な攻撃を検出できる。 |
| SP-3 | 検出された連携攻撃は、該当する合成Inputや後続Actionへ伝播する前に遮断される。検知だけでは足りない。 |
| SP-4 | 変換、会話継続、Retry、Fallback等でも、元Fragmentと判定の対応を失って未評価の組合せを通さない。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 画像とTextをそれぞれ検査し、双方で「安全」と出る | 組合せの検出能力は示さない。攻撃が合成後に成立するなら別途評価する。 |
| 画像中の隠し指示だけで攻撃が成立する | 主にC2.2.3／C2.1.3の対象。別形式との連携が必要かを確認する。 |
| Textの指示とMediaの内容を合わせると危険な操作になる | 本Controlの中心例。合成地点での検出と遮断を確認する。 |
| 連携攻撃を検出してAlertを送るがModelへ渡し続ける | 遮断しておらずFail。 |
| 検出されたInputは止まるが別経路で同じ合成PayloadをRetryする | 遮断の迂回でFail。 |
| Toolの権限Policyが攻撃後の操作を拒否する | Blast Radiusを下げる重要な別保証。連携攻撃の検出能力の代替ではない。 |

## Threat and failure-mode rationale

攻撃者は、Textに「別Mediaの指示を採用せよ」と書き、Mediaには隠し命令や
目的Dataを置くなどして、単体の分類器が全体の意図を見られない状況を作る。
Media側の内容が前処理で変わり、後続StepでTextと結び付く場合もある。
個別検査の結果だけをAND／ORで集計しても、関係性から初めて生じる攻撃を
見つけられない。外部Threat IDへの厳密なMappingは未評価とする。

## Verification

### Architecture and configuration review

各形式が取り込まれ、抽出・変換され、Request／Context／Agent Stepへ統合される
順序を追う。Detectorが個々のFragmentだけでなく関係性を見られるか、
判定がどの合成Inputに付くか、遮断がどの地点で発動するかを確認する。
前段の検査結果が履歴や要約を経て失われる場合、後段での再評価を確認する。

### Positive verification

通常の画像説明、動画要約、音声文字起こし、TextとMediaを組み合わせた
正当な作業を通し、組合せ自体を一律に攻撃と扱わないことを確認する。
正常例と攻撃例で、検出結果と遮断対象が正しいRequest／Stepに付くことを観測する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 単体では無害と判定されるTextと画像に攻撃のFragmentを分割し、合わせて一つの不正指示を成立させる | 組合せで検出し、合成Inputまたは有効な下流への伝播を遮断する。SP-1〜SP-3 |
| N-2 | 同じFragmentを音声＋Text、動画＋字幕等、製品が受け付ける別の形式対へ配置する | 到達可能な形式対で関係性を評価し、検出時に遮断する。SP-1〜SP-3 |
| N-3 | 画像をRAG／Toolから取得し、UserのTextと後続Stepで結び付ける | 入力源やTurnが違っても、同じ判断に使う地点で評価・遮断する。SP-1, SP-4 |
| N-4 | Media変換や要約の後にだけ攻撃Fragmentが見えるようにする | 最終的に利用する表現で再評価し、事前の単体判定を流用しない。SP-2, SP-4 |
| N-5 | Detectorが連携攻撃をFlagした状態でModel、Tool、Retry／Fallbackを監視する | Flagだけで継続せず、Policyで定めた遮断点を迂回できない。SP-3, SP-4 |
| N-6 | 内容が無関係な正常なText＋Mediaを同じ経路へ流す | 形式が混在するだけで一律に遮断せず、誤検知を測定する。SP-2 |

### Failure conditions

複数形式が同じ判断に届くのに単体の検査結果だけで安全と結論付ける、
代表的な連携攻撃を合成経路で試していない、検出してもLog／Alertだけで
Modelや後続Actionへ通す、またはRetry等で遮断を迂回できる場合はFail。
未知攻撃の完全遮断を求めるのではなく、評価した形式対と検出限界を明示する。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 複数形式のData Flow | Application Owner | 形式、入力源、抽出・変換、合成地点、遮断点 | Architecture変更時 | 機密Mediaを含めずRevision保持 | 同じ判断に寄与するFragmentの経路を追える。 |
| Version付き複合攻撃Corpus | Security／Test Owner | 対象形式対、単体・組合せ・正常例 | Threat／Model変更時 | 合成Dataと期待結果を保持 | 単体では無害、組合せでは攻撃となる差を再現できる。 |
| Detector・Gate試験結果 | Test Harness | N-1〜N-6、Model／Tool／Fallback経路 | Release・Policy変更時 | Payloadを最小化しRequest関連付けを保護 | 検出結果と実際の遮断を同じ合成Inputで確認できる。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C2.1.3` | Modelを誘導し得る入力のInjection検査とFlag時遮断。本Controlは複数形式へ分割された連携攻撃を扱う。 |
| `v1.0-C2.2.1` | Promptの四区分による内容分類と閾値超過時の投入前制御。単体PromptのScoreでは組合せの意味を評価しきれない。 |
| `v1.0-C2.2.3` | 各非テキスト入力内の隠蔽・攪乱を検査する。本Controlは異なる形式間の関係性と遮断を問う。 |
| `v1.0-C9.5.1` | Tool・引数の認可。連携攻撃の検出とActionの権限判断は独立した保証。 |

## Known limitations and uncertainty

実用的な複合形式Detectorは、形式、抽出品質、Context長、攻撃の分散範囲に
依存する。OCRや文字起こしで失われる成分、Provider内部の変換、異なるTurnに
分散したFragmentは検出しにくい。単体で無害な入力の組合せには正当な用途も
多いため、誤検知を含めて測る。確率的な検出器のみを権限判断にせず、
下流の決定論的認可と被害範囲制限を別途維持する。
`verifiable`は本Artifactの成熟度であり、製品適合や全連携攻撃の防止を示さない。

## References

- [AISVS v1.0 C2 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md)
- [AISVS v1.0 C2.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-02-Content-Policy-Screening.md)
- [C2 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-30 | C2.2.4初版。複数形式の関係性の検出と実際の遮断を分けて検証可能にした | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
