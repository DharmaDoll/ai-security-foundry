# AISVS C9 Orchestration and Agentic Security

対象はAISVS v1.0、固定Revision `78775233666a2022dcfb82037e5e029116955c00`。
以下は原文の代替や適合チェックリストではなく、各保証の違いを俯瞰するためのRepository interpretation。
完全な解釈と検証条件はリンク先のControl本文を参照する。

## この章で保証したいこと

C9は自律的・複数段階の行動で、権限、意図、実行量、承認、追跡可能性、停止を維持する。
正しい主体の認証だけでは、返金先のすり替え、無限の再試行、別Agentへの過大な委任、
停止後に続く下流処理を防げない。Model、Runtime、Tool、下流API、人の承認・運用機能の
境界をそれぞれ確認する。

### 隣接するC5との違い

| 観点 | C5で主に問うこと | C9で主に問うこと |
|---|---|---|
| 主体・資源 | 誰がどのDataや資源へアクセスできるか | Agentの行動・委任・実行量をどう制限するか |
| 認可 | Policy決定と権限の境界 | Toolと具体的引数、行動連鎖、実行時の継続評価 |
| 資格情報 | Scope、Audience、寿命 | Agent間委任、個体Identity、操作連鎖への結合 |
| 人の関与 | 主体の強い認証 | 高影響操作の内容確認、承認の結合、停止 |

Research上の注意：Timeout応答と実処理停止、承認画面の表示と暗号的結合、
Manifestの宣言とRuntime強制、出力Schema適合と意味内容の安全性、Trace IDと暗号的帰属、
有効なTokenと現在の認可、親Agent停止と下流停止はそれぞれ別の保証である。
特にC9.2.2は表示、C9.2.8は承認の暗号的結合、C9.3.2はTool出力形式を扱う。
Researchの追加試験案をすべて各要件の必須条件とみなさない。

## Category：C9 Orchestration and Agentic Security

| 問うこと | できてはいけないこと |
|---|---|
| 自律・複数段階の実行でも、Agentの行動を許可された、意図された、制限された範囲に保ち、人が停止できるか。 | 個々の処理が正常に見えるまま、権限・実行量・承認・追跡・停止の境界を越えて副作用が広がる。 |

## Sectionの見取り図

| Section | 問うこと | できてはいけないこと |
|---|---|---|
| [C9.1 実行予算・ループ・遮断](#c91-実行予算ループ遮断) | 個別Tool、実行全体、Agent群の消費と継続を制限・停止できるか。 | 再試行・並列・子Agentによって上限を越え、停止指示後も処理が続く。 |
| [C9.2 高影響操作の承認・可逆性](#c92-高影響操作の承認可逆性) | 人が正しい対象を承認し、その承認と影響分類を実行時まで保てるか。 | Agentが承認を迂回・偽造・再利用し、自分の制限や審査を解除する。 |
| [C9.3 構成要素の隔離・Tool制約](#c93-構成要素の隔離tool制約) | Toolの権限・入出力・外部資源・違反後の状態を実効的に制約できるか。 | 非信頼DataやTool出力が、直接強い操作能力へ到達する。 |
| [C9.4 Agent・Orchestrator Identity](#c94-agentorchestrator-identity) | Agent個体と実行連鎖、Credential、保存状態を信頼できる形で識別・保護できるか。 | 共通Identityや改ざん可能な記録により、誰が何をしたか分からなくなる。 |
| [C9.5 認可・委任・継続的強制](#c95-認可委任継続的強制) | Tool、引数、利用者からの委任を各実行時点のPolicyで制限できるか。 | モデル判断、広いCredential、古い権限、無制限な再委任で認可を越える。 |
| [C9.6 停止・安全な機能縮退](#c96-停止安全な機能縮退) | 人の停止と承認期限切れを、Agentから独立した経路で確実に反映できるか。 | 承認がない処理、推論、出力、下流処理が停止操作後も進む。 |

<a id="c91-requirement"></a>

## C9.1 実行予算・ループ・遮断

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C9.1.1](v1.0-c9.1.1-per-tool-resource-quotas-and-timeouts/README.md) | 1 | ToolごとのCPU・Memory・通信・時間等に上限を強制するか。 | Timeout応答後も実処理が続く、または一つのToolが資源を使い続ける。 |
| [C9.1.2](v1.0-c9.1.2-per-execution-cumulative-budgets/README.md) | 1 | 一回の実行に属する再帰・Token・費用等を合算して制限するか。 | 子Agent・再試行・並列呼出しを別勘定にして全体予算を越える。 |
| [C9.1.3](v1.0-c9.1.3-swarm-wide-agent-halt/README.md) | 2 | Agent群全体の活動を一つの停止操作で止められるか。 | 親だけ停止し、子・Worker・Queue上の処理が実行を続ける。 |

<a id="c92-requirement"></a>

## C9.2 高影響操作の承認・可逆性

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C9.2.1](v1.0-c9.2.1-human-approval-before-high-impact-actions/README.md) | 1 | 特権・高影響・不可逆な操作を、明示的な人の承認まで阻止するか。 | 起動時の包括同意や別APIによって、具体的承認前に実行する。 |
| [C9.2.2](v1.0-c9.2.2-complete-canonical-approval-display/README.md) | 2 | 人へ実際に実行する完全・正確な操作内容を示すか。 | 要約・切捨て・表現差により、危険な引数や対象を隠して承認させる。 |
| [C9.2.3](v1.0-c9.2.3-trusted-action-reversibility-classification/README.md) | 2 | 実副作用と復旧条件から、操作の可逆性を信頼できる根拠で分類するか。 | ToolやAgentの自己申告だけで、不可逆な操作を安全側へ分類する。 |
| [C9.2.4](v1.0-c9.2.4-enforce-reversibility-based-action-policy/README.md) | 2 | 分類に応じた阻止・承認・制限を、全実行経路で強制するか。 | 再試行・直接API・障害時に分類Policyを通らず実行する。 |
| [C9.2.5](v1.0-c9.2.5-bounded-agent-self-modification/README.md) | 2 | Agentの自己変更を許可した項目・値・有効化経路に限定するか。 | Prompt、Tool、上限、承認設定を変え、自分の制限を解除する。 |
| [C9.2.6](v1.0-c9.2.6-additive-ai-review-before-high-risk-actions/README.md) | 2 | 高Risk計画を実行前にAIで追加レビューし、決定論的Gateを維持するか。 | レビューAIの許可でPolicyの拒否や必要な人の承認を上書きする。 |
| [C9.2.7](v1.0-c9.2.7-protect-ai-action-review-from-manipulation/README.md) | 2 | レビューAIの入力・結果・経路を敵対的入力の操作から守るか。 | 審査対象の文書が審査指示・正式結果・審査省略を支配する。 |
| [C9.2.8](v1.0-c9.2.8-cryptographically-bound-single-use-approvals/README.md) | 3 | 承認を操作・要求者・Context・一回限りのnonceへ暗号的に結び付けるか。 | 正しい承認を別の金額・対象・実行先へ転用、または二重使用する。 |
| [C9.2.9](v1.0-c9.2.9-approval-issuing-key-and-credential-isolation/README.md) | 3 | 承認発行の鍵と権限をAgent Runtimeから隔離するか。 | Agentが鍵を読むか、署名APIを自由に使って自分の承認を発行する。 |
| [C9.2.10](v1.0-c9.2.10-chain-wide-highest-impact-approval/README.md) | 3 | 行動連鎖中の最大影響を、連鎖全体の承認Gateへ反映するか。 | 危険な一段を無害な複数段へ分解し、低い承認条件で実行する。 |

<a id="c93-requirement"></a>

## C9.3 構成要素の隔離・Tool制約

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C9.3.1](v1.0-c9.3.1-least-privilege-tool-execution-isolation/README.md) | 1 | 各Toolを必要最小限の権限で隔離して実行するか。 | Tool侵害からModel、Host、他Tool、不要なDataへ到達する。 |
| [C9.3.2](v1.0-c9.3.2-tool-output-schema-validation/README.md) | 1 | Tool出力を期待するSchemaに照らして検証するか。 | 欠落・余分・型違い・不正構造の出力を正常値として後段へ渡す。 |
| [C9.3.3](v1.0-c9.3.3-explicit-tool-manifest-security-requirements/README.md) | 2 | Manifestに必要権限・資源上限・出力検証要件を明示するか。 | Runtimeが何を制限すべきか宣言されず、暗黙の広い能力で動く。 |
| [C9.3.4](v1.0-c9.3.4-runtime-enforcement-of-tool-manifests/README.md) | 2 | Manifestの宣言をRuntimeの実効権限・上限・検証へ反映するか。 | 正しい宣言があっても、実行時には広い権限や未検証出力を許す。 |
| [C9.3.5](v1.0-c9.3.5-isolate-untrusted-data-processing-from-tool-capabilities/README.md) | 2 | 非信頼Dataを処理する構成要素をTool呼出し能力から隔離するか。 | Web文書等の処理だけで、外部への送信・変更・実行を起動できる。 |
| [C9.3.6](v1.0-c9.3.6-architectural-separation-of-untrusted-tool-outputs/README.md) | 2 | 非信頼Tool出力の処理とAgent操作を構造的に分離するか。 | Tool出力中の命令が、そのまま次の特権操作を決める。 |
| [C9.3.7](v1.0-c9.3.7-verify-model-named-external-resources/README.md) | 2 | Modelが示した外部資源を、承認済みRegistry等で利用前に確認するか。 | Model出力のURL、Package、Tool、Serverを未確認でInstall・実行する。 |
| [C9.3.8](v1.0-c9.3.8-automatic-tool-containment-on-policy-violation/README.md) | 3 | Policy違反を検出したToolを自動的に封じ込めるか。 | 違反を記録するだけで、同じToolが操作と副作用を続ける。 |

<a id="c94-requirement"></a>

## C9.4 Agent・Orchestrator Identity

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C9.4.1](v1.0-c9.4.1-unique-cryptographic-agent-instance-identity/README.md) | 2 | 各Agent Instanceが固有の暗号的Identityで下流へ認証するか。 | 複数Agentが共通Identityを使い、実行主体を識別できない。 |
| [C9.4.2](v1.0-c9.4.2-cryptographic-action-chain-attribution/README.md) | 2 | 各操作を実行連鎖の各段階へ暗号的に結び付けるか。 | Trace IDや編集可能なLogだけで、誰がどの段階を実行したか主張する。 |
| [C9.4.3](v1.0-c9.4.3-scheduled-agent-credential-rotation/README.md) | 3 | Agent Identity Credentialを定義した周期で更新するか。 | 一度発行した長期Credentialを更新せず使い続ける。 |
| [C9.4.4](v1.0-c9.4.4-integrity-protection-for-persisted-agent-state/README.md) | 3 | 呼出し間に保存するAgent状態の改ざんを検出・拒否できるか。 | MemoryやCheckpointを書き換え、正規状態として次回実行へ読み込ませる。 |

<a id="c95-requirement"></a>

## C9.5 認可・委任・継続的強制

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C9.5.1](v1.0-c9.5.1-fine-grained-tool-and-parameter-authorization/README.md) | 2 | Agentが使えるToolと指定可能な引数を細粒度Policyで制限するか。 | Toolが許可済みという理由で、任意の対象・金額・宛先を許す。 |
| [C9.5.2](v1.0-c9.5.2-scope-limited-user-context-through-downstream-calls/README.md) | 2 | 利用者の委任Contextを完全性保護し、各下流呼出しで強制するか。 | Agentや中継Serviceの広い権限へ置き換え、利用者の範囲を越える。 |
| [C9.5.3](v1.0-c9.5.3-application-enforced-authorization-outside-model-decisions/README.md) | 2 | Access ControlをApplicationまたはPolicy Engineで強制するか。 | Modelの「許可されている」という出力を認可判断として実行する。 |
| [C9.5.4](v1.0-c9.5.4-keep-runtime-secrets-out-of-model-context/README.md) | 2 | RuntimeのSecretやCredentialをModelの観測可能なContextから除外するか。 | System Prompt、Context、Tool引数・結果へ秘密を渡し、Model出力から漏らせる。 |
| [C9.5.5](v1.0-c9.5.5-explicit-inter-agent-delegation-policy/README.md) | 2 | Agent間の委任先・Task・権限を明示Policyで制限するか。 | 親Agentが持たない権限を子へ渡す、または子が無制限に再委任する。 |
| [C9.5.6](v1.0-c9.5.6-current-authorization-for-each-privileged-action/README.md) | 3 | 長時間Sessionでも、各特権操作を現在のBackend Policyで再評価するか。 | Session開始時の権限を保持し、失効・Role変更後も特権操作を続ける。 |

<a id="c96-requirement"></a>

## C9.6 停止・安全な機能縮退

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C9.6.1](v1.0-c9.6.1-manual-stop-of-inference-and-outputs/README.md) | 1 | 人がModel推論と出力を直ちに停止できるか。 | UIだけ閉じ、推論・Streaming・出力配信が継続する。 |
| [C9.6.2](v1.0-c9.6.2-deny-actions-after-approval-timeout/README.md) | 2 | 承認期限内に成立しない操作を阻止するか。 | 期限切れ・未回答・承認基盤障害を暗黙の許可として実行する。 |
| [C9.6.3](v1.0-c9.6.3-out-of-band-shutdown-control-isolation/README.md) | 3 | 停止指示をAgent Runtimeから隔離した別経路で強制するか。 | Agent侵害・停止拒否・同一障害によりKill-switchまで操作不能になる。 |

## 関連する洞察

個別要件の理解・設計レビューを助ける参照であり、追加要件や正式なMappingではない。

- [ControlはSystem安全性の合否ではなく、Failureを切り分ける診断軸である](../../../docs/insights/assurance-properties-are-diagnostic-lenses.md)：対象 C9.2.7。個別保証の合否と製品全体の危険性を分け、修正すべき境界を見つける。
- [Bounded Autonomyには階層ごとの上限と停止意味論が必要である](../../../docs/insights/bounded-autonomy-requires-hierarchical-controls.md)：対象 C9.1.1・C9.1.2・C9.1.3。Tool・一実行・Agent群の上限と、停止後も残る副作用を区別する。
- [Human ApprovalはButtonではなくSecurity Protocolである](../../../docs/insights/human-approval-is-a-security-protocol.md)：対象 C9.2.1・C9.2.2・C9.2.6・C9.2.7・C9.2.8・C9.2.9・C9.2.10。承認の表示・主体・操作内容・実行を結び、承認の迂回や再利用を確認する。
- [Identity、Authority、Intent、Transaction Integrityを分ける](../../../docs/insights/identity-authority-and-intent-are-different.md)：対象 C9.2.1・C9.2.8。本人性、権限、今回の意図、承認した操作との一致を分けて確認する。
- [不要なAuthorityを消し、残る全経路を完全仲介する](../../../docs/insights/minimize-and-mediate-authority.md)：対象 C9.2.5・C9.3.1・C9.3.4。不要な能力を取り除き、残した操作経路で認可を迂回できないか確認する。
- [Security Artifactは証明できる範囲を越えて信頼しない](../../../docs/insights/security-artifacts-have-bounded-claims.md)：対象 C9.3.2・C9.3.3・C9.3.4。署名・Schema・Manifest等が示せる保証を、内容や判断の安全性へ広げない。
- [Web SecurityからAgent Securityへ：ParameterではなくCapability Flowを追う](../../../docs/insights/web-security-to-agent-capability-flow.md)：対象 C9.3.4・C9.3.5。非信頼情報がAgentの権限行使へ影響する経路を、Toolや状態をまたいで追う。

個別の具体例・対話・洞察は[C9学習ガイド](../../learning/c09-orchestration-and-agentic-security/README.md)から各`learning.md`を参照する。

## 境界を跨ぐ攻撃経路から読む

以下は既存の保証を組み合わせて理解するためのRepository interpretationであり、追加要件や正式なMappingではない。
[7接点の図を含むユーザ提供メモの技術改訂版](../../../sources/user-provided/2026-10-27-agentic-seven-trust-boundaries.md)と
[Capability FlowのInsight](../../../docs/insights/web-security-to-agent-capability-flow.md)を補助資料にする。
7接点はOWASPの公式分類として確認したものではなく、C9の保証範囲とも一致しない。

例として、正規の検索Toolが返した文書に送信指示が含まれ、Agentが別Toolで外部へ送ろうとする経路を考える。
文書の受信と操作の許可は別であり、認証や検索が正常でも、正規Credentialで不正な開示が起こり得る。

| 経路上の問い | 読む箇所と保証の違い |
|---|---|
| Tool応答が次の操作へそのまま影響できないか | C9.3.2は形式、C9.3.5・C9.3.6は非信頼処理と能力・操作の分離。形式適合だけで認可しない |
| 生成された操作を誰の権限で実行するか | C9.5.1・C9.5.3・C9.5.6で対象・引数・現在のPolicyをモデル外で確認する |
| 別Agentや下流APIへ渡したときに権限が広がらないか | C9.5.2・C9.5.5で利用者Contextと委任範囲を保つ。C9.4の本人性だけで操作を許可しない |
| 高影響の操作に対する承認が実行内容と一致するか | C9.2.2・C9.2.8・C9.2.10で実内容の表示、承認との結合、行動連鎖の影響を区別する |

Memory／RAGへの保存・検索時の開示はC8・C5、入力の取扱いはC2、モデル出力の扱いはC7にも跨る。
担当者が資料を読めることと、外部の宛先へその内容を渡してよいことを区別し、隣接するData Protectionの保証も確認する。
それらをC9だけで保証したと扱わない。運用ではC9.1・C9.6の予算・停止を併せて読み、親Agent以外の処理も追う。

レビューでは開発者・運用者へ、次のように依頼する。

> 評価するRelease・環境・Policy版を指定し、検索結果の成功・Errorから次のTool実行までの図を見せてください。
> 各段階の本人・Task・委任Scopeと、宛先・対象・内容をどこで検証するかを記してください。
> 正常な操作が成功し、Schema適合の不正な宛先や権限外委任が実行側で拒否された記録を、模擬Dataで示してください。

図と設定は設計上の強制点を、拒否記録と下流の状態・受信記録は試験条件下で副作用を止めたことを示す。
モデルの拒否応答だけなら、同じ実行境界へ不正要求を直接与えた結果と、迂回経路から副作用がないことを追加確認する。
証拠がなければ未確認と記録する。これは製品横断のレビュー例であり、一つのControlの合否へ全条件を押し込まない。

## Source

- [AISVS v1.0 C9要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)

## MITRE ATLASとの対応

[Content 2026.10の対応評価](../../atlas-mapping-review-2026-10.md#c9)で、対象Requirement・攻撃経路・対応の限界を確認できます。Mappingは`proposed`で、Family全体の網羅や製品適合を意味しません。
