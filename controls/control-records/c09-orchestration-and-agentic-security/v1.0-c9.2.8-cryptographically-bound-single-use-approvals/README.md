---
title: "承認を操作・要求者・実行Contextと一回限りの値へ暗号的に結合する"
versioned_id: "v1.0-C9.2.8"
requirement_id: "C9.2.8"
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

# 承認を操作・要求者・実行Contextと一回限りの値へ暗号的に結合する

AISVS Verification Level: 3

## Upstream basis

AISVS `v1.0-C9.2.8`を解釈する。要件本文は承認を操作引数、要求者Identity、実行Context、固有の一回限りのNonceへ暗号的に結合することを求める。
採用済みstable v1.0の固定Revisionで本文と対応Researchの要件別検証・限界を確認した。
最新の版・製品への追従を意味しない。

Researchは正規化、署名検証、並列Replay、消費済みNonceの保持、実行前の検証を補足する。
以下の具体例・Property・検証条件はRepository interpretationである。
Researchの製品、統計、事件、外部Framework Mappingを未検証のまま転記せず、
例示された実装方式を一律の適合条件にしない。

## Interpretation

承認証票を別の操作や別Sessionへ転用できず、同じ証票を二度実行へ使えないようにする。Nonceは一回の承認を識別する固有値であり、付けるだけでなく再利用を拒否する必要がある。

注文Aへの返金承認を注文B、別金額、別要求者へ差し替えたら暗号検証・対応確認で拒否する。同じ正当な承認を並列に二度送っても二度の返金を開始しない。

## Security objective

承認の差替え・盗用・Replayによる未承認操作を防ぐ。

## Applicability

高影響操作等の承認を実行者へ渡す構成。

### Non-applicability

承認対象操作が存在しない範囲は対象外。単一Processや内部通信であることは暗号的結合を省略する理由にならない。

## Scope and assumptions

署名または安全なMAC等で結合を検証する。単なるHashだけは発行者の真正性を示さない。必要な実行Contextを列挙し、Nonceの消費・障害復旧・保存期限を定義する。特定Algorithmをここで推奨せず、採用時に一次仕様を検証する。

対象構成・採用Policy・許容する動作と評価境界を検証前に固定する。
不明な構成を安全と仮定せず、未確認範囲をEvidenceの不足として残す。

## Assets, actors, identities, and trust boundaries

資産は承認証票・検証鍵・Nonce状態。承認発行者、Agent、Executor、Nonce Storeを分ける。強制点は副作用前の暗号検証と不可分な使用済み判定。

## Required security properties

Security Invariantは守るべき性質、Enforcement Pointはそれを実際に強制する場所を指す。

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 全必須要素を暗号的に結合し、Executorが信頼する発行者の証票を検証する。 |
| SP-2 | 正規化された承認内容と実行要求が一致する。 |
| SP-3 | Nonceの一回使用が並列・再試行・再起動でも維持される。 |

## Scope calibration and adjacent assurance

人が見た内容の完全性はC9.2.2、鍵の隔離はC9.2.9。暗号的に正当な承認でも業務判断の正しさは保証しない。

## Threat and failure-mode rationale

攻撃者が承認証票をコピーし、引数やContextを変更して再利用する。二つのWorkerが同時に未使用と判断すると二重実行が起きる。

この保証の分析では外部脅威IDを付与する追加価値を確定していない。
攻撃者能力・失敗経路を具体化し、`threat_mappings`は空とする。
ResearchのMappingを自動採用せず、必要時に一次Sourceの固定版で別途評価する。

## Verification

### Architecture and configuration review

署名対象のSchema、Canonicalization、検証鍵の信頼元、実行引数への結合、Nonce状態の原子的更新を追う。

### Positive verification

正当な承認を一度使い、同じ操作だけが成功する。副作用前後でNonceと結果が追跡できることを確かめる。

### Negative and abuse-case verification

許可された試験環境と模擬Dataを用いる。モデルが協力することに依存せず、
必要に応じて実行境界へ試験要求を直接与える。

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 引数・要求者・Context・Nonceを一項目ずつ変更 | 検証または対応確認で拒否。SP-1, SP-2 |
| N-2 | 同じ承認を並列にReplay | 最大一回の実行受付。SP-3 |
| N-3 | 消費直後にWorkerを再起動し再送 | 未使用へ戻らない。結果不明時も盲目的に再実行しない。SP-3 |
| N-4 | 異なる表現の数値・JSON・文字列で意味を変える | 署名と実行の解釈差で操作を差し替えられない。SP-2 |
| N-5 | 検証鍵・Nonce Storeを利用不能にする | 検証なしの実行を拒否。SP-1, SP-3 |

### Failure conditions

上表の期待結果に反する観測やSPの不成立は、本ControlのFailを裏付ける。
試験未実施、構成不明、結果を追跡できない場合はPassを裏付ける証拠不足であり、
実証された回避と区別する。隣接要件の不備だけで本Controlの意味を広げない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 結合Schemaと検証設定 | 承認基盤管理者 | 必須要素と信頼鍵 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 全要素の結合が説明できる |
| 改変・並列・再起動試験 | 検証者 | 証票から副作用 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 改変拒否と一回性を観測 |
| Nonceと実行結果の対応 | Nonce Store・Executor | 受付・消費・復旧 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 重複実行と未使用への巻戻りがない |

成功と失敗の両方について、設定だけでなく実際の結果を採用構成へ対応付ける。
本Repositoryには期待値のみを置き、本番Evidence、Secret、顧客情報は保存しない。
特定の監査製品やログ形式は、本Controlが明示する性質を満たすための唯一の方式ではない。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C9.2.2` | 承認表示の正確さ |
| `v1.0-C9.2.9` | 承認発行鍵の隔離 |
| `v1.0-C9.6.2` | 期限切れ承認の拒否 |

## Known limitations and uncertainty

分散Systemで副作用とNonce更新を一つのTransactionにできない場合、結果照会・冪等性・安全な復旧が必要。一回の受付だけで外部System全体の厳密なExactly-onceを主張しない。

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

