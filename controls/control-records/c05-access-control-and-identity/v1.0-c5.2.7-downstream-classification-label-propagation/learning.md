---
title: "AISVS v1.0-C5.2.7 Downstream Classification Label Propagation Learning Note"
document_kind: "requirement-learning-note"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
requirement_id: "C5.2.7"
verification_level: 3
research_last_researched: "2026-07-14"
last_updated: "2026-09-07"
---

# C5.2.7 Downstream Classification Label Propagation 学習ノート

[Control本文：解釈・検証・証拠・限界](README.md)


## この文書について

この文書は、AISVS `v1.0-C5.2.7`を題材に行った学習セッションを、後から単独で
参照できる講義として再構成したものである。

これはControl本文、製品の適合判定、またはAISVS原文の代替ではない。次を分離する。

- **Normative:** AISVS v1.0が実際に要求していること。
- **Research:** AISVS Researchが示すThreat、Verification、実装上の注意。
- **Repository interpretation:** 現場のArchitecture Reviewへ適用するための解釈。
- **Derived insight:** 具体例と質疑から得た、Requirement外を含むSecurity上の洞察。

学習の完了によってControl maturityは変更しない。
別途整備した[Control本文](README.md)
では、適用範囲、検証、Evidenceと保証の限界を整理している。

## 1. Normative Requirement

- Versioned ID: `v1.0-C5.2.7`
- AISVS Verification Level: `3`

> Verify that data classification labels propagate to downstream resources
> (embeddings, prompt caches, model outputs).

意味を崩さない日本語訳:

> Data Classification Labelが、Embedding、Prompt Cache、Model Output等の下流Resourceへ
> 伝播することを検証する。

原文が直接要求するのは、元DataのClassification Labelが、AI Pipelineで形を変えた後に
失われないことである。特定のLabel体系、Vector Database、DLP製品、Metadata schema、
Policy Engineを指定していない。

## 2. C5における位置づけ

C5.2.7は、Dataの形が変わる境界で、必要なProtection stateを維持するRequirementである。

```text
C5.2.2:
  Retrieval／Assemblyの各段階でEnd UserのAuthorizationを維持する

C5.2.3:
  Sensitive DataをModel Weightへ固定せずRetrievalで扱う

C5.2.4:
  Unauthorized DataをRequesterへのOutputから除外する

C5.2.7:
  加工されたDataにもClassification Labelを失わずに引き継ぐ
```

このRequirementを一言で表すなら、次である。

> Dataを加工しても、そのDataに必要な保護レベルを失わせない。

ClassificationはAuthorization DecisionのInputになり得るが、Classification Labelが存在する
だけでAccessを拒否できるわけではない。PropagationとEnforcementを分けて評価する。

## 3. 最初に一つの具体Scenarioを見る

人事Documentに`Restricted`というClassification Labelが付いている。

```text
Original document
  id: doc-123
  classification: Restricted
  tenant: company-a
  retention: 7 years
```

RAG PipelineはDocumentをChunkへ分割し、Embeddingを作り、Vector Databaseへ保存する。

```text
Restricted document
  -> Chunk 1
  -> Chunk 2
  -> Chunk 3
  -> Embeddings
  -> Vector Database
```

### Failure-proneな構成

Derived ChunkにはText、Embedding、Source IDだけが保存される。

```json
{
  "chunk_id": "chunk-456",
  "source_id": "doc-123",
  "text": "Alice's performance rating is ...",
  "embedding": [0.12, 0.45, 0.98]
}
```

`Restricted` LabelはChunkへ引き継がれていない。別のPipeline、Cache、Export、Evaluation、
BackupがこのChunkを利用したとき、必要なProtectionを判断できない。Vector検索がLabelを
前提にAccess trimmingする設計でも、対象LabelがなければControlを適用できない。

```text
Restricted source
  -> unlabeled chunk
  -> unlabeled embedding
  -> lower-protection path
  -> unauthorized disclosure or retention failure
```

これはC5.2.7の典型的なFailである。

### Labelを伝播する構成

```json
{
  "chunk_id": "chunk-456",
  "source_id": "doc-123",
  "source_label_version": 7,
  "classification": "Restricted",
  "tenant": "company-a",
  "retention": "7-years"
}
```

ChunkとEmbeddingに明示的なClassification bindingがあり、SourceとのLineageも維持する。
Downstream Consumerは、Artifact単体から必要なProtectionを判断し、必要ならAuthoritative
Sourceの最新状態を確認できる。

## 4. 用語

### Data Classification Label

Dataに必要なProtection LevelまたはHandling Ruleを示すMetadata。組織によって、例えば次の
区分を定義する。

```text
Public
Internal
Confidential
Restricted
```

AISVS原文は具体的なLabel体系を定義していない。Repositoryでは、組織が承認したData
Classification Policyに基づき、Downstream Consumerが機械的にProtectionを選べるLabelを
対象とする。

### Classificationと隣接Metadata

次は関連するが、同じ概念ではない。

- **Classification:** Dataにどの程度のProtectionが必要か。
- **Authorization attribute:** 誰がDataをRead、Write、Exportできるか。
- **Tenant metadata:** DataがどのTenantへ属するか。
- **Purpose limitation:** 何の目的で利用できるか。
- **Retention metadata:** いつまで保持し、いつ削除するか。
- **Provenance／Lineage:** どのSourceから生成されたか。

AISVS Researchは、Source LabelとともにLineage、Tenant、Purpose、Retention等の関連Metadataも
確認するよう補足している。これらをすべて`classification`という一つのFieldへ押し込まず、
意味とEnforcementを分けて設計する。

### Downstream Resource／Derived Artifact

Source Dataの変換、検索、利用から生成された下流Resource。C5.2.7はEmbedding、Prompt Cache、
Model Outputを明示例として挙げるが、それらだけに限定されない。

### Chunk

DocumentをRAG検索等のために分割したText単位。Source DocumentにLabelがあっても、Chunkが
Labelを失えば、Vector検索やPrompt Assemblyで適切なProtectionを選べない。

### Embedding

Text、Image等を数値Vectorへ変換したDerived Artifact。人間に直接読めるTextでなくても、
検索、類似性、復元可能性、Sourceとの関連を持つため、無条件にPublicとは扱わない。

### Prompt Cache

Prompt処理、中間状態、またはResponseを再利用するCache。Tenant AのRestricted Contextから
作られたEntryをTenant Bへ再利用すると、Source側のAccess Controlを迂回し得る。

### Model Output

ModelがSource Dataを要約、変換、結合して生成したResponseまたはArtifact。新しい文章である
ことは、新しいProtection Levelを自動的に意味しない。

### Label Propagation

SourceのClassification stateを、Derived Artifactが明示的に引き継ぐこと。最も検証しやすい
方法は、ArtifactへLabelとSource Label VersionをMaterializeすることである。

専用のClassification Referenceを使う間接方式もあり得るが、単なる`source_id`をLabelとして
扱わない。間接方式を採用するなら、Reference自体がClassificationを明示し、改ざん不能で、
すべてのConsumerが利用前に必ず解決し、解決失敗時にFail closedする必要がある。この扱いは
AISVS原文が実装形式を指定していないことに対するRepository interpretationである。

### Reclassification／Declassification

- **Reclassification:** Dataの内容、Context、Policy変更に基づきClassificationを変更すること。
- **Declassification:** 承認された手続きによってProtection Levelを下げること。

Modelの自己判断だけでLabelを下げない。Protectionを弱めるTransitionには、Trusted Authority、
定義されたRule、必要なVerificationとEvidenceを要求する。

## 5. Threat ModelとTrust Boundary

### Attacker capability

このRequirementでは、次のFailureまたはAttacker capabilityを考える。

- Malicious DocumentまたはData ProducerがLabelを欠落、改ざん、Down-labelする。
- Ingestion、Chunking、Embedding、Cache PipelineにLabel処理の実装不備がある。
- Prompt Injection等でModelへ自己分類やDeclassificationを行わせる。
- TenantまたはUserが、別のClassificationを持つArtifactをCacheから取得する。
- Source Labelの変更後も、古いDerived Artifactが低いProtectionのまま残る。
- Export、Evaluation、Logging、Backup等のSecondary pathがLabelを捨てる。

### 保護対象

- Source Dataに必要なConfidentiality、Integrity、Retention、Handling condition。
- Chunk、Embedding、Prompt Cache、Model Output等のDerived Artifact。
- Label、Label Version、Classification Reference、LineageのIntegrity。
- Labelに基づくAuthorization、Storage、Export、Retention Controlの入力。

### 主なTrust Boundary

1. Source RepositoryとIngestion Pipeline。
2. IngestionとChunking／Embedding Service。
3. Transformation PipelineとVector Database／Cache。
4. RetrievalとPrompt Assembly／Model Context。
5. Model OutputとResponse、Cache、Log、Export先。
6. Authoritative Classification Serviceと各Downstream Consumer。
7. Label変更Eventと既存Derived Artifactの更新／Invalidation処理。

## 6. Security Invariant

平易な言葉で表す。

> Dataから生成されたArtifactは、信頼された再分類または機密解除が行われない限り、Sourceより
> 弱いProtectionで扱われてはならない。

具体的には、次を要求する。

- Derived ArtifactがSourceのClassification bindingとLineageを失わない。
- Label欠落または解決不能なArtifactをPublicとしてDefaultしない。
- 複数Sourceを組み合わせたOutputが、もっとも強いProtection conditionを失わない。
- Labelを下げる場合、Modelの自己判断ではなくTrusted Reclassificationを通す。
- Source Labelの変更後、定義した時間内にDerived Artifactへ反映またはInvalidationする。

「もっとも強いProtection」は、単一の上下関係だけで決まらない場合がある。Tenant、Region、
Purpose、Retention等が異なるなら、必要な条件を結合し、一つを選ぶことで他を失わない。

## 7. Classificationの結合と信頼された再分類

### 複数Sourceの結合

```text
Public source
  +
Restricted source
  -> Combined summary
```

このSummaryを、Public Dataが多数を占めるという理由でPublicにしてはならない。Restricted
Sourceの情報を含む限り、原則としてRestrictedのProtectionを引き継ぐ。

### Modelによる自己分類

```text
Restricted employee records
  -> LLM summary
  -> LLM says "No PII found"
  -> Internal
```

LLMはDataを変換できるが、Protection Levelを下げるAuthorityにはしない。間接識別子、複数
属性の組合せ、Domain固有のSensitive informationを見逃す可能性があり、判断も確率的だから
である。

### 信頼された再分類

```text
Restricted employee records
  -> approved deterministic aggregation
  -> identifiers removed
  -> minimum cohort rule verified
  -> re-identification negative tests
  -> Data Owner approval
  -> Internal result with lineage
```

このようなProcessを通じて、Outputへ新しい`Internal` Labelを付与することはPassし得る。
Label Propagationは同じ文字列を永久にコピーすることではなく、Protection stateをTrusted
Transitionなしに弱くしないことである。

De-identificationやRe-identification Testの正しさ自体はC5.2.7だけでは保証しない。誤った
Trusted ProcessがInternalと判定した場合、Label管理は存在してもData Protection全体はFail
し得る。

## 8. 決定論的なEnforcement Point

Label PropagationはDataが形を変える境界ごとに強制する。

```text
Source
  -> Ingestion gate
  -> Chunking
  -> Embedding generation
  -> Vector storage
  -> Retrieval
  -> Prompt assembly
  -> Model output
  -> Cache／Log／Export
```

### Ingestion Gate

- Authoritative Source Label、Label Version、Lineageを取得する。
- Labelが必要なのに欠落しているDataをRejectまたはQuarantineする。
- UserやModelが申告したLabelを無条件にAuthoritativeとしない。

### Transformation／Storage Write Gate

- Chunk、Embedding、Summary等へClassification bindingを付与する。
- 必須LabelまたはReferenceがないArtifactをDownstream StoreへCommitしない。
- 複数SourceのProtection conditionを失わずに結合する。

### Retrieval／Response PEP

- ClassificationとRequesterのAuthorizationを照合する。
- Model Context、Citation、Attachment、Structured Outputへ同じProtectionを適用する。
- Label解決不能時にUnfiltered RetrievalまたはResponseへFail openしない。

### Cache／Secondary-use Boundary

- Tenant、Classification、Authorization Contextが異なるEntryを共有しない。
- Evaluation、Logging、Feedback、Export、BackupでLabelを落とさない。
- Cache keyだけでなく、Cache Entry自体にClassification bindingとLineageを持たせる。

## 9. Label PropagationとEnforcementを分ける

次のSystemを考える。

```text
Restricted source
  -> Restricted chunk
  -> Restricted embedding
  -> Restricted model output
  -> Response API ignores label
  -> every user can read
```

この場合、C5.2.7のLabel PropagationはPassし得る。一方、System全体のAuthorizationはFailする。
特にPost-inference ResponseではC5.2.4等のEnforcementを別途評価する。

```text
Classification:
  このDataにはどのProtectionが必要か

Authorization:
  このRequesterへ、このDataを渡してよいか

Enforcement:
  Deny Decisionを実際のData flowへ強制する
```

> LabelはAuthorization Decisionの材料であり、LabelそのものがAccessを拒否するわけではない。

逆に、現在のApplicationが別の条件でAccessを正しく拒否していても、Derived Artifactから
Labelが失われていればC5.2.7にはFailする。別Consumerへ移動したときにProtection stateを
復元できないためである。

## 10. Direct LabelとSource IDを区別する

次のDerived Chunkは`source_id`だけを持ち、利用時にAuthoritative Classification Serviceへ
問い合わせる。

```text
Derived chunk
  source_id: doc-123
  classification: absent

Trusted PEP
  -> doc-123の現在Labelを取得
  -> Label取得失敗時はDeny
```

このAccess pathのAuthorizationは正しく動き得る。しかし、汎用的な`source_id`はLineageで
あり、Classification Labelではない。Chunkが別Consumer、Backup、Export、Evaluationへ渡ると、
必要なProtectionを単体で判断できない。RepositoryではC5.2.7をFailと評価する。

先の講義では、Trusted LineageからLabelを解決できればPassし得ると広く説明した。しかし、
genericなSource IDだけをLabel Propagationとみなすのは緩すぎるため、対話後に訂正した。

間接方式を認める場合も、少なくとも次が必要である。

- `classification_ref`等、Classificationを明示する専用Binding。
- Label namespaceとVersion。
- ArtifactからBindingを分離または改ざんできないIntegrity。
- すべてのConsumerでのMandatory resolution。
- Resolution failure時のFail-closed behavior。

検証可能性とPortabilityを優先する場合、Materialized LabelとTrusted Lineageの両方を保持する
方が明確である。

## 11. Label LifecycleとFreshness

Source Labelは後から変更され得る。

```text
Monday:
  document = Internal

Tuesday:
  incident reviewでRestrictedへ変更
```

Embedding、Prompt Cache、Model Output Cacheが古い`Internal`のままなら、作成時のPropagationは
成功しても、現在必要なProtectionと一致しない。

次を設計する。

- Label変更Eventによる再同期。
- Derived ArtifactとCacheのInvalidationまたは再分類。
- Index更新までの最大遅延。
- Source Label Versionと更新時刻。
- 更新失敗時のQuarantineまたはFail-closed behavior。
- Backup、Export、Evaluation Dataset等のLong-lived copyへの伝播。

AISVS原文は一律の更新時間を定めていない。Repositoryでは、SourceのClassificationが強く
なった後に古いProtectionで利用できる時間を明示し、RiskとSystem capabilityに基づいて
妥当性を評価する。

## 12. Pass／FailとScope Calibration

| Scenario | C5.2.7 | 理由 |
|---|---|---|
| Restricted DocumentのChunkとEmbeddingがLabelを失う | Fail | Downstream ResourceへClassificationが伝播していない |
| Labelは伝播するがResponse APIが無視する | Passし得る | Propagationは成立するがAuthorization／Enforcementは別途Fail |
| Chunkがgenericな`source_id`だけを持つ | Fail | Lineageだけであり、Classification bindingを持たない |
| ExplicitなClassification Referenceを持ち、全Consumerが必ず解決する | Passし得る | Repository interpretationとして間接的なLabel bindingになり得る |
| Restricted SourceをLLMの自己判断だけでInternalへ下げる | Fail | Trusted ReclassificationなしにProtectionを弱めている |
| 承認済みAggregationとNegative Test後にInternalへ再分類する | Passし得る | Trusted Transitionによって新しいLabelとLineageを付与している |
| PublicとRestrictedを結合したOutputをPublicにする | Fail | Restricted SourceのProtectionを失っている |
| SourceをRestrictedへ変更したがCacheはInternalのまま | Failし得る | 定義したFreshness boundaryを越えて古いProtectionが残る |
| Labelは正しいが元DataのClassification自体が誤っている | C5.2.7単独ではPassし得る | PropagationとSource classification correctnessは別Property |

ここで`Passし得る`はSystem全体の安全を意味しない。C5.2.7のLabel Propagationだけを評価した
Scope上の表現である。

## 13. ApplicabilityとNot Applicable

C5.2.7はSystem仕様によってNot Applicableになり得る。例えば、次が確認できる場合である。

- In-scope Sourceが、組織のAuthoritative Classification上すべてPublicである。
- User固有またはTenant固有のNon-public Dataを受け取らない。
- Tool、Memory、Feedback、EvaluationからNon-public Dataを取り込まない。
- Prompt Cache、Model Output、Log、ExportにもNon-public Dataが生成または混入しない。
- 将来Non-public Dataを取り込む変更時にApplicabilityを再評価するGateがある。

ただし、「Internetで閲覧できる」と「組織のClassification上Public」は同じではない。
公開SourceにもPersonal Data、利用条件のあるData、組織内で取扱制限すべきDataが含まれ得る。
また、複数の公開情報を結合し、個人の健康状態、行動、位置等のSensitiveな属性を推論する
場合、Derived OutputまでPublicとは限らない。

### Publicが正式なLabelである場合

組織が`Public`を正式なClassification Labelとして管理し、ConsumerがそのLabelをProtection
Decisionに使うなら、対象外とせず`Public` LabelのPropagationを検証する方が自然である。

```text
Source: Public
  -> Chunk: Public
  -> Embedding: Public
  -> Output: Public
```

これにより、AuthoritativeなPublic判定と、単なるLabel欠落を区別できる。

### N/A判断に残す情報

N/Aは「今のSample Dataに秘密がなかった」という結果ではない。少なくとも次を簡潔に残す。

- In-scope Data flowとResource。
- 使用するClassification Policy。
- Publicと判断したAuthority。
- User Data、Tool Result、Cache、Output、Secondary useを含む確認範囲。
- Applicabilityを再評価するChange trigger。

> C5.2.7のN/AはInputだけでなく、Output、Cache、User Data、Tool Resultを含むData flow全体で
> 判断する。

## 14. VerificationとNegative Test

### Architecture review

1. Authoritative Source LabelとClassification Policyを特定する。
2. SourceからChunk、Embedding、Cache、Prompt、Output、Log、ExportまでData flowを描く。
3. Dataが形を変えるTransformation Boundaryを列挙する。
4. 各ArtifactのLabel、Label Version、Lineage、更新方法を確認する。
5. 複数SourceのLabel compositionとDeclassification pathを確認する。
6. Label変更後の再同期、Invalidation、最大遅延を確認する。
7. N/Aなら、すべてPublicと判断したScopeとChange triggerを確認する。

### Positive verification

- Restricted Sourceから作ったすべてのChunkとEmbeddingがClassification bindingを持つ。
- Authorized ConsumerがLabelを解決し、期待したProtectionを適用できる。
- 複数SourceのOutputが必要なProtection conditionを保持する。
- 承認されたReclassification後、新しいLabelと元Source Lineageが残る。
- Source Label変更後、定義した時間内にDerived Artifactが更新またはInvalidationされる。

### Negative verification

- Labelを削除したChunkまたはEmbeddingをPipelineへ投入する。
- Missing Labelを`Public`としてDefaultさせようとする。
- Source ID、Classification Reference、Label Versionを改ざんする。
- RestrictedとPublicのSourceを結合し、OutputをPublicへDown-labelする。
- Prompt InjectionでModelへ`classification=Public`を出力させる。
- TenantまたはClassificationの異なるCache Entryを再利用する。
- SourceをRestrictedへ変更し、古いCacheまたはEmbeddingを利用する。
- Label ServiceをUnavailableにし、Unlabeled pathへFail openさせる。
- Export、Evaluation、Logging、BackupでLabelを落とす。

TestはLabel Fieldの存在だけで終わらせず、Sourceから各Derived Artifactまで同じDataを追跡する。
ただし、Authorization Enforcementの成否はC5.2.7とは分けて報告する。

## 15. AISVS Level 3について

AISVSは、C5.2.7をLevel 3とした個別理由をNormative chapterまたはC5.2 Researchで説明して
いない。次はRepository上の推論である。

- Labelを一つのDatabase FieldではなくEnd-to-end Data flowで維持する必要がある。
- Chunk、Embedding、Prompt Cache、Model Output等、AI固有のDerived Artifactを扱う。
- 複数SourceのLabel compositionとTrusted Reclassificationが必要になる。
- Source Label変更とLong-lived Cache／IndexのFreshnessを管理する。
- Third-party Model、Vector Store、Logging、Evaluation等のBoundaryをまたぐ。
- すべてPublicのSystem等、Applicabilityが仕様に強く依存する。

この実装難易度と状況依存性は、AISVSが示すLevel 3の一般的な説明と整合する。特に
Non-public Dataを扱うRAG、Agent、Long-term Memoryでは、Level 3であっても初期Data
Architectureから考慮する価値がある。

## 16. このRequirementだけでは保証しないこと

C5.2.7にPassしても、次は別途評価する。

- Source Dataへ正しいClassificationが付いていること。
- LabelとClassification Referenceが改ざんされないこと。
- RequesterのIdentityとAuthorization Contextが正しいこと。
- Labelに基づくAccess Controlが実際に強制されること。
- Post-inference FilteringがUnauthorized Dataを除外すること。
- De-identification、Aggregation、Reclassification ProcessがSecurity上正しいこと。
- Embedding、Cache、OutputのEncryption、Retention、Deletionが適切であること。
- Prompt Injection、RAG Poisoning、Cache Poisoningそのものを防ぐこと。
- Data Classification Policy自体が法令、契約、Business Riskへ適合すること。

> 正しいLabelが存在することと、そのLabelに従ってSystemが正しく行動することは別である。

## 17. 質疑の再構成

### 問い1: Labelは伝播するがResponse APIが無視する

**Scenario:** Restricted LabelはSourceからChunk、Embedding、Model Outputまで伝播する。
しかしResponse APIはLabelを確認せず、すべてのUserへOutputを返す。

**学習者の判断:** C5.2.7はPass。System全体のAuthorizationはFail。

**整理:** 正しい。ClassificationはAuthorization DecisionのInputであり、それ自体がAccessを
拒否するわけではない。PropagationとEnforcementを別のSecurity Propertyとして評価する。

### 問い2: ChunkにLabelはなく、Source IDから毎回解決する

**Scenario:** Restricted Sourceから作ったChunkは、改ざん不能な`source_id`だけを持つ。
Trusted PEPは利用前にAuthoritative Classification Serviceから現在Labelを取得し、取得失敗時は
Denyする。

**学習者の判断:** Fail。ChunkにClassificationを設定していないため、適切なControlを行えない。

**整理:** C5.2.7はFailとする。特定PEPのAccess pathは正しく動き得るが、genericなSource IDは
LineageでありClassification Labelではない。Chunkが別Consumerへ移動した場合、Protectionを
判断できない。

**講義側の訂正:** 当初はTrusted Lineageによる毎回のLabel解決を広くPass候補と説明したが、
Source IDだけをLabel Propagationとみなすのは緩すぎた。ExplicitなClassification Referenceを
間接Labelとして認める場合の最低条件を別途明確化した。

### 問い3: Model自己判断とTrusted Declassification

**Scenario A:** Restricted Employee RecordをLLMが要約し、LLM自身が「Personal Dataはない」と
判断してOutputをInternalへDown-labelする。

**学習者の判断:** Fail。Labelを検証していない。

**整理:** 正しい。より厳密には、Trusted Reclassificationを通さず、Classification Authorityで
ないModelの自己判断でProtectionを弱くしたことがFailureである。

**Scenario B:** 承認済みの決定論的Aggregation、Identifier除去、Minimum cohort rule、
Re-identification Negative Test、Data Owner承認を通じてInternalへ再分類する。

**学習者の判断:** Pass。

**整理:** Passし得る。Trusted Transitionによって新しいLabelを付け、Lineageを維持している。
ただし、De-identificationの正しさ自体はC5.2.7以外のData Protection評価も必要である。

### 問い4: 公開情報だけを扱うSystem

**学習者の所感:** 仕様によってはC5.2.7が対象外になるCaseも多い。例えば公開情報のみを
扱うSystemである。

**整理:** 正しい。ただし、Internetで公開されていることとAuthoritative Classification上の
`Public`を区別する。InputだけでなくUser Data、Tool Result、Derived Output、Cache、Log、
Secondary useまでNon-public Dataがないことを確認する。`Public`が正式なLabelなら、N/Aでは
なくPublic LabelのPropagationを検証する選択も自然である。

## 18. このセッションから得られた洞察

1. **加工後のDataもProtectionを引き継ぐ。** TextがVectorやSummaryへ変わっても、Sourceに
   必要なProtectionは自動的に消えない。
2. **Label、Authorization、Enforcementは別のPropertyである。** Label PropagationにPassしても、
   Labelを無視するSystemは情報を漏えいし得る。
3. **Generic Source IDはLabelではない。** LineageだけをClassification bindingとみなさない。
4. **ModelをClassification Authorityにしない。** ModelはDataを変換できるが、Protectionを
   下げるDecisionはTrusted Processへ置く。
5. **Label Propagationは永久コピーではない。** Trusted Reclassificationを通じたProtection
   stateの変更は許容し得る。
6. **FreshnessもPropagationの一部である。** Source Label変更後に古いDerived Artifactを
   低いProtectionのまま残さない。
7. **公開情報だけのSystemはN/Aになり得る。** ただしInternet公開とPublic Classificationを
   同一視せず、Derived Dataを含むData flow全体で判断する。
8. **PublicもLabelになり得る。** 正式なPublic Labelを伝播すれば、Label欠落との区別が明確に
   なる。

## 19. 設計レビュー項目

- Authoritative Data Classification PolicyとLabel Sourceを特定したか。
- SourceからChunk、Embedding、Prompt Cache、Model OutputまでData flowを描いたか。
- Dataが形を変えるすべてのTransformation Boundaryを列挙したか。
- Derived ArtifactがClassification LabelまたはExplicitなClassification Referenceを持つか。
- GenericなSource IDだけをLabelとして扱っていないか。
- Label、Reference、Lineage、VersionをArtifactから分離または改ざんできないか。
- MissingまたはUnknown LabelをPublicへDefaultしていないか。
- 複数SourceのProtection conditionを失わずに結合しているか。
- Modelの自己判断だけでLabelを下げていないか。
- Reclassification／DeclassificationのAuthority、Rule、Test、Evidenceがあるか。
- Source Label変更後の再同期、Invalidation、最大遅延を定義したか。
- Cache、Log、Evaluation、Feedback、Export、BackupでLabelを落としていないか。
- Label解決不能時にUnfiltered pathへFail openしないか。
- Label PropagationのPassとAuthorization EnforcementのPassを混同していないか。
- N/AならInputだけでなくOutput、Cache、User Data、Tool Resultも確認したか。
- Internet公開を根拠なくPublic Classificationと同一視していないか。
- Non-public Dataを追加する変更時のApplicability再評価Gateがあるか。

## 20. References

### Normative／Research

- [OWASP AISVS v1.0 C5 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [OWASP AISVS v1.0 C5.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-02-AI-Resource-Authorization-Classification.md)
- [OWASP AISVS v1.0 Verification Levels](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x03-Using-AISVS.md)

AISVS Researchは具体的なPlatform例も示すが、それらをC5.2.7の唯一の実装方法または
NormativeなPass条件とはしない。
