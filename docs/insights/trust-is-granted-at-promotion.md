---
title: "信頼はContainerから継承せず、利用状態への昇格時に判断する"
document_kind: "cross-cutting-insight"
status: "draft"
last_updated: "2026-10-27"
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

## 保存・昇格・検索時の認可を分ける

| 判断 | 強制する場所と条件 |
|---|---|
| 保存してよいか | 受付・書込み処理で書込み主体、Tenant、保存可能な情報と用途を確認する |
| 判断材料として利用してよいか | 昇格・索引公開処理で出所、内容、目的を評価し、利用範囲を限定する |
| 今回の利用者へ開示してよいか | 検索・Context組立て時に現在の権限、Tenant、目的、有効期限を確認する |
| 汚染・失効後に使われないか | 検索、Cache、派生要約、再索引・復旧経路で利用停止を強制する |

一度の昇格で、全利用者・全Taskへの利用を許可しない。署名済みのDataでも、内容が汚染されていれば危険である。
暗号化は内容の正当性を証明せず、TTLも期限前の失効や別に保存した要約の排除を保証しない。
検出器で全ての悪意を判定できるとは考えず、昇格後も操作の認可と能力制限を維持する。
疑わしい内容が見つかったら、元Dataと派生物の出所を辿って通常利用から隔離し、調査用の保持と利用可能状態を分ける。
停止・削除後の再出現は[利用停止・消去・再出現防止](retirement-is-more-than-deletion.md)で扱う。

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
- 署名済みMemoryに操作誘導を含めても、署名を根拠に送信・削除の認可が増えないか。
- 昇格後に閲覧権限を失効させ、検索・Context組立てで開示されないか。汚染を利用停止した後、派生要約やCacheから復活しないか。

確認する証拠は、保存・昇格・検索の判断記録、出所と派生関係、実行側の拒否、停止後の検索結果である。
これらは検証観点であり、製品試験の実施結果ではない。

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
- [ユーザ提供メモの技術改訂版](../../sources/user-provided/2026-10-27-agentic-seven-trust-boundaries.md)：2026-10-27の技術レビューを起点に、Memoryの保存・昇格・利用・停止の区別を補足した。

これはSourceやAISVSの直接引用ではなく、複数のTrust Boundaryに共通するRepositoryの解釈である。
