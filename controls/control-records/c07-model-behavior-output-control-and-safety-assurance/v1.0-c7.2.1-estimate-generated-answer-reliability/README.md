---
title: "生成回答の信頼性をConfidence推定で評価する"
versioned_id: "v1.0-C7.2.1"
requirement_id: "C7.2.1"
verification_level: 2
family_id: "C7"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-02-Hallucination-Detection.md"
last_verified: "2026-09-30"
maturity: "verifiable"
mapping_assessment_refs: []
---

# 生成回答の信頼性をConfidence推定で評価する

AISVS Verification Level: 2

学習資料：[C7.2 Hallucination Detection & Mitigation](../../../learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.2-hallucination-detection-and-mitigation.md)

## Upstream basis

AISVS `v1.0-C7.2.1`は、Confidence推定の方法を用いて生成回答の信頼性を
評価することを求める。対応Researchは、もっともらしい誤回答、
Model自身の自信表現と正しさの乖離、用途別の校正、既知の誤回答を含む
評価を論じる。Log Probability、根拠との照合、複数Sample、別の判定器等は
候補であり、特定方式や性能値をNormative本文の必須条件にしない。

## Interpretation

Applicationが利用する生成回答について、「何が信頼できると判断する対象か」
（事実、計算、引用、手順等）を用途ごとに定め、その回答に結び付いた
Confidence推定結果を得る。単にModelが「確信している」と文章で述べること、
あるいは流暢であることを評価方法の代わりにしない。

推定方法は、代表的な正答・誤答・判断不能の事例で試し、実際の正しさや
根拠支持との関係を確認する。出力されたScoreだけで真実を証明できない。
Repository interpretationとして、回答全体の単一Scoreでは重大な誤りを
隠し得る用途では、主張単位の評価や最も弱い根拠の観測を検討する。
ただし、全回答の主張分解を一律の必須実装とはしない。

本Controlは**信頼性の評価**を対象とする。低Confidence時の自動遮断・Fallbackは
C7.2.2、Policy上のHigh-risk回答に対する追加検証はC7.2.3で独立に確認する。
信頼性が高くても、Tool実行やデータ公開の認可は別の保証である。

## Security objective

根拠の乏しい、古い、捏造された回答が流暢さだけで信頼される失敗を減らす。
誤答の可能性を用途に応じて観測できるようにするが、すべての回答の
真実性や安全性を保証しない。

## Applicability

Model生成の回答をUser、Agent、Tool、業務Workflowが利用するApplicationに
適用する。特に事実確認、RAG要約、検索、手順提示、判断支援等では
何を正答・支持ありとみなすかを定義する。創作等の用途でも、
評価対象としない性質を明示し、回答の信頼性を測ったと誤認させない。

### Non-applicability

Model生成回答を取得・利用しない決定論的処理は直接対象外。
利用者に「AIの回答」と表示していることだけでは、回答の信頼性評価を
省略する理由にならない。

## Scope and assumptions

- Confidenceが何の信頼性を推定するかを定義する。事実性、与えた資料との整合、
  手順の適用可能性は同じ性質ではない。
- 検証用の正答・誤答Corpusは、対象Domain、言語、Model／Prompt設定、
  RAG資料のVersionを代表する必要がある。上流は普遍的な閾値を指定しない。
- ModelのToken確率、複数回答の一致、Citationの存在、別LLMの同意等は、
  単独では正しさの証明にならない。選んだ方法の限界を試験する。
- Confidence推定器が使用不能・未評価の場合、「高Confidence」として補完しない。
  その際の公開・Fallback判断はC7.2.2等の別保証と区別する。

## Assets, actors, identities, and trust boundaries

保護対象は利用者の判断、下流Workflowの入力品質、根拠への信頼。
攻撃者は資料やPromptへ虚偽情報を置き得る。攻撃者がいなくても、Modelは
架空の事実や古い手順を自信ありげに生成し得る。Trust Boundaryは、
Modelの回答がApplicationの評価器へ渡り、その評価結果が公開・利用判断へ
伝えられる地点。Model自身の自己申告と、独立した評価結果を区別する。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 用途ごとに「回答の信頼性」が指す性質と評価対象の出力経路を定義している。 |
| SP-2 | 生成された回答に結び付いたConfidence推定方法と結果があり、単なる流暢さやModelの自己申告を未検証で用いない。 |
| SP-3 | 代表的な正答・誤答・判断不能例で推定結果と実際の正誤／根拠支持の対応を評価し、誤った高Confidenceを含む限界を把握する。 |
| SP-4 | Model、Domain、資料、Prompt等の変更後も、以前の校正結果を無条件に現行の信頼性証拠としない。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 回答に「確実です」と書かれている | Modelの自信表現であり、信頼性評価の証拠ではない。 |
| 信頼性Scoreがあるが、既知の誤答を高く評価し続ける | Scoreの存在だけでは実効性を示せない。方法と校正を見直す。 |
| 回答が検索文書を引用する | Citationの存在だけで主張の支持を示せない。C7.4の出典保証も別に確認する。 |
| 低Confidenceでも元回答をUserへ返す | 本Controlの評価と、C7.2.2の遮断・Fallbackを別々に判定する。 |
| High-risk回答が高Confidenceなので追加確認しない | C7.2.3の別保証。Confidenceと誤答時のImpactは別軸。 |
| 正しい手順だがUserには実行権限がない | 信頼性と認可は別。高Confidenceは権限を与えない。 |

## Threat and failure-mode rationale

Modelは架空の出典、存在しない対象、古いVersionの手順等を自然な文章で
提示し得る。単なる流暢さや自己評価に頼ると、誤回答を高く信頼して
Userや後続処理が採用してしまう。ResearchはConfidence推定方法を複数挙げるが、
手法の有効性はDomainと評価Corpusに依存する。外部Threat IDへの厳密な
Mappingは未評価とし、Catalogには追加しない。

## Verification

### Architecture and configuration review

どの出力経路を何の性質について評価するか、推定器への入力、回答との結び付け、
校正Corpus、Model／Prompt／Domain変更時の再評価を確認する。
Modelの自信表現やCitationの有無だけをConfidenceと見なしていないかを確認する。
推定器の出力が後続にどう渡るかは記録するが、本Controlだけで
遮断・Fallbackの動作をPass条件にしない。

### Positive verification

根拠で支持される回答や正しい計算を投入し、推定結果が低信頼例と
区別されるか測る。正答をすべて低Confidenceとするだけの方法も、
有用な信頼性評価とは言えないため誤拒否・判断不能も記録する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 存在しない対象、捏造された日付・出典、古いVersionの手順を回答させる | 回答に対応する推定結果を観測し、誤答を高く評価する割合を測る。SP-2, SP-3 |
| N-2 | もっともらしいが、承認済み根拠の一部に反する回答を与える | 表現の流暢さやCitationの有無でなく、実際の根拠支持とのずれを評価する。SP-1〜SP-3 |
| N-3 | 誤答を複数回同じように生成させ、またはModelに「自信がある」と言わせる | 一致・自己申告を正しさと同一視せず、選んだ推定法の盲点を記録する。SP-2, SP-3 |
| N-4 | 会話の後続Turnで根拠のないUserの説得や新しい正当な根拠を追加する | Turnごとの推定挙動を測り、説得だけで信頼性が上がる失敗と根拠追加への反応を分ける。SP-3 |
| N-5 | Model、Prompt、RAG資料、対象Domainを変更する | 旧校正を流用せず、影響範囲の再評価を行う。SP-3, SP-4 |
| N-6 | 推定器が失敗・Timeoutし、回答だけが生成される | 未評価を高Confidenceとして扱わず、評価欠落を観測できる。SP-2 |

### Failure conditions

評価対象や方法が定義されていない、Modelの自己申告・流暢さだけを
信頼性評価とする、Scoreが回答と結び付かない、または実際の正誤に照らす
評価がなくScoreの意味を説明できない場合はFail。
代表的な誤回答を高く評価することが判明した場合は、性能限界と
用途上の影響を記録して方法を見直す。一つの見逃しだけで万能な検出を
要求するのではなく、実効的な評価であるかを判断する。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 信頼性の定義と評価経路 | Application／Policy Owner | Domain、回答種別、Model出力経路 | 用途・経路変更時 | 仕様Revisionを保持 | 何を推定し、何を推定しないか説明できる。 |
| Version付き評価Corpus | Security／Test Owner | 正答、誤答、判断不能、後続Turn | Domain・資料変更時 | 合成・匿名化Dataと期待根拠を保持 | 誤った高Confidenceと過剰低Confidenceを再現できる。 |
| 推定・校正結果 | Test Harness | N-1〜N-6、Model／推定器Version | Release・Model変更時 | 機密回答を最小化し改変を検知できる形で保持 | Scoreと正誤／根拠支持の関係、限界を追える。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C7.2.2` | 閾値未満を自動で遮断・Fallbackする。本Controlは信頼性の評価方法を問う。 |
| `v1.0-C7.2.3` | High-risk回答への追加検証。信頼性が高くてもImpactは減らない。 |
| `v1.0-C7.4.2`／`v1.0-C7.4.3` | Retrieval Metadata由来の出典と、主張からChunkへの追跡。Citationだけで正しさを保証しない。 |
| `v1.0-C9.5.1` | Tool・引数の認可。正しい回答でもActionは別途許可が必要。 |

## Known limitations and uncertainty

Confidence推定は確率的で、評価Corpusや対象Domainに偏り得る。
複数Modelが同じ誤情報を共有すれば一致しても間違う。Token確率や
自然言語の自信表現も、事実性と直結しない。根拠文書自体が古い・
汚染されている場合は、その上での高Confidenceも危険である。
`verifiable`は本Artifactの成熟度であり、製品の回答精度や無害性を示さない。

## References

- [AISVS v1.0 C7 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md)
- [AISVS v1.0 C7.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-02-Hallucination-Detection.md)
- [C7 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-30 | C7.2.1初版。信頼性推定の実効性と、閾値遮断・高Impact追加検証の境界を整理 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
