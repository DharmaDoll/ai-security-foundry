---
title: "AISVS C12.5 Training Data & Model Lifecycle Audit 学習ノート"
document_kind: "section-learning-note"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
section_id: "C12.5"
requirements:
  - "v1.0-C12.5.1"
  - "v1.0-C12.5.2"
  - "v1.0-C12.5.3"
  - "v1.0-C12.5.4"
last_updated: "2026-09-27"
---

# C12.5 Training Data & Model Lifecycle Audit

## 1. 文書の役割とSource separation

本書は全4 Requirementの講義と対話の再構成である。学習の完了はControl maturityや製品適合を変更しない。

- **Normative:** 固定Revisionの下表のRequirement原文とLevel。
- **AISVS Research:** DatasetからModelへの来歴、Label変更、Model変更記録、文書の書込み時Tagの調査上の価値を補足する。
- **Repository interpretation:** 安全性の検証と、材料・変更履歴の再構成を別の保証として扱う。特定製品や全記録への一律の変更不能要件を追加しない。
- **Derived insight:** 学習者は他の記録要件との違いに疑問を持った。実行時の処理・承認履歴と、AIを構成する材料・変更履歴の違いを具体例で整理した。

## 2. Normative Requirements

| ID | Level | AISVS English | 日本語訳 |
|---|---:|---|---|
| `v1.0-C12.5.1` | 1 | Verify that dataset lineage records each dataset and its components, including all transformations, augmentations, and merges. | 各Datasetとその構成要素について、すべての変換・増強・結合を含む来歴を記録することを確認する。 |
| `v1.0-C12.5.2` | 1 | Verify that all labeling activities are recorded in logs. | すべてのLabel付け活動をLogへ記録することを確認する。 |
| `v1.0-C12.5.3` | 2 | Verify that all model changes generate immutable audit records. | すべてのModel変更について変更不能な監査記録を生成することを確認する。 |
| `v1.0-C12.5.4` | 2 | Verify that every ingested document is tagged at write time with source, writer identity, and timestamp. | 取り込むすべての文書に、書込み時点でSource、書き手のIdentity、時刻を付けることを確認する。 |

正本は[固定版のC12要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md)である。

## 3. Sectionの本質と隣接要件との違い

**今使っているAIの材料と変更履歴を、後から辿れるようにする**のがC12.5の本質である。記録基盤が他Sectionと共通でも、再構成したい対象が違う。

| Section | 後から辿りたいもの |
|---|---|
| C12.1 | 一回のAI処理で何を検索・推論・判断したか。 |
| C12.4 | Agentの重要操作で誰が何を承認・拒否・停止したか。 |
| C12.5 | Data、文書、Modelがどこから来て、どう変わったか。 |

危険な変更を防ぐことと、変更の経緯を説明できることは別である。Dataの毒入れ対策はC1、Modelの承認・検証はC3、Supply Chainの検証はC6、Memory／RAGの安全性はC8等と組み合わせる。C12.5内で変更不能を明示しているのはC12.5.3であり、他の三要件へ暗黙に同じ適合条件を追加しない。

## 4. 用語とConcrete Scenario

**Lineage（来歴）**は、元Dataから加工・結合を経て成果物へ至るつながり。**Augmentation（増強）**は、例の追加や変形等でDataを増やす工程。**Labeling**は、学習等のために項目へ分類・正解等の注釈を付ける活動であり、認可用の機密区分Tagと必ずしも同じではない。**Immutable Audit Record**は、過去の記録を後から自由に書き換えられない監査記録である。

社内Dataを洗浄・結合し、担当者または自動ServiceがLabelを付け、Modelを学習・配備する。別の取込Serviceが人事文書をRAGへ登録する。後日、誤った回答が見つかった。

調査者は、どの元Data・加工・Label変更がどのModelへ影響したか、誰がModelを変更したか、問題のRAG文書を誰がどこから取り込んだかを辿りたい。ファイル名と「latest」だけでは変更前後の対象を区別できない。

## 5. Threat ModelとTrust Boundary

攻撃者は元Data、注釈作業、取込文書、またはModel管理権限の一部を操作できる場合がある。変更記録も同じ権限で削除できれば、不正な変更とその証拠をまとめて隠せる。

```text
元Data → 加工／Label変更 → Model生成・配備
外部文書 → 取込Service → RAG文書／Chunk
各工程の操作 → 来歴・監査記録 → 調査者
```

境界を越える際、対象のVersion、処理のIdentity、時刻、変換関係が結合できることが重要である。書き手のIdentityをUserが送るBodyから無条件に採用せず、取込ServiceがTrusted Contextに基づき付与する。

## 6. Security InvariantとEnforcement Point

| 対象 | 守る性質と地点 |
|---|---|
| C12.5.1 | Pipelineが入力・出力Datasetと変換・増強・結合の関係を記録する。未記録のNotebook加工も対象Scopeから落とさない。 |
| C12.5.2 | Annotation／自動Labeling ServiceがLabel付けと変更の活動を記録する。誰が何を変えたか等はResearchに基づく調査上の具体化。 |
| C12.5.3 | Model管理・配備の変更Eventを、過去記録の変更を許さない監査境界へ残す。修正は過去の上書きではなく訂正Event等で追跡する。 |
| C12.5.4 | 取込Serviceが文書の書込み時にSource・Writer Identity・Timestampを付ける。後から推測した値で代替しない。 |

特定のWORM製品、暗号署名、完全な自動再学習を唯一の実装としない。署名による改ざん検知だけを、記録の変更・削除を防ぐことと同一視しない。

## 7. Pass／Failと保証範囲

| 観測 | 判定 |
|---|---|
| Dataset名だけ残し、加工や結合が辿れない | C12.5.1 Fail候補。 |
| Labelの最終値しかなく、Label付け活動が記録されない | C12.5.2 Fail候補。 |
| Model管理者が同じ権限で過去のModel変更記録を自由に書換え・削除できる | C12.5.3 Fail。 |
| Trusted取込Serviceが書込み時に必要な三つのTagを正しく付ける | C12.5.4 Pass候補。本文が無害との保証ではない。 |
| 文書本文に悪意があるが、取込時Tagは正しく残っている | 悪意ある本文の存在だけでC12.5.4をFailにはしない。Content防御は別に評価する。 |

外部Model APIだけを使い学習・Labelingを行わない製品では、各Requirementの対象工程とProviderの責任範囲を整理する。一部の工程がないことを理由に、RAG取込の記録まで一括で対象外としない。

## 8. 対話の再構成

### 問い1：正しいTagが付いた文書に悪意ある指示がある

**学習者の判断:** 悪意ある本文があるだけでC12.5.4はFailにならない。

**整理:** 正しい。来歴は無害さの証明ではなく、問題時に出所を辿る手掛かりである。

### 問い2：Model管理者が過去の変更記録も編集できる

**学習者の判断:** C12.5.3は満たさない。ただし他要件との違い、Sectionの本質が分かりにくい。

**整理:** 過去の記録を自由に変更できるため、変更不能という明示条件を満たさない。Section全体では「材料と変更履歴を再構成する」ことが共通軸である。C12.1の実行時処理、C12.4の重要操作・承認、C12.5のData／Modelの来歴という対象の違いを比較した。共通基盤を使うことは自然であり、別々の技術を導入する必要があるという説明ではない。

## 9. 洞察と設計レビュー

> 来歴は「安全だった」という保証ではなく、「何が起きたかを辿れる」という保証を支える。

> 操作できる人が過去の変更記録も自由に消せるなら、変更と証拠隠しを同じ権限で完結できる。

これらは対話由来のRepository interpretationである。

- Datasetの加工・増強・結合を一つずつ追い、対象Versionと成果物が結び付くか。
- Human／自動ServiceのLabel変更を試し、活動記録と対象項目を辿れるか。
- Model変更を試し、管理者による過去Recordの変更・削除も試すか。
- Source欠落、偽のWriter Identity、時刻欠落の文書を投入し、書込み時のTrusted Tag付与を確認するか。
- 学習用DataとRAG文書のScopeを区別し、対象外・Provider依存・未確認を明示するか。

## 10. References

- [AISVS v1.0 C12 Requirements](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md)
- [AISVS v1.0 C12.5 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-05-Training-Data-Model-Lifecycle-Audit.md)
