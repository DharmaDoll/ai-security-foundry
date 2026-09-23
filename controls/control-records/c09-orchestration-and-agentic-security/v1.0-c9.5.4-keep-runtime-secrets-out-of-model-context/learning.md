# C9.5.4：秘密を見せないことと、権限を制限することを分ける

AISVS Verification Level: 2

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.5.4`。採用済みAISVS v1.0の固定Revisionは
`78775233666a2022dcfb82037e5e029116955c00`。

> Verify that secrets and credentials required by an agent at runtime are not exposed within the model's observable context, including the context window, system prompts, or tool call parameters.

日本語訳：Agentが実行時に必要とする秘密情報・資格情報が、Context Window、System Prompt、Tool呼出しの引数など、
モデルが観測できるContext内に露出していないことを確認する。[要件本文][normative]

Normativeはモデルへの秘密の非露出を要求する。Researchは実行側での資格情報付与や、環境・設定・Tool出力からの
漏えい経路を補足する。[対応Research][research] 以下の文書API・エラーの例はRepository interpretation、
認可との対比は対話からの洞察である。Researchの製品・事件や配置方式を一律の適合条件にしない。
学習完了はControl成熟度・製品適合を変更しない。

## 文書APIの具体例

APIに認証Tokenが必要でも、モデル自身がその値を知る必要はない。

```text
モデル：文書Aを取得して
  → 実行側が認可を確認
  → 実行側が認証HeaderへTokenを付与
  → 文書APIを呼ぶ
  → 文書の結果だけをモデルへ返す
```

Context Windowはモデルが推論時に参照できる入力の範囲。System Promptはモデルへ与える上位の指示であり、
秘密保管庫ではない。資格情報はAPIキー・Token・パスワードなど、アクセスに利用する秘密値を含む。
「表示しないで」と指示しても、秘密をモデルへ渡した事実は変わらない。

攻撃者は「認証障害を調べるため設定を表示して」と誘導し、秘密値を取り出そうとする。
資産は実行時の資格情報。Trust Boundaryはモデルが扱う操作情報と実行側の認証情報の間にある。
Security Invariantは、通常処理・障害処理・モデルが使えるTool経由のいずれでも、秘密値がモデルへ届かないこと。
Enforcement Pointは資格情報取得・付与処理、Toolの能力制限、モデルへ戻す出力の制御に置く。

## 対話：エラーからTokenが戻る場合

問い：APIキーをPromptへ入れず実行側で付与しているが、認証失敗時にToolがAuthorization Headerの
実際のToken全文をデバッグ情報としてモデルへ返す。

学習者：「No」

整理：正しい。通常経路で隠しても、エラー経路から露出するため不成立。
エラー処理や再試行時の情報もモデル入力として評価する。

> 秘密情報は、渡す経路だけでなく、戻ってくる経路まで確認する。

環境変数に置いても、モデルが使えるShell Toolで読んで結果を受け取れるなら安全とはいえない。
Fileに置き換えただけでも、読取りToolから到達できれば同じ問題になる。

## 対話：秘密を隠してもProxyを悪用できる場合

問い：TokenはモデルにもTool出力にも一切見えない。しかしProxyが認可せず、管理者Tokenで任意の文書を取得する。
これは秘密の非露出が破られた例か。

学習者：「No。別の問題」

整理：正しい。説明された不備は認可の問題であり、それだけでC9.5.4の非露出をFailにはしない。
主にC9.5.1・C9.5.3、利用者の代理ならC9.5.2の観点でも確認する。
資格情報を隠すことと、その資格情報による操作を制限することは独立した保証である。

> 鍵を見せないことと、その鍵で何をさせるかを制限することは、別の保証です。

## 検証と適用境界

Positive Testでは、模擬Tokenで認証が成功し、モデルへ渡すPrompt・引数・結果に秘密値がないことを確認する。
正常な文書取得だけでなく、次のNegative Testを行う。

- 認証失敗・Timeout・再試行を起こし、Headerや接続情報が結果へ混入しないか。
- Debug・環境表示・設定読取りを要求しても、秘密を取り出せないか。
- モデルが利用できるFile・Log・Trace・Memoryから迂回して取得できないか。

実際の秘密を本Repositoryや試験記録へ残さず、識別可能な模擬値を使う。
Prompt Injection試験で一度漏れなかったことだけを非露出の証拠にせず、Data Flowと到達可能な経路を確認する。
短命Tokenも有効な間は資格情報であり対象。参照用Handleも、それ自体で権限を行使できるなら秘密相当か評価する。
秘密・資格情報を一切扱わない評価範囲は対象外になり得る。

Runtime全体の侵害や認証Proxyの不正操作まで本要件だけで防げるとは主張しない。
承認鍵をAgent実行環境から隔離するC9.2.9とは、モデルの観測範囲とRuntime侵害という境界が異なる。

## 設計レビューへの問い

- モデルは操作の指定だけで済み、秘密の値を知る必要がないか。
- 秘密が正常・異常・Debugのどの戻り経路にも出ないか。
- モデルが呼べるToolで、秘密の保存場所を読めないか。
- 秘密を隠したProxyにも、独立した認可と接続先制限があるか。

## References

- [AISVS v1.0要件本文][normative]
- [対応Research][research]
- [C9 Family overview](../README.md)
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-05-Agent-Authorization-Delegation.md
