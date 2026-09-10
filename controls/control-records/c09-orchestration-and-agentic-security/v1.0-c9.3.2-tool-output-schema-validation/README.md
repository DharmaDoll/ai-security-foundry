---
title: "ツール出力をSchemaに照らして検証する"
versioned_id: "v1.0-C9.3.2"
requirement_id: "C9.3.2"
verification_level: 1
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

# ツール出力をSchemaに照らして検証する

AISVS Verification Level: 1

## Upstream basis

AISVS `v1.0-C9.3.2`を解釈する。要件本文はツール出力をSchemaで検証することを求める。
採用済みstable v1.0の固定Revisionで本文と対応Researchの要件別検証・限界を確認した。
最新の版・製品への追従を意味しない。

Researchは型・Field・Size等の検証を補足するが、引数からShellへの検証案は本要件の出力対象と区別する。Schema内の意味的攻撃は残る。
以下の具体例・Property・検証条件はRepository interpretationである。
Researchの製品、統計、事件、外部Framework Mappingを未検証のまま転記せず、
例示された実装方式を一律の適合条件にしない。

## Interpretation

ツールから戻る値を、合意した出力契約に適合するか確認してから利用する。信頼するツール名でも戻り値を無条件にモデルや後段へ渡さない。

数値の残高を期待するFieldへObjectや過大な文字列が返ったら、成功値として採用しない。一方、正しい文字列型に注入文が含まれることはSchema検証だけでは見抜けない。

## Security objective

不正形式・契約外の出力で後段処理を誤動作させる経路を減らす。

## Applicability

構造化・非構造化・Streamを含むツール出力の利用経路。

### Non-applicability

ツール出力を利用しない範囲は対象外。自由Textでも型・構造・境界の契約を定められるため、自由Textという理由だけで除外しない。

## Scope and assumptions

Schemaは出力の型・必須項目・許容値等の契約。必要なSize上限や未知Fieldの扱いを用途に応じて定義する。外部値を全て受け入れるSchemaで実質的に無検証にしない。

対象構成・採用Policy・許容する動作と評価境界を検証前に固定する。
不明な構成を安全と仮定せず、未確認範囲をEvidenceの不足として残す。

## Assets, actors, identities, and trust boundaries

資産は後段処理の入力契約。外部Tool、Validation層、モデル・Consumerを区別し、最初の使用前に強制する。

## Required security properties

Security Invariantは守るべき性質、Enforcement Pointはそれを実際に強制する場所を指す。

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | ツール・版ごとに有用な出力契約がある。 |
| SP-2 | 成功・Error・Stream完了等の使用経路で検証する。 |
| SP-3 | 契約違反を成功Dataとして後段へ渡さない。 |

## Scope calibration and adjacent assurance

Schema適合は内容の真実性・権限・Prompt Injection耐性を証明しない。Schema内の悪意ある文への能力分離はC9.3.6等。

## Threat and failure-mode rationale

侵害Toolが型・必須値・構造を崩し、Consumerの誤解釈や検証の例外経路を使う。

この保証の分析では外部脅威IDを付与する追加価値を確定していない。
攻撃者能力・失敗経路を具体化し、`threat_mappings`は空とする。
ResearchのMappingを自動採用せず、必要時に一次Sourceの固定版で別途評価する。

## Verification

### Architecture and configuration review

Tool版とSchema、成功・Error経路、Streamの組立と検証時点、Consumerの使用開始を追う。

### Positive verification

有効な出力と有効なErrorを通し、規定した結果として利用されることを示す。

### Negative and abuse-case verification

許可された試験環境と模擬Dataを用いる。モデルが協力することに依存せず、
必要に応じて実行境界へ試験要求を直接与える。

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 必須Field欠落・型違反を返す | 後段で成功値として利用しない。SP-1, SP-3 |
| N-2 | 契約外Size・未知Fieldを返す | 定義したSchema規則どおり扱う。SP-1 |
| N-3 | Error経路から不正形式を返す | 例外経路でも検証する。SP-2 |
| N-4 | Stream途中は正常で終端を不正にする | 未検証の完成値を使用しない。SP-2, SP-3 |

### Failure conditions

上表の期待結果に反する観測やSPの不成立は、本ControlのFailを裏付ける。
試験未実施、構成不明、結果を追跡できない場合はPassを裏付ける証拠不足であり、
実証された回避と区別する。隣接要件の不備だけで本Controlの意味を広げない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 出力Schema | Tool・Consumer管理者 | 各版と戻り経路 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 実際の契約を表す |
| 契約試験 | 検証者 | 正常・不正・Error・Stream | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 未検証の利用がない |
| Data Flow | Application管理者 | ToolからConsumer | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 使用前の検証位置を確認 |

成功と失敗の両方について、設定だけでなく実際の結果を採用構成へ対応付ける。
本Repositoryには期待値のみを置き、本番Evidence、Secret、顧客情報は保存しない。
特定の監査製品やログ形式は、本Controlが明示する性質を満たすための唯一の方式ではない。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C9.3.6` | Tool出力の分離 |
| `v1.0-C9.3.3` | 出力検証要件の宣言 |
| `v1.0-C9.3.4` | 宣言の強制 |

## Known limitations and uncertainty

正しい形式の嘘・機密情報・注入文は残る。Parser差、過度な型変換、巨大出力の取込前資源消費も別途評価する。

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

