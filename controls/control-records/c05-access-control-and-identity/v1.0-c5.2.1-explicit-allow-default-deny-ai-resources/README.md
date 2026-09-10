---
title: "Explicit Allow and Default Deny for AI Resources"
versioned_id: "v1.0-C5.2.1"
requirement_id: "C5.2.1"
verification_level: 2
family_id: "C5"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-02-AI-Resource-Authorization-Classification.md"
last_verified: "2026-09-08"
maturity: "verifiable"
mapping_assessment_refs: []
---

# AI Resourceへの明示的な許可とDefault Deny

AISVS Verification Level: 2

初めて読む方へ：[具体例・用語・対話を含む学習ノート](learning.md)。

## Upstream basis

AISVS `v1.0-C5.2.1`、Verification Level 2を解釈する。
原文は、AI Resource全体について、明示的な許可と、許可がなければ拒否するアクセス制御を求める。
対象例はDataset、Endpoint、Vector Collection、Embedding Index、Compute Instanceである。
参照先はMetadataの固定Revisionであり、将来の版を取り込むものではない。

同RevisionのC5.2 Research（Last Researched: 2026-07-14）の該当行も確認した。
ResearchはResource棚卸し、匿名・低権限・Service Account等による検証、
通常のUI以外の経路での強制確認、判断の追跡情報を補足する。
これらは検証設計の参考であり、特定製品、Policy Engine、ログ形式を必須にはしない。
Research中の個別CVE、製品Version、外部Framework Mappingは本Controlへ転載・採用しない。

本書のSecurity Property、試験条件、適用境界は原文を実務へ翻訳したRepository interpretationである。
OWASP Authorization Cheat Sheetは一般的な認可設計の補足として参照する。

## Interpretation

**誰が、どのResourceに、何を、どの条件で行えるかを明示し、その許可に一致しない
アクセスを、どの到達経路からも実行させない。**

Allow-listは固定された名前一覧に限定しない。役割に基づく許可、属性に基づく許可、
検証可能な権限証票などでも、許可条件が明確で、その他が拒否されればよい。
必要な属性は用途による。すべてのResourceへTenantや時刻の条件を機械的に要求しない。

例えば、検索用Serviceには指定CollectionのQueryだけを許可し、WriteやDeleteは許可しない。
同じServiceでも別Collectionへのアクセスには別の適用可能な許可が必要になる。

Resource自身の認可機能でも、外部の認可Proxyでも実現できる。
外部で強制するなら、許可判断を通らない経路でResourceを操作できないことが必要である。

## Security objective

未管理のAI Resource、暗黙の許可、認可の迂回による情報漏えい・改ざん・不正実行を防ぐ。
認証済み、社内ネットワーク内、Agentからの呼出し、といった事実だけで包括的に許可しない。
許可条件を定義することと、それをすべてのアクセスへ強制することを一組として扱う。

## Applicability

AI SystemのData、Model Artifact、推論・管理Endpoint、Vector Store、Embedding Index、
Tool、Cache、計算Job等への読取・変更・実行・管理に適用する。
Backup、Snapshot、Export等が同じ保護対象への別経路になる場合も含める。
内部環境、単一Tenant、Service間通信でも認可境界が不要になるわけではない。

### Non-applicability

評価対象に存在せず、そのSystemから利用もしないResource種別は対象外とできる。
単に「機密情報がない」「Cloud提供者が管理する」だけではControl全体を対象外にしない。
外部提供者が強制する範囲は、責任分界と依存する保証を記録する。

公開Datasetの匿名Readは、公開対象と操作を明示した許可として扱える。
これはDefault Allowではなく、限定した公開Ruleである。Writeや管理操作まで公開しない。

## Scope and assumptions

- Resourceの範囲、実際の操作、アクセス経路、Policyの管理主体を特定できることを前提とする。
  棚卸しは検証の出発点であり、それ自体がアクセスを止めるEnforcementではない。
- 認証が必要な許可では、呼出元のIdentityと属性が信頼できる経路から得られる必要がある。
  PromptやRequest内の自己申告Roleだけでは許可を成立させない。
- Resource名、Alias、Path等が実際に操作される対象へ正しく解決されることを確認する。
- 明示的な広い許可と暗黙のDefault Allowは区別する。ただし、単なるAllow-allで安全と
  結論せず、対象と目的を説明できるかを確認し、過大権限は別の設計上の問題として残す。
- 原文はPolicy Cacheの寿命や失効伝播時間を指定しない。採用する場合は、許可の有効条件と
  更新・失効の扱いを定める。無期限の古い判断を障害時の代替許可にしない。

## Assets, actors, identities, and trust boundaries

社内RAGの例では、保護対象は文書Collectionとその読取・変更機能である。
呼出元には検索Service、取込Service、管理者、侵害された別Workloadが存在する。
Workloadは、実行中のApplicationやJobなどの単位を指す。

通常は認可Gatewayを経由するが、侵害された別Workloadが内部PortからVector DBへ
直接接続できれば、GatewayのRuleだけでは文書を守れない。

- **PDP（Policy Decision Point）:** 許可条件を評価する場所。
- **PEP（Policy Enforcement Point）:** 判断を実際の読取・変更・実行へ強制する場所。
- **Trust Boundary:** 呼出元とResource、自己申告の入力と信頼する認可情報、
  Policyを変更できる管理主体と通常の利用主体の境界。

同じ条件を認可しても、検査したCollectionと実際に操作するCollectionが違えば保証は破れる。
入口の認可成功ではなく、最終的なResource操作まで判断の対象が一致することを確認する。

## Required security properties

| ID | 必要な性質 | 観測できる成立条件 |
|---|---|---|
| SP-1 | 許可の明示 | Resource、操作、主体または公開対象、必要な条件が特定でき、正規アクセスを適用Ruleへ追跡できる |
| SP-2 | Default Deny | 一致する有効な許可がない、または必要な判断材料を検証できない場合、操作が実行されない |
| SP-3 | 全経路での強制 | UI以外のAPI、直接接続、管理、Batch、Export等も適用する認可境界を迂回できない |
| SP-4 | 判断と操作の結び付け | 許可した主体・操作・対象・条件が実際の操作と一致し、入力の差替えで許可範囲を広げられない |
| SP-5 | 作成・変更・障害時の維持 | 新規ResourceやPolicy未設定状態で暗黙に公開されず、障害で無制限許可へ切り替わらない |

SP-3はComplete Mediation、すなわち保護対象へのアクセスが必ず認可で仲介される性質である。
各アクセスの有効な許可が確認できればよく、毎回リモートPDPを呼ぶTopologyは要求しない。

## Scope calibration and adjacent assurance

| 状況 | 本Controlの評価 | 別途必要な判断 |
|---|---|---|
| Gatewayは拒否するが別Portから無認可で読める | Fail | SP-3の迂回 |
| 空のAllow-listを「制限なし」と処理する | Fail | SP-2の不成立 |
| 公開Datasetの匿名Readだけを明示的に許可し、その他を拒否する | Pass候補 | 公開判断の妥当性、書込・計算資源の保護は確認する |
| 意図した隔離状態として許可集合を空にし、全操作を拒否する | Pass候補 | 隔離のPolicyと実動作が一致すること |
| 稼働用Ruleの登録漏れで正規利用者も全員拒否される | 完成したControlのPassを裏付けない | 安全側の拒否は成立するが、意図した許可の実装は未完了。漏えいとは別の不備 |
| 中央PDP停止中も、整合性と有効性を検証したローカルPolicyで範囲内の操作を許可する | Pass候補 | 障害そのものではなく、許可の根拠が維持されるかで判断する |
| 広いService権限は明示的で、他の呼出元は拒否されるが、RAGがEnd-user権限を失う | C5.2.1にはPassし得る | C5.2.2が扱う代理実行の問題。System全体は安全ではない |

## Threat and failure-mode rationale

想定する攻撃者は、匿名Caller、正規の低権限利用者、侵害されたServiceやAgentである。
通常の認可管理権限は持たず、到達できるAPIやResource識別子、操作引数を変更できるとする。

代表的な失敗は、未登録のCollectionが公開される、Read権限でDeleteできる、
Gatewayを迂回する、空Policyや評価エラーをAllowと解釈することである。
結果としてData漏えい、ModelやIndexの改ざん、計算Jobの不正実行が発生する。

Prompt Injectionは操作を誘導する入口になり得るが、認可欠落そのものの定義ではない。
本改訂では、これらを適切な粒度で表す外部脅威IDの有用なMappingを確定していない。
単語の類似からATLAS等への関係を主張せず、`threat_mappings`は空とする。
脅威・攻撃者能力・失敗条件の記述は、Mappingの有無とは独立して維持する。

## Verification

### Architecture and configuration review

1. 実DeploymentからResourceと全アクセス経路を列挙し、設計上の一覧と突き合わせる。
2. Resourceごとに主体、操作、許可条件、Policy管理元、PDP、PEPを対応付ける。
3. 公開Rule、Wildcard、管理者Rule、継承Rule、空Policyの実際の意味を確認する。
4. 内部Port、管理API、Batch、Backup、再試行、障害時の代替経路を追う。
5. 判断材料の信頼元、対象の解決、Policy変更とCache失効の条件を確認する。

検証は許可された試験環境と模擬Dataで行う。実顧客のDataや認証情報を試験用に持ち込まない。

### Positive verification

検索ServiceにはCollection AのQuery、取込ServiceにはAのWriteを許可する。
同じRequestの操作前後を観測し、それぞれが意図した操作を成功させ、適用Ruleへ追跡できることを確認する。
公開Readや隔離状態がある場合も、意図したPolicy状態を別々に検証する。
これは許可された操作の成立を確認する試験であり、単なるHTTP成功応答の確認ではない。

### Negative and abuse-case verification

| ID | 試験 | 期待結果 | Property |
|---|---|---|---|
| N-1 | 許可のない主体・匿名Callerから保護対象を操作する | Dataも操作権限も取得できず、副作用も発生しない。公開Readの明示Ruleは別扱い | SP-1, SP-2 |
| N-2 | 検索ServiceでWrite/Delete、未許可Collection BのQueryを要求する | 別操作・別対象が拒否される | SP-2, SP-4 |
| N-3 | 必要なRole、Tenant等を欠落・偽造し、対象IDやAliasを差し替える | 自己申告や検査対象と実行対象の不一致で許可を広げられない | SP-2, SP-4 |
| N-4 | 内部Workloadから直接Port、別API、管理・Export経路へアクセスする | その経路の有効な許可がなければResourceを利用できない | SP-3 |
| N-5 | 新規Resourceを作り、Allow未設定・空Policy・未知の操作を試す | 暗黙のAllowや継承による意図しない公開がない | SP-2, SP-5 |
| N-6 | 判断に必要なPolicyを破損・取得不能にし、有効な代替判断も利用不能にする | Fail closedとなり、無制限アクセスや広い代替Credentialへ切り替わらない | SP-2, SP-5 |
| N-7 | Grantを削除し、許可の有効条件が失われた後に再試行・Cache・既存Sessionを利用する | 失効条件に従って操作が拒否され、古いAllowを無期限に再利用しない | SP-4, SP-5 |

拒否応答だけでは足りない。読取内容、変更後の状態、Job受付等を確認し、拒否前に副作用が
発生していないことを確かめる。共通PEPの試験は再利用できるが、経路ごとの強制確認は省略しない。

### Failure conditions

SP-1からSP-5に反するアクセス成功、判断対象と操作対象の不一致、暗黙のAllow、
迂回経路、根拠を失った許可の継続はControlの不成立を示す。

一方、経路や適用Policyが不明、必要な試験が未実施といった証拠不足は、Passを
裏付けられない評価上の不足として記録する。脆弱性が実証された場合とは区別する。
全員を拒否できたことだけで、意図したAllow Policyまで完成したと扱わない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Resource・経路一覧 | System Ownerと構成収集処理 | 評価対象Deployment、内部・管理・代替経路 | Deployment変更時 | Revision管理、内部識別子は外部公開時に除去 | Resourceから適用PolicyとPEPまで追跡でき、未確認経路が明示される |
| 許可Matrixと有効Policy | Resource/Policy管理者 | 主体・操作・対象・必要属性・公開/隔離状態 | Policy変更時 | 改ざん防止、適用Revisionを保持 | 意図した許可と実構成が一致し、その他の拒否が確認できる |
| Positive/Negative試験結果 | Test Harnessまたは再現手順を持つ検証者 | N-1〜N-7または根拠のある同等試験、各強制経路 | Policy・経路・Resource実装変更時と定期回帰時 | 模擬Data、Build・Policy・試験IDを保持 | 許可された操作は成功し、未許可操作は内容も副作用も生じない |
| 判断と実操作のTrace | 信頼するPEP・Resource・試験計測 | 成功/拒否の代表例と迂回試験 | 評価した構成と一致する時点 | 閲覧制限、Credentialや本文の不要な記録を避ける | 主体・操作・対象・判断・適用Ruleを実操作へ対応付けられる |
| 変更・障害・失効試験 | 運用/Policy管理者と検証者 | 新規作成、Policy読込失敗、Cache/Sessionを含む失効 | 関連機構変更時 | 時刻・有効条件・構成Revisionを記録 | 変化の途中でも許可根拠のないアクセスを許さない |

このRepositoryにはEvidenceの期待値だけを置く。実際の本番証拠、Secret、顧客情報は保存しない。
ログの存在自体を適合条件にせず、同等に追跡可能な試験計測等でも保証を確認できる。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C5.2.2` | Resourceへ入るService権限だけでなく、検索・組立でEnd-userの権限を維持する |
| `v1.0-C5.2.4` | 出力に含まれる情報の受取権限を推論後に確認する。Resourceの入口認可の代替ではない |
| `v1.0-C5.2.5` | Agentの実行環境から認可判断基盤を分離する。C5.2.1単独では特定の分離Topologyを要求しない |
| `v1.0-C5.3.1` | 共有Serving状態を介した他Tenantの処理への影響・観測を扱う |
| `v1.0-C5.3.2` | 共有計算資源を経由した観測・干渉を扱う。API認可だけでは保証できない |

## Known limitations and uncertainty

- 明示的なPolicyの存在は、業務上の権限設計や最小権限の妥当性を証明しない。
- 許可された操作自体が有害になる場合、目的・引数・承認等の追加保証が必要になる。
- 認証、代理実行、Prompt Injection耐性、出力制御、Hardware分離の全体を保証しない。
- 上流はResource粒度や許可の有効期間を一律に規定しない。実装の前提を記録して評価する。
- 学習ノートにある「PDP停止ならDeny」は、有効な判断が得られない場合として扱う。
  有効なローカルPolicyの利用まで否定しない。また公開Readの明示Ruleと無認可公開を区別する。
- 有限の試験で未発見の全経路を証明できるわけではない。構成確認と試験を組み合わせる。

Engineering Pattern Mappingは未評価であり、特定Patternの存在を本Controlの成熟条件にしない。
`verifiable`は本Artifactに検証方法と証拠期待値が揃ったことを表す。製品適合や学習進捗ではない。

## References

- [AISVS v1.0 C5 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [AISVS v1.0 C5.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-02-AI-Resource-Authorization-Classification.md)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html): 継続更新される補足Guidance。2026-09-08確認。公開Resourceの認可、Default Deny、全Requestでの検査、失敗時の安全な終了を参照。
- [C5.2.1学習ノート](learning.md): 対話由来の洞察。Normativeの代替ではない。

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-08 | 解釈、適用境界、脅威、検証、Evidenceを備えた初版。公開Ruleと有効なローカルPolicyを区別 | AISVS固定Revision、OWASP補足Guidance、Repository interpretation | 本変更のSP-1〜SP-5、N-1〜N-7、Evidence expectations。製品試験は未実施 |
