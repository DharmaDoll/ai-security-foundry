---
title: "RAG検索のQuery・取得文書・Knowledge Sourceを記録する"
versioned_id: "v1.0-C12.1.4"
requirement_id: "C12.1.4"
verification_level: 2
family_id: "C12"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-01-Request-Response-Logging.md"
last_verified: "2026-10-04"
maturity: "verifiable"
mapping_assessment_refs: []
---

# RAG検索のQuery・取得文書・Knowledge Sourceを記録する

AISVS Verification Level: 2

学習資料：[C12.1 Request & Response Logging](../../../learning/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.1-request-response-logging.md)

## Upstream basis

AISVS `v1.0-C12.1.4`は、RAG PipelineのRetrieval Eventについて、Query、
取得した文書、Knowledge Sourceを記録することを求める。対応Researchは、
攻撃を受けた文書がModelへ渡った経路を事後に追う必要性と、複数Sourceの
識別、Document ID・Score等の検証例を挙げる。またQueryや文書本文の
無制限なLog複製による機密性の問題を指摘する。Normative本文は特定の
Telemetry Schema、Score、Top-k、全文Document保存を指定しない。

## Interpretation

各RAG検索について、実際にRetrieverへ渡されたQueryと、その検索が返した
文書の識別情報、どのKnowledge Sourceから得たかを、後から同じ検索Event
として辿れるようにする。Userの元PromptとQuery Rewrite後の検索Queryは
同一とは限らない。監査対象は検索に使われたQueryであり、元Promptだけの
記録では置き換えられない。

例えば一つの回答が人事Indexと公開Indexを検索したなら、両方のQuery、
返された文書、Sourceの対応を区別して記録する。「３件取得」だけ、または
文書IDの一覧だけでSourceを示さないEventでは、どの資料がどこから
入ったか再構成できない。

Queryの正確な内容は、権限を絞った別のStoreへ置き、Retrieval Eventから
参照してもよい。その場合は必要な保存期間内に内容を復元できることを
確かめる。復元不能なHashだけでは「Queryを記録した」とは評価しない。
取得文書は全文複製を必須とせず、Document ID、版、Chunk ID等から
当時の対象を識別できるかを確認する。

## Security objective

RAGの回答へ混入した文書や検索範囲を事後調査できるようにし、汚染文書、
誤ったSource、意図しない検索の影響範囲を特定する材料を残す。同時に、
Queryや取得文書が新たなLog漏えい源になることを認識して扱う。

## Applicability

回答生成やAgentの処理のために文書等をRetrievalするRAG経路に適用する。
Keyword、Vector、Hybrid、Federated Search、Cache、Parent Expansion等、
検索方式によってEventの表現は異なってよい。複数Sourceと複数段階の
取得がある場合は、実際にContentを得た各検索を対象にする。

### Non-applicability

対象SystemにRAG検索が存在しない場合に限り、このRetrieval Event要件は
直接適用しない。RetrieverがCacheから返す、外部Serviceを利用する、
またはModelに検索を委ねるというだけでN/Aにしない。実際の取得があるなら
そのEventをどう記録するか評価する。

## Scope and assumptions

- Queryは検索時に使った表現を指す。Text、構造化Filter、Embedding等、
  実際のRetriever Inputが異なる場合は、検索を後から説明できる表現と
  その限界を記録する。User Promptを自動的にQueryと同一視しない。
- 「取得文書」は検索が返した対象を指す。文書本文の全量複製ではなく、
  後日も同じ対象・版へ辿れる識別子を用いる構成があり得る。
- Knowledge Sourceは論理的なIndex／Repository等の取得元。複数Tenant、
  Collection、版があり、それが識別に必要なら対応を保つ。Source名だけで
  文書の認可や真正性を証明したとは扱わない。
- Queryと取得文書が機微情報を含む場合、通常Eventと制限付きContent保管を
  分けてもよい。ただし参照が切れれば記録要件の証拠にならない。
- Session／Requestとの相関は調査上重要だが、C12.1.1のSession保証と
  C12.1.4のRetrieval項目を混同しない。

## Assets, actors, identities, and trust boundaries

保護対象は取得経路の再構成可能性と、Query・文書情報の機密性。Actorsは
利用者、Agent、Query Rewriter、Retriever、Index／Knowledge Source管理者、
Telemetry Store、調査者。攻撃者は文書を汚染し、検索QueryやSourceを
操作したり、広いLog閲覧権限を悪用したりし得る。

Trust Boundaryは、User／AgentからQuery生成、QueryからRetriever、
Retrieverから取得文書、RetrieverからTelemetry Store、Storeから
調査者への間にある。Modelが生成した「参照しました」という文章を、
Retrieverが返した結果の記録として採用しない。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 実際のRAG Retrievalごとに、検索へ渡したQueryを後から確認できるEventまたは有効な参照を残す。 |
| SP-2 | 各Eventで、返された文書を識別でき、必要に応じて当時の版・Chunkとの対応を辿れる。ゼロ件も結果として記録する。 |
| SP-3 | 各取得文書がどのKnowledge Sourceから返されたかを区別でき、複数SourceやCache／追加取得で対応が失われない。 |
| SP-4 | Eventと保護されたQuery参照が必要な期間に実際に検索・解決可能であり、元の処理との相関を確認できる。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 「３件取得」とだけ記録し、Query・文書・Sourceがない | 直接の指定項目が欠落しFail。 |
| 元のUser Promptだけ残し、Retrieverへ送ったRewrite済みQueryがない | 実際の検索Queryを再構成できなければFail。 |
| QueryのHashだけ残し、本文や同等の検索表現を復元できない | Query記録のPassは主張できない。 |
| Queryを制限付きStoreに置き、Eventの参照から期間内に復元できる | 参照整合性と権限を確認したうえでPass候補。 |
| 文書ID・版・Sourceを記録し、本文は元Storeから同一版で確認できる | 全文のLog複製なしでも取得対象を辿れる。 |
| 文書名は残るが、更新後に当時の版を区別できない | 取得対象の再現に限界があり、識別可能性を再評価する。 |
| 正しい検索Logがあるが未認可文書を取得した | 本Controlの記録がPassでも、Retrieval認可はC5・C8の別保証でFail。 |
| 文書IDは正しいがModelのCitationが別文書を示す | C7.4の出典・主張支持を別に評価する。 |

## Threat and failure-mode rationale

取得文書はModelが見た非信頼の入力である。Query、文書、Sourceのどれかが
欠けると、Prompt Injectionや汚染文書がどの検索を通じて入ったか、どの
利用者に影響したかを追いにくい。逆に、全Query・全文書を一般運用Logへ
コピーすると、Log閲覧者や侵害者へ機密情報が集中する。外部Threat IDとの
厳密なMappingは未評価とする。

## Verification

### Architecture and configuration review

User PromptからQuery Rewrite、Retriever、Cache、Index、Parent Expansion、
Result Assemblyまでを追い、どの段階のQueryと結果をEventへ記録するか
確認する。Document ID・版・Sourceの正本、Query Contentの保管場所、
参照のRetention、Session相関、Log閲覧権限を点検する。特定OTel属性や
Scoreの採用を一律のPass条件にはしない。

### Positive verification

二つのKnowledge Sourceに異なる文書を置き、Query Rewriteを含む合成RAG
処理を実行する。保管Eventから、実際に送った各Query、返された文書と
Source、元のRequestを再構成する。ゼロ件検索とCache経路でもEventが
残ることを確認する。Queryを別Storeに置く場合は、許可された調査者が
参照を解決できることを試す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | QueryをRewriteした後、元PromptだけをLogへ残す | 実際のQuery欠落を検出する。SP-1 |
| N-2 | 異なるSourceで同じ文書IDを返し、Source Fieldを消す | 文書の取り違えを検出する。SP-2, SP-3 |
| N-3 | 取得件数のみ残す、またはIndex更新後に文書IDが別版を指す | 当時の対象を特定できないことを検出する。SP-2 |
| N-4 | Queryを別Storeへ移した後、参照を削除または早期失効させる | 必要な期間のQuery再構成が失敗し、SP-1, SP-4の証拠にならない。 |
| N-5 | Cache HitやParent Expansionで新しい文書を得るが、初回検索だけ記録する | 実際の取得経路の欠落を発見する。SP-2, SP-3 |
| N-6 | 未認可の運用RoleでQuery本文や機密文書のLogを読む | Log保護の別保証として拒否し、過剰記録を発見する。 |

### Failure conditions

対象のRetrieval Eventがない、実際のQueryが後から確認できない、取得した
文書やSourceを識別できない、または分離したContent参照が切れて必要な
期間の調査に使えない場合はFail。Hashだけを残して復元不能なQueryは
本Requirementの「queryを記録する」証拠にはならない。Score・Top-k・
特定Telemetry Schema・全文DocumentのLog複製がないことだけをFailと
しない。Log閲覧・保持の不備は別の重大な問題として報告する。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Retrieval Event設計とData Flow | RAG／Telemetry Owner | Query Rewrite、Retriever、Cache、複数Source | Pipeline・Index変更時 | Query本文・文書内容は必要最小限に | Query、文書、Sourceの正本と保管先が分かる。 |
| 合成RAGのEnd-to-end Trace | Test Harness／Collector | N-1〜N-5、ゼロ件・追加取得 | Release・Retriever変更時 | 合成Query・文書を使用 | 保管Eventから各検索のQueryと文書・Sourceを再構成できる。 |
| 保護されたQuery参照・閲覧試験 | Telemetry／Security Owner | Content分離、参照、N-4・N-6 | Retention・権限変更時 | 閲覧監査と保存期間を制限 | 許可された調査者が必要期間だけ復元し、非許可者は読めない。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C12.1.1` | AI InteractionのSession Context。検索項目を持っても元処理へ結び付けられなければ調査は困難。 |
| `v1.0-C12.1.3` | AI推論EventのModel／Provider／Token等の共通Schema。Retrieval Eventの指定項目とは別。 |
| `v1.0-C5.2.2`／`v1.0-C8.1.3` | Retrievalの認可・Scope強制。記録だけでは権限外取得を防げない。 |
| `v1.0-C7.4.2`／`v1.0-C7.4.3` | 出典のMetadata由来と主張からChunkへの対応。Retrieval Logだけでは表示・支持を証明しない。 |

## Known limitations and uncertainty

取得文書のIDとSourceが残っていても、元文書の版が失われれば当時のContentを
再現できないことがある。Queryを保護された別Storeへ移すと、閲覧権限・
Retention・参照整合性の運用負担が増す。Vector Query等で人が読める
検索Textがない場合、何をQueryとして保存すれば調査に十分かはSystem依存。
Researchが提案するOTel属性、Score、全文のOpt-inは補助情報であり、
Normativeの指定３項目と同一ではない。`verifiable`は本Artifactの成熟度
であり、実製品のLog品質やRetrieval認可を証明しない。

## References

- [AISVS v1.0 C12 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md)
- [AISVS v1.0 C12.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-01-Request-Response-Logging.md)
- [C12 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-10-04 | C12.1.4初版。実際のQuery・取得文書・Sourceの再構成とLog内Contentの扱いを分離 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
