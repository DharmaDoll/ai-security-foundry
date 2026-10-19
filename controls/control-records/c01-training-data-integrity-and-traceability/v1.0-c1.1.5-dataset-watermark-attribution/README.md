---
title: データセットのウォーターマークで利用を識別する
versioned_id: v1.0-C1.1.5
requirement_id: C1.1.5
verification_level: 3
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

# データセットのウォーターマークで利用を識別する

AISVS Verification Level: 3

[C1.1 Section講義](../../../learning/c01-training-data-integrity-and-traceability/v1.0-c1.1-training-data-origin-and-security.md)

## Upstream basis

AISVS `v1.0-C1.1.5`は、Datasetへ識別用の印を付け、利用の帰属と無断利用の検出を可能にする。
ResearchはWatermarkの識別精度、変換への耐性、誤判定と観測条件の制約を強調する。単なるFile Hashや、モデル出力の印だけではDatasetへのWatermarkを示せない。
採用基準は固定Revisionのv1.0であり、1.01への移行ではない。
以下の検証・証拠の具体化はRepositoryの解釈である。

## Interpretation

対象Dataset版に帰属を識別するWatermarkを適用し、検出手順と観測できる対象を定義する。
印付きDataの利用を検出する正例と、無関係なDataの誤検出を測る対照例を備える。
想定される加工・一部抽出・学習等の利用経路で検出可能な条件と限界を記録し、根拠以上の無断利用検出を主張しない。
特定製品の導入や設定の存在だけで実効性を判断しない。

## Security objective

Datasetへ識別用の印を付け、利用の帰属と無断利用の検出を可能にする。
学習用Datasetが無断複製・再利用されても、提供者が元Dataset由来の利用だと識別できず、調査の根拠を得られない。

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
| SP-1 | 対象Dataset版に帰属を識別するWatermarkを適用し、検出手順と観測できる対象を定義する。 |
| SP-2 | 印付きDataの利用を検出する正例と、無関係なDataの誤検出を測る対照例を備える。 |
| SP-3 | 想定される加工・一部抽出・学習等の利用経路で検出可能な条件と限界を記録し、根拠以上の無断利用検出を主張しない。 |

## Scope calibration and adjacent assurance

C1.1.3の完全性照合やC7.4.4の生成Mediaへの印とは対象が異なる。Watermarkの検出は無断利用の法的断定でもアクセス防止でもない。
本ControlがPassでも、他のC1要件やモデル全体の安全性を満たしたことにはならない。

## Threat and failure-mode rationale

学習用Datasetが無断複製・再利用されても、提供者が元Dataset由来の利用だと識別できず、調査の根拠を得られない。
外部脅威IDとの厳密なMappingは未評価。用語の一致だけによるMappingは追加しない。

## Verification

### Architecture and configuration review

対象Datasetの収集から実際の学習入力までの経路を辿り、SP-1〜SP-3の判定点と証拠の作成元を確認する。
委託、手動Export、再実行、Cache、派生物の経路が通常Jobと異ならないか点検する。

### Positive verification

識別用の印を付けた合成Datasetを、想定する再利用経路へ通して帰属を検出する。印なしの無関係な対照Datasetを同じ検出器で試し、誤検知としきい値を記録する。
対象版、処理設定、観測点、期待値、実測結果を保存し、SP-1〜SP-3をそれぞれ評価する。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | File HashだけをWatermarkの証拠として提出する | 改変照合と利用帰属の違いから、不足と判定する。 |
| N-2 | 印なしDatasetや別所有者のDataへ検出器を適用する | 誤検出を計測し、任意の検出を帰属の証拠にしない。 |
| N-3 | 想定する部分抽出や変換で印を弱める | 検出不能条件を記録する。想定用途で識別できなければPassにしない。 |

### Failure conditions

対象DatasetにWatermarkがない、検出手順がない、または主張する利用経路で帰属を識別できない場合はFail。外部利用を観測できない場合は検出可能性が未立証とする。
観測できない範囲や欠落証拠は未立証として残し、設定や説明文だけで合格を宣言しない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認時期 | 完全性と機微性 | 合格の目安 |
|---|---|---|---|---|---|
| 対象一覧と設計・設定 | Data管理者と学習基盤担当者 | Dataset版、経路、SP-1〜SP-3の判定点 | 採用時と経路変更時 | 権限付き管理。実Dataは公開しない | 各性質がどの実入力に適用されるか追える |
| 正例・負例の実測記録 | 検証担当者 | 上記Positive試験とN-1〜N-3 | 初回とDataset・処理・検証方式の変更時 | 合成Dataを使い、設定版と結果を結び付ける | 期待結果を実測し、失敗・未観測範囲も記録する |
| 運用時の判定記録 | 対象Pipelineと運用担当者 | 実際に使用するDataset版 | 各処理または定義した評価周期 | 不正改変から保護し、内容・秘密を最小化 | 判定と対象版が一致し、古い成功結果を流用しない |

## Related requirements

[C1.1.3](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.1.3-stored-and-transferred-training-data-integrity/README.md)の完全性照合やC7.4.4の生成Mediaへの印とは対象が異なる。Watermarkの検出は無断利用の法的断定でもアクセス防止でもない。
[C1 Family概要](../README.md)から隣接Requirementへ進める。Engineering Mappingは別途評価する。

## Known limitations and uncertainty

あらゆる無断利用の検出は保証できない。攻撃者による除去、Data量、Model構造、観測可能性、偽陽性に依存する。印の追加が学習品質へ与える影響も別に評価する。
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
