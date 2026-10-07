---
title: "RAG回答に参照元文書への出典を示す"
versioned_id: "v1.0-C7.4.1"
requirement_id: "C7.4.1"
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

# RAG回答に参照元文書への出典を示す

AISVS Verification Level: 1

学習資料：[C7.4 Source Attribution & Citation Integrity](../../../learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.4-source-attribution-and-citation-integrity.md)

## Upstream basis

AISVS `v1.0-C7.4.1`は、RAGを使って生成したResponseに参照元文書への
Attributionが含まれることを求める。対応Researchは、引用が見えるだけでなく
取得文書のIDや参照先へ辿れるかを検証する例を挙げ、引用の存在だけでは
事実性を保証しないと注意する。Researchの特定Vendor機能、URL到達性の
自動検査、Streamingの最初のTokenからの表示は、一律の必須方式にしない。

## Interpretation

RAGで取得した資料を利用して回答するなら、そのResponseの受取人が
「どの元文書を参照したか」を特定できる出典を、実際の回答とともに示す。
例えば社内規程を使った回答なら、単なる「出典あり」という印ではなく、
対象の規程を識別できる名前・ID・版・アクセス可能な参照先等を、
利用形態に合う形で提示する。全てを同時に表示する必要はないが、
「規程」とだけ書かれて区別できない場合はAttributionとして不十分である。

本Controlは、出典が**示され、元文書へ辿れること**を問う。
その出典をModelが作文せずRetrieval Metadataから構成することはC7.4.2、
回答中の個々の主張が該当Chunkに支持されることはC7.4.3として分ける。
出典の表示だけを、正しい主張や真正な引用の証拠にしない。

## Security objective

利用者やReviewerがRAG回答の参照元を確認できないまま、流暢な回答を
根拠付きの事実として受け取る失敗を減らす。出典表示を、後続の
来歴・主張検証へ進むための入口とする。

## Applicability

文書、Record、Knowledge Base等を検索・取得し、その内容を回答生成に
使うRAGのResponseに適用する。User向けUIだけでなく、API、Export、
別Agentへの回答等、製品が「回答」として届ける経路を確認する。

### Non-applicability

取得資料を回答生成に使わない処理には直接適用しない。RAG機能を持つ
製品であっても、該当Responseが本当に検索を使ったかをTraceで確認して
判断する。引用を出したくないというUI方針だけではN/Aにしない。

## Scope and assumptions

- 「参照元文書」を識別できる粒度はCorpusによって異なる。版管理があるなら
  版の違いを識別できる方法を検討するが、原文は固定の表示Fieldを指定しない。
- 出典が含まれても、受取人にその文書への閲覧権限があるとは限らない。
  LinkやTitle自体の開示範囲は別途認可とData Policyに従う。
- Streamingの場合、受取人が完了したResponseを利用する時点で出典へ
  辿れることを確認する。最初のTokenに出典が付くことを一律に要求しない。
- 出典があるだけで、その文書を実際に検索したか、主張が支持されるか、
  文書内容が正しいかを証明したことにはならない。

## Assets, actors, identities, and trust boundaries

保護対象は回答を受け取る人の判断、参照元の識別可能性、監査可能な
回答と資料の関係。Actorsは質問者、Retrieval Component、Model、
回答組立・表示Component、資料管理者。攻撃者が取得文書を汚染する場合や、
Modelが出典らしい文字列を誤生成する場合がある。

Trust Boundaryは、取得された文書群からModelの回答へ、回答から受取人が
見るCitation表示へ移る地点。出典の表示と、出典の真正な生成経路は分ける。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | どのResponseがRAGを利用したかを識別でき、出典表示の対象範囲を確認できる。 |
| SP-2 | RAG利用Responseには、受取人が元文書を特定・参照できるAttributionが含まれる。 |
| SP-3 | 表示・API・Export等で回答とAttributionが分離・欠落せず、元文書への参照が辿れる。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| RAGで社内規程を読んだが、回答に出典がない | SP-2を満たさずFail。 |
| 「出典：社内文書」とだけ書き、どの文書か特定できない | 実用上のAttributionにならずFail。 |
| 出典表示はあるが、ModelがTitleを作文した | C7.4.2の生成主体の保証を満たさない。本Controlの出典実在性も別途確認する。 |
| 実在する文書を引用したが、回答中の数値は文書と矛盾する | C7.4.3等の主張支持の失敗。出典表示だけでPass範囲を広げない。 |
| 受取人に許されない文書名・LinkがCitationとして見える | Data開示・認可の別保証も失敗。本Controlのために権限を迂回しない。 |
| 回答の最後に正しい出典が付く | 最初のTokenにないだけではFailとしない。回答として利用される状態で確認する。 |

## Threat and failure-mode rationale

出典のないRAG回答は、利用者が原文を確認する入口を失い、Modelの誤りや
文書汚染を見抜きにくい。引用らしい文言があっても元文書を識別できなければ
同じ問題が残る。実在する出典の表示でも誤答は起こり得るため、
真偽の保証を本Controlへ過剰に含めない。外部Threat IDとの厳密なMappingは
未評価とする。

## Verification

### Architecture and configuration review

検索が使われる条件、取得文書の識別子、回答とCitationの組立・配送経路、
UI／API／Exportでの表示方式を追う。権限により元文書へ直接Linkできない
場合は、許可された範囲でどの資料かを識別・確認できる代替経路を確認する。

### Positive verification

代表的な質問で文書を取得して回答させ、受取人がResponseの出典から
実際の元文書を識別できることを確認する。複数の取得文書が関係する回答、
版の異なる同名文書、UIとAPIの両方を試し、出典と回答が揃って届くか見る。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | RAG回答からCitation表示だけを除去する | 出典の欠落を検出し、RAG回答を出典付きと誤認しない。SP-1, SP-2 |
| N-2 | 同名・別版の文書を取得し、曖昧なTitleだけを出典にする | 受取人が元文書を区別できるか確認する。区別不能ならFail。SP-2 |
| N-3 | Citationに存在しない、または今回の元文書ではない参照先を置く | 表示先を実際の参照元へ辿れず、Attributionを成立したと扱わない。SP-2, SP-3 |
| N-4 | UIではCitationを表示し、API／Export／Streaming完了時には落とす | 回答を利用する各経路で出典が残る。SP-1〜SP-3 |

### Failure conditions

RAG利用Responseに出典がない、出典表示が元文書を特定できない、
あるいは実際の回答配送経路でCitationが欠落する場合はFail。
URLの文字列が付くだけ、CitationがLogだけに残るだけではPassにしない。
出典が実在してもModel生成の出典を許すC7.4.2違反や、主張が裏付かない
C7.4.3違反を本ControlのPassで打ち消さない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| RAG利用・取得文書Trace | Retrieval／Application | 質問、取得文書、回答ID | Retrieval構成・Release変更時 | 質問・文書名を最小化 | RAG対象と元文書を追える。 |
| 出典表示・配送の試験結果 | Test Harness | N-1〜N-4、UI／API／Export | 回答Format変更時 | 合成文書を使用 | 実際の回答に識別可能な出典が含まれる。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C7.4.2` | 出典をRetrieval Metadataから得る。元文書を示しても、Modelが出典を作れる構成なら別途Fail。 |
| `v1.0-C7.4.3` | 各主張を取得Chunkへ辿る。Document-levelのAttributionだけでは主張支持を示さない。 |
| `v1.0-C7.2.1` | 生成回答の信頼性推定。出典表示の有無はConfidenceの代替ではない。 |
| `v1.0-C5.2.2` | 検索・組立時のEnd-user認可。出典を付けるために未認可文書を取得しない。 |

## Known limitations and uncertainty

Attributionがあっても、文書自体の品質、検索の適切さ、引用生成主体、
各主張の支持、回答の事実性は確定しない。権限が厳しいCorpusでは
出典の識別性とMetadataの非開示のTrade-offがある。その製品で許される
表示粒度を明示し、見かけ上のCitationで元文書へ辿れない場合を
Attribution成功としない。`verifiable`は本Artifactの成熟度であり、
製品の引用品質の実証ではない。

## References

- [AISVS v1.0 C7 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md)
- [AISVS v1.0 C7.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-04-Source-Attribution-Citation-Integrity.md)
- [C7 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-10-03 | C7.4.1初版。出典表示と生成主体・主張支持を分離した | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
