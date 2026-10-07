# AISVS C11 敵対的な操作に対する耐性

対象はAISVS v1.0の固定Revision `78775233666a2022dcfb82037e5e029116955c00`。
この一覧は[正規要件][normative]の代替ではなく、保証範囲を辿るための
Repository解釈である。個別Controlへのリンクがない行は未整備であり、
学習・製品適合・Mappingの完了を意味しない。正規の成熟度とLevelは
[Catalog](../../catalog.yaml)を参照する。

## この章で保証したいこと

攻撃者が入力を工夫して安全上の制限をすり抜ける、出力から学習Dataを推測
する、APIを使ってModelを複製する、信頼できない情報を改善用Dataへ混ぜる。
C11は、こうした攻撃に対するModelと利用環境の耐性を、訓練、試験、制限、
検知、対処という異なる保証で確かめる章である。単に「安全なModelを使う」
という一文では、どの失敗に備えたか分からない。

安全性の訓練や検知があっても、すべての攻撃を防げるわけではない。
Model出力を認可の根拠にしない、権限と機能を狭めるなどの境界は別途必要。

## Sectionの境界

| Section | 問うこと | できてはいけないこと |
|---|---|---|
| C11.1 Model Alignment, Safety, and Robustness Testing and Training | 許可しない出力や敵対的な入力に対し、Modelを調整し、更新時に試し、弱点を減らしたか。 | 訓練済みとの宣伝、単発の成功例、出力FilterだけでModelの耐性を証明する。 |
| C11.2 Membership-Inference and Model-Inversion Mitigation | 出力や繰り返しの質問から、学習Dataの在籍・属性・内容を推測しにくくするか。 | 汎用API Rate Limitだけで、抽出に必要な質問量を抑えたとみなす。 |
| C11.3 Model-Extraction Defense | APIを通じたModel複製の兆候を見つけ、外部へ出す情報を抑え、必要時に対応できるか。 | 通常の利用量監視だけで抽出の検知・対処が済んだとみなす。 |
| C11.4 Model Runtime Anomaly Detection | 外部・非信頼入力の異常を推論前に調べ、検出後の扱いを決め、改善Feedbackの汚染を防ぐか。 | 異常をFlagしただけで、推論への投入も改善用Dataへの混入も制御したとみなす。 |

## Requirement

LevelはAISVSのVerification Levelであり、本RepositoryのControl成熟度ではない。
下の問いと失敗例は、原文を置き換える新要件ではない。

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C11.1.1](v1.0-c11.1.1-model-alignment-and-safety-training/README.md) | 1 | 対象Modelは、禁止する出力カテゴリを抑える安全性の訓練・調整を受けたか。 | Promptや出力Filterだけを、Model自身の訓練の証拠にする。 |
| [C11.1.2](v1.0-c11.1.2-run-versioned-alignment-suite-on-model-updates/README.md) | 1 | Model更新・Releaseごとに版管理された安全性試験を実行するか。 | 古いModelの試験結果を新Versionへ流用する。 |
| [C11.1.3](v1.0-c11.1.3-evaluate-modality-relevant-adversarial-attacks/README.md) | 1 | 実際に使う入出力形式に関係する既知の攻撃方法で評価するか。 | 画像・音声も扱うのにTextだけを試す。 |
| [C11.1.4](v1.0-c11.1.4-harden-model-against-adversarial-inputs/README.md) | 2 | 敵対的な入力に対し、耐性を高める対策が効くか。 | 対策名や普通の質問での成功だけを耐性の証拠にする。 |
| [C11.1.5](v1.0-c11.1.5-measure-harmful-content-rate-and-flag-regressions/README.md) | 3 | 有害な出力の割合を自動評価し、悪化を定めたしきい値で検知するか。 | 分母や判定基準を変えて悪化を見えなくする。 |
| C11.2.1 | 1 | Modelが推測した敏感な属性を出力で直接返さないか。 | 推測結果をそのまま本人や第三者へ見せる。 |
| C11.2.2 | 1 | 学習Dataの推測を狙う質問量に合わせ、主体別・全体のRate Limitを設けるか。 | 一般的なAPI保護のLimitで抽出リスクも十分と決める。 |
| C11.2.3 | 2 | 過度に自信がある予測を減らすよう出力を調整するか。 | 確からしさの表示を無条件に信じて敏感な推論を許す。 |
| C11.2.4 | 2 | 敏感なDatasetでの学習に差分Privacyを用いた最適化を行うか。 | 通常の学習を差分Privacyと呼ぶ。 |
| C11.2.5 | 3 | 在籍推定攻撃の試験で、評価Data上の正答率が偶然を超えないことを示すか。 | 攻撃試験なしでPrivacyが保たれたと宣言する。 |
| C11.3.1 | 1 | 質問の並び方を分析し、Model抽出の検知へつなぐか。 | リクエスト総数だけで抽出の兆候を見たとする。 |
| C11.3.2 | 2 | 生のModel出力をBackend外へ直接出さず、公開Responseを抽出リスクに合わせるか。 | 生のScoreやResponseを無条件に外部へ公開する。 |
| C11.3.3 | 3 | 無断複製されたModelを識別できる印や特徴を用意するか。 | 攻撃の阻止と、後から複製を見つける能力を混同する。 |
| C11.3.4 | 3 | 抽出が疑われたとき対処を発動するか。 | Alertだけ作って、その後の対応がない。 |
| C11.4.1 | 2 | 外部・非信頼入力の異常を、推論前に調べるか。 | 推論後のLogだけで事前検査をしたとする。 |
| C11.4.2 | 2 | 異常と判定した入力に、定義した制限・保留等を適用するか。 | Flagだけ付けて通常どおり流す。 |
| C11.4.3 | 3 | 安全性違反のFeedback経路に毒入れ検知と人の確認を置くか。 | 攻撃者が作った違反報告をそのまま改善Dataに使う。 |

## 隣接する保証との違い

C2は入力を受け渡す境界、C7はModel出力を利用者や外部へ渡す境界、C12は
運用中の観測と調査を主に扱う。C11.1はModelの訓練・耐性・評価、C11.2と
C11.3はPrivacy推測とModel複製という別の目的への防御を扱う。同じ試験道具や
Telemetryを使っても、各RequirementのPass条件は混ぜない。C9の実行権限や
停止制御も、Modelが安全に答えるかとは独立して検証する。

対応する[AISVS C11 Research][research]は、固定の攻撃例だけでは未知の
変形を尽くせず、Model単体と実際の安全性Pipelineの結果が違い得ると
指摘する。Researchにある製品名、攻撃成功率、特定の試験Corpusを
一律の適合条件にしない。

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C11-Adversarial-Robustness.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C11-Adversarial-Robustness/C11-Adversarial-Robustness.md
