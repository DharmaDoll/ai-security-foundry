# C3 Model Lifecycle Management & Change Control

本番で使うModel一式の出所・完全性、投入前評価、配備・復旧、環境分離、追加学習段階の成果物を区別して保証する。
基準は[AISVS v1.0固定Revision](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)であり、1.01への移行ではない。
[学習ガイド](../../learning/c03-model-lifecycle-management-and-change-control/README.md)の進捗はControl成熟度や製品適合と独立している。

## Sectionの見取り図

| Section | 問うこと | できてはいけないこと |
|---|---|---|
| [C3.1 Model Authorization & Integrity](#c31-model-authorization--integrity) | 本番の構成物を把握し、権限ある主体の署名を投入・読込みで検証するか | Model名や重みだけで一式の同一性を主張する |
| [C3.2 Model Validation & Testing](#c32-model-validation--testing) | 投入前と量子化・Provider変更後に実際の対象を評価するか | 署名の成功を安全性評価に読み替える |
| [C3.3 Controlled Deployment & Rollback](#c33-controlled-deployment--rollback) | 切替を制御し、完全な状態へ復旧し、並行版を分離するか | 重みだけ戻して復旧済みとみなす |
| [C3.4 Secure Development Practices](#c34-secure-development-practices) | 環境の境界と学習基盤を本番から分離するか | 名前空間の違いだけで共有状態を見落とす |
| [C3.5 Pipeline Fine-Tuning](#c35-pipeline-fine-tuning) | 学習入力・段階間出力を検証し、報酬の過剰最適化とCheckpointを追うか | 最終出力の検証だけで全段階を保証する |

<a id="requirement"></a>

## Requirement一覧

C3.1〜C3.5の全15件を整備済み。各Controlの保証境界と検証を個別に確認する。
LevelはAISVS Verification Levelであり、Control成熟度や製品の適合結果ではない。

## C3.1 Model Authorization & Integrity

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C3.1.1](v1.0-c3.1.1-deployed-model-artifact-and-origin-inventory/README.md) | 1 | 本番モデルの全構成物と出所を台帳で把握するか。 | 本番で使う未登録の設定やAdapterを見逃す。 |
| [C3.1.2](v1.0-c3.1.2-authorized-signatures-for-all-model-artifacts/README.md) | 2 | モデル構成物のすべてへ権限ある主体が署名するか。 | 署名範囲外の設定や権限外の署名を正規品とみなす。 |
| [C3.1.3](v1.0-c3.1.3-signature-verification-at-admission-and-load/README.md) | 2 | 本番投入時とモデル読込み時に署名を検証するか。 | 投入後の差替えを未検証で読み込む。 |

## C3.2 Model Validation & Testing

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C3.2.1](v1.0-c3.2.1-automated-input-safety-output-tests-before-deployment/README.md) | 1 | 投入前に入力・安全性・出力無害化の自動試験を行うか。 | 入力と安全性の試験だけで出力無害化も試験済みとする。 |
| [C3.2.2](v1.0-c3.2.2-same-safety-suite-on-quantized-artifact/README.md) | 2 | 量子化後の実構成物へ同じ安全性試験を再実行するか。 | 圧縮前の合格や一般精度だけを圧縮後の安全性評価とする。 |
| [C3.2.3](v1.0-c3.2.3-security-reevaluation-before-provider-route-changes/README.md) | 3 | 提供者のモデル・版・経路変更後は継続利用前に再評価するか。 | 同じAlias名という理由で旧評価のまま使い続ける。 |

## C3.3 Controlled Deployment & Rollback

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C3.3.1](v1.0-c3.3.1-controlled-rollout-with-automated-rollback-triggers/README.md) | 2 | 本番への展開を制御し自動ロールバックを発動するか。 | 通知だけで自動Rollbackと呼ぶ。 |
| [C3.3.2](v1.0-c3.3.2-rollback-restores-complete-model-state/README.md) | 2 | ロールバックでモデルの状態全体を復元するか。 | 重みだけ戻し新設定との混合状態を復旧済みとする。 |
| [C3.3.3](v1.0-c3.3.3-parallel-model-version-runtime-state-isolation/README.md) | 2 | 並行稼働するモデル版の実行状態を分離するか。 | 並行版で同じ会話や推論Cacheを再利用する。 |

## C3.4 Secure Development Practices

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C3.4.1](v1.0-c3.4.1-ai-runtime-component-separation-across-environments/README.md) | 1 | AI実行部品を環境の境界ごとに分離するか。 | 開発・本番で本番権限付きの同じAI実行Instanceを共有する。 |
| [C3.4.2](v1.0-c3.4.2-training-and-fine-tuning-isolated-from-production/README.md) | 2 | 学習・追加学習環境を本番から分離するか。 | 別Projectという名前だけで本番への直接作用を見落とす。 |

## C3.5 Pipeline Fine-Tuning

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C3.5.1](v1.0-c3.5.1-versioned-integrity-verified-models-before-rlhf/README.md) | 2 | RLHFで使うモデルの版と完全性を使用前に確認するか。 | 報酬Modelだけを検証対象から外す。 |
| [C3.5.2](v1.0-c3.5.2-automated-reward-hacking-and-overoptimization-detection/README.md) | 3 | RLHF段階で報酬ハッキングや過剰最適化を自動検知するか。 | 報酬Scoreの増加だけで正常改善とみなす。 |
| [C3.5.3](v1.0-c3.5.3-verify-each-fine-tuning-stage-output-before-consumption/README.md) | 3 | 各追加学習段階の出力を次段階の使用前に検証するか。 | 最初だけ検証して後続段階は未検証で使う。 |
| [C3.5.4](v1.0-c3.5.4-fine-tuning-checkpoints-registered-as-distinct-artifacts/README.md) | 3 | 追加学習の各チェックポイントを別成果物として登録するか。 | Latestの上書きだけで各Checkpointを区別不能にする。 |

## 隣接する保証との違い

台帳は対象の把握、署名は内容と署名者の結び付き、検証は実経路での拒否を支える。
C3.1が成立してもModelの安全な振る舞いは示せず、C3.2等を別に評価する。
C6の供給元評価やC11の耐性評価、C12の監査Logも各々の保証境界を保つ。
Researchにある製品名・版・Scanner推奨・事件の記述は、原文の追加必須条件として自動採用しない。

## References

- [AISVS v1.0 C3 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [AISVS v1.0 C3.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-01-Model-Authorization-Integrity.md)
- [AISVS v1.0 C3.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-02-Model-Validation-Testing.md)
- [AISVS v1.0 C3.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-03-Controlled-Deployment-Rollback.md)
- [AISVS v1.0 C3.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-04-Secure-Development-Practices.md)
- [AISVS v1.0 C3.5 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-05-Pipeline-Fine-Tuning.md)
- [C3学習ガイド](../../learning/c03-model-lifecycle-management-and-change-control/README.md)
