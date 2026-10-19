---
title: RLHFで使うモデルの版と完全性を使用前に確認する
versioned_id: v1.0-C3.5.1
requirement_id: C3.5.1
verification_level: 2
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

# RLHFで使うモデルの版と完全性を使用前に確認する

AISVS Verification Level: 2

[C3.5 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.5-pipeline-fine-tuning.md)

## Upstream basis

AISVS `v1.0-C3.5.1`は、RLHF Fine-tuningで使うModelは版管理し、学習Runで使う前に完全性を検証する。
Researchは報酬Modelも検証対象に含め、信頼する照合基準と実際の読込み対象を対応させることを重視する。RLVRのVerifier等も議論するが、本要件のRLHFという適用Scopeを自動的に広げない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

RLHFに使うPolicy Modelや報酬Model、その他の入力Modelを版で識別し、実際に読む内容が信頼できる期待値と一致するか使用前に検証する。署名や保護されたDigestは実装例であり、特定の署名製品や透明性Logの採用を原文の必須条件とはしない。Modelの内容を確認しても報酬の採点品質は別途評価する。

## Security objective

学習方向を決める入力Modelを差し替えられたまま使用せず、どの版でRunを行ったかを説明できるようにする。

## Applicability

RLHF Fine-tuningのRunに使用する各Modelと、その版情報・信頼基準・読込み入口を対象とする。報酬Modelを固定基盤と呼んで対象から外さない。

### Non-applicability

RLHFを行わない構成は対象外とできる。RAGや外部LLMの通常推論をRLHFと呼ばない。委託RLHFでは実装担当が外部であることだけで確認を省かない。

## Scope and assumptions

対象の学習方式、Run、Model・成果物の版、処理段階と保存・読込み経路を先に定義する。
試験は隔離環境の合成Data・無害な模擬ArtifactやTraceを使う。検証・検知の方式と設定を版で残し、
対象と証拠の不一致や欠落を正常扱いしない。自動処理の判定とModel自身の説明を区別する。

## Assets, actors, identities, and trust boundaries

Registry・保存領域からRLHF Runが入力Modelを読む境界。資産はPolicy／報酬等のModel一式と版・照合基準。提供者、学習Job、Registry・署名管理者が関わる。攻撃者は保存物と付属Hashを置換したり、可変Aliasで別版を読ませたりする。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | Runで使う各Modelの版を特定し、報酬Modelを含めRun記録へ結び付ける。 |
| SP-2 | 実際の使用前にModel内容の完全性を信頼できる基準へ照合し、Dataと基準の同時無断置換を許さない。 |
| SP-3 | 未検証・不一致・検証不能のModelで正常なRunを開始せず、実際に読む版と検証対象を一致させる。 |

## Scope calibration and adjacent assurance

C3.5.2は報酬ハッキング等の自動検知。採点品質が悪いという事実だけで本Controlの版・完全性がFailになるわけではない。C3.5.3は途中成果物の段階間検証。

## Threat and failure-mode rationale

報酬Modelを不正に差し替えると、正規の学習処理が攻撃者の望む方向を高評価してしまう。入力Policyだけの検証ではこの経路を守れない。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

RLHFで読み込む全Model、Registry Alias、照合基準、検証呼出し、例外処理とRun Metadataを追う。報酬Modelだけが除外される経路や検証後の再取得がないか点検する。

### Positive verification

無害なPolicy・報酬Model一式の版と保護した照合値を登録し、Run開始前に両方を検証する。Run記録から実際に読んだ各版と検証結果を辿れることを示す。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 報酬Modelを改変してRunへ渡す | 使用前に不一致を検出し、学習を開始しない。SP-2、SP-3。 |
| N-2 | Dataと同じ書込み権限下のHashも同時に差し替える | 独立した信頼基準がなければ保証不足と検出する。SP-2。 |
| N-3 | Run開始直前にAliasを別版へ解決させる | 検証済み版と使用版の不一致を拒否する。SP-1、SP-3。 |

### Failure conditions

使用Modelの版が不明、完全性検証が使用後のみ、報酬Modelが検証対象外、改変物や検証不能物が正常に使用される場合はFail。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| Run別の入力Model版と検証結果 | 学習JobとRegistry担当者 | Policy・報酬等の実入力 | 各Runの使用前 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 全入力の実体と版・成功結果が一致する |
| 改変・差替え・検証不能の拒否試験 | 検証担当者 | 読込みとRun開始境界 | 初回とLoader・基準変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 不一致Modelで学習が始まらない |

## Related requirements

[C3.5.2](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.5.2-automated-reward-hacking-and-overoptimization-detection/README.md)は報酬ハッキング等の自動検知。採点品質が悪いという事実だけで本Controlの版・完全性がFailになるわけではない。[C3.5.3](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.5.3-verify-each-fine-tuning-stage-output-before-consumption/README.md)は途中成果物の段階間検証。
[C3 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

正規に版管理された報酬Modelにも誤りや偏りがある。完全性は評価品質やModelの安全性ではなく、予定した内容を使うことの保証である。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C3 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [AISVS v1.0 C3.5 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-05-Pipeline-Fine-Tuning.md)
- [C3.5 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.5-pipeline-fine-tuning.md)
- [C3 Family概要](../README.md)

- [関連Insight：Security Artifactは証明できる範囲を越えて信頼しない](../../../../docs/insights/security-artifacts-have-bounded-claims.md)（Repositoryの横断的な考察。規範やMappingではない）

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
