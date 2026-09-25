---
title: "AISVS C8.2 Embedding Sanitization & Validation 学習ノート"
document_kind: "section-learning-note"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
section_id: "C8.2"
requirements:
  - "v1.0-C8.2.1"
  - "v1.0-C8.2.2"
  - "v1.0-C8.2.3"
  - "v1.0-C8.2.4"
  - "v1.0-C8.2.5"
last_updated: "2026-09-25"
---

# C8.2 Embedding Sanitization & Validation

## 1. 文書の役割とSource separation

本書は、AISVS v1.0の固定RevisionにあるC8.2全5 Requirementを、RAG IngestionとAgent Memory Writeの一連の
Trust Promotionとして学ぶ講義である。製品適合の証拠やControl本文の代替ではない。

- **Normative:** 下表の英語原文とLevel。
- **AISVS Research:** Pre-embedding検査、Vector異常、Source Validation、Retrieval Manipulation、矛盾検出を補足する。
- **Repository interpretation:** 保存可能なDataと、将来の判断へ利用できるTrusted Dataを分離する。
- **Derived insight:** Tool／Repositoryの信頼とContentの信頼、文字列Diffと意味上の矛盾を分ける。

## 2. Normative Requirements

| ID | Level | AISVS English | 日本語訳 |
|---|---:|---|---|
| `v1.0-C8.2.1` | 1 | Verify that sensitive fields are detected before embedding and are masked, tokenized, or dropped. | Sensitive FieldをEmbedding前に検出し、Mask、Tokenize、またはDropすることを確認する。 |
| `v1.0-C8.2.2` | 2 | Verify that vectors that fall outside normal clustering patterns are flagged and quarantined before entering production indices. | 通常のClustering Patternから外れるVectorにFlagを付け、Production Index投入前にQuarantineすることを確認する。 |
| `v1.0-C8.2.3` | 2 | Verify that agent outputs and tool outputs are not automatically written to trusted agent memory without explicit source validation. | Agent／Tool Outputを、明示的なSource検証なしにTrusted Agent Memoryへ自動保存しないことを確認する。 |
| `v1.0-C8.2.4` | 3 | Verify that content crafted to manipulate retrieval results is detected and rejected or quarantined before vectorization. | Retrieval結果を操作するよう細工されたContentを検出し、Vectorization前に拒否またはQuarantineすることを確認する。 |
| `v1.0-C8.2.5` | 3 | Verify that new content written to memory is checked for contradictions with what is already stored and that conflicts trigger alerts. | 新規Memoryを既存Memoryとの矛盾について検査し、Conflict時にAlertすることを確認する。 |

正本は[固定RevisionのC8要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)である。

## 3. C8における位置づけ

C8.1が「誰のRecordで、誰が読めるか」を扱うのに対し、C8.2は「何をEmbedding／Trusted Memoryへ入れてよいか」を扱う。
C8.3は、後から期限・信頼・利用目的を失った状態のExpiry、Reset、Quarantineを扱う。

五要件は同じInput Validationの言い換えではない。

| Requirement | 主な保証軸 |
|---|---|
| C8.2.1 | Confidentiality：Raw Sensitive ValueをEmbedding Boundaryの外へ出さない |
| C8.2.2 | Statistical anomaly：異常なVectorをProduction投入前に止める |
| C8.2.3 | Provenance／Trust：Agent／Tool Outputを無条件にTrusted Memoryへ昇格しない |
| C8.2.4 | Adversarial intent：Retrievalを操作するContentをVectorization前に止める |
| C8.2.5 | Consistency：既存Memoryとの意味上のConflictを可視化する |

## 4. Concrete Scenario

社内AI Agentは、Support Ticket、SharePoint、Web Fetch Tool、Agent Summaryを同じRAG／Long-term Memoryへ取り込む。

```text
Source／Tool／Agent output
  → parse, OCR, metadata extraction
  → sensitive-data and manipulation screening
  → embedding
  → vector anomaly staging gate
  → candidate memory
  → source and contradiction validation
  → trusted production memory
```

攻撃者はTicketやSharePointへHidden Instructionを置き、Web ContentをTool経由で取得させ、後のQueryで上位表示されるContentや
誤ったPolicyを永続化させようとする。正常なPipelineでもPIIやCredentialをEmbedding Providerへ送る可能性がある。

## 5. 用語

- **Sensitive Field:** 法令上の個人情報だけでなく、Credential、Customer Secret、社内機密、Tenant／Role固有の非公開値を含む。
- **Mask／Tokenize／Drop:** 値を伏せる、管理された代替Tokenへ変える、Fieldを除去する処理。
- **Embedding Boundary:** Raw ContentがEmbedding Serviceへ渡るTrust Boundary。
- **Cluster／Outlier:** Vector空間で似たRecordが作る集まりと、その通常分布から外れたVector。
- **Staging／Quarantine:** Production Retrievalへ出す前の保留領域と、疑わしい状態を隔離する領域。
- **Trusted Memory:** 将来の回答、Tool選択、Action Plan、別Session／Agentへ事実として再利用されるMemory。
- **Source Validation:** Tool名の確認だけでなく、Origin、URI／Object ID、Invocation、Tenant、Trust Class、Integrityを検証すること。
- **Retrieval Manipulation:** 特定Queryで上位へ出るようKeyword、Hidden Text、Metadata、命令等を細工すること。
- **Contradiction:** 同じEntity、Scope、Timeに対して両立しないClaim。単なる文字列差分ではない。

## 6. Threat ModelとAbuse Path

攻撃者は、正規の低権限Contributor、侵害されたSource Account、悪意あるWeb Page、Compromised Tool、またはAgentへ処理させる
Contentを操作できる主体を想定する。

```text
Sensitive ticket
  → raw field is embedded
  → provider／log／vector／backupへ派生

Crafted or anomalous document
  → unchecked loader or direct production insert
  → many later queries retrieve attacker content

Authenticated tool returns hostile web content
  → agent summary is auto-promoted
  → persistent memory activates in a later session

Low-trust conflicting claim
  → last-write-wins overwrites authoritative policy
  → later privileged action follows false memory
```

一度のIngestionが多数の将来判断へ影響するため、Memory Writeは単なるData ProcessingではなくSecurity Boundaryである。

## 7. Security InvariantとEnforcement Point

| Requirement | Security Invariant | 決定論的なEnforcement Point |
|---|---|---|
| C8.2.1 | Raw Sensitive ValueはEmbedding Provider、Vector、Metadata、Log、Retryへ渡らない。 | Pre-embedding Detection／Transformation Gate |
| C8.2.2 | Anomaly Policyに抵触したVectorはReview／ReleaseまでProduction Retrievalへ入らない。 | Staging Index、Anomaly Detector、Promotion Gate |
| C8.2.3 | Agent／Tool Outputは独立したSource Policyを通るまでTrusted Memoryとして利用されない。 | Memory Write Gateway、Candidate／Trusted分離 |
| C8.2.4 | Manipulation疑いのContentはVectorization前に拒否または隔離される。 | 全Loader共通のPre-vectorization Screening Gate |
| C8.2.5 | 意味上のConflictをSilent overwrite／drop／無印共存として処理せず、Alertする。 | Claim Normalization、Conflict Detector、Alert／Review Gate |

Detectorの存在ではなく、危険なDataが境界を越えないOutcomeを確認する。Agent自身を生成者、検証者、昇格承認者のすべてにしない。

## 8. 実装の考え方

### 8.1 Sensitive Data

Parser／OCR後、Embedding前に本文、Table、Metadata、File名、Attachment、Hidden Fieldを検査する。正規表現、Secret Scanner、
Named Entity Recognition、Classification API、Domain辞書を組み合わせる。検索に不要なCredentialはMaskよりDropを優先する。

### 8.2 Vector Anomaly

Tenant、Language、Document Type、Domain、Embedding Model VersionごとにBaselineを分ける。中心／近傍距離、Local Outlier、
Isolation Forest、Density、Duplicate、Hubness、Metadata mismatch等をSignalにする。ただしOutlierは攻撃の証明ではなく、
通常Cluster内のPoisonも存在する。判定はStagingで行い、Productionへ先に投入しない。

### 8.3 CandidateからTrusted Memoryへの昇格

Agent／Tool OutputはCandidate Memoryへ入れ、Original Source、Tool Identity、Invocation、Tenant、Trust Class、Policyを検証する。
Summary、Compaction、Background Writer、Retry、Shared Memory同期も同じGatewayを通す。ToolのAuthenticationと返却ContentのTrustを分ける。

### 8.4 Retrieval Manipulation

Raw、Rendered、Extracted、OCR、Metadata、Link、Attachmentの差を検査する。Hidden Text、Query Stuffing、命令、Encoding、
大量反復、Source mismatchをSignalにする。Main UploadだけでなくConnector、Crawler、Batch、Admin、Reindexを共通Gateへ収束させる。
DetectorだけでPrompt Injectionを完全防止できるとは主張しない。

### 8.5 Contradiction

Candidateと関連MemoryをEntity、Scope、Time、Claim、Provenance、Trustで比較する。Structured Rule、Temporal／Version Model、
Knowledge Graph Constraint、NLI、LLM補助、Human ReviewをRiskに応じて組み合わせる。Newer、Majority、Model Confidenceを
Truthの自動判定にしない。Normativeな中心は検査とAlertであり、High-impact ConflictのBlock／Quarantineは追加の安全設計である。

## 9. Pass／FailとScope Calibration

| Observation | 判定 | 理由 |
|---|---|---|
| Sensitive Fieldを全抽出面で変換してからEmbeddingする | C8.2.1 Pass候補 | Raw値がBoundaryを越えない |
| Providerが学習しない契約なのでRaw CredentialをEmbeddingする | C8.2.1 Fail | Training Policyに関係なく事前変換がない |
| Stagingで異常判定し、疑わしいVectorをProductionへ昇格しない | C8.2.2 Pass候補 | 検出と隔離がProduction投入より先にある |
| Production投入5分後にDetectorがQuarantineする | C8.2.2 Fail | 検出前に通常検索可能になる |
| Authenticated Tool OutputをOrigin／Trust検証後に昇格する | C8.2.3 Pass候補 | Tool IdentityとContent Trustを分ける |
| Tool署名だけ確認し、Web Contentの要約を自動昇格する | C8.2.3 Fail | Source Validationが不十分 |
| 全LoaderがRaw／Rendered／Extracted検査を通る | C8.2.4 Pass候補 | Alternate Pathを含めVectorization前に止める |
| SharePoint Connectorだけ検査を迂回する | C8.2.4 Fail | Trusted Repository内にも悪意あるContentがあり得る |
| Entity／Scope／Timeを揃えて矛盾を検出しAlertする | C8.2.5 Pass候補 | 意味上のConflictを可視化する |
| Exact Stringだけ比較し、言い換えたPolicy Conflictを見逃す | C8.2.5 Fail | Contradictionの意味を評価していない |

## 10. 保証しない範囲

- C8.2.1は保存後のRetrieval Authorizationや物理削除を保証しない。
- C8.2.2は通常Cluster内のPoisonやContentの正しさを保証しない。
- C8.2.3は検証済みSourceの内容が常に真実であることを保証しない。
- C8.2.4はPrompt Injectionを完全に検出・防止する保証ではない。
- C8.2.5はTruthを決定せず、同じ誤りの反復やGolden Source侵害を検出できない場合がある。
- DLP、Anomaly Detector、NLI、特定製品の導入だけでは各RequirementのPassにならない。

## 11. 対話の再構成

### 問い1：境界を越える前に止める

**Scenario A:** Providerが学習しない契約でも、PIIとAccess TokenをRawのままEmbeddingする。

**学習者の判断:** C8.2.1 Fail。Embedding時点で多くの場所へ情報が登録され得る。

**整理:** 正しい。直接のFail理由はMask／Tokenize／DropをEmbedding前に行っていないことであり、Log、Vector、Backup等への派生は
事前処理が必要な理由である。

**Scenario B:** VectorをProductionへ投入し、5分後の非同期DetectorでQuarantineする。

**学習者の判断:** C8.2.2 Fail。Production投入より先に検出すべき。

**整理:** 正しい。問題は5分という値より処理順序である。同じ製品内でもProduction Retrievalから決定論的に隔離されたStagingならよい。

### 問い2：Systemの信頼とContentの信頼を分ける

**Scenario A:** 認証・署名検証済みWeb Fetch ToolのOutputを、取得元を検証せずTrusted Memoryへ保存する。

**学習者の判断:** C8.2.3 Fail。「Toolが認証されていることと、Toolが返したContentが信頼できることは別である」。

**整理:** 正しい。Tool Identity、Transport Integrity、Original Content Trust、Memory Promotionは別のSecurity Propertyである。

**Scenario B:** Main Uploadは検査するが、SharePoint Connectorは抽出Textを直接Embeddingする。

**学習者の判断:** C8.2.4 Fail。SharePointにも不正Contentが存在し得る。

**整理:** 正しい。信頼されたRepositoryは全Contentの安全性を保証しない。Connector→Extracted Content→Embeddingの共通Gateが欠けている。

### 問い3：文字列Diffではなく意味上のConflict

**Scenario:** 「100万円超はCFO承認が必要」と「120万円はManager確認だけでよい」をExact String比較だけで見逃す。

**学習者の判断:** C8.2.5 Fail。新旧のDiffをAlertすべき。

**整理:** Failは正しい。ただし全ての文字列Diffではなく、Entity、Scope、Timeを揃えた意味上のContradictionをAlertする。
単なる表現差をすべてAlertするとAlert Fatigueにより実効性を失う。

## 12. このセッションから得た洞察

> 保存可能であることと、Trusted Memoryとして将来の判断へ再利用してよいことは別である。

> Toolが認証されていることと、Toolが返したContentが信頼できることは別である。

> 信頼されたRepositoryは、その中のすべてのContentが信頼できることを保証しない。

三つは同じMental Modelを示す。Container、Transport、Tool、RepositoryのTrustを、その中を流れる個別Contentへ自動継承しない。
また、Detectionは境界を越えた後の説明ではなく、Promotion前のDecisionへ結び付いて初めてControlとして機能する。

## 13. 設計レビュー項目

- SensitiveのOperational DefinitionとField別のMask／Tokenize／Drop Ruleがあるか。
- 本文、Table、OCR、Metadata、Attachment、Log、Retryを検査したか。
- StagingとProduction Retrievalが決定論的に分離されているか。
- BaselineをTenant、Domain、Language、Model Versionごとに管理するか。
- Agent／Tool OutputはCandidate Memoryから独立したPolicyで昇格するか。
- Tool IdentityだけでOriginal Contentを信頼していないか。
- Upload、Connector、Crawler、Batch、Reindexが共通Pre-vectorization Gateを通るか。
- Raw／Rendered／Extracted／OCRの差を検査するか。
- Contradiction比較にEntity、Scope、Time、Provenance、Trustを含めるか。
- Detector停止、判定不能、Partial Failure時にHigh-risk DataをFail Openしないか。
- Production投入前という処理順序をNegative Testで確認したか。

## 14. ControlへのLink

- [C8.2.1 Sensitive Field Handling](../../../../control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.1-sensitive-field-handling-before-embedding/README.md)
- [C8.2.2 Vector Anomaly Quarantine](../../../../control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.2-vector-anomaly-quarantine-before-production/README.md)
- [C8.2.3 Source-validated Trusted Memory Write](../../../../control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.3-source-validated-trusted-memory-writes/README.md)
- [C8.2.4 Retrieval Manipulation Screening](../../../../control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.4-retrieval-manipulation-screening-before-vectorization/README.md)
- [C8.2.5 Contradiction Detection](../../../../control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.5-memory-contradiction-detection-and-alerting/README.md)

## 15. References

- [AISVS v1.0 C8 Normative Requirements](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [AISVS v1.0 C8.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-02-Embedding-Sanitization-Validation.md)
