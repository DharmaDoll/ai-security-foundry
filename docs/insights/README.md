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
| Requirement learning note | 一つのRequirementを具体的に理解する |
| Engineering Pattern | 繰り返す設計問題をどう安全に実装・検証するか |
| Mapping | 独立して理解したArtifact間の関係を評価する |
| Insight | 複数領域へ持ち運べる考え方・見方を残す |

InsightはNormativeな要件、製品適合の証拠、Patternの代替ではない。関連SourceやArtifactを示し、上流の事実と
Repository interpretationを区別する。

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

## Current insights

### 分析・保証評価

| Insight | 中心となる見方 |
|---|---|
| [Web SecurityからAgent Securityへ：ParameterではなくCapability Flowを追う](web-security-to-agent-capability-flow.md) | 非信頼情報がAuthorityへ影響できる全経路を追う |
| [ControlはSystem安全性の合否ではなく、Failureを切り分ける診断軸である](assurance-properties-are-diagnostic-lenses.md) | 個別保証とEnd-to-end Riskを混同しない |
| [Security Artifactは証明できる範囲を越えて信頼しない](security-artifacts-have-bounded-claims.md) | 署名、Schema、Manifest、Policy、Logの保証範囲を分ける |
| [不要なAuthorityを消し、残る全経路を完全仲介する](minimize-and-mediate-authority.md) | Least PrivilegeでReasoning surfaceを減らし、残る経路を迂回不能にする |

### Identity・Privilege・Approval

| Insight | 中心となる見方 |
|---|---|
| [Identity、Authority、Intent、Transaction Integrityを分ける](identity-authority-and-intent-are-different.md) | AIは提案できるが、自分の出力からAuthorityを作れない |
| [PrivilegeはToken FieldではなくEnd-to-end Lifecycleで評価する](privilege-is-a-lifecycle-not-a-token-field.md) | 発行、更新、下流利用、失効後の拒否まで追う |
| [Human ApprovalはButtonではなくSecurity Protocolである](human-approval-is-a-security-protocol.md) | 表示、判断、Binding、一回性、発行Authorityを一体で守る |

### Data・Isolation・Runtime

| Insight | 中心となる見方 |
|---|---|
| [Dataは形を変えてもProtectionを失わない](protected-data-survives-transformation.md) | Derived ArtifactとEgressまでProtectionを追跡する |
| [Tenant IsolationはRead禁止だけでなく観測と干渉を防ぐ](shared-isolation-means-no-observation-or-interference.md) | 何がまだ共有され、その共有から何が可能かを見る |
| [Bounded Autonomyには階層ごとの上限と停止意味論が必要である](bounded-autonomy-requires-hierarchical-controls.md) | Tool、Execution、Swarmの上限とStop／Undoを分ける |

### 教育・資料化

| Insight | 中心となる見方 |
|---|---|
| [具体的なFlowからSecurity Invariantへ抽象化して教える](teach-from-concrete-flow-to-security-invariant.md) | 具体は理解の入口、Invariantは応用の出口 |
