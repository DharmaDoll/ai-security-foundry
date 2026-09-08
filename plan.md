# Initial Plan

Keep the repository small until the pattern format and maintenance workflow are proven.

## Phase 0 — Repository foundation

- [x] Define repository mission and two-entry-point model
- [x] Define engineering taxonomy
- [x] Define external source roles
- [x] Create source registry
- [x] Create Codex/agent operating policy
- [x] Create security-pattern template
- [x] Create upstream-update review template
- [ ] Choose repository license
- [x] Define ownership/reviewer policy for `recommended` status

## Phase 1 — Prove the pattern model

Build a small set of high-value patterns before expanding coverage.

These candidates come from recurring system security problems and attack scenarios,
not from framework or control coverage targets.

- [ ] `agents/secure-tool-execution`
- [ ] `rag/secure-multi-tenant-retrieval`
- [ ] `llm/indirect-prompt-injection-containment`
- [ ] `mcp/secure-server-authorization`
- [ ] `skills/secure-skill-onboarding-and-updates`

For each pattern:

- [ ] Threat model is explicit
- [ ] Security invariants are testable
- [ ] Insecure/failure design is shown
- [ ] Recommended architecture is shown
- [ ] Minimal implementation example exists where useful
- [ ] Negative/abuse test exists
- [ ] Observability guidance exists
- [ ] Source versions/maturity are recorded

## Phase 2 — Maintenance workflow

- [ ] Assess mappings separately after independently developed endpoints are reviewable
- [ ] Asserted mappings have technical rationale, strength, and source-state metadata
- [ ] Preserve explicit no-match and gap outcomes without changing endpoint maturity

- [ ] Validate the source-registry schema after first real framework update
- [ ] Define a machine-readable mapping schema only after pattern metadata stabilizes
- [ ] Add a scheduled upstream-change detector
- [ ] Make the detector create an issue/report rather than directly modifying guidance
- [ ] Add semantic-diff/impact-analysis workflow for standards updates
- [ ] Add stale-review reporting based on `last_reviewed`

## Phase 3 — Expand engineering coverage

- [ ] Agent identity and credentials
- [ ] Memory poisoning and integrity
- [ ] RAG corpus ingestion and poisoning
- [ ] Sensitive-data handling and output controls
- [ ] AI/model/software supply-chain integrity
- [ ] Sandboxing and code execution
- [ ] Inter-agent communication
- [ ] AI security logging and incident evidence
- [ ] Model/provider boundary and fallback behavior

## Phase 4 — Developer adoption

- [ ] Add a concise secure-design checklist
- [ ] Add architecture-review examples
- [ ] Add CI examples for security regression tests
- [ ] Add discoverability index by use case
- [ ] Add discoverability index by framework
- [ ] Track adoption/feedback without turning framework coverage into the primary KPI

## Future application — Agent-assisted threat modeling

Status: planned / backlog。Repositoryの知識が充実した段階で、実際のSystem設計を入力に、
Agentが脅威モデリングと検証計画の作成を支援する応用を検討する。
まず既存のControlsとEngineering Patternを独立して育て、少数の具体的な構成で有用性を試す。
この計画の追加は、ツールの実装開始や現在の知識開発の優先順位変更を意味しない。

### 目的と知識の利用方法

設計上の見落としを減らし、何を検討し、何が未確認かを説明できる分析を目指す。
Frameworkの項目消化率やPattern数を、Systemの安全性や分析の完全性の証明にはしない。

- Engineering Pattern: 実際のUse Case、Trust Boundary、Attack Pathに合う設計問題と解決原則を参照する。
- STRIDE: 構成要素とData Flowを、なりすまし、改ざん、否認、情報漏えい、サービス拒否、
  権限昇格の観点から系統的に問い直す。脅威を発見する方法として用い、Control標準とは扱わない。
- MITRE ATLAS: AIに関する攻撃者の戦術・技術・事例から、攻撃の前提、経路、影響を具体化する。
  対象Systemで成立する条件を確認し、技術名が似ているだけで適用しない。
- 業務固有のAbuse Case: 正規権限の悪用、承認回避、取引上限の分割回避等を、業務ルール、
  利用者の意図、許容損失から検討する。既存分類に載っていなくても分析対象とする。
- Controls: 独立したSystem分析の後に、適用可能な保証要件の見落としを点検する。
- Negative Test／Evidence guidance: 各Security Invariantを検証できる操作、期待結果、必要証跡へ翻訳する。
- Mappings: 理解済みの関係を根拠として参照する。Mappingがないことを安全または対象外と解釈しない。

Control一覧からPattern候補やSystemの脅威を機械的に生成しない。既存知識へ一致しない
System固有の脅威も扱い、知識不足を明示する。学習ノート由来の洞察は探索の補助とし、
要件の確定や検証済みEvidenceの代替にはしない。

Repository内の知識だけで分析を完結させない。対象Systemの設計・実装・運用情報を基礎とし、
必要な一次仕様、攻撃事例、外部知識を追加参照する。参照する版と根拠を記録し、外部知識の
更新は既存のSource verification／maintenance方針に従う。

方法の参考: [Microsoft STRIDE](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)、
攻撃知識の参照先: [MITRE ATLAS](https://atlas.mitre.org/)。

### 想定する分析と出力

1. 構成図、Use Case、Data Flow、Identity、権限、外部Service、運用条件を入力として整理する。
2. Asset、Tenant、Trust Boundary、攻撃者能力を特定し、不明な構成や前提を質問する。
3. 通常処理に加え、非同期処理、再試行、Cache、Export、削除、障害、復旧を追う。
4. STRIDEで各構成要素・経路を問い直し、ATLASの攻撃手法・事例と業務固有のAbuse Caseで
   攻撃経路を具体化する。分類に一致しない脅威や複数段階の攻撃も記録する。
5. 発見した脅威を原因、攻撃者能力、経路、影響で比較して統合する。同じ脅威が複数の
   分類・資料に現れても発見件数を増やさず、一つの記録へ根拠を結び付ける。
   異なる経路や必要対策まで同一のカテゴリ名だけで統合しない。
6. 各脅威にSecurity Invariantと決定論的なEnforcement Pointを示し、関連Patternを使って
   対策・検証へ翻訳する。その後Controlsで保証の抜けを点検し、適用外、未確認、知識Gapを示す。
7. Positive／Negative Testの条件、操作、期待結果と、判断に必要なEvidenceを提示する。
8. 人が修正できる脅威モデル、優先順位付き対策、検証計画、未解決事項を出力する。

分析対象の構成・Revisionと、参照した資料のVersion・成熟度・根拠箇所を残す。
観測事実、入力された主張、Agentの推論を区別し、提案したTestを実行済みと表現しない。
初期版は設計支援を対象とし、外部Systemへの診断・変更は別途明示的な依頼を必要とする。

### 段階的なロードマップと評価

- [ ] 適用条件、必要な構成情報、保証範囲、Negative Testが明確な少数の資料を選ぶ。
- [ ] 複数TenantのRAG等、一つの具体的なSystemで手動の脅威モデリング参照例を作る。
- [ ] 同じSystemに対し、既存資料の検索と根拠付き分析を行う最小のAgent試作を評価する。
- [ ] 同じ入力でRepository単独とSTRIDE・ATLAS併用を比較し、追加発見、見逃し、誤検出、
  重複、分析負荷を測る。一般的な脅威、AI攻撃、業務固有の悪用を評価例に含める。
- [ ] 既知の設計不備を埋め込んだ例と安全な例で、見逃し、誤検出、適用判断、質問の有用性を比較する。
- [ ] 人のレビューで追加発見された脅威と、根拠のないMapping・適合断定を評価する。
- [ ] 構成情報が欠ける例で、不明点を安全とみなさず未確認として報告できることを確認する。
- [ ] 通常・障害・復旧等の経路とTrust Boundaryごとに、検討済み／未確認を追跡する。
- [ ] 一つの構成で有用性と保守性を確認してから、Agent、MCP等の構成へ段階的に広げる。

成功基準は、根拠付きで現場の設計判断と検証を改善し、未確認範囲を可視化できること。
網羅性は対象Systemと評価用シナリオの範囲内で示し、未知の脅威を含む完全性は主張しない。
