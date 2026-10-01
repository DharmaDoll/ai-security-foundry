# AISVS Familyはシステムのどこに効くか

AISVS v1.0の12 Familyを、代表的な三つの構成に重ねた見取り図。
各枠は「そこで何を保証するか」の入口であり、要件の網羅図、製品の適合判定、
Engineering PatternとのMappingではない。同じFamilyが複数の場所に効き、
実際の適用範囲は個別Requirementと製品の構成から判断する。
名称・番号は[固定版AISVS](https://github.com/OWASP/AISVS/tree/78775233666a2022dcfb82037e5e029116955c00/1.0/en)に基づく。

## 1. Modelを作り、受け入れ、稼働させる

```mermaid
flowchart LR
    data["学習Data<br/>C1 由来・完全性"] --> lifecycle["学習・評価・変更<br/>C3 Lifecycle"]
    supplier["外部Model・依存物<br/>C6 Supply Chain"] --> lifecycle
    lifecycle --> serving["配備・推論基盤<br/>C4 Infrastructure"]
    robustness["攻撃条件での評価<br/>C11 Adversarial Robustness"] -.-> lifecycle
    robustness -.-> serving
    serving --> telemetry["監視・調査・対応<br/>C12 Monitoring"]
```

この図で問うのは、DataやArtifactを信頼できる由来から受け取り、
変更を評価してから安全な環境へ配備し、攻撃条件での弱さや運用中の異常を
見逃さないか、ということ。C11は製造工程の末尾だけでなく、変更後・運用中の
評価にも関わる。C12の監視も推論基盤だけに限定されない。

## 2. Userの質問からRAG回答まで

```mermaid
flowchart LR
    user["User"] --> identity["主体・権限<br/>C5 Access Control"]
    identity --> input["入力・取得内容<br/>C2 Input Validation"]
    input --> retrieval["検索・Memory<br/>C8 Memory / Vector"]
    retrieval --> model["Model利用"]
    model --> output["回答の検証・公開<br/>C7 Output Control"]
    output --> user
    identity -. "文書ごとの権限" .-> retrieval
    input -. "観測" .-> monitor["C12 Monitoring"]
    output -. "観測" .-> monitor
```

ここでは「質問を受け付けた」ことと「その文書を読んでよい」ことを分ける。
検索前・検索後の権限、取得内容の未信頼性、Model出力の公開判定は別の境界である。
C2で入力を検査してもC7の出力検査を省けず、C7の出力検査でC5の認可を代替できない。

## 3. AgentがMCP経由で外部Resourceを操作する

```mermaid
flowchart LR
    request["Userの依頼"] --> auth["主体・委任範囲<br/>C5 Access Control"]
    auth --> agent["計画・Tool選択・承認<br/>C9 Orchestration"]
    agent --> mcp["MCP Client / Server境界<br/>C10 MCP Security"]
    mcp --> resource["下流API・Data<br/>C5 Resource認可"]
    resource --> result["Tool結果は未信頼<br/>C2 Input Validation"]
    result --> agent
    agent -. "実行Trace" .-> monitor["C12 Monitoring"]
    mcp -. "通信・操作記録" .-> monitor
```

C9はAgentの行動・権限・停止可能性、C10はMCPを跨ぐ認証・認可・Tool/Resourceの
信頼境界を問う。MCP Serverが認証済みでも、下流Resourceへの操作が許可された
ことにはならない。Tool結果を再びAgentに渡す時も、外部入力として扱う。

三つの図はFamilyの典型的な効き所を示すだけであり、ひとつの構成で全12 Familyが
必ず適用されるという意味ではない。個別の「問うこと」と「できてはいけないこと」は
[Family別Control案内](README.md)から、正確な要件はAISVS原文から確認する。
