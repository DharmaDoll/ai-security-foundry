# PATTERN-RAG-001から読むControl Family・Section

**最初に読むのはC8.1とC5.2。検索時の認可を理解した後、期限切れや基盤分離の追加課題をC8.3・C5.3で確認する。**

対象Pattern：[RAG検索で、利用者に許可された文書だけを渡す](../engineering/domains/rag/secure-multi-tenant-retrieval/README.md)。
独立して作成したPatternと既存Controlを比較した、Section単位の関係案である。
個別Requirementの全充足や、製品の適合・試験合格を示すものではない。

## Family・Sectionの見取り図

Section名はリンク先のRepository表記に合わせる。C5.2の上流名はAI Resource Authorization & Classification、C5.3はMulti-Tenant Isolation。

| Family | Section | このPatternを読むときの問い | 関係の範囲 |
|---|---|---|---|
| C8 Memory, Embeddings & Vector Database Security | [C8.1 Access Controls on Memory & RAG Indices](../controls/control-records/c08-memory-embeddings-and-vector-database-security/README.md#c81-access-controls-on-memory--rag-indices) | 文書断片・検索・キャッシュに、会社と利用者の閲覧範囲をどう維持するか | 中心となる設計。`partial`：書込みやMetadata不変性まで含むSection全体は扱わない |
| C5 Access Control and Identity | [C5.2 Authorization](../controls/control-records/c05-access-control-and-identity/README.md#c52-authorization) | 検索サービスの広い権限ではなく、依頼した本人の権限で検索・回答組立を制限するには何が必要か | 中心となる設計。`partial`：全AI資源、特権管理、分類ラベル伝播等は含まない |
| C8 Memory, Embeddings & Vector Database Security | [C8.3 Memory Expiry & Revocation](../controls/control-records/c08-memory-embeddings-and-vector-database-security/README.md#c83-memory-expiry--revocation) | 文書自体が期限切れ・検疫対象になったら、検索・複製・復元経路からどう除外するか | 追加設計への入口。`context`：本人の権限取消を確認するだけではVectorの期限管理・Resetを満たさない |
| C5 Access Control and Identity | [C5.3 Tenant Isolation](../controls/control-records/c05-access-control-and-identity/README.md#c53-tenant-isolation) | 検索結果以外の共有モデル状態・計算資源からも、他社の情報を観測・操作できないか | 追加設計への入口。`context`：検索の行制限は、推論基盤やCPU/GPUの分離を保証しない |

例えば、担当者Aが異動してA100を読めなくなるのは、主に現在の閲覧範囲を扱うC8.1／C5.2の問題である。
一方、A100そのものが保存期限を迎え、以前の正当な読者にも検索させない条件はC8.3で別に確認する。
どちらもキャッシュを確認するが、失う権利・状態が違う。

## 関係評価の記録

以下の共通メタデータは4行すべてに適用する。`partial`は扱う範囲が一部、`context`は周辺理解に役立つ参照を意味する。

- relationship: `control-pattern`（Section単位）
- status: `proposed`。AIによる比較案であり、人によるMappingレビューは未実施。
- pattern_id: `PATTERN-RAG-001`（`draft`、2026-10-23の実装ノート・チェックシート追補を含む）
- source: `owasp-aisvs`
- source_version / source_status: `1.0` / `stable`（採用済み基準。現在の最新版という主張ではない）
- upstream_revision: `78775233666a2022dcfb82037e5e029116955c00`
- last_reviewed: `2026-10-23`（AIによる関係比較日。人による承認日ではない）
- 基準の正本：[source registry](../sources/registry.yaml)。今回、新版採用やControlの意味の変更は行わない。

| mapping_id | Control endpoint / exact identifier | Pattern endpoint | strength |
|---|---|---|---|
| MAP-AISVS-V1-RAG001-C81 | [v1.0-C8.1](../controls/control-records/c08-memory-embeddings-and-vector-database-security/README.md#c81-access-controls-on-memory--rag-indices) | [PATTERN-RAG-001](../engineering/domains/rag/secure-multi-tenant-retrieval/README.md) | partial |
| MAP-AISVS-V1-RAG001-C52 | [v1.0-C5.2](../controls/control-records/c05-access-control-and-identity/README.md#c52-authorization) | [PATTERN-RAG-001](../engineering/domains/rag/secure-multi-tenant-retrieval/README.md) | partial |
| MAP-AISVS-V1-RAG001-C83 | [v1.0-C8.3](../controls/control-records/c08-memory-embeddings-and-vector-database-security/README.md#c83-memory-expiry--revocation) | [PATTERN-RAG-001](../engineering/domains/rag/secure-multi-tenant-retrieval/README.md) | context |
| MAP-AISVS-V1-RAG001-C53 | [v1.0-C5.3](../controls/control-records/c05-access-control-and-identity/README.md#c53-tenant-isolation) | [PATTERN-RAG-001](../engineering/domains/rag/secure-multi-tenant-retrieval/README.md) | context |

### C8.1：検索対象の範囲を強制する

比較の中心は[C8.1.3のControl解釈](../controls/control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.1.3-retrieval-scope-enforcement/README.md)。
PatternのI1〜I5、[質問から回答までの①〜⑤](../engineering/domains/rag/secure-multi-tenant-retrieval/README.md#3-質問から回答まで5か所で確かめる)、[実装ノート](../engineering/domains/rag/secure-multi-tenant-retrieval/implementation-notes.md)のRLS・追加取得、[チェックシート](../engineering/domains/rag/secure-multi-tenant-retrieval/negative-tests.md)のN1〜N6・N9〜N12・N14〜N16が、Trusted Scopeの強制と迂回防止を具体化する。
Sectionには識別子の衝突防止・初回書込み後のMetadata不変性も含まれる。Patternは複合キーと管理面の分離を示すが、取り込み全体の保証は対象外。
また、Graph・Federated検索の網羅的設計や、件数・速度からの推測防止は未完了であり、Section全体の`direct`とはしない。

### C5.2：本人の権限を検索と回答組立へ持ち越す

比較の中心は[C5.2.2のControl解釈](../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.2-end-user-authorization-retrieval-assembly/README.md)。
PatternのI1〜I6、[質問から回答までの①〜⑤](../engineering/domains/rag/secure-multi-tenant-retrieval/README.md#3-質問から回答まで5か所で確かめる)と[キャッシュ・権限変更](../engineering/domains/rag/secure-multi-tenant-retrieval/README.md#6-キャッシュと権限変更をどう扱うか)、N1〜N4・N6〜N10・N13〜N16が、本人に束縛した検索・再利用・失効確認を具体化する。
回答返却前の権限再確認も扱うが、モデルの内部知識や任意出力に含まれる機密情報の分類・認可まで保証するものではない。
Section全体にはAI資源の既定拒否、PDPの分離、特権の期限、分類ラベル伝播などがあるため、検索パイプライン部分に限定した`partial`とする。

### C8.3：権限取消と、文書の期限管理を区別する

比較した[C8.3.1のControl解釈](../controls/control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.3.1-expired-vector-retrieval-exclusion/README.md)は、期限切れのVectorを全検索経路から除外する性質を扱う。
Pattern第6節とN7〜N9・N13の再認可は参考になるが、期限の管理元・時計・TTL判定・Replica／復元後の再出現防止を実装していない。
`active`や文書版のチェックだけをExpiry保証とはみなさず、Reset・Quarantineも含む追加設計への`context`とする。

### C5.3：検索の論理的な分離より広い境界を確認する

比較した[C5.3.1](../controls/control-records/c05-access-control-and-identity/v1.0-c5.3.1-shared-model-serving-tenant-isolation/README.md)は共有Servingの状態、[C5.3.2](../controls/control-records/c05-access-control-and-identity/v1.0-c5.3.2-shared-compute-tenant-isolation/README.md)は共有計算資源を扱う。
Pattern第9節はこの残余リスクを明示するが、KV Cache、Model／Adapter状態、CPU/GPUの観測・干渉対策を設計していない。
会社IDの照合・DBのRLSだけでこれらを満たしたとはせず、`context`とする。

## 根拠資料・再評価条件

2026-10-23に、固定Revisionの[AISVS v1.0 C8要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)と[C5要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)、上記Repository Controlを比較した。
上流は要件の根拠、各ControlはRepositoryの解釈、本書の強度・範囲は今回の比較判断である。

Patternの権限モデル・検索経路・失効保証、Control解釈、採用AISVS版が変わった場合は関係を再評価する。
本書の作成はPatternやControlの成熟度変更を意味しない。個別Requirement単位のMappingは別途評価する。

| 日付 | 変更 |
|---|---|
| 2026-10-23 | 開発済みRAG Patternと既存ControlをSection単位で比較し、中心となる部分と周辺の追加課題を記録 |
| 2026-10-23 | Patternの構成整理に合わせて説明箇所への参照を更新。関係の強度・範囲・評価状態の変更なし |
