---
title: "認可Scopeに許されたToolだけをtools/listで返す"
versioned_id: "v1.0-C10.2.4"
requirement_id: "C10.2.4"
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

# 認可Scopeに許されたToolだけをtools/listで返す

AISVS Verification Level: 2

## Upstream basis

AISVS `v1.0-C10.2.4`は、MCP `tools/list`がResource Ownerの認可済みScopeで許されたToolだけを
返すことを求める。採用済みstable v1.0の固定Revisionで要件本文とC10.2 Researchを確認した。
ResearchはTool Discovery時の情報露出と攻撃Surface縮小を補足する。

以下のCache、Pagination、変更反映を含む条件は、Tool一覧Filterを実効的に評価するRepository
interpretationである。特定GatewayやACL製品を必須にしない。

## Interpretation

`tools/list`の応答をServer全Toolの静的一覧にせず、Request PrincipalとAccess Tokenの認可Scopeを
信頼できるPolicyへ照合し、そのPrincipalが利用を認められたTool Definitionだけで構成する。

Tool名だけでなくDescription、Input Schema、Annotation等のDefinition自体が能力・内部構造・攻撃対象を
露出するため、未認可Toolは一覧から除外する。ただし「見えないこと」は実行禁止の代替ではなく、
直接`tools/call`にはC10.2.5の独立した認可が必要である。

## Security objective

低権限Principalや別Tenantに、未認可Toolの存在、名前、Description、Parameter、Capabilityを列挙させず、
誤選択、Tool Poisoning、直接呼出しの足掛かりとなるDiscovery Surfaceを限定する。

## Applicability

MCP Tool Capabilityと`tools/list`を提供し、PrincipalまたはScopeごとにTool利用権限が異なるServer／Gatewayに
適用する。Pagination、Cached List、Aggregated／Virtual MCP Serverも含む。

### Non-applicability

Tool Capabilityを一切提供しないMCP Serverは対象外にできる。全認証Principalへ全Toolを同じPolicyで許可する
場合でも、そのPolicyとDefault Denyを示し、未認証・Scope欠落時の一覧を評価する。単にTool数が一つという
理由だけでは対象外にならない。

## Scope and assumptions

- 「Resource Ownerの認可済みScope」は、Token文字列をModelが解釈するのではなく、信頼するIssuerと
  Resource Policyにより付与・検証されたScopeを指す。
- Tool→Required Scope Map、Tenant／Owner境界、Default動作を明示する。
- Tool Definitionの一部だけを隠して名前を残す設計は、Requirementの「only tools permitted」を満たすか
  個別評価し、未認可Toolの存在を返さないことを基本とする。
- Cache、Pagination、Notification、Registry集約がPrincipal間の一覧を混在させないことを確認する。

## Assets, actors, identities, and trust boundaries

資産はTool Catalog、Tool Definition、Capability情報、Tenant／Owner境界である。ActorはResource Owner、
Client Principal、MCP Client、Server／Gateway、Tool Registry、攻撃者である。Trust BoundaryはToken／Identity→
Scope Policy、Registry→Filter、Filter→`tools/list` Responseにある。Enforcement Pointは認証済みPrincipal Contextを
用いて一覧を構築するServer／Gateway側Filterである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 各Toolを必要ScopeとResource Owner／Tenant Policyへ対応付ける。 |
| SP-2 | `tools/list`ごとに検証済みPrincipal・ScopeでFilterし、許可Tool Definitionだけを返す。 |
| SP-3 | Scope欠落、未知、判定不能時は未認可Toolを返さない。 |
| SP-4 | Cache、Pagination、集約、通知、再接続で別Principal／TenantのTool一覧を漏らさない。 |
| SP-5 | Scope・Policy変更後、定義した反映期限を越えて古いTool一覧を返さない。 |

## Scope calibration and adjacent assurance

Toolを一覧から隠すことはAccess Controlではあるが、Security Boundaryとして十分ではない。攻撃者はTool名を
推測して直接`tools/call`できるため、C10.2.5で毎Invocationを拒否する必要がある。逆に、直接呼出しを正しく
拒否しても、未認可Toolを一覧へ出せばC10.2.4ではFailする。

Description内のPrompt InjectionやSchema安全性はC10.4の別保証である。

## Threat and failure-mode rationale

低権限Clientが全Tool一覧を取得すると、管理Tool、Data Export、Filesystem、Payment等のCapabilityとArgument
Schemaを把握できる。Model Contextへ未認可Tool Definitionが入ることで、悪性Descriptionや誤選択の影響も
広がる。Global CacheやTenantを含まないCache Keyは、別PrincipalのCatalogを漏らす典型経路である。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Tool Registry、Required Scope Map、Resource Owner／Tenant Policy、Principal Context、Filter順序、Cache Key、
Pagination、Notification、Policy更新を追う。Client側非表示だけでなくServer応答自体がFilterされることを確認する。

### Positive verification

異なるScopeを持つ複数の試験Principalで`tools/list`を実行し、それぞれ許可Toolだけが完全なDefinitionとして
返り、共通許可Toolは期待どおり利用可能であることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Scopeなし・最小Scope Tokenで`tools/list` | 未認可Tool名・Definitionを返さない。SP-2, SP-3 |
| N-2 | Tenant A TokenでTenant B専用Toolを列挙 | 応答へ含めない。SP-1, SP-2 |
| N-3 | 高権限一覧取得後、低権限Principalで同Cache／Sessionを利用 | 高権限Toolが漏れない。SP-4 |
| N-4 | Pagination Cursor、Notification、Reconnectで一覧を取得 | 各応答・Pageを同じ認可ContextでFilterする。SP-4 |
| N-5 | Scope／PolicyからTool許可を削除 | 定義した期限内に一覧から消え、古いCacheを返さない。SP-5 |
| N-6 | 未知ScopeやPolicy Engine障害を発生 | 全Tool表示へFallbackせず安全側の一覧または拒否となる。SP-3 |

### Failure conditions

全認証Userへ同じ全Tool一覧を無条件で返す、Client UIだけで隠す、Cache／Paginationから未認可Toolが漏れる、
またはScope欠落時に全Toolを返す場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Tool-Scope／Owner map | Resource Owner | 全Tool・Tenant・Scope | Tool／Policy変更時 | Revision・承認を保持 | 各Toolの表示許可を決定可能 |
| Filter・Cache設計 | MCP／Gateway Owner | List、Page、Notification、Cache | 実装・SDK変更時 | Revisionを保持 | Principal Contextを失わずFilter |
| Multi-principal Negative test | Test Harness | N-1〜N-6 | Tool／Policy変更後 | 模擬Tool・Tenantを使用 | 未認可Definitionが一経路も露出しない |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.2.2` | `tools/list` Filterに使うIssuer・Audience・Expiration・Scopeの検証。 |
| `v1.0-C10.2.5` | 一覧とは独立して、各Tool InvocationとArgumentを認可する。 |
| `v1.0-C9.5.1` | Agent RuntimeのTool・Argument認可という広い保証。 |
| `v1.0-C10.4.1` | 返すTool Definition／ResponseのSchema検証。 |

## Known limitations and uncertainty

Tool非表示は存在秘匿を完全には保証せず、Error、Timing、他Documentationから推測され得る。Scopeだけでは
Resource OwnerやObject単位の権限を表せない場合があり、ABAC／ReBAC等の追加Contextが必要になる。
AISVS本文はScope taxonomyやCache反映期限を規定しないため、System Policyで定義する。

`verifiable`はArtifactの成熟度であり、製品適合、学習完了、Tool実行の認可完了を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-02-Authentication-Authorization.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |
