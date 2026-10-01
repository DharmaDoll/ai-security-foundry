---
title: "非対応言語でのPrompt内容分類を評価する"
versioned_id: "v1.0-C2.2.2"
requirement_id: "C2.2.2"
verification_level: 1
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

# 非対応言語でのPrompt内容分類を評価する

AISVS Verification Level: 1

学習資料：[C2.2 Content & Policy Screening](../../../learning/c02-input-validation/v1.0-c2.2-content-policy-screening.md)

## Upstream basis

AISVS `v1.0-C2.2.2`は、Promptの内容分類を、分類器が対応していない言語でも
評価することを求める。Normative本文は、全言語への対応、特定の言語検出器、
翻訳方式、一律拒否を指定しない。対応Researchは、低リソース言語、言語混在、
翻字による分類回避、Providerの対応言語と実際の性能の差を取り上げ、
言語ごとの試験と未評価範囲の把握を提案する。Research中の製品・数値・
ツール例は本Controlの一律必須条件ではない。

## Interpretation

「分類APIが結果を返す」ことと「その言語で内容を正しく分類できる」ことを分ける。
製品が受け付け、またはModelへ到達し得る言語について、分類器の公称対応範囲を
確認し、非対応・不明・低信頼の言語でも内容Policy違反をどの程度検出できるかを
実際のPrompt経路で評価する。結果を、対象言語、Classifier／Policy Version、
誤検知・見逃しと結び付けて記録する。

Repository interpretationとして、言語判定不能や混在言語を「英語扱いで安全」と
暗黙に処理しないことを求める。ただし、このRequirementの直接の判定対象は
**非対応言語での分類評価**であり、評価後の一律遮断までは要求しない。
評価で見つかったGapを許容するか、拒否・確認・別経路へ振り分けるかは、
用途とリスクに応じた別の運用判断として明示する。

## Security objective

英語等で有効な内容分類が、別の言語や言語混在では機能しないにもかかわらず、
同じ保証があると誤認することを防ぐ。特定言語での有害内容の完全検出や、
すべての言語を利用可能にすることを保証しない。

## Applicability

複数言語のPromptを受け付けるApplication、またはUI上の対応言語を限定していても
API、Tool、RAG、履歴、Agentの後続Promptから別言語がModelへ届き得るApplicationに適用する。
対象はC2.2.1の内容分類が用いられるModel投入経路である。

### Non-applicability

ModelへPromptを送らない決定論的処理は対象外。入力段階で許容文字・言語を
確実に制限し、非対応言語がModelへ届かないことを試験で示せる経路は、
到達しない言語の分類性能を製品内で評価する必要性が異なる。
UIの言語設定だけでは非到達の証拠にならない。

## Scope and assumptions

- 「非対応」はClassifierの公称非対応だけでなく、対象用途で性能が未検証、
  または短文・方言・翻字・混在によって対応判定が不確かな場合を含めて棚卸しする。
- 有限の試験で全言語・全表現を保証することはできない。実際の利用言語と
  攻撃可能な入力経路を基に、代表的な対象と言語差の限界を明示する。
- 言語検出器の出力は証拠の一部であり、低信頼・不明の結果を安全判定に変換しない。
  検出器を必須実装とするのではなく、評価対象言語を識別できることが必要である。
- 対応言語表、モデル、閾値、翻訳経路が変われば分類性能を再評価する。

## Assets, actors, identities, and trust boundaries

保護対象は内容Policyの適用範囲と、製品が利用者へ示す言語別の安全保証。
攻撃者は非対応言語、翻字、複数言語を混ぜたPromptを送信し得る。
Trust Boundaryは、任意の言語のTextが入力経路へ入り、Classifierの
対応範囲・言語判定を経てModel送信のPolicy判断へ進む地点である。
「安全なScoreが返った」という事実だけで言語別の検出能力を推定しない。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Modelへ到達し得るPromptの言語範囲と、Classifierの公称対応・未対応・不明範囲を区別できる。 |
| SP-2 | 非対応または不明な言語の代表Corpusで、C2.2.1の内容区分に関する分類結果と見逃し・誤検知を測定できる。 |
| SP-3 | 言語混在、翻字、短文等の現実的な境界例を評価し、単一言語の成功だけで全経路をPassにしない。 |
| SP-4 | 評価結果、未評価範囲、分類器・Policy Versionが製品のリスク判断へ渡され、対応済みという根拠のない主張をしない。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 英語の分類試験だけが成功する | 非対応言語での評価にならずFail。 |
| Providerが「多言語対応」と宣伝する | 対象製品の非対応・不明言語での評価を代替しない。 |
| 非対応言語を試験し、見逃しが多いと分かった | 評価自体の証拠になり得るが、安全な運用状態まで意味しない。Gapとリスク処理を別に判断する。 |
| 非対応言語を入力時に確実に拒否する | Modelへ到達しないことを確認する。単なるUI制限や申告だけでは足りない。 |
| 非対応言語を翻訳して分類する | 一つの候補。原文の意味の変化と翻訳失敗を含めて性能を評価する。必須方式ではない。 |
| 閾値超過をModel投入前に拒否／無害化する | C2.2.1の送信制御。言語別性能の評価とは別の保証。 |

## Threat and failure-mode rationale

分類器が主に特定言語で学習・調整されている場合、別言語の禁止要求にも
低いScoreを返し得る。攻撃者はその差を使い、単一言語の試験では見えない
Policy回避を狙う。混在言語や翻字は言語検出と分類の双方を曖昧にする。
対応Researchはこうした回避を論じるが、個々の研究値を本Repositoryの
適合基準にはしない。外部Threat IDへの厳密なMappingは未評価とする。

## Verification

### Architecture and configuration review

Modelへ届くText経路と利用言語、Classifier／Providerの対応言語表、
言語判定・翻訳・閾値設定、対象外・判定不能時の扱いを確認する。
宣言された対応と製品内の実測を分け、試験結果が実際のPrompt構成経路と
同じClassifier／Policyを通ったか確認する。

### Positive verification

主な利用言語に加え、非対応・不明として選んだ代表言語で、正常な相談、
教育的引用、医療・福祉文脈等を試す。過剰拒否を言語別に測定し、
正当な利用者への影響を確認する。単に拒否率が高いことを分類品質としない。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 公称非対応言語で四つの内容区分の代表Promptを分類する | 対象言語、期待Label、Score、見逃し率を記録できる。SP-1, SP-2 |
| N-2 | 英語では検出される同趣旨の要求を非対応言語に言い換える | 性能差を測定し、英語の成功を非対応言語の証拠にしない。SP-2, SP-4 |
| N-3 | 一つのPrompt内で言語を切り替え、または翻字・短文を使う | 言語判定不能や部分的な見逃しを含めて評価できる。SP-2, SP-3 |
| N-4 | 言語判定が低信頼・不明を返す | 言語を英語として扱ったことにせず、未確定の評価・運用上の扱いを記録する。SP-1, SP-4 |
| N-5 | Classifier、対応言語表、翻訳経路、閾値を変更する | 旧結果を現行性能とみなさず、影響言語を再評価する。SP-2, SP-4 |
| N-6 | UIの対応言語以外をAPI・Tool・履歴からModelへ入れる | 実際に到達する言語を試験範囲へ含めるか、到達しないことを証明する。SP-1, SP-3 |

### Failure conditions

非対応言語の試験がない、Providerの対応表だけで性能を推定する、
英語の試験を全言語の証拠にする、または実際の入力経路にある混在・
不明言語を評価範囲から無根拠に除外する場合はFail。
評価で性能不足が判明した場合は、その事実とリスク処理を記録する。
性能不足を隠して「対応済み」とすることはPassにならないが、
本Requirement自体を全言語の高精度分類義務へ拡張しない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 言語・経路Inventory | Application／Policy Owner | UI、API、Tool、RAG、履歴、AgentのModel送信経路 | 経路・製品変更時 | 設定Revisionを保持 | 到達言語と対応・未対応・不明を区別できる。 |
| Version付き言語別Corpus | Security／Test Owner | 四区分、正常例、混在・翻字・短文 | 脅威・用途変更時 | 合成・匿名化例と期待Labelを保持 | 対象選択と見逃し・誤検知を再現できる。 |
| 評価結果とGap判断 | Test／Risk Owner | 対象Classifier、Policy、言語、N-1〜N-6 | Release・Classifier変更時 | 機密原文を最小化しRevision保持 | 結果、未評価範囲、後続のリスク判断を追跡できる。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C2.2.1` | 内容分類と閾値超過の投入前制御。本Controlは言語が変わったときの分類性能の評価を問う。 |
| `v1.0-C2.2.3` | 画像・音声等の非テキスト検査。画像内の別言語Textは両方の観点を持ち得るが、本Controlは非テキスト検査方式を指定しない。 |
| `v1.0-C2.2.4` | 複数入力形式を組み合わせた攻撃。言語混在だけで複合形式検査を満たすわけではない。 |

## Known limitations and uncertainty

言語名だけでは、方言、地域差、文化的文脈、翻字、コード切替を十分に表せない。
小さいCorpusや翻訳だけのCorpusは現実の見逃しを過小評価し得る。
言語検出器自体も短文や混在入力で誤る。評価してGapを把握しても、
そのGapを許容できるかは製品用途・被害可能性・代替制御に依存する。
`verifiable`は本Artifactの成熟度であり、製品の多言語安全性を保証しない。

## References

- [AISVS v1.0 C2 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md)
- [AISVS v1.0 C2.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-02-Content-Policy-Screening.md)
- [C2 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-30 | C2.2.2初版。言語別分類の評価と評価後のリスク処理を分離 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
