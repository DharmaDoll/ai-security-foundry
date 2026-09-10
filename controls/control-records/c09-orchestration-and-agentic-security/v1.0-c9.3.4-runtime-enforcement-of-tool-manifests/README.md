---
title: "Tool Manifestの制約をRuntimeが強制する"
versioned_id: "v1.0-C9.3.4"
requirement_id: "C9.3.4"
verification_level: 2
family_id: "C9"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-03-Tool-and-Plugin-Isolation.md"
last_verified: "2026-09-09"
maturity: "verifiable"
mapping_assessment_refs: []
---

# Tool Manifestの制約をRuntimeが強制する

AISVS Verification Level: 2

## Upstream basis

AISVS `v1.0-C9.3.4`を解釈する。要件本文はManifestに宣言された権限・資源制限・出力検証要件をRuntimeが強制することを求める。
採用済みstable v1.0の固定Revisionで本文と対応Researchの要件別検証・限界を確認した。
最新の版・製品への追従を意味しない。

Researchは宣言をFile・Network・Quota・Validator等の実効設定へ照合し、制限違反を試験する方法を補足する。
以下の具体例・Property・検証条件はRepository interpretationである。
Researchの製品、統計、事件、外部Framework Mappingを未検証のまま転記せず、
例示された実装方式を一律の適合条件にしない。

## Interpretation

Manifestを登録資料で終わらせず、宣言より広い能力を与えない実行設定へ結び付ける。実行物が更新されても旧契約の確認だけで新しい権限を暗黙に与えない。

通信不要と宣言したToolが外部へ接続できるなら宣言の強制は不成立。GatewayでTool名を制限していても、Tool Processの広い通信権限までは制限していない場合がある。

## Security objective

契約と実行能力のずれから生じる過大権限・資源濫用・不正出力を防ぐ。

## Applicability

Manifestの制約を持つToolを実行するRuntime。

### Non-applicability

ツールがない範囲は対象外。Manifest欠落はC9.3.3の不足として記録し、無制限実行を正当化しない。

## Scope and assumptions

宣言から実設定への変換と非対応項目を明示。強制できない必須制限は『設定済み』と扱わず登録・実行を止める等で対処する。

対象構成・採用Policy・許容する動作と評価境界を検証前に固定する。
不明な構成を安全と仮定せず、未確認範囲をEvidenceの不足として残す。

## Assets, actors, identities, and trust boundaries

資産は宣言された能力境界。登録・起動・実行・出力処理を分け、各制約を実際に止める場所へ結ぶ。

## Required security properties

Security Invariantは守るべき性質、Enforcement Pointはそれを実際に強制する場所を指す。

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 宣言と実行物・有効設定が対応する。 |
| SP-2 | 権限・資源・出力検証の全対象制約を強制する。 |
| SP-3 | 未知・破損宣言や障害時に無制限実行へ落ちない。 |

## Scope calibration and adjacent assurance

Manifest強制はAgentのユーザ別認可やモデル出力の意味的安全性を代替しない。安全なSchemaに見える注入は別保証。

## Threat and failure-mode rationale

Toolが宣言を偽るか起動設定を変え、未宣言のNetwork・File能力を使う。

この保証の分析では外部脅威IDを付与する追加価値を確定していない。
攻撃者能力・失敗経路を具体化し、`threat_mappings`は空とする。
ResearchのMappingを自動採用せず、必要時に一次Sourceの固定版で別途評価する。

## Verification

### Architecture and configuration review

宣言の各項目に強制点と試験を対応付け、起動Option・別経路・Fallbackを追う。

### Positive verification

制限内のTool呼出しで必要処理が完了し、出力Schemaに適合する結果だけが利用されることを示す。

### Negative and abuse-case verification

許可された試験環境と模擬Dataを用いる。モデルが協力することに依存せず、
必要に応じて実行境界へ試験要求を直接与える。

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 未宣言Pathや宛先へアクセス | 実制約で拒否。SP-2 |
| N-2 | 宣言した資源上限を超過 | 定義した抑制・停止を実測。SP-2 |
| N-3 | Schema外の出力を返す | 利用前に拒否。SP-2 |
| N-4 | 宣言差替え・未対応制限・読込障害 | 広い権限で起動・継続しない。SP-1, SP-3 |

### Failure conditions

上表の期待結果に反する観測やSPの不成立は、本ControlのFailを裏付ける。
試験未実施、構成不明、結果を追跡できない場合はPassを裏付ける証拠不足であり、
実証された回避と区別する。隣接要件の不備だけで本Controlの意味を広げない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 宣言と強制設定の対応表 | Runtime管理者 | 全制約 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 未強制項目がない |
| 3種制約の試験 | 検証者 | 権限・資源・出力 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 実動作で制約を示す |
| 版変更・障害結果 | 登録・起動基盤 | 更新とFallback | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 暗黙の権限拡大を防ぐ |

成功と失敗の両方について、設定だけでなく実際の結果を採用構成へ対応付ける。
本Repositoryには期待値のみを置き、本番Evidence、Secret、顧客情報は保存しない。
特定の監査製品やログ形式は、本Controlが明示する性質を満たすための唯一の方式ではない。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C9.3.3` | 宣言契約 |
| `v1.0-C9.3.1` | 最小権限隔離 |
| `v1.0-C9.5.1` | 呼出主体と引数の認可 |

## Known limitations and uncertainty

宣言そのものが過大なら忠実な強制でも危険。遠隔側の実行権限は責任分界を明記し、GatewayだけでProcess隔離を保証しない。

`verifiable`は本Artifactに解釈・脅威・検証・証拠期待値が揃った状態を表す。
製品試験の実施・製品適合・学習完了を意味しない。有限の試験で未知の攻撃を全て否定しない。
Engineering PatternとMappingは独立して評価し、その存在を本Controlの成熟条件にしない。

## References

- [AISVS v1.0 C9要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
- [AISVS v1.0 対応Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-03-Tool-and-Plugin-Isolation.md)
- [C9全体分析](../../../docs/c09-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-09 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |

