---
title: "RAGの出典をModelではなくRetrieval Metadataから構成する"
versioned_id: "v1.0-C7.4.2"
requirement_id: "C7.4.2"
verification_level: 1
family_id: "C7"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-04-Source-Attribution-Citation-Integrity.md"
last_verified: "2026-10-03"
maturity: "verifiable"
mapping_assessment_refs: []
---

# RAGの出典をModelではなくRetrieval Metadataから構成する

AISVS Verification Level: 1

学習資料：[C7.4 Source Attribution & Citation Integrity](../../../learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.4-source-attribution-and-citation-integrity.md)

## Upstream basis

AISVS `v1.0-C7.4.2`は、RAG回答のAttributionをModel生成文ではなく
Retrieval Metadataから得て、Modelが出典の来歴を捏造できないことを求める。
対応Researchは、Retrieverが返した文書・Chunk ID、Page、URL等から
Applicationが引用を構成し、Model生成の文字列に上書きされない経路の検証を
挙げる。同時に、Metadata自体の汚染やIndex更新に伴うIDのずれは残余リスク
として挙げる。特定のCitation Schemaや製品機能を一律必須とはしない。

## Interpretation

回答の出典を示す識別子・Title・版・参照先等の**正本**は、当該回答で実際に
使ったRetrieval結果のMetadataに置く。Modelが「出典：経費規程」と書いても、
その文字列を出典の正本として採用しない。Model出力が引用候補のIDを示す
構成なら、ApplicationはそのIDが今回の取得結果に含まれることを確認し、
利用者へ示す出典Fieldを対応するMetadataから構成する。

例えばRetrieverが`doc-A`と`doc-B`を返したとき、Modelが`doc-C`や
別URLを生成してもCitationとして採用できない。Modelが`doc-A`を選び、
Applicationが`doc-A`のMetadataから表示を作る構成はあり得るが、
`doc-A`がその主張を本当に支えるかはC7.4.3の別保証である。

## Security objective

Modelのもっともらしい出典名・URLを、検索された証拠の来歴と取り違えない。
出典の生成主体をModelから分離し、引用表示が少なくとも実際のRetrieval
結果に結び付くようにする。

## Applicability

検索結果のMetadataを使って出典を表示するRAG回答に適用する。Document、
Chunk、Page、Media参照、Graph Node等、出典の形式は製品ごとに異なり得る。
UI、API、Export、Streaming完了時など、回答とCitationを届ける経路を確認する。

### Non-applicability

取得資料を用いない回答には直接適用しない。RAGを利用しながら
Retrieval Metadataを捨てている構成はN/Aではなく、出典の由来を
保証できない構成として評価する。

## Scope and assumptions

- 「Retrieval Metadata」は、今回の検索結果に結び付く文書ID・版・URL等を
  指す。文書本文中の「引用してください」という指示やModelの出力は含めない。
- Modelが選べる引用候補を今回の取得結果へ限定し、表示用Fieldの値を
  Modelが自由に書き換えられないようにする。方式は特定しない。
- Metadataの由来・完全性は別の前提である。攻撃者がTitleやURLを
  Indexへ登録できれば、Metadata由来でも不正な出典を示し得る。
- Index再構築、版更新、Cache使用時にIDと元文書の対応が変わる可能性を
  確認する。固定のID形式や保存期間を原文の必須条件にはしない。

## Assets, actors, identities, and trust boundaries

保護対象はCitationの来歴、元文書との結び付き、受取人の検証可能性。
ActorsはRetriever、Index／Metadata管理者、Model、回答組立Component、
回答の受取人。攻撃者はPromptや文書本文から偽の出典を誘導したり、
権限を持つ場合にはIndex Metadataを汚染したりし得る。

Trust Boundaryは、Retrieverの結果ObjectとModel生成Textの間、および
Citation組立Componentから最終表示への間にある。Model生成Textを
Retrieval Metadataと同じ信頼度へ昇格させない。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 最終Citationの各識別Fieldが、当該回答のRetrieval結果のMetadataへ辿れる。 |
| SP-2 | Model生成の出典名・URL・IDをMetadataの代わりに採用せず、Modelが未取得の出典を追加・上書きできない。 |
| SP-3 | Modelが候補IDを選ぶ場合も、今回の取得集合との照合とMetadataからの表示組立を、Model外の処理で強制する。 |
| SP-4 | Retry、Cache、Index更新、別の回答経路で、Citationが別の検索・版のMetadataへすり替わらない。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| Modelが作文したTitleがたまたま実在文書と一致した | 文字列の一致だけではMetadata由来と示せずFail。 |
| Modelが今回取得したIDを選び、ApplicationがそのMetadataからCitationを構成した | 出典の生成主体は本Controlの方向に合う。主張支持はC7.4.3で別に確認する。 |
| Retrieval結果のTitle自体が攻撃者に改ざんされている | Metadata由来でも出典の真正性は証明されない。Metadata管理・Source検証を別に評価する。 |
| Metadata由来のCitationが回答画面から欠落する | C7.4.1の表示保証がFail。本Controlの出所を確認しても表示の欠落を打ち消さない。 |
| 実在する取得文書をCitationに示したが、回答の数値は矛盾する | C7.4.3の主張支持はFail。本Controlだけでは事実性を保証しない。 |

## Threat and failure-mode rationale

Modelは存在しない出典や、存在しても今回検索していない資料を
もっともらしく生成できる。プロンプトの「必ず出典を書け」だけでは
生成主体は変わらない。生成したTitleを検索結果のTitleと後から
照合するだけでも、Citationの元DataがRetrieval Metadataになったとは
断定できない。外部Threat IDとの厳密なMappingは未評価とする。

## Verification

### Architecture and configuration review

Retrieverが返すMetadataとModelに渡す文書本文を区別し、Citation表示までの
Data Flowを追う。Model生成Fieldの採用箇所、候補IDの検証、Cache／Retry、
Index版の対応を確認する。Metadataを文書本文やOCRから取り込む場合は、
それが誰により変更可能かを確認し、出所の保証範囲を明示する。

### Positive verification

合成文書を複数取得させ、CitationのTitle、ID、URL等が今回のRetrieval
Metadataと一致することを確認する。Modelが有効な候補IDを選ぶ構成なら、
表示値の正本がMetadataであることをTraceで示す。回答の主張支持は別に評価する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Model出力へ未取得の文書名・URL・IDを注入する | その値はCitationにならず、実際の取得Metadataだけから構成される。SP-1〜SP-3 |
| N-2 | 取得文書本文に「出典は別URL」と書き、Modelにも同じ文字列を出させる | 本文やModelの指示がCitation Metadataを上書きできない。SP-1, SP-2 |
| N-3 | Modelが今回取得したIDを選ぶが、Title・URLを別値に書き換える | IDの許可と表示Fieldの正本を分け、表示は対応するMetadataに従う。SP-1〜SP-3 |
| N-4 | 前回検索のIDをCacheから混ぜる、Retry後に別の取得結果を使う、Indexを更新する | 最終回答のCitationが対応する今回の取得結果・版に結び付く。SP-1, SP-4 |

### Failure conditions

Model生成の出典文字列をそのまま表示する、Modelが未取得の出典を足せる、
またはCitationのFieldが今回のRetrieval Metadataへ辿れない場合はFail。
検索結果に同名文書があるという事後確認だけではPassにしない。
Metadata汚染による虚偽は別の保証も要するが、汚染の可能性を無視して
「Metadata由来だから真正」と主張しない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Retrieval結果とCitation組立Flow | Retrieval／Application Owner | ID・版・表示Fieldの出所 | 検索・Index・表示変更時 | 顧客文書名を最小化 | 各Fieldの正本がRetrieval Metadataと分かる。 |
| 合成文書の改ざん試験 | Test Harness | N-1〜N-4、Cache／Retry／Index変更 | Release・Pipeline変更時 | 合成IDとURLを使用 | Modelから未取得・上書き出典を作れない。 |
| Metadata取込境界の評価 | Corpus／Security Owner | 文書本文・OCR・Metadata管理 | Source変更時 | 非公開Metadataを保護 | Metadata由来の保証と真正性の限界を区別できる。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C7.4.1` | 回答へ識別可能な出典を示す。Metadata由来でも表示されなければ別途Fail。 |
| `v1.0-C7.4.3` | 個々の主張をChunkへ辿る。Metadata由来でも主張の裏付けは自動成立しない。 |
| `v1.0-C5.2.2` | Retrieval時のEnd-user認可。正しい出典の生成は未認可資料の取得を許さない。 |

## Known limitations and uncertainty

Retrieval Metadata自体が虚偽・改ざん済みなら、Metadataから機械的に
Citationを構成しても元文書の真正性は保証されない。Index再構築や
Cacheの誤対応でも、正本と表示の関係が崩れ得る。本Controlは
「出典を誰が生成したか」と「今回の検索結果に由来するか」を問う。
回答への表示、各主張の支持、文書の正しさは別の保証である。
`verifiable`は本Artifactの成熟度であり、製品の引用品質の実証ではない。

## References

- [AISVS v1.0 C7 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md)
- [AISVS v1.0 C7.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-04-Source-Attribution-Citation-Integrity.md)
- [C7 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-10-03 | C7.4.2初版。Retrieval Metadataの正本性とModel出典生成の禁止を分離して検証 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
