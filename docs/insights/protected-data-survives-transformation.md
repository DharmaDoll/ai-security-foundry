---
title: "Dataは形を変えてもProtectionを失わない"
document_kind: "cross-cutting-insight"
status: "draft"
last_updated: "2026-09-14"
---

# Dataは形を変えてもProtectionを失わない

## 中心となる洞察

文書をChunk、Vector、Summary、Prompt、Model Outputへ変換しても、元Dataに必要だったProtectionが自動的に
消えるわけではない。Security Reviewでは形式ではなく、情報の由来、受領権限、利用目的、下流への流れを追う。

> Unauthorized Dataは、要約・翻訳・Vector化・言い換えによってAuthorized Dataにはならない。

## 三つの軸を分ける

| 軸 | 問うこと |
|---|---|
| Classification | Data自体にどのSensitivity・取扱条件があるか |
| Authorization | 今のPrincipalがこのDataやDerived Artifactを受け取れるか |
| Model-use policy | Training、Evaluation、Feedback、Provider利用等に使ってよいか |

Sensitive DataとAccess-controlled Dataは頻繁に重なるが同義ではない。公開範囲の狭い非機密情報もあれば、
機密だが特定Roleには許可された情報もある。分類Labelだけで利用者の権限を決めず、認可だけでTraining利用を
許可しない。

## Data-bearing Stageを追う

```text
Source
  -> Ingestion
  -> Chunk / Embedding / Index
  -> Retrieval candidate
  -> Parent expansion / Secondary retrieval
  -> Reranking
  -> Prompt
  -> Model output proposal
  -> Rendering / Egress
  -> Cache / Log / Evaluation / Feedback
```

各Stageの出力は、その時点のEnd Userに許可されたDataだけで構成する。Rerankerのように候補を増やせないStageと、
Parent Expansionのように新しいProtected Dataを実体化できるStageを区別する。

SimilarityはAuthorizationではない。Vector Searchの近さではなく、Trusted Identity ContextとAuthoritative ACL、
Tenant、Group、Classification等をRetrieval、Materialization、Cache再利用のBoundaryで強制する。

## Model OutputはResponseではなくProposal

Modelが生成したTextをそのまま最終Responseと扱うと、受領権限の判断をModelへ委ねることになる。Trusted
ComponentがProvenanceと現在のEntitlementを使って認可・組立・Renderingし、初めてResponseになる。

```text
Model output proposal
  -> Trusted provenanceとの対応
  -> Requester-specific authorization
  -> Egress PEP
  -> Response
```

DLPは補助になり得るが、Requester固有のBusiness Authorizationを置き換えない。給与額をMaskしても、
「Bobの報酬はTeam平均の2倍」というUnauthorized informationが残り得る。

> 優秀なFilterを探すより、Filterが決定論的に判断できる出力構造を設計する。

## ProvenanceとLabel

Modelが自己申告したProvenanceやClassificationは、未検証のModel Outputである。Source、Retrieval Runtime、
Tool等のTrusted Componentが、Artifactと改ざん不能な形で対応を保持する。

Label Propagationは永久に同じLabelをコピーすることではない。Protectionを弱める場合は、決定論的変換、
再識別試験、Data Owner承認等を持つTrusted Reclassificationを通す。Source Label変更後のDerived Artifactや
CacheのFreshnessも扱う。

## Training入口は一つではない

Direct Fine-tuningだけでなく、Feedback、Evaluation、Quality improvement、Log、ProviderのData-use設定、
LoRA、Adapter、Checkpoint、DistillationもModel Artifactへの入口になり得る。Identifier Maskingだけで
Declassificationしたとみなさず、再識別可能性とBusiness Sensitivityを評価する。

## 設計レビューへの応用

- DataのClassification、Authorization、Model-use policyを別属性で表すか。
- UserとAgent／ServiceのIdentityを区別し、Trusted Contextから認可条件を作るか。
- Chunk MetadataとACLはAuthoritative Sourceに由来し、改ざん・陳腐化を防げるか。
- Parent、Attachment、Citation、Cache、Fallbackで権限外Dataを追加しないか。
- Model-generated Provenanceを信頼していないか。
- Chat以外のWebhook、Export、Attachment、Log等、全EgressをPEPへ通すか。
- Allow前に送信したStreaming Tokenは戻せないことを設計へ反映したか。
- Source削除・権限剥奪・Label変更がDerived Artifactへ反映されるか。

## 誤用と限界

- RAGはDataをModel Weightから分離するが、Vector、Prompt、Cache、Logから消去するわけではない。
- Schemaは決定論的評価を助けるが、Authorizationそのものではない。
- Provenanceがあっても、Sourceの正しさやPolicyの妥当性までは証明しない。
- Public Dataだけなら一部要件をN/Aにできるが、Internet公開を正式なPublic Classificationと同一視しない。

## Slide-ready summary

- TransformationはDeclassificationではない。
- SimilarityはAuthorizationではない。
- Model OutputはResponseではなくProposalである。
- Classification、Authorization、Model-use policyを分ける。
- ProtectionとProvenanceをDerived Artifact、Cache、Egressまで維持する。

## 起点となった学習記録

- [C5.2.2：Retrieval Authorization](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.2-end-user-authorization-retrieval-assembly/learning.md)
- [C5.2.3：Sensitive DataとModel Storage](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.3-sensitive-data-retrieval-not-model-storage/learning.md)
- [C5.2.4：Post-inference Authorization](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.4-post-inference-authorization-filtering/learning.md)
- [C5.2.7：Classification Label Propagation](../../controls/control-records/c05-access-control-and-identity/v1.0-c5.2.7-downstream-classification-label-propagation/learning.md)

本書は上記Controlを一つへ統合せず、Data Flowを横断して繰り返し現れたRepository interpretationを保存する。
