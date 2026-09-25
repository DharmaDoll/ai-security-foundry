---
title: "MCP Componentを信頼済みSourceから取得し暗号的に検証する"
versioned_id: "v1.0-C10.1.1"
requirement_id: "C10.1.1"
verification_level: 1
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

# MCP Componentを信頼済みSourceから取得し暗号的に検証する

AISVS Verification Level: 1

学習資料：[C10.1 Component Integrity](../../../docs/learning/c10-model-context-protocol-security/v1.0-c10.1-component-integrity/learning.md)

## Upstream basis

AISVS `v1.0-C10.1.1`は、MCP Componentを信頼できるSourceからのみ取得し、暗号的に
検証することを求める。採用済みstable v1.0の固定Revisionで、要件本文とC10.1 Researchの
Threat、Verification、Gapsを確認した。最新版への追従やResearch掲載製品の推奨を意味しない。

ResearchはPackage、Container Image、Binary等のSupply Chain侵害を主な失敗として扱い、
Checksum、署名、Attestation、固定Artifact等を検証例として示す。以下はRepository
interpretationであり、特定Registry、署名方式、Scanner、SBOM製品を一律のPass条件にしない。

## Interpretation

導入・更新・復旧のすべての経路で、実際に実行するMCP Client／Server Artifactが、組織が
信頼すると決めたPublisher・Registry・Repository・Build経路から得られたものか確認し、
期待したArtifactから改変されていないことを実行前に暗号的に検証する。

「公式らしい名前」やHTTPSでDownloadできた事実だけでは不足する。また、Hash値をArtifactと
同じ未信頼経路から取得して比較するだけでは、攻撃者が両方を置換できる。信頼するSource、
期待する署名者・Provenance・Digest等と、検証失敗時に実行を止めるAdmission経路が必要である。

## Security objective

Typosquatting、配布元のすり替え、改ざんされたPackage／Image／Binary、未承認Updateを、
MCP ComponentとしてAgent環境へ導入・実行する経路を遮断する。

## Applicability

Package、Container Image、Binary、Extension、Source Build等としてMCP ClientまたはServerを
取得、Install、Build、Update、Rollback、復旧するSystemに適用する。直接依存だけでなく、
実行ArtifactのIdentityを左右するLauncher、Image、Bundle等も、対象Scopeとして明示する。

### Non-applicability

外部からMCP Componentを取得・更新せず、評価対象内でBuildされたArtifactだけを使う場合でも、
Build出力を期待するSource Revisionへ結び付け改変を検出する必要は残る。したがって「内製」だけを
理由に対象外とはしない。MCP Componentを一切使用しないSystemのみ対象外にできる。

## Scope and assumptions

- 「信頼済みSource」は、名称ではなく、Owner、Publisher、Registry／Repository、取得経路、
  必要な署名者やBuild Identityを組織が明示的に承認したSourceを指す。
- 「暗号的検証」は、期待するDigest、署名、Attestation等を信頼AnchorとPolicyに照らし、
  Artifactの使用前に検証することを指す。方式は一つに固定しない。
- Sourceの信頼判断とArtifactの改変確認は両方必要である。署名が有効でも署名者が未承認なら
  Passにしない。
- 対象Componentと全取得経路を検証前に固定する。Developer端末、CI、Emergency復旧、Cache、
  Mirror、Auto-updateを未確認のまま除外しない。

## Assets, actors, identities, and trust boundaries

資産は、MCP Hostの実行権限、接続Credential、利用可能Data、導入するComponentのIdentityである。
ActorはComponent Publisher、Registry／Repository、Build System、Mirror、運用者、MCP Host、
攻撃者である。Trust Boundaryは、Source→取得経路、Source→Build、Artifact Store→Install、
Install→実行にある。

決定論的なEnforcement Pointは、Package取得、Image Pull、Build昇格、Install、Update、Process
起動等のAdmission Gateである。警告を表示するだけで実行を継続できる経路は強制点にならない。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 実行対象のMCP Componentを、承認済みSourceと一意に対応付けられる。 |
| SP-2 | ArtifactのDigest、署名、Attestation等を、独立して信頼する期待値・Identity・Policyに照らして使用前に検証する。 |
| SP-3 | 未信頼Source、検証不能、不一致、期限切れ・失効した信頼情報では、Install・更新・実行へ進めない。 |
| SP-4 | 通常、更新、Rollback、Cache、Mirror、復旧を含む全取得・実行経路で同じ検証を迂回できない。 |

## Scope calibration and adjacent assurance

有効な署名や一致するDigestは、Artifactの出所・同一性・改変有無を対象Policyの範囲で示すが、
Componentが脆弱性や悪意ある正規機能を持たないことまでは保証しない。正しく検証された悪性Component
でもC10.1.1をPassし得るため、Security Review、脆弱性管理、C10.1.2のAllowlist、C10.1.3の
Sandboxを別に評価する。

SBOMやScanner結果は有用な補助Evidenceだが、それだけでTrusted Sourceと暗号的検証の双方を
証明しない。逆に、特定のVersion固定は強いEvidenceになり得るが、要件本文は全Systemに単一の
Versioning方式を要求していない。

## Threat and failure-mode rationale

攻撃者が類似名Packageを公開する、Registry／Mirror／Cache上のArtifactを置換する、Build出力を
差し替える、更新経路を乗っ取ると、MCP ServerはHostのCredential、File、Network、Tool Authorityへ
到達し得る。Source確認か暗号検証の片方だけでは、未承認Publisherによる正しく署名されたArtifact、
または信頼Source名を装った改ざんArtifactを止められない。

ResearchはMITRE ATLAS等への関係を挙げるが、本Controlでは固定Snapshotに基づくMapping評価を
まだ行っていない。`threat_mappings`は空とし、Supply Chainの失敗経路を直接記述する。

## Verification

### Architecture and configuration review

MCP Component inventoryから、Source、Publisher／Build Identity、Artifact形式、Version／Digest、
取得経路、信頼Anchor、検証Tool、失敗時動作、実行点までを追う。Developer端末、CI/CD、Registry、
Mirror、Cache、Auto-update、復旧手順に未検証経路がないか確認する。

### Positive verification

承認済みSourceから取得した試験Artifactを、期待する署名者・Provenance・Digest等で検証し、
検証成功後だけInstallまたは起動できることを示す。結果を実際に起動したArtifact Identityへ
対応付ける。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 類似名だが未承認Publisher／RegistryのArtifactを指定 | 取得または実行前に拒否する。SP-1, SP-3 |
| N-2 | 承認Artifactを1 byte変更、または異なるDigestへ置換 | 暗号検証が失敗し実行しない。SP-2, SP-3 |
| N-3 | 未承認鍵で正しく署名したArtifactを指定 | 暗号自体が正しくても信頼Policy不一致で拒否する。SP-1, SP-2 |
| N-4 | Cache、Mirror、Rollback、Emergency手順から未検証Artifactを投入 | 通常経路と同じGateで拒否する。SP-4 |
| N-5 | 検証Serviceを停止または信頼情報を取得不能にする | Warning-onlyや検証省略へFallbackせず、安全に失敗する。SP-3 |

### Failure conditions

未承認Sourceから取得できる、実行Artifactと検証結果を対応付けられない、検証失敗後も起動する、
または一つでも未検証の導入・更新経路がある場合はFailを裏付ける。ComponentがAllowlistへ登録済み
という事実だけで、本ControlのSource・暗号検証をPassとしない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Component inventoryとSource policy | Component Owner | 全MCP Client／Serverと取得経路 | 導入・Source・Publisher変更時 | Revisionと承認記録を保持 | 実行Artifactを承認Sourceへ追跡可能 |
| 署名・Digest・Attestation検証結果 | Admission Gate／Build System | Install・更新・起動Artifact | Artifactごと、再Build時 | Artifact Identity、Policy Revision、時刻を改ざん防止 | 使用したArtifactに検証成功が対応 |
| Negative test結果 | Test Harness | N-1〜N-5と迂回経路 | 検証機構・取得経路変更後 | 模擬Artifactを使い試験IDを保持 | 未信頼・改ざん・検証不能を実行しない |

本Repositoryには期待値のみを置き、本番Artifact、秘密鍵、内部Registry資格情報を保存しない。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.1.2` | 暗号的に検証できても、そのServerの利用が環境Policyで許可されているとは限らない。 |
| `v1.0-C10.1.3` | 正しく取得したComponentが侵害・悪性化した場合の実行時Blast Radiusを制限する。 |
| `v1.0-C9.3.7` | Modelが示した外部Resourceを承認済みRegistry等で確認する。C10.1.1はComponent ArtifactのSourceと完全性に焦点を置く。 |

## Known limitations and uncertainty

信頼Source自体、Publisher Account、Build Pipeline、署名鍵が侵害された場合、有効な暗号Evidenceを
持つ悪性Artifactが発行され得る。暗号検証はCode Review、Behavior分析、Vulnerability管理、Runtime
Isolationを代替しない。Transitive dependencyをどこまで一つの「MCP Component」として個別検証するかは、
Build・Packaging境界に依存するため、評価Scopeを明示する。

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
