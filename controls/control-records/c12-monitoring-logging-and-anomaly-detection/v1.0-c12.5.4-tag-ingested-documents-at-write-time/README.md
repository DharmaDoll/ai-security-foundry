---
title: "取り込む文書に書込み時の出所と書き手と時刻を付ける"
versioned_id: "v1.0-C12.5.4"
requirement_id: "C12.5.4"
verification_level: 2
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

# 取り込む文書に書込み時の出所と書き手と時刻を付ける

AISVS Verification Level: 2

学習資料：[C12.5 AIの材料と変更履歴](../../../learning/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.5-training-data-and-model-lifecycle-audit.md)

## Upstream basis

AISVS `v1.0-C12.5.4`は、取り込むすべての文書に、書込み時点で
Source、Writer Identity、TimestampのTagが付くことを求める。
対応するAISVS Researchは、RAGのKnowledge BaseやVector Storeへ
文書を取り込んだ後に、問題の文書をどこから誰が登録したか辿る用途を示す。
文書と派生Chunkの対応、出所の偽装、書込み後にTagを推測して補う方式の
限界も検討している。

正規要件が直接指定するのは三つのTagと書込み時点である。Researchにある
特定の署名方式、Content Credentials、検索時のPolicy利用、派生Embedding
への暗号的な結合は、ここで一律の必須条件にしない。

## Interpretation

文書を評価対象のStoreへ書く処理が、その書込みと結び付いた三つの情報を
付ける。**Source**は取り込んだ元の場所や経路、**Writer Identity**は
保存先へ書いた人またはServiceの識別、**Timestamp**はその書込み時刻を
指す。Writer Identityを文書本文に記された著者名と混同しない。

例えば、社内のSharePointから人事文書を取り込む場合、取込Serviceは
どのSharePoint上の文書から来たか、認証されたどの主体が保存を実行したか、
いつ保存したかを文書と結び付ける。後日「この文書が不正な回答に使われた」
と分かったとき、登録経路を調べられる。本文の自己申告や後日の推測で
Writer Identityや時刻を作るだけでは、書込み時の証拠にならない。

## Security objective

取り込んだ文書に問題が見つかった際、対象の文書を特定し、登録元・
書込み主体・時期を遡れるようにする。来歴のTagは調査の入口であり、
文書の内容が安全・正確であることや、書込みが認可されていたことを
単独で保証しない。

## Applicability

RAGのKnowledge Base、検索用文書Store、Agentが参照する文書Corpusなど、
外部または内部の文書を取り込む工程に適用する。API、同期Connector、
Bulk Import、管理画面など、文書を書けるすべての経路を評価する。
外部Serviceが取込みを担う場合も、どこまで書込み時Tagを取得・検証
できるかを責任境界とともに示す。

### Non-applicability

評価範囲に文書を取り込む工程がなく、対象となる文書Storeもない場合は
対象外とできる。「RAGと呼んでいない」「Vector DBを使わない」だけでは、
取り込んだ文書を検索・利用する工程が存在しないとは言えない。

## Scope and assumptions

- 「書込み時点」は、文書がStoreへ保存される操作と三つのTag付与が結び
  付く時点を指す。後日のBatchで不明な値を埋めても代替しない。
- Sourceは、実際に取込処理が観測した元の場所や入力経路を記録する。
  利用者が申告した元URLしか分からない場合は、その申告を検証済みの
  出所と区別し、保証できる範囲を示す。
- Writer Identityは、認証された書込み主体または取込Serviceの信頼できる
  実行Contextから得る。Request Bodyに自由入力された「書き手」を、
  保存先へ書いた主体のIdentityとして無条件に採用しない。
- Timestampは保存側で決める。利用者が本文に記した作成日や送信した
  任意の日時は、書込み時刻の代わりではない。
- 文書からChunkやEmbeddingを作る場合、派生物から元文書へ辿れる設計は
  Research上有益。ただし本要件の直接の対象は取り込む文書である。

## Assets, actors, identities, and trust boundaries

守る対象は文書の来歴と、それを用いた調査の信頼性である。文書提供者、
取込担当者、同期Connector、取込Service、文書Store、調査担当者が関わる。
攻撃者は悪意ある文書を登録する、SourceやWriterを偽る、または正規の
権限を持つ書込み主体として内容を改ざんする可能性がある。

主な境界は、外部文書・利用者入力から取込Serviceへ、認証された書込み
主体からStoreへ、Storeにある文書からChunk・検索結果へ進むところに
ある。Tagの生成地点は信頼できる書込み処理側に置き、本文や利用者入力
の自己申告だけを権威ある書込み時のIdentityとしない。

## Required security properties

| ID | 必要な性質と確かめ方 |
|---|---|
| SP-1 | すべての対象文書の書込み時に、Source、Writer Identity、Timestampの三つが文書と結び付いて保存される。 |
| SP-2 | Writer IdentityとTimestampは、信頼できる書込みContextに基づき、本文や任意の利用者入力で偽装できない。 |
| SP-3 | Sourceが表す範囲と信頼度を区別し、書込み時に観測した元文書または入力経路から対象文書へ辿れる。 |
| SP-4 | 管理画面以外のConnector、API、Bulk Importでも、取り込む文書への三つのTag付与が欠落しない。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 取込Serviceが書込み時に三つのTagを文書へ付け、対象から元の経路へ辿れる | Pass候補。すべての書込み経路も確認する。 |
| 文書は保存されたが、SourceかWriterかTimestampの一つが欠ける | Fail。三つのTagが揃わない。 |
| 利用者がRequest Bodyの`writer`や`timestamp`を偽って保存できる | Fail。書込み時の主体と時刻を信頼できる根拠で示せない。 |
| 後日のJobが文書本文から元URLと著者名を推測して埋める | Fail。書込み時Tagではない。 |
| 外部提供者の申告URLをSourceとして記録し、その未検証性も示す | Sourceとして記録された事実と、元URLの真正性を分けて評価する。 |
| 正しい三つのTagを持つ文書に悪意ある指示が含まれる | 本ControlだけでFailとはしない。内容検査や取込認可は別に評価する。 |
| 文書のTagは正しいが、検索時に別Tenantへ開示される | 本Controlの来歴とは別に、C5・C8等の認可を評価する。 |

## Threat and failure-mode rationale

悪意ある文書や誤った文書が検索結果に混ざったとき、保存時の出所・書込み
主体・時刻がなければ、どの経路から入ったかを調べにくい。Tagを後から
作ったり、文書提供者の自己申告だけで作ったりすると、攻撃者が来歴を
偽装できる。ResearchはChunkと元文書の関係や内容の完全性も論じるが、
来歴のTagだけで悪意ある本文を拒否できるわけではない。外部脅威IDとの
厳密なMappingはまだ評価していない。

## Verification

### Architecture and configuration review

書込みを行うAPI、Connector、Batch、管理画面と、それぞれが実行時に
持つIdentity・Source Contextを一覧にする。Tagが付く時点と文書との
結合方法、後から変更できる主体、派生Chunkから元文書へ戻る方法を
確認する。外部ServiceのTagしか取得できない場合、その作成元と未確認
範囲を示す。Tagの存在だけでSourceの真正性や本文の安全性を推定しない。

### Positive verification

合成した文書を、認証された担当者のUploadと同期Connectorの二経路で
取り込む。保存直後に各文書のSource、Writer Identity、Timestampを
調べ、信頼できる書込みContextと一致するか確認する。Chunk化するなら、
検索結果から元文書のTagへ戻れるかも確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | Source、Writer、Timestampのいずれかを欠かして書く | 欠落をFailと判定する。書込みを拒否する設計なら、欠落文書が保存されないことも確かめる。SP-1。 |
| N-2 | Request Bodyの`writer`を別人に変えてUploadする | 保存されたWriter Identityは認証済みの書込みContextを表す。SP-2。 |
| N-3 | 古い日時を送る、または本文の作成日を偽る | 保存されたTimestampはStoreへの書込み時刻を表す。SP-2。 |
| N-4 | 同期ConnectorやBulk Importで管理画面を迂回する | これらの経路でも三つのTagが付く。SP-1、SP-4。 |
| N-5 | 外部提供者が偽の元URLを申告する | 観測できた入力経路と自己申告のURLを区別し、検証済みSourceと誤認しない。SP-3。 |

### Failure conditions

評価対象の文書に三つのTagの欠落がある、書込み後に初めてTagが作られる、
または利用者がWriter Identityや書込み時刻を自由に偽れる場合はFail。
一部のConnectorやBulk経路だけTagが抜ける場合もFail。Sourceの真正性が
外部提供者の申告に依存する場合は、その限界を明示する。本文が悪意を
含むことだけを本ControlのFail理由にせず、内容・認可は別に評価する。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認する時期 | 保護上の注意 | 合格の目安 |
|---|---|---|---|---|---|
| 書込み経路とTag生成点の一覧 | 取込・Store担当者 | Upload、Connector、API、Bulk Import | 経路追加・変更時 | 実文書や個人名を公開しない | 各経路で三つのTagの作成元と書込み時点が分かる。 |
| 合成文書の保存結果 | 取込Service・Store | 書込み直後の文書と派生Chunk | Release時・Tag方式変更時 | 合成Dataを使用 | 文書ごとのSource、Writer Identity、Timestampを辿れる。 |
| 偽装・欠落の試験 | 試験担当者 | N-1からN-5 | Identity・Connector変更時 | 実Accountで攻撃試験をしない | 欠落と偽装を検出し、未検証Sourceを明示できる。 |

## Related requirements

| Requirement | 関係と違い |
|---|---|
| `v1.0-C12.5.1` | Datasetの材料と加工の来歴。本Controlは取り込む個々の文書の書込み時Tag。 |
| `v1.0-C12.5.2` | 学習等のラベル付け活動のLog。書込み時のSource等はAnnotation履歴ではない。 |
| `v1.0-C12.5.3` | Model変更の変更不能な監査記録。本Controlの三つのTagに同じ不変保存方式を暗黙には要求しない。 |
| `v1.0-C8.1.2` | 書込み後のDocument Metadata Tagの不変性。本Controlは書込み時の三つのTag付与を扱う。 |
| `v1.0-C8.1.3` | 検索Scopeの強制。Tagの存在だけで検索の認可は済まない。 |

## Known limitations and uncertainty

正しいTagでも、正規の書込み主体が悪意ある本文を保存した可能性は残る。
利用者申告の元URLだけが分かる場合、そのURLの真正性までは証明できない。
派生ChunkやEmbeddingと元文書の対応が失われると、Tagを調査へ使う価値が
下がるが、すべての派生物への同一Tag複製を正規要件とはしない。
`verifiable`は本書の成熟度であり、実製品の適合結果ではない。

## References

- [AISVS v1.0 C12 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md)
- [AISVS v1.0 C12.5 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-05-Training-Data-Model-Lifecycle-Audit.md)
- [C12 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-04 | 初版。三つの書込み時Tagと本文の安全性・認可を分離した | AISVS固定版と本Repositoryの解釈 | 本書の必要な性質・試験・証拠。実製品での試験は未実施 |
