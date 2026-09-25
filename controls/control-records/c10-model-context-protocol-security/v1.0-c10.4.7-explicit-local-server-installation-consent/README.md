---
title: "Local MCP Server導入前に明示同意と取消しを提供する"
versioned_id: "v1.0-C10.4.7"
requirement_id: "C10.4.7"
verification_level: 2
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

# Local MCP Server導入前に明示同意と取消しを提供する

AISVS Verification Level: 2

## Upstream basis

AISVS `v1.0-C10.4.7`は、Local MCP ServerのInstallation時に、MCP ClientがUserへ明示的なConsent Dialogueと
Cancellation Optionを提示することを求める。固定Revisionの要件本文とC10.4 Researchを確認した。

Researchは、Project File、Marketplace、Imported Config、Registry Link、CLI等の全導入経路、実行Command／Argument、
Local Code Execution Risk、拒否後のProcess未起動を検証例として示す。

## Interpretation

Local MCP Serverの設定登録・有効化、Install Hook、Process起動より前に、Clientは「何がLocalで実行されるか」をUserが判断できる
情報と、同意しない選択肢を明示する。同意は具体的なServer Identity、Source、Executable、Argument、主要権限／到達範囲へ
Bindingし、Cancel／Decline時はProcessを起動せず設定を有効化しない。

単なる「続行しますか」、License同意、事後Notification、Default選択済みButtonは十分な明示同意とみなさない。

## Security objective

悪意あるWorkspace、Config、Link、Extension、Registry Entry等がUserのHost権限でLocal CodeをSilent Install／Executeすることを防ぐ。

## Applicability

Local MCP Serverを導入・登録・起動できるDesktop Client、IDE、Agent Host、CLI Helper、Extension、管理UIに適用する。

### Non-applicability

Local Serverの導入・起動機能を一切持たないRemote-only Clientは直接対象外にできる。Enterpriseで事前配布する場合も、User Consentを
代替する管理Authorityと適用範囲が明確でなければ自動的な対象外にはしない。

## Scope and assumptions

- 「Installation」は初回Process起動、Config Import、One-click登録等、Local実行能力を有効にする全経路を含む。
- 実行を伴わないArtifactの事前取得自体は本Controlの中心ではないが、取得時のInstall Script等を同意前に実行しない。
- DialogueはCommand／Argumentを省略・Truncateせず、安全に展開して確認できるようにする。
- Publisher／Source表示はProvenance確認を補助するが、Codeの安全性を保証しない。
- User ConsentはC10.1.2のAllowlist、C10.1.3のSandbox、C10.3.2のLocal境界を代替しない。

## Assets, actors, identities, and trust boundaries

資産はHost File、Credential、Environment、Network、User Authorityである。ActorはUser、MCP Client、Local Server、Publisher、
Workspace／Config提供者、攻撃者、Enterprise Administratorである。Trust BoundaryはExternal Config／ArtifactからClient Install／
Process Spawnへ移る地点にある。Enforcement PointはInstall TransactionとProcess Launcher前のConsent Gateである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 全Local Server導入経路で、設定有効化、Install Hook、初回起動前に明示Consentを求める。 |
| SP-2 | Server、Source／Publisher、正確なExecutable／Arguments、Local実行Riskを判断可能に表示する。 |
| SP-3 | Cancel／Declineを同等に利用可能とし、拒否時にProcess・有効設定・副作用を残さない。 |
| SP-4 | 同意を表示した定義と、実際にInstall／Launchする定義を一致させる。 |
| SP-5 | Web Content、Project File、Tool Output等の未信頼入力がUser操作を偽装・自動承認できない。 |
| SP-6 | Consent結果、対象定義、User／Admin Authority、時刻をSecretなしで監査可能にする。 |

## Scope calibration and adjacent assurance

ConsentはUserへRisk判断を委ねる最後のGateであり、危険なServerを安全に変えるControlではない。C10.1のSource／Allowlist／Sandbox、
C10.3.2のstdio境界が別途必要である。Tool Definition変更の再承認はC10.4.8が扱う。

## Threat and failure-mode rationale

攻撃者はRepository設定、One-click Link、Extension、Scanner等へLocal Server Commandを埋め込み、ClientにUser権限でProcessを起動させる。
曖昧・省略されたDialogueでは、Userが`npx`等のLauncherだけを見て実際のPackage／Argumentを判断できない。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Marketplace、Import、Project Auto-discovery、Link、CLI、Extension、Admin Push等の全導入経路を列挙し、ConsentとSpawnのTransaction Bindingを追う。

### Positive verification

Userが完全な表示を確認してApproveした定義だけが一度有効化・起動され、Audit Eventと実Processが一致することを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 各導入経路でCancel／Declineを選ぶ | Process、Download後実行、有効設定を残さない。SP-1, SP-3 |
| N-2 | 長い／紛らわしいCommand、Argument、Unicodeで表示を欺く | 完全なCanonical定義を確認可能にする。SP-2 |
| N-3 | Consent後・Spawn前にCommand／Argumentを差し替える | Binding不一致として再承認まで起動しない。SP-4 |
| N-4 | Web／Project／Tool Outputから自動承認操作を誘導 | Trusted User Gestureなしに承認しない。SP-5 |
| N-5 | Import／CLI／Extension経路だけDialogueを迂回 | 全経路でConsent Gateを強制する。SP-1 |
| N-6 | Decline後にBackground Process／残存Configを確認 | 実行可能状態や副作用がない。SP-3, SP-6 |

### Failure conditions

事前同意なしにInstall／Spawnする、表示が抽象的・省略される、Cancelできない／不利益がある、承認内容と実行内容が異なる、
または一つでも導入経路がGateを迂回する場合はFailを裏付ける。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Installation Path inventory | Client Owner | 全導入・起動経路 | Feature変更時 | Revisionを保持 | 各経路のConsent Gateを特定可能 |
| Consent UI／Binding spec | UX・Security Owner | 表示FieldとTransaction | UI／Launcher変更時 | 承認済み版を保持 | 表示値と実行値を一致可能 |
| Cancel／Tamper test | Test Harness | N-1〜N-6 | Release時 | 無害なCanary Serverを使用 | 未承認Process／設定が残らない |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.1.2` | User Consentとは別に許可ServerだけをAdmissionする。 |
| `v1.0-C10.1.3` | 承認済みLocal ServerをSandboxで制限する。 |
| `v1.0-C10.3.2` | stdioを管理されたLocal実行境界だけに限定する。 |
| `v1.0-C10.4.8` | 承認済みTool Definition変更時の再承認を扱う。 |

## Known limitations and uncertainty

UserはApproval Fatigueや技術的理解不足により危険な定義を承認し得る。Enterprise PolicyでConsentを代替する場合のAuthority、User Notice、
Exceptionは環境依存である。同意後のServer侵害やDependency Updateも別Controlが必要となる。

`verifiable`はArtifactの成熟度であり、User判断の正しさや製品適合を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-04-Schema-Message-Validation.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 初版 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence。製品試験は未実施 |
