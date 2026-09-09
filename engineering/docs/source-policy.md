# Engineering Source and Mapping Policy

## Framework Sources and Mapping Assessment

Frameworks provide evidence and context for engineering decisions.

Relevant sources may include:

* OWASP AISVS;
* MITRE ATLAS;
* OWASP GenAI LLM Top 10;
* OWASP Agentic Top 10;
* OWASP MCP Top 10;
* OWASP Agentic Skills Top 10;
* OWASP AI Exchange;
* relevant primary technical specifications.

Mappings are secondary outputs.

They are derived only after a Pattern and the other endpoint have each been
developed independently. Do not use a control inventory or framework coverage gap
to discover Pattern candidates.

Threat-taxonomy content is different from coverage-driven generation. Techniques,
procedures, and case studies may supply evidence of attacker behavior and recurring
attack paths during Pattern discovery. Analyze their technical content first; record
identifier relationships as Mappings only after the Pattern boundary is stable.

The engineering pattern must remain understandable without requiring the reader to interpret the external framework first.

Do not invent mappings for completeness.

A single pattern may map to multiple controls, threats, or risk categories.

Mappings should be based on technical rationale, not keyword similarity.

## 補完ソースの共通採用方針

外部資料は活用するが、本PJの判断は委ねない。以下は必須の依存・準拠対象ではなく、
具体的な問題から独立して育てるPatternを深めるための補完ソースとする。
利用方針は共通化するが、リスク分類・技術仕様・評価手順という情報源の役割は区別する。

| ソース | 主な利用方法 |
|---|---|
| OWASP GenAI LLM Top 10 | LLMアプリ全般の基本的なリスクや失敗経路を検討する観点 |
| OWASP Top 10 for Agentic Applications | Agentの行動・委譲・連携に関するリスクや失敗経路を検討する観点 |
| OWASP MCP Top 10 | MCP固有の信頼境界・悪用シナリオを検討する観点 |
| OWASP Agentic Skills Top 10 | Skillsの導入・権限・更新などのリスクを検討する観点 |
| [OWASP Agent Control Standard (ACS)](https://github.com/GenAI-Security-Project/agent-control-standard) | 実行時制御、判断と実行の接続、追跡、構成情報を扱う設計の参考 |
| [OWASP Secure Agent Playbook](https://github.com/OWASP/secure-agent-playbook) | 分析・レビュー手順、攻撃経路の見落とし確認、Negative testの問いの参考 |

LLM Top 10はLLMアプリ全般の基本的なリスク観点として活用し、Agentic / MCP / Skills
Top 10はそれぞれ固有の観点を補う。ただし、各Top 10を厳密な親子分類とは扱わず、
重複や適用範囲の違いを個別に評価する。AISVSは引き続きcontrolsの主軸とする。

### Patternを育てる際の使い方

1. 実ユースケース、Trust Boundary、Abuse Caseから問題を定義する。
2. 関連するリスク記述・仕様・Playだけを参照し、失敗経路、設計の選択肢、
   不足している検証観点を補う。
3. 得られた知見を、本PJのSecurity Invariant、決定論的なEnforcement Point、
   Positive / Negative test、運用条件、限界へ翻訳する。
4. 採用した箇所には上流の該当節と版または参照コミットを記録し、上流の説明と
   本PJの解釈を区別する。引用元の規格ID・要件・Mappingは一次資料で確認する。
5. ControlsやFrameworksとのMappingは、独立した内容が理解できてから別途評価する。
   単なる参考文献の追加はMappingの成立を意味しない。

Top 10の記述から着想を得ることもできる。ただし「項目があるから作る」のではなく、
そこで示された失敗が、どのシステムで、どの境界を越えて、なぜ繰り返されるのかを
分析する。Pattern候補にする際は具体的なシナリオと再利用可能性を示し、既存Patternに
統合できないかを検討する。Top 10の項目数や分類をPatternの数・構造に置き換えない。

各ソースの公式URL、版、成熟状態は`../../sources/registry.yaml`を参照し、実際の利用時に
上流を確認する。補完ソースという共通扱いは、beta・public-review・stableなどの
状態差をなくすものではない。今回の方針変更だけで台帳の確認日や状態を更新しない。

例えばPlayの「Agentが自身の権限を変更できないか」という問いは、
「Agentの資格情報で認可ポリシーの変更を試み、要求が拒否され、設定が変わらないことを
確認する」というテストへ具体化する。実行していないテストを検証済みとは記録しない。

### 採用しないもの

- Top 10の項目、仕様の章、チェック項目ごとのPattern量産、専用カテゴリへの再編、網羅率の目標化。
- Top 10の網羅、ACSへの適合、Playbookの実行、Mappingの成立を、
  安全性・Pattern成熟・検出網羅性の保証や必須条件とすること。
- 上流の既定値、リスク評価、推奨構成を、対象システムの条件を検証せずに採用すること。
- 外部skills、plugins、実行指示の自動導入・実行。文書参照と実行許可を混同しない。
- 上流仕様・スキーマ・手順集の丸ごとの複製。参照を優先し、翻案時はライセンスを確認する。

Patternの本体は補完ソースを読まなくても理解・検証できるものとする。
ACS固有の実現方法を紹介する場合も、一般的な安全性の原則とは分ける。
参照しないことも有効な判断であり、全Patternに利用や不採用記録を義務付けない。
AISVSを主軸とするcontrolsの意味や成熟条件は、この採用によって変更しない。

将来のAgent支援による脅威モデリングでも、Playbookは調査・報告手順の参考にできる。
その実装や有効性評価は別タスクとし、今回の情報源採用を実行承認とは扱わない。

## Controls and Engineering Are Independent Domains

`engineering/` answers:

"How should we design, implement, and verify this securely?"

`controls/` answers:

"What security property should be assured and how should it be evaluated?"

Neither domain is subordinate to the other.

Do not:

* generate engineering patterns only because a control exists;
* restructure engineering categories to mirror control families;
* modify controls merely to match an implementation;
* claim that one engineering pattern fully satisfies a control without sufficient evidence.

Use explicit mappings to connect the two domains.

Mapping success is not a Pattern maturity requirement. Record an assessed no-match
or gap when no defensible relationship exists.

If engineering work reveals a missing or unclear control mapping, record the gap for follow-up.

## Sources and Current Guidance

AI security changes rapidly.

Before making claims that depend on current specifications, security guidance, or framework content:

1. identify the authoritative source;
2. verify the relevant version or publication status;
3. prefer primary sources;
4. distinguish stable guidance from drafts or public-review material;
5. record significant version dependencies.

Do not silently treat historical guidance as current.

Avoid copying large sections of external source material into this repository.

Prefer references, concise interpretation, and original engineering guidance.
