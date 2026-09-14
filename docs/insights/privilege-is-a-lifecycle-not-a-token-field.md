---
title: "PrivilegeはToken FieldではなくEnd-to-end Lifecycleで評価する"
document_kind: "cross-cutting-insight"
status: "draft"
last_updated: "2026-09-14"
---

# PrivilegeはToken FieldではなくEnd-to-end Lifecycleで評価する

## 中心となる洞察

短いTTL、狭そうなScope名、正しい署名の一項目だけでは、AgentのAuthorityが本当に限定されているか分からない。
Credentialの発行前から、更新、下流利用、失効後のResource拒否までを一つのLifecycleとして追う。

> Credential単体ではなく、Privilegeが生まれ、使われ、延長され、消える全経路を評価する。

## Short-livedとJITは同じではない

5分Tokenでも、誰でも無条件に再発行できるなら、実質的なStanding Privilegeが残る。JITでは、必要なTask、
Principal、対象Resource、Environment、Approval等のActivation条件を満たした時だけPrivilegeが生まれ、
終了後は新しい特権操作がResource側で拒否される必要がある。

```text
通常時：Privilegeなし
  -> Activation条件を検証
  -> 対象へ限定したCredentialを発行
  -> Task中だけResourceが許可
  -> Refresh / Reissueの上限
  -> ExpiryまたはTask終了
  -> Resource側で新規操作を拒否
```

## Tokenの短命化が隠し得る経路

- Refresh Tokenで長期間更新できる。
- STSやToken Exchangeを繰り返して最大時間を越える。
- QueueやLong-running Jobが期限後も下流処理を続ける。
- Agentが別Identityや別AudienceのCredentialを取得できる。
- ResourceがExpiryを検証せず受け入れる。
- 障害時にBroadなStatic CredentialへFallbackする。

Security上の終了時刻は、管理画面に表示されたTTLではなく、Resourceが実際に特権Operationを拒否する時刻で測る。

## Credential BoundaryをHopごとに置く

Agent、MCP Server、Tool、Downstream APIは異なるAudienceとAuthorityを持つ。受信したTokenをそのまま次のResourceへ
転送せず、必要に応じて対象Resource用の狭いCredentialへ交換する。Token ExchangeがAuthorityを増幅しないことも
確認する。

Sender-constrained Tokenは盗難CredentialのReplayを難しくできるが、侵害済みの正規ProcessがKeyを使うことまでは
止めない。Key possessionとAction Authorizationを分ける。

## 有限なレビューへの分解

広いLifecycleは、次の六点で追える。

1. 対象ResourceとPrivileged Operation。
2. Eligible PrincipalとActivation条件。
3. Credentialの発行とTaskへのBinding。
4. Scope、Audience、Tenant、対象Artifact。
5. Refresh、Reissue、Exchange、Maximum duration。
6. Expiry・Revocation後のResource-side enforcement。

## 設計レビューへの応用

- Scope名ではなく、実際に可能なAction、対象、金額、宛先を見る。
- Credentialの所有者と、各Hopで行使するAuthorityを説明できるか。
- Refreshや再発行を含む最大Privilege時間を測ったか。
- Task終了時の早期Revocationと期限後の拒否を確認したか。
- CredentialがPrompt、Tool引数、Log、Trace、Memoryへ露出しないか。
- STS、CA、Trust Bundle障害時のFallbackを試したか。

## 誤用と限界

- Short-lived Credentialは侵害を防止せず、時間的Blast Radiusを縮める。
- 正しく限定したCredentialでも、許可Scope内の悪用や誤ったPolicyは残る。
- JITへのPassは、Identity、Artifact、Pipeline全体の安全を証明しない。
- mTLSやDPoP等の方式名だけで、Token BindingとResource側検証を証明しない。

## Slide-ready summary

- 短命TokenはJITの一部であり、JIT全体ではない。
- 最大時間はResource-side denialで測る。
- Refresh、Reissue、Exchange、Queueを含むLifecycleを見る。
- HopごとにAudienceとAuthorityのBoundaryを置く。

## 起点となった学習記録

- [C5.1.2：Agent Token](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.1.2-short-lived-minimal-scoped-signed-agent-tokens/learning.md)
- [C5.2.6：JIT Privileged Access](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.6-just-in-time-privileged-access/learning.md)

本書はOAuth等の特定方式を必須化せず、Credential PropertyとPrivilege Lifecycleを分けるためのRepository interpretationである。
