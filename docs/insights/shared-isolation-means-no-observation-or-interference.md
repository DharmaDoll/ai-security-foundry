---
title: "Tenant IsolationはRead禁止だけでなく観測と干渉を防ぐ"
document_kind: "cross-cutting-insight"
status: "draft"
last_updated: "2026-09-14"
---

# Tenant IsolationはRead禁止だけでなく観測と干渉を防ぐ

## 中心となる洞察

別TenantのRecordを直接Readできなくても、共有Cache、Adapter、Worker状態、資源競合、Timing等を通じて、
処理の存在・内容を推測したり、他Tenantの結果へ影響したりできる。

> 「Access権がない」と「情報が伝わらない」は同じではない。

Tenant Isolationでは、何を専用化したかではなく、何がまだ共有され、その共有を通じて何を観測・変更・妨害
できるかを見る。

## 保護対象を広く捉える

- Prompt、Document、Model Output、Job結果。
- Cache、Context、KV state、Conversation state。
- Tenant固有のModel、Adapter、Configuration。
- Resource使用量、Timing、Error、Queue状態等の間接情報。
- Availabilityと他Tenant処理への干渉可能性。

共有GPUだけを確認しても、CPU、Memory、Storage、Network、Scheduler、Control planeが共有されていれば別経路が
残る。反対に共有Infrastructureでも、信頼できる強制と検証によって必要なIsolationを成立させる設計はあり得る。

## 一般的なLLM Applicationでの場所

```text
Tenant Request
  -> Tenant Identityの確定
  -> Model / Adapter選択
  -> Shared Worker / Cache / Batch
  -> Job ownership
  -> Result retrieval
```

Request Body内のTenant IDを信頼せず、認証済みContextとServer-side ownershipを各Boundaryで照合する。Worker切替時に
前TenantのAdapterやStateを残さず、Cache keyとJob resultをAuthority scopeへBindingする。

## Evidenceの扱い

「専用GPU」「別Container」「Providerが分離している」という説明だけではPassの根拠にならない。どの境界を
誰が強制し、どのTestやProvider evidenceで裏付けるかを示す。

未確認は脆弱性の実証ではないが、Passの証拠にもならない。保証の不存在と、保証Evidenceの不足を分ける。

## 設計レビューへの応用

- どのTenant間で、何を秘密・完全・利用可能に保つか。
- Request、Model、Adapter、Cache、Job、ResultのOwnerをどこで確定するか。
- 失敗、再試行、復元、削除、Worker再利用時にも境界を保つか。
- 他Tenantの処理をTimingや資源競合から観測できないか。
- 共有部分から他TenantのStateや挙動へ干渉できないか。
- 自社とProviderでTenantの意味と責任分界が一致するか。
- Cross-tenantのRead、Write、Cancel、Cache hit、Adapter選択をNegative Testしたか。

## 誤用と限界

- 単一Testで漏えいを再現できなかったことは、Side Channelが存在しない証明ではない。
- 専用Hardwareでも、Control planeや結果APIが共有されればIsolation Failureは起こり得る。
- Shared ServingのState Isolationと、一般的なData AuthorizationやMemory管理を混同しない。
- Provider側の未確認範囲とAssumptionを明示する。

## Slide-ready summary

- Read禁止とInformation Flow遮断は同じではない。
- 何を専用にしたかではなく、何がまだ共有されているかを見る。
- Dataだけでなく、Model挙動、State、Timing、Availabilityも保護対象になる。
- 未確認は脆弱性の証明ではないが、Passの証拠でもない。

## 起点となった学習記録

- [C5.3.1：Shared Model Serving Isolation](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.3.1-shared-model-serving-tenant-isolation/learning.md)
- [C5.3.2：Shared Compute Isolation](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.3.2-shared-compute-tenant-isolation/learning.md)

本書は特定CloudやHardwareの適合を主張せず、共有境界を評価するためのRepository interpretationである。
