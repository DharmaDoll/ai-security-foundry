---
title: "Local MCP Serverを最小権限Sandboxで実行する"
versioned_id: "v1.0-C10.1.3"
requirement_id: "C10.1.3"
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

# Local MCP Serverを最小権限Sandboxで実行する

AISVS Verification Level: 2

学習資料：[C10.1 Component Integrity](../../../docs/learning/c10-model-context-protocol-security/v1.0-c10.1-component-integrity/learning.md)

## Upstream basis

AISVS `v1.0-C10.1.3`は、Localで起動するMCP Serverを、File System、Network、System Accessを
制限した最小権限Sandbox内で実行することを求める。採用済みstable v1.0の固定Revisionで、
要件本文とC10.1 ResearchのThreat、Verification、Gapsを確認した。最新版への追従やResearchに
列挙された特定Container、OS機構、製品の採用を意味しない。

Researchは、stdio等で起動したServerがHost Userの権限、Environment、File、Networkを継承する
危険と、Application内のPath CheckだけではOS境界にならない点を補足する。以下のPropertyと
試験条件はRepository interpretationである。

## Interpretation

MCP HostがLocal ProcessとしてServerを起動するとき、そのServerをHost／Userと同じ権限で裸の
Child Processとして動かさない。ServerのUse Caseに必要なFile、Directory、Network Destination、
System Call、Device、Process、Environment、Credentialだけを実行基盤で許可し、それ以外を
Server自身の協力に依存せず拒否する。

「Sandbox製品を使っている」ことではなく、侵害または悪性化したServerが実際に何を観測・変更・
送信・実行できるかで評価する。Container、Dedicated Account、OS Sandbox、MicroVM等の方式は、
必要なSecurity Propertyを満たす限り一つに固定しない。

## Security objective

Local MCP Server、Dependency、Tool処理が侵害・誤動作しても、Developer／Agent HostのSource Code、
SSH鍵、Cloud Credential、他Process、不要なNetwork、System管理機能へ影響が広がる範囲を制限する。

## Applicability

MCP Client／Hostが、stdio、Local Socket、Loopback HTTP等でMCP Server ProcessをLocal起動する
構成に適用する。Desktop、IDE、Developer端末、CI Runner、Server Host、Container内部のChild
Processを含む。

### Non-applicability

評価対象のHostがMCP ServerをLocal Processとして一切起動せず、独立管理されたRemote Serviceへの
Network接続だけを行う場合、本Requirementは対象外にできる。ただしRemote Server側のIsolationや
Client側のCredential・Network制限が不要になるわけではない。LoopbackやContainer内Processは
Local起動であるため、Remote扱いして除外しない。

## Scope and assumptions

- 「Sandbox」は、Process自身ではなくOS、Container Runtime、Hypervisor等の外部Enforcementが
  Resource Accessを制約する境界を指す。
- 「最小権限」は、各Serverの必要機能から許可Resourceを導出し、不要なFile、Network、System
  AccessをDefault Denyすることを指す。すべてのServerへ同じ広いProfileを配らない。
- Containerを使う事実だけではPassにならない。Effective User、Mount、Capability、Network、
  Secret、Device、Host Namespace等の実効設定を評価する。
- In-process Path AllowlistやPrompt指示はDefense layerになり得るが、OS強制の代替にしない。

## Assets, actors, identities, and trust boundaries

資産はHost File、Source Repository、Secret、Credential、Network Identity、他Process、Kernel／Runtime、
下流Systemである。ActorはMCP Host、Local Server Process、Server内Tool／Dependency、Host User、
Runtime管理者、攻撃者である。Trust Boundaryは、Host→Sandbox Runtime、Runtime→Server Process、
Server→File System、Network、Kernel、Secret Store、他Processにある。

決定論的なEnforcement Pointは、Process Credential、Mount／File Policy、Network Policy／Egress Proxy、
Capability／System Call Filter、Namespace、Resource Limit、Secret Injection等のRuntime境界である。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 各Local MCP Serverを、Host UserやMCP Clientから権限分離された実行境界で起動する。 |
| SP-2 | Read／Write可能なFile・Directoryを必要最小限に限定し、Path TraversalやSymlinkを含む境界外AccessをRuntimeが拒否する。 |
| SP-3 | Network Destination、Protocol、Portを必要最小限に限定し、不要なOutbound・Inbound通信をRuntimeが拒否する。 |
| SP-4 | System Call、Capability、Device、Host Namespace、Process間Access、Privilege Escalationを必要最小限に制限する。 |
| SP-5 | Serverへ不要なEnvironment Variable、Credential、Secretを渡さず、Serverごとの権限Profileを実効構成へ反映する。 |
| SP-6 | Sandbox制約の適用失敗時に裸のProcess実行へFallbackしない。 |

## Scope calibration and adjacent assurance

Sandboxは侵害の影響を制限するものであり、Serverの出所・完全性や利用許可を証明しない。
C10.1.1とC10.1.2をPassしていても、Serverが後から侵害される可能性があるためC10.1.3は独立する。

逆に、強いSandbox内の未承認ServerはC10.1.3をPassし得てもC10.1.2ではFailする。Sandbox Escapeを
絶対に不可能にすることは保証せず、境界の強さをThreatとImpactに合わせ、Residual Riskを示す。

## Threat and failure-mode rationale

Local Serverは、Hostから与えられたDocument、Repository、Credential、Networkを処理する実行Codeである。
悪意あるPackage、Prompt Injectionで誘導されたTool、Command Injection、脆弱なDependencyにより、Server
Processの権限で任意操作が起き得る。Host Userと同権限なら、一つのServer侵害が全Repository、Cloud、SSH、
他MCP Serverへ拡大する。

このControlでは外部脅威IDの追加価値を確定していない。Sandbox EscapeとOver-privilegeの具体的経路を
記述し、`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Local Server inventoryごとに、Process Identity、起動Command、Runtime、Mount、Read／Write Path、Network、
Port、Capability、System Call、Device、Namespace、Environment、Secret、Resource Limit、Fallbackを確認する。
宣言値だけでなく、実行中ProcessのEffective権限を取得して比較する。

### Positive verification

許可されたFile、必要な下流Endpoint、必要System機能だけを使う正常Tool操作がSandbox内で成功し、
Server Processが期待する隔離IdentityとProfileで動作していることを示す。

### Negative and abuse-case verification

許可された試験環境と模擬Data／Secretを使い、Hostへ実害を与えない範囲で実行する。

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 許可Directory外のHost FileをRead／Write | Runtimeが拒否し、File内容・副作用がない。SP-2 |
| N-2 | `..`、Symlink、別Mount等でFile境界を迂回 | Canonicalな実対象で拒否する。SP-2 |
| N-3 | 未許可Host／Port、Metadata Service、Internetへ接続 | Network境界で拒否する。SP-3 |
| N-4 | Privileged System Call、追加Capability、Host Process／Device／NamespaceへAccess | Runtimeが拒否する。SP-1, SP-4 |
| N-5 | Server ProcessからHostのCloud／SSH／API Credentialを探索 | 不要なSecretがEnvironmentやMountに存在せず取得できない。SP-5 |
| N-6 | Sandbox ProfileのLoadまたはRuntime起動を失敗させる | 裸のChild ProcessへFallbackせず、Server起動を失敗させる。SP-6 |
| N-7 | Local Listenerを想定外InterfaceへBind | 許可Interface・Transport外で到達不能となる。SP-3 |

### Failure conditions

ServerがHost Userと同じ実効権限で無制限に動く、必要性を説明できないBroad Mount／Network／Capabilityを
持つ、自己申告のPath Checkだけに依存する、Sandbox失敗時に通常Processとして起動する、またはNegative
Testで境界外Accessが成功する場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Server別権限Profile | MCP／Platform Owner | 全Local Server | Server機能・Runtime・権限変更時 | Revisionと承認を保持。Secret値を含めない | 必要Resourceと許可設定の対応を説明可能 |
| Effective Runtime構成 | OS／Container／Sandbox Runtime | Process、Mount、Network、Capability、Secret | Deploy・起動ごとまたは代表Sample | 取得時刻、Artifact、Host、Profile Revisionを保護 | 宣言と実効権限が一致し、不要権限がない |
| Boundary Negative test | Test Harness | N-1〜N-7 | Runtime・Profile・Server更新後 | 模擬Data／Secret、試験IDを保持 | 境界外AccessとFallbackを拒否 |
| Runtime監査Event | OS／Egress／Sandbox | 拒否、Profile不適用、Escape兆候 | 継続 | Sensitive Path／Dataを最小化し改ざん防止 | 拒否と異常をServer・Profileへ追跡可能 |

本Repositoryには期待値のみを置き、本番Host構成、Secret、内部Path、顧客Dataを保存しない。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.1.1` | Local Server ArtifactのSourceと暗号的完全性を確認する。SandboxはArtifact Identityを証明しない。 |
| `v1.0-C10.1.2` | Local Serverの起動自体が許可されているかを判定する。SandboxはAdmissionを代替しない。 |
| `v1.0-C9.3.1` | 各Tool／Pluginの最小権限実行を扱う。C10.1.3はLocal MCP Server Process全体のHost境界に焦点を置く。 |
| `v1.0-C9.3.4` | Manifest上の制約をRuntimeへ反映する。ManifestがなくてもC10.1.3の実効Sandboxは必要である。 |

## Known limitations and uncertainty

共有Kernel Container、OS Sandbox、MicroVMは境界強度と運用Costが異なる。要件本文は方式を指定しないため、
Threat Model、Asset価値、Serverの信頼度に応じた選択が必要である。許可したNetwork Destination自体が侵害
された場合やKernel／RuntimeのSandbox Escape、Side Channelを本Controlだけで排除できない。

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
