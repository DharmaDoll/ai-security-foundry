# AISVS C8：保証範囲と段階的なControl整備

- 調査日：2026-09-24
- 対象：採用済みOWASP AISVS v1.0、C8 Memory, Embeddings & Vector Database Security
- 固定Revision：`78775233666a2022dcfb82037e5e029116955c00`
- 状態：全3節・11要件を分析し、全11要件を`verifiable`まで整備済み。

本資料は採用済みSnapshotの章全体を理解し、Section単位でControlを成熟させるためのRepository interpretationである。
要件本文を正本とし、C8概要と各SectionのResearchを参照した。Researchの製品、事件、統計、将来提案を一括して
適合条件へはしない。

## 1. この章で保証したいこと

C8が扱うMemoryは会話履歴だけではない。RAG Index、Vector Store、Semantic Cache、Agentの長期Memory、
Chunk Metadata等、将来のModel判断へ再利用される半永続・永続状態を含む。

この章は次の三つの時点を保証する。

1. **読むとき**：Similarityだけで返さず、Tenant・User・Role・Task Scopeを各Retrievalで強制する。
2. **書くとき**：Sensitive Data、異常Vector、未検証のAgent／Tool Output、Retrieval操作用Content、矛盾を検査する。
3. **信頼を失った後**：期限切れを返さず、MemoryをResetでき、疑わしいContentを証拠として保持しつつ検索から除外する。

中心となる考え方は、EmbeddingやMemoryへの書込みを「ただのData Processing」とせず、将来の多数の判断へ影響する
永続的なTrust Boundaryとして扱うことである。Vector Similarityは関連度であり、Authorization、Authenticity、Safety、
Freshnessの証明ではない。

## 2. 全3節の見取り図

固定要件本文には11件ある。LevelはAISVS Verification Levelであり、Repository maturityではない。

| Section | ID範囲・件数 | Level内訳 | 主な保証対象 |
|---|---|---|---|
| C8.1 Access Controls on Memory & RAG Indices | 8.1.1–8.1.3：3件 | L1：1、L2：2 | TenantごとのID／Namespace、Metadata Tagの不変性、Query-time Scope。 |
| C8.2 Embedding Sanitization & Validation | 8.2.1–8.2.5：5件 | L1：1、L2：2、L3：2 | Sensitive Field、Vector異常、Memory Write Source、Retrieval Poisoning、矛盾。 |
| C8.3 Memory Expiry & Revocation | 8.3.1–8.3.3：3件 | L2：2、L3：1 | Expiry後の検索除外、Reset、Forensic保持と全検索経路からのQuarantine。 |

合計はL1：2件、L2：6件、L3：3件である。

## 3. Trust BoundaryとSection間の関係

```text
Source / User / Tool / Agent Output
  -> validation, provenance, classification
  -> chunking and embedding
  -> staging / quarantine
  -> production vector and memory stores
  -> scoped retrieval / graph expansion / cache
  -> context assembly
  -> model and downstream action

Expiry / revoke / reset / quarantine
  -> every dense, lexical, hybrid, cache, replica, and restored path
```

- C8.1は、誰のRecordとして書き、誰へ返せるかというIdentity／Authorization境界を作る。
- C8.2は、その境界内へ何をTrusted Memoryとして昇格させてよいかを扱う。
- C8.3は、後から信頼・期限・利用目的を失ったDataを、すべてのRead Pathから外せるかを扱う。

三つは相互依存するが代替しない。正しいTenantへPoisonを保存すればC8.1だけでは防げず、Quarantine Flagが正しくても
Retrieval RouteがScope Filterを迂回すればC8.3は実効性を失う。

## 4. Researchから引き継ぐ問いと注意

- **IngestionでACLを捨てない**：Source Object ID、ACL／Policy Reference、Classification、Owner、Revocation Stateを
  Chunkと結び付ける。後からVectorだけを見て権限を再構成しない。[R1][r1]
- **NamespaceはAuthorizationの一部でしかない**：Tenant Namespaceがあっても、ID正規化、Default Namespace、
  Client指定Filter、Update／Delete、Admin Port、Semantic Cacheから漏れる可能性がある。[R1][r1]
- **Pre-filterを基本にする**：Unauthorized Candidateを一度取得してから捨てる設計は、Score、件数、Latency、Cache、
  Context Assemblyへの漏えいを残す。Graph／Federated／Multi-hopでは境界ごとに再認可する。[R1][r1]
- **Embedding前が重要**：一度Vector化されたSensitive DataやPoisonは、Replica、Cache、Backupまで派生する。
  Original削除だけで影響消失を証明しない。[R2][r2]
- **異常値だけでPoisonを定義しない**：危険なVectorはOutlierだけでなく、多数のQueryへ近い中心的なHubや、
  通常Cluster内の自然なContentとして現れる。Detectionは補助でありProvenance／Reviewを代替しない。[R2][r2]
- **Agent自身をTrusted Writerにしない**：Agent SummaryやTool Outputは過去のUntrusted Contentを含み得る。
  Source Class、Validation、Promotion Ruleを通してTrusted Memoryと分ける。[R2][r2]
- **Logical exclusionとPhysical deletionを分ける**：Expiry／Quarantine後に検索結果から消えることと、Storage、Replica、
  Backupから物理消去されることは別のMilestoneとしてEvidenceを取る。[R3][r3]
- **ResetはIncident Response Operation**：Sessionだけでなく、Derived Summary、Semantic Cache、Background Writer、
  Shared Agent Memoryを含む範囲と完了条件を定義する。[R3][r3]
- **QuarantineとPurgeを分ける**：疑わしいRecordをProduction Retrievalから外しつつ、制限されたForensic Pathへ保持する。
  Privacy Erasureとの衝突はPolicyとHuman Reviewを要する。[R3][r3]

## 5. 最初のSection：C8.1

C8.1を最初に選ぶ。理由は次のとおり。

- C5.2.2で学んだ「SimilarityはAuthorizationではない」をVector／Memoryの全Read／Write Pathへ具体化できる。
- C8.2のQuarantine／PromotionとC8.3のExpiry／Resetを実効化するためのTenant、Metadata、Scopeが先に必要である。
- 同じDocument ID、Metadata変更、Filter omissionという短いNegative Testで、境界の実在を確認できる。
- 製品固有機能へ固定せず、Namespace分離、Metadata Filter、Policy Engine、Database Policy等の複数実装へ適用できる。

ただしC8.1をC5の複製にはしない。C8.1.1はVector Identifier／Namespace collision、C8.1.2はChunkに結び付く
Metadata Tagの不変性、C8.1.3はDense／Lexical／Hybrid／Cache／Graphを含むRetrieval Operationへ焦点を置く。

## 6. 段階的な進め方

1. **完了：章全体分析とC8.1。** 3要件をRequirement単位で`verifiable`まで整備した。
2. **完了：C8.2。** 5要件を一つのSectionとして成熟させ、Detectionを完全防止と誤表現しないControlへ翻訳した。
3. **完了：C8.3。** Expiry、Reset、Quarantineの状態遷移と全Retrieval Pathを3要件として成熟させた。
4. **次：章の整合確認。** ID／Level、Research／解釈、C5／C9との境界、Catalog／Family READMEを確認する。

学習資料は別Artifactであり、このControl成熟化によって学習完了とはしない。Engineering Patternも独立に発見・開発し、
後からMappingを評価する。

## 参照

- [固定RevisionのC8要件本文][normative]
- [C8 Research概要][overview]
- [R1：Access Controls on Memory & RAG Indices][r1]
- [R2：Embedding Sanitization & Validation][r2]
- [R3：Memory Expiry, Revocation & Leakage Prevention][r3]
- [Controls計画](../plan.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md
[overview]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-Memory-and-Embeddings.md
[r1]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-01-Access-Controls-Memory-RAG.md
[r2]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-02-Embedding-Sanitization-Validation.md
[r3]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-03-Memory-Expiry-Revocation-Leakage-Prevention.md
