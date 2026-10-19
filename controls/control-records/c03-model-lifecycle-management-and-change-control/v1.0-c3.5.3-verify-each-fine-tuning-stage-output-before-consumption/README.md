---
title: 各追加学習段階の出力を次段階の使用前に検証する
versioned_id: v1.0-C3.5.3
requirement_id: C3.5.3
verification_level: 3
family_id: C3
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-05-Pipeline-Fine-Tuning.md
last_verified: '2026-10-18'
maturity: verifiable
mapping_assessment_refs: []
---

# 各追加学習段階の出力を次段階の使用前に検証する

AISVS Verification Level: 3

[C3.5 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.5-pipeline-fine-tuning.md)

## Upstream basis

AISVS `v1.0-C3.5.3`は、複数段階Fine-tuningでは、各段階の出力を次の段階が消費する前に完全性検証する。
Researchは各境界の登録と照合、途中Checkpointを改変した負例を重視する。振る舞い検査も推奨するが、暗号学的完全性と安全性評価を混ぜ、すべてのBackdoor検出まで本要件のPass条件へ追加しない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

最初の入力や最後のReleaseだけでなく、全段階の受渡しを列挙し、次の段階が実際に読む出力へ検証を適用する。登録時の照合だけでは、後から変わる保存先の読込みを保証しない。信頼できる基準と対象版を結び付け、不一致時は次段階で消費させない。

## Security objective

中間保存物の差替えや破損が、検証なしで後続段階へ連鎖することを防ぐ。

## Applicability

SFTから次の追加学習等、複数段階で成果物を受け渡すFine-tuning Pipelineの全境界。TeamやCompute環境が同じでも、段階間の保存・読込みは対象とする。

### Non-applicability

一段階のみのFine-tuningで段階間の受渡しが存在しない場合は対象外とできる。段階を一つのJobにまとめても実質的な受渡しがあればScopeを確認する。

## Scope and assumptions

対象の学習方式、Run、Model・成果物の版、処理段階と保存・読込み経路を先に定義する。
試験は隔離環境の合成Data・無害な模擬ArtifactやTraceを使う。検証・検知の方式と設定を版で残し、
対象と証拠の不一致や欠落を正常扱いしない。自動処理の判定とModel自身の説明を区別する。

## Assets, actors, identities, and trust boundaries

各段階の出力、保存領域、次段階の消費入口の間の境界。資産は中間成果物、版、照合基準とRunの対応。段階の実行者、保存管理者、Loaderが関わる。攻撃者が中間Objectや可変参照を置換する経路を想定する。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 全段階の入力・出力・参照先を列挙し、各受渡しで信頼する基準と版を特定する。 |
| SP-2 | 次段階の消費前に実際の出力内容を検証し、再実行・再取得・Cache経路も対象を保つ。 |
| SP-3 | 不一致・基準欠落・検証不能を拒否し、検証したものと異なる内容を後続学習へ渡さない。 |

## Scope calibration and adjacent assurance

C3.5.4はCheckpointの個別登録。登録済みでも使用前検証がなければ本ControlはFail。C3.5.1はRLHFで使うModelの開始前の版・完全性。

## Threat and failure-mode rationale

最初に正しい入力を使っても、第一段階後の保存物を置換すれば次段階が別Modelを学習する。最終成果物の検証だけでは途中の破損位置を追いにくい。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

Pipeline DAGと各Loaderを追い、検証の呼出し・基準保護・戻り値と実消費の順序を確認する。最初だけの検証や同一Team内の暗黙の信頼がないか点検する。

### Positive verification

三段階の模擬Pipelineで各段階の出力を信頼する基準へ結び付ける。次段階で使用する前に検証し、各境界の対象・判定・Runが追えることを確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 第一境界と後半境界でそれぞれ中間Fileを改変する | いずれも次段階の消費前に拒否される。SP-1、SP-2、SP-3。 |
| N-2 | 同じ名称の別版をCacheや再実行経路から渡す | 検証対象との違いを検出し、古い成功結果を流用しない。SP-2、SP-3。 |
| N-3 | 成果物とその基準値を同時に無断変更する | 信頼する元基準との不一致または基準保護の欠落を検出する。SP-1。 |

### Failure conditions

一つでも段階間検証がない、消費後の検証のみ、不一致物を次段階が使用する、信頼基準を保護できず内容差替えが通る場合はFail。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 段階間対応と使用前検証記録 | Pipelineと保存基盤担当者 | 全境界の出力・版・基準・次Run | 受渡しごと | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 検証対象が実消費と一致する |
| 各境界の改変・差替え拒否試験 | 検証担当者 | 通常・再実行・Cache経路 | 初回とDAG・Loader変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 後続消費前に拒否を実測する |

## Related requirements

[C3.5.4](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.5.4-fine-tuning-checkpoints-registered-as-distinct-artifacts/README.md)はCheckpointの個別登録。登録済みでも使用前検証がなければ本ControlはFail。[C3.5.1](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.5.1-versioned-integrity-verified-models-before-rlhf/README.md)はRLHFで使うModelの開始前の版・完全性。
[C3 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

完全性検証は正規に生成された危険な振る舞いや、段階間で協調した毒入れの不在を保証しない。内容の品質・安全性はC1・C3.2・C11等の別保証で評価する。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C3 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [AISVS v1.0 C3.5 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-05-Pipeline-Fine-Tuning.md)
- [C3.5 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.5-pipeline-fine-tuning.md)
- [C3 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
