---
title: "多数の例示によるJailbreakパターンを検知する"
versioned_id: "v1.0-C2.1.8"
requirement_id: "C2.1.8"
verification_level: 3
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

# 多数の例示によるJailbreakパターンを検知する

AISVS Verification Level: 3

学習資料：[C2.1 Prompt Injection Defenses](../../../learning/c02-input-validation/v1.0-c2.1-prompt-injection-defenses.md)

## Upstream basis

AISVS `v1.0-C2.1.8`は、Many-shot JailbreakingのパターンをSystemが検知できることを求める。
対応Researchは、大量の架空問答や反復例示で望ましくない振る舞いをModelに模倣させる攻撃、
複数Turnに分散した変種、正常なFew-shot利用との区別を論じる。Researchにある例示数の固定上限、
特定Detector、Alert設計や遮断方法は検討例であり、Normative本文の一律必須条件ではない。

## Interpretation

入力Contextに含まれる複数の例示が、Modelへ不正な応答様式や指示違反を学習させるように
組み立てられている場合、その**反復構造と誘導意図**を検知する能力を評価する。
単に長文である、問答が多い、連続投稿が多いという理由だけでMany-shotと判定しない。
逆にToken上限内であることやModelがたまたま拒否したことを、検知能力の証拠にしない。

検知対象はModelへ実際に渡すContextと、そこで意味を持つ履歴・資料の組合せである。
Detectorの観測結果をPolicyへどう結び付けるかは別の設計判断であり、AISVS C2.1.8の本文は
検知時の一律遮断を明記していない。高Impactな用途では検知結果の扱い、権限制限、出力確認を
別途設計するが、それらを本Controlの隠れた必須条件にしない。

## Security objective

多数の例示がContext内で安全指示を押し流し、不正な出力様式を「通常の続き」として
Modelへ学習させる試みを見つける。検知が成立しても、未知の攻撃に対する完全防止や
下流Actionの認可まで保証したことにはならない。

## Applicability

外部主体がModelへ届く例示、会話履歴、検索文書、Tool応答、Memory等を投入・変更できる
Applicationに適用する。正規UserがFew-shot Promptを使える製品でも対象となる。
複数Turnや複数文書に分かれた例示が一つのModel Contextに集約される場合は、その合成後の
検知経路も評価する。

### Non-applicability

Modelが非信頼Textや例示を受け取らない決定論的処理は直接対象外。
現在のUIが例示入力欄を持たないだけでは、RAG・Tool・履歴等の経路を対象外にできない。

## Scope and assumptions

- Many-shotは例示数だけで定義されない。反復するInput／Output例、Role-play、架空の成功回答等が
  どの望ましくない振る舞いを誘導するかを含めて評価する。
- 対象Model、Context構成、正規のFew-shot用途によりDetectorの閾値と誤検知率は変わる。
  上流要件は普遍的な例示数・Score閾値を指定しない。
- Inputから分割・要約・検索選択を経て例示構造が変わる場合は、実際に利用するContextでの
  観測可能性を確認する。
- 検知器の性能は確率的であり、検知の有無・結果・限界を試験CorpusのVersionとともに記録する。

## Assets, actors, identities, and trust boundaries

保護対象は上位の指示・安全上の制約、Userの正当な作業意図、Modelの応答の完全性。
攻撃者は下位のPrompt、文書、Tool応答、Memory等へ反復例示を置き得る。
Trust Boundaryは、その例示がApplicationの入力・Context組立てを経てModelの
In-context学習材料になる地点。検知の観測点は合成済みContextを評価できる入力側の境界で、
その結果を記録・利用するSystem ComponentはModelの自己申告と分ける。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 対象WorkflowでMany-shot Jailbreakを、単なる長さや例示数だけでなく攻撃的な反復構造として識別する判定基準がある。 |
| SP-2 | User入力だけでなく、実Contextへ入る履歴、RAG、Tool、Memory等の経路を検知対象に含める。 |
| SP-3 | 代表的な攻撃Corpusで検知結果を観測でき、正常なFew-shot／FAQ等との誤判定も測定する。 |
| SP-4 | 検知結果が後続のPolicy判断・調査に利用できる形で、対象Contextと判定根拠・Versionに結び付く。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| Token上限を超える入力を拒否する | C2.1.4の保証。上限内のMany-shotを検知できる証拠ではない。 |
| 正常な教材の問答を大量に含む入力をすべて攻撃と判定する | 誤検知が大きく、構造と意図を識別するSP-1・SP-3の品質を示さない。 |
| Modelが危険な要求を拒否するが、SystemにMany-shotの検知結果がない | Modelの応答だけでは本Controlの検知能力を示せない。 |
| DetectorがMany-shotと判定し、記録・Policyに結果を渡す | 本ControlのPass根拠になり得る。C2.1.3の検知時遮断と製品全体の安全性は別途評価する。 |
| 単発の役割詐称でModelが指示階層を破る | C2.1.6等の別保証。Many-shotでない場合、本ControlだけのFailとはしない。 |

## Threat and failure-mode rationale

攻撃者は大量の架空の問答や成功例をContextへ配置し、Modelの次の応答をその例の続きへ
寄せようとする。長いContextで合法的なFew-shotが使われるため、単純な長さ制限や
「問答がある」という条件では攻撃を区別できない。Researchは複数Turnに分割された
変種も議論するため、Context合成時に反復構造を見失う経路を確認する。
外部Threat IDとの厳密なMappingは未評価とし、Catalogの`threat_mappings`は空にする。

## Verification

### Architecture and configuration review

User、履歴、RAG、Tool、MemoryからのTextがどの時点でContextへ組み込まれ、
Detectorが何を見られるかを追う。判定基準、閾値、対象Model／言語、結果の出力先と
Corpus管理を確認する。単なる最大Token設定や、Modelによる拒否だけをDetectorとして数えない。

### Positive verification

正当なFew-shot指示、FAQ、教育資料、会話履歴を投入し、用途に必要な例示が
不当に攻撃扱いされないことを確認する。DetectorのScoreだけでなく、結果が
どのContextと結び付いたかを観測する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 上限内のContextに、禁止された回答を模倣させる多数の架空問答を置く | Many-shotとして検知され、長さ判定のみで見逃さない。SP-1, SP-3 |
| N-2 | 同じ例示を複数のUser TurnやRAG文書に分散して合成する | 実Contextの反復構造を対象に評価できる。SP-2, SP-3 |
| N-3 | 例示の形式・言語・区切りを変えて同じ誘導を試す | 対象範囲内の変種を検知し、未対応範囲を明示する。SP-1, SP-3 |
| N-4 | 正常な多数のFAQ、分類例、要約例を与える | 攻撃と同一視せず、誤検知を測定する。SP-1, SP-3 |
| N-5 | Detectorの判定後に資料を追加・差替えする | 最終的にModelへ渡すContextとの対応を失わず再評価する。SP-2〜SP-4 |
| N-6 | Modelが拒否したがDetectorは何も出力しない構成で攻撃Corpusを送る | Model応答と検知結果を区別し、検知できない状態をPassとしない。SP-3, SP-4 |

### Failure conditions

代表的なMany-shot Corpusで検知結果を観測できない、User欄だけを見て他の対象経路を
見逃す、または単なる長さ・投稿回数を検知の代替とする場合はFail。
Detectorの設定だけで動作試験がない場合もPassとはしない。Normative本文が一律遮断を
要求していないため、検知後のRisk処理の不足は別の保証としても評価する。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Context Flowと検知配置 | Application Owner | User、RAG、Tool、Memory、履歴 | Topology変更時 | 機密入力を含めずRevision保持 | 検知器が最終利用Contextの対象部分を見られる。 |
| Version付き試験Corpus | Security／Test Owner | 攻撃例と正常Few-shot、言語・形式 | Threat／Model変更時 | 合成Dataと期待Labelを保持 | Many-shot固有の判定と誤検知を評価できる。 |
| 判定・回帰試験結果 | Test Harness | N-1〜N-6、対象Model | Release・Detector更新時 | 判定基準、Score／Event、Versionを保持 | 攻撃検知と正常系への影響を再現できる。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C2.1.3` | 一般のInjection検査と検知時遮断。本ControlはMany-shotという構造の検知能力を問う。 |
| `v1.0-C2.1.4` | Context上限を超える入力の拒否。上限内のMany-shotを扱えない。 |
| `v1.0-C2.1.6` | 上位指示の優先順位。Many-shot検知だけで階層維持を保証しない。 |
| `v1.0-C9.1.2` | Agent実行の累積Budget。大量の例示を伴う単発Contextの検知とは別。 |

## Known limitations and uncertainty

Many-shotと正常なFew-shotの間に、すべての用途に通用する件数境界はない。
Test Corpusが既知の表現に偏れば、新しい言語・分割・言い換えを見逃す。
研究上の検知手法や数値はSource Revision、Model、Corpusに依存し、
このRepositoryの適合閾値や保証値として採用しない。

`verifiable`はRepository Artifactの成熟度であり、製品適合やJailbreakの完全防止を示さない。

## References

- [AISVS v1.0 C2 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md)
- [AISVS v1.0 C2.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md)
- [C2 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-29 | C2.1.8初版。Many-shot検知と長さ制限・応答拒否の境界を整理 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
