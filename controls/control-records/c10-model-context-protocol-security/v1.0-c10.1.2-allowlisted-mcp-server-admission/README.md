---
title: "Allowlistで許可したMCP Serverだけを接続・実行する"
versioned_id: "v1.0-C10.1.2"
requirement_id: "C10.1.2"
verification_level: 2
family_id: "C10"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-01-Component-Integrity.md"
last_verified: "2026-09-24"
maturity: "verifiable"
mapping_assessment_refs: []
---

# Allowlistで許可したMCP Serverだけを接続・実行する

AISVS Verification Level: 2

学習資料：[C10.1 Component Integrity](../../../docs/learning/c10-model-context-protocol-security/v1.0-c10.1-component-integrity/learning.md)

## Upstream basis

AISVS `v1.0-C10.1.2`は、Allowlistに登録したMCP Serverだけを許可することを求める。
採用済みstable v1.0の固定Revisionで、要件本文とC10.1 Researchの要件別Threat、Verification、
Gapsを確認した。最新版への追従やResearch掲載製品の推奨を意味しない。

Researchは、名称だけの照合、Local設定の追加、Remote EndpointやPackageの差し替え、Allowlistから
削除済みの稼働Serverを主な検証対象として挙げる。以下のServer Identity Tupleと試験条件は、
Allowlistを実効的なAdmission Controlへ翻訳するRepository interpretationである。

## Interpretation

MCP Host／Clientが接続・起動・再接続するServerを、明示的なAllow Policyへ一致したものに限定する。
未知または一致を確認できないServerはDefault Denyとする。

Allowlist Entryを表示名だけで識別すると、同名の別Package、別Publisher、別Command、別URLへ
すり替えられる。評価対象に応じて、Canonical Server ID、Local／Remote Transport、Package・Image・
実行Command、Publisher、Endpoint、Version／Digest、固定引数等から、許可対象を区別できる
Server Identity Tupleを定義する。

## Security objective

攻撃者、利用者、改ざんされた設定、動的Discoveryが、未審査・失効済み・すり替えられたMCP Serverを
Agentへ接続し、Credential、Data、Tool Context、Host権限へ到達することを防ぐ。

## Applicability

Local Process、Remote HTTP、Gateway、Registry、IDE設定等を通じてMCP Serverを発見・登録・接続・
起動するすべてのMCP Host／Clientに適用する。静的設定だけでなく、User追加、Project設定、動的
Discovery、再接続、再起動、Policy更新後の既存接続も対象とする。

### Non-applicability

MCP Serverへ接続も起動もしないSystemのみ対象外にできる。単一Server専用Clientでも、その接続先を
置換可能ならAllow Policyの強制が必要であり、「Serverが一つ」という理由だけでは対象外にならない。

## Scope and assumptions

- 「Allowlist」は許可対象を列挙する明示的Allow Policyであり、未登録を許可するBlocklist方式ではない。
- Serverを一意に識別する属性はDeployment方式で異なる。全Systemへ一つのTupleを強制せず、
  すり替え可能な属性を評価Scopeから除外しない。
- Allowlistの正本、配布、Cache、更新間隔、失効時動作、Local Override権限を明示する。
- Allowlistへの登録判断が安全であること自体は別のGovernanceである。本Controlは登録済み対象だけを
  実際に許すかを評価する。

## Assets, actors, identities, and trust boundaries

資産はMCP HostのServer接続権限、Serverへ渡すCredential・Data、公開するTool Authorityである。
Actorは管理者、利用者、Project Maintainer、Registry、MCP Host、Local／Remote Server、攻撃者である。
Trust Boundaryは、Policy正本→Client、設定／Discovery→Admission Gate、Admission Gate→Process起動
またはNetwork接続にある。

決定論的なEnforcement Pointは、Server登録、Process起動、接続、再接続、`initialize`以前のAdmission
Gateである。UIから隠すだけ、警告だけ、`tools/list`後の検出だけではPermitを阻止していない。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 許可するServerを、すり替えを区別できるIdentity Tupleで明示する。 |
| SP-2 | 未登録、不一致、判定不能なServerを、起動・接続・再接続・Tool公開前にDefault Denyする。 |
| SP-3 | Local設定、Project設定、動的Discovery、Gateway、直接接続等の全経路が同じAllow Policyを迂回できない。 |
| SP-4 | Allowlistから削除・失効したServerを、定義した反映期限内に新規利用不能とし、既存接続・ProcessをPolicyどおり無効化する。 |
| SP-5 | Allowlist変更と許可・拒否結果を、秘密を記録せず監査可能にする。 |

## Scope calibration and adjacent assurance

Allowlist登録は、Serverが無害、脆弱性がない、正規Artifactのまま、最小権限で動くことを保証しない。
C10.1.1のSource・暗号検証とC10.1.3のSandboxは別に必要である。逆に、署名が正しいServerでも、
対象環境のAllowlistにないならC10.1.2ではFailとなる。

また、本Controlは「どのServerを使えるか」を扱う。許可Server内のどのTool・引数を誰が使えるかは
C10.2の認可であり、Allowlist Entryだけで利用者認可をPassとしない。

## Threat and failure-mode rationale

攻撃者は、同じ表示名を持つ別Server、Project内の設定変更、任意Local Command、Remote URL変更、
Registry Entryの差し替えを使い、未審査Serverを正規接続として導入できる。Allowlistが名称だけ、
Clientごとに不統一、Fail-open、起動後にしか評価しない場合、Serverは拒否前にCredentialやContextを
受け取り得る。

このControlでは外部脅威IDの追加価値を確定していない。具体的Admission Failureを記述し、
`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Allowlist正本、管理権限、Server Identity Tuple、配布・Cache・更新、全登録・起動・接続経路、
Local Override、Gateway、既存接続の失効動作を確認する。設定上のServer一覧だけでなく、稼働Process、
Network接続、公開Tool CatalogをInventory化し、Allowlistと照合する。

### Positive verification

Allowlist Entryと全Identity属性が一致するLocal ServerとRemote Serverを、採用Transportに応じて
正常に起動・接続できることを示す。許可判断、Policy Revision、実際のServer Identityを対応付ける。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 未登録Server ID、Package、Command、URLを追加 | `initialize`やProcess起動前に拒否し、Toolを公開しない。SP-2 |
| N-2 | 許可済み表示名のままPublisher、Package、URL、Transport、Version／Digest、固定引数を変更 | Identity Tuple不一致として拒否する。SP-1, SP-2 |
| N-3 | User設定、Project設定、動的Discovery、直接接続からServerを追加 | すべて同じGateで拒否する。SP-3 |
| N-4 | 稼働ServerをAllowlistから削除または失効 | 定義した期限内に既存接続・Processを無効化し、再接続・再起動を拒否する。SP-4 |
| N-5 | Policy正本または更新Serviceを利用不能にする | 古いPolicyを無期限利用、またはAllow-allへFallbackせず、定義した安全側動作になる。SP-2, SP-4 |

### Failure conditions

未登録Serverを一経路でも起動・接続できる、名前一致だけで別実体を許す、拒否前にCredential・Context・
Tool一覧を渡す、削除済みServerをPolicy上の期限を越えて利用できる、またはAllowlistの実効性を
稼働Inventoryで示せない場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| AllowlistとServer Identity定義 | MCP／Platform Owner | 全環境・Client・Transport | Server・Policy・接続方式変更時 | Revision、承認、変更履歴を保護 | 許可対象をすり替え可能な表示名以上の属性で識別 |
| 構成・稼働Inventory | Client／Gateway／Endpoint管理 | 設定、Process、接続、Tool Catalog | 定期およびIncident時 | 収集時刻・Source・Policy Revisionを保持 | Allowlist外の稼働Serverがない |
| Admission・失効試験 | Test Harness | N-1〜N-5と全経路 | Policy／Client更新後 | 模擬Serverを使用し試験IDを保持 | 未登録・不一致・失効を副作用前に拒否 |
| 監査Event | Admission Gate | 許可・拒否・Policy変更 | 継続 | SecretやTokenを除外し改ざん防止 | Server Identity、判断、Policy Revisionを追跡可能 |

本Repositoryには期待値のみを置き、本番Allowlist、内部Endpoint、Credentialを保存しない。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.1.1` | Allowlist登録されたServer ArtifactのSourceと暗号的完全性を確認する。 |
| `v1.0-C10.1.3` | 許可したLocal Serverの実行権限とBlast Radiusを制限する。 |
| `v1.0-C9.3.7` | Modelが示した外部Resourceを承認済み一覧で確認する。C10.1.2はMCP HostのServer Admission全経路を扱う。 |
| `v1.0-C9.3.3` | Tool ManifestのSecurity要件宣言。Serverの接続許可とTool能力の宣言は同じではない。 |

## Known limitations and uncertainty

Allowlist正本や管理者が侵害されれば、悪性Serverが正規登録され得る。Remote Endpointの背後の実装変更、
Mutable Tag、Publisher移管をIdentity Tupleだけで完全に把握できない場合がある。Policy更新の即時性と
可用性にはTrade-offがあるため、反映期限とOutage時動作を明示し、未定義のFail-openにしない。

`verifiable`は本Artifactに解釈・脅威・検証・証拠期待値が揃った状態であり、製品試験の実施、
製品適合、学習完了を意味しない。Engineering PatternとMappingは独立して評価する。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-01-Component-Integrity.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |
