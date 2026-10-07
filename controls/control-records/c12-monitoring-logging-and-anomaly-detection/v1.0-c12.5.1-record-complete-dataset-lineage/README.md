---
title: "Datasetの構成要素と加工の来歴を辿れるようにする"
versioned_id: "v1.0-C12.5.1"
requirement_id: "C12.5.1"
verification_level: 1
family_id: "C12"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-05-Training-Data-Model-Lifecycle-Audit.md"
last_verified: "2026-10-04"
maturity: "verifiable"
mapping_assessment_refs: []
---

# Datasetの構成要素と加工の来歴を辿れるようにする

AISVS Verification Level: 1

学習資料：[C12.5 AIの材料と変更履歴](../../../learning/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.5-training-data-and-model-lifecycle-audit.md)

## Upstream basis

AISVS `v1.0-C12.5.1`は、各Datasetとその構成要素について、すべての
変換・増強・結合を含む来歴の記録を求める。**来歴（Lineage）**は、
ある成果物がどの元Dataと処理から作られたかを辿るつながりである。
ファイル名や「最新版」だけを残すこととは異なる。

対応するAISVS Researchは、元Datasetから学習用成果物までの加工の連鎖を
追う方法や、Notebookで行った臨時の加工が記録から抜ける問題を示す。
特定の来歴製品、内容Hash、完全な再実行、全Record単位の追跡は
Researchが挙げる検証・実装例であり、要件本文の一律の必須条件ではない。

## Interpretation

対象のDatasetの各版について、何を構成要素として取り込み、どの版へ
どの処理を適用し、どの成果物を作ったかを辿れるようにする。変換は
洗浄・正規化・Filterなど元Dataを変える処理、増強は例の追加や変形、
結合は複数のDataを合わせる処理である。必要な粒度は実際のPipelineで
構成要素や処理を識別できること。単に「加工済み」と記すだけでは、
どの工程が何に影響したか分からない。

例えば社内の問い合わせ履歴と公開FAQを結合し、個人情報の除去と
言い換えによる増強を経て、学習用Dataset v3を作る。後で不正確な回答が
見つかったとき、v3がどの履歴・FAQの版から来たか、除去と増強を
どの順番で行ったかを調べられる必要がある。公開FAQの版だけを残して
社内履歴や増強工程を欠けば、来歴は不完全である。

## Security objective

問題のあるDataや加工工程が見つかったとき、影響するDatasetを特定し、
どこで混入・変化したかを調査できるようにする。来歴があることは、
元Dataや加工結果が安全・正確だったという証明ではない。

## Applicability

AI機能のためにDatasetを収集・加工・結合・増強する工程に適用する。
学習・Fine-tuning・評価用Dataのほか、RAG用のCorpusをDatasetとして
組み立てる工程も、対象に含み得る。外部Providerへ工程を委託している
場合は、責任境界と得られる来歴の範囲を明記する。

### Non-applicability

評価範囲にDatasetを作る・加工する工程がなく、既存の外部Model APIを
呼ぶだけの機能では、当該工程は対象外とできる。ただし自前の評価Set、
RAG Corpus、Fine-tuning用Dataを作っているなら、その部分まで一括で
対象外とはしない。工程があるのに記録できていないことは対象外の理由に
ならない。

## Scope and assumptions

- 「各Dataset」は、調査対象のAI Lifecycleで使うDatasetの各版を指す。
  上書きされた同名ファイルを同じ版として扱わない。
- 「構成要素」は、元Dataset、取り込んだSubset・Shard・Sourceなど、
  最終Datasetへ寄与した材料を指す。必要な粒度は工程に応じて決めるが、
  一部のSourceだけを記録して残りを隠さない。
- 変換・増強・結合は、CIのJobだけでなくNotebookや手動操作も対象。
  記録の方式は異なっても、入力、処理、出力の関係を追える必要がある。
- 再現できる処理なら、版と設定を使って結果を照合すると有効である。
  非決定的な増強で完全なByte一致が難しい場合も、元Data、処理、生成物の
  関係と識別子を失わない。

## Assets, actors, identities, and trust boundaries

守る対象はAIへ投入するDatasetの材料と変更経緯、および問題発見時の
影響調査。Data提供者、Pipeline、Notebook利用者、外部Provider、
Dataset管理者、調査担当者が関わる。攻撃者は外部Dataや一部の加工工程を
汚染することがあり、正規の担当者も誤った変換を行う可能性がある。

主な境界は、外部・社内の元Dataから取込へ、取込から加工工程へ、
加工工程から成果物へ、各工程から来歴記録へ渡る地点である。最終Dataset
の自己申告だけでは、途中の工程を独立して確かめられない。

## Required security properties

| ID | 必要な性質と確かめ方 |
|---|---|
| SP-1 | 対象Datasetの各版と、それを構成する元Data・中間成果物を識別できる。 |
| SP-2 | 変換・増強・結合ごとに、入力、実施した処理、出力の関係を辿れる。 |
| SP-3 | 自動Pipeline外の加工を含む実際の経路で、未記録の工程や構成要素を見落とさない。 |
| SP-4 | 成果物から元の材料へ、また元の材料から影響する成果物へ、記録を使って辿れる。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 最終Dataset名だけ残り、どの元Dataを結合したか分からない | Fail。構成要素と結合の来歴がない。 |
| Source一覧はあるが、除去・増強・結合の工程が抜けている | Fail。元Dataだけでは成果物までの変化を説明できない。 |
| Pipelineは記録するが、Notebookで作った中間Fileをそのまま投入する | その経路の来歴が欠ければFail。自動Pipelineだけを見てPassにしない。 |
| 元Dataから最終版まで辿れるが、元Data自体に悪意ある内容がある | 本Controlの来歴はPass候補。内容の安全性は別に評価する。 |
| Labelの変更活動は記録されない | C12.5.2の不足を別に確認する。Dataset加工の来歴だけでは代替できない。 |
| Modelの変更履歴が自由に書き換えられる | C12.5.3の問題。本Controlへ一律の変更不能要件を追加しない。 |
| RAG文書の書込み時にSource・Writer・時刻が付かない | C12.5.4の書込み時Tagを別に評価する。 |

## Threat and failure-mode rationale

Data Poisoningや誤った加工で問題が起きても、Datasetの由来が分からなければ
影響範囲を絞れない。結合した一つのSourceや臨時のNotebook処理だけが
汚染の入口になる場合、最終File名とPipelineの成功Logだけでは原因を
見つけにくい。Researchは完全な再現試験や専用の来歴Toolを提案するが、
要件本文の目的はまず材料と処理のつながりを記録することである。
外部の脅威IDとの厳密な対応付けはまだ評価していない。

## Verification

### Architecture and configuration review

対象Dataset、各版、元Data、加工の入口、手動・Notebook作業、外部Providerへ
委託した工程を洗い出す。実際の入力から出力までを追い、変換・増強・結合
の各段階が来歴記録へ結び付くか確認する。記録を作る主体、失敗時の扱い、
版の付け方、古い成果物の識別方法も調べる。特定の来歴製品、すべての
個別Recordの追跡、Byte単位の完全な再実行を必須とはしない。

### Positive verification

合成した二つの元Datasetを用意し、一方を洗浄、もう一方を増強した後で
結合し、成果物を作る。成果物の版から二つの元Dataと各中間成果物、
変換・増強・結合の順序を辿り、片方の元Dataを起点に影響を受ける
成果物も特定できるか試す。工程の内容が分かる範囲で、結果と記録を
照合する。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | 二つの元Datasetを結合するが、片方を来歴から除く | 欠けた構成要素を発見し、完全な来歴として扱わない。SP-1、SP-2。 |
| N-2 | Notebookで加工した中間FileをPipelineへ直接投入する | 自動Job外の加工が記録され、未記録なら不完全と分かる。SP-2、SP-3。 |
| N-3 | 増強工程を挟み、最終版には元Dataset名だけを記録する | 増強の入力・処理・出力が欠けることを発見する。SP-2。 |
| N-4 | 同じ名前のDatasetを別内容で上書きする | 旧版と新版を区別し、どの成果物がどちらを使ったか辿れる。SP-1、SP-4。 |
| N-5 | 一つの元Datasetに問題が見つかったとして逆引きする | 影響する中間・最終成果物を特定できる。SP-4。 |
| N-6 | 外部Providerから来歴の一部を取得できない | 取得できた範囲と欠落を区別し、不明な工程を推測で埋めない。SP-1〜SP-4。 |

### Failure conditions

対象Datasetの版や構成要素を識別できない、変換・増強・結合の一部が
記録から抜ける、Notebook等の有効な加工経路を見落とす、または
成果物から元Dataへ辿れない場合はFail。外部委託先の来歴が不明なら、
確認できない範囲を証拠不足として残し、完全な来歴を主張しない。
特定のToolを使わないことや全Record単位の追跡がないことだけでは
Failとしない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認する時期 | 保護上の注意 | 合格の目安 |
|---|---|---|---|---|---|
| Datasetと構成要素の一覧 | Data管理者・取込担当者 | 元Data、中間・最終成果物の版 | Sourceや構成要素の変更時 | Dataset本文や機密のSource名を広く公開しない | 各成果物の材料と版を識別できる。 |
| 加工の来歴 | Pipeline・Notebook利用者 | 変換、増強、結合の入力・出力 | 処理の実行・変更時 | 加工設定に含まれるSecretを記録しない | 最終成果物から各工程を順に辿れる。 |
| 合成した来歴試験 | 試験担当者 | 正常な経路とN-1〜N-6 | Release時・Pipeline変更時 | 合成Dataを使う | 欠落を見つけ、元Dataから影響成果物へ逆引きできる。 |

## Related requirements

| Requirement | 関係と違い |
|---|---|
| `v1.0-C12.5.2` | Label付け活動の記録。本ControlはDatasetと加工工程の来歴であり、Label変更の活動記録とは異なる。 |
| `v1.0-C12.5.3` | Model変更の変更不能な監査記録。本ControlはDataset側の材料と加工のつながりを扱う。 |
| `v1.0-C12.5.4` | 個々の取込文書へ書込み時にSource・Writer・時刻を付ける。本ControlのDataset単位の来歴とは粒度と時点が異なる。 |
| `v1.0-C12.1.4` | RAG検索時に取得した文書等の記録。Datasetを作る工程の来歴とは別の実行時Eventである。 |

## Known limitations and uncertainty

記録された来歴は、元Dataの真正性や内容の安全性を証明しない。外部提供の
Dataや非決定的な増強では、個々のRecordの出所や同じByte列の再生成まで
確認できないことがある。来歴記録そのものが改ざんされる危険も残るが、
本要件はC12.5.3のような一律の「変更不能」条件を明示していない。
`verifiable`は本書の成熟度であり、実製品の適合結果ではない。

## References

- [AISVS v1.0 C12 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md)
- [AISVS v1.0 C12.5 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-05-Training-Data-Model-Lifecycle-Audit.md)
- [C12 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-04 | 初版。構成要素と変換・増強・結合の来歴を、Label・Model・取込文書の記録と分けた | AISVS固定版と本Repositoryの解釈 | 本書の必要な性質・試験・証拠。実製品での試験は未実施 |
