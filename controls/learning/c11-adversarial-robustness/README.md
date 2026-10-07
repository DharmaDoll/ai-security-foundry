---
title: "AISVS C11 Adversarial Robustness 学習ガイド"
document_kind: "family-learning-guide"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
current_section: "C11.3"
last_updated: "2026-10-06"
---

# AISVS C11 敵対的な操作に対する耐性：学習ガイド

C11は「安全なModel」という一言を、出力の安全性、学習Dataの推測、Modelの複製、
実行時の異常という別々の問題に分けて学ぶ。攻撃を完全に防げるという意味ではない。

講義と学習ノートの共通方針は[Controls Learning Documentation](../README.md)、
Requirementごとの保証境界は[C11 Control俯瞰図](../../control-records/c11-adversarial-robustness/README.md)を参照する。
学習の進捗はControlの成熟度や製品適合と独立している。

## Section一覧

| Section | Requirement | 学ぶ主題 |
|---|---:|---|
| C11.1 Model Alignment, Safety, and Robustness Testing and Training | 5 | 訓練、更新時の試験、攻撃評価、耐性強化、悪化の測定 |
| C11.2 Membership-Inference and Model-Inversion Mitigation | 5 | 出力からの学習Data・敏感な属性の推測を抑える |
| C11.3 Model-Extraction Defense | 4 | APIを使ったModel複製の検知と対処 |
| C11.4 Model Runtime Anomaly Detection | 3 | 推論前の異常検査と改善用Feedbackの保護 |

## 軽量な進捗

現在学習中のSection：C11.3。チェックは講義と対話を一巡した印であり、理解度の採点ではない。

- [x] [C11.1：Modelの安全性と敵対的入力への耐性](v1.0-c11.1-model-alignment-safety-and-robustness.md)
- [x] [C11.2：学習Dataと機微な属性の推測](v1.0-c11.2-membership-inference-and-model-inversion-mitigation.md)
- [ ] C11.3：Modelの複製
- [ ] C11.4：実行時の異常とFeedback

## 一次資料

- [AISVS v1.0 C11 正規要件（固定Revision）](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C11-Adversarial-Robustness.md)
- [AISVS v1.0 C11 Research（固定Revision）](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C11-Adversarial-Robustness/C11-Adversarial-Robustness.md)
