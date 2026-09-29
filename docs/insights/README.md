# Cross-cutting Security Insights

このDirectoryは、Controls、Engineering Pattern、脅威モデリング、設計レビュー、教育の複数文脈で
再利用できるSecurity上の洞察を保存する。

Frameworkの要約集ではない。Requirementを具体例へ当てはめ、既存Securityの知識と比較し、対話や設計検討から
得られたRepository独自のMental Modelを残す場所である。後からSlide、講義、Architecture Review、Pattern候補の
検討材料として使える粒度を目指す。

## 他のArtifactとの違い

| Artifact | 主な役割 |
|---|---|
| Control | 何を保証・検証すべきか |
| Learning note | 一つのSectionまたは旧方式のRequirementを具体的に理解する |
| Engineering Pattern | 繰り返す設計問題をどう安全に実装・検証するか |
| Mapping | 独立して理解したArtifact間の関係を評価する |
| Insight | 複数領域へ持ち運べる考え方・見方を残す |

InsightはNormativeな要件、製品適合の証拠、Patternの代替ではない。関連SourceやArtifactを示し、上流の事実と
Repository interpretationを区別する。

## 学習上の起点から探す

- [C2 学習ガイド](../../controls/learning/c02-input-validation/README.md)：入力の変換後に実際に利用される内容を検査する。
- [C5 学習ガイド](../../controls/learning/c05-access-control-and-identity/README.md)：Identity、権限、Data Protection、Tenant分離から得たInsightを一覧化する。
- [C7 学習ガイド](../../controls/learning/c07-model-behavior-output-control-and-safety-assurance/README.md)：出力の検証と出典・調査可能性を考える。
- [C8 学習ガイド](../../controls/learning/c08-memory-embeddings-and-vector-database-security/README.md)：Trusted Memoryへの昇格と利用停止・削除を分ける。
- [C9 学習ガイド](../../controls/learning/c09-orchestration-and-agentic-security/README.md)：Agentの行動、承認、Tool、停止から得たInsightを一覧化する。
- [C10 学習ガイド](../../controls/learning/c10-model-context-protocol-security/README.md)：Tool Content、Session、認証済み経路の保証範囲を見分ける。
- [C12 学習ガイド](../../controls/learning/c12-monitoring-logging-and-anomaly-detection/README.md)：調査できるEvidenceとPrivacyの両立を考える。

各Insight本文の「起点となった学習記録」から個別Controlへ辿れる。これらは発見・理解の経路であり、
ControlやEngineering Patternとの正式なMappingではない。Pattern側に適切な成果物ができたら、
別途関係を評価し、必要な入口から同じInsightの正本へリンクする。InsightをFamilyごとに複製・移動しない。
現時点ではEngineering Pattern本文への関係は未評価であり、この索引からPatternの存在や対応を推定しない。

## 文書に含めるもの

一つのInsightは、必要な範囲で次を含める。

1. 中心となる洞察。
2. 既存の考え方との連続性と、何が新しく複雑になったか。
3. 再利用可能なMental Modelや短い図。
4. 具体例。
5. 設計レビュー、脅威モデリング、Negative Testへの応用。
6. 誤用しやすい点と限界。
7. 関連するControl、学習ノート、Pattern、Source。
8. Slide等へ転用できる短いまとめ。

Rawな会話記録や単一Requirementの言い換えは置かない。同じ洞察を複数Fileへ複製せず、正本へLinkする。

## Insight関係索引

この表は「何から着想したか、どこへ辿れるか」を示す入口であり、
[正式なMapping評価](../../mappings/README.md)ではない。
「起点（Control／学習）」は代表例で、各Insight本文の「起点となった学習記録」に関連記録を記す。
AISVSは採用済みの固定Revisionにおける学習上の文脈であり、Insight自体をAISVSの要求と主張しない。
`—`は対応するEngineering Pattern本文との関係が未評価であることを示す。
他のFrameworkやGuidelineは、一次資料を読んで技術的な関係を説明できるまでは追加しない。
将来Patternや外部Guidelineへの関係を追加するときは、相手の実体・版／状態と、Insight本文での
関係の根拠を確認する。引用や学習の起点だけで適合・実装・Risk低減を主張しない。

| Insight | 何に使うか | 起点（Control／学習） | Pattern | Framework／Guideline文脈 |
|---|---|---|---|---|
| [AgentのCapability Flow](web-security-to-agent-capability-flow.md) | 非信頼情報が権限へ影響する経路を追う | [C9.3.4](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.4-runtime-enforcement-of-tool-manifests/README.md)、[C9.3.5](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.5-isolate-untrusted-data-processing-from-tool-capabilities/README.md) | — | [AISVS v1.0 C9][aisvs-c9] |
| [保証を診断軸として使う](assurance-properties-are-diagnostic-lenses.md) | 個別保証とSystem全体の安全性を分ける | [C5.2.5](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.5-agent-authorization-pdp-isolation/README.md)、[C9.2.7](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.7-protect-ai-action-review-from-manipulation/README.md) | — | [AISVS C5][aisvs-c5]・[C9][aisvs-c9] |
| [Security Artifactの保証範囲](security-artifacts-have-bounded-claims.md) | 署名・Schema・Manifest等の証明範囲を越えない | [C5.2.4](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.4-post-inference-authorization-filtering/README.md)、[C9.3.2](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.2-tool-output-schema-validation/README.md) | — | [AISVS C5][aisvs-c5]・[C9][aisvs-c9] |
| [実際に利用されるPayloadを検査する](validation-must-cover-effective-payload.md) | 変換・組立て・公開の前後で検査対象のずれを見つける | [C2.1](../../controls/learning/c02-input-validation/v1.0-c2.1-prompt-injection-defenses.md)、[C7.3](../../controls/learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.3-output-safety.md)、[C10.4](../../controls/learning/c10-model-context-protocol-security/v1.0-c10.4-schema-message-and-input-validation.md) | — | [AISVS C2][aisvs-c2]・[C7][aisvs-c7]・[C10][aisvs-c10] |
| [信頼は昇格時に判断する](trust-is-granted-at-promotion.md) | SourceやContainerの信頼をContentへ自動継承しない | [C8.2](../../controls/learning/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2-embedding-sanitization-validation.md)、[C10.4](../../controls/learning/c10-model-context-protocol-security/v1.0-c10.4-schema-message-and-input-validation.md) | — | [AISVS C8][aisvs-c8]・[C10][aisvs-c10] |
| [利用停止・消去・再出現防止](retirement-is-more-than-deletion.md) | Stateの終了を全利用経路と復活経路で検証する | [C8.3](../../controls/learning/c08-memory-embeddings-and-vector-database-security/v1.0-c8.3-memory-expiry-revocation.md)、[C10.2](../../controls/learning/c10-model-context-protocol-security/v1.0-c10.2-authentication-and-authorization.md) | — | [AISVS C8][aisvs-c8]・[C10][aisvs-c10] |
| [再構成でき、保護されたSecurity Evidence](security-evidence-must-be-reconstructable-and-constrained.md) | 調査可能なEvent連鎖とTelemetryの機密性を両立する | [C7.4](../../controls/learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.4-source-attribution-and-citation-integrity.md)、[C12.1](../../controls/learning/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.1-request-response-logging.md) | — | [AISVS C7][aisvs-c7]・[C12][aisvs-c12] |
| [Authorityの最小化と完全仲介](minimize-and-mediate-authority.md) | 不要な能力を消し、残る経路を迂回不能にする | [C5.2.1](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.1-explicit-allow-default-deny-ai-resources/README.md)、[C9.3.4](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.4-runtime-enforcement-of-tool-manifests/README.md) | — | [AISVS C5][aisvs-c5]・[C9][aisvs-c9] |
| [Identity・Authority・Intentの分離](identity-authority-and-intent-are-different.md) | 認証と操作の意図・承認を混同しない | [C5.1.1](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.1.1-step-up-authentication/README.md)、[C9.2.8](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.8-cryptographically-bound-single-use-approvals/README.md) | — | [AISVS C5][aisvs-c5]・[C9][aisvs-c9] |
| [PrivilegeのLifecycle](privilege-is-a-lifecycle-not-a-token-field.md) | 発行から失効後の拒否まで追う | [C5.1.2](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.1.2-short-lived-minimal-scoped-signed-agent-tokens/README.md)、[C5.2.6](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.6-just-in-time-privileged-access/README.md) | — | [AISVS v1.0 C5][aisvs-c5] |
| [Human ApprovalをSecurity Protocolとして扱う](human-approval-is-a-security-protocol.md) | 表示、Binding、一回性、発行Authorityを分けて守る | [C9.2.1](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.1-human-approval-before-high-impact-actions/README.md)、[C9.2.8](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.2.8-cryptographically-bound-single-use-approvals/README.md) | — | [AISVS v1.0 C9][aisvs-c9] |
| [変換後もData Protectionを保つ](protected-data-survives-transformation.md) | Derived ArtifactとEgressまで保護を追う | [C5.2.2](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.2-end-user-authorization-retrieval-assembly/README.md)、[C5.2.7](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.7-downstream-classification-label-propagation/README.md) | — | [AISVS v1.0 C5][aisvs-c5] |
| [Tenant間の観測と干渉](shared-isolation-means-no-observation-or-interference.md) | 共有状態からの情報漏えいと干渉を点検する | [C5.3.1](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.3.1-shared-model-serving-tenant-isolation/README.md)、[C5.3.2](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.3.2-shared-compute-tenant-isolation/README.md) | — | [AISVS v1.0 C5][aisvs-c5] |
| [階層ごとの上限と停止](bounded-autonomy-requires-hierarchical-controls.md) | Tool・Execution・Swarmの上限と停止を分ける | [C9.1.1](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.1-per-tool-resource-quotas-and-timeouts/README.md)、[C9.1.2](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.1.2-per-execution-cumulative-budgets/README.md) | — | [AISVS v1.0 C9][aisvs-c9] |
| [具体FlowからSecurity Invariantへ教える](teach-from-concrete-flow-to-security-invariant.md) | 具体で理解し、Invariantで応用する | [C5.1.1](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.1.1-step-up-authentication/README.md)、[C5.2.2](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.2-end-user-authorization-retrieval-assembly/README.md) | — | [AISVS v1.0 C5][aisvs-c5]（学習の起点） |

[aisvs-c2]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md
[aisvs-c5]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md
[aisvs-c7]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md
[aisvs-c8]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md
[aisvs-c9]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[aisvs-c10]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md
[aisvs-c12]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md
