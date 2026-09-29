---
title: "AISVS C8 Memory, Embeddings & Vector Database Security Learning Guide"
document_kind: "family-learning-guide"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
current_section: "complete"
last_updated: "2026-09-25"
---

# AISVS C8 Memory, Embeddings & Vector Database Security 学習ガイド

## 目的

C8をVector Database製品の設定集ではなく、将来のModel判断へ再利用される状態のLifecycleとして理解する。

1. 誰のMemory／Recordであり、誰が検索できるか。
2. 何をEmbedding／Trusted Memoryへ入れてよいか。
3. 期限切れ、Incident、疑義の発生後にどう利用を止めるか。

全Category共通の講義形式、Source separation、Section単位の保存、Quality checkは
[`../README.md`](../README.md)に従う。C8では11 Requirementを個別学習ファイルへ分けず、
C8.1〜C8.3の三つの講義として扱う。

[C8 Family overview](../../control-records/c08-memory-embeddings-and-vector-database-security/README.md)は
CategoryとSectionの保証境界、整備済みControlへの入口を示す。

## Section一覧

| Section | Requirement | Level内訳 | 学ぶ主題 |
|---|---:|---|---|
| C8.1 Access Controls on Memory & RAG Indices | 3 | L1：1、L2：2 | Tenant識別子、Metadata不変性、全Retrieval経路でのScope強制 |
| C8.2 Embedding Sanitization & Validation | 5 | L1：1、L2：2、L3：2 | Sensitive Field、Vector異常、Trusted Memory昇格、Retrieval操作、矛盾検出 |
| C8.3 Memory Expiry & Revocation | 3 | L2：2、L3：1 | Expiry、Reset、Quarantineと全Retrieval経路への状態反映 |

## 軽量な進捗記録

現在学習中のSection：なし。C8全3 Sectionを一巡済み。次の講義はC10.1。

- [x] [C8.1 Access Controls on Memory & RAG Indices](v1.0-c8.1-access-controls-memory-rag-indices.md)
- [x] [C8.2 Embedding Sanitization & Validation](v1.0-c8.2-embedding-sanitization-validation.md)
- [x] [C8.3 Memory Expiry & Revocation](v1.0-c8.3-memory-expiry-revocation.md)

## このFamilyの学習から生まれた横断的Insight

- [信頼は利用状態への昇格時に判断する](../../../docs/insights/trust-is-granted-at-promotion.md)：C8.2のCandidateとTrusted Memoryを分ける。
- [利用停止・消去・再出現防止](../../../docs/insights/retirement-is-more-than-deletion.md)：C8.3のExpiry、Reset、Quarantineを別の保証として捉える。

これらは学習の起点を示すLinkであり、正式なMappingではない。

## Sources

- [AISVS v1.0 C8 Normative Requirements](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
- [AISVS v1.0 C8 Research overview](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-Memory-and-Embeddings.md)
- [C8.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-01-Access-Controls-Memory-RAG.md)
- [C8.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-02-Embedding-Sanitization-Validation.md)
- [C8.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C08-Memory-and-Embeddings/C08-03-Memory-Expiry-Revocation-Leakage-Prevention.md)

このGuideのChecklistは学習Navigationである。Control maturity、Mapping、製品適合を変更しない。
