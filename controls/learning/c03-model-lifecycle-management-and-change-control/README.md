---
title: "AISVS C3 Model Lifecycle Management and Change Control 学習ガイド"
document_kind: "family-learning-guide"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
current_section: "complete"
last_updated: "2026-10-18"
---

# AISVS C3 モデルのライフサイクルと変更管理

C3では、モデルを選んでから本番へ投入し、変更・復旧するまでを扱う。モデルの出所と同一性、投入前の評価、段階的な配備、開発環境の分離、追加学習の各段階を区別して学ぶ。署名が正しいことと、モデルの振る舞いが安全であることは別の保証である。

講義と保存は[共通学習方針](../README.md)に従う。学習の進捗はControlの成熟度、Mapping、製品の適合判定とは独立している。

[C3 Control概要](../../control-records/c03-model-lifecycle-management-and-change-control/README.md)ではC3.1〜C3.5の全15件を整備済み。

## Section一覧

| Section | Requirement数 | 学ぶ主題 |
|---|---:|---|
| C3.1 Model Authorization & Integrity | 3 | 本番で使うModel Artifactの台帳、署名、投入時と読み込み時の検証 |
| C3.2 Model Validation & Testing | 3 | 投入前の安全評価、量子化後の再評価、Provider側の変更時の再評価 |
| C3.3 Controlled Deployment & Rollback | 3 | 段階的な配備、自動Rollback、完全な状態復元と版間の分離 |
| C3.4 Secure Development Practices | 2 | 開発・検証・本番の境界と、学習環境の分離 |
| C3.5 Pipeline Fine-Tuning | 4 | 追加学習の入力、各段階の成果物、Checkpointの検証と登録 |

## このFamilyから得られた横断的な洞察

- [採点基準への最適化と目的のずれ](../../../docs/insights/optimization-can-exploit-the-evaluator.md)：C3.5.2の対話を起点に、点数へ適応する過程を独立した評価で確認する。
- [整合した状態への復旧](../../../docs/insights/recovery-restores-a-consistent-configuration.md)：C3.3.2を起点に、復旧後の部品の組み合わせを確認する。
- [Security Artifactの保証範囲](../../../docs/insights/security-artifacts-have-bounded-claims.md)：C3.5.1の完全性と、採点役の評価品質を区別する。
- [実際に利用されるPayloadを検査する](../../../docs/insights/validation-must-cover-effective-payload.md)：C3.2.2・C3.2.3の変更後の再評価を、検査対象と使用対象の対応として考える。

Insightは対話から得た再利用可能な整理であり、Control本文や正式なMappingではない。


## 軽量な進捗

C3.1〜C3.5の講義と対話を一巡した。チェックは講義と対話を一巡した印であり、Control成熟や理解度の採点ではない。

- [x] [C3.1：承認されたモデル一式を本番で使う](v1.0-c3.1-model-authorization-and-integrity.md)
- [x] [C3.2：モデルの検証とテスト](v1.0-c3.2-model-validation-and-testing.md)
- [x] [C3.3：制御された配備と復旧](v1.0-c3.3-controlled-deployment-and-rollback.md)
- [x] [C3.4：安全な開発環境](v1.0-c3.4-secure-development-practices.md)
- [x] [C3.5：追加学習パイプライン](v1.0-c3.5-pipeline-fine-tuning.md)

## 一次資料

- [AISVS v1.0 C3 正規要件（固定Revision）](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [AISVS v1.0 C3 Research（固定Revision）](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-Model-Lifecycle-Management.md)
