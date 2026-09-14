# C9.3.1：Tool侵害の到達範囲を必要最小限へ閉じ込める

AISVS Verification Level: 1

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.3.1`。採用済み固定Revisionは
`78775233666a2022dcfb82037e5e029116955c00`。

> Verify that each tool/plugin executes in a least-privilege sandbox or is otherwise isolated from model operations.

日本語訳：各ToolまたはPluginが、最小権限のSandbox内で実行されるか、別の方法によって
モデルの処理から隔離されていることを確認する。[要件本文][normative]

Normativeは要件本文、Researchは補足。文書変換と遠隔APIの例はRepository interpretation、
対話からの整理は学習上の洞察である。学習完了はControl成熟度や製品適合を変更しない。

## 具体例と用語

Agentが外部PDFを文書変換Toolへ渡す。悪意あるPDFや変換Libraryの脆弱性によってTool内で
任意Codeが実行されても、Host、他Tool、Credential、別Tenantへ被害を広げない必要がある。

Sandboxは、Toolが利用できるFile、Process、Network、権限等を制限する実行環境。
最小権限は、そのToolの仕事に必要な能力だけを与えることを意味する。

| 文書変換に許可する例 | 許可しない例 |
|---|---|
| 入力PDFの読取、一時領域への書込、結果の返却 | Hostの秘密、他Toolの領域、任意通信、Runtime管理機能へのAccess |

ContainerやSandboxという製品・機能名ではなく、侵害されたToolが実際にどこまで到達できるかを
評価する。ResearchもFile・Network・Processの実効到達性と、隔離機能が使えない場合の
無隔離Fallbackを確認するよう補足する。[Research][research]

## 信頼境界と周辺要件

保護対象はHost、秘密、Model処理、他Workload、Tenant Data。Trust Boundary（信頼境界）は
非信頼入力を処理するToolと、それ以外の資源・管理基盤の間にある。
Security Invariant（守るべき性質）は、Toolが侵害されても仕事に不要な資源を操作できないこと。
Enforcement Point（強制点）はOS、Container・VM、File Mount、Network、Credential等の実効境界。

| Requirement | 問うこと |
|---|---|
| C9.1.1 | CPU・Memory・実行時間等を使い過ぎないか。 |
| C9.3.1 | Tool侵害から不要な資源や他の処理へ到達できないか。 |
| C9.5.1 | AgentがそのToolを、その引数で呼ぶ権限を持つか。 |

許可されたToolにも脆弱性や悪意はあり得る。Toolを呼ぶ認可と、Tool侵害の被害範囲を区別する。

## 遠隔API型Tool

処理本体が外部Serviceで動く場合、ローカルProcessのSandboxだけで評価しない。Agent側Credentialの
権限、接続可能なAPI・Resource、Tenant分離、外部Serviceとの責任境界を確認する。
原文にはSandbox「または別の方法による隔離」とあるため、ローカルSandboxがないだけではFailにしない。

外部Serviceだから安全とも仮定しない。外部側の分離は仕様、契約、構成、試験など確認できる証拠と
責任範囲を明示する。許可Tenant内で任意の宛先へ送信できる問題は、引数認可等で別途評価する。

## 検証と対話の再構成

Negative Test（不正や失敗条件を意図的に試す検証）では、作業領域外の模擬File、未許可Host、
管理Socket、特権起動OptionへのAccessを試す。Sandbox Backendを停止させ、通常Processへ無言で
切り替わらないことも確認する。設定表だけでなく、実際に越境できない結果を証拠にする。

**問い：文書変換ToolはDocker Container内だが、rootで動き、HostのHomeを読み書き可能でMountし、
Docker管理SocketにもAccessできる。Container利用を理由に適合と言えるか。**

学習者：「No」

整理：そのとおり。ToolからHost FileとContainer管理へ広く到達でき、必要範囲へ閉じ込めていない。
Container内のrootだけでHost rootと同一とは限らないが、広いMountと管理Socketとの組合せは
強い権限になる。構成名ではなく実効到達性を見る。

**問い：外部メールAPI型ToolにはローカルSandboxがない。一方、Credentialは特定Tenantの送信だけに
限定され、他API、Host、別Tenantへ到達できない。Sandboxがないという理由だけでFailか。**

学習者：「No？」

整理：その理解でよい。別方式で最小権限の隔離を実現し得る。ただし、記載された制限が実際に
強制され、外部Service側の責任範囲が確認できることがPassの証拠として必要。

## 洞察と設計レビューへの問い

**Toolが侵害されたと仮定し、その実効的な到達範囲を必要最小限へ閉じ込める。**

- Toolの正常動作に本当に必要なFile・Network・Credentialは何か。
- Containerや外部Serviceという名称の内側で、実際には何へ到達できるか。
- 管理Socket、Metadata Service、共有Volumeなどの迂回経路はないか。
- 隔離機構の障害時に、弱い実行方式へ自動的に切り替わらないか。

## References

- [AISVS v1.0 C9.3.1][normative]
- [対応Research][research]
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-03-Tool-and-Plugin-Isolation.md
