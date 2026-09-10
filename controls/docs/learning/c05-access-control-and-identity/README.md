---
title: "AISVS C5 Access Control and Identity Learning Guide"
document_kind: "family-learning-guide"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
current_requirement: null
last_updated: "2026-09-08"
---

# AISVS C5 Access Control and Identity 学習ガイド

## 目的

AISVS C5の各Requirementを、現場のIdentity、Authentication、Authorization、
Classification、Tenant Isolationの設計判断に使える言葉で理解する。

全Category共通の講義形式、Source separation、対話の永続化、Naming、Quality checkは
[`../README.md`](../README.md)に従う。この文書ではC5固有のRequirement一覧、学習順、
進捗、Sourceだけを管理する。

## 進め方

原則としてC5.1から順に進める。一度に一つのRequirementだけを扱い、対応するResearch
資料へ必ず一度触れる。すべてのCaseを口頭試問にはせず、講義本文を理解の中心とする。

有益な対話になったRequirementは、対応する版付きControl Directoryの`learning.md`へ永続化する。
永続化後も、学習結果とControl maturityは独立して扱う。

## C5 Requirement一覧

LevelはAISVSのVerification Levelであり、このRepositoryのControl成熟度や学習難易度
ではない。

| Requirement | Level | 学ぶ主題 |
|---|---:|---|
| C5.1.1 | 3 | High-risk AI OperationのStep-up Authentication |
| C5.1.2 | 3 | Federated／Multi-system Agentの短命・最小Scope Token |
| C5.2.1 | 2 | AI Resourceの明示的AllowとDefault Deny |
| C5.2.2 | 2 | Retrieval／Assembly各段階でのEnd-user Authorization |
| C5.2.3 | 2 | Sensitive DataをModelへ固定せずRetrievalで扱うこと |
| C5.2.4 | 2 | Unauthorized DataのPost-inference Filtering |
| C5.2.5 | 2 | Agent Authorization PDPの隔離 |
| C5.2.6 | 3 | Privileged AccessのJust-in-time付与と自動失効 |
| C5.2.7 | 3 | Data Classification LabelのDownstream伝播 |
| C5.3.1 | 2 | Shared Model ServingにおけるTenant分離 |
| C5.3.2 | 3 | Shared ComputeにおけるTenant間の観測・干渉防止 |

## 軽量な進捗記録

現在学習中のRequirementはなし。C5全11 Requirementの学習を一巡した。完了は、学習者が
次の3点を短く説明できた時点で記録する。

- Requirementの本質
- 具体的なPass／Failとその理由
- このRequirementだけでは保証しない範囲

今後の候補は、C5一巡で得た再利用可能な洞察の整理である。Control成熟度とは別に扱う。C5全11 Requirementを
一巡したかどうかは、この一覧に
チェックを付けるだけで管理し、Module、Evidence、Session Log、日付別Statusは
管理しない。

- [x] [C5.1.1](../../../control-records/c05-access-control-and-identity/v1.0-c5.1.1-step-up-authentication/learning.md)
- [x] [C5.1.2](../../../control-records/c05-access-control-and-identity/v1.0-c5.1.2-short-lived-minimal-scoped-signed-agent-tokens/learning.md)
- [x] [C5.2.1](../../../control-records/c05-access-control-and-identity/v1.0-c5.2.1-explicit-allow-default-deny-ai-resources/learning.md)
- [x] [C5.2.2](../../../control-records/c05-access-control-and-identity/v1.0-c5.2.2-end-user-authorization-retrieval-assembly/learning.md)
- [x] [C5.2.3](../../../control-records/c05-access-control-and-identity/v1.0-c5.2.3-sensitive-data-retrieval-not-model-storage/learning.md)
- [x] [C5.2.4](../../../control-records/c05-access-control-and-identity/v1.0-c5.2.4-post-inference-authorization-filtering/learning.md)
- [x] [C5.2.5](../../../control-records/c05-access-control-and-identity/v1.0-c5.2.5-agent-authorization-pdp-isolation/learning.md)
- [x] [C5.2.6](../../../control-records/c05-access-control-and-identity/v1.0-c5.2.6-just-in-time-privileged-access/learning.md)
- [x] [C5.2.7](../../../control-records/c05-access-control-and-identity/v1.0-c5.2.7-downstream-classification-label-propagation/learning.md)
- [x] [C5.3.1](../../../control-records/c05-access-control-and-identity/v1.0-c5.3.1-shared-model-serving-tenant-isolation/learning.md)
- [x] [C5.3.2](../../../control-records/c05-access-control-and-identity/v1.0-c5.3.2-shared-compute-tenant-isolation/learning.md)

## 永続化した学習ノート

- [C5.1.1 Step-up Authentication：講義、対話、洞察](../../../control-records/c05-access-control-and-identity/v1.0-c5.1.1-step-up-authentication/learning.md)
- [C5.1.2 Agent Token：講義、対話、mTLS／DPoP比較](../../../control-records/c05-access-control-and-identity/v1.0-c5.1.2-short-lived-minimal-scoped-signed-agent-tokens/learning.md)
- [C5.2.1 AI Resource Authorization：講義、対話、Complete Mediation](../../../control-records/c05-access-control-and-identity/v1.0-c5.2.1-explicit-allow-default-deny-ai-resources/learning.md)
- [C5.2.2 Retrieval Authorization：講義、対話、委任IdentityとVector検索](../../../control-records/c05-access-control-and-identity/v1.0-c5.2.2-end-user-authorization-retrieval-assembly/learning.md)
- [C5.2.3 Sensitive Data Retrieval：講義、対話、Data ClassificationとTraining Boundary](../../../control-records/c05-access-control-and-identity/v1.0-c5.2.3-sensitive-data-retrieval-not-model-storage/learning.md)
- [C5.2.4 Post-inference Filtering：講義、対話、Trusted ProvenanceとAuthorized Response Assembly](../../../control-records/c05-access-control-and-identity/v1.0-c5.2.4-post-inference-authorization-filtering/learning.md)
- [C5.2.5 Agent Authorization PDP Isolation：講義、対話、Effective Control BoundaryとScope Calibration](../../../control-records/c05-access-control-and-identity/v1.0-c5.2.5-agent-authorization-pdp-isolation/learning.md)
- [C5.2.6 Just-in-time Privileged Access：講義、対話、CredentialとPrivilege Lifecycleの分離](../../../control-records/c05-access-control-and-identity/v1.0-c5.2.6-just-in-time-privileged-access/learning.md)
- [C5.2.7 Classification Label Propagation：講義、対話、Derived ArtifactとN/A境界](../../../control-records/c05-access-control-and-identity/v1.0-c5.2.7-downstream-classification-label-propagation/learning.md)
- [C5.3.1 Shared Model Serving：講義、対話、一般LLM Applicationへの適用と責任分界](../../../control-records/c05-access-control-and-identity/v1.0-c5.3.1-shared-model-serving-tenant-isolation/learning.md)
- [C5.3.2 Shared Compute：講義、対話、共有基盤の観測・干渉と保証の裏付け](../../../control-records/c05-access-control-and-identity/v1.0-c5.3.2-shared-compute-tenant-isolation/learning.md)

## Sources

- [OWASP AISVS v1.0 C5 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [AISVS C5 Research overview](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-Access-Control.md)
- [AISVS C5.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-01-Identity-Management-Authentication.md)
- [AISVS C5.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-02-AI-Resource-Authorization-Classification.md)
- [AISVS C5.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-03-Multi-Tenant-Isolation.md)
