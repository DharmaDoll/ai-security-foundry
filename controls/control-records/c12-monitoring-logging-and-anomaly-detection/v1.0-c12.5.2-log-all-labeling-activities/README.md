---
title: "ラベル付けの活動を漏れなく記録する"
versioned_id: "v1.0-C12.5.2"
requirement_id: "C12.5.2"
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

# ラベル付けの活動を漏れなく記録する

AISVS Verification Level: 1

学習資料：[C12.5 AIの材料と変更履歴](../../../learning/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.5-training-data-and-model-lifecycle-audit.md)

## Upstream basis

AISVS `v1.0-C12.5.2`は、すべてのラベル付け活動がLogに記録されることを
求める。ここでのラベルは、学習や評価用Dataに付ける分類・正解・注釈など
を指す。完成したDatasetの現在値だけを保存することとは異なる。

対応するAISVS Researchは、誰がどの項目のラベルを付け直したか、変更前後の
値と時刻を辿る方法を提案する。人の作業と自動ラベル付けの区別、作業時の
基準の版も、誤りと不正な変更を調べる手掛かりになる。ただし特定の
Annotation製品、Field名、基準の版の記録、変更不能な保管方式は、
要件本文が一律に指定した条件ではない。

## Interpretation

対象Dataのラベルを新しく付ける、付け直す、削除するなど、実際に行った
ラベル付けの活動を、その時々に記録する。人が画面で編集する経路だけでなく、
自動処理、まとめて取り込む処理、表計算Fileからの反映も対象に含む。
最終値だけを見せる画面では、途中で何が変わったかを調べられない。

例えば「危険な指示を含む」文章を、担当者が「含まない」に変更したとする。
変更後のラベルだけを保存すると、元の判断、変更した作業、再学習前に
何が起きたかを辿れない。記録から対象の項目、活動の種類、時期、結果を
結び付けて確認できるようにする。作業者や自動処理の出所、変更前後の値も
調査に有益であり、使える範囲で信頼できる作業経路から得る。

## Security objective

誤ったラベルや意図的なラベルの書換えが見つかったとき、その変更の経緯と
影響するDataを調べられるようにする。記録があることだけで、ラベルの
正しさや付与者の善意は証明できない。

## Applicability

学習、Fine-tuning、評価などのために人や自動処理がDataへラベルを付ける
工程に適用する。外部のAnnotation Serviceに委託している場合も、どの
活動が記録され、どこまで確認できるかを責任境界とともに評価する。

### Non-applicability

評価範囲にラベル付けの工程がなく、ラベル付きDataを作成・変更しない
場合は対象外とできる。ただし、表計算Fileで人がラベルを付けてから
取り込む、またはModelが仮ラベルを自動生成する工程があるなら、
専用のAnnotation製品がないことを理由に対象外にはしない。

## Scope and assumptions

- 対象の「活動」を、初回付与、変更、削除、再確認など、ラベルの状態や
  採用判断に影響する操作として明確にする。単なる閲覧や、操作が行われ
  なかった画面表示をすべて記録する要件とは解釈しない。
- Labelの現在値と活動Logを区別する。作業後に現在値を上書きする方式でも、
  以前の値へ至る活動を失わない。
- 人、自動Service、外部委託先、Bulk Importなど、実際にラベルを変更
  できる入口を洗い出す。管理画面だけの監査では足りない場合がある。
- 調査できる記録には、対象Dataの識別、活動の種類、時期、結果が必要。
  Researchが勧める作業者・変更前後の値・基準の版の扱いは、適用する
  Workflowと調査目的に合わせて確認する。
- ラベル付けの記録には敏感なDataが含まれ得る。Data本文を丸ごと複製せず、
  必要な人だけが対象へ辿れるようにする。

## Assets, actors, identities, and trust boundaries

守る対象はラベル付きDataの変更経緯と、それを利用する学習・評価の判断。
作業者、Annotation Service、自動Labeler、Import担当者、Dataset管理者、
調査担当者が関わる。攻撃者や侵害された作業Accountがラベルを反転させ、
Modelの学習結果を歪める可能性がある。善意の基準変更による付け直しも
同じように結果を変える。

主な境界は、作業者・自動処理からラベル保存先へ、保存先から活動Logへ、
ラベル付きDataからDatasetや学習工程へ進むところにある。Importされた
完成Fileだけでは、外部で行われたラベル付け活動を再構成できない。

## Required security properties

| ID | 必要な性質と確かめ方 |
|---|---|
| SP-1 | 対象Workflowの初回付与、変更、削除などのラベル付け活動を、その実行経路に関係なくLogへ残せる。 |
| SP-2 | Logから対象項目、行われた活動、時期、結果を辿り、最終値だけでは分からない変更経緯を確認できる。 |
| SP-3 | 人の作業、自動処理、Bulk Importなどの経路を区別し、対象Datasetのラベルと活動Logを結び付けられる。 |
| SP-4 | ラベルの変更が保存されたのに活動Logが失われる経路を見つけられる。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 最終的なラベルだけがDatasetにあり、付与や変更の履歴がない | Fail。活動を記録したとは言えない。 |
| 人の画面操作は記録するが、自動Labelerの結果を無記録で反映する | Fail。対象となる活動の一部が抜けている。 |
| 変更前後の値は別の保護されたStoreにあり、Logから確実に対象へ辿れる | 活動の経緯を再構成できればPass候補。 |
| Logはあるが、作業時のラベル付け基準の版が分からない | Research上の調査の限界として示す。版の欠如だけで、この短い正規要件のFailとはしない。 |
| ラベルの変更は辿れるが、ラベル自体が誤りだった | 本Controlの記録はPass候補。正しさの検証は別の保証。 |
| Datasetの元Dataや結合工程が不明 | C12.5.1の来歴の問題であり、ラベル活動のLogとは別に評価する。 |
| Model変更の記録を自由に書き換えられる | C12.5.3の変更不能な監査記録の問題。本Controlへ同じ条件を暗黙に加えない。 |

## Threat and failure-mode rationale

悪意あるラベル反転や大量の誤注釈が起きても、活動Logがなければ意図的な
変更と元からあった誤りを区別しにくい。最終値だけでは、いつ・どの経路で
状態が変わったかも分からず、影響するDataの調査が遅れる。Researchは
人の作業と自動処理の区別や基準の版も勧めるが、特定の製品・方式を
正規要件に追加しない。外部の脅威IDとの厳密な対応付けはまだ評価していない。

## Verification

### Architecture and configuration review

ラベル付けを行う画面、API、Bulk Import、自動Labeler、外部委託先を
列挙する。各経路で、対象の項目と活動がいつLogへ届き、完成Datasetと
どう結び付くか確認する。既存ラベルの訂正、削除、審査を含む場合は
その経路も調べる。Logの保存期間と閲覧権限を確認し、単に最終値の
Tableがあることを活動Logの証拠としない。

### Positive verification

無害な合成Dataの二つの項目へ、人と自動処理でラベルを付ける。一つを
人が付け直し、もう一つをBulk Importで変更する。各活動が対象項目と
結果に結び付いて記録され、最終値から最初の付与と途中の変更を
時系列で辿れるか確かめる。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | 既存のラベルを上書きし、最終値だけ残す | 変更活動の欠落を検出し、履歴があると誤認しない。SP-1、SP-2。 |
| N-2 | 自動LabelerやBulk Importから直接ラベルを反映する | 画面以外の経路も活動Logへ残る。SP-1、SP-3。 |
| N-3 | 付けたラベルを削除・訂正する | 結果が変わる活動として対象と時期を辿れる。SP-1、SP-2。 |
| N-4 | 同じ項目を複数回付け直す | 最終値だけでなく、各変更を順に辿れる。SP-2。 |
| N-5 | 委託先から最終的なラベル付きFileだけを受け取る | 委託先の活動を確認できない範囲を示し、完全なLogがあると主張しない。SP-1、SP-3。 |
| N-6 | Logの配送先を一時的に使えなくしてからラベルを保存する | 活動Logが失われないか確認し、失われた変更をPassとはしない。SP-4。 |

### Failure conditions

対象のラベル付け経路に活動Logがない、初回付与や付け直しが最終値に
上書きされるだけ、または自動・Bulk経路の活動が抜ける場合はFail。
保存済みラベルに対応する活動Logが失われた場合もFail。委託先での
活動が不明なら、確認できない範囲を証拠不足として残す。すべての
画面閲覧のLog、特定のAnnotation製品、基準の版、変更不能な保存方式が
ないことだけではFailとしない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認する時期 | 保護上の注意 | 合格の目安 |
|---|---|---|---|---|---|
| ラベル付け経路の一覧 | Data・Annotation担当者 | 人、自動処理、Bulk Import、委託先 | 経路の追加・変更時 | 実DataやAccount名を広く公開しない | 活動できる各経路とLogの作成元が分かる。 |
| 合成した活動記録 | Annotation Service・Import処理 | 初回付与、変更、削除、訂正 | Release時・記録方式の変更時 | 合成Dataを使用し、本文を最小化 | 各対象と活動を最終ラベルから逆に辿れる。 |
| 欠落の試験 | 試験担当者 | N-1、N-2、N-5、N-6 | Log経路・委託範囲の変更時 | 閲覧権限を限定 | 未記録の活動や委託先の証拠不足を発見できる。 |

## Related requirements

| Requirement | 関係と違い |
|---|---|
| `v1.0-C12.5.1` | Datasetの材料と変換・増強・結合の来歴。本Controlは個々のラベル付け活動のLog。 |
| `v1.0-C12.5.3` | Model変更に変更不能な監査記録を求める。本Controlはラベル活動の記録を求めるが、同じ保存方式は指定しない。 |
| `v1.0-C12.5.4` | 取込文書に書込み時のSource・Writer・時刻を付ける。文書の出所Tagと、学習用ラベルの変更活動は異なる。 |

## Known limitations and uncertainty

記録があってもラベルの正しさ、不正な意図、作業基準の妥当性は証明できない。
委託先の記録が取得できない場合は調査に空白が残る。活動Log自体が改ざん
される危険もあるが、C12.5.2はC12.5.3のような一律の変更不能条件を
明示していない。`verifiable`は本書の成熟度であり、実製品の適合結果ではない。

## References

- [AISVS v1.0 C12 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md)
- [AISVS v1.0 C12.5 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-05-Training-Data-Model-Lifecycle-Audit.md)
- [C12 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-04 | 初版。最終値ではなく全ラベル付け活動の記録を、Dataset来歴やModel変更監査と分けた | AISVS固定版と本Repositoryの解釈 | 本書の必要な性質・試験・証拠。実製品での試験は未実施 |
