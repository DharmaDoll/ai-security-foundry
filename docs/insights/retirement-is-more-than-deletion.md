---
title: "使わせない、消す、再出現させないは別の保証である"
document_kind: "cross-cutting-insight"
status: "draft"
last_updated: "2026-09-29"
---

# 使わせない、消す、再出現させないは別の保証である

## 中心となる洞察

Memory、Vector、Cache、Session等を「削除した」と言っても、通常の利用から外れたのか、
Storageから物理的に消えたのか、ReplicaやBackupから戻らないのかは別である。
安全な終了は一つのDelete APIではなく、状態遷移と全利用経路での強制として設計する。

> 終了は書込み時の操作ではなく、次に使おうとした時の拒否で証明する。

## 実用的なモデル

| 状態 | 通常利用 | 調査用Access | 物理保存 |
|---|---|---|---|
| Active | Policy内で可 | 必要時 | 有 |
| Expired／Revoked | 不可 | Policy次第 | 残り得る |
| Quarantined | 不可 | 限定して可 | 証拠として保持 |
| Purged | 不可 | 不可 | 定義したScopeから消去 |

Resetは対象ScopeのActive／Derived Stateを一括して利用不能にする操作で、必ずしも即時の物理消去ではない。
Privacy上の消去要求は別のPolicyと期限を持つ可能性があり、Forensic保持との衝突を明示して判断する。

実装上は、Dense／Lexical／Hybrid検索、Direct ID、Parent Expansion、Cache、Replica、Restore、
Queue、Background Writerを列挙し、終了後にどの経路からも古いStateを再利用できないことを確かめる。
MCP等のSessionでは、接続を閉じてもSession ID、Subscription、Handle、Queued Workが残れば
実効的な利用が続き得る。

## 具体例

Userが長期MemoryをResetした。主Indexは空になったが、要約CacheとBackground Writerが古いContentを
再投入し、次の質問でModelが引用した。このSystemは「主Indexを削除した」とは言えるが、
「Memoryを使わせない」「再出現させない」とは言えない。

一方、疑わしい文書をQuarantineした場合は通常検索からは消し、調査担当者が制限された経路で
元ContentとHash、検出理由を確認できる状態が必要なこともある。Quarantineを即時Purgeと同一視しない。

## 設計レビューとNegative Test

- 終了操作の対象Scope、Authority、完了条件、Propagation時間を定義したか。
- Reset後にCache、Replica、Backup Restore、Background Writerから古い内容が復活しないか。
- Expired／Quarantined RecordをDirect IDや別Indexから取得できないか。
- Session終了後に旧ID、Subscription、Queued Tool Workから処理を再開できないか。
- Partial Failureを成功と報告せず、再試行と調査のためのEvidenceを残すか。
- Forensic Accessを通常User／Agentの検索経路から分離し、閲覧自体を監査するか。

## 限界と隣接Insight

本Insightは全てのDataを即時物理消去すべきだとは主張しない。Retention、Privacy、Incident Responseは
用途・法域・契約に依存するため、Policy Ownerによる判断が必要である。
[PrivilegeのLifecycle](privilege-is-a-lifecycle-not-a-token-field.md)はAuthorityの発行・失効を扱う。
本Insightは**保存済みStateの利用停止、保持、消去、再出現防止**を区別する。

## Slide-ready summary

- 検索から消えたことと、Storageから消えたことは違う。
- Resetの成否は、次の利用経路で確かめる。
- Quarantineは「使わせず、調査できる」状態である。

## 起点となった学習記録

- [C8.3：Memory Expiry & Revocation](../../controls/learning/c08-memory-embeddings-and-vector-database-security/v1.0-c8.3-memory-expiry-revocation.md)
- [C10.2：Authentication & Authorization／Session終了](../../controls/learning/c10-model-context-protocol-security/v1.0-c10.2-authentication-and-authorization.md)

これはAISVSの複数要件に現れるLifecycle上の失敗を一般化したRepositoryの解釈であり、個別要件の適用範囲を置き換えない。
