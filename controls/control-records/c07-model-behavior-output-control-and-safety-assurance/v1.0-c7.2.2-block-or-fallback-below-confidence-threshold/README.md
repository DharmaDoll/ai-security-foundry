---
title: "閾値未満の低Confidence回答を遮断またはFallbackする"
versioned_id: "v1.0-C7.2.2"
requirement_id: "C7.2.2"
verification_level: 2
family_id: "C7"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-02-Hallucination-Detection.md"
last_verified: "2026-10-01"
maturity: "verifiable"
mapping_assessment_refs: []
---

# 閾値未満の低Confidence回答を遮断またはFallbackする

AISVS Verification Level: 2

学習資料：[C7.2 Hallucination Detection & Mitigation](../../../learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.2-hallucination-detection-and-mitigation.md)

## Upstream basis

AISVS `v1.0-C7.2.2`は、Confidence Scoreが定義済み閾値を下回った場合、
Applicationが回答を自動的に遮断するか、Fallback Messageへ切り替えることを求める。
対応Researchは、信頼性評価の結果が警告だけで終わる失敗、用途に応じた閾値の
校正、誤受入れと誤拒否を論じる。Research中の製品、数値、特定の誤答型すべてを
Fallbackさせる提案は参考であり、Normative本文の一律必須条件ではない。

## Interpretation

対象回答に結び付いたConfidence Scoreと、その経路に適用する定義済み閾値を
Applicationが比較する。Scoreが閾値より低ければ、元回答をUserへ表示したり、
Tool／Workflowへ渡したりせず、自動で遮断またはFallback Messageへ切り替える。
Modelに「不確かなら答えないで」と頼むこと、低ScoreをLogやWarningに記録するだけ、
または人手による後追い確認だけでは、この要件の自動処理にならない。

Fallbackは元の低Confidence回答を別の表現で再掲するものではない。
「確認できない」等の代替メッセージへ切り替えたことを、実際の公開・利用Payloadで
確認する。Retryや別Modelで再生成する場合、新しい回答とそのScoreを改めて照合する。
定義済み閾値の境界値をどう扱うかはPolicyで明示する。原文は「閾値未満」と述べ、
等値の一律拒否を指定していない。

本Controlは**低Scoreが出た後のGate**である。Scoreが信頼性を適切に表すかは
C7.2.1、高Impact回答へ追加検証するかはC7.2.3で分けて評価する。
高Scoreを「真実」や「実行許可」と読み替えない。

## Security objective

信頼性評価が低いと判定した回答が、警告付きのまま公開・実行される失敗を防ぐ。
不確かな回答を元の形で流さないことが目的であり、全誤答の検出・除去を
保証するものではない。

## Applicability

Confidence Scoreを用いて生成回答を公開・利用するApplicationに適用する。
User表示、API応答、Agentの後続Step、Tool引数、Cacheからの再配信等、
元回答が到達し得る経路を対象にする。Streamingでも公開前に適用できる
判定単位と時点を説明する。

### Non-applicability

Model生成回答を取得・利用しない決定論的処理は直接対象外。
Confidence推定をまだ実装していないことは、Model回答を利用している
Applicationで本Controlを対象外にする理由にはならない。

## Scope and assumptions

- Scoreが何の信頼性を表すか、Score方向、適用Domain、閾値を明示する。
  AISVSは普遍的な数値閾値を指定しない。
- 閾値はC7.2.1の評価・校正結果と用途の許容Riskを踏まえて選ぶが、
  一つの閾値がすべてのDomainやModelに適切だと仮定しない。
- Scoreが欠ける、推定器がTimeoutする等は「閾値以上」と同じではない。
  未評価時の扱いを別Policyとして定め、低Score時のGateと混同しない。
- 公開済みのStreaming断片や実行済みActionは後から取り消せない。
  判定前にどの情報がどの境界を越えるかを確認する。

## Assets, actors, identities, and trust boundaries

保護対象はUserの判断、後続Workflowの入力品質、元回答に含まれる
誤った指示や事実。攻撃者はPromptや資料を介して誤回答を誘い得る。
攻撃者がいなくてもModelは低信頼回答を生成し得る。
Trust Boundaryは、Model回答と推定器のScoreをApplicationが結合し、
その回答をUser／Tool／後続Stepへ公開・利用する地点。許可判断を
Modelの自己申告ではなくApplicationのGateで行う。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 対象経路に、Scoreの意味・方向と定義済み閾値があり、回答に対応するScoreを照合できる。 |
| SP-2 | Scoreが閾値未満ならApplicationが自動で元回答を遮断するか、元回答を含まないFallbackへ切り替える。 |
| SP-3 | 低Scoreの元回答が、Streaming、Cache、API、Tool、後続Agent Step等の利用経路へ先に漏れない。 |
| SP-4 | Retry、再生成、Model切替、Policy変更時も、実際に利用する回答とScore・閾値の対応を保つ。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| Scoreが閾値未満だが警告を添えて元回答を表示する | 自動遮断・FallbackではなくFail。 |
| Scoreが閾値未満で「確認できない」に切り替え、元回答を送らない | 本ControlのPass根拠になり得る。推定器の品質は別に確認する。 |
| Scoreは高いが回答が事実と異なる | C7.2.1の評価・校正やC7.2.3等で扱う。高Score誤答だけで本Gateの動作をFailとはしない。 |
| Policy上High-riskだがScoreは閾値以上 | C7.2.3の追加検証が必要になり得る。高Scoreは省略理由にならない。 |
| 回答を最後に遮断するが、その前にStreamingで一部を表示する | 公開済み部分は撤回できず、SP-3を満たさない。 |
| Fallbackを再生成したが、新しい回答も低Score | 元回答と同様に評価・制御する。無限Retryや未評価公開をPassにしない。 |

## Threat and failure-mode rationale

推定器が不確かと判定しても、結果が実際の公開経路へ接続されていなければ、
誤回答は通常の回答と同様に消費される。警告や事後監査だけでは、
Userの判断やTool動作を取り消せない。Researchは数値矛盾、架空の引用等を
評価例に挙げるが、高Scoreで通るすべての誤答を本Requirementの
自動Fallback対象へ拡張しない。外部Threat IDとの厳密なMappingは未評価とする。

## Verification

### Architecture and configuration review

Confidence推定器、Scoreの方向、対象回答との結合、閾値の設定元とVersion、
比較を行うApplication Component、公開・利用Sinkを追う。
Streaming開始時点、Retry／Fallback、Cache、複数Modelの経路でも
同じGateが作用するか確認する。UIのWarning表示だけを遮断と数えない。

### Positive verification

閾値以上の代表的な回答を通し、Gateが不要なFallbackへ切り替えないことを
確認する。これはその回答の真実性や、他の出力安全・認可要件のPassを
意味しない。境界値の扱いはPolicyと一致させる。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Test Double等で対象回答に閾値未満のScoreを確実に付ける | 元回答がUser／API／Toolへ届かず、遮断またはFallbackが自動で発動する。SP-1〜SP-3 |
| N-2 | 閾値の直下、同値、直上のScoreを与える | 比較演算と等値の扱いが定義済みPolicyに一致する。SP-1, SP-2 |
| N-3 | 低Score回答をStreaming、Cache、後続Agent Stepへ流そうとする | いずれの利用経路でも判定前の断片や元回答を公開・利用しない。SP-2, SP-3 |
| N-4 | 元回答を遮断し、Fallback Messageへ元の未検証主張を引用する | 元回答の実質的な再掲を防ぐ。SP-2 |
| N-5 | Retry／再生成で回答が変わる、またはModel／閾値を切り替える | 新しい回答とScore・現行閾値を照合し、旧判定を流用しない。SP-1, SP-4 |
| N-6 | 推定器がTimeoutしScoreを返さない | 欠測を高Scoreとして扱わず、別Policyで定めた未評価時の経路へ進む。SP-1, SP-4 |

### Failure conditions

閾値がない、Scoreと回答が結び付かない、閾値未満でも元回答を警告付きで
公開・利用する、Fallbackが元回答を再掲する、または一部経路で
Gateを迂回できる場合はFail。閾値設定画面があるだけではPassとせず、
実際に利用するPayloadと遮断結果を観測する。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 閾値・Fallback Policy | Application／Policy Owner | Domain、Score方向、等値、対象Sink | 用途・閾値変更時 | Revisionと変更理由を保持 | 低Score時の決定が再現できる。 |
| 回答・Score・GateのData Flow | Application Owner | Model、推定器、公開・Tool・Cache経路 | Architecture変更時 | 機密回答を含めず境界を記録 | 判定が各利用経路の前にある。 |
| Gate回帰試験結果 | Test Harness | N-1〜N-6、Model／推定器Version | Release・Policy変更時 | 合成回答と期待結果を保持 | 閾値未満の元回答が利用されずFallbackが発動する。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C7.2.1` | 回答の信頼性を評価する方法とその妥当性。本ControlはScoreを公開判定へ結び付ける。 |
| `v1.0-C7.2.3` | High-risk回答への追加検証。閾値以上でも不要にはならない。 |
| `v1.0-C7.3.1` | 出力の有害内容検査。低Confidence遮断は有害性分類の代替ではない。 |
| `v1.0-C9.5.1` | Tool実行の認可。高ConfidenceだけでActionを許可しない。 |

## Known limitations and uncertainty

Confidence推定器が高く評価した誤答は、この閾値Gateだけでは通り得る。
閾値を厳しくすると正当な回答も多く拒否され、緩くすると誤受入れが増える。
Scoreの校正、Domain差、生成後の回答変更はC7.2.1と併せて確認する。
Fallbackは回答の代替であり、必要な根拠確認や人間の判断を常に置き換えるものではない。
`verifiable`は本Artifactの成熟度であり、製品の回答精度を示さない。

## References

- [AISVS v1.0 C7 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md)
- [AISVS v1.0 C7.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-02-Hallucination-Detection.md)
- [C7 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-10-01 | C7.2.2初版。閾値未満の自動GateとScore評価・High-risk追加検証を分離 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
