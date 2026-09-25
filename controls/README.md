# Controls View

This directory is the requirement-oriented entry point.

See [`plan.md`](plan.md) for the incremental plan for developing the controls knowledge base.

## Current artifacts

個別Controlは`control-records/<family>/<versioned-requirement>/README.md`に置き、
解釈・検証・証拠・限界の正本とする。新しい学習コンテンツは
`docs/learning/<family>/<versioned-section>/learning.md`にSection単位で置き、各Sectionの
全Requirementを一つの講義として扱う。両者は必要時に相互リンクし、CatalogはControl本文だけを参照する。
[Family README](control-records/c05-access-control-and-identity/README.md)は、Category、Section、
Requirementを俯瞰して個別Controlへ辿るための入口である。
[学習方針・進捗一覧](docs/learning/README.md)は従来どおり独立して管理する。

- [`catalog.yaml`](catalog.yaml): machine-readable control inventory with AISVS Verification
  Levels and lifecycle metadata; it is not a copy of the standard.
- [`schema/control-catalog.schema.json`](schema/control-catalog.schema.json): catalog
  structure and enumerated lifecycle states.
- [`templates/control.md`](templates/control.md): required structure for a substantive
  Control document.

### C5 Control records

C5の全11件について、解釈・適用範囲・脅威・検証・証拠期待値・限界を備えた
`verifiable` Controlを整備した。初期Golden ControlはC5.2.5である。
[C5 Family overview](control-records/c05-access-control-and-identity/README.md)では、
Categoryから各Requirementまでの保証範囲を短い問いで俯瞰できる。

| Requirement | Level | Control |
|---|---:|---|
| C5.1.1 | 3 | [高Risk操作のStep-up](control-records/c05-access-control-and-identity/v1.0-c5.1.1-step-up-authentication/README.md) |
| C5.1.2 | 3 | [Agentの短命・最小Scope・署名Token](control-records/c05-access-control-and-identity/v1.0-c5.1.2-short-lived-minimal-scoped-signed-agent-tokens/README.md) |
| C5.2.1 | 2 | [明示的AllowとDefault Deny](control-records/c05-access-control-and-identity/v1.0-c5.2.1-explicit-allow-default-deny-ai-resources/README.md) |
| C5.2.2 | 2 | [検索・組立でのEnd-user認可](control-records/c05-access-control-and-identity/v1.0-c5.2.2-end-user-authorization-retrieval-assembly/README.md) |
| C5.2.3 | 2 | [Sensitive DataのModel固定回避](control-records/c05-access-control-and-identity/v1.0-c5.2.3-sensitive-data-retrieval-not-model-storage/README.md) |
| C5.2.4 | 2 | [推論後の受取権限制御](control-records/c05-access-control-and-identity/v1.0-c5.2.4-post-inference-authorization-filtering/README.md) |
| C5.2.5 | 2 | [Agent認可PDPの隔離](control-records/c05-access-control-and-identity/v1.0-c5.2.5-agent-authorization-pdp-isolation/README.md) |
| C5.2.6 | 3 | [JIT特権と自動失効](control-records/c05-access-control-and-identity/v1.0-c5.2.6-just-in-time-privileged-access/README.md) |
| C5.2.7 | 3 | [分類Labelの伝播](control-records/c05-access-control-and-identity/v1.0-c5.2.7-downstream-classification-label-propagation/README.md) |
| C5.3.1 | 2 | [共有Serving状態のTenant分離](control-records/c05-access-control-and-identity/v1.0-c5.3.1-shared-model-serving-tenant-isolation/README.md) |
| C5.3.2 | 3 | [共有計算基盤のTenant分離](control-records/c05-access-control-and-identity/v1.0-c5.3.2-shared-compute-tenant-isolation/README.md) |

Validate the catalog and its repository-level invariants with:

```shell
python3 -m pip install -r controls/requirements.txt
python3 controls/scripts/validate_catalog.py
python3 controls/tests/test_validate_catalog.py
```

The current catalog contains metadata and substantive documents for all 11 C5
Requirements, all 11 C8 Requirements, all 34 C9 Requirements, and all 23 C10 Requirements (79 Controls).
`verification_level` records AISVS Level 1, 2, or 3; it is distinct from repository
Control maturity. All 79 substantive
Controls are `verifiable`, the current target for a mature repository Control. This
describes the artifacts, not a maintainer's learning progress or proof that a
product implements them. No Engineering Pattern Mapping is asserted.

## C8 development plan

[C8の全体分析と着手順序](docs/c08-landscape.md)に、全3節・11要件の保証範囲と
Researchからの注意点を整理した。C8.1 Access Controls on Memory & RAG Indicesの3要件に加え、
C8.2 Embedding Sanitization & Validationの5要件を`verifiable`まで整備した。C8.2では、Sensitive Fieldの
Pre-embedding処理、Vector異常のProduction投入前検疫、Source検証を伴うTrusted Memory昇格、
Retrieval操作ContentのVectorization前検査、既存Memoryとの矛盾Alertを別々の保証として扱う。
C8.3 Memory Expiry & Revocationの3要件も`verifiable`まで整備し、期限切れのLogical Exclusion、
宣言したScopeのMemory Reset、Forensic保持を伴うQuarantineを分離した。これによりC8全11要件の初期成熟化を完了した。

[C8 Family overview](control-records/c08-memory-embeddings-and-vector-database-security/README.md)は、
CategoryとSectionの保証境界、および整備済みRequirementへの入口を示す。

| Requirement | Level | Control |
|---|---:|---|
| C8.1.1 | 1 | [Vector IDとNamespaceをTenantごとに一意・衝突不能にする](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.1.1-tenant-unique-vector-identifiers-and-namespaces/README.md) |
| C8.1.2 | 2 | [Document Metadata Tagを初回Write後に不変にする](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.1.2-immutable-document-metadata-tags/README.md) |
| C8.1.3 | 2 | [すべてのRetrieval OperationでScopeを強制する](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.1.3-retrieval-scope-enforcement/README.md) |
| C8.2.1 | 1 | [Sensitive FieldをEmbedding前に検出・変換・除外する](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.1-sensitive-field-handling-before-embedding/README.md) |
| C8.2.2 | 2 | [異常なVectorをProduction Index投入前に検疫する](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.2-vector-anomaly-quarantine-before-production/README.md) |
| C8.2.3 | 2 | [Agent／Tool OutputをSource検証なしにTrusted Memoryへ書かない](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.3-source-validated-trusted-memory-writes/README.md) |
| C8.2.4 | 3 | [Retrieval操作用ContentをVectorization前に検出・拒否・検疫する](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.4-retrieval-manipulation-screening-before-vectorization/README.md) |
| C8.2.5 | 3 | [新規Memoryと既存Memoryの矛盾を検出しAlertする](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.5-memory-contradiction-detection-and-alerting/README.md) |
| C8.3.1 | 2 | [期限切れVectorをRetrieval結果から除外する](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.3.1-expired-vector-retrieval-exclusion/README.md) |
| C8.3.2 | 2 | [定義したMemory範囲を完全にResetできるようにする](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.3.2-complete-memory-reset/README.md) |
| C8.3.3 | 3 | [Quarantine Contentを保持しつつ全Retrieval結果から除外する](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.3.3-quarantine-retention-and-retrieval-exclusion/README.md) |

## C10 development plan

[C10の全体分析と着手順序](docs/c10-landscape.md)に、全4節・23要件の保証範囲と
Researchからの注意点を整理した。最初の代表要件はC10.2.7（Level 2：受信Tokenの
下流APIへの転送禁止）。この代表Controlを解釈・適用境界・脅威・正常/拒否試験・
証拠期待値・限界まで整備し、Catalogへ`verifiable`で追加した。
C10全4 Section・23要件を同じ成熟度まで整備した。C10.4ではSchemaと内容検査、ParameterとPayload、
Response署名、Local導入同意、Tool定義変更を別々のPass／Failとして扱う。学習進捗および製品適合とは独立する。

[C10 Family overview](control-records/c10-model-context-protocol-security/README.md)は、
CategoryとSectionの保証境界、および整備済みRequirementへの入口を示す。

| Requirement | Level | Control |
|---|---:|---|
| C10.1.1 | 1 | [MCP Componentを信頼済みSourceから取得し暗号的に検証する](control-records/c10-model-context-protocol-security/v1.0-c10.1.1-trusted-source-and-cryptographic-component-verification/README.md) |
| C10.1.2 | 2 | [Allowlistで許可したMCP Serverだけを接続・実行する](control-records/c10-model-context-protocol-security/v1.0-c10.1.2-allowlisted-mcp-server-admission/README.md) |
| C10.1.3 | 2 | [Local MCP Serverを最小権限Sandboxで実行する](control-records/c10-model-context-protocol-security/v1.0-c10.1.3-least-privilege-local-server-sandbox/README.md) |
| C10.2.1 | 1 | [各RequestでAccess Tokenを検証する](control-records/c10-model-context-protocol-security/v1.0-c10.2.1-per-request-access-token-validation/README.md) |
| C10.2.2 | 1 | [Issuer・Audience・Expiration・Scopeを検証する](control-records/c10-model-context-protocol-security/v1.0-c10.2.2-issuer-audience-expiration-and-scope-validation/README.md) |
| C10.2.3 | 1 | [Access TokenとUser Credentialを永続化しない](control-records/c10-model-context-protocol-security/v1.0-c10.2.3-no-access-token-or-user-credential-persistence/README.md) |
| C10.2.4 | 2 | [許可Scopeに応じてTool Discoveryを制限する](control-records/c10-model-context-protocol-security/v1.0-c10.2.4-scope-filtered-tool-discovery/README.md) |
| C10.2.5 | 2 | [各InvocationでToolとArgumentを認可する](control-records/c10-model-context-protocol-security/v1.0-c10.2.5-per-invocation-tool-and-argument-authorization/README.md) |
| C10.2.6 | 2 | [Session終了時にArtifactを除去する](control-records/c10-model-context-protocol-security/v1.0-c10.2.6-session-artifact-removal/README.md) |
| C10.2.7 | 2 | [受信したClient Access Tokenを下流APIへ転送しない](control-records/c10-model-context-protocol-security/v1.0-c10.2.7-no-client-token-passthrough-to-downstream-apis/README.md) |
| C10.3.1 | 1 | [Remote MCPに認証・暗号化済みStreamable HTTPを使う](control-records/c10-model-context-protocol-security/v1.0-c10.3.1-authenticated-encrypted-streamable-http/README.md) |
| C10.3.2 | 1 | [stdioを管理されたLocal環境だけに限定する](control-records/c10-model-context-protocol-security/v1.0-c10.3.2-stdio-only-in-controlled-local-environments/README.md) |
| C10.3.3 | 2 | [OriginとHostを独立に検証する](control-records/c10-model-context-protocol-security/v1.0-c10.3.3-independent-origin-and-host-validation/README.md) |
| C10.3.4 | 2 | [最低MCP Protocol Versionを強制する](control-records/c10-model-context-protocol-security/v1.0-c10.3.4-minimum-mcp-protocol-version-enforcement/README.md) |
| C10.3.5 | 3 | [Access Tokenを送信Clientへ拘束する](control-records/c10-model-context-protocol-security/v1.0-c10.3.5-sender-constrained-access-tokens/README.md) |
| C10.4.1 | 1 | [Tool Responseを宣言Schemaで検証する](control-records/c10-model-context-protocol-security/v1.0-c10.4.1-validate-tool-responses-against-schemas/README.md) |
| C10.4.2 | 1 | [Tool ResponseをIndirect Prompt Injection観点で検査する](control-records/c10-model-context-protocol-security/v1.0-c10.4.2-screen-tool-responses-for-indirect-prompt-injection/README.md) |
| C10.4.3 | 1 | [未知・過大なFunction Parameterを拒否する](control-records/c10-model-context-protocol-security/v1.0-c10.4.3-reject-unrecognized-or-oversized-function-parameters/README.md) |
| C10.4.4 | 2 | [Strict Server-side Schema Validationを強制する](control-records/c10-model-context-protocol-security/v1.0-c10.4.4-strict-server-side-schema-validation/README.md) |
| C10.4.5 | 2 | [Transport Payload Sizeを制限する](control-records/c10-model-context-protocol-security/v1.0-c10.4.5-transport-payload-size-limits/README.md) |
| C10.4.6 | 2 | [Tool Response署名でReplayを検出する](control-records/c10-model-context-protocol-security/v1.0-c10.4.6-signed-tool-responses-with-replay-protection/README.md) |
| C10.4.7 | 2 | [Local Server導入前に明示同意を求める](control-records/c10-model-context-protocol-security/v1.0-c10.4.7-explicit-local-server-installation-consent/README.md) |
| C10.4.8 | 3 | [Tool Definition変更後は再承認まで実行を止める](control-records/c10-model-context-protocol-security/v1.0-c10.4.8-tool-definition-change-reapproval/README.md) |

## C9 Control records

[C9の全体分析と着手順序](docs/c09-landscape.md)に、全6節・34要件の保証範囲、
C5との違い、Researchからの検討観点を整理した。C9全34件について、
解釈・適用境界・脅威・Positive/Negative Verification・証拠期待値・限界を備えた
`verifiable` Controlを整備した。最初の代表要件はC9.5.1。
これはRepository Artifactの完成であり、製品適合・攻撃への完全保証・学習完了を意味しない。
[C9 Family overview](control-records/c09-orchestration-and-agentic-security/README.md)では、
Categoryから各Requirementまでの保証範囲を短い問いで俯瞰できる。

| Requirement | Level | Control |
|---|---:|---|
| C9.1.1 | 1 | [ツール単位の資源上限と実行期限](control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.1-per-tool-resource-quotas-and-timeouts/README.md) |
| C9.1.2 | 1 | [実行全体の累積予算をRuntimeで強制する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.2-per-execution-cumulative-budgets/README.md) |
| C9.1.3 | 2 | [Agent群全体を停止できるKill-switch](control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.3-swarm-wide-agent-halt/README.md) |
| C9.2.1 | 1 | [高影響操作を人の承認前に実行させない](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.1-human-approval-before-high-impact-actions/README.md) |
| C9.2.2 | 2 | [承認画面に実際の操作内容を完全かつ正確に示す](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.2-complete-canonical-approval-display/README.md) |
| C9.2.3 | 2 | [高影響操作の可逆性を信頼できる根拠で分類する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.3-trusted-action-reversibility-classification/README.md) |
| C9.2.4 | 2 | [可逆性分類を実行制限へ結び付ける](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.4-enforce-reversibility-based-action-policy/README.md) |
| C9.2.5 | 2 | [Agentの自己変更能力を強制可能な範囲に限定する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.5-bounded-agent-self-modification/README.md) |
| C9.2.6 | 2 | [高Risk操作のAI補助レビューを決定論的Gateに追加する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.6-additive-ai-review-before-high-risk-actions/README.md) |
| C9.2.7 | 2 | [AI補助レビューの入力・結果・実行経路を操作から守る](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.7-protect-ai-action-review-from-manipulation/README.md) |
| C9.2.8 | 3 | [承認を操作・要求者・実行Contextと一回限りの値へ暗号的に結合する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.8-cryptographically-bound-single-use-approvals/README.md) |
| C9.2.9 | 3 | [承認を発行する鍵・資格情報をAgentから隔離する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.9-approval-issuing-key-and-credential-isolation/README.md) |
| C9.2.10 | 3 | [行動連鎖の最大影響を承認Gateへ反映する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.10-chain-wide-highest-impact-approval/README.md) |
| C9.3.1 | 1 | [ツール実行を最小権限で隔離する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.1-least-privilege-tool-execution-isolation/README.md) |
| C9.3.2 | 1 | [ツール出力をSchemaに照らして検証する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.2-tool-output-schema-validation/README.md) |
| C9.3.3 | 2 | [Tool Manifestに権限・資源・出力検証要件を宣言する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.3-explicit-tool-manifest-security-requirements/README.md) |
| C9.3.4 | 2 | [Tool Manifestの制約をRuntimeが強制する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.4-runtime-enforcement-of-tool-manifests/README.md) |
| C9.3.5 | 2 | [非信頼データ処理をツール呼出し能力から隔離する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.5-isolate-untrusted-data-processing-from-tool-capabilities/README.md) |
| C9.3.6 | 2 | [非信頼ツール出力の処理とAgent操作を構造的に分離する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.6-architectural-separation-of-untrusted-tool-outputs/README.md) |
| C9.3.7 | 2 | [モデルが示した外部資源を承認済み一覧で確認する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.7-verify-model-named-external-resources/README.md) |
| C9.3.8 | 3 | [Policy違反時にツールを自動的に封じ込める](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.8-automatic-tool-containment-on-policy-violation/README.md) |
| C9.4.1 | 2 | [各Agent Instanceを固有の暗号的Identityで認証する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.4.1-unique-cryptographic-agent-instance-identity/README.md) |
| C9.4.2 | 2 | [Agent操作を実行連鎖へ暗号的に結び付ける](control-records/c09-orchestration-and-agentic-security/v1.0-c9.4.2-cryptographic-action-chain-attribution/README.md) |
| C9.4.3 | 3 | [AgentのIdentity資格情報を定めた周期で更新する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.4.3-scheduled-agent-credential-rotation/README.md) |
| C9.4.4 | 3 | [呼出し間に保存するAgent状態の完全性を保護する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.4.4-integrity-protection-for-persisted-agent-state/README.md) |
| C9.5.1 | 2 | [Agentのツールと引数に対する細粒度認可](control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.1-fine-grained-tool-and-parameter-authorization/README.md) |
| C9.5.2 | 2 | [利用者の委任Contextを各下流呼出しで維持・強制する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.2-scope-limited-user-context-through-downstream-calls/README.md) |
| C9.5.3 | 2 | [アクセス制御をモデルではなくApplicationで強制する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.3-application-enforced-authorization-outside-model-decisions/README.md) |
| C9.5.4 | 2 | [Runtimeの秘密・資格情報をモデルから観測できなくする](control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.4-keep-runtime-secrets-out-of-model-context/README.md) |
| C9.5.5 | 2 | [Agent間のタスク委任を明示的Policyで制限する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.5-explicit-inter-agent-delegation-policy/README.md) |
| C9.5.6 | 3 | [長時間Agentの各特権操作を現在のPolicyで再評価する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.6-current-authorization-for-each-privileged-action/README.md) |
| C9.6.1 | 1 | [推論と出力を手動で停止できるようにする](control-records/c09-orchestration-and-agentic-security/v1.0-c9.6.1-manual-stop-of-inference-and-outputs/README.md) |
| C9.6.2 | 2 | [承認期限が切れた操作を実行させない](control-records/c09-orchestration-and-agentic-security/v1.0-c9.6.2-deny-actions-after-approval-timeout/README.md) |
| C9.6.3 | 3 | [停止指示をAgentから隔離した別経路で強制する](control-records/c09-orchestration-and-agentic-security/v1.0-c9.6.3-out-of-band-shutdown-control-isolation/README.md) |

今後は利用・レビューからの改善を行う。Engineering Mappingは別の評価として扱う。

## Navigation and learning

- [Common Controls learning method](docs/learning/README.md): shared teaching,
  dialogue-reconstruction, insight, storage, and quality rules for every AISVS
  Category.
- [AISVS C5 Access Control and Identity learning guide](docs/learning/c05-access-control-and-identity/README.md):
  legacy Requirement sequence, progress, and persistent learning notes.
- [AISVS C10 Model Context Protocol Security learning guide](docs/learning/c10-model-context-protocol-security/README.md):
  current Section-based sequence for the four C10 lectures.
- [AISVS C5 family overview](control-records/c05-access-control-and-identity/README.md):
  Category, Section, and Requirement-level questions and prohibited failure states.
- [AISVS C9 family overview](control-records/c09-orchestration-and-agentic-security/README.md):
  a compact overview of what each C9 assurance layer asks and must prevent.

## Control record layout

Store substantive AISVS Control records under one AISVS-family directory:

```text
control-records/
└── cNN-family-slug/
    ├── README.md
    └── vX.Y-cN.N.N-descriptive-control-name/
        └── README.md

docs/learning/
└── cNN-family-slug/
    ├── README.md
    └── vX.Y-cN.N-section-slug/
        └── learning.md
```

For example, the Golden Control is stored under
`c05-access-control-and-identity/`. The family number and versioned Requirement ID
provide direct upstream traceability; the descriptive suffix keeps the security
subject understandable without looking up the identifier.

The Control family `README.md` is the navigation and assurance overview rendered by
default in GitHub. Individual Requirement `README.md` files remain the canonical
Control interpretations, and `catalog.yaml` points only to those individual files.

Section learning notes are revision-aware teaching artifacts. They cover all
Requirements in one Section but do not replace the individual Controls. Existing
C5/C9 Requirement-level notes are retained as legacy learning history and are not
automatically moved or merged.

Within `control-records/`, use only the family and versioned Requirement levels;
do not create Section directories such as `c05.2/`. Versioned Section directories
are used only under `docs/learning/` and only when a substantive lecture exists.
Do not create empty family directories.

The filesystem layout is a navigation aid. `catalog.yaml` remains authoritative for
source version, lifecycle state, Verification Level, maturity, related Requirements, and
Mappings. When AISVS renames or renumbers content, preserve the historical record
and perform a semantic change review; do not silently rename or overwrite it.

## Primary backbone

OWASP AISVS is the primary verification/control backbone.

## AISVS Research documentation

When developing, interpreting, mapping, or reviewing an AISVS control, always read
both:

1. the requirement in the applicable versioned AISVS chapter; and
2. the corresponding chapter or section page in the
   [AISVS Research Wiki](https://github.com/OWASP/AISVS/blob/main/1.0/research/README.md).

Use the Research documentation to investigate threat rationale, verification
approaches, tooling maturity, implementation caveats, open questions, and related
requirements. It is a required research input, but it is supporting material rather
than the normative requirement text.

If the Research documentation and the versioned requirement appear inconsistent,
do not silently choose or merge them. Treat the versioned requirement as the AISVS
normative source, record the discrepancy and uncertainty, and determine whether an
upstream or repository follow-up is required.

Do not copy Research pages wholesale. Record the page URL and reviewed source state,
summarize only the relevant findings with attribution, and independently validate
security-significant claims before using them in control interpretation,
verification, evidence expectations, or mappings.

Do not copy the entire AISVS standard into this repository. Prefer:

- versioned requirement ID;
- concise interpretation;
- security objective and required security properties;
- verification evidence;
- optional references to separately maintained mapping assessments;
- source version/status.

Example conceptual record:

```yaml
source: owasp-aisvs
requirement: v1.0-C9.4.3
interpretation: "...repository-authored interpretation..."
mapping_assessment_refs: []
```

Mapping assessment status and relationship details belong under `mappings/`.
Control records may link to those canonical assessments but must not duplicate them.

## Why controls are separate from engineering patterns

Controls answer "what should be verified?" while engineering patterns answer "how should we build and test it?"

A single pattern can satisfy or partially address many controls, and a single control can require several patterns.

Develop each side independently. Mapping is a later, derived artifact and does not
determine control maturity. Do not force a one-to-one mapping or generate Pattern
candidates from the Control inventory. See [`../mappings/README.md`](../mappings/README.md).
