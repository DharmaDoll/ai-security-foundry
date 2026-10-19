---
title: セキュリティ判断に使うモデルの偏りを評価する
versioned_id: v1.0-C1.3.3
requirement_id: C1.3.3
verification_level: 2
family_id: C1
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C01-Training-Data-Integrity-and-Traceability.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C01-Training-Data/C01-03-Training-Data-Quality-Security-Assurance.md
last_verified: '2026-10-17'
maturity: verifiable
mapping_assessment_refs: []
---

# セキュリティ判断に使うモデルの偏りを評価する

AISVS Verification Level: 2

[C1.3 Section講義](../../../learning/c01-training-data-integrity-and-traceability/v1.0-c1.3-training-data-quality-and-security-assurance.md)

## Upstream basis

AISVS `v1.0-C1.3.3`は、セキュリティに関係する判断へ使うモデルで偏りのパターンを評価する。
Researchは条件別の偽陽性・偽陰性と回避可能性を調べ、全体平均が条件別の盲点を隠すと注意する。原文は全群の指標一致や特定の公平性Libraryを要求していない。
採用基準は固定Revisionのv1.0であり、1.01への移行ではない。
以下の検証・証拠の具体化はRepositoryの解釈である。

## Interpretation

対象Modelの出力が実際にセキュリティ判断へ使われる経路と影響を特定する。
用途に関係する集団・入力条件と比較指標を定義し、条件別の偏りを評価する。単なる全体平均で済ませない。
利用中のModel版・設定と評価結果を結び付け、少数標本や未評価条件を明記する。
特定製品の導入や設定の存在だけで実効性を判断しない。

## Security objective

セキュリティに関係する判断へ使うモデルで偏りのパターンを評価する。
不正判定Modelが特定言語や入力属性で攻撃を見逃しても、全体正解率に埋もれる。攻撃者はその条件を選び検査を回避する。

## Applicability

セキュリティに関係する判断へ使うモデルに適用する。自社学習かProvider提供かを問わず、
不正検知・アクセス判断・安全性Filter等へ実際に影響する経路を確認する。

### Non-applicability

セキュリティ判断へ使わない話題整理等は対象外。RAGを使うだけでも、そのモデルが
セキュリティ判断を左右するなら適用され得る。評価Dataが足りないことは対象外の理由にしない。

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
| SP-1 | 対象Modelの出力が実際にセキュリティ判断へ使われる経路と影響を特定する。 |
| SP-2 | 用途に関係する集団・入力条件と比較指標を定義し、条件別の偏りを評価する。単なる全体平均で済ませない。 |
| SP-3 | 利用中のModel版・設定と評価結果を結び付け、少数標本や未評価条件を明記する。 |

## Scope calibration and adjacent assurance

FAQへの話題タグ付け等、セキュリティ判断に使わないModelは本要件の対象外。後にアクセス判断等へ転用されれば再評価する。C11の攻撃耐性とも別の保証。
本ControlがPassでも、他のC1要件やモデル全体の安全性を満たしたことにはならない。

## Threat and failure-mode rationale

不正判定Modelが特定言語や入力属性で攻撃を見逃しても、全体正解率に埋もれる。攻撃者はその条件を選び検査を回避する。
外部脅威IDとの厳密なMappingは未評価。用語の一致だけによるMappingは追加しない。

## Verification

### Architecture and configuration review

対象Datasetの収集から実際の学習入力までの経路を辿り、SP-1〜SP-3の判定点と証拠の作成元を確認する。
委託、手動Export、再実行、Cache、派生物の経路が通常Jobと異ならないか点検する。

### Positive verification

無害な不正判定模擬Dataを言語や入力条件で分け、条件別の見逃し・誤拒否を比較する。発見した差と標本数、未評価範囲を記録する。
対象版、処理設定、観測点、期待値、実測結果を保存し、SP-1〜SP-3をそれぞれ評価する。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | 全体精度は同じまま一条件の見逃しを増やす | 層別の評価で偏りを観測できる。全体平均の合格だけで済ませない。 |
| N-2 | 一条件の試験Dataを空にする | 偏りゼロと表示せず評価不能として記録する。 |
| N-3 | モデル更新後に旧版の評価を提出する | 現在の版の証拠にならないと識別する。 |

### Failure conditions

対象となるModelで偏りを評価していない、または全体指標だけで偏りを評価済みとする場合はFail。偏りの発見自体は評価の未実施とは異なる。
観測できない範囲や欠落証拠は未立証として残し、設定や説明文だけで合格を宣言しない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認時期 | 完全性と機微性 | 合格の目安 |
|---|---|---|---|---|---|
| 対象一覧と設計・設定 | Data管理者と学習基盤担当者 | Dataset版、経路、SP-1〜SP-3の判定点 | 採用時と経路変更時 | 権限付き管理。実Dataは公開しない | 各性質がどの実入力に適用されるか追える |
| 正例・負例の実測記録 | 検証担当者 | 上記Positive試験とN-1〜N-3 | 初回とDataset・処理・検証方式の変更時 | 合成Dataを使い、設定版と結果を結び付ける | 期待結果を実測し、失敗・未観測範囲も記録する |
| 運用時の判定記録 | 対象Pipelineと運用担当者 | 実際に使用するDataset版 | 各処理または定義した評価周期 | 不正改変から保護し、内容・秘密を最小化 | 判定と対象版が一致し、古い成功結果を流用しない |

## Related requirements

FAQへの話題タグ付け等、セキュリティ判断に使わないModelは本要件の対象外。後にアクセス判断等へ転用されれば再評価する。C11の攻撃耐性とも別の保証。
[C1 Family概要](../README.md)から隣接Requirementへ進める。Engineering Mappingは別途評価する。

## Known limitations and uncertainty

群の選び方や標本数による盲点が残る。本要件は評価を求めるもので、すべての格差解消や普遍的な数値基準への到達を単独で要求しない。
本書の`verifiable`はControl文書の成熟度であり、実製品での試験完了や適合認定ではない。

## References

- [AISVS v1.0 C1 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C01-Training-Data-Integrity-and-Traceability.md)
- [AISVS v1.0 C1.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C01-Training-Data/C01-03-Training-Data-Quality-Security-Assurance.md)
- [C1.3 Section講義](../../../learning/c01-training-data-integrity-and-traceability/v1.0-c1.3-training-data-quality-and-security-assurance.md)
- [C1 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-17 | 初版。要件固有の性質、合否、正負試験と証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品での試験は未実施 |
