---
title: "C7.4 Source Attribution & Citation Integrity：出典の由来と主張の裏付けを分ける"
document_kind: "section-learning-note"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
last_updated: "2026-09-28"
---

# C7.4 Source Attribution & Citation Integrity

## Normative Requirements

[AISVS v1.0固定版の英語原文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md)を正本とする。大量転載は避け、以下は日本語要約とする。LevelはVerification Levelであり、Control成熟度ではない。

| ID | Level | 日本語要約 |
|---|---:|---|
| v1.0-C7.4.1 | 1 | RAGを使う回答へ参照元文書の出典を付ける。 |
| v1.0-C7.4.2 | 1 | 出典はModelに生成させず、検索結果のMetadataから取得する。 |
| v1.0-C7.4.3 | 2 | 回答中の主張を、検索された該当Chunkまで追跡できるようにする。 |
| v1.0-C7.4.4 | 3 | 生成Mediaへ、AI生成であることを示すWatermarkを付ける。 |

## Source separation・Category内の位置

Normativeは上記原文。Researchは偽の引用、主張と根拠の不一致、Media表示の補足。以下のScenario・設計例はRepository interpretation。対話由来の原則はDerived insightとして示す。[Family guide](../README.md)へ戻る。学習完了はControl maturity、Mapping、製品適合を変更しない。

C7.1は形式、C7.2は回答の信頼性、C7.3は出力の安全性、C7.4は出典の由来・主張の裏付けを扱う。ただし、これらは必ず順番どおり実装するPipelineではなく、同じ出力に重なる評価軸である。7.4.4はRAGの引用から外れ、生成Mediaの由来表示という別の枝に属する。

## 具体Scenarioと用語

社内規程を検索するRAGが「経費承認上限は100万円。出典：経費規程」と答える。経費規程は実在し、検索結果にも含まれるが、該当箇所は「10万円」と記す。Modelが出典名を捏造し得るほか、実在文書を引用しても、その主張が誤りである可能性がある。

- RAG：回答生成前に関連資料を検索してModelへ渡す構成。
- Retrieval Metadata：検索側が記録する文書ID、版、該当箇所等。Modelが作文した出典名とは区別する。
- Chunk：検索・表示の単位に分けた文書の一部分。
- Attribution：回答をどの資料へ結び付けるか。
- Claim support：引用箇所が、その回答中の個々の主張を本当に裏付けるか。
- Watermark：AI生成を識別するために生成Mediaへ付ける標識。特定Systemの発行者認証や内容の正確性とは別。

攻撃者は文書やMetadataの一部を書き換える、またはModelの回答へ影響する指示を注入することがある。Model自体も悪意なしに数値や出典を取り違える。Trust Boundaryは資料から検索Index、検索Metadataから出典表示、Model回答からUserの意思決定、生成Mediaから閲覧者の由来判断。

## 一本の線と別の枝

```text
RAG文書を検索
  → 検索Metadataから出典を構成【7.4.2】
  → 回答へ出典を示す【7.4.1】
  → 各主張と引用Chunkの対応を追う【7.4.3】

生成画像・音声等
  → AI生成を示すWatermark【7.4.4：別の枝】
```

Security Invariantは「Modelが出典の正本を作らない」「検索された文書と実際に示した引用箇所を追える」「出典が実在するだけで主張が正しいと推定しない」。Enforcement Pointは検索サービスのMetadata、アプリの引用組立て、回答公開前または評価時の主張とChunkの照合。主張の意味上の支持判定には不確実性が残るため、誤りの完全排除は主張しない。

具体設計では文書ID・版・Chunk IDを検索結果に持たせ、アプリが出典表示を構成する。Modelが生成した文書名を検索リストで照合するだけでは、出典の由来がModelでないことを保証しない。Metadata自体が信頼できるかも別途考える。

## Pass／FailとNegative tests

- Fail（7.4.2）：Modelへ本文だけを渡し、Modelが生成した「出典：経費規程」をそのまま表示する。
- 7.4.2をPassと評価できる構成例：出典表示が検索結果の文書ID・該当箇所のMetadataからアプリにより構成され、Modelに捏造できない。
- Fail（7.4.3）：出典文書が検索された事実だけを確認し、「100万円」という主張を「10万円」と記すChunkと照合しない。
- 7.4.4の限界：WatermarkでAI生成を示すことと、どの特定Systemが出したか、内容が真実か、改変されていないかは別。署名付き来歴Metadata等が提供する保証は方式・検証条件ごとに評価する。
- Negative test：存在しない出典、検索していない文書、実在するが数値が矛盾するChunkを提示し、由来と支持の異なる失敗を区別する。MediaではWatermarkの欠落・変換後の検出不能を試す。
- 正常系：正しく検索・引用した回答で、文書と該当箇所へ辿れる。生成Mediaで想定方式のWatermarkを検出できる。

## 対話の再構成

1. 問い：本文だけをModelへ渡し、出典名もModelに生成させる。学習者：「Fail」。整理：7.4.2は出典の生成主体を問う。
2. 問い：引用文書が検索結果にあったが、個々の主張と箇所を照合しない。学習者：「7.4.2はPass、7.4.3はFail」。訂正：7.4.3のFailは正しい。7.4.2は出典をアプリがMetadataから作ったならPassと評価できるが、Model生成の出典名が検索結果に存在したと後から確認するだけではPassと断定できない。問いの条件不足を明示した。
3. 所感：「要件は細かいが、Section全体、ひいてはCategoryを線として理解することが重要」。整理：7.4.1～3は検索・出典・支持の線で追える。7.4.4は別の枝。C7全体の各Sectionは直列処理ではなく評価軸。
4. 所感：「7.4はコーディング設計の内容になる」。整理：Controlは何を保証・検証するか、Engineeringは検索結果のData構造・組立て・照合・テストを具体化する。特定実装へControl本文を固定しない。
5. 問い：Watermarkがあれば内容も事実で改変されていないか。学習者：「Fail。内容の事実とは関係ない。そのSystemが出した事実だけ」。訂正：内容の正しさは証明しない。さらにWatermarkだけで特定Systemの発行や非改変まで証明できるとは限らない。AISVS 7.4.4が求める直接の対象はAI生成であることの標識。

## Derived insights・設計レビュー項目

> 出典の存在、出典の由来、主張の裏付けは、三つの異なる問い。

> Sectionを線で理解し、線に乗らない要件は別の枝として明示する。

- 出典表示の値をModelが生成・書換えできるか。
- 検索Metadataの文書ID、版、Chunk IDを回答から辿れるか。
- 出典の文書全体ではなく、主張を支える該当箇所を確認したか。
- Metadata自体の出所・改ざん耐性をどう扱うか。
- AI生成の識別と、発行者認証・非改変・事実性を混同していないか。

## References

- [C7.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-04-Source-Attribution-Citation-Integrity.md)
