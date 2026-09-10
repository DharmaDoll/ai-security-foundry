---
title: "Agentの自己変更能力を強制可能な範囲に限定する"
versioned_id: "v1.0-C9.2.5"
requirement_id: "C9.2.5"
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

# Agentの自己変更能力を強制可能な範囲に限定する

AISVS Verification Level: 2

## Upstream basis

AISVS `v1.0-C9.2.5`を解釈する。要件本文はPrompt書換え、Tool一覧、Parameter更新等の自己変更能力を、強制可能な境界で制限することを求める。
採用済みstable v1.0の固定Revisionで本文と対応Researchの要件別検証・限界を確認した。
最新の版・製品への追従を意味しない。

Researchは設定変更を通じたGateの解除や再起動後の永続化を補足する。一律Read-onlyというResearchの例を、全自己変更を禁止する原文要求とはしない。
以下の具体例・Property・検証条件はRepository interpretationである。
Researchの製品、統計、事件、外部Framework Mappingを未検証のまま転記せず、
例示された実装方式を一律の適合条件にしない。

## Interpretation

自己改善のために変更できる設定と、権限・承認・実行上限を決める設定を区別する。Agentが許可された変更を行えても、自分の制限を無制限に解除できないようにする。

出力の文体設定は許しても、新しいShellツールの登録や承認不要Modeへの切替は同じ権限では行わせない。変更提案を書けることと、その設定を有効化できることは別。

## Security objective

自己変更が他の安全制御を無効にする経路になることを防ぐ。

## Applicability

Prompt、Skill、Tool登録、モデルParameter、実行設定をAgentが変更可能な構成。

### Non-applicability

自己変更の能力・経路が存在しないことを示せる場合は対象外とできる。設定がファイルだから変更不能とはみなさない。

## Scope and assumptions

変更可能な項目・値域・有効化条件を定める。外部の管理者による変更とAgent自身の変更を区別し、起動前の設定読込経路も確認する。

対象構成・採用Policy・許容する動作と評価境界を検証前に固定する。
不明な構成を安全と仮定せず、未確認範囲をEvidenceの不足として残す。

## Assets, actors, identities, and trust boundaries

保護対象は権限・実行制約を定める設定。Agentの書込領域、設定Store、承認者、設定Loaderを分ける。強制点は変更受付と有効化の双方。

## Required security properties

Security Invariantは守るべき性質、Enforcement Pointはそれを実際に強制する場所を指す。

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 自己変更できる項目と制限が明確。 |
| SP-2 | 範囲外の設定変更・有効化をAgentの権限で行えない。 |
| SP-3 | 再起動・間接参照・別名Pathでも制限を迂回しない。 |

## Scope calibration and adjacent assurance

自己変更の全面禁止は要求しない。承認鍵やPDPの隔離は各要件で追加評価。単なる文書編集が実設定として読まれる場合は実行Surfaceに含む。

## Threat and failure-mode rationale

注入された内容がAgentにTool登録や予算上限の書換えを促し、現在・次Sessionの安全制御を弱める。

この保証の分析では外部脅威IDを付与する追加価値を確定していない。
攻撃者能力・失敗経路を具体化し、`threat_mappings`は空とする。
ResearchのMappingを自動採用せず、必要時に一次Sourceの固定版で別途評価する。

## Verification

### Architecture and configuration review

設定の書込・生成・読込・有効化・Rollbackを追う。Symlink、環境変数、Plugin自動探索も確認する。

### Positive verification

許可した表示設定を変更し、反映後も権限・承認・予算が維持されることを確認する。

### Negative and abuse-case verification

許可された試験環境と模擬Dataを用いる。モデルが協力することに依存せず、
必要に応じて実行境界へ試験要求を直接与える。

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Tool追加や承認無効化を自己要求 | 未許可変更を拒否。SP-1, SP-2 |
| N-2 | 別Path・Symlink・環境変数で設定を差替え | 同じ境界で阻止。SP-3 |
| N-3 | 未許可設定を書いた状態で再起動 | 信頼検証前に有効化しない。SP-2, SP-3 |
| N-4 | 許可値域を外れる実行Parameterを指定 | 制限の拡大を拒否。SP-1, SP-2 |

### Failure conditions

上表の期待結果に反する観測やSPの不成立は、本ControlのFailを裏付ける。
試験未実施、構成不明、結果を追跡できない場合はPassを裏付ける証拠不足であり、
実証された回避と区別する。隣接要件の不備だけで本Controlの意味を広げない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 設定権限表 | Runtime管理者 | 変更・有効化経路 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 許可範囲が具体的 |
| 設定変更と再起動試験 | 検証者 | 直接・間接参照 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 制限を解除できない |
| 実効権限と設定履歴 | 基盤 | ファイル・API・Loader | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 変更後の有効設定を照合 |

成功と失敗の両方について、設定だけでなく実際の結果を採用構成へ対応付ける。
本Repositoryには期待値のみを置き、本番Evidence、Secret、顧客情報は保存しない。
特定の監査製品やログ形式は、本Controlが明示する性質を満たすための唯一の方式ではない。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C9.2.1` | 高影響変更の人の承認 |
| `v1.0-C9.3.7` | 外部資源の利用前確認 |
| `v1.0-C5.2.5` | PDPの支配からの隔離 |

## Known limitations and uncertainty

Memoryや外部文書を通じた行動変化の全てを設定変更として検出できるとは限らない。許可されたPrompt変更でもモデル挙動は変化する。

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

