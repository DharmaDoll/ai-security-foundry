# Engineering Patterns

## Scope

Engineering-facing entry point. Organize Pattern content under [`domains/`](domains/)
by relatively stable technologies and trust boundaries, not external Top 10 chapter
order. Threat and defense belong together inside each concrete Pattern.

## Pattern rule

A Pattern captures either a security design problem that recurs across systems or a
real attack/failure scenario that generalizes beyond one product, together with
reusable security invariants and solution principles.

Discover Pattern candidates from concrete system archetypes, assets, identities,
trust boundaries, data flows, incidents, attack paths, and recurring failure modes.
Do not generate them from a control inventory or add a document that merely restates
a framework item.

A concrete Pattern should define testable security invariants, recommend an
architecture and implementation approach, and provide verification. Mapping is a
later assessment between independently developed artifacts; an assessed no-match or
gap is valid. The canonical assessment belongs under `mappings/` and is not a
Pattern maturity requirement.

Use `templates/security-pattern.md` for new patterns.

## 設計の入口

**まず、危険や複雑さを減らせる構成を選ぶ。そのうえで、何をもとに、何を、どこでチェックするかを示す。**

利用場面から、実行場所・実行主体・資格情報を預ける相手・共有状態・公開する接続口・保守責任を比較する。
不要な権限や境界を減らせる構成を先に検討し、複雑な構成を選ぶ場合は必要性と運用負担を説明する。
ローカルなら常に安全、部品が少なければ安全とはしない。簡潔な選択表の後に一つの要求を図と例で追い、詳細な代替方式は後段へ置く。

## Patterns

### [Agents](domains/agents/README.md)

- [Agentのツール実行を、利用者の権限内に閉じ込める](domains/agents/secure-tool-execution/README.md) — `draft`（構成選択を改訂し、再レビュー待ち）。注文照会・返金の構成図、具体技術、処理例と[Negative testチェックシート](domains/agents/secure-tool-execution/negative-tests.md)。
- [社内情報を読むAgentから、顧客へ渡す情報と宛先を制限する](domains/agents/untrusted-content-to-action-containment/README.md) — `draft`。調査と下書き・送信を分け、開示する材料、確認した本文、宛先を結び付ける。[実装例](domains/agents/untrusted-content-to-action-containment/implementation-notes.md)と[正常系・Negative test](domains/agents/untrusted-content-to-action-containment/negative-tests.md)。

### [RAG](domains/rag/README.md)

- [RAG検索で、利用者に許可された文書だけを渡す](domains/rag/secure-multi-tenant-retrieval/README.md) — `draft`。会社・文書権限・キャッシュ・失効の設計と[正常系・Negative testチェックシート](domains/rag/secure-multi-tenant-retrieval/negative-tests.md)。

### [MCP](domains/mcp/README.md)

- [MCPの接続構成と、下流APIを呼ぶ主体を選ぶ](domains/mcp/audience-bound-downstream-delegation/README.md) — `draft`。ローカルの直接認証・サービスアプリ・リモート委任の選び方、資格の保持場所と[正常系・Negative testチェックシート](domains/mcp/audience-bound-downstream-delegation/negative-tests.md)。

## Navigation

- 横断的なEngineering資料と調査記録: [`docs/README.md`](docs/README.md)
- Patternを配置するEngineering Domain: [`domains/README.md`](domains/README.md)
- 段階的な開発計画とDomainの責務: [`plan.md`](plan.md)
- Pattern化前の候補比較: [`docs/pattern-landscape.md`](docs/pattern-landscape.md)
- 普遍的な候補発見手法: [`docs/pattern-discovery.md`](docs/pattern-discovery.md)
