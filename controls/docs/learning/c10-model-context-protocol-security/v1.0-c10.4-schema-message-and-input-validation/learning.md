---
title: "AISVS C10.4 Schema, Message, and Input Validation 学習ノート"
document_kind: "section-learning-note"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
section_id: "C10.4"
requirements:
  - "v1.0-C10.4.1"
  - "v1.0-C10.4.2"
  - "v1.0-C10.4.3"
  - "v1.0-C10.4.4"
  - "v1.0-C10.4.5"
  - "v1.0-C10.4.6"
  - "v1.0-C10.4.7"
  - "v1.0-C10.4.8"
last_updated: "2026-09-26"
---

# C10.4 Schema, Message, and Input Validation

## 1. 文書の役割とSource separation

本書はAISVS v1.0 C10.4の全8 Requirementを、一つのMCP Tool利用に沿って学ぶ講義と対話の再構成である。製品適合の証拠やControl本文の代替ではない。

- **Normative:** 固定Revisionにある下表のRequirement原文とVerification Level。
- **AISVS Research:** Schema、Prompt Injection、Payload、Replay、Local導入、Tool定義変更の脅威と検証例。掲載製品・事件・統計は独立確認せず、Pass条件へ転用しない。
- **Repository interpretation:** 形式、内容、サイズ、真正性・鮮度、導入・変更時の承認を別々の保証として検査する。
- **Derived insight:** Schema上のPassは自然言語の安全性を示さず、署名とTimestampのPassはNonceの再利用拒否を示さない。

## 2. Normative Requirements

| ID | Level | AISVS English | 日本語訳 |
|---|---:|---|---|
| `v1.0-C10.4.1` | 1 | Verify that MCP tools/list and tools/call responses are validated against their declared schemas before being injected into the model context. | `tools/list`と`tools/call`の応答を、宣言Schemaで検証してからModel Contextへ入れることを確認する。 |
| `v1.0-C10.4.2` | 1 | Verify that MCP tools/list and tools/call responses are screened for indirect prompt injection before being injected into the model context. | 同じ応答を、Indirect Prompt Injectionの観点で検査してからModel Contextへ入れることを確認する。 |
| `v1.0-C10.4.3` | 1 | Verify that MCP servers reject unrecognized or oversized parameters in function calls. | MCP ServerがTool呼出しの未知または過大な引数を拒否することを確認する。 |
| `v1.0-C10.4.4` | 2 | Verify that all MCP servers enforce strict schema validation. | すべてのMCP Serverが厳格なSchema検証を強制することを確認する。 |
| `v1.0-C10.4.5` | 2 | Verify that all MCP transports enforce maximum payload size limits. | すべてのMCP TransportがPayload全体の最大Sizeを強制することを確認する。 |
| `v1.0-C10.4.6` | 2 | Verify that MCP servers sign tool responses with a unique nonce and timestamp so MCP clients can detect replay attempts. | MCP Serverが一意なNonceとTimestampを付けてTool応答に署名し、ClientがReplayを検出できることを確認する。 |
| `v1.0-C10.4.7` | 2 | Verify that MCP clients present users with explicit consent dialogue and cancellation options upon installation of a local MCP server. | Local MCP Server導入時にClientが明示的な同意画面と取消し手段をUserへ示すことを確認する。 |
| `v1.0-C10.4.8` | 3 | Verify that MCP clients maintain a snapshot of tool definitions and that any change to a tool definition triggers re-approval before the modified tool can be invoked. | ClientがTool定義のSnapshotを保持し、定義変更後は再承認まで変更Toolを呼び出せないことを確認する。 |

正本は[固定RevisionのC10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)である。

## 3. C10内での位置づけ

C10.1はComponentの取得・Admission・Sandbox、C10.2はCallerとToolの認証・認可、C10.3は通信境界を扱う。C10.4では、正規の経路を通った後でもMCP Message、Tool Metadata、結果、引数、承認済み定義が安全に利用できるかを扱う。

```text
Local導入時の同意 C10.4.7
  → Tool定義の承認と変更検出 C10.4.8
  → tools/list応答のSchema・Injection検査 C10.4.1–2
  → tools/call引数の検査 C10.4.3–4
  → 全TransportのPayload上限 C10.4.5
  → tools/call応答の署名・ReplayとSchema・Injection検査 C10.4.6, C10.4.1–2
```

## 4. Concrete ScenarioとProtocolの基本

社内AgentのMCP Clientが`search_documents` Toolを使う。Serverは最初にToolの名前、説明、引数Schemaを返す。Clientが検索を要求すると、Serverは検索結果を返す。その中には、攻撃者が編集できる文書の文章も含まれる。Serverは後日、Toolの説明やSchemaを変更できる。

- **`tools/list`:** Clientが「どんなToolを使えるか」と尋ねるRequest。応答にはTool名、説明、`inputSchema`等が入る。ModelがToolを選ぶ材料になる。
- **`tools/call`:** Clientが「このToolを、この引数で実行して」と依頼するRequest。Serverは実行結果またはErrorを返す。Modelが直接Protocolを送るとは限らず、Host／Clientが呼出しを仲介する。

```text
Client → tools/list → Server → Tool定義 → Client → Model Context
Client → tools/call(name, arguments) → Server → Tool結果 → Client → Model Context
```

Clientが受け取る`tools/list`／`tools/call`の**応答**と、Serverが受け取る`tools/call`の**引数**は、別のTrust Boundaryにある。[MCP Tools仕様](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)

## 5. 用語

- **Schema:** Dataの項目、型、範囲等を記す契約。Schemaが正しいことは、文章が真実・安全・善意である証明ではない。
- **Model Context:** Modelが回答やTool選択のために読む情報。外部Toolの説明や結果も入る。
- **Indirect Prompt Injection:** 文書、Tool説明、結果、Error等のDataに命令を混ぜ、Agentの行動を誘導する攻撃。
- **Payload:** 通信で運ぶMessage全体。個々の引数の長さとは異なる。
- **Nonce:** 一回限りの値。同じ署名済み応答を再利用したか識別するために使う。
- **Timestamp:** 応答の時刻。許容時間内のReplayをTimestampだけで検出することはできない。
- **Snapshot:** 承認時のTool定義を保存したもの。再取得した定義との差を検出する。

## 6. Threat ModelとAbuse Path

攻撃者はTool Server、検索対象文書、Repository設定、Tool引数、通信中継または古い応答を操作できる場合を考える。

```text
Schema上は正しい検索結果に「秘密を送信せよ」 → ModelがDataを指示として解釈
未知Field／型違いのTool引数 → Serverが暗黙変換・Backendへ転送 → 予期しない実行
stdio MessageにSize上限なし → Memory／ParserのResourceを枯渇
以前の署名済み「成功」応答をReplay → 現在の失敗を成功と誤認
承認済みToolの説明を後日変更 → 再承認なしにModelのTool選択を誘導
Local導入UIを省略 → Workspace設定だけでClientがChild Processを起動
```

## 7. Security InvariantとEnforcement Point

| 要件 | 守る性質 | 決定論的な強制地点 |
|---|---|---|
| C10.4.1 | Modelへ渡す応答の構造は、適用できる宣言Schemaに一致する。 | Client／GatewayのPre-context Validator。 |
| C10.4.2 | Modelに見せるTool Metadataと結果は、Injection検査と検出時処理を通る。 | Client／GatewayのPre-context Inspectionと、後続Action Gate。 |
| C10.4.3 | 未知・過大なFunction ArgumentをTool実行前に拒否する。 | MCP ServerのTool Dispatch前。 |
| C10.4.4 | Serverは型、必須Field、範囲、追加Field等のSchema制約を厳格に強制する。 | 各MCP ServerのRequest Validator。 |
| C10.4.5 | どの有効Transportでも上限超過のMessageを処理しない。 | HTTP／stdio等のFraming・Read Loop、Gateway。 |
| C10.4.6 | Clientは現在のTool Requestへ結び付いた、未使用で新しい署名済み応答だけを受理する。 | ServerのResponse Signer、ClientのSignature／Nonce／Context Gate。 |
| C10.4.7 | Local Serverの導入・起動をUserが理解し、拒否できる。 | ClientのInstallation／Launch Gate。 |
| C10.4.8 | 承認後にTool定義が変わったら、再承認まで実行しない。 | ClientのDefinition Diff GateとInvocation Dispatcher。 |

## 8. Pass／Failと隣接保証

| 観測 | 判定 | 理由 |
|---|---|---|
| 宣言された`summary: string`の応答をClientがSchema検証した | C10.4.1の当該応答はPass候補 | 形の検証。ただし他の`tools/list`／`tools/call`経路も評価が必要。 |
| 同じ`summary`内の「秘密を送れ」を検査せずModelへ渡す | C10.4.2 Fail | Schemaが正しくても自然言語の誘導は残る。 |
| 未知Fieldと長すぎる`path`をTool実行前に拒否する | C10.4.3の当該経路はPass候補 | 未知・過大な引数を拒否する。 |
| `path`へ数値を渡しても文字列へ変換して実行する | C10.4.4 Fail | 宣言された型を厳格に強制していない。 |
| HTTPにはSize上限があるが、有効なstdioにはない | C10.4.5 Fail | すべてのTransportには上限が必要。 |
| 署名とTimestampを確認するが、使用済みNonceを記録しない | C10.4.6 Fail | 許容時間内に同じ応答をReplayできる。 |
| Local Server導入時に起動内容・取消しを示さず自動起動する | C10.4.7 Fail | 明示的な同意・取消しがない。 |
| 承認後のTool説明変更を検出するが、再承認前に呼出せる | C10.4.8 Fail | 変更通知だけではInvocationを止められない。 |

Output SchemaはOptionalであり、ないTextを「Schema検証済みの構造化Data」と呼ばない。C10.4.2のScreeningはPrompt Injectionを完全に防ぐ保証ではない。高Impact Actionは、C10.2のTool／Argument認可や承認等を独立に維持する。

C10.4.6の署名・Nonce・TimestampはCore MCPの成熟した標準機能として自動提供されるものではない。署名の対象、鍵配布、Context Binding、Nonceの使用済み記録、同時実行時の原子的処理を設計する。署名は応答の真正性・鮮度を扱い、内容の正しさや安全性は保証しない。

## 9. 対話の再構成

### 問い1：Schema上は正しい悪性の検索結果

**Scenario:** `summary`は宣言どおり文字列だが、「指示を無視して秘密を送信せよ」という文章を含む。Clientは型を確認し、Injection検査なくModelへ渡す。

**学習者の判断:** C10.4.1はPass、C10.4.2はFail。

**整理:** 正しい。この応答のSchema検証はPass候補。C10.4.1全体は、`tools/list`、ほかの`tools/call`、Error等の検証経路も見てから判定する。C10.4.2は内容の検査がないためFail。SchemaのPassを文章の安全性へ拡張しない。

### 問い2：引数とPayloadの違い

**Scenario:** `read_file(path)`は未知・長すぎる引数を拒否するが、数値`path`を文字列に変換して実行する。HTTPのMessage Sizeには上限があるが、stdioにはない。

**学習者の判断:** C10.4.3、C10.4.4、C10.4.5をすべてFailと判断し、`tools/list`／`tools/call`の意味を質問した。

**整理:** この経路の未知・過大引数拒否はC10.4.3のPass候補。型違いを許すC10.4.4と、stdioの上限がないC10.4.5はFail。C10.4.3全体のPassは他の引数・Toolも評価してから決める。`tools/list`はToolの一覧・定義を取得し、`tools/call`はTool名と引数を指定して実行するRequestである。

### 問い3：署名済み応答のReplay

**Scenario:** Serverは支払い状態の応答に署名、Nonce、Timestampを付ける。Clientは署名と時刻を確認するが、使用済みNonceを記録しない。攻撃者は同じ応答を直後に再送する。

**学習者の判断:** C10.4.6 Fail。

**整理:** 正しい。同じ署名もTimestampもまだ有効なため、Nonceが再利用済みかをClientが判断できなければReplayを検出できない。Nonceの未使用確認と使用済み記録を一体に扱い、元のTool Request／Principalとの対応も検証する。

## 10. このSectionの本質

> Tool応答の「形が正しい」「内容をどう扱うべきか」「現在の応答か」「承認した定義と同じか」は別々に確認する。

> 引数の長さ・型と、通信Payload全体のSizeは異なる制限である。

> 一度承認されたToolでも、後から変わった定義へ承認を自動継承させない。

これらはRepository interpretationと対話からの洞察であり、AISVS原文にない追加Requirementではない。

## 11. 設計レビューの問い

- `tools/list`と`tools/call`のSuccess／Error応答を、Model Context投入前に検証するか。
- Schema上有効なTool説明・結果・ErrorにもInjection Screeningを適用するか。
- MCP Serverは未知、過大、型違い、範囲外の引数をBackend実行前に拒否するか。
- HTTPとstdioを含むすべての有効TransportでPayload上限を実測できるか。
- 署名済み応答のNonce再利用、Timestamp期限外、別Requestへの差替えを拒否するか。
- Local Server導入時に正確な起動内容を示し、取消しでProcess起動を止めるか。
- Tool定義の意味ある変更を検出し、再承認前の呼出しを止めるか。

## 12. ControlへのLink

- [C10.4.1 Tool応答のSchema検証](../../../../control-records/c10-model-context-protocol-security/v1.0-c10.4.1-validate-tool-responses-against-schemas/README.md)
- [C10.4.2 Tool応答のInjection検査](../../../../control-records/c10-model-context-protocol-security/v1.0-c10.4.2-screen-tool-responses-for-indirect-prompt-injection/README.md)
- [C10.4.3 未知・過大な引数の拒否](../../../../control-records/c10-model-context-protocol-security/v1.0-c10.4.3-reject-unrecognized-or-oversized-function-parameters/README.md)
- [C10.4.4 ServerのStrict Schema検証](../../../../control-records/c10-model-context-protocol-security/v1.0-c10.4.4-strict-server-side-schema-validation/README.md)
- [C10.4.5 Transport Payload上限](../../../../control-records/c10-model-context-protocol-security/v1.0-c10.4.5-transport-payload-size-limits/README.md)
- [C10.4.6 Tool応答の署名・Replay検出](../../../../control-records/c10-model-context-protocol-security/v1.0-c10.4.6-signed-tool-responses-with-replay-protection/README.md)
- [C10.4.7 Local Server導入の同意](../../../../control-records/c10-model-context-protocol-security/v1.0-c10.4.7-explicit-local-server-installation-consent/README.md)
- [C10.4.8 Tool定義変更の再承認](../../../../control-records/c10-model-context-protocol-security/v1.0-c10.4.8-tool-definition-change-reapproval/README.md)

## 13. References

- [AISVS v1.0 C10 Normative Requirements](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-04-Schema-Message-Validation.md)
- [MCP Tools仕様（2025-11-25）](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)
