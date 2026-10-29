# Controls — 保証項目を探す

`controls/` は「何を満たし、どう検証するか」を探すための入口です。
まず [AISVS Familyの見取り図](family-assurance-map.md) でシステム上の関係を掴み、
下のFamily一覧から対象を選び、Section、個別Controlへ進んでください。
見取り図は代表的な構成を示すもので、要件の網羅図や製品の適合判定ではありません。

## Family別Control案内

AISVS v1.0の全12 Familyを示します。**主に確認すること**は保証の問い、
**主な検討場面**は設計中にそのFamilyを開くきっかけとなる代表例です。
実際の適用範囲は個別Requirementと製品の構成から判断します。
各FamilyのREADMEには、Categoryの保証目的、**Sectionの見取り図**、Requirementごとの
「問うこと」「できてはいけないこと」と、**個別Control本文へのリンク**があります。
個別Control本文が解釈・検証方法・証拠期待値・限界の正本です。
採用済み固定Revisionの全191 Requirementに個別Control本文を整備しています。
これは文書の整備状況であり、製品の適合やAISVS 1.01への移行を意味しません。
各Familyの学習ガイドへのリンクを併記します。学習資料の存在や学習の完了は、
個別Controlの整備・成熟とは別です。

| Family | 主に確認すること | 主な検討場面 | 学習ガイド |
|---|---|---|---|
| [C1 Training Data Integrity & Traceability](control-records/c01-training-data-integrity-and-traceability/README.md) | 学習Dataの出所・改ざん・Label・品質を追跡し、検証できるか。 | Datasetの収集・受入れ、Labeling、学習・再学習。 | [学習ガイド](learning/c01-training-data-integrity-and-traceability/README.md) |
| [C2 Input Validation](control-records/c02-input-validation/README.md) | 入力と取得内容が、変換や複数の形式を経ても検査の想定から外れないか。 | User入力、検索文書、画像・音声などをModel Contextへ取り込むとき。 | [学習ガイド](learning/c02-input-validation/README.md) |
| [C3 Model Lifecycle Management & Change Control](control-records/c03-model-lifecycle-management-and-change-control/README.md) | Model Artifactと変更を検証し、許可した版だけを本番へ反映・復旧できるか。 | Model・Provider版の変更、Fine-tuning、段階的な配備とRollback。 | [学習ガイド](learning/c03-model-lifecycle-management-and-change-control/README.md) |
| [C4 Infrastructure, Configuration & Deployment Security](control-records/c04-infrastructure-configuration-and-deployment-security/README.md) | Model実行基盤・Accelerator・Edge環境を隔離し、実行状態を検証できるか。 | Model Serving、GPU共有、Edge・Mobileへの配備。 | [学習ガイド](learning/c04-infrastructure-configuration-and-deployment-security/README.md) |
| [C5 Access Control & Identity for AI Components & Users](control-records/c05-access-control-and-identity/README.md) | 主体・権限・Credential・Tenant境界を、AIを介しても維持できるか。 | 権限付きRAG、複数Tenantでの共有基盤、Agentへの権限付与。 | [学習ガイド](learning/c05-access-control-and-identity/README.md) |
| [C6 Supply Chain Security for Models](control-records/c06-supply-chain-security-for-models/README.md) | 外部由来のModel・Dataset・Adapterの出所と完全性を確認し、構成を追跡できるか。 | Third-party Artifactの取込み、AI BOMの作成、供給元の変更。 | [学習ガイド](learning/c06-supply-chain-security-for-models/README.md) |
| [C7 Model Behavior, Output Control & Safety Assurance](control-records/c07-model-behavior-output-control-and-safety-assurance/README.md) | Model出力の形式、信頼性、安全性、出典を利用前に確認できるか。 | 回答の公開、出力のTool利用、RAGの引用、生成Mediaの配布。 | [学習ガイド](learning/c07-model-behavior-output-control-and-safety-assurance/README.md) |
| [C8 Memory, Embeddings & Vector Database Security](control-records/c08-memory-embeddings-and-vector-database-security/README.md) | MemoryやVectorを、正しい範囲・出所・期限・信頼状態で扱えるか。 | RAG Indexの作成・検索、Agent Memoryの書込み・失効・削除。 | [学習ガイド](learning/c08-memory-embeddings-and-vector-database-security/README.md) |
| [C9 Orchestration and Agentic Security](control-records/c09-orchestration-and-agentic-security/README.md) | Agentの行動・委任・実行量・承認・停止を制御できるか。 | Agentによる連続Tool実行、他Agentへの委任、高影響操作の承認。 | [学習ガイド](learning/c09-orchestration-and-agentic-security/README.md) |
| [C10 Model Context Protocol (MCP) Security](control-records/c10-model-context-protocol-security/README.md) | MCPの構成要素、要求、Transport、Tool入出力を境界ごとに検証できるか。 | MCP Serverの導入・接続、Toolの公開・呼出し、下流API連携。 | [学習ガイド](learning/c10-model-context-protocol-security/README.md) |
| [C11 Adversarial Robustness](control-records/c11-adversarial-robustness/README.md) | 敵対的入力、学習Dataの推測、Model抽出、実行時異常に備えられるか。 | Modelの採用・更新、公開推論APIの運用、改善Feedbackの取込み。 | [学習ガイド](learning/c11-adversarial-robustness/README.md) |
| [C12 Monitoring, Logging & Anomaly Detection](control-records/c12-monitoring-logging-and-anomaly-detection/README.md) | AI処理・変更を再構成し、異常を検知・調査できるか。 | AIサービスの本番監視・インシデント調査、Model・Dataset変更の監査。 | [学習ガイド](learning/c12-monitoring-logging-and-anomaly-detection/README.md) |

## 個別Control（IDから直接開く）

以下はCatalog登録済みのControl本文だけを載せています。IDが分かっている場合は直接開けます。
各Controlの内容と隣接要件の違いは、
上のFamily READMEからも確認できます。この一覧は[Catalog](catalog.yaml)の`control_ref`を辿る索引です。

### C1

| Section | Control本文 |
|---|---|
| C1.1 | [v1.0-C1.1.1](control-records/c01-training-data-integrity-and-traceability/v1.0-c1.1.1-purpose-bound-training-fields/README.md) · [v1.0-C1.1.2](control-records/c01-training-data-integrity-and-traceability/v1.0-c1.1.2-complete-training-source-inventory/README.md) · [v1.0-C1.1.3](control-records/c01-training-data-integrity-and-traceability/v1.0-c1.1.3-stored-and-transferred-training-data-integrity/README.md) · [v1.0-C1.1.4](control-records/c01-training-data-integrity-and-traceability/v1.0-c1.1.4-training-data-integrity-monitoring/README.md) · [v1.0-C1.1.5](control-records/c01-training-data-integrity-and-traceability/v1.0-c1.1.5-dataset-watermark-attribution/README.md) |
| C1.2 | [v1.0-C1.2.1](control-records/c01-training-data-integrity-and-traceability/v1.0-c1.2.1-annotation-create-modify-approve-authorization/README.md) · [v1.0-C1.2.2](control-records/c01-training-data-integrity-and-traceability/v1.0-c1.2.2-labeling-artifact-cryptographic-integrity/README.md) · [v1.0-C1.2.3](control-records/c01-training-data-integrity-and-traceability/v1.0-c1.2.3-protect-sensitive-label-information-before-artifacts/README.md) |
| C1.3 | [v1.0-C1.3.1](control-records/c01-training-data-integrity-and-traceability/v1.0-c1.3.1-training-pipeline-poisoning-and-corruption-detection/README.md) · [v1.0-C1.3.2](control-records/c01-training-data-integrity-and-traceability/v1.0-c1.3.2-automatic-label-confidence-and-consistency-checks/README.md) · [v1.0-C1.3.3](control-records/c01-training-data-integrity-and-traceability/v1.0-c1.3.3-bias-evaluation-for-security-decisions/README.md) · [v1.0-C1.3.4](control-records/c01-training-data-integrity-and-traceability/v1.0-c1.3.4-remove-disallowed-content-before-training/README.md) · [v1.0-C1.3.5](control-records/c01-training-data-integrity-and-traceability/v1.0-c1.3.5-clean-label-poisoning-defenses/README.md) |

### C2

| Section | Control本文 |
|---|---|
| C2.1 | [v1.0-C2.1.1](control-records/c02-input-validation/v1.0-c2.1.1-normalize-input-before-tokenization-or-embedding/README.md) · [v1.0-C2.1.2](control-records/c02-input-validation/v1.0-c2.1.2-detect-and-mitigate-encoded-input-smuggling/README.md) · [v1.0-C2.1.3](control-records/c02-input-validation/v1.0-c2.1.3-screen-and-block-model-steering-inputs/README.md) · [v1.0-C2.1.4](control-records/c02-input-validation/v1.0-c2.1.4-reject-over-limit-input-without-truncation/README.md) · [v1.0-C2.1.5](control-records/c02-input-validation/v1.0-c2.1.5-allowlist-required-input-characters/README.md) · [v1.0-C2.1.6](control-records/c02-input-validation/v1.0-c2.1.6-preserve-instruction-hierarchy-across-steps/README.md) · [v1.0-C2.1.7](control-records/c02-input-validation/v1.0-c2.1.7-render-reserved-tokens-as-literal-content/README.md) · [v1.0-C2.1.8](control-records/c02-input-validation/v1.0-c2.1.8-detect-many-shot-jailbreak-patterns/README.md) |
| C2.2 | [v1.0-C2.2.1](control-records/c02-input-validation/v1.0-c2.2.1-screen-prompts-before-model-context/README.md) · [v1.0-C2.2.2](control-records/c02-input-validation/v1.0-c2.2.2-evaluate-content-classification-for-unsupported-languages/README.md) · [v1.0-C2.2.3](control-records/c02-input-validation/v1.0-c2.2.3-check-non-text-inputs-for-hidden-attacks/README.md) · [v1.0-C2.2.4](control-records/c02-input-validation/v1.0-c2.2.4-detect-and-block-cross-modal-attacks/README.md) |

### C3

| Section | Control本文 |
|---|---|
| C3.1 | [v1.0-C3.1.1](control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.1.1-deployed-model-artifact-and-origin-inventory/README.md) · [v1.0-C3.1.2](control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.1.2-authorized-signatures-for-all-model-artifacts/README.md) · [v1.0-C3.1.3](control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.1.3-signature-verification-at-admission-and-load/README.md) |
| C3.2 | [v1.0-C3.2.1](control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.2.1-automated-input-safety-output-tests-before-deployment/README.md) · [v1.0-C3.2.2](control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.2.2-same-safety-suite-on-quantized-artifact/README.md) · [v1.0-C3.2.3](control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.2.3-security-reevaluation-before-provider-route-changes/README.md) |
| C3.3 | [v1.0-C3.3.1](control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.3.1-controlled-rollout-with-automated-rollback-triggers/README.md) · [v1.0-C3.3.2](control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.3.2-rollback-restores-complete-model-state/README.md) · [v1.0-C3.3.3](control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.3.3-parallel-model-version-runtime-state-isolation/README.md) |
| C3.4 | [v1.0-C3.4.1](control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.4.1-ai-runtime-component-separation-across-environments/README.md) · [v1.0-C3.4.2](control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.4.2-training-and-fine-tuning-isolated-from-production/README.md) |
| C3.5 | [v1.0-C3.5.1](control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.5.1-versioned-integrity-verified-models-before-rlhf/README.md) · [v1.0-C3.5.2](control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.5.2-automated-reward-hacking-and-overoptimization-detection/README.md) · [v1.0-C3.5.3](control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.5.3-verify-each-fine-tuning-stage-output-before-consumption/README.md) · [v1.0-C3.5.4](control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.5.4-fine-tuning-checkpoints-registered-as-distinct-artifacts/README.md) |

### C4

| Section | Control本文 |
|---|---|
| C4.1 | [v1.0-C4.1.1](control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1.1-isolated-sandbox-for-model-execution/README.md) · [v1.0-C4.1.2](control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1.2-safe-serialization-format-allowlist-at-model-loading/README.md) · [v1.0-C4.1.3](control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1.3-workload-attestation-before-model-loading/README.md) · [v1.0-C4.1.4](control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.1.4-protect-confidential-model-weights-during-runtime/README.md) |
| C4.2 | [v1.0-C4.2.1](control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.2.1-pinned-signed-boot-attested-accelerator-firmware/README.md) · [v1.0-C4.2.2](control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.2.2-tee-hardware-isolation-encryption-and-integrity/README.md) · [v1.0-C4.2.3](control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.2.3-hardware-attestation-before-each-accelerator-workload/README.md) · [v1.0-C4.2.4](control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.2.4-accelerator-memory-partitioning-and-job-sanitization/README.md) · [v1.0-C4.2.5](control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.2.5-approved-accelerator-topologies-and-authenticated-endpoints/README.md) |
| C4.3 | [v1.0-C4.3.1](control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3.1-strong-edge-device-authentication-to-central-infrastructure/README.md) · [v1.0-C4.3.2](control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3.2-signed-packaging-and-on-device-model-verification/README.md) · [v1.0-C4.3.3](control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3.3-inference-process-memory-and-file-isolation/README.md) · [v1.0-C4.3.4](control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3.4-hardware-backed-encryption-for-locally-stored-models/README.md) · [v1.0-C4.3.5](control-records/c04-infrastructure-configuration-and-deployment-security/v1.0-c4.3.5-packaged-model-encryption-and-trusted-runtime-decryption/README.md) |

### C5

| Section | Control本文 |
|---|---|
| C5.1 | [v1.0-C5.1.1](control-records/c05-access-control-and-identity/v1.0-c5.1.1-step-up-authentication/README.md) · [v1.0-C5.1.2](control-records/c05-access-control-and-identity/v1.0-c5.1.2-short-lived-minimal-scoped-signed-agent-tokens/README.md) |
| C5.2 | [v1.0-C5.2.1](control-records/c05-access-control-and-identity/v1.0-c5.2.1-explicit-allow-default-deny-ai-resources/README.md) · [v1.0-C5.2.2](control-records/c05-access-control-and-identity/v1.0-c5.2.2-end-user-authorization-retrieval-assembly/README.md) · [v1.0-C5.2.3](control-records/c05-access-control-and-identity/v1.0-c5.2.3-sensitive-data-retrieval-not-model-storage/README.md) · [v1.0-C5.2.4](control-records/c05-access-control-and-identity/v1.0-c5.2.4-post-inference-authorization-filtering/README.md) · [v1.0-C5.2.5](control-records/c05-access-control-and-identity/v1.0-c5.2.5-agent-authorization-pdp-isolation/README.md) · [v1.0-C5.2.6](control-records/c05-access-control-and-identity/v1.0-c5.2.6-just-in-time-privileged-access/README.md) · [v1.0-C5.2.7](control-records/c05-access-control-and-identity/v1.0-c5.2.7-downstream-classification-label-propagation/README.md) |
| C5.3 | [v1.0-C5.3.1](control-records/c05-access-control-and-identity/v1.0-c5.3.1-shared-model-serving-tenant-isolation/README.md) · [v1.0-C5.3.2](control-records/c05-access-control-and-identity/v1.0-c5.3.2-shared-compute-tenant-isolation/README.md) |

### C6

| Section | Control本文 |
|---|---|
| C6.1 | [v1.0-C6.1.1](control-records/c06-supply-chain-security-for-models/v1.0-c6.1.1-malicious-code-scan-before-model-import/README.md) · [v1.0-C6.1.2](control-records/c06-supply-chain-security-for-models/v1.0-c6.1.2-download-ai-artifacts-only-from-approved-sources/README.md) · [v1.0-C6.1.3](control-records/c06-supply-chain-security-for-models/v1.0-c6.1.3-integrity-verifiability-for-every-third-party-model-artifact/README.md) · [v1.0-C6.1.4](control-records/c06-supply-chain-security-for-models/v1.0-c6.1.4-behavioral-acceptance-before-any-nondevelopment-promotion/README.md) |
| C6.2 | [v1.0-C6.2.1](control-records/c06-supply-chain-security-for-models/v1.0-c6.2.1-versioned-machine-readable-ai-bom-for-every-model/README.md) · [v1.0-C6.2.2](control-records/c06-supply-chain-security-for-models/v1.0-c6.2.2-cryptographically-signed-ai-bom-before-deployment/README.md) · [v1.0-C6.2.3](control-records/c06-supply-chain-security-for-models/v1.0-c6.2.3-fail-build-on-missing-ai-bom-component-metadata/README.md) |

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
| C11.2 | [v1.0-C11.2.1](control-records/c11-adversarial-robustness/v1.0-c11.2.1-no-direct-output-of-model-inferred-sensitive-attributes/README.md) · [v1.0-C11.2.2](control-records/c11-adversarial-robustness/v1.0-c11.2.2-principal-and-global-inference-limits-for-extraction-threat/README.md) · [v1.0-C11.2.3](control-records/c11-adversarial-robustness/v1.0-c11.2.3-calibrate-model-outputs-to-reduce-overconfidence/README.md) · [v1.0-C11.2.4](control-records/c11-adversarial-robustness/v1.0-c11.2.4-differentially-private-optimization-for-sensitive-training/README.md) · [v1.0-C11.2.5](control-records/c11-adversarial-robustness/v1.0-c11.2.5-membership-inference-simulations-at-random-baseline/README.md) |
| C11.3 | [v1.0-C11.3.1](control-records/c11-adversarial-robustness/v1.0-c11.3.1-query-pattern-analysis-feeds-model-extraction-detector/README.md) · [v1.0-C11.3.2](control-records/c11-adversarial-robustness/v1.0-c11.3.2-backend-output-boundary-calibrated-to-extraction-risk/README.md) · [v1.0-C11.3.3](control-records/c11-adversarial-robustness/v1.0-c11.3.3-watermark-or-fingerprint-for-unauthorized-model-copies/README.md) · [v1.0-C11.3.4](control-records/c11-adversarial-robustness/v1.0-c11.3.4-suspected-extraction-detection-triggers-response/README.md) |
| C11.4 | [v1.0-C11.4.1](control-records/c11-adversarial-robustness/v1.0-c11.4.1-anomaly-screening-before-inference-for-untrusted-inputs/README.md) · [v1.0-C11.4.2](control-records/c11-adversarial-robustness/v1.0-c11.4.2-anomaly-flags-trigger-effective-input-gating/README.md) · [v1.0-C11.4.3](control-records/c11-adversarial-robustness/v1.0-c11.4.3-poisoning-detection-and-human-review-for-safety-feedback/README.md) |

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
| 設計レビューや教育に再利用できる横断的な洞察 | [Insights一覧](../docs/insights/README.md) |
| 整備順序と今後の作業 | [Controls計画](plan.md) |
| Control本文の構成とCatalogの形式 | [Controlテンプレート](templates/control.md)・[Catalog Schema](schema/control-catalog.schema.json) |
| 執筆・検証時のルール | [Controls Domain Instructions](AGENTS.md) |

Controlの成熟度は文書の状態であり、製品の適合や学習完了を示しません。
AISVSは検証要件の一次資料です。Control本文はその原文の代替ではなく、Repositoryの解釈です。
AISVS Researchは脅威や検証を考えるための補助資料であり、追加の規範要件とは扱いません。
参照している版・成熟状態は [Source Registry](../sources/registry.yaml) を確認してください。
現行資料の採用版はAISVS v1.0です。上流の最新安定版1.01への差分・影響評価は
[Issue #6](https://github.com/DharmaDoll/ai-security-foundry/issues/6)で追跡しています。
Engineering Patternとの関係は、両者を独立に理解した後に [Mappings](../mappings/README.md) で評価します。

## MITRE ATLASの対応評価

[Content 2026.10への更新案](atlas-mapping-review-2026-10.md)に、C5の既存関係の移行とC6・C8・C9・C11・C12の対応根拠・限界をまとめています。正式な情報はCatalog、上流差分と人のレビュー状況はリンク先の更新レビューを参照してください。
