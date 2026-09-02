# Engineering Pattern Candidate Landscape

- Status: discovery
- Last updated: 2026-09-03
- Scope: Pattern候補の比較のみ

## 目的と境界

このLandscapeは、具体的なユースケースから反復するセキュリティ設計問題を抽出し、
Pattern化する前に候補の境界、重複、再利用可能性を比較するための作業記録である。

ここに記載された項目はPattern本文ではなく、Pattern lifecycle上の`draft`でもない。
候補名と配置先は暫定であり、個別Patternのディレクトリやプレースホルダーは作成しない。
Control IDやFramework coverageを候補の発見根拠にせず、Controls／FrameworksへのMappingも
この段階では行わない。

現在、実体のある個別Patternは存在しない。`plan.md`とルート`plan.md`に記載された名称は
計画上の候補として比較する。

## 入力ユースケース

1. Agentが社内APIを呼び出す。
2. RAGが複数テナントの文書を検索する。
3. MCP Serverが下流APIへアクセスする。
4. AgentがWebページを読んで操作を行う。
5. 長期memoryへユーザー入力を保存する。

これに加え、MITRE ATLAS v2026.08の全Technique、Mitigation、Case Study、relationshipを
第二の発見入力としてscreeningした。Source snapshot、除外判断、各候補のATLAS evidenceは
[`docs/mitre-atlas-pattern-discovery-2026-08.md`](docs/mitre-atlas-pattern-discovery-2026-08.md)
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
| P3 | Audience-bound Downstream Delegation | MCP Serverが下流APIへアクセスする | 新規候補 |
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

P7からP19の詳細比較は、上記ATLAS discovery recordを正本とする。ここでは候補の索引と
横断比較だけを維持し、同じ分析を複製しない。

## P1: Deterministically Authorized Tool Execution

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

- 暫定配置: `rag/secure-multi-tenant-retrieval`
- 繰り返し発生する設計問題: Vector similarity、検索query、またはmodel context内の
  `tenant_id`を認可の代わりに使用し、未認可文書を検索結果へ混入させる。
- 主なTrust Boundary: caller identityからRetrieval service、Retrieval serviceから
  Vector／database store、document metadataからauthorization policy、取得文書からmodel context。
- Abuse Case: Tenant Aの利用者がTenant Bと類似した文書を検索する、modelがtenant識別子を
  改変する、または権限失効後もcacheやindexから文書が返る。
- Security Invariant: 検索結果は、検索時点で認証済み主体に許可された文書だけで構成する。
  Similarity、model-generated metadata、取得後のpromptは認可判断にならない。
- 決定論的なEnforcement Point: Retrieval service、DatabaseのRow-Level Security、または
  信頼されたPolicy Enforcement Point。認可済みcorpusへ検索範囲を限定する。
- Negative Test: 類似する他tenant文書、偽造tenant ID、失効済みaccess、cache済み結果、
  filter欠落queryを使い、未認可文書が一件も返らないことを確認する。
- 他のユースケースへの再利用可能性: Enterprise search、Memory retrieval、Document
  assistant、Support knowledge base、検索APIへ再利用できる。
- 既存Patternへの統合判断: 計画中の`rag/secure-multi-tenant-retrieval`に統合できる。P1と
  authorization primitiveは共有するが、近似検索、index、metadata、cacheという検索固有の
  境界があるため、Tool Execution Patternへは統合しない。

## P3: Audience-bound Downstream Delegation

- 暫定配置: `mcp/audience-bound-downstream-delegation`
- 繰り返し発生する設計問題: MCP ServerやTool brokerが受信tokenを異なる下流APIへ転送する、
  または広いService Credentialを使用し、Confused Deputyや権限増幅を起こす。
- 主なTrust Boundary: MCP ClientからMCP Server、MCP Serverからdownstream API、inbound
  tokenからtoken exchange、Tool identityからresource server。
- Abuse Case: MCP向けtokenを別audienceのAPIへ転送する、共有administrator credentialを
  使用する、またはclient scopeを無視して下流resourceへアクセスする。
- Security Invariant: 下流で行使される権限は、起点主体の委任範囲、MCP Toolの許可範囲、
  下流resource policyの共通部分を超えない。別audience向けtokenを再利用してはならない。
- 決定論的なEnforcement Point: MCP Serverのauthorization layer、Security Token Service、
  downstream API gateway。Token exchange、audience binding、scope reduction、resource
  authorizationを行う。
- Negative Test: 異なるaudienceへのtoken passthrough、scope拡張、tenant置換、共有Service
  Credentialによる迂回、期限切れtokenの再利用を拒否することを確認する。
- 他のユースケースへの再利用可能性: Plugin broker、API gateway、Service mesh、
  Agent-to-Agent delegation、OAuth連携、内部Microserviceへ再利用できる。
- 既存Patternへ統合できない理由: P1はmodel requestからTool実行までを扱うが、本候補は
  Tool brokerから別resource serverまでの多段委任を扱う。Token audience、token exchange、
  downstream principal、delegation chainという独立した境界とテストが必要になる。

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

- 計画候補を維持する: P1、P2。
- ATLAS evidenceにより候補を強化する: P1、P4、P6。
- 計画候補のscopeと配置を再検討する: P4。
- 新規候補としてLandscapeに保持する: P3、P5、P6。
- ATLASから新規候補として保持する: P7〜P15、P17〜P19。
- P16は、攻撃者側のmulti-agent infrastructureだけでなく、被害側systemのTrust Boundaryとして
  反復する証拠が増えるまで`hold`とする。
- Predictive AIのadversarial input問題は反復性が高いが、modalityごとにEnforcement Pointと
  Negative Testが異なるため、一つのPatternにせずsplit analysisを継続する。
- P5とP6は同じmemory use caseから生じるが、authorization lifecycleとsemantic poisoningで
  Invariant、Enforcement Point、Negative Testが異なるため、候補段階では分離する。

## Pattern化へ進むためのGate

候補を個別Patternの`draft`へ昇格する前に、次を満たす。

具体的な抽出、cluster、split／merge手順は
[`docs/pattern-discovery.md`](docs/pattern-discovery.md)に従う。

1. 少なくとも二つの独立したsystem archetype、または一般化可能な実攻撃・incident evidenceで
   問題の反復性を確認する。
2. 既存候補では表現できないTrust Boundaryまたはsecurity outcomeを説明する。
3. Security Invariant、deterministic Enforcement Point、Negative Testが一貫している。
4. 主配置先と隣接Patternとのcomposition境界を決める。
5. Human reviewで候補scopeを承認する。

Pattern本文はこのGateの後に一つずつ作成する。Controls／FrameworksへのMappingは、Patternと
相手endpointがそれぞれ独立して理解可能になった後、別成果物として評価する。
