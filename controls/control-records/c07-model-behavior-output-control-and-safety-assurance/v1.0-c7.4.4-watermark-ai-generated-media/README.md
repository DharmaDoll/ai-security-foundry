---
title: "生成MediaにAI生成を示すWatermarkを付けて検証する"
versioned_id: "v1.0-C7.4.4"
requirement_id: "C7.4.4"
verification_level: 3
family_id: "C7"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-04-Source-Attribution-Citation-Integrity.md"
last_verified: "2026-10-03"
maturity: "verifiable"
mapping_assessment_refs: []
---

# 生成MediaにAI生成を示すWatermarkを付けて検証する

AISVS Verification Level: 3

学習資料：[C7.4 Source Attribution & Citation Integrity](../../../learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.4-source-attribution-and-citation-integrity.md)

## Upstream basis

AISVS `v1.0-C7.4.4`は、生成MediaにAI生成であることを示すWatermarkが
付いているか検証する要件で、Verification Level 3である。対応Researchは
機械可読な来歴情報と不可視Watermarkの併用、画像・音声・動画・Textでの
検出、切抜き・再圧縮等の変換に対する頑健性を検討例として挙げる。
ただしNormative本文はC2PA、不可視方式、二層構成、特定製品、または
法令への適合を一律に要求していない。Researchの法令解説もこのControlの
適合判定へ自動的には取り込まない。

## Interpretation

対象となる生成Mediaの配布物に、定義した方法でAI生成を識別できる
Watermarkを付与し、その標識を実際の受渡し先で検出できることを確かめる。
生成時に設定しただけでは足りず、変換・Export・共有を経た最終Artifactで
何が判定できるかを示す。Watermark方式の検出条件・誤判定・除去可能性を
明示し、利用者へ「何を証明する標識か」を過大に伝えない。

例えば画像生成器が内部ファイルだけへWatermarkを付けても、配布時の再圧縮で
消えるなら、受取人が確認できるAI生成表示にはならない。一方、Watermarkの
検出は、その方式の信頼前提の下で「AI生成として標識された」ことを示す。
標識だけで特定事業者の発行、ファイルの非改変、内容の真実性、すべての
AI生成物を見分ける能力までは保証しない。

## Security objective

生成Mediaを無標識の人間制作物・実写記録として誤認する可能性を減らし、
受取人がAI生成の表示を機械的または可視的に確認できるようにする。

## Applicability

この製品・Systemが生成または生成後処理して配布する画像、音声、動画等の
Media経路に適用する。ResearchにはTextも含まれるが、Normativeの「media」が
どのText形式までを指すかは明示されていない。Textを対象に含める判断と
方式の実効性は、製品の出力形式・利用目的ごとに記録する。
Preview、Download、API、SNS向けExport等、実際の配布経路を対象にする。

### Non-applicability

AI生成Mediaを作成・配布せず、単に第三者のMediaを受け取るだけの経路には
直接適用しない。生成機能があるのに配布時の標識が失われる場合はN/Aではない。
外部サービスが生成を担当する場合も、自製品がその成果物を配布するなら、
当該経路の保証範囲と責任分界を評価する。

## Scope and assumptions

- 「Watermark」の方式・検出器・検証条件を特定する。画面上の「AI生成」
  表示だけで、配布Artifactにも検証可能な標識が残ると推定しない。
- 署名付き来歴Metadataは、署名者・ManifestとArtifactの関係を検証できる
  場合に別の有用な保証を与え得るが、それだけをWatermarkと同義にしない。
- 加工や再録音、Screenshot、再生成など、標識が失われ得る変換を列挙する。
  あらゆる敵対的変換への耐性は要求・主張しない。
- 「prove」という上流表現の保証範囲は方式依存である。検出が意味する
  出自、偽陽性・偽陰性、KeyやDetectorへの信頼を分けて扱う。

## Assets, actors, identities, and trust boundaries

保護対象はMediaのAI生成属性に関する受取人の判断。Actorsは生成器、
Watermark付与Component、変換・配布Component、Detector運用者、受取人、
Mediaを改変・再配布する第三者である。攻撃者は標識を削除・弱体化したり、
検証不能な「AI生成」表示を付けて真正な標識と誤認させたりし得る。

Trust Boundaryは、生成器から付与処理、付与済みArtifactから配布用変換、
受取人のDetector判定までにある。生成時の内部状態やUI Labelを、受取人が
得たファイルでの検証結果に置き換えない。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 対象Mediaの全ての生成・配布経路で、方式を定めたAI生成WatermarkがArtifactに付与される。 |
| SP-2 | 最終配布Artifactを定義済みDetector・信頼前提で検査すると、Watermarkを確認できる。 |
| SP-3 | 製品が通常行う変換と想定される共有経路について、検出が維持される範囲と失われる範囲を試験・記録し、失われる経路を無条件に保証済みと扱わない。 |
| SP-4 | 検出結果の意味をAI生成表示の範囲に限定し、検証できない標識や不明な結果を発行者認証・非改変・真実性の証拠として扱わない。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 画面だけに「AI生成」と表示し、DownloadしたMediaには標識がない | 配布ArtifactのWatermarkを示せずFail。 |
| 生成直後は検出できるが、標準Exportで必ず消える | 最終配布経路の保証が成立せずFail。 |
| Watermarkを検出できるが、発行者や内容が正しいかは不明 | 本ControlのAI生成標識として評価する。発行者認証・内容の事実性は別保証。 |
| 署名付き来歴Manifestだけを添え、Watermark付与は確認できない | 来歴検証は有益でも、Watermarkの本Requirementを満たすとは断定しない。 |
| 攻撃者が意図的な大幅加工でWatermarkを除去できる | 直ちに全方式をFailとしない。想定変換での頑健性と残余リスクを明示する。 |
| 第三者の未標識Mediaを受け取る | 標識の不存在だけで「AI生成ではない」と断定しない。 |

## Threat and failure-mode rationale

無標識または検証不能な合成Mediaは、現実の撮影・録音等と取り違えられ得る。
生成元でWatermarkを付けても、配布Pipelineが標識を落とせば、受取人には
保証が届かない。逆にWatermark検出を万能な真正性証明として提示すると、
別の誤認を生む。外部Threat IDへの厳密なMappingは未評価とする。

## Verification

### Architecture and configuration review

生成形式、付与地点、使用する方式・Detector、配布Format、変換、外部
Processor、各配布先を列挙し、受取人が検査するArtifactまで追う。
付与失敗時の処理と、検出用Key・Detector更新、誤判定の評価方法を確認する。
可視表示・不可視信号・署名付き来歴情報を混同せず、それぞれ何を保証するか
明示する。

### Positive verification

各対象Formatの合成Mediaを生成し、通常のPreview、Download、API、Export
を経たArtifactを取り出して、定義済みDetectorでAI生成Watermarkを検出する。
正常な変換の後でも、定めた検出条件を満たすことを確認する。生成していない
Mediaを対照群に用い、誤検出も測る。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 付与処理を失敗させたまま生成Mediaを配布する | 未標識の配布を検知し、保証済みとして公開しない。SP-1, SP-2 |
| N-2 | Previewには標識があるが、Download・再圧縮・Transcodeで消す | 最終Artifactの検出試験で欠落を発見する。SP-2, SP-3 |
| N-3 | Media外のUIに可視Labelだけを付け、配布Artifactには標識を残さない | Watermark検出の成功として扱わない。SP-2, SP-4 |
| N-4 | 非AI生成の対照Media、または偽の「AI生成」Labelを検査する | 誤判定と検出限界を測り、根拠のないAI生成判定をしない。SP-4 |
| N-5 | Crop、Screenshot、再録音等の敵対的・境界的な加工を試す | 成否と方式の限界を記録し、全変換に耐えると主張しない。SP-3, SP-4 |

### Failure conditions

対象となる生成Mediaの配布経路にWatermarkがなく、最終Artifactで指定条件に
従って検出できない、または標準変換で失われる事実を隠して「保証済み」と
扱う場合はFail。Detectorがない、検証条件が不明である場合も有効性を
示せない。敵対的な全加工への耐性や、発行者の暗号学的証明、内容の
正確性がないことだけを本RequirementのFail条件にしない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 付与・配布Data Flowと方式仕様 | Generator／Media Pipeline Owner | 生成、変換、全配布経路 | Format・Processor・方式変更時 | 秘密鍵・検出Keyを公開しない | 付与地点、Detector、対象・例外が明確。 |
| 合成Mediaの検出・対照試験 | Test Harness／評価担当 | 正常、欠落、標準変換、誤検出 | Release・方式更新時 | 合成Materialを使用 | 最終Artifactで検出結果を再現でき、欠落・誤判定が見える。 |
| 変換耐性・残余リスク評価 | Media／Security Owner | 想定加工と共有経路 | 配布経路変更時 | 生産用Key・非公開Sampleを保護 | 対応する変換範囲と限界が明示される。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C7.4.1`〜`v1.0-C7.4.3` | RAG回答の出典表示・来歴・主張支持。生成MediaのAI生成標識は別の枝。 |
| `v1.0-C7.3.4` | 出力に隠れた・誤認を誘うContentを検査する。Watermarkの付与・検出そのものを代替しない。 |

## Known limitations and uncertainty

Watermarkは除去・劣化・偽装され得る。未検出だから人間制作物とは言えず、
検出したから特定者が作った、無改変である、内容が真実であるとも言えない。
署名付き来歴とWatermarkを組み合わせると別の保証を補える場合があるが、
Researchの二層構成や法令に関する記述を本Requirementの一律Pass条件と
しない。Textを含む「media」の境界、方式間の互換性、Detectorの誤判定、
敵対的加工に対する耐性は製品ごとに評価が必要である。`verifiable`は本Artifact
の成熟度であり、実製品の標識が機能した証拠ではない。

## References

- [AISVS v1.0 C7 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md)
- [AISVS v1.0 C7.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-04-Source-Attribution-Citation-Integrity.md)
- [C7 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-10-03 | C7.4.4初版。生成・配布経路でのWatermark検出と保証の限界を分離 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
