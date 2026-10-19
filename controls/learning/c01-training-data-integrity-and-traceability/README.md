---
title: "AISVS C1 Training Data Integrity and Traceability 学習ガイド"
document_kind: "family-learning-guide"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
current_section: "complete"
last_updated: "2026-10-17"
---

# AISVS C1 学習データの完全性と追跡可能性

C1は、モデルの学習や追加学習に使うデータについて、何を入れるか、どこから来たか、誰がどう変更したか、汚染されていないかを学ぶ。既存LLMへ検索した文書を渡すだけのRAGは、通常はモデルの学習ではない。適用範囲を先に確かめ、学習していないシステムへC1の適合を無理に求めない。

講義と保存は[共通学習方針](../README.md)に従う。学習の進捗はControlの成熟度、Mapping、製品の適合判定とは独立している。

[C1 Control概要](../../control-records/c01-training-data-integrity-and-traceability/README.md)では、C1.1〜C1.3の全13件を整備している。

## Section一覧

| Section | Requirement数 | 学ぶ主題 |
|---|---:|---|
| C1.1 Training Data Origin & Data Security | 5 | 必要な項目、出所台帳、保存・転送中の完全性、変更監視、無断利用の識別 |
| C1.2 Data Labeling and Annotation Security | 3 | Labelを作成・変更・承認する権限、Artifactの完全性、敏感な情報の保護 |
| C1.3 Training Data Quality and Security Assurance | 5 | 毒入れ、誤Label、偏り、禁止Contentを学習前に見つける |

## 軽量な進捗

C1.1〜C1.3の講義と対話を一巡した。チェックは講義と対話を一巡した印であり、Control成熟や理解度の採点ではない。

- [x] [C1.1：学習データの出所と保護](v1.0-c1.1-training-data-origin-and-security.md)
- [x] [C1.2：LabelとAnnotationの保護](v1.0-c1.2-data-labeling-and-annotation-security.md)
- [x] [C1.3：学習データの品質と安全性](v1.0-c1.3-training-data-quality-and-security-assurance.md)

## 一次資料

- [AISVS v1.0 C1 正規要件（固定Revision）](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C01-Training-Data-Integrity-and-Traceability.md)
- [AISVS v1.0 C1 Research（固定Revision）](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C01-Training-Data/C01-Training-Data.md)
