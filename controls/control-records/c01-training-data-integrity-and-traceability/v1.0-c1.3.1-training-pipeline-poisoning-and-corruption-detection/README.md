---
title: 学習経路で毒入れと偶発的な破損の疑いを検出する
versioned_id: v1.0-C1.3.1
requirement_id: C1.3.1
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

# 学習経路で毒入れと偶発的な破損の疑いを検出する

AISVS Verification Level: 2

[C1.3 Section講義](../../../learning/c01-training-data-integrity-and-traceability/v1.0-c1.3-training-data-quality-and-security-assurance.md)

## Upstream basis

AISVS `v1.0-C1.3.1`は、学習・追加学習Pipelineへ毒入れ検出技術を組み込み、疑わしい毒入れや偶発的な破損を識別する。
Researchは形式・分布・異常やBackdoor兆候を組み合わせ、単一検出器では全攻撃を捉えられないと注意する。特定のLibraryや全異常の自動削除を原文が要求するわけではない。
採用基準は固定Revisionのv1.0であり、1.01への移行ではない。
以下の検証・証拠の具体化はRepositoryの解釈である。

## Interpretation

使用する学習・追加学習経路の実Dataに、想定する毒入れと破損の検出処理が適用される。
正常例と無害な模擬毒入れ・破損例で検出結果を確認し、対象攻撃・しきい値・見逃しを記録する。
検出した対象とDataset版が追跡可能で、検出失敗や未実行を検査成功として扱わない。
特定製品の導入や設定の存在だけで実効性を判断しない。

## Security objective

学習・追加学習Pipelineへ毒入れ検出技術を組み込み、疑わしい毒入れや偶発的な破損を識別する。
攻撃者の投稿や合成Dataを収集する経路から、特定の反応を植え付ける例が混入する。処理不良による破損も、単なるSource署名検証だけでは見つからない。

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
| SP-1 | 使用する学習・追加学習経路の実Dataに、想定する毒入れと破損の検出処理が適用される。 |
| SP-2 | 正常例と無害な模擬毒入れ・破損例で検出結果を確認し、対象攻撃・しきい値・見逃しを記録する。 |
| SP-3 | 検出した対象とDataset版が追跡可能で、検出失敗や未実行を検査成功として扱わない。 |

## Scope calibration and adjacent assurance

C1.3.4は明示された禁止内容の学習前除去まで問う。C1.3.5は正しいLabelを持つ攻撃への防御であり、一般的な異常検出だけで代替しない。
本ControlがPassでも、他のC1要件やモデル全体の安全性を満たしたことにはならない。

## Threat and failure-mode rationale

攻撃者の投稿や合成Dataを収集する経路から、特定の反応を植え付ける例が混入する。処理不良による破損も、単なるSource署名検証だけでは見つからない。
外部脅威IDとの厳密なMappingは未評価。用語の一致だけによるMappingは追加しない。

## Verification

### Architecture and configuration review

対象Datasetの収集から実際の学習入力までの経路を辿り、SP-1〜SP-3の判定点と証拠の作成元を確認する。
委託、手動Export、再実行、Cache、派生物の経路が通常Jobと異ならないか点検する。

### Positive verification

合成の正常Datasetと、定義した異常・破損を加えたDatasetを同じ処理へ通し、正常例の誤検知と異常例の検出を観測する。
対象版、処理設定、観測点、期待値、実測結果を保存し、SP-1〜SP-3をそれぞれ評価する。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | 主経路を通らない追加学習JobからDataを投入する | 検査範囲の欠落を発見し、全経路を検査したと主張しない。 |
| N-2 | Scannerを停止するか例外を返させる | 検査不能と正常を区別し、成功結果を作らない。 |
| N-3 | 署名が正しい模擬汚染Dataを投入する | 完全性検証だけで内容検査を省かない。定義した攻撃クラスの検出結果を確認する。 |

### Failure conditions

対象Pipelineに検出処理がない、実Dataへ適用されない、定義した検証例で検出を立証できない場合はFailまたは証拠不足。
観測できない範囲や欠落証拠は未立証として残し、設定や説明文だけで合格を宣言しない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認時期 | 完全性と機微性 | 合格の目安 |
|---|---|---|---|---|---|
| 対象一覧と設計・設定 | Data管理者と学習基盤担当者 | Dataset版、経路、SP-1〜SP-3の判定点 | 採用時と経路変更時 | 権限付き管理。実Dataは公開しない | 各性質がどの実入力に適用されるか追える |
| 正例・負例の実測記録 | 検証担当者 | 上記Positive試験とN-1〜N-3 | 初回とDataset・処理・検証方式の変更時 | 合成Dataを使い、設定版と結果を結び付ける | 期待結果を実測し、失敗・未観測範囲も記録する |
| 運用時の判定記録 | 対象Pipelineと運用担当者 | 実際に使用するDataset版 | 各処理または定義した評価周期 | 不正改変から保護し、内容・秘密を最小化 | 判定と対象版が一致し、古い成功結果を流用しない |

## Related requirements

[C1.3.4](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.3.4-remove-disallowed-content-before-training/README.md)は明示された禁止内容の学習前除去まで問う。[C1.3.5](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.3.5-clean-label-poisoning-defenses/README.md)は正しいLabelを持つ攻撃への防御であり、一般的な異常検出だけで代替しない。
[C1 Family概要](../README.md)から隣接Requirementへ進める。Engineering Mappingは別途評価する。

## Known limitations and uncertainty

検出は確率的であり、既知の模擬例の成功は未知の攻撃の不在を証明しない。検出後の処置は別途定めるが、本要件だけから全疑い例の自動削除を義務にしない。
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
