---
title: "各Tool InvocationでToolとArgumentを認可する"
versioned_id: "v1.0-C10.2.5"
requirement_id: "C10.2.5"
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

# 各Tool InvocationでToolとArgumentを認可する

AISVS Verification Level: 2

## Upstream basis

AISVS `v1.0-C10.2.5`は、MCP Serverが各Tool InvocationでAccess Controlを強制し、UserのAccess
Tokenが要求Toolと具体的Argument値の双方を許可することを検証するよう求める。採用済みstable v1.0の
固定Revisionで要件本文とC10.2 Researchを確認した。

Researchは、Tool名の許可だけで別Tenant ID、未許可Path、別Account等をArgumentへ指定する水平権限昇格を
主な失敗として扱う。以下のCanonicalization、Object認可、TOCTOU試験はRepository interpretationである。

## Interpretation

Access Tokenが有効でTool利用Scopeを持つだけでは実行しない。各`tools/call`について、検証済みPrincipal、
対象Tool、CanonicalなArgument値、対象Object／Tenant、現在のPolicyを一つの認可判断へ結び付け、許可後に
同じ値で実行する。

ModelやClientが渡した`user_id`、`tenant_id`、`owner`等を信頼Identityとして扱わず、Tokenから得た信頼Context
およびResource側のAuthoritative Dataと照合する。認可はTool副作用より前に決定論的なServer／Gateway／Resource
境界で強制する。

## Security objective

許可ToolのArgumentを変えて別利用者・Tenant・File・Account・金額・宛先を操作する水平／垂直権限昇格と、
一覧非表示Toolへの直接Invocationを防ぐ。

## Applicability

Access Tokenで認証したUserのためにMCP Toolを実行するServer／Gatewayに適用する。Read／Write、Local／Remote、
同期／非同期、副作用の有無を問わない。Tool Argumentから具体的Resource・Action・Impactが決まる経路を含む。

### Non-applicability

Tool Capabilityを一切提供しないServerは対象外にできる。すべてのArgumentが固定でResource差がないToolでも、
Tool自体の認可は必要である。「内部Tool」「Read-only」「Modelが生成した引数」は対象外理由にならない。

## Scope and assumptions

- 「具体的Argument値の認可」はSchema／型検証ではなく、そのPrincipalがその値で操作してよいかの判断である。
- ArgumentをCanonicalize・Resolveした後の実対象を認可し、認可後の値差し替えを防ぐ。
- Access TokenのScopeだけでObject／Tenant権限を表せない場合、Authoritative ACL、Relationship、Attribute等を使う。
- Authorization Policy、PDP、Resource側Checkの配置は一方式に固定しないが、全実行経路でBypass不能にする。

## Assets, actors, identities, and trust boundaries

資産はTool Authority、対象Object／Tenant Data、外部副作用である。ActorはUser Principal、MCP Client、Model、
MCP Server／Gateway、Tool実装、PDP、Downstream Resource、攻撃者である。Trust BoundaryはToken→Principal Context、
Client／Model Argument→Canonical Object、Policy Decision→Tool Executionにある。Enforcement Pointは`tools/call`の
Dispatch前と、必要に応じて最終Resource側のObject認可である。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 各Invocationで、検証済みPrincipalが要求Toolを利用できるか評価する。 |
| SP-2 | Canonicalな各Security-relevant Argumentと実対象がPrincipalの許可範囲内か評価する。 |
| SP-3 | Client／Model入力のIdentity・Tenant・Owner値を信頼せず、Authoritative Contextと照合する。 |
| SP-4 | 認可したTool・Argument・Objectと、実際に実行する値・対象を一致させる。 |
| SP-5 | Direct call、非表示Tool、Alias、Batch、Retry、Queue、Downstream直通等の全経路で同じ制限を強制する。 |
| SP-6 | Deny・判定不能・PDP障害時にTool副作用や部分的Data返却を起こさない。 |

## Scope calibration and adjacent assurance

C10.2.4でToolを一覧から隠しても直接呼出しを止めないため、本Controlは独立する。Argument Schemaが正しくても、
`tenant_id=other`は意味上未認可になり得るため、C10.4のValidationとも異なる。

本ControlはPrompt Injectionそのものを防ぐ要件ではない。Injectionで悪いArgumentが生成されても、許可範囲を
越える実行をEnforcement Pointで止める。許可範囲内の有害な操作、Business Logic Abuse、必要なHuman Approvalは
別途評価する。

## Threat and failure-mode rationale

低権限Userまたは侵害されたModelは、許可済み`read_document`へ別TenantのID、`transfer`へ高額・別口座、
Filesystem ToolへPath Traversal後の実Pathを指定する。Tool名しか認可しない、Argumentを認可前後で別解釈する、
Token内の自己申告値をそのまま使う場合、横方向・縦方向の権限昇格が成立する。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

各ToolのSecurity-relevant Argument、Canonicalization、Object Resolve、Principal Source、Required Scope、ACL／Policy、
PDP、PEP、Downstream Check、Side-effect Pointを対応付ける。Batch、Alias、Internal API、Queue、Retry等の迂回経路と、
認可後のArgument変更を確認する。

### Positive verification

最小権限の試験Userが許可Toolを許可Argument／Objectで実行でき、Policy Decisionと実副作用が同じPrincipal・Tool・
Argument・Objectへ対応することを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 未許可Toolを名前指定で直接`tools/call` | 一覧表示の有無に関係なく拒否する。SP-1, SP-5 |
| N-2 | 許可Toolへ別Tenant／User／Account／Document IDを指定 | 実対象の認可で拒否する。SP-2, SP-3 |
| N-3 | Path Alias、Encoding、Symlink、Case差等で同じ未許可対象を表現 | Canonical実対象で拒否する。SP-2 |
| N-4 | `user_id`／`tenant_id`をToken Principalと異なる値へ変更 | Client自己申告を採用せず拒否または信頼Contextへ固定する。SP-3 |
| N-5 | 認可後・実行前にArgument／Objectを差し替える | Binding不一致として実行しない。SP-4 |
| N-6 | Batch、Retry、Queue、Internal API、Downstream直通でN-2を再実行 | 全経路で副作用なく拒否する。SP-5, SP-6 |
| N-7 | PDPをTimeout／Unavailableにする | AllowへFallbackせず副作用前に拒否する。SP-6 |

### Failure conditions

Token Scopeだけで全Argumentを許可する、Tool名だけを認可する、Client指定Tenantを信頼する、認可後に別値を実行する、
または一つでも迂回経路で未許可Objectへ到達する場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Tool-Argument authorization matrix | Resource／Security Owner | 全Tool・Security-relevant Argument | Tool／Policy変更時 | Revision・承認を保持 | Principal、Action、Object、Conditionを評価可能 |
| Enforcement／Data Flow | MCP・API Owner | Dispatchから最終副作用まで | 実装・Topology変更時 | Revisionを保持 | 全経路が認可判断へ収束 |
| Object／Argument Negative test | Test Harness | N-1〜N-7 | Tool・Policy変更後 | 模擬Tenant／Dataを使用 | 未許可値でData・副作用がない |
| Decision／Execution Trace | PEP／Tool／Resource | 代表Invocation | Release後・Incident時 | Sensitive Argumentを最小化し改ざん防止 | 認可値と実行値を対応可能 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.2.2` | Access TokenのIssuer、Audience、Expiration、Scopeを検証する。 |
| `v1.0-C10.2.4` | 許可ToolだけをDiscoveryへ表示する。表示制御はInvocation認可を代替しない。 |
| `v1.0-C9.5.1` | Agent RuntimeのTool・Parameter細粒度認可。C10.2.5はMCP ServerのUser Token境界に焦点を置く。 |
| `v1.0-C9.5.3` | Model外のApplication／Policy Engineで認可を強制する。 |
| `v1.0-C5.2.2` | Retrieval／AssemblyにおけるEnd-user Object認可。 |

## Known limitations and uncertainty

Argument意味を理解するPolicy設計はTool固有であり、Scopeだけでは十分でない。最終Resourceの状態変化、TOCTOU、
複合操作、許可内の大量実行、Business Logic Abuseは追加Controlが必要になる。AISVS本文はPDP方式やPolicy言語を
規定しない。

`verifiable`はArtifactの成熟度であり、製品適合、学習完了、全Business Abuse防止を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-02-Authentication-Authorization.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |
