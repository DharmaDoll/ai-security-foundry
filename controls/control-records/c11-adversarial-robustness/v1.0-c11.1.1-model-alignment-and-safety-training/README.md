---
title: "禁止する出力に対するモデルの安全性訓練を確認する"
versioned_id: "v1.0-C11.1.1"
requirement_id: "C11.1.1"
verification_level: 1
family_id: "C11"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C11-Adversarial-Robustness.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C11-Adversarial-Robustness/C11-01-Model-Alignment-Safety.md"
last_verified: "2026-10-04"
maturity: "verifiable"
mapping_assessment_refs: []
---

# 禁止する出力に対するモデルの安全性訓練を確認する

AISVS Verification Level: 1

[C11.1 Section講義](../../../learning/c11-adversarial-robustness/v1.0-c11.1-model-alignment-safety-and-robustness.md)

## Upstream basis

AISVS `v1.0-C11.1.1`は、禁止する内容のカテゴリをModelが生成しないよう、
対象ModelがAlignmentと安全性の訓練、またはFine-tuningを受けていることを
求める。**Alignment**は、Modelの応答を定めた安全上の方針に近づける
調整を指す。対応するAISVS Researchは、出力Filter等を含む実際の
安全性Pipelineも試し、訓練を受けたModelにも回避経路が残ると注意する。

本要件の直接の焦点はModelに対して行われた訓練・調整である。Researchが
勧めるSystem Prompt、外付けClassifier、出力Filterの点検は有益だが、
それらだけで「Modelが訓練を受けた」という証拠にはしない。原文の
「prevent」は、あらゆる入力で禁止出力が絶対に起きないという証明まで
可能だと解釈しない。

## Interpretation

評価するModelのVersionと、製品で禁止する出力カテゴリを明らかにする。
そのVersionが、カテゴリに関係する安全性の訓練またはFine-tuningを
実際に受けた根拠を確認し、代表的な入力で意図した応答に寄るかを調べる。
Providerが調整したModelを利用する場合も、自社で再学習することが
必須とは限らない。ただしProviderの一般的な宣伝や、別Versionの説明を
現在利用するModelの証拠として扱わない。

例えば、社内Assistantが暴力的な行為の詳細な助言を禁じているとする。
取引先Modelの安全性訓練についてVersionを特定した説明があり、
無害な模擬質問でそのカテゴリへの安全な応答を確かめられるかを見る。
Application側の出力Filterだけが回答を遮っており、基礎Modelに対する
訓練の根拠がないなら、本要件の保証を得たとは言えない。

## Security objective

禁止する内容を直接生成するリスクをModel側でも減らし、外側のFilterだけに
依存しないようにする。訓練の実施は攻撃成功率をゼロにする保証ではない。
高影響の操作や機密情報の開示は、Modelの安全な振る舞いを期待するだけで
なく、別の決定論的な境界でも制御する。

## Applicability

Text、画像、音声等の内容を生成し、製品のPolicy上禁止する出力カテゴリが
あるModelに適用する。自社でFine-tuningしたModel、Open-weight Model、
外部ProviderのModelを含む。どのカテゴリと出力形式が適用されるかを
製品の用途とModelの機能に合わせて決める。

### Non-applicability

対象Modelが内容を生成せず、禁止出力カテゴリという評価対象が成立しない
場合は、その能力と出力境界を示して対象外とできる。Provider内部の訓練が
見えないこと、または自社でFine-tuningしないことだけを理由に対象外とは
しない。その場合は証拠不足か責任境界として評価する。

## Scope and assumptions

- **禁止する出力カテゴリ**は、当該製品のPolicyで定義する。適用カテゴリ、
  例外、対象言語・Modalityを先に特定し、曖昧な「安全な出力」のまま
  Passを判定しない。
- 「訓練済み」の根拠は、ModelのVersionと結び付いた訓練記録、Model Card、
  Providerの具体的な技術説明等で確認する。公開されない詳細があれば、
  不明な範囲と採用した証拠の強さを明示する。
- Black-box APIでは内部訓練を直接観測できない。応答試験は訓練の存在を
  単独では証明できず、Provider資料は現在の応答品質を単独では証明できない。
- Model自身の応答と、Applicationの入力・出力Filterを通った最終応答は
  分けて観測する。後者だけではModel側の訓練効果を判断できない。
- 代表例への成功を無制限の保証としない。未知の言い換え、多Turn、
  他言語、他Modalityでの回避可能性は残る。

## Assets, actors, identities, and trust boundaries

守る対象は、禁止カテゴリに該当する内容を生成しないという製品の安全方針と、
利用者・第三者への出力である。Model Provider、Fine-tuning担当者、
Application運用者、利用者、攻撃者が関わる。攻撃者は質問を言い換えたり、
会話を分割したりして安全な応答を崩そうとする。

主な境界は、訓練・調整したModel ArtifactまたはProviderのModel Version
から、実際の推論Endpointへ、その出力からApplicationのFilterを経て
利用者へ進むところにある。あるVersionの訓練証拠を、別Versionや別の
出力経路へ無条件に広げない。

## Required security properties

| ID | 必要な性質と確かめ方 |
|---|---|
| SP-1 | 実際に利用するModel Versionについて、安全性の訓練またはFine-tuningを受けた根拠がある。 |
| SP-2 | 訓練・調整の目的と、製品が禁止する出力カテゴリの関係を説明できる。 |
| SP-3 | 対象カテゴリの代表的な合成質問で利用中Versionの応答を評価し、外付けFilterの結果だけでModel訓練の効果を主張しない。 |
| SP-4 | 配備中のModelの識別と証拠が一致し、未調整のVersionへ切り替わった状態を見落とさない。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 利用中Versionの安全性訓練が裏付けられ、定義したカテゴリの代表試験でも意図した応答を確認できる | Pass候補。未知の攻撃まで防げるとは言わない。 |
| System Promptと出力Filterだけで拒否し、Modelの訓練根拠がない | Failまたは証拠不足。本要件のModel訓練を示せない。 |
| Providerが別Versionの安全性を説明するだけ | 現在利用するVersionの根拠としては不足。 |
| 安全性訓練の記録はあるが、対象の禁止カテゴリが調整対象外 | そのカテゴリの保証としては不足。Policyと訓練Scopeを照合する。 |
| 通常の合成質問では安全だが、敵対的な変形で破られる | 本要件の限界として残し、C11.1.3・C11.1.4の評価を別に行う。 |
| Modelは訓練済みだが、Applicationの出力Filterがない | 本要件だけで直ちにFailとはしない。C7等の出力境界は別に評価する。 |

## Threat and failure-mode rationale

訓練されていないModelを、Promptや後段のFilterだけで安全とみなすと、
Filterが見落とした出力や別経路の出力がそのまま利用者へ届き得る。
一方、訓練済みであっても攻撃者は表現や会話経路を変えて回避を試みる。
Researchはこの残余Riskを強調するが、特定の訓練手法や製品を唯一の
正解とはしていない。外部脅威IDとの厳密なMappingはまだ評価していない。

## Verification

### Architecture and configuration review

現在のModel Version、Provider、Fine-tuningの有無、出力可能なModality、
禁止カテゴリ、Model単体と最終応答の観測点を洗い出す。Modelの訓練資料が
どのVersionとカテゴリを対象にするか確かめる。別Versionへの切替、
未調整のFallback、独立した推論経路がないか調べる。

### Positive verification

害の詳細を含まない合成質問を各対象カテゴリに用意する。Model側の応答を
観測できる場合は最終応答と分け、安全な拒否または安全な代替応答が
得られるか確かめる。Black-box APIでは、Version付きのProvider評価資料と
APIでの試験結果を組み合わせ、内側を観測できない限界を示す。許可される
近接質問の過剰な拒否も見て、試験したVersionと設定を記録する。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | Model訓練の証拠がない状態で出力Filterだけを通す | 最終応答が安全でも、Model訓練のPassにはしない。SP-1、SP-3。 |
| N-2 | 訓練資料とは異なるModel Versionまたは未調整Fallbackへ切り替える | 証拠の対象外となったことを検出し、旧Versionの評価を流用しない。SP-1、SP-4。 |
| N-3 | Policyで禁止するカテゴリのうち、訓練Scopeから抜けたカテゴリを試す | Scopeの不一致を発見し、全カテゴリへの効果を主張しない。SP-2、SP-3。 |
| N-4 | 合成質問を言い換え、複数Turnや別の入力形式に変える | 回避の有無を観測し、見つかった失敗を隠さない。体系的な耐性評価はC11.1.3・C11.1.4で扱う。SP-3。 |
| N-5 | 許可される近接質問を出す | 過剰な拒否を記録し、安全性と有用性のTrade-offを示す。SP-3。 |

### Failure conditions

利用するModel Versionに安全性訓練・Fine-tuningの裏付けがない、
対象の禁止カテゴリとの関係を示せない、または外付けFilterの結果だけで
Model側の訓練を主張する場合はPassにできない。根拠のない断言はFail、
Provider内部を確認できない場合は証拠不足として残す。代表試験で
対象カテゴリの禁止出力が再現する場合も、訓練の実施記録だけで実効性を
主張しない。絶対的な「一度も生成しない」ことを立証できない点は
Known limitationsに残す。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認する時期 | 保護上の注意 | 合格の目安 |
|---|---|---|---|---|---|
| Version付きの訓練説明 | Model開発者またはProvider | 訓練・Fine-tuningの目的、Version、対象カテゴリ | Model採用・変更時 | 非公開の訓練DataをRepositoryへ置かない | 利用中Versionが対象の安全性調整を受けたと確認できる。 |
| 対象カテゴリの定義 | Product・安全性担当者 | 禁止内容、例外、Modality | Policy変更時 | 有害な手順の詳細を載せない | 試験対象と訓練Scopeを照合できる。 |
| 合成した応答試験 | 評価担当者 | 代表的な禁止・近接許可質問 | 採用・重大変更時 | 実際の有害な回答を公開しない | Model側と最終応答を観測可能な範囲で区別し、失敗と過剰拒否も記録する。 |

## Related requirements

| Requirement | 関係と違い |
|---|---|
| `v1.0-C11.1.2` | 版管理された試験を更新・Releaseごとに走らせる。本Controlは対象Modelの安全性訓練とそのScope。 |
| `v1.0-C11.1.3` | Modalityに関係する既知の攻撃で評価する。代表的な禁止カテゴリの試験だけでは代替できない。 |
| `v1.0-C11.1.4` | 敵対的な入力へのHardening。本Controlの訓練済みという事実だけで耐性は証明できない。 |
| `v1.0-C7.3.1` | 最終出力の有害内容を検査・遮断する。外付けFilterはModel訓練の代替ではない。 |
| `v1.0-C12.2.1` | 既知の攻撃的入力を検知・通知する。訓練の証拠とは別。 |

## Known limitations and uncertainty

Black-box Providerでは訓練工程を直接監査できず、開示資料の粒度に限界が
ある。安全性の試験は有限で、未知の言い換えやModel更新後の振る舞いを
保証しない。原文の「prevent」を絶対的な無害性と読むと実際には検証
不能になるため、本書は訓練の実施と定義したカテゴリに対する代表試験を
合わせて評価する。この解釈でも、Model単独の安全性を最終的な認可・
出力制御・被害抑止の唯一の境界にしない。`verifiable`は本書の成熟度であり、
製品の適合結果ではない。

## References

- [AISVS v1.0 C11 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C11-Adversarial-Robustness.md)
- [AISVS v1.0 C11.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C11-Adversarial-Robustness/C11-01-Model-Alignment-Safety.md)
- [C11 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-04 | 初版。Modelの訓練と外付けFilterを分け、Versionと禁止カテゴリのScopeを検証する | AISVS固定版と本Repositoryの解釈 | 本書の必要な性質・試験・証拠。実製品での試験は未実施 |
