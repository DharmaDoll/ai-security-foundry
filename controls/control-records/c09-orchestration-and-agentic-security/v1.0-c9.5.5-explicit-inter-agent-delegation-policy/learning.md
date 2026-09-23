# C9.5.5：依頼先の能力を委任権限と混同しない

AISVS Verification Level: 2

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.5.5`。採用済みAISVS v1.0、固定Revision
`78775233666a2022dcfb82037e5e029116955c00`を使用する。

> Verify that inter-agent task delegation is restricted by an explicit authorization policy.

日本語訳：Agent間のタスク委任が、明示的な認可Policyによって制限されていることを確認する。[要件本文][normative]

NormativeはAgent間委任の明示的な認可を要求する。Researchは委任方向・相手・Scopeの制限と再委任を補足する。
[対応Research][research] 以下の構成案はRepository interpretation、対話からの言葉は学習上の洞察である。
特定のOAuth方式や製品を必須にしない。学習完了はControl成熟度・製品適合を変更しない。

## 具体例と用語

調査Agentは請求書の読取り・分析を担当する。送金Agentは承認された支払いを実行できる。
調査Agentに送金Toolがなくても、送金Agentへ自由に依頼できるなら、侵害された調査Agentから送金が可能になる。

委任は別Agentへ仕事を依頼すること、再委任は受けた仕事をさらに別Agentへ依頼すること。
Scopeは依頼で許された操作・対象の範囲。Policyは誰から誰へ何を依頼できるかを定める規則である。

資産は委任権限とその先の文書・資金。攻撃者は低権限Agentを侵害・誘導し、強いAgentの能力を利用しようとする。
Trust BoundaryはAgent間のタスク送信・受付にある。
Security Invariantは、委任や再委任によってその依頼の許可範囲を拡大できないこと。
Enforcement Pointは実行基盤や受信側の認可処理であり、直接受付・Queue経由にも適用する。

## 対話：相互認証できれば委任を許せるか

問い：固有証明書で相互認証するが、送金Agentは全ての正規社内Agentからの送金依頼を無条件に実行する。
委任元ごとのタスク認可はない。

学習者：「No」

整理：正しい。身元の確認と、その主体から仕事を受けてよいかの判断は異なる。

## 対話：強いAgentにも限定した仕事を依頼できるか

問い：調査Agentから分析Agentへ文書Aの読取り・要約だけを委任する。分析Agent自身は更新能力を持つが、
この依頼では読取りに制限する。再委任時も制限を維持し、更新要求を実行基盤が拒否する。

学習者：「はい」

整理：成立する。依頼の範囲と委任先の能力を分けて強制できている。

> 依頼先の能力が大きくても、その依頼で使ってよい権限まで大きくなるわけではない。

## 技術への具体化：OAuth Tokenで実現できるか

学習者：「どのような技術でこの制御を実現するのですか？OAuth Token？」

OAuth Access Tokenは選択肢となる。ただし発行Policyと受取側の認可を組み合わせる。
以下は構成例であり、Tokenを発行するだけでは本要件を満たさない。

1. アプリやPolicy Engineに「調査Agentから分析Agentへの文書Aの要約を許可」と定義する。
2. 信頼する認可基盤が委任元と許可条件を確認し、分析Agent向けの限定Tokenを発行する。
3. 分析Agentの受付はTokenと依頼を照合し、文書Bや更新の依頼を拒否する。
4. 文書APIを呼ぶ際も当該依頼の範囲を保ち、分析Agent自身の広い権限へ切り替えない。

```text
調査Agent → 分析Agent向けの限定Token → 分析Agent
分析Agent → 文書API向けの読取Token   → 文書API
```

AudienceはTokenの受取先を指定する情報。文書Aという対象制限はToken内の属性や、
Tokenに結び付けたサーバ側の委任記録で表現できる。scope=readだけでは対象文書までは限定できない。

OAuth 2.0 Token Exchangeは既存Tokenを提示し、下流向けTokenを取得する標準方式である。
委任を表す情報を扱えるが、導入だけでScopeが自動的に縮小したり、全委任関係が許可されたりするわけではない。
発行基盤が主体・委任先・元の委任範囲・要求ScopeをPolicyで評価する。[RFC 8693][exchange]
受取先ごとのToken制限にはResource Indicatorsも関連する。[RFC 8707][resource]

同じ信頼する実行基盤内なら、認証済みAgent ID、改変できない委任記録、受付時のPolicy評価で制御する案もある。
毎回OAuth Tokenを発行することは必須でない。Tokenや秘密値はモデルに見せず実行側で扱う。

> Tokenが許可範囲を伝え、認可処理がその範囲を守らせる。

## 検証・隣接要件・限界

Positive Testは、許可された方向・タスク・Scopeで委任が成立すること。
Negative Testでは以下を試す。

- 調査Agentから送金Agentへ未許可の依頼を送る。
- 一方向の委任許可を逆向きにも使う。
- 読取りの委任を更新要求へ変更して再委任する。
- 返信やQueue経由で新規タスクの認可を迂回する。

拒否応答だけでなく、委任先で副作用が起きないことを確認する。
C9.5.1はToolと引数、C9.5.2は利用者の認可Contextの伝播、C9.4.1は個体認証を扱う。
本要件はAgent間の依頼関係を認可するもので、相互認証や通信接続だけでは代替できない。
依頼の許可範囲内での意味的な悪用は残る。明示的な委任能力がない範囲は対象外になり得るが、
Toolの内部で子AgentへDispatchする経路も確認する。

## 設計レビューへの問い

- 誰から誰へ、どの方向・対象・操作の委任を許可するか。
- 受信側の強い権限で依頼の範囲を拡大できないか。
- 再委任・Queue・返信でも元の制限を維持するか。
- Tokenの署名検証だけで終わらず、実際の依頼内容を認可しているか。

## References

- [AISVS v1.0要件本文][normative]、[対応Research][research]
- [OAuth 2.0 Token Exchange：RFC 8693][exchange]
- [Resource Indicators：RFC 8707][resource]
- [C9 Family overview](../README.md)
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-05-Agent-Authorization-Delegation.md
[exchange]: https://www.rfc-editor.org/rfc/rfc8693.html
[resource]: https://www.rfc-editor.org/rfc/rfc8707.html
