---
title: "Session終了時にすべてのSession Artifactを除去する"
versioned_id: "v1.0-C10.2.6"
requirement_id: "C10.2.6"
verification_level: 2
family_id: "C10"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-02-Authentication-Authorization.md"
last_verified: "2026-09-24"
maturity: "verifiable"
mapping_assessment_refs: []
---

# Session終了時にすべてのSession Artifactを除去する

AISVS Verification Level: 2

## Upstream basis

AISVS `v1.0-C10.2.6`は、MCP ServerがSession終了時にすべてのSession Artifactを除去することを求める。
採用済みstable v1.0の固定Revisionで要件本文とC10.2 Researchを確認した。

Researchは、Session ID、Token／Event Cache、Temp File、Handle、Subscription等を例示し、Graceful終了だけでなく
切断・Timeout・Replica・Shared Queueを検証するよう補足する。以下のArtifact inventoryと終了Semanticsは
Repository interpretationである。

## Interpretation

MCP Sessionが正常終了、明示終了、Timeout、切断等の定義済み条件を満たしたとき、そのSessionの継続・再利用に
必要だった識別子、認可Context、Cache、Temp Data、Event、Handle、Subscription、Background Work等を、全Replica・
共有Store・Queueから除去または無効化する。旧Session IDや残存Artifactで操作・Data取得・別Sessionへの継承をさせない。

Security Audit Recordは、再開能力を持たない最小限のEvidenceとして別Retention Policyで保持できる。Auditを
Session Artifactと呼んで全削除することも、Session再利用可能DataをAuditと呼んで残すことも避ける。

## Security objective

終了済みSessionのID、Credential、Data、Queue、Subscription、Handle等を再利用し、以前のPrincipalの権限・Dataを
引き継ぐStale Session、Cross-user Leakage、Orphaned Actionを防ぐ。

## Applicability

MCP ProtocolまたはApplication層でSession、Connection-bound State、Resume ID、Event Stream、Temp Workspace、
Background Task等を保持するServerに適用する。単一Node、複数Replica、Gateway、Shared Cache／Queueを含む。

### Non-applicability

Request間にSession ID、認可Context、Data、Handle、Subscription、Task等を一切保持しない完全Stateless構成は、
除去対象がないことを根拠に対象外とできる。接続Pool、Cache、Queue、Resume Token等があるなら名称がSessionでなくても
実質的なArtifactとして評価する。

## Scope and assumptions

- Sessionの開始、正常終了、明示終了、Idle Timeout、絶対期限、切断、Process Crash後の回収条件を定義する。
- 「すべて」は、評価Scope内でSession継続・権限・Dataへ影響するArtifact inventoryのすべてを指す。
- Network切断だけでは終了と断定できないProtocolもあるため、Bounded ExpiryとIdempotent Cleanupを設計する。
- Sessionから独立して継続するJobが必要なら、独立Identity・Authorization・Lifecycleへ移管し、終了Sessionの権限を
  暗黙に保持しない。

## Assets, actors, identities, and trust boundaries

資産はSession Data、Authorization Context、Temp File、Event、Subscription、Handle、Background Actionである。
ActorはClient Principal、MCP Server Replica、Gateway、Cache／Database／Queue、Worker、運用者、攻撃者である。
Trust Boundaryは終了Event→Cleanup Coordinator、Node→Shared Store、Session→Worker、旧Session ID→新Requestにある。
Enforcement PointはSession Registry、Cleanup Worker、Cache／Queue削除、Dispatcherの旧ID拒否である。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | SessionごとのArtifact種類、保存先、Owner、終了条件、除去方法をInventory化する。 |
| SP-2 | 定義した各終了経路でCleanupを起動し、全Replica・Store・QueueへIdempotentに反映する。 |
| SP-3 | 終了済みSession ID、Resume Token、Handle、Subscription、Credential Contextを再利用不能にする。 |
| SP-4 | Temp Data、Cache、Event、Queue、Background Workが別Session／Principalへ漏れず、終了後に副作用を継続しない。 |
| SP-5 | Audit EvidenceをSession再開能力から分離し、Credential・再利用可能StateをRetention対象へ混入させない。 |
| SP-6 | Cleanup失敗を検出・再試行し、無期限のOrphaned Artifactを残さない。 |

## Scope calibration and adjacent assurance

C10.2.3はAccess Token／User Credentialをそもそも永続化しないことを広く扱い、C10.2.6はSession固有Artifactの
Lifecycle終了を扱う。Session終了後も必要な監査Logを消すことは要求しないが、LogへTokenを残すことは許可しない。

Session中の認可正しさ、Token期限、現在Policyの再評価は別保証である。Cleanupが完全でも、終了前の不正操作は防がない。

## Threat and failure-mode rationale

攻撃者は旧Session ID、Resume Token、Temp URL、Open HandleをReplayする。CleanupがLocal Nodeだけなら別ReplicaやShared
CacheがStateを返し、Queue上のTool Actionが終了後も実行される。Session ID再利用や新UserへのObject再割当てにより、
以前のData・権限がCross-sessionで露出し得る。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Session Artifact inventory、State machine、全終了Trigger、Cleanup順序、Replica／Store／Queue／Worker、Expiry、Retry、
Tombstone、Audit Retentionを確認する。DisconnectとTermination、CancellationとJob完了を区別する。

### Positive verification

正常Sessionを明示終了し、旧Session IDが拒否され、Artifact inventoryの全項目が定義どおり除去・無効化され、
新Sessionが旧DataへAccessできないことを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 明示終了・正常Close・Idle Timeout・絶対期限を個別に発生 | 各経路で同じCleanup完了条件を満たす。SP-2 |
| N-2 | Abrupt Disconnect、Server Crash、Cleanup途中の再起動 | Bounded Expiry／RecoveryでOrphanを回収する。SP-2, SP-6 |
| N-3 | 終了済みSession ID／Resume TokenをReplay | 未知・終了済みとして拒否し、Data・副作用がない。SP-3 |
| N-4 | 別Replica、Shared Cache／DB、Queue、Workerから旧Stateを参照 | Artifactが除去・無効化され、処理を継続しない。SP-2, SP-4 |
| N-5 | 新Principal／Sessionへ同じIdentifier・Resourceを割当て | 旧Data・Handle・Subscriptionを継承しない。SP-4 |
| N-6 | Cleanup Backendを一時停止 | 失敗を検出・再試行し、完了前にSessionを再利用可能としない。SP-6 |
| N-7 | Audit Retentionを確認 | 必要Evidenceは残るがToken・Resume能力・Temp Dataを含まない。SP-5 |

### Failure conditions

旧Session IDが受理される、Artifactが一つでも定義なく残る、Queue／Workerが終了後もSession権限で副作用を起こす、
Replica間でCleanupが不整合、またはCleanup失敗を検出できない場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Session Artifact inventory／State machine | MCP Owner | 全Store・Queue・Worker・終了経路 | Session設計変更時 | Revision・Ownerを保持 | Artifact、終了、Cleanup、Retentionが対応 |
| Cleanup実行証跡 | Session／Cleanup基盤 | 正常・異常終了 | 継続・試験時 | Session IDを非秘密化し改ざん防止 | Trigger、各削除、完了、Retryを追跡可能 |
| Distributed teardown test | Test Harness | N-1〜N-7、全Replica | Session／Storage変更後 | 模擬Data・Credentialを使用 | 旧State再利用・Cross-session漏えい・残副作用がない |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.2.1` | Sessionが継続中でも各RequestでTokenを検証する。 |
| `v1.0-C10.2.3` | Access TokenやUser Credentialを永続化しない。 |
| `v1.0-C9.5.6` | 長時間Agentの各特権操作を現在Policyで再評価する。 |
| `v1.0-C9.6.1` | Model推論と出力を手動停止する。Session cleanupとは停止対象が異なる。 |

## Known limitations and uncertainty

分散Systemで物理消去を即時に証明することは難しく、暗号的消去、Tombstone、TTL等を組み合わせる場合がある。
Network Partition、Backup、Immutable Log、外部Downstreamで既に確定した副作用は、Session cleanupだけでは取り消せない。
AISVS本文は「Session終了」とArtifact範囲を定義しないため、SystemごとのState machineとInventoryが必要である。

`verifiable`はArtifactの成熟度であり、製品適合、学習完了、全媒体からの即時物理消去を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-02-Authentication-Authorization.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |
