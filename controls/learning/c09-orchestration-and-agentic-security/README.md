# AISVS C9 学習ガイド

> **Legacy learning layout:** C9は旧方針のRequirement単位で学習を完了している。
> 既存ノートは対話と洞察を保持するため移動しない。将来再編する場合は、Source versionと
> Linkを保った明示的MigrationとしてC9.1〜C9.6のSection単位へ統合する。

C9ではAgentが許可された、意図された、制限された行動を実行するための保証を学ぶ。
この文書は旧Requirement単位で完了した学習履歴を案内する。今後の新規学習には
[共通学習方針](../README.md)のSection単位方式を使う。
全体の保証範囲・ID・Levelは[章の分析](../../control-records/c09-orchestration-and-agentic-security/README.md)と
[Control一覧](../../README.md#c9)を参照する。
[C9 Family overview](../../control-records/c09-orchestration-and-agentic-security/README.md)では、
Category・Section・Requirementを「問うこと」と
「できてはいけないこと」で俯瞰できる。

## 現在位置

C9の全34要件について、講義・対話とRequirement別の学習ノートを一巡して保存した。
現在学習中の要件はない。学習結果の横断的な洞察への整理は、Control成熟度とは別の作業として扱う。
学習進捗はControl成熟度・製品適合とは独立している。

## 一巡のチェックリスト

- [x] [C9.1.1：ツールごとの資源上限と実行期限](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.1-per-tool-resource-quotas-and-timeouts/learning.md)
- [x] [C9.1.2：実行全体の累積予算](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.2-per-execution-cumulative-budgets/learning.md)
- [x] [C9.1.3：Agent群全体の停止](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.3-swarm-wide-agent-halt/learning.md)
- [x] [C9.2.1：高影響操作への人の承認](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.1-human-approval-before-high-impact-actions/learning.md)
- [x] [C9.2.2：承認対象の完全・正確な表示](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.2-complete-canonical-approval-display/learning.md)
- [x] [C9.2.3：高影響操作の可逆性の分類](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.3-trusted-action-reversibility-classification/learning.md)
- [x] [C9.2.4：可逆性分類に基づく実行制限](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.4-enforce-reversibility-based-action-policy/learning.md)
- [x] [C9.2.5：Agentの自己変更能力の制限](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.5-bounded-agent-self-modification/learning.md)
- [x] [C9.2.6：高Risk操作へのAI補助レビューの追加](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.6-additive-ai-review-before-high-risk-actions/learning.md)
- [x] [C9.2.7：AI補助レビューの操作・迂回への保護](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.7-protect-ai-action-review-from-manipulation/learning.md)
- [x] [C9.2.8：操作に結び付いた一回限りの承認](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.8-cryptographically-bound-single-use-approvals/learning.md)
- [x] [C9.2.9：承認発行鍵・資格情報の隔離](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.9-approval-issuing-key-and-credential-isolation/learning.md)
- [x] [C9.2.10：行動連鎖の最大影響を承認へ反映](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.10-chain-wide-highest-impact-approval/learning.md)
- [x] [C9.3.1：Tool実行の最小権限・隔離](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.1-least-privilege-tool-execution-isolation/learning.md)
- [x] [C9.3.2：Tool出力のSchema検証](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.2-tool-output-schema-validation/learning.md)
- [x] [C9.3.3：Tool ManifestへのSecurity要件の宣言](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.3-explicit-tool-manifest-security-requirements/learning.md)
- [x] [C9.3.4：Manifest宣言のRuntime強制](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.4-runtime-enforcement-of-tool-manifests/learning.md)
- [x] [C9.3.5：非信頼Data処理とTool能力の隔離](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.5-isolate-untrusted-data-processing-from-tool-capabilities/learning.md)
- [x] [C9.3.6：非信頼Tool出力とAgent操作の構造的分離](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.6-architectural-separation-of-untrusted-tool-outputs/learning.md)
- [x] [C9.3.7：Modelが示した外部Resourceの利用前確認](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.7-verify-model-named-external-resources/learning.md)
- [x] [C9.3.8：Policy違反時のTool自動封じ込め](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.8-automatic-tool-containment-on-policy-violation/learning.md)
- [x] [C9.4.1：Agent Instanceの一意な暗号的Identity](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.4.1-unique-cryptographic-agent-instance-identity/learning.md)
- [x] [C9.4.2：操作内容と実行Chainの暗号的結合](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.4.2-cryptographic-action-chain-attribution/learning.md)
- [x] [C9.4.3：AgentのIdentity資格情報の定期更新](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.4.3-scheduled-agent-credential-rotation/learning.md)
- [x] [C9.4.4：保存したAgent状態の完全性保護](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.4.4-integrity-protection-for-persisted-agent-state/learning.md)
- [x] [C9.5.1：Toolと引数の細粒度認可](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.1-fine-grained-tool-and-parameter-authorization/learning.md)
- [x] [C9.5.2：利用者の委任範囲を下流まで維持](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.2-scope-limited-user-context-through-downstream-calls/learning.md)
- [x] [C9.5.3：アクセス制御をモデル外で強制](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.3-application-enforced-authorization-outside-model-decisions/learning.md)
- [x] [C9.5.4：Runtimeの秘密をモデルへ露出させない](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.4-keep-runtime-secrets-out-of-model-context/learning.md)
- [x] [C9.5.5：Agent間の明示的な委任Policy](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.5-explicit-inter-agent-delegation-policy/learning.md)
- [x] [C9.5.6：現在のPolicyで各特権操作を再評価](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.6-current-authorization-for-each-privileged-action/learning.md)
- [x] [C9.6.1：推論と出力の手動停止](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.6.1-manual-stop-of-inference-and-outputs/learning.md)
- [x] [C9.6.2：承認期限切れの操作をブロック](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.6.2-deny-actions-after-approval-timeout/learning.md)
- [x] [C9.6.3：Agentから隔離した停止経路](../../control-records/c09-orchestration-and-agentic-security/v1.0-c9.6.3-out-of-band-shutdown-control-isolation/learning.md)

## このFamilyの学習から生まれた横断的Insight

Insightの正本は[`docs/insights/`](../../../docs/insights/README.md)に置く。以下のIDは議論の起点であり、
Insightが当該Controlだけに属する、または正式なMappingが成立したという意味ではない。

| Insight | 主な学習上の起点 |
|---|---|
| [Web SecurityからAgent Capability Flowへ](../../../docs/insights/web-security-to-agent-capability-flow.md) | C9.3.4、C9.3.5：非信頼情報がAgentの権限行使へ影響する経路を、Toolや状態をまたいで追う。 |
| [階層ごとの上限と停止](../../../docs/insights/bounded-autonomy-requires-hierarchical-controls.md) | C9.1.1〜C9.1.3：Tool・一実行・Agent群の上限と、停止後も残る副作用を区別する。 |
| [Human ApprovalはSecurity Protocol](../../../docs/insights/human-approval-is-a-security-protocol.md) | C9.2.1、C9.2.2、C9.2.6〜C9.2.10：承認の表示・主体・操作内容・実行を結び、承認の迂回や再利用を確認する。 |
| [保証は診断軸](../../../docs/insights/assurance-properties-are-diagnostic-lenses.md) | C9.2.7：個別保証の合否と製品全体の危険性を分け、修正すべき境界を見つける。 |
| [Identity・Authority・Intentの分離](../../../docs/insights/identity-authority-and-intent-are-different.md) | C9.2.1、C9.2.8：本人性、権限、今回の意図、承認した操作との一致を分けて確認する。 |
| [Authorityの最小化と完全仲介](../../../docs/insights/minimize-and-mediate-authority.md) | C9.2.5、C9.3.1、C9.3.4：不要な能力を取り除き、残した操作経路で認可を迂回できないか確認する。 |
| [Security Artifactの保証範囲](../../../docs/insights/security-artifacts-have-bounded-claims.md) | C9.3.2〜C9.3.4：署名・Schema・Manifest等が示せる保証を、内容や判断の安全性へ広げない。 |

## 境界を跨ぐ行動を組み合わせて読む

[7接点の図と技術改訂メモ](../../../sources/user-provided/2026-10-27-agentic-seven-trust-boundaries.md)で
文書・Tool応答・Memory・別Agentからの情報が操作へ戻る経路を確認し、
[Capability FlowのInsight](../../../docs/insights/web-security-to-agent-capability-flow.md)で実Systemの主体と権限を重ねる。
この補助モデルはAISVSの追加要件やOWASP公式の7分類ではない。既存の学習履歴・完了状態を変更するものでもない。

「正規の検索結果に含まれた指示が、外部送信要求へ変わる」例を、次の順で読む。

1. **Tool出力の取扱い（C9.3.2・C9.3.5・C9.3.6）**：形式検証と、出力を次の操作へ利用できる範囲の制限を分ける。
2. **実行認可（C9.5.1・C9.5.3・C9.5.6）**：モデルの提案を、現在の本人・対象・引数のPolicyで確認する。
3. **委任（C9.5.2・C9.5.5）**：別Agentや下流へ渡しても、利用者の委任範囲を広げない。
4. **高影響操作の承認（C9.2.2・C9.2.8・C9.2.10）**：表示した内容・承認対象・実行内容と連鎖の影響を結ぶ。

これは読む順序であり、実装で認可や承認を後回しにする指示ではない。各検証は必要な開示・副作用より前に行う。
Memoryの書込み・利用・失効は[信頼昇格Insight](../../../docs/insights/trust-is-granted-at-promotion.md)からC8等へ進む。

レビューで使う依頼例：

> 対象Releaseと検証環境を固定して、検索Toolの応答に不正宛先への送信指示を入れた場合の処理を説明してください。
> どのComponentが、どのPolicyを根拠に止めるか、正常な送信と拒否の記録を示してください。

その証拠から、出力の扱いと操作認可が別の強制点で維持されたかを確認する。
「モデルが拒否する」という回答だけなら、不正な操作候補を実行側へ直接渡しても拒否され、下流で送信されない証拠を求める。
具体的な宛先・本文・委任の証拠依頼と保証範囲は[Family概要](../../control-records/c09-orchestration-and-agentic-security/README.md#境界を跨ぐ攻撃経路から読む)にまとめる。
この例は製品試験未実施であり、隣接要件の保証を一つのRequirementの合否へ混ぜない。

## Sources

採用済みAISVS v1.0、固定Revision `78775233666a2022dcfb82037e5e029116955c00`。

- [C9要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
- [C9 Research章概要](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-Orchestration-and-Agents.md)
- [C9.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-01-Execution-Budgets.md)
- [C9.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-02-High-Impact-Action-Approval.md)
