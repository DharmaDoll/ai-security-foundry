---
title: "Step-up Authentication for High-risk AI Operations"
versioned_id: "v1.0-C5.1.1"
requirement_id: "C5.1.1"
verification_level: 3
family_id: "C5"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-01-Identity-Management-Authentication.md"
last_verified: "2026-09-08"
maturity: "verifiable"
mapping_assessment_refs: []
---

# 高RiskなAI操作へのStep-up Authentication

AISVS Verification Level: 3

初めて読む方へ：[具体例・用語・対話を含む学習ノート](learning.md)。

## Upstream basis

AISVS `v1.0-C5.1.1`、Verification Level 3を解釈する。ModelのDeploy、WeightのExport、
Training DataへのAccess、本番設定変更等の高Risk操作について、Step-up Authenticationを要求する。
固定RevisionのC5.1 Research（Last Researched: 2026-07-14）の該当行を確認した。
ResearchのFreshness、API迂回、認証情報の追跡という観点を用いる。
Researchが推す特定Authenticator、製品、AAL3を、原文の一律な必須条件とはしない。

RFC 9470（2023-09、Standards Track）は認証強度や認証時刻が不足する場合の再認証交渉を補足する。
本ControlはOAuthを必須とせず、以下の操作別Policyと検証をRepository interpretationとして定める。

## Interpretation

**通常Sessionがあるだけで重要操作を実行させず、その操作が求める認証強度・新しさを確認する。**
Model WeightのExportなら、古いログイン状態だけでは拒否し、要求に適合する再認証後に実行する。
既に十分な強度・新しさの認証を済ませている場合まで、毎Requestで再入力を必須にはしない。

認証時刻とToken発行時刻は別である。既存Sessionから新Tokenを発行しても、
本人が改めて認証した証拠にはならない。

## Security objective

通常Sessionの窃取や長期Integration Credentialだけで、重要AI資産へ操作できる経路を減らす。
認証は主体の確認であり、操作の正当性・内容への同意・安全性を証明するものではない。

## Applicability

対象操作を持つUI、API、CLI、Agent、CI/CD、管理・復旧経路に適用する。
High-riskはModelやDataの価値、操作の影響、公開範囲、回復可能性に基づき定義する。
列挙された操作を理由なく通常操作へ分類し直して除外しない。

### Non-applicability

対象範囲に高Risk操作が存在しない場合は、操作一覧と理由を残す。
自動化やHuman不在を理由に自動で除外しない。非Human経路に同等のStep-upを主張する場合は、
通常のMachine認証と比べて何を追加・更新して検証するかを示す。
単なる短命TokenやJIT許可をHuman再認証と同一視せず、実現できない範囲は例外として残す。

## Scope and assumptions

操作ごとに必要な認証方式・最大認証経過時間・Issuerとの意味の合意を定める。
原文は具体的な分数やAuthenticatorを指定しない。
Freshnessは実際の認証Eventの時刻で測り、Token Refreshで水増ししない。
既にStep-up済みSessionの窃取まで完全に防ぐと主張しない。

## Assets, actors, identities, and trust boundaries

AssetsはWeight、Training Data、Deployment、本番設定。
Actorsは操作者、代理Agent、認証Service、Resource Server、操作Policy管理者。
信頼境界はCallerから認証Service、認証証拠からResource操作、通常Sessionから高Risk操作である。
PDPは要求する認証Contextを決める場所、PEPは実操作を止める場所であり、Modelに任せない。

## Required security properties

| ID | 必要な性質 | 成立条件 |
|---|---|---|
| SP-1 | 操作と認証条件の対応 | 対象操作の強度・Freshnessが決まり、全経路で同じ保証を要求する |
| SP-2 | 信頼する認証証拠 | 主体、認証Context、認証時刻を信頼元で検証し、自己申告を受理しない |
| SP-3 | 操作前の強制 | 不足時は実操作を行わず、条件を満たした場合のみ進む |
| SP-4 | 期限・障害時の維持 | 古い証拠や検証不能状態を、新TokenやFallbackで許可へ変えない |

## Scope calibration and adjacent assurance

| 状況 | 評価 |
|---|---|
| UIは再認証するがCLIは通常SessionでExportできる | Fail |
| Tokenの新しい発行時刻だけでFreshnessを判定する | Fail |
| 要求を満たす直近の認証証拠を検証して実行する | Pass候補。毎回の新しいChallengeは必須ではない |
| 再認証後にExport先が改ざんされる | 認証はPassし得るが、操作認可・Transaction Integrityに重大な別Gap |
| 承認ボタンだけで本人の再認証を確認しない | Step-upの証拠にはならない |
| 強度・Freshnessを満たす証拠が有効な間、認証Service停止中でも検証できる | 停止だけでFailとはしない。証拠が検証不能なら拒否する |

Phishing-resistant認証は有用な追加防御であるが、本要件単独の一律な製品選定条件にはしない。
CSRF対策や操作内容への署名・承認も別の保証として扱う。

## Threat and failure-mode rationale

通常Sessionを盗んだ攻撃者が直接APIを呼び、再認証UIを迂回する。
またはRefreshでToken発行時刻だけを更新し、古い認証を新しい認証に見せかける。
正規Agentが誤った重要操作を行う場合もあるが、再認証だけでAgentの意図は保証できない。
外部脅威IDはこの境界を適切な粒度で確定していないためMappingせず、失敗経路を直接記述する。

## Verification

### Architecture and configuration review

全操作と呼出元を列挙し、認証条件、証拠の発行・検証、操作の開始地点を追う。
UI、API、CI/CD、Recoveryで保証が欠ける箇所を特定する。

### Positive verification

模擬の高Risk操作へ、条件不足のSessionと、適合する認証証拠を順に提示する。
後者だけが実行され、主体・認証Event・対象操作を追跡できることを確認する。
通常操作まで不要に昇格させていないことも確認する。

### Negative and abuse-case verification

| ID | 試験 | 期待結果 |
|---|---|---|
| N-1 | 通常TokenでUIを使わずAPI/CLIの重要操作を呼ぶ | 実操作前に拒否または再認証要求 |
| N-2 | 古い認証から新TokenをRefreshする | 許容経過時間を超えた認証は古いまま扱う |
| N-3 | 認証時刻・強度・主体・Issuerを改ざんする | 不正な証拠を拒否する |
| N-4 | 許容期限を超えて再試行、別管理経路を利用する | Silent downgradeせず拒否する |
| N-5 | 有効な認証証拠を取得も検証もできない状態にする | Static Key等でStep-upを迂回しない |

操作結果と副作用を確認し、Challenge画面の表示だけを合格根拠にしない。

### Failure conditions

不足した認証で高Risk操作が成功、発行時刻によるFreshness偽装、未検証Contextの受理、
迂回経路は不成立。操作一覧や検証証拠の不足は、Passを裏付けられない状態として区別する。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 操作と認証Policyの表 | System/認証管理者 | 全高Risk操作・経路 | 操作/認証Policy変更時 | Revision管理 | 強度・認証経過時間・適用理由が明確 |
| 認証から操作までのTrace | 認証Service/PEP | 成功・拒否 | 評価構成と一致 | Token本体は保存せず相関IDで追跡 | 認証Eventと実操作が結び付く |
| Positive/Negative結果 | 検証者/Test Harness | N-1〜N-5または同等 | 関連変更時・定期回帰 | 模擬主体、Build/Policy記録 | 不足・古い・不正証拠では副作用なし |
| 非Human経路の設計根拠 | 自動化/認証Owner | CI/CD、代理・復旧 | 経路変更時 | 秘密なし、例外を明示 | 単なる通常Machine認証をStep-upと誤称しない |

本番証拠やCredentialはRepositoryへ置かない。

## Related requirements

- `v1.0-C5.1.2`: AgentのSystem間Credentialの性質。認証の追加確認とは別。
- `v1.0-C5.2.1`: 認証後にどのResource操作を許可するか。
- `v1.0-C5.2.6`: 特権付与の開始・最大時間・終了。Fresh AuthenticationとJITは別。

## Known limitations and uncertainty

High-risk定義と必要な強度・Freshnessは運用依存であり、一律の数値を発明しない。
非HumanのStep-upに原文は具体Protocolを定めない。通常のWorkload認証だけでは代替したと主張しない。
操作内容への同意、Phishingへの完全耐性、Step-up済みSessionの窃取防止は別評価。
本Artifactは検証可能なControlを示すもので製品適合ではなく、Engineering Mappingも未評価である。

補足仕様: [RFC 9470](https://www.rfc-editor.org/rfc/rfc9470.html)
（Standards Track、2023-09、2026-09-08確認）。認証強度・時刻の交渉を参考とし、
具体Claim名を全実装へ要求しない。

## References

- [AISVS v1.0 C5 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [同RevisionのAISVS Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-01-Identity-Management-Authentication.md): 補足資料でありNormativeではない。

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-08 | 初版。解釈・適用境界・脅威・検証・証拠期待値を整備 | 固定RevisionのAISVS、Repository interpretation | 本文のSecurity Properties、試験、Evidence expectations。製品試験は未実施 |
