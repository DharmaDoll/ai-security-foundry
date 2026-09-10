---
title: "停止指示をAgentから隔離した別経路で強制する"
versioned_id: "v1.0-C9.6.3"
requirement_id: "C9.6.3"
verification_level: 3
family_id: "C9"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-06-Shutdown-Graceful-Degradation.md"
last_verified: "2026-09-09"
maturity: "verifiable"
mapping_assessment_refs: []
---

# 停止指示をAgentから隔離した別経路で強制する

AISVS Verification Level: 3

## Upstream basis

AISVS `v1.0-C9.6.3`を解釈する。要件本文はKill-switch指示をAgent Runtimeから隔離されたOut-of-band経路で実装することを求める。
採用済みstable v1.0の固定Revisionで本文と対応Researchの要件別検証・限界を確認した。
最新の版・製品への追従を意味しない。

ResearchはAgentが停止Policyを変更・遮断できる問題と、別資格情報・管理API・実行権限を通じた実効的独立性を補足する。
以下の具体例・Property・検証条件はRepository interpretationである。
Researchの製品、統計、事件、外部Framework Mappingを未検証のまま転記せず、
例示された実装方式を一律の適合条件にしない。

## Interpretation

停止されるAgentの正常動作や協力を前提にせず、人が別の制御経路で停止を強制できるようにする。Out-of-bandは対象の通常実行経路とは独立した管理経路を指す。

Agent内の停止関数を呼ぶだけでは、侵害Agentが関数を置換・無視できる。外部の制御基盤がProcess・通信・権限を止め、Agentがその設定や資格情報を変更できないことを確かめる。

## Security objective

Agentが侵害・暴走しても、自分を止める権限を無効にできないようにする。

## Applicability

Agent Runtimeを対象とするKill-switchの指示・強制機構。

### Non-applicability

停止対象のAgent Runtimeがない範囲は対象外。Kill-switch未実装は停止要件の欠落であり、隔離不要の理由ではない。

## Scope and assumptions

Runtime侵害を仮定し、管理・Deploy・Network・資格情報・停止設定への実効権限を調べる。別Hostや別UIだけでなく、同じ管理権限で書き換えられないか確認する。

対象構成・採用Policy・許容する動作と評価境界を検証前に固定する。
不明な構成を安全と仮定せず、未確認範囲をEvidenceの不足として残す。

## Assets, actors, identities, and trust boundaries

資産は人の停止権限と制御経路。Agent、運用者、停止Controller、基盤の強制点を分ける。停止手段の管理・復旧経路も境界へ含める。

## Required security properties

Security Invariantは守るべき性質、Enforcement Pointはそれを実際に強制する場所を指す。

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 停止命令がAgentの協力不要な経路で強制点へ届く。 |
| SP-2 | Agentが停止鍵・Policy・Controllerを取得・変更・無効化できない。 |
| SP-3 | 通常経路の妨害時にも停止を試験でき、失敗を成功と表示しない。 |

## Scope calibration and adjacent assurance

本要件は停止経路の独立性。全群の停止範囲はC9.1.3、推論・出力の実停止はC9.6.1。資格情報の失効だけでは進行中の計算停止にならない場合がある。

## Threat and failure-mode rationale

侵害Agentが停止Hookを削除、管理APIを書換え、停止通知を握り潰し、通常経路に残る処理を続ける。

この保証の分析では外部脅威IDを付与する追加価値を確定していない。
攻撃者能力・失敗経路を具体化し、`threat_mappings`は空とする。
ResearchのMappingを自動採用せず、必要時に一次Sourceの固定版で別途評価する。

## Verification

### Architecture and configuration review

停止指示から強制までと、Agentが取得できる全管理権限を追う。停止基盤のDeploy・Rollback・復旧権限も確認する。

### Positive verification

Agentを応答不能にし、別の運用Identityから停止を起動して強制点の動作を確認する。

### Negative and abuse-case verification

許可された試験環境と模擬Dataを用いる。モデルが協力することに依存せず、
必要に応じて実行境界へ試験要求を直接与える。

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Agent内の停止Hookを無効化 | 外部経路で停止できる。SP-1 |
| N-2 | Agent権限でController・Policy・鍵を変更 | 拒否される。SP-2 |
| N-3 | 通常通信を遮断・飽和させる | 独立経路の効果を測り、停止不能なら未完了を示す。SP-3 |
| N-4 | 停止基盤を再Deploy・Rollbackしようとする | Agentの権限で停止権限を奪えない。SP-2 |

### Failure conditions

上表の期待結果に反する観測やSPの不成立は、本ControlのFailを裏付ける。
試験未実施、構成不明、結果を追跡できない場合はPassを裏付ける証拠不足であり、
実証された回避と区別する。隣接要件の不備だけで本Controlの意味を広げない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 停止Architectureと権限Matrix | 基盤・Security管理者 | 命令・強制・管理・復旧 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 通常Runtimeの支配から独立 |
| 非協力Agentでの停止試験 | 検証者・運用者 | 応答不能・Hook破壊 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 協力不要の強制を確認 |
| 管理権限の越境試験 | 検証者 | 鍵・Policy・Deploy | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 停止権限をAgentが変更不可 |

成功と失敗の両方について、設定だけでなく実際の結果を採用構成へ対応付ける。
本Repositoryには期待値のみを置き、本番Evidence、Secret、顧客情報は保存しない。
特定の監査製品やログ形式は、本Controlが明示する性質を満たすための唯一の方式ではない。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C9.1.3` | 全群停止 |
| `v1.0-C9.6.1` | 推論・出力停止 |
| `v1.0-C5.2.5` | PDPの隔離 |

## Known limitations and uncertainty

共有基盤の全面障害や管理者侵害までは独立経路だけで解決しない。停止遅延・残処理・再開権限を具体的に記録する。

`verifiable`は本Artifactに解釈・脅威・検証・証拠期待値が揃った状態を表す。
製品試験の実施・製品適合・学習完了を意味しない。有限の試験で未知の攻撃を全て否定しない。
Engineering PatternとMappingは独立して評価し、その存在を本Controlの成熟条件にしない。

## References

- [AISVS v1.0 C9要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
- [AISVS v1.0 対応Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-06-Shutdown-Graceful-Degradation.md)
- [C9全体分析](../../../docs/c09-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-09 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |

