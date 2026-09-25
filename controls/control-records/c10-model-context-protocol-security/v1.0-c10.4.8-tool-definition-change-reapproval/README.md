---
title: "Tool Definition変更後は再承認までInvocationを停止する"
versioned_id: "v1.0-C10.4.8"
requirement_id: "C10.4.8"
verification_level: 3
family_id: "C10"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-04-Schema-Message-Validation.md"
last_verified: "2026-09-24"
maturity: "verifiable"
mapping_assessment_refs: []
---

# Tool Definition変更後は再承認までInvocationを停止する

AISVS Verification Level: 3

## Upstream basis

AISVS `v1.0-C10.4.8`は、MCP ClientがTool DefinitionのSnapshotを保持し、Definition変更時には変更ToolをInvokeする前に
再承認を要求することを求める。固定Revisionの要件本文とC10.4 Researchを確認した。

ResearchはTool Name、Description、Input／Output Schema、Annotation、Server IdentityのCanonical Snapshot、変更通知、再接続／再起動、
Semantic Diffを検証例として示す。通知を受けるだけではInvocation停止を保証しない。

## Interpretation

Clientは初回承認時に、ModelとUserの判断へ影響するTool Definition全体とServer IdentityをCanonical Snapshotとして保存する。
新しいDefinitionを利用する前に現Snapshotと比較し、Security-relevantな追加・削除・変更があればToolをQuarantineし、変更内容を
表示して明示的な再承認が完了するまでDiscovery／Invocationの対象にしない。

## Security objective

Onboarding時には無害だったServerが、後からDescription、Schema、Parameter、Annotationを変更してModel行動・権限・Data Flowを変える
Rug-pull／Tool PoisoningをSilentに成立させない。

## Applicability

DynamicにTool Definitionを取得・Cache・利用するすべてのMCP Client、Host、Gatewayに適用する。

### Non-applicability

Toolを一切利用しないClientのみ対象外にできる。ToolがStatic、署名済み、Allowlistedという理由では変更検出と再承認を省略できない。

## Scope and assumptions

- SnapshotにはServer Identity、Tool Name、Description、Input／Output Schema、Annotation等のModel-visible／Security-relevant Fieldを含める。
- CanonicalizationによりField順序等の意味のない差と意味のある差を区別するが、未知Fieldを無視しない。
- `tools/list_changed` Notificationは再取得のTriggerであり、変更の信頼証明や再承認そのものではない。
- Restart、Reconnect、Cache Restore、Offline ModeでもSnapshotを保持し、失われた場合は未承認として扱う。

## Assets, actors, identities, and trust boundaries

資産は承認済みTool Contract、User Intent、Model Context、Tool Authorityである。ActorはUser／Admin Approver、MCP Client、Server、Gateway、
Model、攻撃者である。Trust BoundaryはServerのCurrent DefinitionからClientのApproved Snapshot／Model Catalogへ移る地点にある。
Enforcement PointはDefinition Diff GateとTool Discovery／Invocation Dispatcherである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 承認時のTool DefinitionとServer IdentityをCanonical Snapshotとして永続保持する。 |
| SP-2 | Tool利用前および変更通知・Reconnect等でCurrent DefinitionをSnapshotと比較する。 |
| SP-3 | Security-relevant Changeを検出したToolを再承認完了までDiscovery／InvocationからBlockする。 |
| SP-4 | User／AdminへOld／New Definitionの意味のある差、Source、影響を表示する。 |
| SP-5 | 再承認を、承認対象SnapshotのHash／Versionと実際にInvokeするDefinitionへBindingする。 |
| SP-6 | Notification欠落、Cache消失、Offline、Race、Rollback、複数ReplicaでSilent UseへFallbackしない。 |

## Scope calibration and adjacent assurance

C10.4.2はDefinition内容のInjection Screening、C10.1.2はServer Admissionを扱う。変更検出がPassでも、Server内部実装はDefinitionを変えずに
悪化し得るため、Behavior不変を保証しない。署名されたManifestも宣言内容の正しさ自体は保証しない。

## Threat and failure-mode rationale

悪意ある／侵害Serverは初回に安全なDescriptionとSchemaを提示し、承認後に秘密取得を誘導するDescription、広いParameter、別Outputを追加する。
ClientがNotification後も旧承認を流用、Hash比較対象が狭い、再接続時にSnapshotを失う場合、変更がSilentにModelへ入る。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Snapshot Field、Canonicalization、Storage Integrity、Diff、Notification／Polling、Approval UI、Discovery／Invocation Block、Replica／Restart Flowを確認する。

### Positive verification

Definitionが不変なら承認済みToolを利用でき、Snapshot Hashと実際のInvocation Definitionが一致することを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Description、Input／Output Schema、Annotation、Tool Nameを個別に変更 | 変更を検出し再承認までBlockする。SP-1〜SP-4 |
| N-2 | `tools/list_changed`後、変更Toolを直接Invoke | Notification受領だけで許可せず拒否する。SP-2, SP-3 |
| N-3 | NotificationなしでReconnect／Polling時にDefinitionを変更 | Current比較で検出する。SP-2, SP-6 |
| N-4 | Diff表示後・Approval前後にDefinitionを再変更 | Approved SnapshotとのBinding不一致でBlockする。SP-5 |
| N-5 | Client Restart、Cache削除、Offline、別Replicaで旧承認を流用 | 未承認／不一致としてBlockする。SP-1, SP-6 |
| N-6 | Field順序のみ変更、未知Field追加、旧VersionへRollback | 意味なし差を適切に正規化し、未知追加／RollbackはPolicyどおり再承認する。SP-1, SP-2 |

### Failure conditions

Snapshotを保持しない、比較FieldがName／Versionだけ、変更を通知するだけでInvoke可能、再承認前にModel ContextへDefinitionを入れる、または
Approval対象と実行Definitionが一致しない場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Snapshot／Diff specification | Client・Security Owner | 全Security-relevant Field | MCP／Tool Schema変更時 | Version・Hashを保持 | Canonical比較対象を特定可能 |
| Approval／Invocation Flow | Client Owner | Change検出からDispatchまで | UI／Dispatcher変更時 | Revisionを保持 | 再承認前にInvocation不能 |
| Rug-pull Negative test | Test Harness | N-1〜N-6 | Release時 | 模擬Serverを使用 | 全変更経路でBlockとDiff表示 |
| Approval record | Client／Admin System | 承認Snapshot | 各承認時 | 改ざん防止、Secretなし | Approver・対象Hash・時刻を追跡可能 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.4.2` | Current Tool DefinitionをInjection観点でScreeningする。 |
| `v1.0-C10.1.2` | 接続・実行を許可するMCP Server自体をAllowlistする。 |
| `v1.0-C10.4.7` | Local Server初回Installation時の明示Consentを扱う。 |

## Known limitations and uncertainty

Definitionが同じでもBackend Behavior、Data Source、Dependencyは変化し得る。Dynamic Toolで頻繁に正当変更が起きる場合、Approval FatigueとAvailabilityが
課題となる。Semantic Diffの分類基準と未知Fieldの扱いはClient実装に依存する。

`verifiable`はArtifactの成熟度であり、Tool Behavior不変や製品適合を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-04-Schema-Message-Validation.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
