# AISVS C9 学習ガイド

> **Legacy learning layout:** C9は旧方針のRequirement単位で学習を完了している。
> 既存ノートは対話と洞察を保持するため移動しない。将来再編する場合は、Source versionと
> Linkを保った明示的MigrationとしてC9.1〜C9.6のSection単位へ統合する。

C9ではAgentが許可された、意図された、制限された行動を実行するための保証を学ぶ。
この文書は旧Requirement単位で完了した学習履歴を案内する。今後の新規学習には
[共通学習方針](../README.md)のSection単位方式を使う。
全体の保証範囲・ID・Levelは[章の分析](../../c09-landscape.md)と
[Control一覧](../../../README.md#c9-control-records)を参照する。
[C9 Family overview](../../../control-records/c09-orchestration-and-agentic-security/README.md)では、
Category・Section・Requirementを「問うこと」と
「できてはいけないこと」で俯瞰できる。

## 現在位置

C9の全34要件について、講義・対話とRequirement別の学習ノートを一巡して保存した。
現在学習中の要件はない。学習結果の横断的な洞察への整理は、Control成熟度とは別の作業として扱う。
学習進捗はControl成熟度・製品適合とは独立している。

## 一巡のチェックリスト

- [x] [C9.1.1：ツールごとの資源上限と実行期限](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.1-per-tool-resource-quotas-and-timeouts/learning.md)
- [x] [C9.1.2：実行全体の累積予算](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.2-per-execution-cumulative-budgets/learning.md)
- [x] [C9.1.3：Agent群全体の停止](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.3-swarm-wide-agent-halt/learning.md)
- [x] [C9.2.1：高影響操作への人の承認](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.1-human-approval-before-high-impact-actions/learning.md)
- [x] [C9.2.2：承認対象の完全・正確な表示](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.2-complete-canonical-approval-display/learning.md)
- [x] [C9.2.3：高影響操作の可逆性の分類](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.3-trusted-action-reversibility-classification/learning.md)
- [x] [C9.2.4：可逆性分類に基づく実行制限](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.4-enforce-reversibility-based-action-policy/learning.md)
- [x] [C9.2.5：Agentの自己変更能力の制限](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.5-bounded-agent-self-modification/learning.md)
- [x] [C9.2.6：高Risk操作へのAI補助レビューの追加](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.6-additive-ai-review-before-high-risk-actions/learning.md)
- [x] [C9.2.7：AI補助レビューの操作・迂回への保護](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.7-protect-ai-action-review-from-manipulation/learning.md)
- [x] [C9.2.8：操作に結び付いた一回限りの承認](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.8-cryptographically-bound-single-use-approvals/learning.md)
- [x] [C9.2.9：承認発行鍵・資格情報の隔離](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.9-approval-issuing-key-and-credential-isolation/learning.md)
- [x] [C9.2.10：行動連鎖の最大影響を承認へ反映](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.10-chain-wide-highest-impact-approval/learning.md)
- [x] [C9.3.1：Tool実行の最小権限・隔離](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.1-least-privilege-tool-execution-isolation/learning.md)
- [x] [C9.3.2：Tool出力のSchema検証](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.2-tool-output-schema-validation/learning.md)
- [x] [C9.3.3：Tool ManifestへのSecurity要件の宣言](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.3-explicit-tool-manifest-security-requirements/learning.md)
- [x] [C9.3.4：Manifest宣言のRuntime強制](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.4-runtime-enforcement-of-tool-manifests/learning.md)
- [x] [C9.3.5：非信頼Data処理とTool能力の隔離](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.5-isolate-untrusted-data-processing-from-tool-capabilities/learning.md)
- [x] [C9.3.6：非信頼Tool出力とAgent操作の構造的分離](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.6-architectural-separation-of-untrusted-tool-outputs/learning.md)
- [x] [C9.3.7：Modelが示した外部Resourceの利用前確認](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.7-verify-model-named-external-resources/learning.md)
- [x] [C9.3.8：Policy違反時のTool自動封じ込め](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.8-automatic-tool-containment-on-policy-violation/learning.md)
- [x] [C9.4.1：Agent Instanceの一意な暗号的Identity](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.4.1-unique-cryptographic-agent-instance-identity/learning.md)
- [x] [C9.4.2：操作内容と実行Chainの暗号的結合](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.4.2-cryptographic-action-chain-attribution/learning.md)
- [x] [C9.4.3：AgentのIdentity資格情報の定期更新](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.4.3-scheduled-agent-credential-rotation/learning.md)
- [x] [C9.4.4：保存したAgent状態の完全性保護](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.4.4-integrity-protection-for-persisted-agent-state/learning.md)
- [x] [C9.5.1：Toolと引数の細粒度認可](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.1-fine-grained-tool-and-parameter-authorization/learning.md)
- [x] [C9.5.2：利用者の委任範囲を下流まで維持](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.2-scope-limited-user-context-through-downstream-calls/learning.md)
- [x] [C9.5.3：アクセス制御をモデル外で強制](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.3-application-enforced-authorization-outside-model-decisions/learning.md)
- [x] [C9.5.4：Runtimeの秘密をモデルへ露出させない](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.4-keep-runtime-secrets-out-of-model-context/learning.md)
- [x] [C9.5.5：Agent間の明示的な委任Policy](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.5-explicit-inter-agent-delegation-policy/learning.md)
- [x] [C9.5.6：現在のPolicyで各特権操作を再評価](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.6-current-authorization-for-each-privileged-action/learning.md)
- [x] [C9.6.1：推論と出力の手動停止](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.6.1-manual-stop-of-inference-and-outputs/learning.md)
- [x] [C9.6.2：承認期限切れの操作をブロック](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.6.2-deny-actions-after-approval-timeout/learning.md)
- [x] [C9.6.3：Agentから隔離した停止経路](../../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.6.3-out-of-band-shutdown-control-isolation/learning.md)

## Sources

採用済みAISVS v1.0、固定Revision `78775233666a2022dcfb82037e5e029116955c00`。

- [C9要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
- [C9 Research章概要](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-Orchestration-and-Agents.md)
- [C9.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-01-Execution-Budgets.md)
- [C9.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-02-High-Impact-Action-Approval.md)
