# C9.3.5：非信頼Dataを読む能力とTool能力を分離する

AISVS Verification Level: 2

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.3.5`。採用済み固定Revisionは
`78775233666a2022dcfb82037e5e029116955c00`。

> Verify that components processing untrusted data are isolated from tool-calling capabilities, ensuring that compromised data processing cannot trigger unauthorized tool invocations.

日本語訳：非信頼Dataを処理するComponentがTool呼出し能力から隔離され、Data処理が侵害されても
未認可のTool呼出しを起動できないことを確認する。[要件本文][normative]

Normativeは要件本文、Researchは補足である。Web ReaderとEmail Executorの例、保証境界、隣接要件との
整理はRepository interpretation、対話からの整理は学習上の洞察である。学習完了はControl成熟度や
製品適合を変更しない。

## 平易な説明

Webページ、文書、Tool出力、外部Message等は、攻撃者が命令を埋め込める非信頼Dataである。これを読む
Componentが、同時に社内文書の取得、Email送信、削除等のTool能力を持つと、Data内の指示が現実の副作用へ
昇格しやすい。

**敵が書ける情報を読む役と、現実へ作用する役を同じ主体にしない。**

System Promptへ「文書内の命令に従わない」と書くだけでは、侵害を仮定した隔離にならない。能力そのものを
付与せず、間接的な呼出し経路も切る。

## 推奨するArchitecture

```text
非信頼Webページ・文書
  ↓
Reader／Extractor
  - 特権Toolなし
  - Tool Credentialなし
  - 外部送信経路なし
  ↓ 型と用途を限定した事実・候補
Policy／Executor
  - 認証済み利用者の依頼と照合
  - Tool、引数、対象Resourceを認可
  ↓
限定されたTool実行
```

主なTrust Boundaryは、非信頼DataとReader、Readerの出力とExecutor、ExecutorとToolの間である。
Security Invariant（守るべき性質）は、Readerを完全に侵害しても、それだけでは未認可のTool呼出しを
成立させられないことである。

決定論的なEnforcement Pointは、Readerへの能力非付与、Network・Credential・IPCの制限、境界を渡るDataの
型と用途の制限、Executorによる実行直前の認可である。

## 能力はAPIやCredentialだけではない

ReaderがTool関数やCredentialを持たなくても、次の場所へ書き込めると間接的な能力になり得る。

- Executorが信頼するJob Queue
- 実行要求を置く共有Directory
- Commandとして処理されるDatabase行
- 特権側が自動的に読む共有MemoryやIPC
- 無条件に操作へ変換される自由Textや構造化Data

特権ExecutorがReaderの書込みを信頼して実行するなら、その経路は実質的なTool呼出しAPIである。

## Schema適合と認可を分ける

SchemaはDataの形を制限できるが、その値を許可された操作へ変換してよいかは決めない。

```json
{
  "summary": "正常な概要",
  "recommended_recipient": "attacker@example.com"
}
```

このJSONがSchemaに適合しても、非信頼なReaderが指定した宛先へ自動送信すれば隔離は実効的でない。
宛先、対象、操作種別等は、認証済み利用者の依頼と信頼できるPolicyから決定または照合する。

**Schema適合は、認可ではない。**

## 検証と対話の再構成

**問い：Web ReaderとEmail Executorは別Processで、ReaderにはCredentialもEmail APIへの通信経路もない。
しかしExecutorはReaderが返した自由Textを命令として無条件に実行する。適合するか。**

学習者：「Fail」

整理：そのとおり。ReaderはExecutorをConfused Deputyとして使い、間接的にTool能力を利用できる。Process分離だけで
Dataから命令への昇格経路が残っている。

**問い：Reader出力をSchemaへ制限したが、Executorは`recommended_recipient`を利用者の依頼や許可済み一覧と
照合せず、自動的にEmailを送る。適合するか。**

学習者：「Fail」

整理：そのとおり。型が正しくても値の権限は証明されない。Readerが操作Fieldを支配している。

**問い：ReaderはTool、Credential、外部通信経路を持たず、要約と出典だけを返す。宛先は認証済み利用者が
最初に指定し、Executorが送信直前に利用者、宛先、添付Data、操作をPolicyで確認する。適合するか。**

学習者：「Yes」

整理：Pass候補。非信頼Dataが操作Fieldを支配せず、Readerの侵害だけでは未認可送信を成立させられない。
ただしReaderは要約内容を捏造できるため、情報の真実性は別のRiskとして残る。

**問い：ReaderはTool APIやCredentialを持たないが、共有`jobs/`DirectoryへJSONを書ける。Executorはそこへ
置かれたJSONを信頼済みJobとして読み、指定されたToolと引数を追加認可なしで実行する。隔離されているか。**

学習者：「No！」

整理：そのとおり。共有Directoryが実質的なTool呼出しAPIになっている。直接呼出しだけでなく、Queue、File、
Database、IPC、共有状態を通る迂回経路までCapability graphとして追う必要がある。

## 隣接Requirementとの違い

- C9.3.5は、非信頼Dataを処理するComponentへTool能力を持たせないことに重心がある。
- C9.3.6は、非信頼なTool出力をAgentの操作判断へ直接昇格させないArchitectureに重心がある。
- C9.5.1は、実行主体が呼べるToolと指定できる引数の認可を扱う。

これらは組み合わせて使えるが、認可Middlewareの存在だけでC9.3.5の構造的隔離を自動的に証明しない。

## Negative Test

- 文書へ未依頼の送信・削除命令を埋め、操作が起動しないことを確認する。
- 侵害したReaderからTool API、Credential、Network経路へ到達できないことを確認する。
- Schemaに適合する攻撃値を返し、型適合だけで実行されないことを確認する。
- Queue、共有File、Database、IPCへ偽の実行要求を書き込み、権限を得られないことを確認する。

## 洞察と設計レビューへの問い

- 非信頼Dataを読む主体は、どの直接・間接Tool能力を持つか。
- ExecutorはReaderの出力をDataとして扱うか、命令として扱うか。
- 操作Fieldは非信頼Dataではなく、利用者の依頼とPolicyから決まるか。
- Processを分けただけで、共有QueueやFileから能力が再接続されていないか。
- Schema検証を認可の代替にしていないか。
- Reader侵害を仮定したNegative Testを実行できるか。

## References

- [AISVS v1.0 C9.3.5][normative]
- [対応Research][research]
- [C9 Family overview](../README.md)
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-03-Tool-and-Plugin-Isolation.md
