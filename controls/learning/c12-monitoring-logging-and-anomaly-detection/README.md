---
title: "AISVS C12 Monitoring, Logging & Anomaly Detection 学習ガイド"
document_kind: "family-learning-guide"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
current_section: "complete"
last_updated: "2026-09-27"
---

# AISVS C12 Monitoring, Logging & Anomaly Detection 学習ガイド

## 目的

C12を製品別のLog設定集ではなく、AI Systemの処理を再構成し、異常を検知・調査できるかという観点で学ぶ。C5・C8・C9・C10で扱った認可、検索、Agent行動、MCPの失敗を運用中に観測する保証である。

1. AIとのやり取り、Policy判断、検索結果を、同じ処理へ結び付けられるか。
2. 攻撃や異常を検知し、調査に必要なContextを残せるか。
3. Model・Dataの変化とAgentの自発的行動を追えるか。
4. Training DataとModel Artifactの変更履歴を辿れるか。
5. 調査に必要な記録と、Log自体への機密情報の集中をどう両立するか。

全Category共通の講義・保存方法は[学習方針](../README.md)に従う。C12の21 Requirementを個別の学習ファイルへ分けず、Section単位で学ぶ。学習進捗はControl maturityや製品適合を示さない。

## Section一覧

| Section | Requirement | Level内訳 | 学ぶ主題 |
|---|---:|---|---|
| C12.1 Request & Response Logging | 4 | L1：1、L2：3 | Session・推論・Policy・RAG検索の追跡と機密性 |
| C12.2 Detection and Alerting | 6 | L1：1、L2：4、L3：1 | 攻撃・異常行動・Token使用・Covert Channelの検知 |
| C12.3 Model, Data, and Performance Drift Detection | 4 | L1：1、L2：2、L3：1 | Input分布、幻覚、振る舞い変化の継続監視 |
| C12.4 Proactive Security Behavior Monitoring | 3 | L2：3 | Agentの自発的行動、承認、停止操作の監査 |
| C12.5 Training Data & Model Lifecycle Audit | 4 | L1：2、L2：2 | Dataset、Label、Model、取込文書の変更履歴 |

## 軽量な進捗記録

全5 Section・21 Requirementの講義と対話を保存済み。Control成熟・製品適合の完了を意味しない。

- [x] [C12.1 Request & Response Logging](v1.0-c12.1-request-response-logging.md)
- [x] [C12.2 Detection and Alerting](v1.0-c12.2-detection-and-alerting.md)
- [x] [C12.3 Model, Data, and Performance Drift Detection](v1.0-c12.3-model-data-and-performance-drift-detection.md)
- [x] [C12.4 Proactive Security Behavior Monitoring](v1.0-c12.4-proactive-security-behavior-monitoring.md)
- [x] [C12.5 Training Data & Model Lifecycle Audit](v1.0-c12.5-training-data-and-model-lifecycle-audit.md)

実質的な講義と対話を保存するときだけ、版付きSectionファイルを追加する。空のSectionファイルやRequirement別のPlaceholderは作らない。

## このFamilyの学習から生まれた横断的Insight

- [再構成でき、保護されたSecurity Evidence](../../../docs/insights/security-evidence-must-be-reconstructable-and-constrained.md)：C12.1・C12.2・C12.5のEvent、Alert、変更履歴を調査可能かつ最小限に扱う。
- [Security Artifactの保証範囲](../../../docs/insights/security-artifacts-have-bounded-claims.md)：C12.3のDrift Signalを侵害の確証や認可Decisionと混同しない。

これらは学習の起点を示すLinkであり、正式なMappingではない。

## Sources

- [AISVS v1.0 C12 Normative Requirements](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md)
- [AISVS v1.0 C12.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-01-Request-Response-Logging.md)
- [AISVS v1.0 C12.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-02-Abuse-Detection-Alerting.md)
- [AISVS v1.0 C12.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-03-Model-Drift-Detection.md)
- [AISVS v1.0 C12.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-04-Proactive-Security-Behavior-Monitoring.md)
- [AISVS v1.0 C12.5 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-05-Training-Data-Model-Lifecycle-Audit.md)

Researchの実装例や製品仕様をNormativeな適合条件として扱わない。Sourceの版・Statusと、Repository interpretationを区別する。
