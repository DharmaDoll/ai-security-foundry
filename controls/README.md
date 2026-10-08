# Controls — 保証項目を探す

`controls/` は「何を満たし、どう検証するか」を探すための入口です。
まず [AISVS Familyの見取り図](family-assurance-map.md) でシステム上の関係を掴み、
下のFamily一覧からSection、個別Controlへ進んでください。
見取り図は代表的な構成を示すもので、要件の網羅図や製品の適合判定ではありません。

## Family別Control案内

各FamilyのREADMEには、Categoryの保証目的、**Sectionの見取り図**、整備済みRequirementごとの
「問うこと」「できてはいけないこと」と、**個別Control本文へのリンク**があります。
個別Control本文が解釈・検証方法・証拠期待値・限界の正本です。

| Family（個別Control一覧へ） | 主に確認すること |
|---|---|
| [C2 Input Validation](control-records/c02-input-validation/README.md) | 入力と取得内容が、変換や複数の形式を経ても検査の想定から外れないか。 |
| [C5 Access Control and Identity](control-records/c05-access-control-and-identity/README.md) | 主体・権限・Credential・Tenant境界を、AIを介しても維持できるか。 |
| [C7 Model Behavior, Output Control & Safety Assurance](control-records/c07-model-behavior-output-control-and-safety-assurance/README.md) | Model出力の形式、信頼性、安全性、出典を利用前に確認できるか。 |
| [C8 Memory, Embeddings & Vector Database Security](control-records/c08-memory-embeddings-and-vector-database-security/README.md) | MemoryやVectorを、正しい範囲・出所・期限・信頼状態で扱えるか。 |
| [C9 Orchestration and Agentic Security](control-records/c09-orchestration-and-agentic-security/README.md) | Agentの行動・委任・実行量・承認・停止を制御できるか。 |
| [C10 Model Context Protocol Security](control-records/c10-model-context-protocol-security/README.md) | MCPの構成要素、要求、Transport、Tool入出力を境界ごとに検証できるか。 |
| [C11 Adversarial Robustness](control-records/c11-adversarial-robustness/README.md) | 敵対的入力、学習Dataの推測、Model抽出、実行時異常に備えられるか。 |
| [C12 Monitoring, Logging & Anomaly Detection](control-records/c12-monitoring-logging-and-anomaly-detection/README.md) | AI処理・変更を再構成し、異常を検知・調査できるか。 |

[AISVS Familyの見取り図](family-assurance-map.md) には12 Familyが登場します。
この一覧は、そのうち個別Controlを整備したFamilyへの案内です。

## 個別Control（IDから直接開く）

IDが分かっている場合はここからControl本文を直接開けます。各Controlの内容と隣接要件の違いは、
上のFamily READMEからも確認できます。この一覧は[Catalog](catalog.yaml)の`control_ref`を辿る索引です。

### C2

| Section | Control本文 |
|---|---|
| C2.1 | [v1.0-C2.1.1](control-records/c02-input-validation/v1.0-c2.1.1-normalize-input-before-tokenization-or-embedding/README.md) · [v1.0-C2.1.2](control-records/c02-input-validation/v1.0-c2.1.2-detect-and-mitigate-encoded-input-smuggling/README.md) · [v1.0-C2.1.3](control-records/c02-input-validation/v1.0-c2.1.3-screen-and-block-model-steering-inputs/README.md) · [v1.0-C2.1.4](control-records/c02-input-validation/v1.0-c2.1.4-reject-over-limit-input-without-truncation/README.md) · [v1.0-C2.1.5](control-records/c02-input-validation/v1.0-c2.1.5-allowlist-required-input-characters/README.md) · [v1.0-C2.1.6](control-records/c02-input-validation/v1.0-c2.1.6-preserve-instruction-hierarchy-across-steps/README.md) · [v1.0-C2.1.7](control-records/c02-input-validation/v1.0-c2.1.7-render-reserved-tokens-as-literal-content/README.md) · [v1.0-C2.1.8](control-records/c02-input-validation/v1.0-c2.1.8-detect-many-shot-jailbreak-patterns/README.md) |
| C2.2 | [v1.0-C2.2.1](control-records/c02-input-validation/v1.0-c2.2.1-screen-prompts-before-model-context/README.md) · [v1.0-C2.2.2](control-records/c02-input-validation/v1.0-c2.2.2-evaluate-content-classification-for-unsupported-languages/README.md) · [v1.0-C2.2.3](control-records/c02-input-validation/v1.0-c2.2.3-check-non-text-inputs-for-hidden-attacks/README.md) · [v1.0-C2.2.4](control-records/c02-input-validation/v1.0-c2.2.4-detect-and-block-cross-modal-attacks/README.md) |

### C5

| Section | Control本文 |
|---|---|
| C5.1 | [v1.0-C5.1.1](control-records/c05-access-control-and-identity/v1.0-c5.1.1-step-up-authentication/README.md) · [v1.0-C5.1.2](control-records/c05-access-control-and-identity/v1.0-c5.1.2-short-lived-minimal-scoped-signed-agent-tokens/README.md) |
| C5.2 | [v1.0-C5.2.1](control-records/c05-access-control-and-identity/v1.0-c5.2.1-explicit-allow-default-deny-ai-resources/README.md) · [v1.0-C5.2.2](control-records/c05-access-control-and-identity/v1.0-c5.2.2-end-user-authorization-retrieval-assembly/README.md) · [v1.0-C5.2.3](control-records/c05-access-control-and-identity/v1.0-c5.2.3-sensitive-data-retrieval-not-model-storage/README.md) · [v1.0-C5.2.4](control-records/c05-access-control-and-identity/v1.0-c5.2.4-post-inference-authorization-filtering/README.md) · [v1.0-C5.2.5](control-records/c05-access-control-and-identity/v1.0-c5.2.5-agent-authorization-pdp-isolation/README.md) · [v1.0-C5.2.6](control-records/c05-access-control-and-identity/v1.0-c5.2.6-just-in-time-privileged-access/README.md) · [v1.0-C5.2.7](control-records/c05-access-control-and-identity/v1.0-c5.2.7-downstream-classification-label-propagation/README.md) |
| C5.3 | [v1.0-C5.3.1](control-records/c05-access-control-and-identity/v1.0-c5.3.1-shared-model-serving-tenant-isolation/README.md) · [v1.0-C5.3.2](control-records/c05-access-control-and-identity/v1.0-c5.3.2-shared-compute-tenant-isolation/README.md) |

### C7

| Section | Control本文 |
|---|---|
| C7.1 | [v1.0-C7.1.1](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.1.1-validate-and-reject-model-outputs-by-schema/README.md) · [v1.0-C7.1.2](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.1.2-bound-model-output-length-and-termination/README.md) |
| C7.2 | [v1.0-C7.2.1](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.2.1-estimate-generated-answer-reliability/README.md) · [v1.0-C7.2.2](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.2.2-block-or-fallback-below-confidence-threshold/README.md) · [v1.0-C7.2.3](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.2.3-additional-verification-for-high-risk-responses/README.md) |
| C7.3 | [v1.0-C7.3.1](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.3.1-classify-and-block-harmful-responses/README.md) · [v1.0-C7.3.2](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.3.2-block-system-prompt-and-backend-data-disclosure/README.md) · [v1.0-C7.3.3](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.3.3-prevent-output-triggered-outbound-requests/README.md) · [v1.0-C7.3.4](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.3.4-check-hidden-encoded-and-misleading-outputs/README.md) |
| C7.4 | [v1.0-C7.4.1](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.4.1-attribute-rag-responses-to-source-documents/README.md) · [v1.0-C7.4.2](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.4.2-derive-rag-attributions-from-retrieval-metadata/README.md) · [v1.0-C7.4.3](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.4.3-trace-rag-claims-to-retrieved-chunks/README.md) · [v1.0-C7.4.4](control-records/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.4.4-watermark-ai-generated-media/README.md) |

### C8

| Section | Control本文 |
|---|---|
| C8.1 | [v1.0-C8.1.1](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.1.1-tenant-unique-vector-identifiers-and-namespaces/README.md) · [v1.0-C8.1.2](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.1.2-immutable-document-metadata-tags/README.md) · [v1.0-C8.1.3](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.1.3-retrieval-scope-enforcement/README.md) |
| C8.2 | [v1.0-C8.2.1](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.1-sensitive-field-handling-before-embedding/README.md) · [v1.0-C8.2.2](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.2-vector-anomaly-quarantine-before-production/README.md) · [v1.0-C8.2.3](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.3-source-validated-trusted-memory-writes/README.md) · [v1.0-C8.2.4](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.4-retrieval-manipulation-screening-before-vectorization/README.md) · [v1.0-C8.2.5](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.5-memory-contradiction-detection-and-alerting/README.md) |
| C8.3 | [v1.0-C8.3.1](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.3.1-expired-vector-retrieval-exclusion/README.md) · [v1.0-C8.3.2](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.3.2-complete-memory-reset/README.md) · [v1.0-C8.3.3](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.3.3-quarantine-retention-and-retrieval-exclusion/README.md) |

### C9

| Section | Control本文 |
|---|---|
| C9.1 | [v1.0-C9.1.1](control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.1-per-tool-resource-quotas-and-timeouts/README.md) · [v1.0-C9.1.2](control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.2-per-execution-cumulative-budgets/README.md) · [v1.0-C9.1.3](control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.3-swarm-wide-agent-halt/README.md) |
| C9.2 | [v1.0-C9.2.1](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.1-human-approval-before-high-impact-actions/README.md) · [v1.0-C9.2.2](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.2-complete-canonical-approval-display/README.md) · [v1.0-C9.2.3](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.3-trusted-action-reversibility-classification/README.md) · [v1.0-C9.2.4](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.4-enforce-reversibility-based-action-policy/README.md) · [v1.0-C9.2.5](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.5-bounded-agent-self-modification/README.md) · [v1.0-C9.2.6](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.6-additive-ai-review-before-high-risk-actions/README.md) · [v1.0-C9.2.7](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.7-protect-ai-action-review-from-manipulation/README.md) · [v1.0-C9.2.8](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.8-cryptographically-bound-single-use-approvals/README.md) · [v1.0-C9.2.9](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.9-approval-issuing-key-and-credential-isolation/README.md) · [v1.0-C9.2.10](control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.10-chain-wide-highest-impact-approval/README.md) |
| C9.3 | [v1.0-C9.3.1](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.1-least-privilege-tool-execution-isolation/README.md) · [v1.0-C9.3.2](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.2-tool-output-schema-validation/README.md) · [v1.0-C9.3.3](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.3-explicit-tool-manifest-security-requirements/README.md) · [v1.0-C9.3.4](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.4-runtime-enforcement-of-tool-manifests/README.md) · [v1.0-C9.3.5](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.5-isolate-untrusted-data-processing-from-tool-capabilities/README.md) · [v1.0-C9.3.6](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.6-architectural-separation-of-untrusted-tool-outputs/README.md) · [v1.0-C9.3.7](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.7-verify-model-named-external-resources/README.md) · [v1.0-C9.3.8](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.8-automatic-tool-containment-on-policy-violation/README.md) |
| C9.4 | [v1.0-C9.4.1](control-records/c09-orchestration-and-agentic-security/v1.0-c9.4.1-unique-cryptographic-agent-instance-identity/README.md) · [v1.0-C9.4.2](control-records/c09-orchestration-and-agentic-security/v1.0-c9.4.2-cryptographic-action-chain-attribution/README.md) · [v1.0-C9.4.3](control-records/c09-orchestration-and-agentic-security/v1.0-c9.4.3-scheduled-agent-credential-rotation/README.md) · [v1.0-C9.4.4](control-records/c09-orchestration-and-agentic-security/v1.0-c9.4.4-integrity-protection-for-persisted-agent-state/README.md) |
| C9.5 | [v1.0-C9.5.1](control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.1-fine-grained-tool-and-parameter-authorization/README.md) · [v1.0-C9.5.2](control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.2-scope-limited-user-context-through-downstream-calls/README.md) · [v1.0-C9.5.3](control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.3-application-enforced-authorization-outside-model-decisions/README.md) · [v1.0-C9.5.4](control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.4-keep-runtime-secrets-out-of-model-context/README.md) · [v1.0-C9.5.5](control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.5-explicit-inter-agent-delegation-policy/README.md) · [v1.0-C9.5.6](control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.6-current-authorization-for-each-privileged-action/README.md) |
| C9.6 | [v1.0-C9.6.1](control-records/c09-orchestration-and-agentic-security/v1.0-c9.6.1-manual-stop-of-inference-and-outputs/README.md) · [v1.0-C9.6.2](control-records/c09-orchestration-and-agentic-security/v1.0-c9.6.2-deny-actions-after-approval-timeout/README.md) · [v1.0-C9.6.3](control-records/c09-orchestration-and-agentic-security/v1.0-c9.6.3-out-of-band-shutdown-control-isolation/README.md) |

### C10

| Section | Control本文 |
|---|---|
| C10.1 | [v1.0-C10.1.1](control-records/c10-model-context-protocol-security/v1.0-c10.1.1-trusted-source-and-cryptographic-component-verification/README.md) · [v1.0-C10.1.2](control-records/c10-model-context-protocol-security/v1.0-c10.1.2-allowlisted-mcp-server-admission/README.md) · [v1.0-C10.1.3](control-records/c10-model-context-protocol-security/v1.0-c10.1.3-least-privilege-local-server-sandbox/README.md) |
| C10.2 | [v1.0-C10.2.1](control-records/c10-model-context-protocol-security/v1.0-c10.2.1-per-request-access-token-validation/README.md) · [v1.0-C10.2.2](control-records/c10-model-context-protocol-security/v1.0-c10.2.2-issuer-audience-expiration-and-scope-validation/README.md) · [v1.0-C10.2.3](control-records/c10-model-context-protocol-security/v1.0-c10.2.3-no-access-token-or-user-credential-persistence/README.md) · [v1.0-C10.2.4](control-records/c10-model-context-protocol-security/v1.0-c10.2.4-scope-filtered-tool-discovery/README.md) · [v1.0-C10.2.5](control-records/c10-model-context-protocol-security/v1.0-c10.2.5-per-invocation-tool-and-argument-authorization/README.md) · [v1.0-C10.2.6](control-records/c10-model-context-protocol-security/v1.0-c10.2.6-session-artifact-removal/README.md) · [v1.0-C10.2.7](control-records/c10-model-context-protocol-security/v1.0-c10.2.7-no-client-token-passthrough-to-downstream-apis/README.md) |
| C10.3 | [v1.0-C10.3.1](control-records/c10-model-context-protocol-security/v1.0-c10.3.1-authenticated-encrypted-streamable-http/README.md) · [v1.0-C10.3.2](control-records/c10-model-context-protocol-security/v1.0-c10.3.2-stdio-only-in-controlled-local-environments/README.md) · [v1.0-C10.3.3](control-records/c10-model-context-protocol-security/v1.0-c10.3.3-independent-origin-and-host-validation/README.md) · [v1.0-C10.3.4](control-records/c10-model-context-protocol-security/v1.0-c10.3.4-minimum-mcp-protocol-version-enforcement/README.md) · [v1.0-C10.3.5](control-records/c10-model-context-protocol-security/v1.0-c10.3.5-sender-constrained-access-tokens/README.md) |
| C10.4 | [v1.0-C10.4.1](control-records/c10-model-context-protocol-security/v1.0-c10.4.1-validate-tool-responses-against-schemas/README.md) · [v1.0-C10.4.2](control-records/c10-model-context-protocol-security/v1.0-c10.4.2-screen-tool-responses-for-indirect-prompt-injection/README.md) · [v1.0-C10.4.3](control-records/c10-model-context-protocol-security/v1.0-c10.4.3-reject-unrecognized-or-oversized-function-parameters/README.md) · [v1.0-C10.4.4](control-records/c10-model-context-protocol-security/v1.0-c10.4.4-strict-server-side-schema-validation/README.md) · [v1.0-C10.4.5](control-records/c10-model-context-protocol-security/v1.0-c10.4.5-transport-payload-size-limits/README.md) · [v1.0-C10.4.6](control-records/c10-model-context-protocol-security/v1.0-c10.4.6-signed-tool-responses-with-replay-protection/README.md) · [v1.0-C10.4.7](control-records/c10-model-context-protocol-security/v1.0-c10.4.7-explicit-local-server-installation-consent/README.md) · [v1.0-C10.4.8](control-records/c10-model-context-protocol-security/v1.0-c10.4.8-tool-definition-change-reapproval/README.md) |

### C11

| Section | Control本文 |
|---|---|
| C11.1 | [v1.0-C11.1.1](control-records/c11-adversarial-robustness/v1.0-c11.1.1-model-alignment-and-safety-training/README.md) · [v1.0-C11.1.2](control-records/c11-adversarial-robustness/v1.0-c11.1.2-run-versioned-alignment-suite-on-model-updates/README.md) · [v1.0-C11.1.3](control-records/c11-adversarial-robustness/v1.0-c11.1.3-evaluate-modality-relevant-adversarial-attacks/README.md) · [v1.0-C11.1.4](control-records/c11-adversarial-robustness/v1.0-c11.1.4-harden-model-against-adversarial-inputs/README.md) · [v1.0-C11.1.5](control-records/c11-adversarial-robustness/v1.0-c11.1.5-measure-harmful-content-rate-and-flag-regressions/README.md) |

### C12

| Section | Control本文 |
|---|---|
| C12.1 | [v1.0-C12.1.1](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.1.1-log-ai-interactions-with-session-context/README.md) · [v1.0-C12.1.2](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.1.2-log-safety-filter-and-policy-decisions/README.md) · [v1.0-C12.1.3](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.1.3-structured-interoperable-inference-event-logs/README.md) · [v1.0-C12.1.4](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.1.4-log-rag-retrieval-queries-documents-and-sources/README.md) |
| C12.2 | [v1.0-C12.2.1](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.2.1-detect-and-alert-on-known-adversarial-inputs/README.md) · [v1.0-C12.2.2](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.2.2-detect-unusual-conversation-and-probing-behavior/README.md) · [v1.0-C12.2.3](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.2.3-detect-ai-specific-attacks-with-custom-rules/README.md) · [v1.0-C12.2.4](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.2.4-include-offending-query-metadata-in-extraction-alerts/README.md) · [v1.0-C12.2.5](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.2.5-attribute-token-usage-by-user-session-feature-and-team/README.md) · [v1.0-C12.2.6](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.2.6-monitor-llm-api-traffic-for-covert-c2-activity/README.md) |
| C12.3 | [v1.0-C12.3.1](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.3.1-monitor-input-distribution-drift-by-data-type/README.md) · [v1.0-C12.3.2](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.3.2-identify-and-flag-factually-wrong-contradictory-or-fabricated-outputs/README.md) · [v1.0-C12.3.3](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.3.3-track-hallucination-rate-over-time/README.md) · [v1.0-C12.3.4](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.3.4-distinguish-unexplained-behavior-from-expected-drift/README.md) |
| C12.4 | [v1.0-C12.4.1](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.4.1-evaluate-autonomous-action-triggers/README.md) · [v1.0-C12.4.2](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.4.2-audit-security-critical-proactive-actions/README.md) · [v1.0-C12.4.3](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.4.3-log-kill-switch-activations-and-override-commands/README.md) |
| C12.5 | [v1.0-C12.5.1](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.5.1-record-complete-dataset-lineage/README.md) · [v1.0-C12.5.2](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.5.2-log-all-labeling-activities/README.md) · [v1.0-C12.5.3](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.5.3-immutable-audit-records-for-model-changes/README.md) · [v1.0-C12.5.4](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.5.4-tag-ingested-documents-at-write-time/README.md) |

## 資料の使い分け

| 探したいもの | 入口 |
|---|---|
| 個別ControlのID、AISVS Verification Level、成熟度、参照先 | [Control Catalog](catalog.yaml) |
| Section単位の講義、対話、学習進捗 | [学習ガイド](learning/README.md) |
| 整備順序と今後の作業 | [Controls計画](plan.md) |
| Control本文の構成とCatalogの形式 | [Controlテンプレート](templates/control.md)・[Catalog Schema](schema/control-catalog.schema.json) |
| 執筆・検証時のルール | [Controls Domain Instructions](AGENTS.md) |

Controlの成熟度は文書の状態であり、製品の適合や学習完了を示しません。
AISVSは検証要件の一次資料です。Control本文はその原文の代替ではなく、Repositoryの解釈です。
AISVS Researchは脅威や検証を考えるための補助資料であり、追加の規範要件とは扱いません。
参照している版・成熟状態は [Source Registry](../sources/registry.yaml) を確認してください。
Engineering Patternとの関係は、両者を独立に理解した後に [Mappings](../mappings/README.md) で評価します。
