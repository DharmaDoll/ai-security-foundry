---
title: "Security Evidenceは再構成でき、かつ保護されていなければならない"
document_kind: "cross-cutting-insight"
status: "draft"
last_updated: "2026-09-29"
---

# Security Evidenceは再構成でき、かつ保護されていなければならない

## 中心となる洞察

Log、Alert、Citation、変更履歴は、単体で存在するだけでは調査可能なEvidenceにならない。
誰のどの操作に由来し、どのData・Policy・Versionを使い、どの副作用へつながったかを
辿れる必要がある。一方、すべてのPromptや文書本文を広いTelemetryへ複製すると、
調査基盤そのものが機密情報の集積場所になる。

> 記録の量ではなく、必要な人が必要な連鎖を安全に再構成できることを保証する。

## 実用的なモデル

```text
Trusted identity / session
  -> request and retrieval event（source, document ID, version）
  -> model / tool / policy decision（version, rule, result）
  -> render, egress, side effect
  -> incident investigation
```

各EventをCorrelation IDで結び、調査に必要なFieldと保存期間を定義する。
高SensitivityなQuery本文や取得文書は制限されたStoreへ分離してもよいが、参照が切れれば
再構成できない。調査者のAccess、閲覧履歴、Retentionも設計する。
変更履歴では、変更できる主体が過去のEvidenceを自由に消せないようにする。

## 具体例

RAGへの不正な質問を調査する。Workspace単位のToken急増Alertだけでは、どのSessionが何を検索し、
どの文書がModel Contextへ入ったか分からない。一方、Alertへ全Prompt本文を載せれば、
Alert閲覧者と転送先へ機密情報を増殖させる。通常EventにはSession、時刻、文書ID・Version、
判断理由と制限付き参照を残し、必要な調査者だけが保護されたQueryへアクセスする。

Modelの回答に付いたCitationも同じ発想で読む。出典IDの存在、Sourceの真正性、
その箇所が主張を支持することは別の問いである。来歴は「何が起きたか」を辿る助けであり、
内容が真実・安全だったという証明にはならない。

## 設計レビューとNegative Test

- 一つのSynthetic SessionをRequest、Retrieval、Model、Policy、Egressまで追えるか。
- Parent文書、Cache Hit、再試行、Tool呼出しでもSource IDとVersionがつながるか。
- Alertだけから調査に必要なQueryへ、許可された担当者が辿れるか。
- 通常の運用Roleが保護されたQueryや文書本文を読めないか。調査者の閲覧を監査できるか。
- Model／Datasetを変更できる主体が、過去の変更記録も改ざん・削除できないか。
- CitationのSourceは存在しても、その主張を支持しない例を検出できるか。
- DetectorのAlert率やDriftを、即座に侵害の判決や自動認可Decisionへ変えていないか。

## 限界と隣接Insight

完全なLogを作っても侵害は自動的に阻止されない。誤った入力やPolicyを忠実に記録することもある。
詳細なTelemetryは調査力を高め得るが、Storage費用、Privacy、Access管理負荷も増やす。
[Security Artifactの保証範囲](security-artifacts-have-bounded-claims.md)はLog等のClaimの限界を述べる。
本Insightは、**調査で実際に使える連鎖と、その連鎖を守る運用境界**を扱う。

## Slide-ready summary

- Eventがあることと、因果を辿れることは違う。
- Alertの価値は件数ではなく、安全に調査・対処できることである。
- Provenanceは真実性ではない。LogはPreventionではない。

## 起点となった学習記録

- [C7.4：Source Attribution & Citation Integrity](../../controls/learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.4-source-attribution-and-citation-integrity.md)
- [C12.1：Request & Response Logging](../../controls/learning/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.1-request-response-logging.md)
- [C12.2：Detection and Alerting](../../controls/learning/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.2-detection-and-alerting.md)
- [C12.3：Drift Detection](../../controls/learning/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.3-model-data-and-performance-drift-detection.md)
- [C12.5：Training Data & Model Lifecycle Audit](../../controls/learning/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.5-training-data-and-model-lifecycle-audit.md)

これは学習記録から抽出したRepositoryの横断的なモデルであり、個々のAISVS要件のPass条件を追加・変更しない。
