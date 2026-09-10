---
title: "可逆性分類を実行制限へ結び付ける"
versioned_id: "v1.0-C9.2.4"
requirement_id: "C9.2.4"
verification_level: 2
family_id: "C9"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-02-High-Impact-Action-Approval.md"
last_verified: "2026-09-09"
maturity: "verifiable"
mapping_assessment_refs: []
---

# 可逆性分類を実行制限へ結び付ける

AISVS Verification Level: 2

## Upstream basis

AISVS `v1.0-C9.2.4`を解釈する。要件本文は可逆性分類に基づきRuntimeが操作の阻止・承認要求・制限を強制することを求める。
採用済みstable v1.0の固定Revisionで本文と対応Researchの要件別検証・限界を確認した。
最新の版・製品への追従を意味しない。

Researchは分類台帳と実行経路の断絶、未知LabelのFail-open、代替経路による迂回を補足する。
以下の具体例・Property・検証条件はRepository interpretationである。
Researchの製品、統計、事件、外部Framework Mappingを未検証のまま転記せず、
例示された実装方式を一律の適合条件にしない。

## Interpretation

分類を表示するだけでなく、その分類に対応するPolicyが実行を変える。不可逆に設定した操作がRead-onlyと同じ経路で無条件実行されないことを検証する。

本番削除は阻止、復元可能な設定変更は承認付き、閲覧は認可内で許可という模擬Policyを定め、各分類の実動作を比較する。これは例であり一律の対応表ではない。

## Security objective

正しい分類を持っていても安全制御が働かない状態を防ぐ。

## Applicability

可逆性によってAgentの行動を制限する実行基盤。

### Non-applicability

対象高影響操作がない範囲は対象外。分類の欠落はC9.2.3の問題であり、本要件の強制不要とは扱わない。

## Scope and assumptions

各分類へのPolicy対応を管理者が定める。不明・矛盾・古い分類では緩い既定値へ落とさず、拒否または確認待ちにする。

対象構成・採用Policy・許容する動作と評価境界を検証前に固定する。
不明な構成を安全と仮定せず、未確認範囲をEvidenceの不足として残す。

## Assets, actors, identities, and trust boundaries

資産は分類に基づく実行制御。分類の信頼元、Policy評価、実行者、Agent入力を分け、最終実行経路で強制する。

## Required security properties

Security Invariantは守るべき性質、Enforcement Pointはそれを実際に強制する場所を指す。

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 信頼する分類から実行結果へのPolicy対応が明示される。 |
| SP-2 | 実際の操作と分類が結び付き、対応する制限が実行前に働く。 |
| SP-3 | 未知・偽造分類や別経路で制限を弱められない。 |

## Scope calibration and adjacent assurance

本要件は分類の強制。分類の正しさはC9.2.3、承認取得の正当性はC9.2.1で深める。

## Threat and failure-mode rationale

Agentや攻撃者が低影響Labelを自己申告し、Gateを通らない経路で変更する。

この保証の分析では外部脅威IDを付与する追加価値を確定していない。
攻撃者能力・失敗経路を具体化し、`threat_mappings`は空とする。
ResearchのMappingを自動採用せず、必要時に一次Sourceの固定版で別途評価する。

## Verification

### Architecture and configuration review

分類からPolicy、PEP、実行までを追い、API・Queue・再試行・管理経路を確認する。PEPは判断を実操作へ強制する場所。

### Positive verification

各分類の許可・拒否・承認待ちを模擬操作で再現し、対応表どおりの下流結果を確認する。

### Negative and abuse-case verification

許可された試験環境と模擬Dataを用いる。モデルが協力することに依存せず、
必要に応じて実行境界へ試験要求を直接与える。

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 不可逆操作にRead-onlyを自己申告 | 信頼する分類を使いPolicyどおり制限する。SP-2, SP-3 |
| N-2 | 分類を欠落・未知値にする | 緩い既定値で実行しない。SP-3 |
| N-3 | 直接APIや再試行でGateを避ける | 同じ分類Policyが働く。SP-2 |
| N-4 | 承認後に対象を変更して分類が上がる | 旧分類の許可で実行しない。SP-2, SP-3 |

### Failure conditions

上表の期待結果に反する観測やSPの不成立は、本ControlのFailを裏付ける。
試験未実施、構成不明、結果を追跡できない場合はPassを裏付ける証拠不足であり、
実証された回避と区別する。隣接要件の不備だけで本Controlの意味を広げない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 分類Policy対応表 | Policy管理者 | 各分類と例外 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 制限結果が明示 |
| 経路別の実行試験 | 検証者・実行基盤 | 許可・拒否・待機 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 対応どおりの実結果を示す |
| 分類変更・未知値試験 | 検証者 | 条件変化とFallback | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 制限を緩めない |

成功と失敗の両方について、設定だけでなく実際の結果を採用構成へ対応付ける。
本Repositoryには期待値のみを置き、本番Evidence、Secret、顧客情報は保存しない。
特定の監査製品やログ形式は、本Controlが明示する性質を満たすための唯一の方式ではない。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C9.2.3` | 分類の信頼性 |
| `v1.0-C9.2.1` | 人の承認 |
| `v1.0-C9.2.10` | 連鎖単位の分類強制 |

## Known limitations and uncertainty

分類が粗いと適切なPolicyでも危険を捉えられない。制御が正しくても可逆操作の復旧が必ず成功するとは限らない。

`verifiable`は本Artifactに解釈・脅威・検証・証拠期待値が揃った状態を表す。
製品試験の実施・製品適合・学習完了を意味しない。有限の試験で未知の攻撃を全て否定しない。
Engineering PatternとMappingは独立して評価し、その存在を本Controlの成熟条件にしない。

## References

- [AISVS v1.0 C9要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
- [AISVS v1.0 対応Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-02-High-Impact-Action-Approval.md)
- [C9全体分析](../../../docs/c09-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-09 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |

