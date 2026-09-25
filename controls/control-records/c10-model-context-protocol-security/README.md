# AISVS C10 Model Context Protocol (MCP) Security

対象はAISVS v1.0、固定Revision `78775233666a2022dcfb82037e5e029116955c00`。
以下は原文の代替や適合チェックリストではなく、C10の保証境界と、整備済みControlへの
入口を示すRepository interpretationである。全23要件の分析と段階的な着手順序は
[C10全体分析](../../docs/c10-landscape.md)を参照する。

## Category：C10 Model Context Protocol (MCP) Security

| 問うこと | できてはいけないこと |
|---|---|
| MCPを通じて外部機能・Dataを利用するとき、許可した構成要素・相手・権限・Messageだけを信頼し、各境界で検証できるか。 | 接続成功、Server名、Session、Token、Tool定義、署名等の一つの事実だけを全体の信頼へ拡張し、意図しない権限行使やData露出を許す。 |

## Sectionの見取り図

| Section | 問うこと | できてはいけないこと |
|---|---|---|
| C10.1 Component Integrity | 導入・接続するMCP Serverの出所、許可状態、Local実行権限を制約できるか。 | 名前が一致するだけで未検証Componentを実行し、Hostの広い権限を与える。 |
| C10.2 Authentication & Authorization | 各要求とTool操作を正しい主体・Scope・引数で認可し、Credentialの境界を保てるか。 | Sessionや接続成功だけを信頼し、Tokenを別Resourceの鍵として使い回す。 |
| C10.3 Secure Transport | RemoteとLocalのTransportごとに、通信相手・要求先・Protocolを検証できるか。 | 暗号化だけでOrigin、Host、Protocol、実行環境まで安全とみなす。 |
| C10.4 Schema, Message, and Input Validation | Tool定義、入力、応答、変更、再送を利用前に検証・制限できるか。 | Schema適合や署名だけで内容まで安全とみなし、変更後も以前の承認で実行する。 |

## 整備済みRequirement

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C10.1.1](v1.0-c10.1.1-trusted-source-and-cryptographic-component-verification/README.md) | 1 | MCP Componentを信頼済みSourceから取得し、実行前に暗号的に検証するか。 | 公式らしい名前や同じ経路のChecksumだけを信じ、未承認・改ざんArtifactを実行する。 |
| [C10.1.2](v1.0-c10.1.2-allowlisted-mcp-server-admission/README.md) | 2 | Server実体を区別できるAllowlistで、許可対象だけを接続・起動するか。 | 表示名一致、Local設定、別URL、失効済みEntryで未許可Serverを利用する。 |
| [C10.1.3](v1.0-c10.1.3-least-privilege-local-server-sandbox/README.md) | 2 | Local ServerのFile・Network・System Accessを実行基盤で最小限に制限するか。 | Host Userと同権限の裸Processで動かし、侵害をHost全体へ拡大させる。 |
| [C10.2.1](v1.0-c10.2.1-per-request-access-token-validation/README.md) | 1 | MCP Serverは各RequestでAccess Tokenを検証するか。 | Session、TLS、localhost、過去の成功だけを根拠に後続Requestを通す。 |
| [C10.2.2](v1.0-c10.2.2-issuer-audience-expiration-and-scope-validation/README.md) | 1 | Issuer、Audience、Expiration、Scopeを要求ごとに検証するか。 | 署名が正しいだけで、別Issuer・別Audience・期限切れ・Scope不足のTokenを受理する。 |
| [C10.2.3](v1.0-c10.2.3-no-access-token-or-user-credential-persistence/README.md) | 1 | Resource ServerがAccess TokenやUser Credentialを永続化しないか。 | Log、Cache、Prompt、Session Store、Crash Dump等へ再利用可能なCredentialを残す。 |
| [C10.2.4](v1.0-c10.2.4-scope-filtered-tool-discovery/README.md) | 2 | `tools/list`が許可ScopeのToolだけを返すか。 | 呼出し時に拒否するからよいとして、未許可Toolの定義を列挙・露出する。 |
| [C10.2.5](v1.0-c10.2.5-per-invocation-tool-and-argument-authorization/README.md) | 2 | 各InvocationでToolと具体的Argument値を認可するか。 | 許可Toolなら、別Tenant・別Object・未許可PathをArgumentにしても実行する。 |
| [C10.2.6](v1.0-c10.2.6-session-artifact-removal/README.md) | 2 | Session終了時に再利用可能なArtifactをすべて除去・無効化するか。 | 終了後も旧Session ID、Cache、Handle、Subscription、Queued Workを残す。 |
| [C10.2.7](v1.0-c10.2.7-no-client-token-passthrough-to-downstream-apis/README.md) | 2 | Clientから受信したAccess Tokenを使い回さず、下流Resource向けの別Credentialを使うか。 | 交換失敗、Retry、Proxy、任意URL指定等で元Tokenを下流APIへ転送する。 |
| [C10.3.1](v1.0-c10.3.1-authenticated-encrypted-streamable-http/README.md) | 1 | Remote MCPを認証・暗号化済みStreamable HTTPに限定するか。 | 平文、証明書未検証、認証なし、Remote stdio／Legacy RouteへFallbackする。 |
| [C10.3.2](v1.0-c10.3.2-stdio-only-in-controlled-local-environments/README.md) | 1 | stdioを管理されたLocal親子Process境界だけで使うか。 | Remote／未信頼入力から`command`、`args`、`env`を指定してProcessを起動する。 |
| [C10.3.3](v1.0-c10.3.3-independent-origin-and-host-validation/README.md) | 2 | 全HTTP TransportでOriginとHostを独立に検証するか。 | 片方、CORS、Loopback、TLSだけを信頼してDNS Rebinding Requestを通す。 |
| [C10.3.4](v1.0-c10.3.4-minimum-mcp-protocol-version-enforcement/README.md) | 2 | Clientが最低Protocol Versionを持ち、下回る提案を拒否するか。 | 実装が理解できるという理由で旧Versionへ自動Fallbackする。 |
| [C10.3.5](v1.0-c10.3.5-sender-constrained-access-tokens/README.md) | 3 | mTLSまたはDPoPでTokenを送信ClientのKeyへ拘束するか。 | Token単体、別Key／Certificate、再利用Proof、Bearer Downgradeを受理する。 |
| [C10.4.1](v1.0-c10.4.1-validate-tool-responses-against-schemas/README.md) | 1 | Tool Responseを宣言Schemaで検証してからModel Contextへ入れるか。 | Schema外・曖昧なResponseをRaw TextへFallbackしてModelへ渡す。 |
| [C10.4.2](v1.0-c10.4.2-screen-tool-responses-for-indirect-prompt-injection/README.md) | 1 | Tool定義・応答をIndirect Prompt Injection観点で検査するか。 | 外部Dataを信頼Instructionとして連結し、Screeningだけを認可境界にする。 |
| [C10.4.3](v1.0-c10.4.3-reject-unrecognized-or-oversized-function-parameters/README.md) | 1 | 未知または過大なFunction ParameterをHandler前に拒否するか。 | 宣言外Fieldを無視・転送し、上限超過をParse／副作用後に判定する。 |
| [C10.4.4](v1.0-c10.4.4-strict-server-side-schema-validation/README.md) | 2 | 全Serverが宣言SchemaをRuntime ContractとしてStrictに強制するか。 | Client検証だけに依存し、型Coercionや広すぎるSchemaで危険値をSinkへ渡す。 |
| [C10.4.5](v1.0-c10.4.5-transport-payload-size-limits/README.md) | 2 | 全TransportでPayload SizeをBuffer／Parse前に制限するか。 | Chunking、Compression、Direct Backendで上限を迂回し、部分Messageを処理する。 |
| [C10.4.6](v1.0-c10.4.6-signed-tool-responses-with-replay-protection/README.md) | 2 | Tool ResponseをNonce・Timestamp・Contextとともに署名しReplayを検出するか。 | Nonce再利用、期限外、別Tool／UserへのResponse差替えを受理する。 |
| [C10.4.7](v1.0-c10.4.7-explicit-local-server-installation-consent/README.md) | 2 | Local Server導入前に実行内容を示し、Userが取消可能か。 | 曖昧な表示や導入経路の迂回で、未承認Processを起動する。 |
| [C10.4.8](v1.0-c10.4.8-tool-definition-change-reapproval/README.md) | 3 | Tool Definition変更を検出し、再承認までInvocationを止めるか。 | 通知だけで旧承認を流用し、変更後DefinitionをSilentにModelへ渡す。 |

未整備Requirementの行やPlaceholderは作らない。要件本文、Research、Repository解釈を確認して
個別Controlが`verifiable`になった時点で、この一覧へ追加する。

講義と対話は[C10学習ガイド](../../docs/learning/c10-model-context-protocol-security/README.md)から、
C10.1〜C10.4のSection単位で辿る。学習完了とControl maturityは独立している。

## Source

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10 Research概要](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-MCP-Security.md)
- [AISVS v1.0 C10.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-01-Component-Integrity.md)
- [AISVS v1.0 C10.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-02-Authentication-Authorization.md)
- [AISVS v1.0 C10.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-03-Secure-Transport.md)
- [AISVS v1.0 C10.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-04-Schema-Message-Validation.md)
