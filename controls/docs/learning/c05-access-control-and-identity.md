---
title: "AISVS C5 Access Control and Identity Learning Guide"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
current_requirement: "C5.2.5"
last_updated: "2026-09-04"
---

# AISVS C5 Access Control and Identity 学習ガイド

## 目的

AISVS C5の各Requirementを、現場の設計判断に使える言葉で理解する。
暗記、網羅的な口頭試問、Control成熟度の判定は、この学習の目的ではない。

学習進捗とControl成熟度は独立して扱う。Controlが`verifiable`でも理解済みとは
みなさず、学習が終わってもControlの成熟度は変更しない。

## 進め方

一度に一つのRequirementだけを扱う。

1. AgentがNormative Requirementと対応するAISVS Research資料を読む。
2. Agentが下記フォーマットで、単独で読んでも分かる短い教材を提示する。
3. 学習者が教材を読んだ後、2〜3問の短い質疑で理解を確かめる。
4. 誤解や現場上重要な洞察があれば教材へ反映する。
5. 次のRequirementへ進む。

すべてのRequirementと対応するResearch資料には一度触れる。ただし、すべての
Security PropertyやCaseを質問形式でなぞらない。理解の中心は教材本文に置き、
質疑は理解しづらい境界を明らかにするためだけに使う。

## Requirementごとの教材フォーマット

### 1. ひとことで

Requirementの本質を、専門用語に頼らず1〜2文で示す。

### 2. 具体的な場面

登場人物、System、Data、実行されるActionが見える一つのScenarioで説明する。
抽象的な「AI System」だけで説明しない。

### 3. 初めて出る用語

教材内で初めて使う専門用語は、使う直前または直後に必ず説明する。

- 日本語の平易な説明を先に置く。
- 検索できるよう、英語の正式名称や略語を括弧内に残す。
- その用語がScenarioのどこに存在するかも示す。
- 教材は単独で読めるよう、別Requirementで説明済みでも必要な用語は再説明する。

### 4. なぜ必要か

このRequirementがないと何が起こるかを、FailureまたはAbuse Caseで示す。

### 5. 守るべきこと

Security Invariantを平易な文で示し、誰が、何に対して、何をしてはならないかを
明確にする。

### 6. どこで守らせるか

Trust Boundaryと決定論的なEnforcement Pointを示す。ModelやAgentの判断だけに
依存する場合は、その限界を明記する。

### 7. Pass／Failの具体例

最低一つずつ示し、構成要素の有無ではなく、守るべき結果が実際に成立するかで
説明する。

### 8. このRequirementだけでは保証しないこと

隣接RequirementやDefense in Depthを混ぜず、適用範囲の外側を明示する。

### 9. まとめ

最後に次の3点を短く再掲する。

- 本質
- 見るべき境界またはEnforcement Point
- 典型的な見落とし

### 10. 確認のための質疑

原則2〜3問に絞る。

- 自分の言葉で本質を説明する問い
- 一つの具体例をPass／Fail判定する問い
- 必要な場合だけ、隣接Requirementとの境界を確認する問い

用語暗記や例外の網羅を目的とした問題は出さない。誤答は評価ではなく、教材本文の
不足または理解しづらい境界を見つける材料として扱う。

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

現在はC5.2.5を学習中とする。完了は、学習者が次の3点を短く説明できた時点で記録する。

- Requirementの本質
- 具体的なPass／Failとその理由
- このRequirementだけでは保証しない範囲

完了後はC5.2.6へ進む。C5全11 Requirementを一巡したかどうかは、この一覧に
チェックを付けるだけで管理し、Module、Evidence、Session Log、日付別Statusは
管理しない。

- [ ] C5.1.1
- [ ] C5.1.2
- [ ] C5.2.1
- [ ] C5.2.2
- [ ] C5.2.3
- [ ] C5.2.4
- [ ] C5.2.5（学習中）
- [ ] C5.2.6
- [ ] C5.2.7
- [ ] C5.3.1
- [ ] C5.3.2

## Sources

- [OWASP AISVS v1.0 C5 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [AISVS C5 Research overview](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-Access-Control.md)
- [AISVS C5.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-01-Identity-Management-Authentication.md)
- [AISVS C5.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-02-AI-Resource-Authorization-Classification.md)
- [AISVS C5.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-03-Multi-Tenant-Isolation.md)
