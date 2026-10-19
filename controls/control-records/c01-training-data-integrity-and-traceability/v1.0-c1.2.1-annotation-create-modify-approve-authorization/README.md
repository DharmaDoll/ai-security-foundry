---
title: 注釈の作成・変更・承認を権限で制限する
versioned_id: v1.0-C1.2.1
requirement_id: C1.2.1
verification_level: 1
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

# 注釈の作成・変更・承認を権限で制限する

AISVS Verification Level: 1

[C1.2 Section講義](../../../learning/c01-training-data-integrity-and-traceability/v1.0-c1.2-data-labeling-and-annotation-security.md)

## Upstream basis

AISVS `v1.0-C1.2.1`は、Labeling Platformで注釈を作成・変更・承認できる主体を権限で制限する。
ResearchはRole分離と権限昇格の試験を推奨する。全案件で作成者と承認者を別人にすることや、特定のEnterprise製品を原文が必須とするわけではない。
採用基準は固定Revisionのv1.0であり、1.01への移行ではない。
以下の検証・証拠の具体化はRepositoryの解釈である。

## Interpretation

主体・Project・対象注釈ごとに、作成・変更・承認の許可条件を定義する。
UIからの操作とAPI・一括Import・自動処理でも、操作を確定する前に定義した権限を強制する。
Roleや担当範囲の変更・失効が判定に反映され、入力中のRole申告や対象IDだけを信頼しない。
特定製品の導入や設定の存在だけで実効性を判断しない。

## Security objective

Labeling Platformで注釈を作成・変更・承認できる主体を権限で制限する。
委託作業者が別Projectの注釈IDを指定して内容を変更し、承認APIも直接呼ぶ。画面上のボタン非表示だけでは制限にならない。

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
| SP-1 | 主体・Project・対象注釈ごとに、作成・変更・承認の許可条件を定義する。 |
| SP-2 | UIからの操作とAPI・一括Import・自動処理でも、操作を確定する前に定義した権限を強制する。 |
| SP-3 | Roleや担当範囲の変更・失効が判定に反映され、入力中のRole申告や対象IDだけを信頼しない。 |

## Scope calibration and adjacent assurance

C1.2.2はExport等の暗号学的完全性であり、権限外の操作を後から署名しても本ControlのFailは消えない。C1.3.2は自動Labelの質を扱う。
本ControlがPassでも、他のC1要件やモデル全体の安全性を満たしたことにはならない。

## Threat and failure-mode rationale

委託作業者が別Projectの注釈IDを指定して内容を変更し、承認APIも直接呼ぶ。画面上のボタン非表示だけでは制限にならない。
外部脅威IDとの厳密なMappingは未評価。用語の一致だけによるMappingは追加しない。

## Verification

### Architecture and configuration review

対象Datasetの収集から実際の学習入力までの経路を辿り、SP-1〜SP-3の判定点と証拠の作成元を確認する。
委託、手動Export、再実行、Cache、派生物の経路が通常Jobと異ならないか点検する。

### Positive verification

許可されたProjectで担当者が作成・変更し、承認権限を持つ主体が承認できることを各操作で確認する。
対象版、処理設定、観測点、期待値、実測結果を保存し、SP-1〜SP-3をそれぞれ評価する。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | 権限のない別ProjectのIDを直接指定する | 作成・変更・承認をそれぞれ拒否し、保存状態が変わらない。 |
| N-2 | 画面を迂回して承認APIや一括Importを呼ぶ | 同じ権限判定が適用され、経路による迂回がない。 |
| N-3 | Roleを失効させて既存Sessionから変更する | 失効Policyに従い拒否する。自己申告の管理者Roleで許可しない。 |

### Failure conditions

権限外の主体がいずれかの操作を実行できればFail。認証済みという事実や操作Logだけでは認可の証明にならない。
観測できない範囲や欠落証拠は未立証として残し、設定や説明文だけで合格を宣言しない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認時期 | 完全性と機微性 | 合格の目安 |
|---|---|---|---|---|---|
| 対象一覧と設計・設定 | Data管理者と学習基盤担当者 | Dataset版、経路、SP-1〜SP-3の判定点 | 採用時と経路変更時 | 権限付き管理。実Dataは公開しない | 各性質がどの実入力に適用されるか追える |
| 正例・負例の実測記録 | 検証担当者 | 上記Positive試験とN-1〜N-3 | 初回とDataset・処理・検証方式の変更時 | 合成Dataを使い、設定版と結果を結び付ける | 期待結果を実測し、失敗・未観測範囲も記録する |
| 運用時の判定記録 | 対象Pipelineと運用担当者 | 実際に使用するDataset版 | 各処理または定義した評価周期 | 不正改変から保護し、内容・秘密を最小化 | 判定と対象版が一致し、古い成功結果を流用しない |

## Related requirements

[C1.2.2](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.2.2-labeling-artifact-cryptographic-integrity/README.md)はExport等の暗号学的完全性であり、権限外の操作を後から署名しても本ControlのFailは消えない。[C1.3.2](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.3.2-automatic-label-confidence-and-consistency-checks/README.md)は自動Labelの質を扱う。
[C1 Family概要](../README.md)から隣接Requirementへ進める。Engineering Mappingは別途評価する。

## Known limitations and uncertainty

許可された作業者による意図的な誤Labelは残る。作業者の本人確認や職務分離はRiskに応じた補強であり、本要件の普遍的な追加条件とはしない。
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
