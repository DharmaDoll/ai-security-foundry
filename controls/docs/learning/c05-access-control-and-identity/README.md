---
title: "AISVS C5 Access Control and Identity Learning Guide"
document_kind: "family-learning-guide"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
current_requirement: "C5.2.1"
last_updated: "2026-09-05"
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

有益な対話になったRequirementは、このDirectoryへVersioned filenameで永続化する。
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

現在はC5.2.1を学習中とする。C5.1から順に体系的に進める。完了は、学習者が
次の3点を短く説明できた時点で記録する。

- Requirementの本質
- 具体的なPass／Failとその理由
- このRequirementだけでは保証しない範囲

完了後はC5.2.2へ進む。C5全11 Requirementを一巡したかどうかは、この一覧に
チェックを付けるだけで管理し、Module、Evidence、Session Log、日付別Statusは
管理しない。

- [x] [C5.1.1](v1.0-c5.1.1-step-up-authentication.md)
- [x] [C5.1.2](v1.0-c5.1.2-short-lived-minimal-scoped-signed-agent-tokens.md)
- [ ] C5.2.1（学習中）
- [ ] C5.2.2
- [ ] C5.2.3
- [ ] C5.2.4
- [x] C5.2.5
- [ ] C5.2.6
- [ ] C5.2.7
- [ ] C5.3.1
- [ ] C5.3.2

## 永続化した学習ノート

- [C5.1.1 Step-up Authentication：講義、対話、洞察](v1.0-c5.1.1-step-up-authentication.md)
- [C5.1.2 Agent Token：講義、対話、mTLS／DPoP比較](v1.0-c5.1.2-short-lived-minimal-scoped-signed-agent-tokens.md)

## Sources

- [OWASP AISVS v1.0 C5 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [AISVS C5 Research overview](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-Access-Control.md)
- [AISVS C5.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-01-Identity-Management-Authentication.md)
- [AISVS C5.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-02-AI-Resource-Authorization-Classification.md)
- [AISVS C5.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-03-Multi-Tenant-Isolation.md)
