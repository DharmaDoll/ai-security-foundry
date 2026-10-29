# MITRE ATLAS 2026.10：Controlとの対応評価

- 評価日：2026-10-29。評価者：AI agent。人によるSecurity Reviewは未実施。
- 対象：AISVS採用版`1.0`と、ATLAS Content `2026.10`／Format `6.1.0`（rolling）。AISVS 1.01への移行ではない。
- ATLAS固定版：[公式YAML](https://github.com/mitre-atlas/atlas-data/blob/f56c1468731d6428e5bf875263b4643b46d67437/dist/v6/ATLAS-2026.10.yaml)。版・変更分類・旧IDの扱いは[更新レビュー](../sources/updates/2026-10-29-atlas-2026.10-review.md)を参照。

**以下はRepository独自の対応案です。公式なAISVS–ATLAS対応表ではありません。** 正本は[Catalog](catalog.yaml)の`threat_mappings`。各関係の安定した識別には`<versioned_id>/mitre-atlas/<source_version>/<identifier>`の組を使います。全件`proposed`で、`partial`は攻撃経路の一部、`context`は脅威理解・評価の参考を意味します。Controlの成熟度や試験結果とは別です。

既存MappingはC5の3件でした。他Familyは空欄だったため、今回は具体的に比較できたRequirementへ限定して追加しました。記載がないRequirementは、対応なし・対策不要と判定したものではありません。

## C5

| Control | ATLAS Technique | 関係／強さ | 根拠と限界 |
|---|---|---|---|
| [v1.0-C5.2.5](control-records/c05-access-control-and-identity/v1.0-c5.2.5-agent-authorization-pdp-isolation/README.md) | `AML.T0053` AI Agent Tool Invocation | mitigates / partial | Agentから認可判断主体を変更・置換できなくすることで、Agentの権限を代理悪用する経路の一部を制限する。全ツールがPDPを通ることや、委任範囲・Policyの正しさまでは保証しない。 |
| [v1.0-C5.2.5](control-records/c05-access-control-and-identity/v1.0-c5.2.5-agent-authorization-pdp-isolation/README.md) | `AML.T0051` LLM Prompt Injection | context / context | Prompt InjectionはAgentを攻撃者の意図へ誘導する入口の一つ。PDP隔離は認可制御の侵害を制限するが、Injection自体の検知・防止を実装する要件ではない。 |
| [v1.0-C5.3.1](control-records/c05-access-control-and-identity/v1.0-c5.3.1-shared-model-serving-tenant-isolation/README.md) | `AML.T0085.002` Data from AI Services: Conversation Context and Memory | mitigates / partial | 共有Model-servingのPrompt、応答、Cache等のTenant分離は、他Tenantの会話Contextを取得する経路の一部を制限する。認可された同一Tenant内での漏洩、外部Memory API、学習済み重みからの情報取得はこの対応の範囲外。旧AML.T0057との関係は2026.10移行レビューに保存した。 |

## C6

| Control | ATLAS Technique | 関係／強さ | 根拠と限界 |
|---|---|---|---|
| [v1.0-C6.1.2](control-records/c06-supply-chain-security-for-models/v1.0-c6.1.2-download-ai-artifacts-only-from-approved-sources/README.md) | `AML.T0010.003` Supply Chain Compromise: Model Repository | mitigates / partial | 承認したPublisher・Repository・Artifact種別を実際の取得先で照合し、偽の配布元やRedirectからのModel取得を拒否する。承認済みPublisherの侵害、同じ配布元での版差替え、取得後の実行安全性は別の保証。 |
| [v1.0-C6.2.1](control-records/c06-supply-chain-security-for-models/v1.0-c6.2.1-versioned-machine-readable-ai-bom-for-every-model/README.md) | `AML.T0010` Supply Chain Compromise | context / context | Model版とDataset・重み・由来を結ぶBOMは、供給元侵害時の影響調査を助ける。BOMの存在だけでは配布元侵害、Artifact差替え、悪性コードを防止・検知できず、ATLASの広いSupply Chain全体を満たすという対応ではない。 |

## C8

| Control | ATLAS Technique | 関係／強さ | 根拠と限界 |
|---|---|---|---|
| [v1.0-C8.1.3](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.1.3-retrieval-scope-enforcement/README.md) | `AML.T0085.000` Data from AI Services: RAG Databases | mitigates / partial | 信頼する利用者・Tenant・委任範囲から検索Scopeを強制し、RAGからの未認可Data取得を制限する。閲覧可能な文書の別宛先への開示や、検索外の直接DB侵害は含まない。 |
| [v1.0-C8.1.3](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.1.3-retrieval-scope-enforcement/README.md) | `AML.T0085.002` Data from AI Services: Conversation Context and Memory | mitigates / partial | 会話履歴やMemoryを検索対象にする構成では、検索・Cache・Context組立てでScopeを強制し、別利用者の記録の取得を制限する。既に現在のContextへ入った秘密の抽出や、検索を通らない履歴APIは別途確認する。 |
| [v1.0-C8.2.3](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.3-source-validated-trusted-memory-writes/README.md) | `AML.T0080.000` AI Agent Context Poisoning: Memory | mitigates / partial | Agent・Tool出力を直接Trusted Memoryへ書かず、由来とWrite Authorityを独立した昇格Gateで確認する。要約・圧縮・共有Memory経路にも適用するが、正規Sourceの意味的な毒入れや全てのMemory操作を防ぐとは言えない。 |
| [v1.0-C8.2.3](control-records/c08-memory-embeddings-and-vector-database-security/v1.0-c8.2.3-source-validated-trusted-memory-writes/README.md) | `AML.T0143` LLM Prompt Propagation | mitigates / partial | 転送・要約された攻撃指示をAgent・Tool出力からTrusted Memoryへ取り込む区間で、由来確認と昇格Gateを強制する。メール・Repository・別Agentへの伝播全般や、既に保存された複製の回収は対象外。 |

## C9

| Control | ATLAS Technique | 関係／強さ | 根拠と限界 |
|---|---|---|---|
| [v1.0-C9.3.5](control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.5-isolate-untrusted-data-processing-from-tool-capabilities/README.md) | `AML.T0051.001` LLM Prompt Injection: Indirect | mitigates / partial | 非信頼文書やTool応答を扱うComponentから特権Tool能力を隔離し、戻り値を無条件に命令へ昇格させない。間接Injectionから未認可操作への経路を制限するが、回答の偏りや命令を含むDataの伝播自体を完全には防がない。 |
| [v1.0-C9.5.2](control-records/c09-orchestration-and-agentic-security/v1.0-c9.5.2-scope-limited-user-context-through-downstream-calls/README.md) | `AML.T0053` AI Agent Tool Invocation | mitigates / partial | 利用者の認可Contextと限定Scopeを各下流で強制し、仲介の広いService権限で利用者の範囲を越える代理操作を制限する。利用者自身に許可された操作の悪用や目的の逸脱はToken検証だけでは判定できない。 |

## C11

| Control | ATLAS Technique | 関係／強さ | 根拠と限界 |
|---|---|---|---|
| [v1.0-C11.2.4](control-records/c11-adversarial-robustness/v1.0-c11.2.4-differentially-private-optimization-for-sensitive-training/README.md) | `AML.T0137.000` Training Data Information from AI Models: Infer Membership | mitigates / partial | 保護単位・隣接Data・Privacy予算を定めたDP最適化により、一記録の学習参加が出力へ与える影響を制限する。保証は会計・組成・予算の前提に依存し、集団の性質の推定やあらゆる情報開示の禁止を意味しない。 |
| [v1.0-C11.2.5](control-records/c11-adversarial-robustness/v1.0-c11.2.5-membership-inference-simulations-at-random-baseline/README.md) | `AML.T0137.000` Training Data Information from AI Models: Infer Membership | context / context | Membership推定のSimulationで対象Modelの漏洩可能性を評価する関係。攻撃者の観測権限、独立評価Data、偶然の基準を固定するが、試験を行うこと自体は本番攻撃の阻止・検知ではない。 |
| [v1.0-C11.3.2](control-records/c11-adversarial-robustness/v1.0-c11.3.2-backend-output-boundary-calibrated-to-extraction-risk/README.md) | `AML.T0005.001` Replicate AI Model Behavior: Replicate Behavior from Model Outputs | mitigates / partial | Backendで外部公開する出力Fieldと精度を選び、能力模倣の教師Dataとしての有用性を制限する。通常回答も模倣へ使えるため、モデル複製の完全防止や内部Parameterの復元防止を一括で主張しない。 |
| [v1.0-C11.4.3](control-records/c11-adversarial-robustness/v1.0-c11.4.3-poisoning-detection-and-human-review-for-safety-feedback/README.md) | `AML.T0145` Poison AI Agent Learning Environment | mitigates / partial | 安全性Feedbackが改善・追加学習へ昇格する経路で毒入れ検知と人の確認Gateを設ける。環境操作から生成された経験を学習へ取り込む攻撃の一部に対応し、一般の強化学習環境・報酬設計・全Memory更新を覆わない。 |

## C12

| Control | ATLAS Technique | 関係／強さ | 根拠と限界 |
|---|---|---|---|
| [v1.0-C12.2.3](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.2.3-detect-ai-specific-attacks-with-custom-rules/README.md) | `AML.T0085.003` Data from AI Services: System Instructions | detects / partial | 内部指示の引き出しを対象システムに合わせたルールで検知する。観測した要求や挙動に限る対応であり、設定Fileからの直接窃取や未知の引き出し方の検知は保証しない。 |
| [v1.0-C12.2.3](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.2.3-detect-ai-specific-attacks-with-custom-rules/README.md) | `AML.T0140` Centralized AI Service Request Routing | context / context | 要求を複数Account・経路へ分散する回避行動は、協調した脱獄を単一Sessionの件数だけで判断できない根拠となる。C12.2.3はモデル蒸留Campaign全体の検知要件ではなく、全Provider横断の相関も保証しない。 |
| [v1.0-C12.5.3](control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.5.3-immutable-audit-records-for-model-changes/README.md) | `AML.T0138` Indicator Removal | mitigates / partial | Model変更者・Registry管理者による過去の変更記録の削除・上書きを防ぎ、侵害後の証拠隠しの一経路を制限する。記録生成前の隠蔽や会話・Tool実行を含む全監査基盤の完全性までは覆わない。 |

## Mitigationの読み方と、今回対応を広げない範囲

- **C6.2と`AML.M0023`**：新版BOMにはAgent設定、接続Tool・Data Source等も含まれる。一方、C6.2.1のModel Artifact向けBOM要件を、それだけで全Agent運用資産の棚卸し義務へ広げない。BOMは供給元の安全証明ではない。
- **C11.2・C11.3と`AML.M0040`／`AML.M0041`**：応答の情報量の調整とPrivacy保護は別の介入点。集団の性質の推定、在籍推定、記憶内容の回収、能力模倣を一つの試験で覆わない。応答劣化は有用性・誤検知・安全な応答への影響を別途評価する。
- **C12と`AML.M0024`／`AML.M0042`**：実際の実行記録とモデルの説明を分け、情報収集を具体的な検知・設計の変更へ結び付ける補助資料。全Threat Intelligence運用をC12の個別要件が要求するとは扱わない。
- **C9と`AML.M0043`**：Agentが作った外部資源の期限・所有者・回収の問題。停止やToken失効だけで既存の公開Artifact・外部アカウントが消えるとは限らない。今回の個別Controlへ全面的な対応を付けず、[Engineeringの残存課題](../engineering/docs/mitre-atlas-impact-2026-10.md)に残す。

Mitigationは防御案、Techniqueは攻撃者の行動であり、上記Mitigationを`threat_mappings`の攻撃IDとして混在させません。上流の`mitigates`関係も本Repositoryの対応評価へ自動継承しません。

## 人のレビューで確かめること

1. C5.3.1の旧`AML.T0057`からの移行で、学習データと会話状態を混同していないか。旧関係と固定版への参照は更新レビューに保存した。
2. 各`partial`の境界に、当該Controlが実際に要求する強制・検知箇所があるか。特にTokenの正しさと操作目的の妥当性は区別する。
3. 試験を行う要件、BOM、観測を助ける情報に、攻撃阻止の強さを付けていないか。
4. 未掲載のRequirementの追加評価が必要か。今回の表の件数を網羅率・適合率として使わない。
