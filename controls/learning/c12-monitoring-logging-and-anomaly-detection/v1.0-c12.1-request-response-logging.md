---
title: "AISVS C12.1 Request & Response Logging 学習ノート"
document_kind: "section-learning-note"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
section_id: "C12.1"
requirements:
  - "v1.0-C12.1.1"
  - "v1.0-C12.1.2"
  - "v1.0-C12.1.3"
  - "v1.0-C12.1.4"
last_updated: "2026-09-26"
---

# C12.1 Request & Response Logging

## 1. 文書の役割とSource separation

本書はAISVS v1.0 C12.1の全4 Requirementを、RAGを使うAgentの一連の処理として学ぶ講義と対話の再構成である。製品適合の証拠やControl本文の代替ではない。

- **Normative:** 固定Revisionの下表のRequirement原文とVerification Level。
- **AISVS Research:** AI特有のTelemetry、Policy判断、推論Event、RAG検索の追跡と、過剰なContent記録の懸念を補足する。記載製品・数値・事件は適合条件として採用しない。
- **Repository interpretation:** 同一処理をSessionから検索、推論、Policy判断まで辿れるEvent設計と、Logへの機密情報集積を制限する設計を提案する。
- **Derived insight:** 学習者は、RAG EventがSessionへつながらない調査上の欠落と、Query記録によるPrivacy・監査・運用費用のトレードオフを指摘した。

## 2. Normative Requirements

| ID | Level | AISVS English | 日本語訳 |
|---|---:|---|---|
| `v1.0-C12.1.1` | 1 | Verify that AI interactions are logged with session context and AI-specific telemetry. | AIとのやり取りをSession ContextとAI固有のTelemetryとともに記録することを確認する。 |
| `v1.0-C12.1.2` | 2 | Verify that safety filtering and policy decisions are logged with sufficient detail to support audit, debugging, and forensic analysis of content moderation systems. | Safety FilterとPolicy判断を、監査・不具合調査・事後調査に十分な詳細で記録することを確認する。 |
| `v1.0-C12.1.3` | 2 | Verify that log entries for AI inference events follow a structured, interoperable schema that includes at least the model identifier, token usage (input and output), provider name, and operation type. | AI推論EventのLogが、少なくともModel ID、入力・出力Token数、Provider名、Operation Typeを含む構造化・相互運用可能なSchemaに従うことを確認する。 |
| `v1.0-C12.1.4` | 2 | Verify that RAG pipeline retrieval events are logged, including the query, documents retrieved, and knowledge source. | RAGの検索Eventに、Query、取得した文書、Knowledge Sourceが記録されることを確認する。 |

正本は[固定RevisionのC12要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md)である。

## 3. C12における位置づけ

C12.1は「後から何が起きたかを再構成できる材料」を扱う。C12.2は攻撃や異常の検知、C12.3はModel・Data・Performanceの変化、C12.4はAgentの自発的な重要行動、C12.5はTraining DataとModel Lifecycleの変更履歴を扱う。

C12.1の四つの直接の問いは、次のとおりである。

```text
AI InteractionはどのSessionの処理か                       C12.1.1
どのSafety Filter／Policyが何を判断したか                C12.1.2
どのModel／Providerで何Tokenの何Operationを行ったか       C12.1.3
RAGは何をQueryし、どの文書をどのSourceから取得したか        C12.1.4
```

## 4. Concrete Scenario

AliceがAgentへ人事規程の要約を依頼する。RAGは人事Indexと公開Indexを検索し、三つの文書Chunkを取得する。Agentは結果をModelへ渡し、出力Safety Policyの判断を経て回答する。後日、Aliceに許されない人事文書がModelへ渡った疑いが生じる。

調査者は、AliceのSession→個々のRequest→Retrieval Event→取得した文書のIDとVersion、Knowledge Source→推論Event→Policy判断へ辿りたい。Retrieval Logが「3件取得」としか示さなければ、文書とSourceを特定できない。Retrieval EventをSessionへ結び付けられなければ、誰の処理で取得したかも分からない。

## 5. 用語

- **Session Context:** 複数のRequestを同一の会話・一連の処理へ結び付ける情報。Session IDだけを記録しても、検索・推論・Policy Eventと結合できなければ調査に使いにくい。
- **Correlation／Trace ID:** 異なるComponentのEventを同じ処理へ結び付ける識別子。
- **AI-specific Telemetry:** Model、Token使用量、推論・Tool操作等、AI処理の理解に必要な計測情報。
- **Inference Event:** Modelへ入力を渡して出力を得る処理の記録。
- **Policy Decision:** Safety Filter、出力制限などが下した許可・拒否・変更等の判断と、その根拠を示す情報。
- **Knowledge Source:** RAGが文書を取得したIndex、Repository、Data Store等の論理的な取得元。
- **Content Capture:** Query、Prompt、Response、文書本文などの内容自体をLogへ保存すること。識別子やToken数だけのMetadata記録とは影響が違う。

## 6. Threat ModelとAbuse Path

攻撃者は権限外文書の取得を誘発する利用者、悪性文書、侵害されたAgent、またはLog閲覧権限を持つ内部者を想定する。

```text
権限外文書の取得 → Retrieval Eventに文書ID／Sourceなし → 事後に影響範囲を特定できない
Policy回避 → 判断結果・Rule IDなし → 拒否すべき出力が通った原因を再構成できない
Model／Provider切替 → 構造化Fieldなし → 行動変化の原因や影響を追えない
全Prompt／Query／文書本文を広い運用Logへ複製 → Log閲覧者や侵害者へ機密情報が集中
```

Privacyの脅威は「Logを取らない」だけで解消しない。記録不足と過剰記録の両方に対応する。

## 7. Security InvariantとEnforcement Point

| 要件 | 守る性質 | 決定論的な強制地点 |
|---|---|---|
| C12.1.1 | 各AI InteractionをSessionへ結び付け、AI固有の処理情報を残す。 | Application／GatewayのEvent生成とTrace Context伝播。 |
| C12.1.2 | Safety・Policy判断について、いつ・何が・どの結果となったかを調査可能にする。 | Policy／Filter Engineの判断Event生成。 |
| C12.1.3 | 推論EventがModel ID、入出力Token数、Provider、Operation Typeを共通の構造で持つ。 | Inference Adapter／Telemetry PipelineのSchema検証。 |
| C12.1.4 | RAG検索のQuery、取得文書、Knowledge Sourceを、対応する処理から辿れる。 | RetrieverとEvent Exporter、および必要なContent保管先への参照整合性。 |

Logの閲覧権限、保存期間、完全性、費用管理は、要件の記録項目とは別に設計するSecurity Propertyである。Log自体を新たな機密情報の保管場所として扱う。

## 8. Pass／FailとScope Calibration

| 観測 | 判定 | 理由 |
|---|---|---|
| 推論EventにSession IDとAI固有の計測情報があり、対応Requestへ結び付く | C12.1.1 Pass候補 | AI InteractionのContextを追える。 |
| Safety Filterが拒否した事実だけを記録し、判断したPolicyや対象Stageを残さない | C12.1.2 Fail候補 | 監査・原因調査に必要な詳細が不足する。 |
| 推論EventにModel、Provider、Operation Type、入出力Token数が構造化される | C12.1.3 Pass候補 | 最低限指定されたFieldが揃う。 |
| RAG Eventに「3件取得」だけを記録する | C12.1.4 Fail | Query、文書、Sourceが分からない。 |
| Query本文は保護された別Storeにあり、Eventから権限を持つ調査者が確実に辿れる | C12.1.4 Pass候補 | Queryが復元可能な記録として存在する。分離しただけで参照が失われないことを確認する。 |
| QueryのHashだけを残し、Query本文を再構成できない | C12.1.4のPassは主張しない | 「Queryを記録する」の保証を満たすか不明であり、事後調査にも限界がある。 |

文書本文の全量を運用Logへ複製することはC12.1.4の明示的な文面にはない。文書IDだけで足りるかは、後日同じVersionの文書を参照できるかに依存するため、ID・Version・Knowledge Sourceの対応を確認する。Query本文を保管する場合は、機密情報・個人情報を含み得る前提でAccess、Retention、Deletionを設計する。

AISVS ResearchにはMetadata中心・条件付きContent Captureの提案がある。しかし、C12.1.3のNormative原文は「ContentをDefaultで除外する」とは述べていない。その提案を追加のPrivacy設計原則として扱い、原文のPass条件に混ぜない。OpenTelemetryのSensitive／VerboseなFieldをOpt-inとする考え方は実装上の参考となる。[AISVS C12.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-01-Request-Response-Logging.md)、[OpenTelemetry Semantic Convention Guidance](https://opentelemetry.io/docs/specs/semconv/how-to-write-conventions/)

## 9. 運用負荷を抑える実装判断

以下はRepository interpretationであり、特定の製品・方式をAISVSの唯一のPass条件にはしない。

1. 通常のTelemetryにはSession／Trace／Retrieval ID、Source、文書IDとVersion、Model、Token数、Policy判断など調査の索引となるFieldを置く。全文のPrompt・Response・文書本文は自動的に複製しない。
2. 正確なQueryは、必要な保管期間と閲覧権限を定めた既存のRestricted Indexまたは暗号化Storeへ置き、Retrieval Eventから参照できるようにする。必ずしも新しい専用Serviceを作らない。
3. 調査用Contentの閲覧はIncident Response等の限定Roleへ与え、誰がいつどのQueryを参照したかを既存StoreのAccess Auditで追う。監査Event自体へQuery本文を再複製しない。Ticket IDや理由の記録はRiskに応じて追加する。通常のMetadata閲覧すべてに手動承認を要求するわけではない。
4. Metadata Eventは処理の再構成に必要な範囲で継続記録する。保存量はPayload、保持期間、Index数、検索頻度を計測し、Raw Contentの複製や無制限Retentionから先に減らす。容量・費用の上限を運用で監視し、節約のために必須Fieldや相関IDを欠落させない。
5. Queryを別Storeへ分離しても、参照切れ、Key消失、権限の過大設定、監査Logの欠落があれば、追跡性とPrivacyの両方を損なう。定期的にSynthetic Requestで結合とアクセス拒否を試す。

機密情報を含むQueryが常に保存される構成なら、そのStore自体の侵害Impactも残る。高い調査能力には費用と管理責任が伴い、Risk、Retention、利用目的に合わせて決める。

## 10. 対話の再構成

### 問い1：RAG Eventが「3件取得」としか示さない

**Scenario:** Aliceの推論EventにはSession ID、Model、Provider、Token数、Policy判断がある。RAG Eventには取得件数だけあり、Query、文書ID、Sourceがない。

**学習者の判断:** どのSessionがRAGを使ったか分からない。

**整理:** その通り。Sessionとの結合がないため一連の処理を追えない。さらにC12.1.4が直接求めるQuery、取得文書、Knowledge Sourceも不足する。C12.1.1のSession ContextとC12.1.4のRAG Eventを接続する必要性は、Repositoryの調査可能性に関する解釈である。

### 問い2：追跡性とPrivacyの両立

**Scenario:** 通常EventにSession ID、取得元、文書ID・Versionを残し、正確な検索Queryは暗号化された制限付きStoreへ置く。Eventの参照IDから調査者だけが辿れる。

**学習者の判断:** 方向性はよい。ただし、閲覧者を監査する運用や保管Infraの費用が増える。

**整理:** 正しい懸念。保護されたQuery Storeを追加すれば、誰が何を閲覧したか、権限と保存期間を管理する責任が生じる。既存Telemetry基盤のRestricted IndexとAccess Auditを利用できるなら、専用Infraを増やさず実現できる場合もある。全Prompt・全文書を恒久保存するより、必要Fieldと保管期間を絞る。運用費を無視して「Logを増やすほど安全」とは評価しない。

## 11. このSectionの本質

> Incident時に、誰の処理で、何を検索し、どの文書をModelが参照し、どのPolicyが判断したかを辿れるようにする。

> Logは調査の資産であると同時に、新たな機密情報の集積場所にもなる。

> Query本文を保護された場所へ分離しても、参照が切れれば追跡性は失われる。

これらはSourceからの直接引用ではなく、C12.1の保証を現場の設計・運用判断へ翻訳したRepositoryの洞察である。

## 12. 設計レビューとNegative Test

- 一つのSynthetic Sessionを作り、Request→RAG Event→推論Event→Policy Eventを同じTraceで辿れるか。
- 二つのKnowledge Sourceから文書を取得し、Query、文書ID・Version、Sourceを区別できるか。
- Policy拒否と許可を起こし、Decision、Rule／Policy ID、Stage、Requestの対応を調べられるか。
- 推論EventにModel、Provider、Operation Type、入力・出力Token数があるか。
- 許可されない運用Roleから保護されたQueryを読めず、許可された調査者の閲覧を監査できるか。
- Query StoreのRetention後も参照だけが残る場合、調査能力がどう変わるか明示しているか。
- 通常TelemetryへPrompt、文書本文、Secretを意図せずExportしていないか。

## 13. References

- [AISVS v1.0 C12 Normative Requirements](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md)
- [AISVS v1.0 C12.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-01-Request-Response-Logging.md)
- [OpenTelemetry Semantic Convention Guidance](https://opentelemetry.io/docs/specs/semconv/how-to-write-conventions/)
