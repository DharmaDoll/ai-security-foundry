# Engineering Pattern Candidate Landscape

- Status: discovery
- Last updated: 2026-10-23
- Scope: Pattern候補の比較のみ

## 目的と境界

このLandscapeは、具体的なユースケースから反復するセキュリティ設計問題を抽出し、
Pattern化する前に候補の境界、重複、再利用可能性を比較するための作業記録である。

ここに記載された項目は候補の分析記録であり、Pattern本文とその成熟度はリンク先で管理する。
未選定候補の名前と配置先は暫定であり、ディレクトリやプレースホルダーは作成しない。
Control IDやFramework coverageを候補の発見根拠にせず、Controls／FrameworksへのMappingも
この段階では行わない。

P1を選定し、[安全なツール実行のPattern](../domains/agents/secure-tool-execution/README.md)を作成した。
続いてP2を選定し、[検索時認可のPattern](../domains/rag/secure-multi-tenant-retrieval/README.md)を`draft`として作成した。
P3とP4の比較後、利用者本人として下流APIを呼ぶ範囲でP3の開発着手が承認された。[下流APIへの委任のPattern](../domains/mcp/audience-bound-downstream-delegation/README.md)を`draft`として作成した。

## 入力ユースケース

1. Agentが社内APIを呼び出す。
2. RAGが複数テナントの文書を検索する。
3. MCP Serverが下流APIへアクセスする。
4. AgentがWebページを読んで操作を行う。
5. 長期memoryへユーザー入力を保存する。
6. Agent runtimeとAuthorization PDPが同じ管理IdentityまたはDeployment権限を
   共有し、Agent侵害からPDPを再配置・変更できる。

6番目の観察はAuthorization ControlのReview対話で発見したが、Control IDやRequirement
coverageではなく、共有管理Identityによって実際のTrust Boundaryが消失するSystem failureを
入力とする。Controlとの関係は候補の発見根拠にせず、両Endpointの開発後に別途評価する。

これに加え、MITRE ATLAS v2026.08の全Technique、Mitigation、Case Study、relationshipを
第二の発見入力としてscreeningした。Source snapshot、除外判断、各候補のATLAS evidenceは
[`mitre-atlas-pattern-discovery-2026-08.md`](mitre-atlas-pattern-discovery-2026-08.md)
に記録する。ATLAS IDは発見根拠であり、この段階ではMappingではない。

## 抽出方法

次の順序で、ユースケース名ではなく設計問題を比較する。

```text
実ユースケース
  -> Trust Boundary
  -> Abuse Case
  -> Security Invariant
  -> deterministic Enforcement Point
  -> Negative Test
  -> 複数コンテキストでの再利用可能性
  -> Pattern候補
```

同じ問題、Invariant、Enforcement Point、Negative Testを共有するユースケースは一つの候補へ
まとめる。新しいTrust Boundary、異なる失敗結果、独立したEnforcement Pointまたは固有の
Negative Testが必要なら、別候補として保持する。複数候補で使われる原則やprimitiveは、
それだけでPattern候補にしない。

## 候補一覧

| ID | 暫定候補 | 主な入力ユースケース | 既存の計画候補との関係 |
| --- | --- | --- | --- |
| P1 | Deterministically Authorized Tool Execution | Agentが社内APIを呼び出す | `agents/secure-tool-execution`を支持 |
| P2 | Authorization-aware Retrieval Isolation | RAGが複数テナントを検索する | `rag/secure-multi-tenant-retrieval`を支持 |
| P3 | Audience-bound Downstream Delegation | MCP Serverが下流APIへアクセスする | `mcp/audience-bound-downstream-delegation`を選定・作成 |
| P4 | Untrusted Content-to-Action Containment | AgentがWebを読んで操作する | `llm/indirect-prompt-injection-containment`の境界を再検討 |
| P5 | Authorized Memory Lifecycle | 長期memoryへ入力を保存する | 新規候補 |
| P6 | Persistent Context Poisoning Containment | 長期memoryへ入力を保存する | 新規候補 |
| P7 | Provenance-Bound RAG Ingestion | ATLASのRAG poisoning Case Studies | P2とはingestionとretrievalで分離 |
| P8 | Provenance-Bound Training Data Pipeline | ATLASのtraining data poisoning incidents／exercises | P7とはruntime contextとmodel trainingで分離 |
| P9 | Immutable AI Artifact Resolution and Promotion | ATLASのdependency confusion、rug pull、namespace reuse | 新規候補 |
| P10 | Safe AI Artifact Loading and Processing | ATLASのunsafe model、template、processing pipeline | P9とはidentity resolutionとactive processingで分離 |
| P11 | Capability-Bounded Agent Extension Admission | ATLASのpoisoned Tool／Skill／MCP cases | P9のartifact identityだけでは不足 |
| P12 | Agent Control-Plane Configuration Integrity | ATLASのrules、prompt construction、Tool definition cases | P11とはproject configurationとpackage lifecycleで分離 |
| P13 | Agent Runtime Host and Network Isolation | ATLASのagent RCE、host escape、secret access cases | P1のTool authorizationだけでは不足 |
| P14 | Mediated AI Credential Use | ATLASのcredential harvesting／exfiltration cases | P1、P3とはcredential exposure boundaryで分離 |
| P15 | Bounded Autonomous Objective and Resource Execution | ATLASのautonomous scope adaptation incidents | P1とはsingle actionとmulti-step scopeで分離 |
| P16 | Authenticated and Bounded Inter-Agent Delegation | ATLASのdirect／shared-artifact agent communication | Evidence不足のためhold |
| P17 | Untrusted Model Output at Active Interpreter Boundaries | ATLASのcode execution、rendering、generated command cases | P4とはinput influenceとoutput sinkで分離 |
| P18 | Abuse-Resistant AI Service Resource Budgets | ATLASのdenial／cost／agentic consumption Techniques | Production evidenceを追加確認 |
| P19 | Minimum-Disclosure Inference API | ATLASのmodel extraction／inversion／data leakage cases | P18とはconfidentialityとavailabilityで分離 |
| P20 | Isolated Agent Authorization Control Plane | Agent runtimeとAuthorization PDPが管理境界を共有する | P1、P12、P13とは保護対象とEnforcement Pointが異なる |

P7からP19の詳細比較は、上記ATLAS discovery recordを正本とする。ここでは候補の索引と
横断比較だけを維持し、同じ分析を複製しない。

## P1: Deterministically Authorized Tool Execution

2026-10-22：[P1候補レビュー](tool-execution-candidate-review.md)へ、一次報告の確認、二つの
業務例、不変条件・反証テスト、隣接候補との境界をまとめた。同日の対話で方針と開発着手の
了承を得て`select`へ移行し、[Pattern本文](../domains/agents/secure-tool-execution/README.md)を作成した。
開発者向けガイド・Mermaid図・要点サンプルを中心とし、正負のケースは読者向け確認事項として扱う。
本文は2026-10-23の人によるレビュー承認で`reviewed`となった。対象版と範囲は[レビュー記録](../domains/agents/secure-tool-execution/README.md#human-review-2026-10-23)を参照。実行検証は未実施。


- 暫定配置: `agents/secure-tool-execution`
- 繰り返し発生する設計問題: AgentやLLMが生成したTool／API要求へ、Applicationや
  Service Accountの広い権限をそのまま与え、起点主体の権限を超えた操作を可能にする。
- 主なTrust Boundary: UserからAgent、model outputからTool broker、Agent runtimeから
  社内API、credential issuerからresource server。
- Abuse Case: Prompt Injectionや誤った計画により、Agentが別tenantのデータ取得、管理API、
  または許可されていない副作用を要求する。
- Security Invariant: model-generated requestだけでは操作を認可できない。実行権限は、
  認証済み起点主体の権限、許可された目的、Tool capability、resource policyの共通部分を
  超えてはならない。
- 決定論的なEnforcement Point: Agent外部のTool gatewayまたはPolicy Enforcement Point。
  主体、resource、action、tenant、Tool argumentsを検証し、必要なら狭い資格情報を発行する。
- Negative Test: 未認可API、別tenant ID、引数改ざん、Policy Decision Pointの迂回、
  認可サービス障害時のfail-openを試し、すべて拒否されることを確認する。
- 他のユースケースへの再利用可能性: Database、Cloud API、Ticket、決済、メール、MCP Tool、
  Browser actionなど、model outputが外部副作用へ変換されるシステムへ再利用できる。
- 既存Patternへの統合判断: 計画中の`agents/secure-tool-execution`そのものであり、別候補に
  分離する理由はない。社内API呼出しを最初の具体的ユースケースとして利用できる。

## P2: Authorization-aware Retrieval Isolation

2026-10-23：ユーザーが、テナントを異なる会社とする説明例を確認し、「この方針で進めてください！」と開発着手を承認した。
以下の候補確認により`retain`から`select`へ移行した。本文の人による技術レビューとは別の判断である。
[Pattern本文](../domains/rag/secure-multi-tenant-retrieval/README.md)と[チェックシート](../domains/rag/secure-multi-tenant-retrieval/negative-tests.md)を作成済み。状態は`draft`、製品の実行検証は未実施。

| 観察したシステム類型 | 繰り返される失敗経路 | 共通の設計と適用上の違い |
|---|---|---|
| 複数企業に提供する文書検索SaaS | 共有検索基盤が、質問に似ている他社文書を返す。質問やモデル指定の会社IDを検索権限として使う | 検証済み所属と文書の会社を照合する。会社をまたぐ検索品質への影響は、情報開示の認可とは別に扱う |
| 一社内の部署・担当別ナレッジ検索 | 同じ会社であれば全員が読めると扱い、制限文書や権限変更前のキャッシュを返す | 文書単位の閲覧権限も照合する。グループ・担当の変更を検索経路とキャッシュへ反映する |

二つの類型は本PJの設計分析であり、実被害や再現実験の報告ではない。
技術的な裏付けとして、[pgvector v0.8.7のMultitenancy／Filtering](https://github.com/pgvector/pgvector/blob/v0.8.7/README.md#multitenancy)、
[PostgreSQL 18のRLS](https://www.postgresql.org/docs/18/ddl-rowsecurity.html)、
[Azure AI Searchのsecurity filter方式](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search)を2026-10-23に確認した。
Azure資料は更新型（表示上の更新日2026-08-24）。識別子を含むフィルターだけでは本人確認にならないことを確認した。
製品ごとの構文は異なるが、信頼する本人・文書権限に検索を束縛し、開示前に強制する点を再利用できる。

主な例は会社A・Bのサポート用RAGとし、会社内の文書権限とキャッシュ再利用も扱う。
選定理由は、開示される資産・強制箇所・反証方法が具体的で、P1と異なる検索固有の境界があること。
P7は文書の取り込みと出所・汚染、P5は保存されたmemoryのライフサイクルを扱うため統合しない。
物理分離や規制上の専用環境が必要な用途は、本例の論理的な検索時認可だけでは足りない。

- 暫定配置: `rag/secure-multi-tenant-retrieval`
- 繰り返し発生する設計問題: Vector similarity、検索query、またはmodel context内の
  `tenant_id`を認可の代わりに使用し、未認可文書を検索結果へ混入させる。
- 主なTrust Boundary: caller identityからRetrieval service、Retrieval serviceから
  Vector／database store、document metadataからauthorization policy、取得文書からmodel context。
- Abuse Case: Tenant Aの利用者がTenant Bと類似した文書を検索する、modelがtenant識別子を
  改変する、または権限失効後もcacheやindexから文書が返る。
- Security Invariant: 開示する検索結果は、明示した権限確認時点で認証済み主体に許可された文書だけで構成する。
  失効の反映期限を定め、期限を超えた古い許可を再利用しない。Similarity、model-generated metadata、取得後のpromptは認可判断にならない。
- 決定論的なEnforcement Point: Retrieval service、DatabaseのRow-Level Security、または
  信頼されたPolicy Enforcement Point。認可済みcorpusへ検索範囲を限定する。
- Negative Test: 類似する他tenant文書、偽造tenant ID、失効済みaccess、cache済み結果、
  filter欠落queryを使い、未認可文書が一件も返らないことを確認する。
- 他のユースケースへの再利用可能性: Enterprise search、Memory retrieval、Document
  assistant、Support knowledge base、検索APIへ再利用できる。
- 既存Patternへの統合判断: 計画中の`rag/secure-multi-tenant-retrieval`に統合できる。P1と
  authorization primitiveは共有するが、近似検索、index、metadata、cacheという検索固有の
  境界があるため、Tool Execution Patternへは統合しない。

## 次候補の比較：P3とP4

2026-10-23、ユーザーの「次に進もう」を受け、P2の作業計画にある次候補比較を実施した。
**比較後、P3を開発対象に選定した。** P2の文書整理は完了しているが、現在版への明示的な技術レビュー承認とは区別し、`draft`を維持する。

| 判断軸 | P3：下流APIへの権限委任 | P4：非信頼コンテンツから操作への誘導 |
|---|---|---|
| 具体的な失敗 | MCPの入口で本人を確認しても、下流APIを広い共通資格情報で呼び、別会社の注文を返す | メールや文書内の指示が、利用者の依頼・承認として扱われ、送信や更新を誘発する |
| P1・P2から増える境界 | 別サービス用のトークン取得と、下流APIでの利用者・対象の照合 | 情報の出所、読み取りと操作の分離、外部送信経路 |
| 既存成果物との重なり | P1の操作判断と区別し、別APIへ本人の資格を引き継ぐ部分を独立して説明できる | タスク範囲と承認の偽装はP1、文書の開示はP2にも説明済み。追加する境界の絞込みが必要 |
| 最初の説明のまとまり | 「注文1001を照会する」を、入口から下流APIの応答まで追える | ブラウザー、メール、文書のどれを主例とするか、送信制御の範囲を先に決める必要がある |
| 今回の判断 | `select`。本人の下流アクセスと既存APIの認可に絞って開発 | `retain`。重要性は維持し、P3と同時に開発しない |

P4の問題の反復性は[既存のATLAS調査](mitre-atlas-pattern-discovery-2026-08.md#p4-untrusted-content-to-action-containment)で整理済み。
今回確認した[MSRCの多層防御の説明](https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks)も、外部入力の誤解釈と、認可・送信制御等による影響制限を分けている。
P4を不採用にする判断ではなく、最初に扱う独立した境界を明確にできるP3を優先する本PJの判断である。

## P3: Audience-bound Downstream Delegation

- 配置: [`mcp/audience-bound-downstream-delegation`](../domains/mcp/audience-bound-downstream-delegation/README.md)。`select`、本文は`draft`。
- 繰り返し発生する設計問題: MCP ServerやTool brokerが受信tokenを異なる下流APIへ転送する、
  または広いService Credentialを使用し、Confused Deputyや権限増幅を起こす。
- 主なTrust Boundary: MCP ClientからMCP Server、MCP Serverからdownstream API、inbound
  tokenからtoken exchange、Tool identityからresource server。
- Abuse Case: MCP向けtokenを別audienceのAPIへ転送する、共有administrator credentialを
  使用する、またはclient scopeを無視して下流resourceへアクセスする。
- Security Invariant: 下流で行使される権限は、起点主体の委任範囲、MCP Toolの許可範囲、
  下流resource policyの共通部分を超えない。別audience向けtokenを再利用してはならない。
- 決定論的なEnforcement Point: MCP Serverのauthorization layer、Security Token Service、
  downstream APIの対象認可。各APIのaudience・必要scopeを確認し、設定された利用者委任方式で
  下流用資格を得る。Gatewayでトークンを検証するだけで対象認可が完成するとはしない。
- Negative Test: 異なるaudienceへのtoken passthrough、scope拡張、tenant置換、共有Service
  Credentialによる迂回、期限切れtokenの再利用を拒否することを確認する。
- 他のユースケースへの再利用可能性: Plugin broker、API gateway、Service mesh、
  Agent-to-Agent delegation、OAuth連携、内部Microserviceへ再利用できる。
- 既存Patternへ統合できない理由: P1はmodel requestからTool実行までを扱うが、本候補は
  Tool brokerから別resource serverまでの多段委任を扱う。Token audience、token exchange、
  downstream principal、delegation chainという独立した境界とテストが必要になる。

### P3の最初の範囲：担当注文の照会を下流APIへ引き継ぐ

会社Aの担当者Aが注文1001を照会し、HTTP型MCPサーバーが本人の委任で注文APIを呼ぶ。
注文APIの既存認可が、他社の9001・同じ会社の担当外1003を拒否する。
**入口だけOAuth、下流は共通管理者という構成を避け、本人のアクセス制御をサービス間で保つ。**

| 決めた項目 | 開発範囲 |
|---|---|
| 対象 | 利用者のいるHTTP型MCP → 管理下の注文APIへの読取り。既存APIの利用者・注文認可を活用する |
| 根拠情報 | 検証済みの利用者資格、API側の所属・注文権限、管理された接続先・委任設定 |
| 強制箇所 | MCP入口の資格・ツール認可、MCP側の本人と下流資格の対応、注文APIの資格検証・対象認可 |
| 主例 | Entra OBOとMSALで下流用資格を取得。①要求 → ②MCPの確認 → ③資格取得 → ④API呼出し → ⑤APIの対象認可を追う |
| 対象外 | stdio、無人バッチ、任意の第三者SaaS、返金・決済。タスク単位の追加制限はP1との組合せ |

利用者が通常読める1002を「今回の依頼外だから拒否する」条件は、最初の計画から分離した。
OAuthによる本人の委任と、エージェントに任せたタスクの範囲を混同しない。
MCPへ注文の権限表を複製することも要求しない。

**二つの構成での再利用根拠：** MCPのHTTPプロキシ型構成と、従来のWeb API A → API Bの利用者委任。
前者はMCP公式仕様、後者はEntra OBO公式資料で境界を確認した。実インシデントの件数・製品試験の証拠ではない。
P1は操作可否、P2は検索本文の開示、P3は別APIへ渡る資格と主体の対応を扱う。

### 成果物と確認方法

- [Pattern本文](../domains/mcp/audience-bound-downstream-delegation/README.md)：一件の注文照会、図、照合責務、OBOの要点、運用・限界・参照情報。
- [確認用チェックシート](../domains/mcp/audience-bound-downstream-delegation/negative-tests.md)：正常系、別宛先・別人の資格、権限外注文、失効・障害。操作・期待結果・証拠・結果欄と依頼例を提供。

下流用資格の取得は対象認可・即時失効・タスク制限を自動で完成させるものではない。
Entra OBOは利用者委任の一方式であり、app-onlyへ適用しない。RFC 8693のToken Exchangeとは要求形式が異なり、MCP全実装にいずれかの採用を義務付ける説明にもしない。
詳細は本文を正本とし、この選定記録へ重複した図・チェックリストを置かない。製品試験は未実施。

### 一次資料の確認範囲

確認日：2026-10-23。以下は仕様・製品説明の確認であり、連携の動作検証ではない。

| 一次資料 | 参照状態と、今回確認したこと |
|---|---|
| [MCP Authorization 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) | [2025-11-25公開の仕様版](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/)を参照。HTTP向け認可、宛先検証、入力トークンのパススルー禁止。最新版という主張やRepository全体の新版採用はしない |
| [MCP Security Best Practices](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices) | 版付き入口から到達する公式補足ガイド。トークンパススルーと代理権限の濫用を区別する。独立した規格の成熟度認定ではない |
| [Microsoft Entra OBO](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-on-behalf-of-flow) | 更新型の製品資料、表示更新日2025-01-04。利用者の委任、API A用とAPI B用のトークン、同意・適用制約。SDK版は未選定 |
| [RFC 8693](https://www.rfc-editor.org/rfc/rfc8693.html) | 2020-01公開、Standards Track。Token Exchangeの要求・宛先・権限を参照。交換サービス固有の認可方針を自動で保証するものではない |
| [MSRCの間接Prompt Injection対策](https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks) | 2025-07-29公開のベンダー解説。P4の比較材料として使用 |

2026-10-23、OAuthで下流まで本人の権限が引き継がれる場合は構成を簡潔にする議論を経て、ユーザーが「これまでの議論も踏まえP3の実装をすすめてくれ」と指示した。
これを以下の候補範囲への承認として`select`へ移行した：利用者のいるHTTP型MCP、管理下の注文APIへの読取り、本人の委任と既存APIの対象認可、タスク制限はP1への補足。
作成した本文の技術レビュー承認とは区別し、P3は`draft`、P2も`draft`を維持する。

## P4: Untrusted Content-to-Action Containment

- 暫定配置: `agents/untrusted-content-to-action-containment`
- 繰り返し発生する設計問題: Web、メール、文書、Tool outputなどの非信頼content内の命令が
  model planへ混入し、外部操作や機密情報送信へ変換される。
- 主なTrust Boundary: external contentからBrowser／retriever、取得contentからmodel context、
  model planからAction broker、read capabilityからwrite capability。
- Abuse Case: Webページ内の命令により、Agentがcredentialや内部情報を外部送信する、購入、
  削除、設定変更を行う、または承認済みと偽って操作する。
- Security Invariant: 非信頼contentは、新しい権限、操作目的、承認、送信先を設定できない。
  Content由来のmodel outputだけでは外部副作用や機密データ送信を認可できない。
- 決定論的なEnforcement Point: Action broker、Egress gateway、user-intent binding、read-onlyと
  side-effect capabilityの分離、およびhigh-impact action approval。
- Negative Test: Webページへ秘密の外部送信、管理設定変更、承認省略の命令を埋め込み、Agentが
  従ってもAction／Egress境界で拒否されることを確認する。
- 他のユースケースへの再利用可能性: メール、Support ticket、RAG文書、MCP Resource、
  Tool output、共有文書、長期memoryへ再利用できる。
- 既存Patternへ統合できない理由: P1は生成済みTool requestの認可を扱うが、本候補は
  非信頼contentがcontrol contextやuser intentへ化ける上流の情報フローも扱う。Content
  provenance、read／write capability分離、Egress制御が必要なため、P1のNegative Testだけでは
  完結しない。計画中の`llm/indirect-prompt-injection-containment`とは重なるが、Pattern化前に
  一般的なPrompt InjectionではなくContent-to-Action境界へscopeを絞るか再検討する。

## P5: Authorized Memory Lifecycle

- 暫定配置: `memory/authorized-memory-lifecycle`
- 繰り返し発生する設計問題: 長期memoryのwrite、read、update、deleteにprincipal、tenant、
  purpose、retentionの制約がなく、別利用者や将来sessionへデータが漏れる。
- 主なTrust Boundary: User／AgentからMemory write service、Memory serviceからpersistent store、
  stored memoryからfuture session、およびtenant間境界。
- Abuse Case: Agentが別利用者のmemoryを書き換える、共有keyへ保存する、または削除・失効済み
  memoryが再取得される。
- Security Invariant: Memoryのread、write、update、deleteは認証済み主体、tenant、purpose、
  retention policyへ結合する。失効・削除されたmemoryは将来contextへ戻らない。
- 決定論的なEnforcement Point: Memory API gateway、tenant-bound storage policy、
  retention／deletion service、retrieval authorization layer。
- Negative Test: 別tenantへのwrite、owner ID偽造、期限切れmemory取得、削除後の再出現、cacheを
  使った失効回避を試し、すべて拒否または除外されることを確認する。
- 他のユースケースへの再利用可能性: 会話履歴、User profile、Agent scratchpad、Workflow
  state、Personalization storeへ再利用できる。
- 既存Patternへ統合できない理由: P2とtenant isolationは共有するが、Memoryにはwrite
  authorization、update、retention、delete、future sessionへの再投入という時間軸がある。
  検索時認可だけを扱うRAG Patternではlifecycle全体を検証できない。

## P6: Persistent Context Poisoning Containment

- 暫定配置: `memory/persistent-context-poisoning-containment`
- 繰り返し発生する設計問題: User inputやexternal contentが長期memoryへ保存され、後続sessionで
  信頼されたinstruction、fact、authorization contextとして再利用される。
- 主なTrust Boundary: untrusted inputからMemory writer、stored contentからContext assembler、
  memory provenanceからmodel、future model outputからTool／action boundary。
- Abuse Case: 利用者が「今後すべての承認を省略する」と保存させ、別sessionでAgentを
  乗っ取る。または悪意ある内容が共有memoryを通じて他の利用者へ影響する。
- Security Invariant: 永続化によって非信頼contentの信頼レベルを上昇させない。Memory contentは
  system policy、authorization context、approval record、信頼されたidentity attributeを
  上書きできない。
- 決定論的なEnforcement Point: Memory write policy、provenance付与、typed memory schema、
  Context assembler、信頼レベル別の分離、最終Action Enforcement Point。
- Negative Test: 永続化した命令を別sessionで再読込し、system policy変更、承認省略、秘密送信、
  別tenantへの影響を試す。Modelが従ってもsecurity invariantが維持されることを確認する。
- 他のユースケースへの再利用可能性: RAG ingestion、Conversation history、Shared agent state、
  Tool cache、Profile enrichment、Agent間message storeへ再利用できる。
- 既存Patternへ統合できない理由: P4と非信頼contentの扱いは共有するが、永続化、後続sessionでの
  再生、provenance保持、削除、修復という時間的境界がある。単一実行内のWeb content
  containmentへ統合すると、蓄積、再生、回復のテストが埋没する。

## P20: Isolated Agent Authorization Control Plane

- 暫定配置: `identity-and-authorization/`。`agents/`を隣接Domainとする。
- 繰り返し発生する設計問題: Agent runtimeとAuthorization PDPが同じService identity、
  Policy storage、Deployment権限、管理Interface、またはLifecycle controlを共有し、Agent
  runtimeの侵害が認可判断を行うControl Planeの侵害へ直結する。
- 主なTrust Boundary: Agent runtimeからPDP execution boundary、Agent workload identityから
  PDP administrative plane、Policy Administration PointからPolicy store、Deployment systemから
  PDP workloadおよびrecovery configuration。
- Abuse Case: Prompt Injection、Agent frameworkの脆弱性、悪意あるTool outputなどでAgent
  runtimeを制御した攻撃者が、共有Identityや管理Interfaceを使ってPolicyを変更する、PDPを
  攻撃者管理Imageへ再配置する、PDPを停止する、またはRecovery時に置き換える。
- Security Invariant: Agent runtimeが完全に侵害されても、その実効Identityと到達可能な
  Interfaceだけでは、PDP、Authoritative policy、Administrative credential、Deployment、
  Lifecycle、Recovery stateを変更・置換・制御できない。
- 決定論的なEnforcement Point: 分離されたWorkload／Administrative identity、IAM policy、
  Policy administration path、Deployment admission、Process／Container／Host boundary、管理
  Network、Secret store、および独立したRecovery control。
- Negative Test: Agentの実効IdentityとNetwork位置から、Policy write、PDP debug／admin access、
  Workload impersonation、Secret read、PDP停止、Image／Endpoint差替え、Rollback、Recovery
  configuration変更を試し、すべて拒否またはAuthoritative PDPに影響しないことを確認する。
- 他のユースケースへの再利用可能性: Internal APIを呼ぶAgentのTool gateway、Multi-tenant
  RAGのRetrieval authorization service、MCP ServerのDownstream authorization、Memory
  read／write policy serviceで、同じ管理境界、Invariant、Negative Testを再利用できる。
- CounterexampleとScope外: Agentが偽のIdentity attributeをRequestへ入れる問題、PDP Response
  の改ざん、PEPを通らないResource access、PolicyのRead-only参照、Decision logの削除は、
  それだけでは本候補のInvariant違反としない。それぞれAuthorization context、Decision
  binding、Complete mediation、Least disclosure、Evidence integrityの別問題として扱う。
- 既存候補へ統合できない理由: P1は個々のTool actionを許可する判断と実行を扱い、P12は
  Project contentからAgent自身のConfigurationへの遷移を扱い、P13はAgent runtimeからHost／
  Networkへの到達範囲を扱う。本候補は、認可判断を行うAuthority自体の管理・Deployment・
  Lifecycle boundaryを保護し、異なるNegative Testを必要とする。
- Evidence gap: 複数System archetypeへの適用可能性は確認できるが、独立したProduction事例、
  Incident、または再現可能なDemonstrationはまだ紐付いていない。候補選定前にEvidenceを
  追加し、P1やP13の一部へ統合すべきでないか再評価する。
- Decision: `retain`。Pattern本文やDirectoryはまだ作成しない。

## 候補間の関係

```text
P4 Untrusted content containment
  -> P1 Deterministically authorized action

P1 Tool execution
  -> P3 Multi-hop downstream delegation

P5 Authorized memory lifecycle
  + P6 Persistent context poisoning containment
  -> 安全な長期memory use case

P2 Retrieval isolation
  <-> P5 Memory retrieval authorization

P7 RAG ingestion integrity
  -> P4 Untrusted content containment
  -> P2 Retrieval isolation

P9 Artifact resolution
  -> P10 Safe artifact processing
  -> P11 Agent extension admission

P12 Agent control-plane integrity
  + P13 Runtime isolation
  + P14 Credential mediation
  -> P1 Authorized Tool execution

P20 Authorization control-plane isolation
  -> P1 Tool execution
  -> P2 Retrieval isolation
  -> P5 Authorized memory lifecycle

P15 Autonomous scope continuity
  + P16 Inter-agent delegation
  -> bounded multi-agent workflow

P17 Active output sinks
  <-> P4 Content-to-action containment

P18 Resource budgets
  <-> P15 Autonomous workflow bounds
```

この関係はPattern間のcomposition候補であり、Control／Framework Mappingではない。

次は横断的な原則またはprimitiveであり、現段階では独立Pattern候補にしない。

- model外部の決定論的authorization;
- least privilegeとscoped credential;
- provenanceとtrust levelの保持;
- tenant binding;
- fail-closed behavior;
- security decisionとactionの監査証跡。

これらは複数の具体的Patternで同じ安定した実装問題が確認されてから、共有ガイダンスとして
抽出する。

## 現時点の比較結果

- 開発対象として選定済み: P1（本文は`reviewed`）、P2・P3（本文は`draft`、人による本文レビュー待ち）。
- ATLAS evidenceにより候補を強化する: P1、P4、P6。
- 計画候補のscopeと配置を再検討する: P4。
- P3は本人の下流アクセスに範囲を絞って作成した。P4・P5・P6は候補として保持する。
- ATLASから新規候補として保持する: P7〜P15、P17〜P19。
- System boundary Reviewから新規候補として保持する: P20。ただし独立したEvidenceを追加するまで
  Pattern開発対象には選定しない。
- P16は、攻撃者側のmulti-agent infrastructureだけでなく、被害側systemのTrust Boundaryとして
  反復する証拠が増えるまで`hold`とする。
- Predictive AIのadversarial input問題は反復性が高いが、modalityごとにEnforcement Pointと
  Negative Testが異なるため、一つのPatternにせずsplit analysisを継続する。
- P5とP6は同じmemory use caseから生じるが、authorization lifecycleとsemantic poisoningで
  Invariant、Enforcement Point、Negative Testが異なるため、候補段階では分離する。

## Pattern化へ進むためのGate

候補を個別Patternの`draft`へ昇格する前に、次を満たす。

具体的な抽出、cluster、split／merge手順は
[`pattern-discovery.md`](pattern-discovery.md)に従う。

1. 少なくとも二つの独立したsystem archetype、または一般化可能な実攻撃・incident evidenceで
   問題の反復性を確認する。
2. 既存候補では表現できないTrust Boundaryまたはsecurity outcomeを説明する。
3. Security Invariant、deterministic Enforcement Point、Negative Testが一貫している。
4. 主配置先と隣接Patternとのcomposition境界を決める。
5. Human reviewで候補scopeを承認する。

Pattern本文はこのGateの後に一つずつ作成する。Controls／FrameworksへのMappingは、Patternと
相手endpointがそれぞれ独立して理解可能になった後、別成果物として評価する。
