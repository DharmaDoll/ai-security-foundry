---
title: "承認画面に実際の操作内容を完全かつ正確に示す"
versioned_id: "v1.0-C9.2.2"
requirement_id: "C9.2.2"
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

# 承認画面に実際の操作内容を完全かつ正確に示す

AISVS Verification Level: 2

初めて読む方へ：[具体例・用語・対話を含む学習ノート](learning.md)。

## Upstream basis

AISVS `v1.0-C9.2.2`を解釈する。要件本文は承認要求に正規化した完全な操作引数を、切り詰めや危険な変換なしで表示することを求める。
採用済みstable v1.0の固定Revisionで本文と対応Researchの要件別検証・限界を確認した。
最新の版・製品への追従を意味しない。

Researchは長いDiff、制御文字、モデルの要約、AliasやSymlinkの解決結果と表示の食い違いを補足する。Researchの暗号的結合案はC9.2.8と分ける。
以下の具体例・Property・検証条件はRepository interpretationである。
Researchの製品、統計、事件、外部Framework Mappingを未検証のまま転記せず、
例示された実装方式を一律の適合条件にしない。

## Interpretation

人が承認する材料を、信頼する実行要求から作る。モデルの説明が『Cache削除』でも実対象が本番Dataなら、その対象を隠さず表示する。

長いコマンドの末尾だけに危険な対象がある場合、先頭だけの省略表示では足りない。折り畳みやページ分けを用いても全内容を確認でき、重要部分が失われた要約だけで承認できない設計にする。

## Security objective

表示と実態の差による誤承認、承認者を欺く内容の隠蔽を抑える。

## Applicability

人に操作内容を示して承認を求めるUI、CLI、通知・API。

### Non-applicability

承認要求を作らない範囲は対象外。C9.2.1上必要な承認そのものが欠落している場合は、その不備を先に記録する。

## Scope and assumptions

Canonicalizationは別名や表現差を実行上の意味へ揃えること。危険な制御文字は無害に表示するが、操作の意味や対象を削ってはならない。Secretそのものを表示する必要が生じないよう、操作は権限参照等で設計する。

対象構成・採用Policy・許容する動作と評価境界を検証前に固定する。
不明な構成を安全と仮定せず、未確認範囲をEvidenceの不足として残す。

## Assets, actors, identities, and trust boundaries

保護対象は人の判断材料。モデル・ツール由来の文字列、信頼する操作Object、表示Renderer、人を分ける。強制点は承認要求の生成・表示であり、説明文の生成モデルではない。

## Required security properties

Security Invariantは守るべき性質、Enforcement Pointはそれを実際に強制する場所を指す。

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 表示は承認対象の正規化された実行要求に由来する。 |
| SP-2 | 対象・値・Scope・変更内容を失わず確認できる。 |
| SP-3 | 表示制御文字・Markup等が重要部分を隠したり別の操作に見せたりしない。 |

## Scope calibration and adjacent assurance

完全に表示できても実行前に引数を変えられるならC9.2.8等で別評価。全内容が閲覧可能でも実際に人が理解した保証はない。

## Threat and failure-mode rationale

攻撃者が長い入力、不可視文字、偽Diff、Pathの別名を使って、承認者には無害な操作だけを見せる。

この保証の分析では外部脅威IDを付与する追加価値を確定していない。
攻撃者能力・失敗経路を具体化し、`threat_mappings`は空とする。
ResearchのMappingを自動採用せず、必要時に一次Sourceの固定版で別途評価する。

## Verification

### Architecture and configuration review

実行要求から表示への変換を追い、Path解決、Diff生成、省略、折り畳み、文字escape、画面幅の影響を確認する。

### Positive verification

短い要求と長いDiffの双方で、実対象・送信先・金額・Scopeを元要求と照合する。閲覧経路から全変更を復元できることを確認する。

### Negative and abuse-case verification

許可された試験環境と模擬Dataを用いる。モデルが協力することに依存せず、
必要に応じて実行境界へ試験要求を直接与える。

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 危険な引数を長文末尾へ置く | 切り詰めず確認可能。表示不能なら承認を進めない。SP-2 |
| N-2 | Markup・端末制御文字・方向制御文字を挿入 | 意味を可視化して誤表示を防ぐ。SP-3 |
| N-3 | 無害なAliasを保護対象へ解決させる | 実際の対象を表示し、解決不能なら確定操作として承認させない。SP-1 |
| N-4 | モデルの要約と実要求を矛盾させる | 実要求に基づく表示が維持される。SP-1, SP-2 |

### Failure conditions

上表の期待結果に反する観測やSPの不成立は、本ControlのFailを裏付ける。
試験未実施、構成不明、結果を追跡できない場合はPassを裏付ける証拠不足であり、
実証された回避と区別する。隣接要件の不備だけで本Controlの意味を広げない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 操作Objectと表示対照 | 表示基盤・検証者 | 各UIと操作種別 | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 省略や意味変化がない |
| Rendererと解決規則 | Application管理者 | 文字・Path・Diff | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 信頼元と変換が追跡可能 |
| 悪意ある表示試験 | 検証者 | 長文・制御文字・Alias | 対象機構・Policy変更後、定期回帰時 | 評価Revision・時刻・試験IDを保持。アクセス制限し模擬Dataを使う | 危険部分を隠せない |

成功と失敗の両方について、設定だけでなく実際の結果を採用構成へ対応付ける。
本Repositoryには期待値のみを置き、本番Evidence、Secret、顧客情報は保存しない。
特定の監査製品やログ形式は、本Controlが明示する性質を満たすための唯一の方式ではない。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C9.2.1` | 承認の実行前強制 |
| `v1.0-C9.2.8` | 承認した要求と実行の暗号的結合 |

## Known limitations and uncertainty

大きい操作は人の認知負荷が高い。安全な小単位へ分割する運用を検討する。表示の正確さは復元可能性や認可の妥当性を保証しない。

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

