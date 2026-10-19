---
title: 追加学習の各チェックポイントを別成果物として登録する
versioned_id: v1.0-C3.5.4
requirement_id: C3.5.4
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

# 追加学習の各チェックポイントを別成果物として登録する

AISVS Verification Level: 3

[C3.5 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.5-pipeline-fine-tuning.md)

## Upstream basis

AISVS `v1.0-C3.5.4`は、Fine-tuning Checkpointをそれぞれ別のArtifactとして登録する。
ResearchはRun・Step・親Checkpointとの関係を含む個別識別を例示し、Registry Identityだけでは内容の完全性を保証しないと注意する。特定製品のModel ID方式や全Checkpointの永久保存は原文の直接の要求ではない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

Fine-tuningで保存する各Checkpointを別々に識別し、その登録から対象の成果物へ辿れるようにする。一つのLatest名を繰り返し上書きして過去の成果物を区別できない状態では満たせない。Aliasを使っても、その背後で各成果物の登録と識別が維持されればよい。RunやStep等のMetadataは識別と追跡を実効的にする方法である。

## Security objective

途中成果物を区別できず、比較・調査・再開対象を取り違えることを減らす。

## Applicability

Fine-tuningが保存するCheckpointとその登録先を対象とする。Full Model、Adapter等のCheckpoint形式によらず、保存する成果物を一つずつ追う。

### Non-applicability

Fine-tuningを行わずCheckpointを保存しない構成は対象外とできる。保存した中間成果物を一時Fileと呼ぶだけで登録対象から除かない。

## Scope and assumptions

対象の学習方式、Run、Model・成果物の版、処理段階と保存・読込み経路を先に定義する。
試験は隔離環境の合成Data・無害な模擬ArtifactやTraceを使う。検証・検知の方式と設定を版で残し、
対象と証拠の不一致や欠落を正常扱いしない。自動処理の判定とModel自身の説明を区別する。

## Assets, actors, identities, and trust boundaries

学習処理が出力するCheckpointからRegistryの個別記録へ進む境界。資産はCheckpointの識別と対応、作成Run・Stepの追跡性。Trainer、登録Job、Registry管理者、再開担当者が関わる。名前の上書き、未登録の中間成果物、再開時の取り違えを想定する。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 保存された各Checkpointに、他の成果物と区別できる登録記録がある。 |
| SP-2 | 登録と実Checkpointの対応を維持し、同じ可変名の上書きだけで個別の識別を失わない。 |
| SP-3 | 複数Checkpointを一覧・参照して意図した対象を特定でき、Runの実出力との照合で登録漏れを検出できる。 |

## Scope calibration and adjacent assurance

C3.5.3は後続消費前の完全性検証。本要件がPassでも、その検証がない場合はC3.5.3のFailが残る。C3.3.2は本番Rollbackの完全復元であり、Checkpoint登録だけでは満たせない。

## Threat and failure-mode rationale

上書きされたLatestだけでは、どの途中Modelが問題を導入し、どの成果物で学習を再開したかを確認できない。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

Trainerの保存条件と登録Job、Registry一覧、Alias更新、成果物参照を追う。最終版だけを登録して中間Checkpointを対象外にしていないか確認する。保持・削除方針は個別識別の成立時点と分けて記録する。

### Positive verification

短い模擬Fine-tuningで複数Checkpointを保存する。実出力をRegistry一覧と突き合わせ、各々が別記録で識別でき、意図した途中Checkpointを参照できることを確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | Checkpointをすべて同じLatest名で上書きする | 個別識別の喪失を検出し、複数登録済みとしない。SP-1、SP-2。 |
| N-2 | 途中一件の登録を失敗させ最終版だけ成功させる | 出力一覧との照合で登録漏れを発見する。SP-3。 |
| N-3 | 二つの異なるCheckpointを同じ登録へ誤結合する | 実体と個別登録の対応不一致を検出する。SP-1、SP-2。 |

### Failure conditions

保存Checkpointの一部が未登録、異なる成果物を区別できない、登録が実体と対応しない場合はFail。個別登録の成功から内容の完全性までPassと推論しない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| Run出力一覧とRegistry Export | TrainerとRegistry担当者 | 保存した全Checkpointと登録ID | 各Runの保存・登録時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 全成果物の個別対応を照合できる |
| 複数Checkpoint参照と登録失敗の検証 | 検証担当者 | 途中・最終CheckpointとAlias | 初回と登録実装変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 上書き・漏れ・誤結合を検出できる |

## Related requirements

[C3.5.3](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.5.3-verify-each-fine-tuning-stage-output-before-consumption/README.md)は後続消費前の完全性検証。本要件がPassでも、その検証がない場合はC3.5.3のFailが残る。[C3.3.2](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.3.2-rollback-restores-complete-model-state/README.md)は本番Rollbackの完全復元であり、Checkpoint登録だけでは満たせない。
[C3 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

個別IDやRegistry参照は改ざん防止でも安全性保証でもない。保存期間・完全な来歴・復元可能性はRiskに応じた運用として定め、登録と混同しない。
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
