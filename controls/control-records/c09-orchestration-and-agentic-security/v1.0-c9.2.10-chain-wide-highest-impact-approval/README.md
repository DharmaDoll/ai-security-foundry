---
title: "行動連鎖の最大影響を承認Gateへ反映する"
versioned_id: "v1.0-C9.2.10"
requirement_id: "C9.2.10"
verification_level: 3
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

# 行動連鎖の最大影響を承認Gateへ反映する

AISVS Verification Level: 3

## Upstream basis

AISVS `v1.0-C9.2.10`を解釈する。要件本文は多段・複数Agentの行動連鎖に含まれる最大影響の可逆性分類を承認Gateが強制することを求める。
採用済みstable v1.0の固定Revisionで本文と対応Researchの要件別検証・限界を確認した。
最新の版・製品への追従を意味しない。

Researchは低RiskのWrapperに隠れた不可逆な子操作、委任時の分類喪失、動的計画の不確実性を補足する。
以下の具体例・Property・検証条件はRepository interpretationである。
Researchの製品、統計、事件、外部Framework Mappingを未検証のまま転記せず、
例示された実装方式を一律の適合条件にしない。

## Interpretation

表面のタスク名や最後の操作だけで承認水準を決めない。連鎖内の高影響操作が要求する制限を、途中のAgentやWrapperが弱めない。

『報告書作成』の子処理に本番Data削除が含まれるなら、閲覧タスクとしてだけ承認しない。後から削除が計画に加わる場合も古い低影響承認で続行しない。

## Security objective

操作の分割・委任で高影響の承認をすり抜けることを防ぐ。

## Applicability

多段または複数Agentの行動連鎖に承認対象操作を含む構成。

### Non-applicability

単一操作で行動連鎖がない範囲は対象外とできる。裏の子呼出しを見落として単一扱いしない。

## Scope and assumptions

連鎖の範囲と分類間の制限関係を定義する。順序付け不能な制約は弱い一方へ丸めず、両方の制限を保つ。未確定の動的計画は許される能力範囲を先に限定するか、高影響の追加前に連鎖を再評価する。

対象構成・採用Policy・許容する動作と評価境界を検証前に固定する。
不明な構成を安全と仮定せず、未確認範囲をEvidenceの不足として残す。

## Assets, actors, identities, and trust boundaries

資産は計画・委任Context・承認水準。親Agent、子Agent、分類管理、Gateを跨ぐ境界で分類と承認範囲を保持する。

## Required security properties

Security Invariantは守るべき性質、Enforcement Pointはそれを実際に強制する場所を指す。

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 子・入れ子操作を含む連鎖の影響を把握する。 |
| SP-2 | 最大影響に必要なGateを連鎖に適用する。 |
| SP-3 | 計画変更・委任で分類や必要承認を下げられない。 |

## Scope calibration and adjacent assurance

最も高い単一操作の分類だけで、複数操作の組合せによる新しい影響が尽くされるとは限らない。追加の業務分析を残す。

## Threat and failure-mode rationale

攻撃者が危険操作を子タスクへ隠し、各Agentには低影響の仕事と見せかける。

この保証の分析では外部脅威IDを付与する追加価値を確定していない。
攻撃者能力・失敗経路を具体化し、`threat_mappings`は空とする。
ResearchのMappingを自動採用せず、必要時に一次Sourceの固定版で別途評価する。

## Verification

### Architecture and configuration review

連鎖ID、子操作、分類伝達、承認範囲、動的変更時の再評価を追う。

### Positive verification

読取と変更を含む模擬計画で、高影響側の承認が得られるまで対象連鎖を解放しないことを示す。

### Negative and abuse-case verification

許可された試験環境と模擬Dataを用いる。モデルが協力することに依存せず、
必要に応じて実行境界へ試験要求を直接与える。

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 低影響Wrapper内に不可逆操作を置く | 高影響Gateが適用される。SP-1, SP-2 |
| N-2 | 子へ渡す分類を欠落・低下させる | 弱い分類で続行しない。SP-3 |
| N-3 | 承認後に高影響Stepを追加 | 実行前に連鎖の承認範囲を再評価。SP-2, SP-3 |
| N-4 | 未知の子操作を実行時に発見 | 無確認の低影響扱いをせず停止・再承認。SP-1, SP-3 |

### Failure conditions

上表の期待結果に反する観測やSPの不成立は、本ControlのFailを裏付ける。
試験未実施、構成不明、結果を追跡できない場合はPassを裏付ける証拠不足であり、
実証された回避と区別する。隣接要件の不備だけで本Controlの意味を広げない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 連鎖と分類の対応 | 統括基盤・管理者 | 親子・動的Step | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 最大影響を把握 |
| 委任・承認Trace | Gate・各Agent | 分類と承認範囲 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 境界で低下しない |
| 追加・隠蔽試験 | 検証者 | 計画変更・子操作 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 高影響操作を旧承認で実行不可 |

成功と失敗の両方について、設定だけでなく実際の結果を採用構成へ対応付ける。
本Repositoryには期待値のみを置き、本番Evidence、Secret、顧客情報は保存しない。
特定の監査製品やログ形式は、本Controlが明示する性質を満たすための唯一の方式ではない。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C9.2.3` | 信頼する分類 |
| `v1.0-C9.2.4` | 分類のRuntime強制 |
| `v1.0-C9.5.5` | 委任の認可 |

## Known limitations and uncertainty

全未来Stepを予測する保証はない。不明な範囲を明示し、実行可能範囲を保守的に限定する。複合的な不可逆性は別途評価する。

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

