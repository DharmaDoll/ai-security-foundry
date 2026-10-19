---
title: 機微なラベル情報を成果物に入れる前に保護する
versioned_id: v1.0-C1.2.3
requirement_id: C1.2.3
verification_level: 2
family_id: C1
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C01-Training-Data-Integrity-and-Traceability.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C01-Training-Data/C01-02-Data-Labeling-Annotation-Security.md
last_verified: '2026-10-17'
maturity: verifiable
mapping_assessment_refs: []
---

# 機微なラベル情報を成果物に入れる前に保護する

AISVS Verification Level: 2

[C1.2 Section講義](../../../learning/c01-training-data-integrity-and-traceability/v1.0-c1.2-data-labeling-and-annotation-security.md)

## Upstream basis

AISVS `v1.0-C1.2.3`は、機微情報をLabeling Artifactへ使う前に削除・匿名化・暗号化する。
ResearchはLabel値だけでなく自由記述理由やMetadata、派生Exportへの残存も調べる。検出製品のVersionや一般的な精度値だけを充足証拠にはしない。
採用基準は固定Revisionのv1.0であり、1.01への移行ではない。
以下の検証・証拠の具体化はRepositoryの解釈である。

## Interpretation

Label値・理由・付随情報の機微情報の種類を定義し、成果物作成前の保護点を特定する。
対象の機微情報を削除・匿名化・暗号化し、Export・中間File・派生成果物に未処理の値を残さない。
暗号化や再識別可能な方式では鍵・対応表を成果物から分離して保護し、未処理情報を利用者がそのまま読める状態にしない。
特定製品の導入や設定の存在だけで実効性を判断しない。

## Security objective

機微情報をLabeling Artifactへ使う前に削除・匿名化・暗号化する。
作業者が判断理由へ顧客の氏名や病歴を記入し、署名付きCSVやLogへ平文のまま残る。保存先のアクセス制御だけでは内容の保護を代替しない。

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
| SP-1 | Label値・理由・付随情報の機微情報の種類を定義し、成果物作成前の保護点を特定する。 |
| SP-2 | 対象の機微情報を削除・匿名化・暗号化し、Export・中間File・派生成果物に未処理の値を残さない。 |
| SP-3 | 暗号化や再識別可能な方式では鍵・対応表を成果物から分離して保護し、未処理情報を利用者がそのまま読める状態にしない。 |

## Scope calibration and adjacent assurance

C1.2.1の認可とC1.2.2の完全性は機微情報の内容保護を代替しない。C1.1.1の項目最小化とC1.3.4の禁止内容排除も別に確かめる。
本ControlがPassでも、他のC1要件やモデル全体の安全性を満たしたことにはならない。

## Threat and failure-mode rationale

作業者が判断理由へ顧客の氏名や病歴を記入し、署名付きCSVやLogへ平文のまま残る。保存先のアクセス制御だけでは内容の保護を代替しない。
外部脅威IDとの厳密なMappingは未評価。用語の一致だけによるMappingは追加しない。

## Verification

### Architecture and configuration review

対象Datasetの収集から実際の学習入力までの経路を辿り、SP-1〜SP-3の判定点と証拠の作成元を確認する。
委託、手動Export、再実行、Cache、派生物の経路が通常Jobと異ならないか点検する。

### Positive verification

合成氏名・識別子・病歴をLabel値と理由へ入れ、Artifact生成前に定義した保護が働くことを確認する。許可した非機微Labelは利用でき、全派生Exportでも元の値が残らないことを調べる。
対象版、処理設定、観測点、期待値、実測結果を保存し、SP-1〜SP-3をそれぞれ評価する。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | 理由やMetadataに機微情報を埋める | Label列だけの処理を迂回せず、対象情報を成果物前に保護する。 |
| N-2 | 保護処理前の一時CSVをExportやCacheとして残す | 未保護の成果物を検出し、最終Fileだけの成功を全体のPassとしない。 |
| N-3 | 暗号鍵や対応表を同じExportに添付する | 情報を容易に復元できるため保護不足と判定する。 |

### Failure conditions

対象機微情報が成果物へ平文のまま残る、保護が成果物使用後にしか行われない、鍵等の同梱で保護が無意味になる場合はFail。
観測できない範囲や欠落証拠は未立証として残し、設定や説明文だけで合格を宣言しない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認時期 | 完全性と機微性 | 合格の目安 |
|---|---|---|---|---|---|
| 対象一覧と設計・設定 | Data管理者と学習基盤担当者 | Dataset版、経路、SP-1〜SP-3の判定点 | 採用時と経路変更時 | 権限付き管理。実Dataは公開しない | 各性質がどの実入力に適用されるか追える |
| 正例・負例の実測記録 | 検証担当者 | 上記Positive試験とN-1〜N-3 | 初回とDataset・処理・検証方式の変更時 | 合成Dataを使い、設定版と結果を結び付ける | 期待結果を実測し、失敗・未観測範囲も記録する |
| 運用時の判定記録 | 対象Pipelineと運用担当者 | 実際に使用するDataset版 | 各処理または定義した評価周期 | 不正改変から保護し、内容・秘密を最小化 | 判定と対象版が一致し、古い成功結果を流用しない |

## Related requirements

[C1.2.1](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.2.1-annotation-create-modify-approve-authorization/README.md)の認可とC1.2.2の完全性は機微情報の内容保護を代替しない。[C1.1.1](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.1.1-purpose-bound-training-fields/README.md)の項目最小化とC1.3.4の禁止内容排除も別に確かめる。
[C1 Family概要](../README.md)から隣接Requirementへ進める。Engineering Mappingは別途評価する。

## Known limitations and uncertainty

匿名化の再識別Risk、言語・分野依存の検出漏れ、暗号化した値を学習側で復号する境界は残る。単なる仮名置換を不可逆な匿名化とみなさず、保護の実効性を評価する。
本書の`verifiable`はControl文書の成熟度であり、実製品での試験完了や適合認定ではない。

## References

- [AISVS v1.0 C1 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C01-Training-Data-Integrity-and-Traceability.md)
- [AISVS v1.0 C1.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C01-Training-Data/C01-02-Data-Labeling-Annotation-Security.md)
- [C1.2 Section講義](../../../learning/c01-training-data-integrity-and-traceability/v1.0-c1.2-data-labeling-and-annotation-security.md)
- [C1 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-17 | 初版。要件固有の性質、合否、正負試験と証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品での試験は未実施 |
