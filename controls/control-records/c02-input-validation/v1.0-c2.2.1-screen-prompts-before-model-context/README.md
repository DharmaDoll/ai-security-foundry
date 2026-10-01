---
title: "Promptの内容を分類し、閾値超過をModel投入前に制御する"
versioned_id: "v1.0-C2.2.1"
requirement_id: "C2.2.1"
verification_level: 1
family_id: "C2"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-02-Content-Policy-Screening.md"
last_verified: "2026-09-29"
maturity: "verifiable"
mapping_assessment_refs: []
---

# Promptの内容を分類し、閾値超過をModel投入前に制御する

AISVS Verification Level: 1

学習資料：[C2.2 Content & Policy Screening](../../../learning/c02-input-validation/v1.0-c2.2-content-policy-screening.md)

## Upstream basis

AISVS `v1.0-C2.2.1`は、各Promptを暴力・自傷・憎悪・性的内容について
Content ClassifierでScore化し、設定可能な閾値と比較することを求める。
閾値を超えたPromptは、Model Contextへ届く前に拒否または無害化する。
対応Researchは分類と遮断の接続、閾値調整、正当な相談等の過剰拒否、
言い換えや複数Turnを用いた回避を論じる。Research中の製品・閾値・運用例を
Normative本文の一律必須条件にはしない。

## Interpretation

このControlは「分類器を置いたか」ではなく、**Modelへ送る各Promptについて、
分類結果に従い投入前の処理が実際に変わるか**を問う。四つの内容区分と
用途別に設定した閾値を明示し、閾値超過時の拒否、または有害部分を除いた
Promptへの変換がModel呼出しより先に完了する必要がある。

Repository interpretationとして、初回入力だけでなく、会話継続、Agentが生成する
後続Prompt、Retry、FallbackでModelへ送られるPromptも送信経路として棚卸しする。
分類後にContextを変更するなら、変更後のPromptについて判定がなお有効かを確認する。
System／Developerの正規Instructionや教育・医療等の引用を機械的に禁止する趣旨ではなく、
分類対象、閾値、許容する引用・相談の扱いを用途に合わせて定義する。

「無害化」は文字列を一部置換したという事実だけでは足りない。
変換後の内容が適用Policyの閾値を超えず、未処理の原文もContextに残らないことを確認する。
その確認方法は製品設計に依存し、特定の分類器や実装方式を要求しない。

## Security objective

禁止内容を求めるPromptが、内容分類とPolicy判断をすり抜けてModelへ投入される
失敗を減らす。入力段階の制御であり、Model応答、Tool実行、データ参照の安全性を
単独で保証するものではない。

## Applicability

外部User、Agent、Tool、検索結果等から組み立てたPromptをModelへ渡すApplicationに適用する。
入力の由来だけでなく、最終的にModel Contextへ含める内容と経路を確認する。
同じPromptが複数Model・Provider・Routeへ送られる場合は各経路の判定を確認する。

### Non-applicability

ModelへPromptを送らない決定論的処理は直接対象外。ただし、User入力欄がないことだけで
Agent生成PromptやRAGを含むModel呼出し経路を除外しない。
非テキスト入力の隠蔽攻撃や複数形式をまたぐ攻撃の検証はC2.2.3／C2.2.4で別途扱う。

## Scope and assumptions

- 「各Prompt」は製品がModelへ実際に送るPromptを指す。すべての保存文書を個別に
  分類する義務と読み替えないが、文書を組み込んだPromptの送信経路は対象となる。
- 閾値は四区分について設定可能であり、用途・言語・Modelによる変更を追跡できるようにする。
  AISVSは普遍的な数値閾値を指定していない。
- ClassifierのScoreは誤検知・見逃しを含む。分類品質と、閾値超過時に送信を止める
  Enforcementの双方を別々に検証する。
- 分類不可・Timeout時に未評価のPromptを通す経路を「各PromptをScore化した」証拠とはしない。
  安全な代替経路と可用性のTrade-offは製品ごとに決める。

## Assets, actors, identities, and trust boundaries

保護対象はContent Policy、Modelへ投入するContext、正当な利用者のアクセス可能性。
攻撃者は外部入力や取得資料へ禁止内容、婉曲表現、会話を跨ぐ要求を置ける。
境界は、非信頼内容からPromptを構成する地点、分類結果をApplicationの送信判定へ渡す地点、
送信許可済みPromptをModel Contextへ投入する地点である。
ClassifierのScoreをModel自身の自己申告や応答後の検査で代替しない。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Modelへ送る対象Promptが、暴力・自傷・憎悪・性的内容の四区分について分類される。 |
| SP-2 | 各区分の適用閾値をPolicyとして設定・識別でき、分類結果との比較が送信判定に接続される。 |
| SP-3 | 閾値超過のPromptはModel Contextへ投入される前に拒否するか、無害化した内容だけを渡す。Logのみの処理では足りない。 |
| SP-4 | 分類後の変更、Retry、Fallback等で未評価・未処理のPromptがModelへ入る経路を作らない。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| Prompt Injectionを検知して遮断する | C2.1.3の保証。内容Policyの四区分と閾値判定の代替ではない。 |
| 閾値超過をLogに残すが、そのままModelへ送る | SP-3を満たさずFail。 |
| 閾値超過を拒否する | SP-3を満たし得る。Classifierの四区分・対象経路・閾値設定は別途確認する。 |
| 閾値超過を無害化するが、原文が履歴に残り送られる | 未処理の原文が到達するためFail。 |
| Modelの出力だけを別の安全分類器で検査する | C7等の別保証。入力段階の分類・投入前制御にはならない。 |
| 内容が安全と判定されたPromptが無権限Toolを要求する | 認可はC5／C9等の別境界。内容分類で許可してよいActionは決めない。 |

## Threat and failure-mode rationale

形式的に正しいPromptでも、製品が扱わない暴力、自傷、憎悪、性的内容を要求し得る。
入力内容が無検査、または分類しても警告だけでModelへ転送されれば、内容Policyの
Enforcement Pointがない。複数経路やFallbackがあれば、一つのGatewayだけで遮断しても
回避され得る。外部Threat Taxonomyへの厳密なMappingは独立に評価するため、
Catalogの`threat_mappings`は空にする。

## Verification

### Architecture and configuration review

Model呼出し経路を列挙し、各経路のPrompt構成、Classifierの入力、四区分のScore、
閾値設定、送信判定、無害化後の内容を追う。分類結果と実際のModel Payloadを結び付け、
Loggingだけの経路、分類後の追記、Retry／Fallback、Classifier異常時の扱いを確認する。

### Positive verification

通常の作業依頼に加え、医療相談、被害申告、教育目的の引用等、区分の語を含んでも
正当に扱うべき例を評価する。用途に応じた過剰拒否率を確認し、許容されたPromptのみが
送信されること、無害化する場合は必要な意味まで失っていないことを観測する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 四区分それぞれの代表Corpusを各Model送信経路へ投入する | 該当区分のScoreと設定閾値を観測でき、超過時は投入前に拒否／無害化される。SP-1〜SP-3 |
| N-2 | Test Double等で閾値超過Scoreを確定させ、Model呼出しを監視する | Logだけで送信する実装はFail。拒否または確認済み無害化後のPayloadだけが送られる。SP-2, SP-3 |
| N-3 | 無害化前の原文を履歴・引用・Tool結果に残したまま次のPromptを構成する | 原文がContextに再流入しない。必要なら次Promptを再評価する。SP-3, SP-4 |
| N-4 | 分類後にPromptへ内容を追記する、またはRetry／Fallbackへ送る | 未分類の最終Payloadが送信されず、判定とPayloadの対応を確認できる。SP-1, SP-4 |
| N-5 | ClassifierをTimeout／失敗させる | 未評価を安全判定と混同して送信しない。SP-1, SP-4 |
| N-6 | 境界近傍の正当な相談・引用、婉曲表現や複数Turnの禁止要求を試す | 誤検知と見逃しを測定し、対象範囲と閾値の妥当性を見直せる。SP-1, SP-2 |

### Failure conditions

四区分のいずれかが対象外、閾値が設定・識別できない、閾値超過を警告するだけで
未処理のPromptを送る、または送信経路の一部で分類を迂回できる場合はFail。
分類器の設定画面や単発のModel拒否応答だけではPassとしない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Model送信経路とPolicy設定 | Application／Policy Owner | Model、Provider、Retry、Fallback、四区分と閾値 | 経路・Policy変更時 | 機密Promptを含めずRevision保持 | 対象経路と適用閾値を再現できる。 |
| Version付き評価Corpus | Security／Test Owner | 四区分、正当な境界例、言い換え、複数Turn | Classifier／用途変更時 | 合成・匿名化例と期待Labelを保持 | 誤検知・見逃しと用途上の影響を評価できる。 |
| 送信Gate試験結果 | Test Harness | N-1〜N-6、Model Payloadと判定結果 | Release・Policy変更時 | 原文を最小化し監査可能に保持 | 閾値超過がModel Contextへ未処理で入らないことを再現できる。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C2.1.3` | Prompt Injection検知とFlag時の遮断。内容Policyの四区分とは評価軸が異なる。 |
| `v1.0-C2.2.2` | 非対応言語における分類の評価。四区分を実装しただけで言語の適用性は示せない。 |
| `v1.0-C2.2.3`／`v1.0-C2.2.4` | 非テキストと複合入力の攻撃。Text Promptの分類だけでは代替できない。 |
| `v1.0-C7` | 出力側の安全性。入力を許した後の応答・公開可否は別途扱う。 |

## Known limitations and uncertainty

Classifierは確率的で、婉曲表現、文脈依存、言語差、正当な相談を誤判定し得る。
無害化の品質も用途に依存する。四区分の内容判定だけでPrompt Injection、
機密漏えい、不正Tool操作、非テキストの隠蔽攻撃を防いだと主張しない。
`verifiable`は本Artifactの成熟度であり、実製品の適合や分類精度の保証ではない。

## References

- [AISVS v1.0 C2 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md)
- [AISVS v1.0 C2.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-02-Content-Policy-Screening.md)
- [C2 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-29 | C2.2.1初版。内容分類、閾値判定、投入前制御と別保証の境界を整理 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
