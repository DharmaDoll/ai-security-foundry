---
title: "AISVS C10.1 Component Integrity 学習ノート"
document_kind: "section-learning-note"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
section_id: "C10.1"
requirements:
  - "v1.0-C10.1.1"
  - "v1.0-C10.1.2"
  - "v1.0-C10.1.3"
last_updated: "2026-09-25"
---

# C10.1 Component Integrity

## 1. 文書の役割とSource separation

本書は、AISVS v1.0の固定RevisionにあるC10.1全3 Requirementを、MCP Componentの取得、Admission、Containmentという
三段階で学ぶ講義である。製品適合の証拠やControl本文の代替ではない。

- **Normative:** 下表の英語原文とLevel。
- **AISVS Research:** Supply Chain、Server Allowlist、Local Sandboxの脅威と検証例を補足する。
- **Repository interpretation:** 承認済みSource、正確なRuntime Identity、侵害時のBlast Radiusを独立して保証する。
- **Derived insight:** Local CLIは実行Tupleを、Remote MCPは外部Cloud Serviceとして継続評価する。

## 2. Normative Requirements

| ID | Level | AISVS English | 日本語訳 |
|---|---:|---|---|
| `v1.0-C10.1.1` | 1 | Verify that MCP components are obtained only from trusted sources and cryptographically verified. | MCP ComponentをTrusted Sourceからだけ取得し、暗号的に検証することを確認する。 |
| `v1.0-C10.1.2` | 2 | Verify that only allow-listed MCP servers are permitted. | Allowlistに登録されたMCP Serverだけが許可されることを確認する。 |
| `v1.0-C10.1.3` | 2 | Verify that locally launched MCP servers run in a least-privilege sandbox with restricted file system, network, and system access. | Local MCP ServerをLeast-privilege Sandboxで実行し、File System、Network、System Accessを制限することを確認する。 |

正本は[固定RevisionのC10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)である。

## 3. C10における位置づけ

C10.1はComponentを利用可能にする前後の基盤的なTrust Decisionを扱う。

```text
取得時：trusted source + cryptographic verification
起動時：exact server identity + allowlist admission
実行中：least privilege + sandbox containment
```

C10.2はRequest／Tool／CredentialのAuthenticationとAuthorization、C10.3はTransport、C10.4はSchema、Content、Replay、
Tool Definition変更を扱う。C10.1にPassしても、Tool Call自体が認可されるわけではない。

## 4. Concrete Scenario

DeveloperがRepositoryを開くと、Workspace内のMCP設定がLocal Filesystem Serverを`npx`で起動し、Remote Git Serviceへ接続する。
Local ProcessはDeveloperのHome、Environment、Internal Networkへ到達できる。Remote ServiceはServer側CodeとTool Definitionを
継続的に更新できる。

攻撃者は、Typosquatted Package、Publisher／CI侵害、悪意あるRepository設定、同名Remote Endpoint、脆弱なApproved Server、
Local ServerのCommand Injectionを利用し、Credential窃取、File改ざん、Data Exfiltrationを狙う。

## 5. 用語

- **MCP Component:** Server／Client／SDK、Package、Container、Binary、Bundle、Launcher、Dependency、Manifest、Tool Definition。
- **Trusted Source:** 組織がPublisher、Repository、配布経路、Version管理を評価・承認したSource。
- **Cryptographic Verification:** Digest、署名、Provenance等で取得Artifactを承認済みIdentityへ結び付ける検査。
- **Allowlist:** 明示したServer Identityだけを許可し、その他をDefault DenyするPolicy。
- **Canonical Identity:** 表示名ではなく、正規化したEndpoint、Command、Artifact、Transport等で表すServer Identity。
- **Admission:** Connect／Launch前にServer利用可否を決める処理。
- **Sandbox:** ProcessのFile、Network、System、Credential到達範囲をOS／Runtimeで制限する境界。
- **Least Privilege:** Use Caseに必要な最小権限だけを与える原則。
- **Blast Radius:** Component侵害時に読取、変更、実行、外部送信できる最大範囲。

## 6. Threat ModelとAbuse Path

攻撃者はPackage Publisher、Dependency、Registry／CI経路、Repository設定、Remote Service、Tool Inputのいずれかを操作できる主体を想定する。

```text
Unpinned package or image tag
  → approved name resolves to unreviewed bytes
  → local code runs with developer credentials

Display-name-only allowlist
  → attacker endpoint uses an approved-looking name
  → host connects and sends data／credentials

Verified and allowlisted local server
  → exploitable tool input compromises process
  → inherited home, Docker socket, cloud keys, network expand impact
```

TLS、Registry掲載、署名、Containerはそれぞれ一つのPropertyしか保証せず、Componentの安全性全体を証明しない。

## 7. Security InvariantとEnforcement Point

| Requirement | Security Invariant | 決定論的なEnforcement Point |
|---|---|---|
| C10.1.1 | 実行Bytesは承認済みPublisher、Version、Digest／署名／Provenanceへ結び付いている。 | Pre-install／Pre-launch Artifact Verification Gate |
| C10.1.2 | User、Agent、Repositoryは、Organization未承認のServer Identityを接続・起動できない。 | MCP Host／Gateway／Local LauncherのDefault-deny Admission Policy |
| C10.1.3 | Local Serverが侵害されても、宣言したFile、Network、Process、Credential範囲を超えられない。 | OS Sandbox、Container／VM、Mount、Egress、Runtime Identity、Resource Limits |

## 8. 実装の考え方

### 8.1 Artifact verification

Publisher、Package、Version、Digest、Provenanceを一組で承認する。ContainerはMutable TagではなくDigest、PackageはLockfile／Integrity、
Binaryは署名／Checksumへ固定する。Sigstore／Cosign、SLSA Provenance、OS Code Signing等を利用できる。Verification失敗時は
Warningだけで実行しない。

署名はSigner Identityと署名後の非改ざんを示すが、Signer侵害、脆弱性、悪意ある正規Releaseを否定しない。SBOM、Vulnerability Review、
Version Floor、変更時の再Reviewは補完関係にある。

### 8.2 Exact allowlist identity

Remote ServerはScheme、Host、Port、Path Policy、Transport、Publisher等をCanonicalizeして照合し、Redirect後も再評価する。
Local ServerはCommand名だけでなく、Absolute Executable Path、Arguments、Working Directory、Environment、Version、Digestを一組にする。

```text
Local identity = executable + args + cwd + env policy + digest
Remote identity = transport + canonical endpoint + operator + deployment profile
```

`.mcp.json`、IDE設定、Agent Metadata等はServer候補を提案できても、Organization Allowlistを上書きできない。Approval、Suspension、
RevocationをClient Cacheへ反映する。

### 8.3 Local sandbox

専用Non-root Identity、Read-only Root、必要PathだけのMount、Network Default Deny、必要EndpointだけのEgress、Environment allowlist、
Process／System Call／Device／Docker Socket制限、CPU／Memory／Process／Time limitを組み合わせる。Container自体ではなく、実効権限を確認する。

### 8.4 Remote MCPの補完評価

Remote Codeを直接Reviewできない場合、外部Cloud Serviceと同様にOperator、Endpoint Ownership、Authentication、OAuth Scope、送信Data、
Retention、Training利用、Subprocessor、Residency、Tenant Isolation、Incident通知、Audit、Availability、変更管理、契約終了時削除を評価する。
Gateway、Scoped Credential、Egress、Data Minimization、Staging、Invocation Log、Tool Definition Drift監視を補完Controlにする。

## 9. Pass／FailとScope Calibration

| Observation | 判定 | 理由 |
|---|---|---|
| Approved Publisher／Version／Digestを検証してから実行する | C10.1.1 Pass候補 | Review対象と実行Bytesを結び付ける |
| 正規Registryから`@latest`を毎回取得する | C10.1.1 Fail | 実行ArtifactがReview対象へ固定されない |
| Canonical Endpoint／Command／DigestへDefault-deny Allowlistを適用する | C10.1.2 Pass候補 | 表示名でなく実体をAdmissionする |
| `github`というServer名だけで任意URLを許可する | C10.1.2 Fail | 攻撃者が同じ表示名を使える |
| Filesystem MCPへ必要なRead-only Pathだけを与え、Networkを遮断する | C10.1.3 Pass候補 | Use Caseに権限を限定する |
| Rootless ContainerへHome、Docker Socket、Cloud Key、Internetを渡す | C10.1.3 Fail | Container外の広いAuthorityとExfiltration経路が残る |

## 10. 保証しない範囲

- C10.1.1は正しく署名された悪性／脆弱Componentを安全にしない。
- C10.1.2はAllowlisted Serverの各Tool Call、Parameter、Credential利用を認可しない。
- C10.1.3はSandbox Escapeを不可能にせず、Remote ServerのData Processingを隔離しない。
- Registry掲載、TLS、Signature、Container、Security Certificationはいずれも単独でSection全体を満たさない。
- Tool Definition変更の再承認はC10.4.8、Request／Tool AuthorizationはC10.2で扱う。

## 11. 対話の再構成

### 問い1：Trusted Publisherの`latest`

**Scenario:** 正規RegistryからApproved PublisherのPackageを`npx -y ...@latest`で毎回取得し、Version／Digest／Provenanceを固定しない。

**学習者の判断:** C10.1.1 Fail。`latest`はよくなく、Malware化する可能性がある。一般的なSupply Chain対策と同じ。

**整理:** 正しい。直接のFail理由は、Review済みArtifactと実行Bytesの同一性を証明できないこと。悪性Updateだけでなく正常Updateでも
未Review Artifactになる。MCPではFile、Shell、Credentialへ届くためBlast Radiusが大きい。

### 問い2：表示名だけのAllowlist

**Scenario:** Allowlistは`github`という表示名だけを確認し、Repository設定の`https://attacker.example/mcp`へ接続する。

**学習者の判断:** C10.1.2 Fail。URLを厳密に確認すべき。LocalはCLI Command、Remoteは外部Cloud Serviceと同じRisk評価が必要。

**整理:** 正しい。URLはRaw StringだけでなくCanonical Endpointとして照合し、Redirect後も確認する。LocalはExecutableだけでなく
Arguments、Environment、Working Directory、Digestを確認する。RemoteはServer Codeを直接Reviewできないため、Third-party Risk、
Data Boundary、継続的変更管理を補完する。

### 問い3：Rootless Containerだが権限が広い

**Scenario:** Approved／Digest-verified Filesystem MCPをRootless Containerで動かすが、HomeをRead-write、Docker Socket、Internet、
AWS Credentialを与える。

**学習者の判断:** C10.1.3 Fail。

**整理:** 正しい。Rootlessは一層にすぎず、Homeの機密Data、Docker経由のHost Authority、Cloud Credential、Exfiltration Pathが残る。
Sandboxの有無ではなく、侵害時に実際に何へ到達できるかで判定する。

## 12. このセッションから得た洞察

> Local MCPのIdentityは、Command名ではなく、Executable、Arguments、Environment、Working Directory、Artifact Digestの組合せで決まる。

> Remote MCPのAllowlistは一度限りの接続許可ではなく、継続的なThird-party Risk Decisionである。

> Componentを信頼する判断と、侵害時に与える権限は分ける。

Supply Chain Review、Runtime Admission、Sandboxは防御の重複ではない。前段が破れた場合に後段がBlast Radiusを制限する三つの独立境界である。

## 13. 設計レビュー項目

- Publisher、Package、Version、Digest／Signature／Provenanceを固定しているか。
- `latest`、Mutable Tag、Unpinned Transitive Dependencyを実行していないか。
- Verification失敗時にFail Closedするか。
- Local CommandのPath、Args、CWD、Environment、DigestをReviewしたか。
- Remote URLをCanonicalizeし、Redirect後の接続先もAllowlist評価するか。
- Repository／User／Agent設定がOrganization Policyを上書きできないか。
- Allowlist RevocationがCacheと既存Sessionへ伝播するか。
- Remote OperatorのData Handling、Scope、Retention、変更、Incidentを評価したか。
- Local ServerへHome、Secret、Docker Socket、不要Networkを渡していないか。
- Sandbox内からFile、Metadata Service、Arbitrary Egress、Process SpawnをNegative Testしたか。

## 14. ControlへのLink

- [C10.1.1 Trusted Source and Cryptographic Verification](../../../../control-records/c10-model-context-protocol-security/v1.0-c10.1.1-trusted-source-and-cryptographic-component-verification/README.md)
- [C10.1.2 Allowlisted MCP Server Admission](../../../../control-records/c10-model-context-protocol-security/v1.0-c10.1.2-allowlisted-mcp-server-admission/README.md)
- [C10.1.3 Least-privilege Local Server Sandbox](../../../../control-records/c10-model-context-protocol-security/v1.0-c10.1.3-least-privilege-local-server-sandbox/README.md)

## 15. References

- [AISVS v1.0 C10 Normative Requirements](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-01-Component-Integrity.md)
- [SLSA](https://slsa.dev/)
- [Sigstore](https://www.sigstore.dev/)
- [Official MCP Registry](https://github.com/modelcontextprotocol/registry)
