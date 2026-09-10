---
title: "高影響操作の可逆性を信頼できる根拠で分類する"
versioned_id: "v1.0-C9.2.3"
requirement_id: "C9.2.3"
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

# 高影響操作の可逆性を信頼できる根拠で分類する

AISVS Verification Level: 2

## Upstream basis

AISVS `v1.0-C9.2.3`を解釈する。要件本文は高影響操作ごとに信頼できる可逆性分類を持つことを求める。読取専用、可逆、外部依存の可逆、不可逆は例示である。
採用済みstable v1.0の固定Revisionで本文と対応Researchの要件別検証・限界を確認した。
最新の版・製品への追従を意味しない。

Researchは同じツールでも対象や復旧条件で分類が変わること、自己申告Metadataだけでは信頼できないことを補足する。
以下の具体例・Property・検証条件はRepository interpretationである。
Researchの製品、統計、事件、外部Framework Mappingを未検証のまま転記せず、
例示された実装方式を一律の適合条件にしない。

## Interpretation

操作を元へ戻せるかを実際の副作用と回復条件から判断する。『Backupあり』だけで可逆とせず、誰が何をどこまで戻せるかを確かめる。

通知メールは送信記録を削除しても相手の受信を取り消せない。一方、未公開設定の変更は管理された履歴から戻せる場合がある。同じ更新ツールに一つの固定Labelを付けるだけでは足りない。

## Security objective

可逆性の誤認によって必要な慎重さや承認を弱めることを防ぐ。

## Applicability

高影響操作の分類・承認・復旧を行うAgent Runtimeと管理Catalog。

### Non-applicability

高影響操作能力がない範囲は対象外とできる。分類未実施だから高影響ではないとはしない。

## Scope and assumptions

分類体系は対応関係が説明できれば上流例の語彙に固定しない。回復可能な時間、失われる状態、外部主体の協力条件を明示する。

対象構成・採用Policy・許容する動作と評価境界を検証前に固定する。
不明な構成を安全と仮定せず、未確認範囲をEvidenceの不足として残す。

## Assets, actors, identities, and trust boundaries

資産は分類の正確性と回復可能性。Tool作者の説明、モデルの提案、信頼する分類管理者・復旧証拠を分ける。強制対象は分類の発行・変更・参照。

## Required security properties

Security Invariantは守るべき性質、Enforcement Pointはそれを実際に強制する場所を指す。

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 全高影響操作と引数依存の変種に分類がある。 |
| SP-2 | 分類の根拠・管理主体・回復条件を追跡できる。 |
| SP-3 | 非信頼の自己申告や古い回復条件で安全側の分類を偽れない。 |

## Scope calibration and adjacent assurance

分類が正しくてもRuntimeが無視する問題はC9.2.4。可逆性は影響の大きさと同義ではなく、一時的な障害でも大きな損害を生む。

## Threat and failure-mode rationale

悪意あるToolが破壊的操作をRead-onlyと名乗り、復旧不能な操作を軽く扱わせる。

この保証の分析では外部脅威IDを付与する追加価値を確定していない。
攻撃者能力・失敗経路を具体化し、`threat_mappings`は空とする。
ResearchのMappingを自動採用せず、必要時に一次Sourceの固定版で別途評価する。

## Verification

### Architecture and configuration review

操作・対象・副作用・復旧手順を照合し、分類変更権限とBackup失効時の更新を確認する。

### Positive verification

模擬の可逆操作を実行して戻し、分類に示す範囲まで復旧できることを示す。外部依存なら依存と未保証条件を区別する。

### Negative and abuse-case verification

許可された試験環境と模擬Dataを用いる。モデルが協力することに依存せず、
必要に応じて実行境界へ試験要求を直接与える。

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | ToolがRead-onlyと偽る | 未検証のLabelを正本にしない。SP-2, SP-3 |
| N-2 | 同じToolで破壊的な引数へ変える | 実操作に対応する分類へ変わる。SP-1 |
| N-3 | Backupや復旧権限を失わせる | 旧分類の根拠喪失を検出し再分類・未確認扱いにする。SP-2, SP-3 |
| N-4 | Agentが分類を直接書き換える | 権限外の変更は拒否される。SP-3 |

### Failure conditions

上表の期待結果に反する観測やSPの不成立は、本ControlのFailを裏付ける。
試験未実施、構成不明、結果を追跡できない場合はPassを裏付ける証拠不足であり、
実証された回避と区別する。隣接要件の不備だけで本Controlの意味を広げない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 可逆性台帳 | 業務・復旧管理者 | 高影響操作と変種 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 根拠・責任者・回復条件が追跡可能 |
| 復旧実験または外部保証 | 復旧担当 | 可逆とする範囲 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 主張する復元範囲を確認できる |
| 分類更新試験 | 検証者 | 偽Label・条件変更 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 信頼しないLabelや古い根拠を採用しない |

成功と失敗の両方について、設定だけでなく実際の結果を採用構成へ対応付ける。
本Repositoryには期待値のみを置き、本番Evidence、Secret、顧客情報は保存しない。
特定の監査製品やログ形式は、本Controlが明示する性質を満たすための唯一の方式ではない。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C9.2.4` | 分類に基づく実行制限 |
| `v1.0-C9.2.10` | 行動連鎖の最大影響の扱い |

## Known limitations and uncertainty

既知の条件で復旧できても将来の成功を保証しない。法的・対人的な影響は技術的Rollbackで消えない。

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

