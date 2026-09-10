---
title: "Runtimeの秘密・資格情報をモデルから観測できなくする"
versioned_id: "v1.0-C9.5.4"
requirement_id: "C9.5.4"
verification_level: 2
family_id: "C9"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-05-Agent-Authorization-Delegation.md"
last_verified: "2026-09-09"
maturity: "verifiable"
mapping_assessment_refs: []
---

# Runtimeの秘密・資格情報をモデルから観測できなくする

AISVS Verification Level: 2

## Upstream basis

AISVS `v1.0-C9.5.4`を解釈する。要件本文はAgentが実行時に必要とする秘密・資格情報を、Context Window・System Prompt・Tool呼出し引数等のモデルが観測するContextへ露出させないことを求める。
採用済みstable v1.0の固定Revisionで本文と対応Researchの要件別検証・限界を確認した。
最新の版・製品への追従を意味しない。

ResearchはTransport側の資格情報付与と、環境変数・設定・Tool結果等の漏えい経路を補足する。保存場所を変えるだけで非露出が成立するとはしない。
以下の具体例・Property・検証条件はRepository interpretationである。
Researchの製品、統計、事件、外部Framework Mappingを未検証のまま転記せず、
例示された実装方式を一律の適合条件にしない。

## Interpretation

モデルはどの操作を行うかを指定し、認証に必要な秘密値は信頼する実行側が扱う。秘密を知るToolを呼べる構成では、その結果からモデルへ戻らないことまで確認する。

モデルは『文書Aを取得』だけを要求し、実行側が認証Headerを付与する。認証ErrorにToken全文を含めてモデルへ返せば、通常経路で隠しても不成立。

## Security objective

モデルに見える情報から資格情報を抜き取る経路を減らす。

## Applicability

実行に秘密・認証情報を必要とするAgentとそのTool・Memory・観測系。

### Non-applicability

該当する秘密・資格情報を一切扱わない範囲は対象外。短命Tokenも有効な間は資格情報として対象。

## Scope and assumptions

モデルが直接受信する値と、Toolを使って観測できる値を含める。環境変数とFileのどちらかを一律安全としない。資格情報を参照するHandleも、それ自体で権限を行使できるなら秘密相当か評価する。

対象構成・採用Policy・許容する動作と評価境界を検証前に固定する。
不明な構成を安全と仮定せず、未確認範囲をEvidenceの不足として残す。

## Assets, actors, identities, and trust boundaries

資産は秘密値。モデルContext、Runtimeの認証層、Tool、Log・Trace・Memoryを分ける。強制点は資格情報の取得・注入とモデルへの全戻り経路。

## Required security properties

Security Invariantは守るべき性質、Enforcement Pointはそれを実際に強制する場所を指す。

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Prompt・引数・Contextへ資格情報値を入れない。 |
| SP-2 | Toolの正常・Error・Debug出力からも秘密を返さない。 |
| SP-3 | モデルが使えるFile・環境・Log経路から秘密を取り込めない。 |

## Scope calibration and adjacent assurance

資格情報がモデルに見えなくても、広い権限のProxyを悪用できれば別の認可不備。Runtime侵害から承認鍵を守るC9.2.9とは範囲を分ける。

## Threat and failure-mode rationale

攻撃者がDebugや認証復旧を装い、Agentに環境・設定・Errorを表示させて秘密を取得する。

この保証の分析では外部脅威IDを付与する追加価値を確定していない。
攻撃者能力・失敗経路を具体化し、`threat_mappings`は空とする。
ResearchのMappingを自動採用せず、必要時に一次Sourceの固定版で別途評価する。

## Verification

### Architecture and configuration review

秘密の発行・注入・送信・Error処理・観測・保存を追い、モデルへ届く全Payloadを模擬秘密で計測する。

### Positive verification

識別可能な模擬Tokenで正常APIを呼び、下流認証は成功するがモデルへの送受信に値が現れないことを示す。

### Negative and abuse-case verification

許可された試験環境と模擬Dataを用いる。モデルが協力することに依存せず、
必要に応じて実行境界へ試験要求を直接与える。

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | System Prompt・Tool定義・引数を検査 | 模擬秘密がない。SP-1 |
| N-2 | 認証失敗・Debug・例外を誘発 | 秘密を含むErrorをモデルへ渡さない。SP-2 |
| N-3 | File・環境・Log読取Toolで秘密を要求 | 値がContextへ流れない。SP-3 |
| N-4 | 再試行・Memory保存・Trace閲覧を行う | 二次経路でも非露出。SP-2, SP-3 |

### Failure conditions

上表の期待結果に反する観測やSPの不成立は、本ControlのFailを裏付ける。
試験未実施、構成不明、結果を追跡できない場合はPassを裏付ける証拠不足であり、
実証された回避と区別する。隣接要件の不備だけで本Controlの意味を広げない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 秘密Data Flow | Runtime管理者 | 注入・戻り・保存 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | モデル非露出経路が明確 |
| 模擬秘密の観測試験 | 検証者 | 正常・Error・Debug | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 資格情報がモデルへ届かない |
| 実効読取権限 | 基盤・Tool管理者 | File・環境・Log | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | Tool経由の取得を防ぐ |

成功と失敗の両方について、設定だけでなく実際の結果を採用構成へ対応付ける。
本Repositoryには期待値のみを置き、本番Evidence、Secret、顧客情報は保存しない。
特定の監査製品やログ形式は、本Controlが明示する性質を満たすための唯一の方式ではない。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C9.2.9` | 承認発行鍵の隔離 |
| `v1.0-C9.5.1` | 資格情報を使う操作の認可 |
| `v1.0-C5.1.2` | TokenのScope・寿命 |

## Known limitations and uncertainty

Provider内部の秘密管理まで本Controlだけでは証明しない。暗号化済みでも復号Toolをモデルが自由利用できれば非露出にはならない。

`verifiable`は本Artifactに解釈・脅威・検証・証拠期待値が揃った状態を表す。
製品試験の実施・製品適合・学習完了を意味しない。有限の試験で未知の攻撃を全て否定しない。
Engineering PatternとMappingは独立して評価し、その存在を本Controlの成熟条件にしない。

## References

- [AISVS v1.0 C9要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
- [AISVS v1.0 対応Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-05-Agent-Authorization-Delegation.md)
- [C9全体分析](../../../docs/c09-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-09 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |

