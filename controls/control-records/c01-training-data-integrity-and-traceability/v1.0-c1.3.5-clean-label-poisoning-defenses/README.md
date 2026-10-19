---
title: 正しいラベルに紛れる毒入れへの防御を検証する
versioned_id: v1.0-C1.3.5
requirement_id: C1.3.5
verification_level: 3
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

# 正しいラベルに紛れる毒入れへの防御を検証する

AISVS Verification Level: 3

[C1.3 Section講義](../../../learning/c01-training-data-integrity-and-traceability/v1.0-c1.3-training-data-quality-and-security-assurance.md)

## Upstream basis

AISVS `v1.0-C1.3.5`は、Clean-label毒入れ攻撃への防御を実装する。
ResearchはLabelの正誤検査と異なる防御を求め、Data浄化や集約方式等を例示する。特定手法の必須採用や、画像分野での実績をTextへそのまま一般化することはしない。
採用基準は固定Revisionのv1.0であり、1.01への移行ではない。
以下の検証・証拠の具体化はRepositoryの解釈である。

## Interpretation

攻撃者が変更できる例・量・特徴と対象Model・Modalityを定め、正しいLabelのまま成立する攻撃を評価対象にする。
Labelの誤り検査だけに依存せず、その攻撃経路へ働く防御を実際のData・学習処理へ適用する。
無害なClean-label模擬攻撃で防御効果と通常精度への影響を測り、事前に定めた対象Scopeと受容基準に照らして判定する。
特定製品の導入や設定の存在だけで実効性を判断しない。

## Security objective

Clean-label毒入れ攻撃への防御を実装する。
正しくLabel付けされた自然な例に攻撃者が特徴を混ぜ、後でその特徴を持つ不正入力を安全と誤判定させる。通常のLabel品質検査は通過してしまう。

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
| SP-1 | 攻撃者が変更できる例・量・特徴と対象Model・Modalityを定め、正しいLabelのまま成立する攻撃を評価対象にする。 |
| SP-2 | Labelの誤り検査だけに依存せず、その攻撃経路へ働く防御を実際のData・学習処理へ適用する。 |
| SP-3 | 無害なClean-label模擬攻撃で防御効果と通常精度への影響を測り、事前に定めた対象Scopeと受容基準に照らして判定する。 |

## Scope calibration and adjacent assurance

C1.3.2は自動Labelの確信度と整合性、C1.3.1は一般的な毒入れ検出。本ControlにはLabelが正しいままの攻撃への独立した防御の証拠が必要。
本ControlがPassでも、他のC1要件やモデル全体の安全性を満たしたことにはならない。

## Threat and failure-mode rationale

正しくLabel付けされた自然な例に攻撃者が特徴を混ぜ、後でその特徴を持つ不正入力を安全と誤判定させる。通常のLabel品質検査は通過してしまう。
外部脅威IDとの厳密なMappingは未評価。用語の一致だけによるMappingは追加しない。

## Verification

### Architecture and configuration review

対象Datasetの収集から実際の学習入力までの経路を辿り、SP-1〜SP-3の判定点と証拠の作成元を確認する。
委託、手動Export、再実行、Cache、派生物の経路が通常Jobと異ならないか点検する。

### Positive verification

隔離した合成Dataと試験Modelで、Labelの正しさを維持した模擬攻撃を用意する。防御なしで攻撃が成立することを対照にし、防御ありの攻撃成功率と通常精度を同じ条件で比較する。
対象版、処理設定、観測点、期待値、実測結果を保存し、SP-1〜SP-3をそれぞれ評価する。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | 誤Labelを混ぜる試験だけを提出する | Clean-label攻撃の検証にならないと判定する。 |
| N-2 | Labelが正しいことだけを確認して承認する | 防御が対象攻撃へ働く証拠を要求し、品質検査だけでPassにしない。 |
| N-3 | 別Modalityや別Modelの防御結果を流用する | 対象Scopeの不一致を検出し、利用環境で再評価する。 |

### Failure conditions

防御がない、Label正誤検査しかない、対象Clean-label攻撃への効果を示せない場合はFailまたは証拠不足。
観測できない範囲や欠落証拠は未立証として残し、設定や説明文だけで合格を宣言しない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認時期 | 完全性と機微性 | 合格の目安 |
|---|---|---|---|---|---|
| 対象一覧と設計・設定 | Data管理者と学習基盤担当者 | Dataset版、経路、SP-1〜SP-3の判定点 | 採用時と経路変更時 | 権限付き管理。実Dataは公開しない | 各性質がどの実入力に適用されるか追える |
| 正例・負例の実測記録 | 検証担当者 | 上記Positive試験とN-1〜N-3 | 初回とDataset・処理・検証方式の変更時 | 合成Dataを使い、設定版と結果を結び付ける | 期待結果を実測し、失敗・未観測範囲も記録する |
| 運用時の判定記録 | 対象Pipelineと運用担当者 | 実際に使用するDataset版 | 各処理または定義した評価周期 | 不正改変から保護し、内容・秘密を最小化 | 判定と対象版が一致し、古い成功結果を流用しない |

## Related requirements

[C1.3.2](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.3.2-automatic-label-confidence-and-consistency-checks/README.md)は自動Labelの確信度と整合性、[C1.3.1](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.3.1-training-pipeline-poisoning-and-corruption-detection/README.md)は一般的な毒入れ検出。本ControlにはLabelが正しいままの攻撃への独立した防御の証拠が必要。
[C1 Family概要](../README.md)から隣接Requirementへ進める。Engineering Mappingは別途評価する。

## Known limitations and uncertainty

全攻撃への保証は困難で、検出器に適応した攻撃も残る。実験的な防御と数学的な保証を区別し、予算・前提・精度低下・計算費用を明記する。
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
