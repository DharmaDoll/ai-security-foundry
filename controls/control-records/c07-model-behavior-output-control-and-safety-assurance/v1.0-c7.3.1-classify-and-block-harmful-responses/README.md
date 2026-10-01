---
title: "全Responseの有害内容を分類し、該当出力を遮断する"
versioned_id: "v1.0-C7.3.1"
requirement_id: "C7.3.1"
verification_level: 1
family_id: "C7"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-03-Output-Safety-Privacy-Explainability.md"
last_verified: "2026-10-01"
maturity: "verifiable"
mapping_assessment_refs: []
---

# 全Responseの有害内容を分類し、該当出力を遮断する

AISVS Verification Level: 1

学習資料：[C7.3 Output Safety](../../../learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.3-output-safety.md)

## Upstream basis

AISVS `v1.0-C7.3.1`は、自動Classifierが各Responseを検査し、
定義済みの有害内容Categoryに該当するContentを遮断することを求める。
対応Researchは有害な回答、Classifier回避、誤検知、公開経路ごとの
遮断とLatencyのTrade-offを論じる。特定製品、固定Category一覧、
研究上の検出率をNormative本文の一律必須条件にはしない。

## Interpretation

Applicationが利用・公開するModel Responseを、定義した有害内容Categoryについて
自動分類し、その結果を公開判定へ接続する。該当したResponseはUser表示、
API返却、Tool／後続Agent Step等の利用へ進めない。ClassifierのAlertを
Logに残すだけ、あるいはModelの自己検閲に期待するだけでは足りない。

「各Response」は、最終回答だけを指すと決め付けない。製品で実際に
公開・利用されるResponse、再生成、Fallback、Streaming断片等の経路を
棚卸しし、検査済み内容と利用された内容が一致することを確認する。
Streamingという方式自体はFailではないが、全文判定を要するCategoryについて
危険な断片を先に公開し、完了後に遮断しても既公開の内容は戻せない。

Categoryと判定基準は用途に応じたPolicyとして定義する。
C2.2.1の入力側の四Categoryと同じ設定を必須とはしない。
分類の有効性と、該当した場合の決定論的な遮断動作を別々に試験する。

## Security objective

Modelが生成した有害な内容が、分類結果をすり抜けて利用者や
後続Systemへ届く失敗を減らす。分類器の誤検知・見逃しがあるため、
未知の有害表現の完全な防止は保証しない。

## Applicability

Model ResponseをUser、API Client、Tool、別Agent、Memory等が
利用するApplicationに適用する。Text以外のResponseを扱う場合は、
利用形式に対するClassifierの対応範囲と別の検査要件を明示する。

### Non-applicability

Model Responseを取得・利用しない決定論的処理は直接対象外。
Responseが「内部用」であるだけでは、別AgentやToolへ渡る経路を
対象外にできない。

## Scope and assumptions

- 有害内容Categoryを用途に応じて定義し、Classifierの対象形式・言語・
  Version、ScoreやLabelの扱いを明示する。AISVSは普遍的な閾値を指定しない。
- Classifierは確率的で、言い換え、文脈依存、分割された出力を見逃し得る。
  正常な教育・医療・報道文脈を過剰遮断する可能性も評価する。
- Providerの内蔵安全機能は利用できるが、実際の公開経路で
  検査と遮断が働くことを確認する。機能名だけを適合証拠としない。
- Classifierが利用不能・判定不能の場合を安全な判定結果と同一視しない。
  未評価時の扱いは製品Policyで定める。

## Assets, actors, identities, and trust boundaries

保護対象は利用者、後続Systemの受入れ境界、製品のContent Policy。
攻撃者はPromptや取得資料から有害Responseを誘い得る。
Modelも攻撃なしに不適切な内容を生成し得る。Trust Boundaryは、
Model ResponseがClassifierとApplicationの公開判定を経て、User、
API、Tool、別Agent等へ進む地点。意味判定は確率的でも、
該当判定後の通過可否はApplicationが強制する。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 利用するResponse経路と、適用する有害内容Category・判定基準を特定できる。 |
| SP-2 | 各対象Responseが対応する自動Classifierで検査され、判定結果を利用するResponseへ結び付けられる。 |
| SP-3 | 定義した有害Categoryに該当したResponseは、公開・利用前にApplicationが遮断する。Alertだけでは足りない。 |
| SP-4 | Streaming、Retry、Fallback、別Sinkへの転送でも未検査・遮断対象Responseを通す経路がない。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 入力Promptを分類し、有害入力を拒否する | C2.2.1の入力側保証。出力Responseの検査・遮断の証拠ではない。 |
| 有害ResponseをClassifierがFlagしたが、そのまま表示する | SP-3を満たさずFail。 |
| Modelがたまたま有害な要求を拒否した | Modelの応答だけでは全Responseの出力分類と遮断を示せない。 |
| ResponseのJSON Schemaが正しい | C7.1.1の形式保証。有害性は別。 |
| Responseが内部DataやSystem Promptを含む | C7.3.2の別保証。定義した有害Categoryだけで漏えいを網羅したとしない。 |
| Markdownの画像URLが外部Requestを起こす | C7.3.3の通信境界。内容分類だけで外向き通信を防いだとしない。 |

## Threat and failure-mode rationale

Modelは有害な表現を出力することがあり、入力検査を置いても
生成結果の内容を保証できない。Classifierの判定が公開処理と
接続されていなければ、検出済みの内容も利用者へ届く。
Researchは回避表現や文脈依存の誤判定を挙げるため、
製品用途に応じたCorpusで検出能力を評価する。
外部Threat IDへの厳密なMappingは未評価とする。

## Verification

### Architecture and configuration review

全Model ResponseがUser表示、API、Tool、別Agent、Memoryへ至る経路を追い、
Classifierの配置、Category Policy、判定結果と公開Gateの接続を確認する。
Streaming、再生成、Provider切替、Classifier Timeout時に未検査内容が
通らないかを確認する。出力を変換・Rendererへ渡す順序も追う。

### Positive verification

正常な回答と、危険語を説明・引用する正当な教育、医療、報道等の回答を
投入し、用途に必要な表現が不当にすべて遮断されないことを測る。
Score／Labelと実際に公開されたPayloadの対応を確認する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 定義した各有害Categoryの代表Responseを最終回答経路へ流す | Classifierが検査し、該当判定した内容を公開前に遮断する。SP-1〜SP-3 |
| N-2 | Test Double等で該当判定を固定し、API／User／Tool経路を監視する | LogやWarningだけで通さず、各Sinkへの配送を止める。SP-2〜SP-4 |
| N-3 | Streaming途中に有害内容を置き、後続ChunkでClassifierがFlagする | 判定前の不可逆な公開を生じさせない設計を確認する。SP-3, SP-4 |
| N-4 | Retry／Fallbackで新しいResponseを生成し、または検査後に内容を変更する | 実際に利用する新しいPayloadを検査し、旧判定を流用しない。SP-2, SP-4 |
| N-5 | 言い換え・婉曲表現・混在言語のResponseと正常な引用を試す | 見逃しと誤検知を対象範囲内で測り、Category Policyの限界を記録する。SP-1, SP-2 |
| N-6 | ClassifierをTimeout／失敗させる | 未検査を安全判定に変換せず、定義済みの障害時Policyへ進む。SP-2, SP-4 |

### Failure conditions

Categoryが未定義、対象Responseの一部がClassifierを迂回する、
有害判定を記録するだけで元Responseを公開する、または
検査済みPayloadと利用Payloadが異なる場合はFail。
Classifierの設定画面やモデル側の安全指示だけではPassにしない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Response FlowとCategory Policy | Application／Policy Owner | 公開・API・Tool・別Agent経路、Category、Classifier | 経路・Policy変更時 | 機密Responseを含めずRevision保持 | 全対象経路と遮断点を辿れる。 |
| Version付き評価Corpus | Security／Test Owner | 有害例と正当な境界例、形式・言語 | Threat・Classifier変更時 | 合成・匿名化例と期待Labelを保持 | 見逃しと誤検知を再現できる。 |
| Classifier・Gate試験結果 | Test Harness | N-1〜N-6、実公開・下流Sink | Release・Model変更時 | 原文を最小化し判定を追跡可能に保持 | 該当Responseが利用前に遮断される。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C2.2.1` | Prompt入力の四Category分類と投入前制御。本Controlは生成Responseの出力側。 |
| `v1.0-C7.1.1` | 出力Schemaの適合と拒否。形式と意味上の有害性は別。 |
| `v1.0-C7.3.2` | System Prompt・Backend Data漏えいの検出・遮断。一般の有害Categoryでは代替できない。 |
| `v1.0-C7.3.3`／`v1.0-C7.3.4` | 外向きRequestと隠れた内容の別境界。Classifierだけで保証しない。 |

## Known limitations and uncertainty

Classifierは確率的で、未知の言い換え、文脈、言語、形式によって
見逃しや誤検知を生む。全Responseを検査しても、既公開のStreaming断片、
別Sinkで発生する通信、出力に含まれる内部情報をすべて防いだとは言えない。
`verifiable`は本Artifactの成熟度であり、製品の出力安全性を保証しない。

## References

- [AISVS v1.0 C7 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md)
- [AISVS v1.0 C7.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-03-Output-Safety-Privacy-Explainability.md)
- [C7 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-10-01 | C7.3.1初版。出力分類と公開前遮断を別々に検証可能にした | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
