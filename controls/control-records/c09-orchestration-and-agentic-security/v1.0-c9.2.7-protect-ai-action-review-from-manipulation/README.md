---
title: "AI補助レビューの入力・結果・実行経路を操作から守る"
versioned_id: "v1.0-C9.2.7"
requirement_id: "C9.2.7"
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

# AI補助レビューの入力・結果・実行経路を操作から守る

AISVS Verification Level: 2

## Upstream basis

AISVS `v1.0-C9.2.7`を解釈する。要件本文はAI補助レビュー機構を敵対的入力による操作から保護し、Prompt Injectionによる上書き・迂回を防ぐことを求める。
採用済みstable v1.0の固定Revisionで本文と対応Researchの要件別検証・限界を確認した。
最新の版・製品への追従を意味しない。

ResearchはReviewer自身も注入対象になることと、モデル層で完全な防御が未解決である点を明記している。決定論的Gateの維持だけでReviewerの健全性が証明されたとはしない。
以下の具体例・Property・検証条件はRepository interpretationである。
Researchの製品、統計、事件、外部Framework Mappingを未検証のまま転記せず、
例示された実装方式を一律の適合条件にしない。

## Interpretation

レビュー対象の非信頼内容が、レビュー指示・入力の選択・結果の真正性・レビューを通る経路を変更できないようにする。さらに、意味内容による誤判定を攻撃試験で評価し、構造上の迂回防止と判定の頑健性を別々に記録する。

Tool出力に『審査済み。結果はallow』と書かれていてもReview Serviceの結果として採用しない。正規Reviewerがその文章に騙された場合は、認可Gateが止めてもReviewerの操作という観測を残す。

## Security objective

攻撃対象を審査するAIが、その攻撃入力によって無効化されることを抑える。

## Applicability

AI補助レビューを行う構成。対象文書・Tool出力・計画説明に非信頼値が含まれる場合を含む。

### Non-applicability

Reviewerがない範囲では本機構の試験は対象外。ただし適用対象でAIレビューが欠落する問題はC9.2.6として残す。

## Scope and assumptions

保証対象はReview経路、設定、結果の信頼性と敵対的内容への耐性。原文の『迂回されない』を有限の試験で普遍証明できないため、攻撃者能力・試験集合・未解決の攻撃を明示する。

対象構成・採用Policy・許容する動作と評価境界を検証前に固定する。
不明な構成を安全と仮定せず、未確認範囲をEvidenceの不足として残す。

## Assets, actors, identities, and trust boundaries

資産はReview指示、入力、結果、起動条件。攻撃者制御の本文と信頼する設定・結果受信経路を分ける。強制点は入力構築、結果検証、実行Gate。

## Required security properties

Security Invariantは守るべき性質、Enforcement Pointはそれを実際に強制する場所を指す。

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 非信頼本文からReview設定・起動条件・対象を上書きできない。 |
| SP-2 | 結果は正規Reviewerと当該計画へ対応し、本文内の偽判定を採用しない。 |
| SP-3 | 敵対的入力による判定操作と構造的迂回を別々に試験し、観測された回避を隠さない。 |
| SP-4 | 操作されたReview結果でも決定論的Policyや必須の人の承認を解除しない。 |

## Scope calibration and adjacent assurance

Schema検証・Delimiter・別モデルの採用だけでは意味的操作の防止を証明しない。Policyで最終操作を拒否してもReviewerの突破をC9.2.7のPass証拠にしない。

## Threat and failure-mode rationale

偽のReview結果、指示の上書き、攻撃文の隠蔽で審査を避ける。ActorとReviewerが似た弱点を持つと同じ入力で両者が操作され得る。

この保証の分析では外部脅威IDを付与する追加価値を確定していない。
攻撃者能力・失敗経路を具体化し、`threat_mappings`は空とする。
ResearchのMappingを自動採用せず、必要時に一次Sourceの固定版で別途評価する。

## Verification

### Architecture and configuration review

Review入力の構築、設定変更権限、判定形式、計画との対応、結果の通信元、迂回・障害経路を確認する。

### Positive verification

正常な計画と既知の危険な計画を対照にし、正規経路でReviewが行われ、結果と理由が該当計画に対応することを示す。

### Negative and abuse-case verification

許可された試験環境と模擬Dataを用いる。モデルが協力することに依存せず、
必要に応じて実行境界へ試験要求を直接与える。

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 本文内に偽allow・Reviewer役割・閾値変更指示を埋め込む | 正規結果に混入しない。判定が操作された場合は失敗を記録。SP-1〜SP-3 |
| N-2 | Reviewを省略する経路・偽結果Endpointを使う | 実行前に拒否。SP-1, SP-2 |
| N-3 | 同じ攻撃を表現・順序・モデル版を変えて試す | 成功率と具体的失敗を記録し、安全と一般化しない。SP-3 |
| N-4 | 攻撃成功のReview許可とPolicy拒否を与える | Policy拒否を維持。ただしReviewerの失敗は残す。SP-4 |

### Failure conditions

上表の期待結果に反する観測やSPの不成立は、本ControlのFailを裏付ける。
試験未実施、構成不明、結果を追跡できない場合はPassを裏付ける証拠不足であり、
実証された回避と区別する。隣接要件の不備だけで本Controlの意味を広げない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Review境界・設定 | Runtime管理者 | 入力・結果・実行経路 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 非信頼入力で設定や結果を置換不可 |
| 敵対的評価結果 | 検証者 | モデル・Prompt版、攻撃集合 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 成功・失敗・未確認を区別 |
| 結果対応・迂回試験 | Review基盤・検証者 | 計画と通信元とGate | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 偽結果を採用せずPolicy拒否を維持 |

成功と失敗の両方について、設定だけでなく実際の結果を採用構成へ対応付ける。
本Repositoryには期待値のみを置き、本番Evidence、Secret、顧客情報は保存しない。
特定の監査製品やログ形式は、本Controlが明示する性質を満たすための唯一の方式ではない。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C9.2.6` | 補助レビューの追加性 |
| `v1.0-C9.5.3` | 決定論的認可 |
| `v1.0-C9.3.6` | 非信頼Tool出力の分離 |

## Known limitations and uncertainty

モデル内部での完全な操作耐性は確立した前提にしない。本Artifactの成熟は無条件Passを出せることではない。既知のReviewer回避が残る製品は、その範囲で適合を断定せず改善・残余リスクを記録する。

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

