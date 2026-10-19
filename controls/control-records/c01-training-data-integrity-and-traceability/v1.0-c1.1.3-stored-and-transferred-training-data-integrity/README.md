---
title: 保存・転送中の学習データの完全性を確かめる
versioned_id: v1.0-C1.1.3
requirement_id: C1.1.3
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

# 保存・転送中の学習データの完全性を確かめる

AISVS Verification Level: 2

[C1.1 Section講義](../../../learning/c01-training-data-integrity-and-traceability/v1.0-c1.1-training-data-origin-and-security.md)

## Upstream basis

AISVS `v1.0-C1.1.3`は、学習データが保存・転送されても、期待する承認済みの内容から不正に変わらず、破損を見逃して利用されないよう完全性を保つ。
Researchは通信の完全性と保存後の照合を扱い、暗号化だけでは完全性の証拠にならず、攻撃者がDataとChecksumを共に置換できる問題を指摘する。
採用基準は固定Revisionのv1.0であり、1.01への移行ではない。
以下の検証・証拠の具体化はRepositoryの解釈である。

## Interpretation

保存物と転送物を信頼できる基準に照合でき、Dataset版と全Shardの範囲を特定する。
通信先の認証と転送の完全性を検証し、保存後・受領後に利用する内容にも保護が及ぶ。
改変や破損、検証不能なDataを成功扱いで学習へ渡さない。基準値もDataと同時に無断置換されないよう保護する。
特定製品の導入や設定の存在だけで実効性を判断しない。

## Security objective

学習データが保存・転送されても、期待する承認済みの内容から不正に変わらず、破損を見逃して利用されないよう完全性を保つ。
保存領域への書込み権限を得た攻撃者がShardと同じ場所のChecksumを置換する。転送時の差替えや破損を見逃すと、受入れ時に承認したものと異なるDataで学習する。

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
| SP-1 | 保存物と転送物を信頼できる基準に照合でき、Dataset版と全Shardの範囲を特定する。 |
| SP-2 | 通信先の認証と転送の完全性を検証し、保存後・受領後に利用する内容にも保護が及ぶ。 |
| SP-3 | 改変や破損、検証不能なDataを成功扱いで学習へ渡さない。基準値もDataと同時に無断置換されないよう保護する。 |

## Scope calibration and adjacent assurance

C1.1.4は変更の監視。学習読込み時の照合だけでは継続監視を証明しない。C1.3は元から存在する毒入れや品質を別に評価する。
本ControlがPassでも、他のC1要件やモデル全体の安全性を満たしたことにはならない。

## Threat and failure-mode rationale

保存領域への書込み権限を得た攻撃者がShardと同じ場所のChecksumを置換する。転送時の差替えや破損を見逃すと、受入れ時に承認したものと異なるDataで学習する。
外部脅威IDとの厳密なMappingは未評価。用語の一致だけによるMappingは追加しない。

## Verification

### Architecture and configuration review

対象Datasetの収集から実際の学習入力までの経路を辿り、SP-1〜SP-3の判定点と証拠の作成元を確認する。
委託、手動Export、再実行、Cache、派生物の経路が通常Jobと異ならないか点検する。

### Positive verification

承認済み合成Datasetを保管・転送し、受信側と学習読込み側で対象版と全Shardが信頼できる基準に一致することを示す。
対象版、処理設定、観測点、期待値、実測結果を保存し、SP-1〜SP-3をそれぞれ評価する。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | 保存Shardの一部を変更する | 照合失敗を観測し、変更Dataを正常入力として学習しない。 |
| N-2 | 転送先を偽装し、証明書検証を無効化する経路を試す | 認証・完全性の欠落を検出し、保護された転送と判定しない。 |
| N-3 | Dataと付属Checksumを同時に置換する | 独立した信頼基準との不一致を検出する。同じ書込み権限下のChecksumだけではPassにしない。 |

### Failure conditions

保存または転送のいずれかに未保護経路がある、基準値を無断で一緒に置換できる、改変物が検証成功として学習される場合はFail。
観測できない範囲や欠落証拠は未立証として残し、設定や説明文だけで合格を宣言しない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認時期 | 完全性と機微性 | 合格の目安 |
|---|---|---|---|---|---|
| 対象一覧と設計・設定 | Data管理者と学習基盤担当者 | Dataset版、経路、SP-1〜SP-3の判定点 | 採用時と経路変更時 | 権限付き管理。実Dataは公開しない | 各性質がどの実入力に適用されるか追える |
| 正例・負例の実測記録 | 検証担当者 | 上記Positive試験とN-1〜N-3 | 初回とDataset・処理・検証方式の変更時 | 合成Dataを使い、設定版と結果を結び付ける | 期待結果を実測し、失敗・未観測範囲も記録する |
| 運用時の判定記録 | 対象Pipelineと運用担当者 | 実際に使用するDataset版 | 各処理または定義した評価周期 | 不正改変から保護し、内容・秘密を最小化 | 判定と対象版が一致し、古い成功結果を流用しない |

## Related requirements

[C1.1.4](../../../../controls/control-records/c01-training-data-integrity-and-traceability/v1.0-c1.1.4-training-data-integrity-monitoring/README.md)は変更の監視。学習読込み時の照合だけでは継続監視を証明しない。C1.3は元から存在する毒入れや品質を別に評価する。
[C1 Family概要](../README.md)から隣接Requirementへ進める。Engineering Mappingは別途評価する。

## Known limitations and uncertainty

正当な署名者自身が承認した汚染や、検証後のメモリ内変更まで自動的に防げない。署名付きManifestは実装例であり、唯一の必須形式ではない。
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
