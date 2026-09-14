---
title: "Web SecurityからAgent Securityへ：ParameterではなくCapability Flowを追う"
document_kind: "cross-cutting-insight"
status: "draft"
last_updated: "2026-09-14"
---

# Web SecurityからAgent Securityへ：ParameterではなくCapability Flowを追う

## 中心となる洞察

Agentic Systemの脆弱性の多くは、Injection、Confused Deputy、過大権限、認可不足、SSRF、Replay、
Supply Chain等、Web Securityから続く問題として理解できる。一方、非信頼入力から副作用までの経路が、
Model、Memory、Tool、複数Agent、外部Systemをまたいで動的に構成されるため、診断単位を広げる必要がある。

> Agent SecurityではParameterを列挙するのではなく、非信頼情報が権限へ影響できる全経路を列挙する。

## Web Securityとの連続性

典型的なWeb Applicationは、次の流れで考えられる。

```text
Request Parameter
  -> Application Logic
  -> SQL / Command / Filesystem / Response
```

Agentic Systemでは、入口と処理、到達先が増える。

```text
Prompt / Web / Document / Retrieval / Tool Output / Memory / Inter-agent Message
  -> Model Context
  -> Reasoning / Planning / Tool Selection
  -> Tool Parameters
  -> API / Filesystem / Message / Payment / Deletion
```

根源は、非信頼DataがInterpreterを介してSecurity-sensitiveなSinkへ到達する問題である。この意味で、
入力検証、出力Encoding、Parameterization、認可、Least Privilege、Egress制御、Sandbox、Replay対策等の
Web Security知識は引き続き有効である。

## Agentは単なるParameterではない

「Web SecurityでいうParameterがAgentになった」という比喩は、攻撃面が広がったことを捉えている。ただし、
より正確にはAgentはParameterではなく、次の役割を兼ねる非決定的なInterpreter兼Dispatcherである。

- 多数の非信頼入力を集める。
- DataをContext、Memory、別Agent、Toolへ伝播する。
- Dataと命令を解釈する。
- 計画、Tool、引数、実行順を選ぶ。
- 人、Application、ServiceのIdentityと権限で副作用を起こす。

この性質により、入力Fieldだけを列挙する従来型の診断では、間接的・持続的・連鎖的な影響を見落としやすい。

## 新しい診断単位：Influence FlowとCapability Graph

二つの図を重ねてSystemを見る。

### Influence Flow

```text
非信頼Data
  -> どこへ保存・変換されるか
  -> どこで命令または判断材料として解釈されるか
  -> どの操作Fieldへ影響できるか
```

### Capability Graph

```text
主体
  -> どのIdentityを使うか
  -> どのTool・API・Queue・Fileへ到達できるか
  -> どのResourceへどの副作用を起こせるか
```

二つが交差する場所が重要なTrust Boundaryになる。非信頼Dataが操作Fieldを支配し、同じ主体またはConfused
Deputyを通じて強いCapabilityへ到達できるなら、攻撃経路が成立し得る。

CapabilityはTool関数やCredentialだけではない。特権Executorが信頼するJob Queue、共有Directory、Database行、
IPC、MemoryへのWriteも、間接的な操作能力になり得る。

## なぜAgentic Contextでは複雑になるのか

| 複雑性 | Security上の意味 |
|---|---|
| 入力源が多い | User Promptだけでなく、Web、RAG、Tool出力、Memory等から攻撃できる |
| 制御Flowが確率的 | 同じ入力でも計画、Tool、引数が変わり、列挙試験だけでは保証しにくい |
| 状態が持続する | MemoryやCheckpointを介して後のSessionで攻撃が発火し得る |
| 権限が連鎖する | Agent、Tool、下流API、別Agentを経由してBlast Radiusが広がる |
| Dataと命令の境界が曖昧 | 自然言語Dataが制御指示として解釈されやすい |
| 能力が動的に増える | Tool discovery、Skill、Plugin、外部ResourceによりAttack Surfaceが変化する |

これは「AIにだけ存在する全く新しい脆弱性」というより、既存のSecurity Failureが、非決定的なOrchestrationに
よって複合・増幅される側面が大きい。ただしPrompt Injection、Model Context、Memory Poisoning等、Model特有の
挙動を既存用語だけで過小評価してはいけない。

## 設計レビューと脅威モデリングへの応用

Systemごとに次を追う。

1. 攻撃者が書込み・操作できるData入口を列挙する。
2. Dataが変換、要約、保存、検索、再利用される経路を追う。
3. Dataが命令や操作Fieldへ昇格する場所を特定する。
4. 各主体のIdentity、Credential、Tool、Network、共有状態へのCapabilityを列挙する。
5. 最終的なSecurity-sensitive Sinkと副作用を特定する。
6. 経路上の決定論的なEnforcement Pointを確認する。
7. 各入口から許可されない副作用までをNegative Testで試す。

```text
Ingress
  -> Transformation / Storage
  -> Interpretation
  -> Identity / Capability
  -> Deterministic Gate
  -> Side Effect
```

Negative Testは「悪意あるPromptを入力したか」だけで終わらせない。Schemaに適合する攻撃値、Tool出力、保存済み
Memory、共有Queue、子Agent等から同じ副作用へ到達できないかを試す。

## AISVS C9.3から見える保証層

AISVS C9.3のRequirementを具体的なSystemへ当てはめると、Failureの場所を次のように分けて考えられる。

| Requirement | 診断する主なFailure |
|---|---|
| C9.3.2 | Tool出力の形式上の契約を検証していない |
| C9.3.3 | ToolのSecurity契約が宣言されていない |
| C9.3.4 | 宣言した契約がRuntimeで強制されない |
| C9.3.5 | 非信頼Dataを処理する主体が強いCapabilityへ到達できる |
| C9.3.6 | 非信頼Tool出力がAgentの操作判断へ昇格する |

この表はAISVS原文の代替や適合Check Listではない。Requirementを分けることで、同じ攻撃経路のどの層が
壊れているかを診断しやすくなる、というRepository interpretationである。

## 具体例

Web Readerが外部ページを読み、Email Executorが要約を送るSystemを考える。

```text
攻撃者が書いたWebページ
  -> Reader
  -> summary / source
  -> Executor
  -> Email API
```

ReaderがEmail Credentialを持たなくても、ExecutorがReaderの自由Textや`recommended_recipient`を無条件に
実行すれば、ReaderはExecutorをConfused Deputyとして使える。反対に、送信先と操作は認証済み利用者の依頼から
構成し、Executorが送信直前にPolicyで認可すれば、Webページから送信先へのInfluence Flowを切れる。

ここでSchema検証は必要になり得るが、Schema適合は認可を意味しない。正しい形式の攻撃値も存在する。

## 誤解しやすい点と限界

- Agent Securityを既存Web Securityの用語へ置き換えるだけでは、Model固有の失敗を捉えきれない。
- Processを分けただけでは、Queue、File、Text等の間接経路が残り得る。
- System PromptやData Sanitizationだけでは、強いCapabilityのSecurity Boundaryにならない。
- Schema検証はDataの形を保証するが、値の権限、真実性、安全性を保証しない。
- Deterministicな認可があっても、過大権限、誤ったPolicy、正規範囲内の悪用は残る。
- 有限のNegative Testだけで、確率的な全挙動を証明することはできない。

## Slide-ready summary

- 根源は既存Securityと連続しているが、非信頼入力から副作用までの経路が長く動的になった。
- AgentはParameterではなく、非決定的なInterpreter兼Dispatcherである。
- Parameter一覧だけでなく、Influence FlowとCapability Graphを重ねて見る。
- Schema、Prompt、Process分離を認可や能力分離の代替にしない。
- Negative Testは各Data入口から許可されない副作用までをEnd-to-endで試す。

## 起点となった学習記録と関連Artifact

本書はAISVSを眺めただけで得られる要約ではなく、C9.3のControlを具体例へ適用し、Web Securityとの連続性を
検討した対話から得たRepository interpretationである。

- [C9 Family overview](../../controls/control-records/c09-orchestration-and-agentic-security/README.md)
- [C9.3.4学習ノート](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.4-runtime-enforcement-of-tool-manifests/learning.md)
- [C9.3.5学習ノート](../../controls/control-records/c09-orchestration-and-agentic-security/v1.0-c9.3.5-isolate-untrusted-data-processing-from-tool-capabilities/learning.md)
- [Repository design](../repository-design.md)
- [AISVS v1.0 C9要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
