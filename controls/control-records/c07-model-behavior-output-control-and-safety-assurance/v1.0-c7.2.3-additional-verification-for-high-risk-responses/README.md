---
title: "高リスク回答に追加検証を行う"
versioned_id: "v1.0-C7.2.3"
requirement_id: "C7.2.3"
verification_level: 3
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

# 高リスク回答に追加検証を行う

AISVS Verification Level: 3

学習資料：[C7.2 Hallucination Detection & Mitigation](../../../learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.2-hallucination-detection-and-mitigation.md)

## Upstream basis

AISVS `v1.0-C7.2.3`は、PolicyによってHigh-riskと分類された回答について、
Systemが追加のVerification Stepを行うことを求める。対応Researchは、
誤答時の影響が大きい回答ではConfidence Scoreだけでは足りず、主張と根拠の照合、
決定論的確認、別経路の検証、専門家の確認等を検討すると述べる。
Researchにある特定の業種、複数Modelの合議、人間の承認を、すべての製品で
Normative本文の一律必須条件とはしない。

## Interpretation

何をHigh-risk回答とするかを製品のPolicyで定義する。その分類に該当した回答は、
Confidenceが高くても、通常の回答経路に加えて**別の検証Step**を通す。
追加Stepは、対象の主張や操作内容が何を根拠に正しいと判断できるかを
実際に確認できるものでなければならない。C7.2.1の同じScoreを再表示するだけ、
Citationの書式だけを確認する、またはModelに根拠なく「正しいか」と尋ねるだけでは、
追加検証の保証として弱い。

検証方式は用途に応じて選ぶ。例として、承認済みのVersion付き手順との照合、
Resource／値の決定論的照会、隔離環境での試験、根拠箇所を示す別の判定、
対象Systemを理解する人の具体的な確認がある。複数方式を常に必要とはしないが、
選んだ方式が元の回答と同じ誤りを無批判に共有しないかを評価する。

本Controlの必須の問いは、High-risk分類から実際の追加検証へ進むかである。
検証に失敗・判断不能となった回答を「検証済み」と扱わず、公開・利用の扱いを
別途定義したPolicyへ渡す。原文は検証失敗時の一律の拒否方法までは指定しない。
追加検証が通っても、Tool実行の認可や人間の承認が必要な場合は別に満たす。

## Security objective

Confidenceが高いという理由で、誤れば被害の大きい回答を無確認で
利用者や後続Systemへ渡す失敗を減らす。検証の質と残余Riskを明示し、
高リスクな誤答を通常回答と同じ扱いにしない。

## Applicability

回答が重大な判断・操作に利用される可能性のあるApplicationに適用する。
例として本番Systemの変更、医療・法務・金融に関わる助言、重要な設定変更があるが、
High-risk分類は業種名だけで固定しない。回答の用途、対象Resource、
利用者、下流の副作用をPolicyで考慮する。

### Non-applicability

Model生成回答を利用しない決定論的処理は対象外。
一部の回答をLow-riskと分類することは可能だが、Modelの自己申告や
UI上のラベルだけでHigh-risk用途を対象外にしない。High-riskの回答を
一件も生じないという主張には、実際の利用・下流経路の確認が必要となる。

## Scope and assumptions

- 「High-risk」は正答確率が低いことではなく、誤答したときのImpactを含む
  Policy上の分類である。ConfidenceとRiskを独立した軸として扱う。
- 追加検証で確認すべき主張・値・副作用は用途で異なる。AISVSは
  特定のEvidence Source、Verifier、Human Approvalを指定しない。
- 元回答を検証した後に内容が変更されたなら、検証結果を新しい回答へ
  無条件に流用しない。
- 検証の実施・結果を観測可能にすることと、あらゆる誤答を
  完全に見つけることは同義ではない。

## Assets, actors, identities, and trust boundaries

保護対象は重要な意思決定、Production Data、Userや第三者に生じる被害。
攻撃者はPromptや根拠資料に虚偽情報を混ぜ得る。攻撃者がいなくてもModelは
架空・古い・適用外の手順を高Confidenceで生成し得る。
Trust Boundaryは、Model回答がPolicyによるHigh-risk分類を受け、
追加Verifierへ渡り、その結果を踏まえてUser／Tool／Workflowに進む地点。
Risk分類と確認結果をModel自身の自己申告だけに委ねない。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 高リスク回答のPolicy条件と分類経路が定義され、実際の用途・下流Impactに適用される。 |
| SP-2 | High-riskと分類された回答はConfidenceの大小にかかわらず通常経路に追加したVerification Stepを通る。 |
| SP-3 | 追加Stepは対象の重要な主張・操作内容を具体的な根拠や別の検証方法で確認し、単なる同一Scoreの再利用で終わらない。 |
| SP-4 | 検証対象の回答、根拠、結果と、実際に公開・利用する回答が対応し、失敗・判断不能を成功として扱わない。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 回答はHigh-riskだがConfidenceが高い | 追加検証を省略できない。 |
| Confidenceが閾値未満で回答を遮断した | C7.2.2の保証。High-risk回答の検証経路が存在する証拠にはならない。 |
| 別LLMが根拠を示さず「正しい」と答えた | 追加Stepという形式だけでは保証が弱い。具体的な主張・根拠との対応を確認する。 |
| 承認済みの手順・対象Versionと主要な手順を照合した | 対象範囲を定めた追加検証のPass根拠になり得る。完全な正しさは別。 |
| 人間が承認Buttonを押したが、対象の主張や根拠を見ていない | 形式的な承認だけでは検証内容を示せない。人間承認そのものを一律必須とはしない。 |
| 追加検証に通ったTool実行指示が無権限である | Action認可はC5／C9等で別途強制する。 |

## Threat and failure-mode rationale

生成回答は流暢かつ高Confidenceでも、Version違い、根拠の読み違い、
存在しない対象、危険な操作順序を含み得る。被害が大きい用途では
同じConfidence Gateを通過したことだけでは十分でない。
Researchは独立した根拠を用いる確認を提案するが、どの方式が有効かは
用途とRoot Causeに依存する。外部Threat IDへの厳密なMappingは未評価とする。

## Verification

### Architecture and configuration review

High-riskを定義するPolicy、分類に用いる信頼できるContext、追加Verifierの入力と
根拠、結果の扱い、公開・Tool利用の順序を追う。High-risk分類が
回答本文やModelの自己ラベルだけで迂回できないか、Verifierが
単なるConfidence再表示や無根拠の追認になっていないか確認する。

### Positive verification

正当なHigh-risk回答を投入し、追加Stepが実施され、該当する根拠・対象Version・
操作条件が確認されることを観測する。Low-risk回答にはPolicyどおりの
通常経路が適用されることも確認し、High-risk処理を単なる全件拒否としない。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | High-risk用途の回答に高Confidence Scoreを付ける | Scoreにかかわらず追加Verifierが実行される。SP-1, SP-2 |
| N-2 | Model本文に「Low-risk」等と自己申告させ、実際の下流用途はHigh-riskにする | 信頼できるPolicy分類で追加Stepへ進み、自己申告で迂回しない。SP-1, SP-2 |
| N-3 | 正しいSource名を含むが、重要な数値・Version・操作順序が根拠と矛盾する回答を与える | Citationの存在では済ませず、対象の主張を確認し不一致を観測する。SP-3 |
| N-4 | 別Verifierへ同じ誤ったSourceだけを渡し、一致する答えを出させる | 独立性・根拠の限界を把握し、単なる同意を検証成功としない。SP-3 |
| N-5 | 検証失敗／判断不能、Verifier Timeout、根拠欠落を発生させる | 成功と記録せず、公開・利用について定義済みPolicyへ渡す。SP-4 |
| N-6 | 検証後に回答を再生成・編集し、または別Routeで公開する | 古い検証結果を別の回答へ流用せず、実際に利用する内容と対応を保つ。SP-2, SP-4 |

### Failure conditions

High-risk分類が定義されていない、対象回答が通常経路へ抜ける、
高Confidenceを理由に追加Stepを省略する、Stepが同じScoreの再表示だけ、
または実施・結果を回答に結び付けられない場合はFail。
Verifierが失敗した結果を成功として扱う場合もPassとしない。
検証後の具体的な公開・拒否判断は用途のPolicyと別の保証も踏まえて評価する。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| High-risk Policyと分類経路 | Policy／Application Owner | 用途、対象Resource、回答種別、下流Impact | 用途・Policy変更時 | Revisionと変更理由を保持 | 代表的なHigh-risk回答が追加Stepへ進む。 |
| 追加検証の仕様と根拠 | Domain／Security Owner | 重要主張、検証方法、根拠Source、失敗時の扱い | Source・手順変更時 | 機密資料を最小化しVersion保持 | 再Scoreとは異なる具体的な確認内容を示す。 |
| 経路・Abuse Case試験結果 | Test Harness | N-1〜N-6、実際の公開・Tool経路 | Release・Policy変更時 | 合成回答と期待結果を保持 | High-riskの検証実施・結果・利用値の対応を再現できる。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C7.2.1` | 生成回答の信頼性推定。高Confidenceでも追加検証を省略しない。 |
| `v1.0-C7.2.2` | 閾値未満の自動遮断・Fallback。High-risk分類はScoreと独立。 |
| `v1.0-C7.4.2`／`v1.0-C7.4.3` | 出典の由来と主張の追跡。Citationの表示だけで追加検証とはしない。 |
| `v1.0-C9.5.1` | Tool・引数の認可。検証済み手順でも権限判断は別。 |

## Known limitations and uncertainty

別Modelの合意は共有された誤情報によるFalse Consensusを起こし得る。
承認済み資料も古い・誤った可能性がある。人間の確認もApproval Fatigueや
専門性不足の影響を受ける。追加検証の範囲を明示し、
確認していない主張まで「検証済み」と表示しない。
`verifiable`は本Artifactの成熟度であり、製品の正確性や適合を保証しない。

## References

- [AISVS v1.0 C7 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md)
- [AISVS v1.0 C7.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-02-Hallucination-Detection.md)
- [C7 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-10-01 | C7.2.3初版。ConfidenceとImpactを分離し、High-risk回答の追加検証を具体化 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
