# C9.3.4：ManifestのSecurity契約をRuntime制約へ変換する

AISVS Verification Level: 2

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.3.4`。採用済み固定Revisionは
`78775233666a2022dcfb82037e5e029116955c00`。

> Verify that the runtime enforces the privileges, resource limits, and output-validation requirements declared in tool manifests.

日本語訳：Runtimeが、Tool Manifestに宣言された権限、資源制限、出力検証要件を強制していることを
確認する。[要件本文][normative]

Normativeは要件本文、Researchは補足である。文書変換Toolの例、保証境界、隣接要件との整理は
Repository interpretation、対話からの整理は学習上の洞察である。学習完了はControl成熟度や
製品適合を変更しない。

## 平易な説明

C9.3.3で作ったManifestを説明書のままにせず、Toolが破れない実行制約へ変換するRequirementである。

例えば文書変換Toolが次を宣言するとする。

```yaml
privileges:
  filesystem:
    read: ["/input"]
    write: ["/output"]
  network: deny
resources:
  timeout_seconds: 30
  memory_mb: 512
output:
  schema: "document-result-v1"
  max_bytes: 1048576
```

Runtimeは宣言を、Filesystem Sandbox、Network Policy、Process終了を伴うTimeout、Memory上限、
出力Validator等へ対応付ける。設定が存在するだけでなく、制限を越えた操作が実際に拒否・停止されることを
確認する。

## Trust BoundaryとEnforcement Point

主なTrust Boundaryは次の三つである。

1. Manifestと、Runtimeが生成・採用する実行設定の間。
2. Tool Processと、Host・Filesystem・Network・他Processの間。
3. Tool出力と、その出力を利用するAgentやApplicationの間。

Security Invariant（守るべき性質）は、ToolがManifestで宣言した範囲より広い能力を、通常経路でも
侵害時でも利用できないことである。

| 宣言 | 主な決定論的Enforcement Point |
|---|---|
| File権限 | Mount、Filesystem Policy、OS／Sandbox権限 |
| Network権限 | Network Namespace、Firewall、Egress Policy、強制Proxy |
| CPU・Memory | Runtime Quota、cgroup等の資源制御 |
| 実行時間 | RuntimeのTimeoutと実Processの終了 |
| 出力契約 | Consumerが利用する前のSchema・Size Validator |

Runtimeが理解できない宣言、壊れたManifest、Version不一致、制約設定の失敗時に、広い既定権限で
起動してはいけない。必要な制約を強制できないなら実行を拒否する、Fail closedが基本となる。

## 隣接Requirementとの違い

| Requirement | 主に問うこと |
|---|---|
| C9.3.1 | Toolへ与える実権限そのものが必要最小限か |
| C9.3.3 | 必要権限・資源上限・出力検証要件がManifestに宣言されているか |
| C9.3.4 | RuntimeがManifestの宣言どおりに制約を強制しているか |

Manifestが過剰な権限を宣言し、Runtimeが忠実にその権限を与える場合、C9.3.4単独ではPass候補になり得る。
しかしC9.3.1はFailとなり、System全体は危険である。

**契約への忠実さと、契約そのものの安全性は別である。**

## 検証と対話の再構成

Negative Test（制限違反を意図的に試す検証）では、未宣言Pathや外部Networkへのアクセス、CPU・Memory・
時間上限の超過、Schema外出力、Manifestの差替え、未対応Field、読込み障害を直接試す。正常時に違反が
偶然発生しなかったことは、制約が強制されている証拠にならない。

**問い：RuntimeはSchema違反を記録するが、違反出力をそのままAgentへ渡す。適合するか。**

学習者：「Fail」

整理：そのとおり。記録は検出であって強制ではない。違反出力がConsumerへ渡る前に拒否し、安全なErrorとして
扱う必要がある。

**問い：新しいManifestは外部Network接続禁止を宣言した。古いRuntimeはそのFieldを理解できず、警告だけを
出してNetwork接続可能な状態でToolを起動する。適合するか。**

学習者：「Fail」

整理：そのとおり。未対応制約を無視して広い能力で起動するFail openであり、宣言を強制していない。

**問い：ManifestはHost全体へのRead／Write、任意のNetwork、非常に大きな資源上限、緩い出力Schemaを明示し、
Runtimeはその内容を完全に強制する。C9.3.4単独では適合するか。**

学習者：「Pass」

整理：C9.3.4単独ではPass候補。ただし権限が必要最小限でないためC9.3.1はFailとなる。個別RequirementのPassを
Systemの安全性へ拡大解釈しない。

**問い：ManifestはNetwork接続禁止を宣言する。Agent用Gatewayは外部通信Toolの呼出しを拒否するが、
文書変換ToolのProcessにはInternetへの直接経路が残る。適合するか。**

学習者は当初Passと判断した。主体が必ずGatewayを通ることが強制されている前提で考えたためである。

整理：設問のようにProcessの直接経路が残るならFail。Gatewayが制限する正規のTool呼出し経路と、侵害された
Processが利用できるNetwork能力は別である。一方、FirewallやNetwork Policyによって全通信が必ずGatewayを
通り、GatewayがDefault Denyを強制するなら、Network制約についてはPass候補となる。前提を明示すると判断が
変わる好例である。

## Agent化しないという設計判断

学習者は、文書変換ToolをAgent化しない設計にすべきだと指摘した。これは不要な自律性、Model判断、Tool能力を
増やさないという意味で有効である。定型処理は狭い入出力契約を持つ決定論的Toolとして実装する方が、考慮する
状態と攻撃経路を減らせる。

ただし、Agent化しなければSandboxが不要になるわけではない。悪意ある文書によってParser等が侵害されれば、
通常のProcessでもFile窃取や外部送信を試みられる。

**Agentにしないことで不要な自律性を減らし、Sandboxで残った実行能力を制限する。**

## C9.3.3との実装上の一体化

C9.3.3とC9.3.4はControl上のFailureを診断するため分離されているが、実装・運用では一つのPipelineにできる。

```text
Manifest登録
  -> 必須宣言とVersionの検証
  -> 採用Policyによる審査
  -> Runtime制約の生成・適用
  -> Negative Test
  -> 宣言と実構成のDrift検出
```

この構成なら、宣言だけをCompliance evidenceとして扱うことを避け、契約と実効制御を継続的に結び付けられる。

## 洞察と設計レビューへの問い

- Manifestの各宣言に、実際のEnforcement Pointが一つ以上対応しているか。
- 正規のAgent経路だけでなく、Tool Process自身の能力を制限しているか。
- Timeout応答後に実Processや下流処理が継続していないか。
- 未対応Field、Manifest破損、制約設定失敗時に実行を拒否するか。
- 正常試験だけでなく、制限を破ろうとするNegative Testを実施しているか。
- C9.3.4のPassを、Manifestの最小性やSystem全体の安全性と混同していないか。
- Agent化する必要のない定型処理へ不要な自律性を持たせていないか。

## References

- [AISVS v1.0 C9.3.4][normative]
- [対応Research][research]
- [C9 Family overview](../README.md)
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-03-Tool-and-Plugin-Isolation.md
