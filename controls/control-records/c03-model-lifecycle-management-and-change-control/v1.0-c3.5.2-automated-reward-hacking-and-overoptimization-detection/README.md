---
title: RLHF段階で報酬ハッキングや過剰最適化を自動検知する
versioned_id: v1.0-C3.5.2
requirement_id: C3.5.2
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

# RLHF段階で報酬ハッキングや過剰最適化を自動検知する

AISVS Verification Level: 3

[C3.5 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.5-pipeline-fine-tuning.md)

## Upstream basis

AISVS `v1.0-C3.5.2`は、RLHFの学習段階に、報酬ハッキングまたは報酬Modelへの過度な最適化を自動検知する仕組みを含める。
Researchは保持した独立評価、報酬分布、基準Policyとの差等を使う検知を例示する。昇格停止も推奨するが、原文が直接求める自動検知と検知後の対応を区別する。単一のKL指標等で完全検知できるとは解釈しない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

学習中に報酬Scoreの向上を本来の品質向上と無条件に同一視せず、採点の抜け道や過剰適応の兆候を自動で識別する。例えば独立した正確さ評価と報酬の食い違いを追う。検知の対象と基準、実行時点、検出結果をRun・Stepへ結び付ける。検出後の停止・採用保留・人による調査は運用として定めるが、自動停止の有無だけで本要件の検知成否を決めない。

## Security objective

点数だけが改善して実際の安全性や目的の達成が悪化する学習を、正常な改善として見逃さないようにする。

## Applicability

RLHFの学習段階と、その報酬Model、Policy、検出用の独立Probeや指標を対象とする。人間の攻撃者が直接操作しなくても、最適化が採点役の弱点を突く失敗を含む。

### Non-applicability

RLHFの学習段階がない構成は対象外とできる。別の最適化方式にも同様のRiskはあるが、本要件のScopeを黙って拡大しない。委託RLHFでは検知の証拠を確認する。

## Scope and assumptions

対象の学習方式、Run、Model・成果物の版、処理段階と保存・読込み経路を先に定義する。
試験は隔離環境の合成Data・無害な模擬ArtifactやTraceを使う。検証・検知の方式と設定を版で残し、
対象と証拠の不一致や欠落を正常扱いしない。自動処理の判定とModel自身の説明を区別する。

## Assets, actors, identities, and trust boundaries

報酬の採点とPolicy更新から、学習過程を評価する独立検知へ移る境界。資産は望ましい品質、安全性とRunの評価結果。Policy、報酬Model、Trainer、評価器と運用者が関わる。報酬を最適化する同じSignalだけで改善を判断すると評価の独立性を失う。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | RLHF段階に、定義した報酬ハッキング／過剰最適化の兆候を識別する自動検知が組み込まれる。 |
| SP-2 | 報酬Scoreの記録だけではなく、目的との乖離を検出できる条件・観測値を明示し、Run中に適用する。 |
| SP-3 | 正常改善と模擬的な不適切最適化を試し、検出結果・Run・Step、誤検出と検出不能状態を区別する。 |

## Scope calibration and adjacent assurance

C3.5.1の入力Model完全性と本Controlの学習方向の検知は独立。C3.2の最終Model評価も、Run中の自動検知の代わりにはならない。

## Threat and failure-mode rationale

迎合や回答長だけを高評価する採点役へPolicyが適応すると、Scoreは上がっても正確さが落ちる。Modelの改ざんがなくても起こるため、完全性検証だけでは防げない。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

Trainer内の検知呼出しと周期、独立ProbeのData、しきい値、評価条件、Run記録を確認する。報酬値のDashboard表示だけや、学習後の手動読解だけを自動検知と呼んでいないか点検する。

### Positive verification

合成したRun Traceで報酬と独立品質が共に改善する例を通す。別に、報酬のみ上がり正確さが下がる、または迎合が増える模擬Traceで検知が発動することを自動試験する。実Runで同じ検知経路が呼ばれることも確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 報酬増加と独立評価の悪化が同時に起こるTraceを入れる | 事前に定義した兆候が自動検知される。SP-1、SP-2。 |
| N-2 | 検知Jobを外して報酬ScoreだけLogに残す | 自動検知の欠落と識別し、監視済みとしない。SP-1。 |
| N-3 | 独立Probeを失敗・欠測させる | 正常改善と判断せず、検知不能として記録する。SP-3。 |

### Failure conditions

自動検知がない、学習段階で実行されない、報酬Scoreの記録しかない、定義した兆候を模擬試験で識別できない場合はFailまたは証拠不足。報酬Modelの欠点が見つかったことだけで検知未実施と同一視しない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 検知設計・実装設定とRun中の実行記録 | 学習・評価担当者 | 兆候・観測値・しきい値・Run／Step | Runごとと検知条件変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | Score記録と異なる自動検知が実行される |
| 正常・不適切最適化・欠測の模擬試験 | 検証担当者 | 実検知経路と対象Scope | 初回と検知器・報酬変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 検出・誤検出・不能を区別する |

## Related requirements

[C3.5.1](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.5.1-versioned-integrity-verified-models-before-rlhf/README.md)の入力Model完全性と本Controlの学習方向の検知は独立。C3.2の最終Model評価も、Run中の自動検知の代わりにはならない。
[C3 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

検知は実験的・確率的で、独立評価自体にも偏りや抜け道がある。特定の指標の正常値を全種類の報酬ハッキング不在の証明とせず、検知後の対応と評価器更新を運用で扱う。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## 関連する洞察

個別要件の理解・設計レビューを助ける参照であり、追加要件や正式なMappingではない。

- [最適化される採点基準には、目的とのずれを監視する評価が必要](../../../../docs/insights/optimization-can-exploit-the-evaluator.md)：評価点の改善と本来の目的の達成を分け、採点への過適応を確認する。
- [Security Artifactは証明できる範囲を越えて信頼しない](../../../../docs/insights/security-artifacts-have-bounded-claims.md)：署名・Schema・Manifest等が示せる保証を、内容や判断の安全性へ広げない。

## References

- [AISVS v1.0 C3 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [AISVS v1.0 C3.5 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-05-Pipeline-Fine-Tuning.md)
- [C3.5 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.5-pipeline-fine-tuning.md)
- [C3 Family概要](../README.md)



## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
