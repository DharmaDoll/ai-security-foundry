---
title: "RAG回答の主張を取得Chunkへ辿れるようにする"
versioned_id: "v1.0-C7.4.3"
requirement_id: "C7.4.3"
verification_level: 2
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

# RAG回答の主張を取得Chunkへ辿れるようにする

AISVS Verification Level: 2

学習資料：[C7.4 Source Attribution & Citation Integrity](../../../learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.4-source-attribution-and-citation-integrity.md)

## Upstream basis

AISVS `v1.0-C7.4.3`は、RAG回答の主張を取得したChunkまで追跡できることを
求める。C7.4の章目的は、引用された主張が取得Contentで検証可能な形で支えられる
ことである。対応Researchは、文書名だけを添えた事後的な引用、主体を取り違えた
根拠、話題は同じでも主張を支えない箇所を失敗例として扱い、主張単位で引用Chunkを
照合する方法を挙げる。Researchに列挙されたNLI・検出器・製品は実装・評価の
選択肢であり、特定技術の採用をこのRequirementの規範条件へ昇格させない。

## Interpretation

回答中の検証可能な主張から、それを支えるために当該回答で実際に取得した
Chunkの識別子・版・該当箇所へ辿れるようにする。出典文書全体へのリンクだけ、
または「検索集合のどこかに書いてある」は足りない。主張が複数のChunkを合わせて
成立するなら、使ったChunk集合と組合せの理由を追えるようにする。

例えば「経費承認上限は100万円」という回答に実在する経費規程を引用しても、
対応Chunkが「10万円」と記すなら支持の確認は失敗する。正しいChunk IDを
付けたことだけで意味上の支持まで実証したとは扱わない。一方、本Requirementは
全回答の事実性や、外部世界における元資料の真実性までは保証しない。

## Security objective

利用者・レビュー担当者・検証処理が、個々の主張と根拠の対応を再現して確認できる
ようにし、もっともらしい文書名による誤答の正当化を防ぐ。

## Applicability

取得Contentを根拠に事実的な回答を作るRAG経路に適用する。本文、表、OCR、
要約、再ランキング、親文書展開などを通る場合も、最終回答を支えるChunkと
対応する版を特定できる必要がある。UI、API、Export等の回答経路を含めて評価する。

### Non-applicability

Retrievalを使わず、取得Chunkを根拠とする主張もない回答には直接適用しない。
RAGを使いながらChunk識別子を保持していない構成はN/Aではなく、追跡可能性を
示せない構成として評価する。

## Scope and assumptions

- 「主張」は数値、主体、条件、時点等、根拠との対応を確認できる回答内容を指す。
  文法上の全断片へ機械的に引用を付けることは要求しない。
- 「取得Chunk」は当該回答のRetrievalで利用可能になった本文・位置・版の単位。
  後から検索して見つかった同名資料だけでは今回の根拠を証明しない。
- 複数Chunkの共同支持はあり得る。単一Chunkへの無理な切詰めも、無関係な
  Chunkを大量に並べることも、主張の支持を明瞭にしない。
- 意味上の支持を自動判定する精度には限界がある。方式や閾値は用途・Impactに
  応じて決めるが、追跡Linkの整合性だけを「内容検証済み」と表示しない。

## Assets, actors, identities, and trust boundaries

保護対象は回答の根拠の検証可能性と、誤答に基づく利用者・下流処理の判断。
ActorsはRetriever、Chunk／Index管理者、Model、回答組立・検証Component、
回答利用者。攻撃者は取得Contentを汚染したり、Modelに実在するが無関係な
Chunkを引用させたりし得る。善意のModelも数値・主体・版を取り違える。

Trust Boundaryは、取得ChunkとModel生成主張の間、主張とCitationの紐付けから
最終回答への間にある。Modelが生成した「根拠あり」という自己評価を、取得
Chunkによる裏付けと同一視しない。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 検証対象の各主張から、当該回答で取得した具体的なChunkまたは明示されたChunk集合へ辿れる。 |
| SP-2 | 対応にはChunk IDだけでなく、照合可能な本文・位置・版または同等のSnapshotがあり、Retry、Cache、Index更新後にも別の箇所へすり替わらない。 |
| SP-3 | そのChunkが主張の主体・数値・条件・時点を実際に支えるか評価でき、明白な矛盾や無関係な引用を「支持あり」として扱わない。 |
| SP-4 | 主張とChunkの対応が不明・破損・不足した場合は、対象主張を根拠付きとして公開・利用しない。代替表示や保留などの扱いを製品Policyで定める。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 取得文書名は表示されるが、どのChunkがどの主張に対応するか不明 | C7.4.1の表示があっても本ControlはFail。 |
| Citation FieldはRetrieval Metadata由来だが、主張とChunkの関係がない | C7.4.2だけでは不足し、本ControlはFail。 |
| IDの対応は正しいが、引用Chunkは別の社員や金額を述べる | 追跡できても支持の判定を誤っておりFail。 |
| 複数Chunkを合わせて主張が成立し、各Chunkと結合根拠を追える | 単一Chunkに限定せず評価できる。 |
| 対応Chunkは主張を支持するが、Chunk自体が汚染・古い、または未認可 | 本Controlの局所的なPassはあり得る。Source品質、更新、Retrieval認可は別に評価する。 |
| 一般的な雑談など、取得Chunkを根拠にしていない内容 | RAG根拠付き主張として偽装していなければ、本Controlの対象から分ける。 |

## Threat and failure-mode rationale

検索された文書が存在するだけでは、回答がその文書の該当箇所から導かれたとは
言えない。Modelは既知の知識から主張を先に作り、話題だけ近い文書を後付けで
引用し得る。主体や適用条件が違うChunkも、表面的にはもっともらしい根拠に
見える。外部Threat IDへの厳密なMappingは未評価とする。

## Verification

### Architecture and configuration review

Retrieverの結果から回答組立てまで、Chunk ID・文書版・Offset／Page・本文
Snapshotと主張の対応がどこで保持・確定されるかを追う。要約、再ランキング、
親文書展開、Cache、Streaming、Exportで対応が落ちないか確認する。Modelに
引用候補を選ばせる場合は、候補が今回の取得集合に含まれるかをModel外で
照合し、意味上の支持の確認を別の評価軸として説明できることを確認する。

### Positive verification

合成文書の異なるChunkに異なる主体・限度額を置き、回答の各主張から正しい
Chunkの版と該当箇所を再現できることを確認する。複数Chunkを使う主張では
取得集合と結合の理由を示す。追跡Linkの妥当性と意味上の支持を別々に記録する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 文書名だけを示し、個々の主張のChunk対応を消す | 根拠付きと判定しない。SP-1, SP-4 |
| N-2 | 「100万円」という主張へ「10万円」と記す取得Chunkを対応させる | IDが正しくても支持ありと判定しない。SP-3, SP-4 |
| N-3 | Aliceの条件を述べる主張へ、同じ話題だがBobの条件を記すChunkを対応させる | 主体の不一致を見落として支持ありとしない。SP-3 |
| N-4 | 未取得のChunkや前回のCache／Index版のChunkを引用候補に混ぜる | 今回の取得集合と版の照合で不一致を検出する。SP-1, SP-2, SP-4 |
| N-5 | 長い根拠を途中で切り、否定や例外条件を落としたChunkだけを検証する | 不足した根拠で支持ありとせず、必要な範囲を再確認する。SP-3, SP-4 |

### Failure conditions

主張から今回取得した該当Chunkへ辿れない、IDと本文・版がずれる、または
明白に支持しないChunkを根拠付きと扱う場合はFail。評価器のスコアが高い、
引用先URLが実在する、文書全体が検索された、というだけではPassにしない。
すべての事実誤認を検出できることはPass条件にしない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 主張からChunkへのData FlowとPolicy | RAG／Application Owner | 取得、組立て、表示、Fallback | Pipeline変更時 | 顧客本文・識別子を最小化 | 対応の作成・保持・失敗時の扱いを説明できる。 |
| 合成Corpusと支持／矛盾Test結果 | Test Harness／評価担当 | N-1〜N-5、主体・数値・条件の差 | Release・Index更新時 | 合成データで実施 | Chunkへ再現可能に辿れ、誤対応・明白な矛盾を支持としない。 |
| 取得と回答のTrace Sample | Retrieval／Application Owner | Chunk ID、版、主張、Citation | 運用の代表期間 | 本文やUser情報を保護し保持期間を制限 | 対象主張と取得Snapshotの対応を安全に再構成できる。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C7.4.1` | 出典文書を回答へ示す。表示があっても主張とChunkの支持は別。 |
| `v1.0-C7.4.2` | 出典FieldをRetrieval Metadataから構成する。正しい来歴でも主張支持は別。 |
| `v1.0-C7.2.1` | 回答全体の信頼性推定。個々の主張からChunkへの追跡を代替しない。 |
| `v1.0-C7.2.3` | Policy上High-risk回答の追加検証。適用時は本Controlの評価結果を一入力にできるが、同一保証ではない。 |
| `v1.0-C5.2.2` | Retrieval時のUser認可。主張を支持するChunkでも未認可取得を正当化しない。 |

## Known limitations and uncertainty

Chunkとの対応が正しくても、元文書の虚偽、汚染、失効、資料間の矛盾は残る。
支持判定には意味理解が必要であり、NLI・LLM評価器・類似度・人手レビューの
いずれも完全ではない。特に主体の入替え、否定、条件、長文の切詰め、複数箇所を
要する主張は見落とし得る。Researchは主張単位の自動判定を提案するが、Normative
本文は特定検出器や全回答でのリアルタイムNLIを義務付けていない。本Controlの
`verifiable`はArtifactの成熟度であり、製品の回答が全て正しい証拠ではない。

## References

- [AISVS v1.0 C7 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md)
- [AISVS v1.0 C7.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-04-Source-Attribution-Citation-Integrity.md)
- [C7 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-10-03 | C7.4.3初版。Claimから取得Chunkへの追跡と支持の確認を分けて検証 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
