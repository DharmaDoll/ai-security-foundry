# AISVS C5 Access Control and Identity

対象はAISVS v1.0、固定Revision `78775233666a2022dcfb82037e5e029116955c00`。
以下は原文の代替や適合チェックリストではなく、各保証の違いを俯瞰するためのRepository interpretation。
完全な解釈と検証条件はリンク先のControl本文を参照する。

## Category：C5 Access Control and Identity

| 問うこと | できてはいけないこと |
|---|---|
| AIシステムが使うIdentity、権限、データ範囲、Tenant境界を、モデルの主張に依存せず維持できるか。 | Agentや共有基盤を経由したことで、本人確認・認可・データ分離が失われる。 |

## Sectionの見取り図

| Section | 問うこと | できてはいけないこと |
|---|---|---|
| C5.1 Authentication | 高Risk操作とAgent間通信で、利用主体とCredentialを十分な強さで確認できるか。 | 盗まれたSessionや広い長期Tokenだけで、高Risk操作や複数Systemへのアクセスが成立する。 |
| C5.2 Authorization | AI資源・検索・出力・特権を、信頼できるIdentityとPolicyで制限できるか。 | モデルの判断、暗黙の許可、失われたLabelにより権限外の資源やDataへ到達する。 |
| C5.3 Tenant Isolation | 共有するModel Servingと計算基盤でTenant間の状態・資源を分離できるか。 | 別Tenantの状態を観測、取得、推測、または干渉できる。 |

## Requirement単位

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C5.1.1](v1.0-c5.1.1-step-up-authentication/README.md) | 3 | 高Risk操作の直前に、現在の主体を十分な強さで再確認するか。 | 盗まれた既存Sessionだけで高Risk操作を実行できる。 |
| [C5.1.2](v1.0-c5.1.2-short-lived-minimal-scoped-signed-agent-tokens/README.md) | 3 | Agent間・System間Tokenが短命・最小Scope・検証可能か。 | 一つの長期Credentialを、別の相手・資源・目的へ転用できる。 |
| [C5.2.1](v1.0-c5.2.1-explicit-allow-default-deny-ai-resources/README.md) | 2 | AI資源への許可を明示し、それ以外を既定で拒否するか。 | 許可Ruleがない資源を暗黙に利用できる。 |
| [C5.2.2](v1.0-c5.2.2-end-user-authorization-retrieval-assembly/README.md) | 2 | 検索と回答組立の各段階で、End-userの認可範囲を保つか。 | 類似度やAgentの権限だけで、利用者に許可されない文書を検索・回答へ含める。 |
| [C5.2.3](v1.0-c5.2.3-sensitive-data-retrieval-not-model-storage/README.md) | 2 | Sensitive Dataを制御可能な検索元から必要時に取得するか。 | Sensitive DataをModel内部へ固定し、削除・認可・更新を制御できなくする。 |
| [C5.2.4](v1.0-c5.2.4-post-inference-authorization-filtering/README.md) | 2 | 推論結果を、受取主体の権限と信頼できるData根拠で制御するか。 | モデル出力だからという理由で、権限外の情報をそのまま返す。 |
| [C5.2.5](v1.0-c5.2.5-agent-authorization-pdp-isolation/README.md) | 2 | Agentの認可を判断するPDPをAgentの支配から分離するか。 | AgentがPolicy、判断入力、判断処理を変更して自分の権限を広げる。 |
| [C5.2.6](v1.0-c5.2.6-just-in-time-privileged-access/README.md) | 3 | 特権を必要な時・対象・期間だけ付与し、不要になれば失効させるか。 | 局所的に短いTokenを使っても、Privilege全体が常時有効なまま残る。 |
| [C5.2.7](v1.0-c5.2.7-downstream-classification-label-propagation/README.md) | 3 | Dataの分類をDerived Artifactと下流処理まで維持するか。 | 変換・Chunk化・転送によってLabelが失われ、必要な制御を適用できない。 |
| [C5.3.1](v1.0-c5.3.1-shared-model-serving-tenant-isolation/README.md) | 2 | 共有Model Servingの状態をTenantごとに分離するか。 | Cache、Batch、Context等を介して別Tenantの情報が混ざる。 |
| [C5.3.2](v1.0-c5.3.2-shared-compute-tenant-isolation/README.md) | 3 | 共有計算基盤でTenant間の観測と干渉を防ぐか。 | 他TenantのMemory・Storage・資源利用を観測または変更できる。 |

個別の具体例・対話・洞察は[C5学習ガイド](../../docs/learning/c05-access-control-and-identity/README.md)から各`learning.md`を参照する。

## Source

- [AISVS v1.0 C5要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)
