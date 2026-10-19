---
title: 学習データへの無断変更と破損を監視する
versioned_id: v1.0-C1.1.4
requirement_id: C1.1.4
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

# 学習データへの無断変更と破損を監視する

AISVS Verification Level: 2

[C1.1 Section講義](../../../learning/c01-training-data-integrity-and-traceability/v1.0-c1.1-training-data-origin-and-security.md)

## Upstream basis

AISVS `v1.0-C1.1.4`は、学習データの完全性を監視し、受入れ後の無断変更や破損を発見できるようにする。
Researchは変更Eventと定期照合の組合せ、監視経路自体の保護を例示する。原文は具体的な監視間隔や製品を指定しない。
採用基準は固定Revisionのv1.0であり、1.01への移行ではない。
以下の検証・証拠の具体化はRepositoryの解釈である。

## Interpretation

対象Dataset版・保存先・派生物の監視範囲、検知までの時間目標、担当者を明示する。
無断変更と破損を信頼できる基準や変更Eventで検知でき、許可した更新との区別を説明できる。
監視停止・Event欠落・基準値改変を見逃す状態を点検し、検出結果を担当者へ届けられる。
特定製品の導入や設定の存在だけで実効性を判断しない。

## Security objective

学習データの完全性を監視し、受入れ後の無断変更や破損を発見できるようにする。
侵害されたCredentialが学習の間隔中にDatasetを少しずつ改変する。取込み時だけの検査では保存中の変更も監視停止も気付かない。

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
| SP-1 | 対象Dataset版・保存先・派生物の監視範囲、検知までの時間目標、担当者を明示する。 |
| SP-2 | 無断変更と破損を信頼できる基準や変更Eventで検知でき、許可した更新との区別を説明できる。 |
| SP-3 | 監視停止・Event欠落・基準値改変を見逃す状態を点検し、検出結果を担当者へ届けられる。 |

## Scope calibration and adjacent assurance

C1.1.3の保存・転送時の保護とは別の検知保証。C12.5.1の来歴Logの存在も内容の完全性監視を代替しない。
本ControlがPassでも、他のC1要件やモデル全体の安全性を満たしたことにはならない。

## Threat and failure-mode rationale

侵害されたCredentialが学習の間隔中にDatasetを少しずつ改変する。取込み時だけの検査では保存中の変更も監視停止も気付かない。
外部脅威IDとの厳密なMappingは未評価。用語の一致だけによるMappingは追加しない。

## Verification

### Architecture and configuration review

対象Datasetの収集から実際の学習入力までの経路を辿り、SP-1〜SP-3の判定点と証拠の作成元を確認する。
委託、手動Export、再実行、Cache、派生物の経路が通常Jobと異ならないか点検する。

### Positive verification

合成Datasetを承認手順で更新し、正当な更新と確認できることを示す。別に無断変更と破損を発生させ、定めた時間内に対象版付きの検出結果が届くことを確認する。
対象版、処理設定、観測点、期待値、実測結果を保存し、SP-1〜SP-3をそれぞれ評価する。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | 次回学習を待たず保存Dataを書き換える | 学習開始とは独立した監視で検知し、時刻と対象を記録する。 |
| N-2 | 監視Workerを止め、変更Eventを落とす | 監視の欠損を検出する。無Alertを変更なしの証拠にしない。 |
| N-3 | 監視対象外の複製・派生物を学習に使う | 範囲漏れを発見し、監視済みとの主張を取り消す。 |

### Failure conditions

取込み時または学習直前の単発照合しかない、監視範囲内の無断変更・破損を検知しない、監視が停止しても正常と判定する場合はFail。
観測できない範囲や欠落証拠は未立証として残し、設定や説明文だけで合格を宣言しない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認時期 | 完全性と機微性 | 合格の目安 |
|---|---|---|---|---|---|
| 対象一覧と設計・設定 | Data管理者と学習基盤担当者 | Dataset版、経路、SP-1〜SP-3の判定点 | 採用時と経路変更時 | 権限付き管理。実Dataは公開しない | 各性質がどの実入力に適用されるか追える |
| 正例・負例の実測記録 | 検証担当者 | 上記Positive試験とN-1〜N-3 | 初回とDataset・処理・検証方式の変更時 | 合成Dataを使い、設定版と結果を結び付ける | 期待結果を実測し、失敗・未観測範囲も記録する |
| 運用時の判定記録 | 対象Pipelineと運用担当者 | 実際に使用するDataset版 | 各処理または定義した評価周期 | 不正改変から保護し、内容・秘密を最小化 | 判定と対象版が一致し、古い成功結果を流用しない |

## Related requirements

[C1.1.3](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.1.3-stored-and-transferred-training-data-integrity/README.md)の保存・転送時の保護とは別の検知保証。[C12.5.1](../../../../controls/control-records/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.5.1-record-complete-dataset-lineage/README.md)の来歴Logの存在も内容の完全性監視を代替しない。
[C1 Family概要](../README.md)から隣接Requirementへ進める。Engineering Mappingは別途評価する。

## Known limitations and uncertainty

監視間隔には検知遅延がある。検知自体は学習停止や復旧ではなく、対応手順と利用時の完全性保護は別に必要。時間目標は製品Riskに応じたRepository解釈である。
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
