# Engineering Pattern Candidate Landscape

- Status: discovery
- Last updated: 2026-10-27
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
P3とP4の比較後、利用者本人として下流APIを呼ぶ範囲でP3の開発着手が承認された。[MCPの構成・実行主体を選ぶPattern](../domains/mcp/audience-bound-downstream-delegation/README.md)を`draft`として作成した。
2026-10-27、ユーザーのP4実装指示を受け、顧客への情報開示に絞って選定し、[返信材料と送信先を制限するPattern](../domains/agents/untrusted-content-to-action-containment/README.md)を`draft`として作成した。既存Patternの本文レビュー完了を意味しない。

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
| P3 | MCP Access Configuration and Acting Identity（旧 Audience-bound Downstream Delegation） | MCP Serverが下流APIへアクセスする | `mcp/audience-bound-downstream-delegation`を選定・作成 |
| P4 | Untrusted Content-to-Action Containment（開発範囲：顧客への情報開示） | 社内調査から顧客への返信を作るAgent | `agents/untrusted-content-to-action-containment`を選定・作成。一般的な間接Prompt Injection全体には広げない |
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
2026-10-23の対象版は人によるレビュー承認を受けた。2026-10-25に照会・提案を主例へ改訂し、現在版は再レビュー待ちの`draft`。対象版と範囲は[レビュー記録](../domains/agents/secure-tool-execution/README.md#human-review-2026-10-23)を参照。実行検証は未実施。


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

以下は2026-10-23の選定理由を、10-25に見直したP3の範囲へ合わせて整理した比較である。

| 判断軸 | P3：MCPの構成・実行主体・資格の利用 | P4：非信頼コンテンツから操作への誘導 |
|---|---|---|
| 具体的な失敗 | 本人として使うつもりで広いサービス資格を選ぶ、共有処理で別人の資格を使う | メールや文書内の指示が、利用者の依頼・承認として扱われ、送信や更新を誘発する |
| P1・P2から増える境界 | 起動・資格の取得と保持・下流主体の対応。共有サービスを作らず省ける境界も判断する | 情報の出所、読み取りと操作の分離、外部送信経路 |
| 既存成果物との重なり | P1の操作判断と区別し、配置・主体・資格を預かる責任を選べる | タスク範囲と承認の偽装はP1、文書の開示はP2にも説明済み。追加する境界の絞込みが必要 |
| 最初の説明のまとまり | ローカルの本人認証でOktaの管理対象U1を照会し、その後にサービス主体・リモート提供を比較できる | ブラウザー、メール、文書のどれを主例とするか、送信制御の範囲を先に決める必要がある |
| 今回の判断 | `select`。構成選択を先に示すガイドへ再構成 | `retain`。重要性は維持し、P3と同時に開発しない |

P4の問題の反復性は[既存のATLAS調査](mitre-atlas-pattern-discovery-2026-08.md#p4-untrusted-content-to-action-containment)で整理済み。
今回確認した[MSRCの多層防御の説明](https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks)も、外部入力の誤解釈と、認可・送信制御等による影響制限を分けている。
P4を不採用にする判断ではなく、最初に扱う独立した境界を明確にできるP3を優先する本PJの判断である。

## P3: Audience-bound Downstream Delegation

この見出し・配置パスは旧参照を維持する。現在の範囲は**MCPの接続構成と、下流APIを呼ぶ主体の選択**である。

- 配置：[PATTERN-MCP-001](../domains/mcp/audience-bound-downstream-delegation/README.md)。`select`、本文は`draft`。
- 反復する問題：MCPを挟む際、誰の権限で下流APIを呼ぶかが曖昧になり、広いサービス資格や別人の資格で実行する。不要な共有サービスを設けると、資格の集中・利用者分離・公開入口の管理責任も増える。
- 入力：個人端末のMCPから管理APIを利用する構成、共有HTTP型MCPからAPIへ委任する構成、無人のサービスアプリ。Control一覧ではなく異なる主体・配置・資格管理境界を比較する。
- 不変条件：選んだ主体の許可範囲内で実行し、資格の利用先と要求・主体・返却先の対応を保つ。判断不能時に権限を広げない。
- 強制箇所：OS・起動設定、資格管理、MCPの操作境界、下流APIの対象認可。リモートなら入口認可と利用者別の資格・応答分離も必要。
- 確認：権限外対象、資格の取り違え、意図しないサービス主体への切替、別宛先への送信、失効・障害を構成別に試す。
- 隣接境界：P1は個々の操作認可、P2は検索本文の開示。P3は実行場所・主体・資格の保持と利用の選択。任意コードや端末侵害全体の隔離はP13・P14等の別候補で扱う。

### 範囲変更の経緯

2026-10-23にHTTP型MCPから管理下APIへ本人の委任を引き継ぐ範囲で開発着手の承認を得た。
2026-10-25、ユーザーが想定したOkta MCP Serverのローカル直接認証と区別し、構成選択を先に行う共通方針とP3の書直しを明示的に指示した。
これを現在の範囲への開発承認として記録する。本文の技術レビュー完了とは扱わない。

| 構成 | 現在の扱い |
|---|---|
| ローカルstdio＋本人認証 | 主例。OktaのDevice Authorizationで下流用資格を直接取得する流れ |
| サービスアプリ資格 | 別の主体として比較。本人の権限で動くとは扱わない |
| リモートHTTP＋本人の対応付け | 中央提供が必要な場合の選択肢。OBOは委任対応APIを使う場合の一例 |

一次資料の版・状態・採用上の注意は[本文の参照情報](../domains/mcp/audience-bound-downstream-delegation/README.md#7-参照とレビュー情報)に集約する。
Oktaの更新型README・認証処理、MCPの2025-11-25仕様、OktaのOAuth資料、Entra OBO資料を使用し、製品間の相互接続や安全性の実証とはしない。
[構成別の確認用チェックシート](../domains/mcp/audience-bound-downstream-delegation/negative-tests.md)は未実施。
タスク単位の追加制限はP1との組合せとする。このP3選定時点ではP2は`draft`、P4は`retain`。その後のP4選定は次節に記録する。

## P4: Untrusted Content-to-Action Containment

以下は初期候補の観察である。実際に開発した範囲は、この節後半の「2026-10-27の選定」に限定する。

- 選定した配置: [`agents/untrusted-content-to-action-containment`](../domains/agents/untrusted-content-to-action-containment/README.md)。IDは`PATTERN-AGENTS-002`、状態は`draft`。
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

### 2026-10-27の選定：社内で読める情報を、顧客へ何でも送らせない

上記は当初の広い候補。開発対象は「社内情報を調べて顧客へ返信するAgent」に絞った。
ユーザーがこの範囲の提案に続けて「P4の実装を進めなさい」と指示したことを、候補範囲と開発着手の承認として記録する。本文の技術レビューや`recommended`への承認には流用しない。

| 観察・一次資料 | システムと失敗経路 | 再利用する判断・限界 |
|---|---|---|
| [Zendesk Ticket Comments](https://developer.zendesk.com/api-reference/ticketing/tickets/ticket_comments/)（API v2、更新型、2026-10-27確認） | サポート記録には公開コメントと内部メモが共存する。内部情報を読める担当者の返信生成が、その情報を顧客へ公開する経路になる | 閲覧対象と公開対象を分ける業務構造の根拠。Zendeskでの事故や防御の実証を主張しない |
| [AnthropicのブラウザAgent研究](https://www.anthropic.com/research/prompt-injection-defenses)（2025-11-24公開、2026-10-27確認） | メールを読み返信案を作る個人向けAgentに、外部からのメールが機密メールの転送を指示する例 | 非信頼の本文を開示先・目的の決定根拠にしない境界を再利用できる。研究上の例であり、このPatternの実地検証ではない |

- **独立した結果:** P1の操作許可、P2の閲覧許可が両方成立しても、許可された相手へ社内限定情報を送る漏洩は残る。P4は情報を受け取る相手と開示可能な材料を対応付ける。
- **強制点と反証:** サーバーが業務データから返信材料を選び直し、下書き入力・本人の確認・実際の送信へ対応付ける。担当者には読める社内メモを、正規顧客への返信に混ぜる試験が反証になる。
- **再利用性:** サポート返信と個人向けメール処理に、読取り・外部開示の分離、確認済み宛先、内容に結び付く確認を適用できる。主例はWebアプリの固定ツール構成とし、任意ブラウザ操作の実装全体には広げない。
- **統合しない理由:** 操作ごとの認可と承認はP1を再利用するが、返信材料の開示可否とコンテキストの分離は別の設計責務。全入力の意味的な汚染追跡、汎用sandbox、永続memoryの汚染は別候補に残す。
- **適用しない例:** 公開情報だけを固定形式で返す処理では、内部情報から外部開示への境界がない。逆に、内部情報から自由文を自動送信し完全な非漏洩保証を求める構成には、本例の人による確認は十分でない。
- **Decision:** `select`。本文・実装ノート・正負のチェックシートを作成。独立した製品実証、本文の人によるレビュー、長期Ownerは未確保。Golden Patternとしての推奨は行わない。

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

- 開発対象として選定済み: P1・P2・P3・P4（本文は`draft`。P1は改訂後の再レビュー、P2・P3・P4は人による本文レビュー待ち）。
- ATLAS evidenceにより候補を強化する: P1、P4、P6。
- P4は顧客への開示にscopeを絞って開発。一般的な非信頼コンテンツからの全操作誘導を、一つのPatternで扱う方針は採らない。
- P3は構成・実行主体の選択を先に行うガイドへ再構成した。P5・P6は候補として保持する。
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
