---
title: 学習項目をモデルの目的に必要なものへ限定する
versioned_id: v1.0-C1.1.1
requirement_id: C1.1.1
verification_level: 1
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

# 学習項目をモデルの目的に必要なものへ限定する

AISVS Verification Level: 1

[C1.1 Section講義](../../../learning/c01-training-data-integrity-and-traceability/v1.0-c1.1-training-data-origin-and-security.md)

## Upstream basis

AISVS `v1.0-C1.1.1`は、学習データに含める特徴量・属性・項目を、モデルが明示した目的に必要な範囲へ限る。
ResearchはFieldごとの必要性の説明と許可項目の選択を重視する。機密情報Scannerだけでは業務上の必要性を判定できない。
採用基準は固定Revisionのv1.0であり、1.01への移行ではない。
以下の検証・証拠の具体化はRepositoryの解釈である。

## Interpretation

利用するモデルの目的と、残す各Fieldの必要性を対応付けて説明できる。
学習が実際に消費する加工後データでも、不要なField・属性を除外する。自由文や派生Fieldに同じ情報が残る経路も確認する。
目的・Schema・加工処理が変わった際、項目選択と実データの検査結果を更新する。
特定製品の導入や設定の存在だけで実効性を判断しない。

## Security objective

学習データに含める特徴量・属性・項目を、モデルが明示した目的に必要な範囲へ限る。
分類用の問い合わせ本文に付随する電話番号や内部認証情報が、既定の全列Exportで学習へ混入する。不要な情報の記憶・推測・抽出の影響を広げる。

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
| SP-1 | 利用するモデルの目的と、残す各Fieldの必要性を対応付けて説明できる。 |
| SP-2 | 学習が実際に消費する加工後データでも、不要なField・属性を除外する。自由文や派生Fieldに同じ情報が残る経路も確認する。 |
| SP-3 | 目的・Schema・加工処理が変わった際、項目選択と実データの検査結果を更新する。 |

## Scope calibration and adjacent assurance

C1.1.2は出所台帳、C1.3.4は禁止Contentの排除。必要な項目であることと、内容が安全であることを混同しない。
本ControlがPassでも、他のC1要件やモデル全体の安全性を満たしたことにはならない。

## Threat and failure-mode rationale

分類用の問い合わせ本文に付随する電話番号や内部認証情報が、既定の全列Exportで学習へ混入する。不要な情報の記憶・推測・抽出の影響を広げる。
外部脅威IDとの厳密なMappingは未評価。用語の一致だけによるMappingは追加しない。

## Verification

### Architecture and configuration review

対象Datasetの収集から実際の学習入力までの経路を辿り、SP-1〜SP-3の判定点と証拠の作成元を確認する。
委託、手動Export、再実行、Cache、派生物の経路が通常Jobと異ならないか点検する。

### Positive verification

合成問い合わせから不要な電話番号列を除き、必要な本文と分類目的に使う項目だけが最終学習入力へ残ることを確認する。
対象版、処理設定、観測点、期待値、実測結果を保存し、SP-1〜SP-3をそれぞれ評価する。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | 未知の列をSourceへ追加する | 既定の全列取込みで学習へ混入しない。採用するなら必要性を再評価する。 |
| N-2 | 削除した電話番号を自由文や派生列へ複製する | 列名だけの検査では見落とす経路を発見し、不要な内容を除く。 |
| N-3 | 別目的の古いField一覧を流用する | 現在の目的に必要との根拠にならず、再評価する。 |

### Failure conditions

不要なFieldが最終学習入力に残る、または残す項目とモデル目的の関係を説明できない場合はFail。
観測できない範囲や欠落証拠は未立証として残し、設定や説明文だけで合格を宣言しない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認時期 | 完全性と機微性 | 合格の目安 |
|---|---|---|---|---|---|
| 対象一覧と設計・設定 | Data管理者と学習基盤担当者 | Dataset版、経路、SP-1〜SP-3の判定点 | 採用時と経路変更時 | 権限付き管理。実Dataは公開しない | 各性質がどの実入力に適用されるか追える |
| 正例・負例の実測記録 | 検証担当者 | 上記Positive試験とN-1〜N-3 | 初回とDataset・処理・検証方式の変更時 | 合成Dataを使い、設定版と結果を結び付ける | 期待結果を実測し、失敗・未観測範囲も記録する |
| 運用時の判定記録 | 対象Pipelineと運用担当者 | 実際に使用するDataset版 | 各処理または定義した評価周期 | 不正改変から保護し、内容・秘密を最小化 | 判定と対象版が一致し、古い成功結果を流用しない |

## Related requirements

[C1.1.2](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.1.2-complete-training-source-inventory/README.md)は出所台帳、[C1.3.4](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.3.4-remove-disallowed-content-before-training/README.md)は禁止Contentの排除。必要な項目であることと、内容が安全であることを混同しない。
[C1 Family概要](../README.md)から隣接Requirementへ進める。Engineering Mappingは別途評価する。

## Known limitations and uncertainty

項目削減は必要なデータ内の機密性や、学習後の漏えい防止を保証しない。必要性の判断には用途の知識が必要であり、Scannerの陰性だけではPassにしない。
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
