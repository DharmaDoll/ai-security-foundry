---
title: すべての学習データ源の台帳と加工履歴を維持する
versioned_id: v1.0-C1.1.2
requirement_id: C1.1.2
verification_level: 2
family_id: C1
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C01-Training-Data-Integrity-and-Traceability.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C01-Training-Data/C01-01-Training-Data-Origin-Traceability.md
last_verified: '2026-10-17'
maturity: verifiable
mapping_assessment_refs: []
---

# すべての学習データ源の台帳と加工履歴を維持する

AISVS Verification Level: 2

[C1.1 Section講義](../../../learning/c01-training-data-integrity-and-traceability/v1.0-c1.1-training-data-origin-and-security.md)

## Upstream basis

AISVS `v1.0-C1.1.2`は、全学習データ源について、出所・責任者・License・収集方法・利用条件・加工履歴の六項目を最新に保つ。
Researchは台帳と実際の入力を照合し、手作業の加工や古い責任者による来歴の断絶も調べる。特定のCatalog製品や公開開示形式は原文の必須条件ではない。
採用基準は固定Revisionのv1.0であり、1.01への移行ではない。
以下の検証・証拠の具体化はRepositoryの解釈である。

## Interpretation

実際の学習入力を構成する全Sourceを列挙し、六項目を空欄や意味のない仮値で済ませない。
加工・結合・収集元や利用条件の変更を台帳へ反映し、対象Dataset版から元Sourceと処理を追える。
台帳の記載を収集記録や提供元資料と照合し、責任者と更新時点を確認できる。
特定製品の導入や設定の存在だけで実効性を判断しない。

## Security objective

全学習データ源について、出所・責任者・License・収集方法・利用条件・加工履歴の六項目を最新に保つ。
担当者がNotebookで追加したDatasetが台帳を通らず、汚染判明後もどのSourceと加工に由来するか追えなくなる。

## Applicability

自社または委託先でモデルの学習・追加学習に使うDatasetと、その準備・加工・保存・受渡しを対象とする。
Providerへ委託する場合も、扱うDataと証拠の責任境界を定める。

### Non-applicability

既存モデルに検索文書を渡すだけで、その文書が学習へ入らないRAGは通常直接の対象外。
Providerが入力を学習へ再利用する場合は契約・設定・実際のData Flowを確認する。
Provider内部が非公開であることだけを理由に対象外とはしない。証拠不足をPassへ読み替えない。

## Scope and assumptions

対象モデル、Dataset版、Source、処理経路、担当者と委託範囲を先に固定する。
正例・負例には機密情報を含まない合成Dataを使う。検証する経路と未観測の経路を区別し、
一部のDatasetの成功を全学習へ広げない。変更後は対象範囲と証拠の鮮度を再確認する。

## Assets, actors, identities, and trust boundaries

守る資産は対象Dataset、その版と処理記録、本Controlの判定に使う証拠。
収集元、Data管理者、加工Job、学習Worker、外部委託先と、Dataを書換え・持出しできる攻撃者を区別する。
候補Dataから承認済みDatasetへ、加工・保管・転送から実際の学習読込みへ進む境界を追う。
Data管理者と検証基準・検出結果を管理する主体の権限が重なる場合、その改変可能性を点検する。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 実際の学習入力を構成する全Sourceを列挙し、六項目を空欄や意味のない仮値で済ませない。 |
| SP-2 | 加工・結合・収集元や利用条件の変更を台帳へ反映し、対象Dataset版から元Sourceと処理を追える。 |
| SP-3 | 台帳の記載を収集記録や提供元資料と照合し、責任者と更新時点を確認できる。 |

## Scope calibration and adjacent assurance

C12.5.1の全体LineageやC6の供給元評価と関係するが、本Controlは全Sourceの六項目と更新性を個別に確かめる。
本ControlがPassでも、他のC1要件やモデル全体の安全性を満たしたことにはならない。

## Threat and failure-mode rationale

担当者がNotebookで追加したDatasetが台帳を通らず、汚染判明後もどのSourceと加工に由来するか追えなくなる。
外部脅威IDとの厳密なMappingは未評価。用語の一致だけによるMappingは追加しない。

## Verification

### Architecture and configuration review

対象Datasetの収集から実際の学習入力までの経路を辿り、SP-1〜SP-3の判定点と証拠の作成元を確認する。
委託、手動Export、再実行、Cache、派生物の経路が通常Jobと異ならないか点検する。

### Positive verification

二つの合成Sourceを加工・結合し、最終Dataset版から両Sourceの六項目と処理順序まで追跡する。
対象版、処理設定、観測点、期待値、実測結果を保存し、SP-1〜SP-3をそれぞれ評価する。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | Notebookから未登録Sourceを混ぜる | 実入力との照合で欠落を検出し、全Source登録済みと判定しない。 |
| N-2 | Licenseと利用条件を空欄にする | 六項目が揃わないためPassにしない。不明点を明示するだけでは充足にならない。 |
| N-3 | 加工Jobと責任者を変え、台帳を更新しない | 実態との差異を検出し、旧版の記録を現在の証拠へ流用しない。 |

### Failure conditions

未登録Source、六項目の欠落、実態と不一致な履歴があればFail。出所を追えない場合は証拠不足として残す。
観測できない範囲や欠落証拠は未立証として残し、設定や説明文だけで合格を宣言しない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認時期 | 完全性と機微性 | 合格の目安 |
|---|---|---|---|---|---|
| 対象一覧と設計・設定 | Data管理者と学習基盤担当者 | Dataset版、経路、SP-1〜SP-3の判定点 | 採用時と経路変更時 | 権限付き管理。実Dataは公開しない | 各性質がどの実入力に適用されるか追える |
| 正例・負例の実測記録 | 検証担当者 | 上記Positive試験とN-1〜N-3 | 初回とDataset・処理・検証方式の変更時 | 合成Dataを使い、設定版と結果を結び付ける | 期待結果を実測し、失敗・未観測範囲も記録する |
| 運用時の判定記録 | 対象Pipelineと運用担当者 | 実際に使用するDataset版 | 各処理または定義した評価周期 | 不正改変から保護し、内容・秘密を最小化 | 判定と対象版が一致し、古い成功結果を流用しない |

## Related requirements

[C12.5.1](../../../../controls/control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.5.1-record-complete-dataset-lineage/README.md)の全体LineageやC6の供給元評価と関係するが、本Controlは全Sourceの六項目と更新性を個別に確かめる。
[C1 Family概要](../README.md)から隣接Requirementへ進める。Engineering Mappingは別途評価する。

## Known limitations and uncertainty

台帳の完全性はSourceの安全性やLicenseの法的有効性を単独では証明しない。外部提供元の申告の真偽には検証限界がある。
本書の`verifiable`はControl文書の成熟度であり、実製品での試験完了や適合認定ではない。

## References

- [AISVS v1.0 C1 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C01-Training-Data-Integrity-and-Traceability.md)
- [AISVS v1.0 C1.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C01-Training-Data/C01-01-Training-Data-Origin-Traceability.md)
- [C1.1 Section講義](../../../learning/c01-training-data-integrity-and-traceability/v1.0-c1.1-training-data-origin-and-security.md)
- [C1 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-17 | 初版。要件固有の性質、合否、正負試験と証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品での試験は未実施 |
