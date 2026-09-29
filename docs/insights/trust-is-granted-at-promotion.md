---
title: "信頼はContainerから継承せず、利用状態への昇格時に判断する"
document_kind: "cross-cutting-insight"
status: "draft"
last_updated: "2026-09-29"
---

# 信頼はContainerから継承せず、利用状態への昇格時に判断する

## 中心となる洞察

認証済みTool、承認済みRepository、署名済みComponent、正しいSchemaから届いたContentでも、
個々の内容が正しい・安全・利用目的に適合するとは限らない。特にMemory、RAG Index、Cacheのように
将来の多数の判断へ再利用される場所へ入れるときは、保存可能性とTrusted Stateへの昇格を分ける。

> 信頼できる経路を通った情報でも、信頼できる判断材料になるには別の審査が要る。

## 実用的なモデル

```text
外部文書 / Tool Output / Agent Summary
  -> Candidate（出所と取得経路を記録）
  -> 内容・分類・権限・目的・矛盾を評価
  -> Promotion Decision（誰のPolicyで、何に使える状態へするか）
  -> Trusted-use Store / Index / Cache
```

`Candidate`を保持することと、Modelが次回の権威あるContextとして利用できることは別の状態である。
昇格の強制点はModelの自己評価ではなく、書込み・索引投入・検索可能化を制御できる信頼された境界に置く。
疑義があれば、通常利用から隔離しつつ調査可能な状態を保つ。

## 具体例

社内の承認済み文書ConnectorがSharePoint文書を取得する。Connectorの認証が正しくても、
文書の編集者が悪意ある指示を書き込めるなら、そのContentは敵対的であり得る。
Agentがそれを要約し、要約を長期Memoryへ保存すれば、攻撃は後のSessionにも持ち越される。
「社内Connector経由」「Agentが作った要約」「Schema適合」は、昇格を許可する十分条件ではない。

同様に、MCP Serverの導入許可とSandboxはComponentを使う際の別の防御層であり、
ServerのTool Responseを高優先度Instructionへ昇格させる許可ではない。

## 設計レビューとNegative Test

- 誰がCandidateを書けて、誰がTrusted Stateへ昇格できるかを分離したか。
- Source ID、編集権限、分類、取得時刻、検査VersionをDerived Artifactまで保持できるか。
- 認証済みToolから悪意ある本文を返し、書込み・索引投入・次回の検索利用を拒否できるか。
- Agentが自分のSummaryだけを根拠にTrusted Memoryへ書けないか。
- Detector障害、判定不能、Batch／Reindex経路でPromotion Gateを迂回しないか。
- 正常な文書は必要なScopeで利用でき、過剰な拒否で業務を止めないか。

## 限界と隣接Insight

Promotion審査が通っても内容の真実性や将来の安全性を永久に保証しない。
編集、権限変更、Source失効、Model変更後は再評価が必要になる場合がある。
[Security Artifactの保証範囲](security-artifacts-have-bounded-claims.md)は署名やSchema等のClaimを校正する。
本Insightは、その校正を**将来再利用されるStateへの昇格Decision**に結び付ける。

## Slide-ready summary

- Sourceの認証は、Contentの無害性ではない。
- 保存できることと、次の判断に使ってよいことは別である。
- Trusted Stateへの昇格を、独立したSecurity Decisionにする。

## 起点となった学習記録

- [C8.2：Embedding Sanitization & Validation](../../controls/learning/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2-embedding-sanitization-validation.md)
- [C10.1：Component Integrity](../../controls/learning/c10-model-context-protocol-security/v1.0-c10.1-component-integrity.md)
- [C10.4：Schema, Message, and Input Validation](../../controls/learning/c10-model-context-protocol-security/v1.0-c10.4-schema-message-and-input-validation.md)

これはSourceやAISVSの直接引用ではなく、複数のTrust Boundaryに共通するRepositoryの解釈である。
