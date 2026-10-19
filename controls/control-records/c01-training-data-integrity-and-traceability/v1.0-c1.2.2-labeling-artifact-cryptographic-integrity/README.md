---
title: 注釈成果物の暗号学的完全性を検証する
versioned_id: v1.0-C1.2.2
requirement_id: C1.2.2
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

# 注釈成果物の暗号学的完全性を検証する

AISVS Verification Level: 2

[C1.2 Section講義](../../../learning/c01-training-data-integrity-and-traceability/v1.0-c1.2-data-labeling-and-annotation-security.md)

## Upstream basis

AISVS `v1.0-C1.2.2`は、Labeling Artifactへ暗号技術による完全性保護を適用する。
Researchは信頼する署名者、Manifest対象範囲と全ファイルの照合を重視する。特定の署名規格やWORM保存だけを唯一の充足手段とはしない。
採用基準は固定Revisionのv1.0であり、1.01への移行ではない。
以下の検証・証拠の具体化はRepositoryの解釈である。

## Interpretation

利用する注釈本体・関連Metadata・付属Fileの保護対象と版を特定し、暗号学的な照合で内容の変更を検出できる。
信頼できる照合基準または許可した署名者に結び付き、攻撃者がDataと基準値を同時に置換して検証を通せない。
Export・加工・受渡し後に実際に学習するArtifactを検証し、改変・未検証物を正常扱いで消費しない。
特定製品の導入や設定の存在だけで実効性を判断しない。

## Security objective

Labeling Artifactへ暗号技術による完全性保護を適用する。
Export後のCSVや付属理由ファイルが改変され、学習側が異なるLabelを使う。誰の署名でも有効なら受け入れる検証も、信頼境界を守らない。

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
| SP-1 | 利用する注釈本体・関連Metadata・付属Fileの保護対象と版を特定し、暗号学的な照合で内容の変更を検出できる。 |
| SP-2 | 信頼できる照合基準または許可した署名者に結び付き、攻撃者がDataと基準値を同時に置換して検証を通せない。 |
| SP-3 | Export・加工・受渡し後に実際に学習するArtifactを検証し、改変・未検証物を正常扱いで消費しない。 |

## Scope calibration and adjacent assurance

C1.2.1は操作権限、C1.2.3は機微情報の保護。署名済みの誤Labelや平文の機密は、それぞれ別の保証で評価する。C1.1.3は学習Data全体の保存・転送を扱う。
本ControlがPassでも、他のC1要件やモデル全体の安全性を満たしたことにはならない。

## Threat and failure-mode rationale

Export後のCSVや付属理由ファイルが改変され、学習側が異なるLabelを使う。誰の署名でも有効なら受け入れる検証も、信頼境界を守らない。
外部脅威IDとの厳密なMappingは未評価。用語の一致だけによるMappingは追加しない。

## Verification

### Architecture and configuration review

対象Datasetの収集から実際の学習入力までの経路を辿り、SP-1〜SP-3の判定点と証拠の作成元を確認する。
委託、手動Export、再実行、Cache、派生物の経路が通常Jobと異ならないか点検する。

### Positive verification

合成注釈をExportし、信頼する基準との一致と全対象Fileの検証を確認する。正当な変換では入力検証と変換後の保護を結び付ける。
対象版、処理設定、観測点、期待値、実測結果を保存し、SP-1〜SP-3をそれぞれ評価する。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | Label一件または理由のSidecarを変更する | 対象File全体の不一致を検出し、学習への正常投入を拒否する。 |
| N-2 | 別の無許可鍵で同じArtifactへ署名する | 数学的に有効な署名でも信頼条件を満たさず拒否する。 |
| N-3 | 検証した版と異なるObject最新版へ参照を差し替える | 消費する実体の不一致を検出する。旧版の検証を流用しない。 |

### Failure conditions

Artifactの一部が未保護、基準も同時に無断置換可能、改変物や対象外の版が検証済みとして利用される場合はFail。
観測できない範囲や欠落証拠は未立証として残し、設定や説明文だけで合格を宣言しない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認時期 | 完全性と機微性 | 合格の目安 |
|---|---|---|---|---|---|
| 対象一覧と設計・設定 | Data管理者と学習基盤担当者 | Dataset版、経路、SP-1〜SP-3の判定点 | 採用時と経路変更時 | 権限付き管理。実Dataは公開しない | 各性質がどの実入力に適用されるか追える |
| 正例・負例の実測記録 | 検証担当者 | 上記Positive試験とN-1〜N-3 | 初回とDataset・処理・検証方式の変更時 | 合成Dataを使い、設定版と結果を結び付ける | 期待結果を実測し、失敗・未観測範囲も記録する |
| 運用時の判定記録 | 対象Pipelineと運用担当者 | 実際に使用するDataset版 | 各処理または定義した評価周期 | 不正改変から保護し、内容・秘密を最小化 | 判定と対象版が一致し、古い成功結果を流用しない |

## Related requirements

[C1.2.1](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.2.1-annotation-create-modify-approve-authorization/README.md)は操作権限、[C1.2.3](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.2.3-protect-sensitive-label-information-before-artifacts/README.md)は機微情報の保護。署名済みの誤Labelや平文の機密は、それぞれ別の保証で評価する。[C1.1.3](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.1.3-stored-and-transferred-training-data-integrity/README.md)は学習Data全体の保存・転送を扱う。
[C1 Family概要](../README.md)から隣接Requirementへ進める。Engineering Mappingは別途評価する。

## Known limitations and uncertainty

署名前の誤りや、許可された署名者による悪意あるLabelを検出する保証ではない。Checksum単体の存在は、信頼できる基準と照合して初めて意味を持つ。
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
