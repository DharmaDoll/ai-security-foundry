---
title: "受信したClient Access Tokenを下流APIへ転送しない"
versioned_id: "v1.0-C10.2.7"
requirement_id: "C10.2.7"
verification_level: 2
family_id: "C10"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-02-Authentication-Authorization.md"
last_verified: "2026-09-23"
maturity: "verifiable"
mapping_assessment_refs: []
---

# 受信したClient Access Tokenを下流APIへ転送しない

AISVS Verification Level: 2

## Upstream basis

AISVS `v1.0-C10.2.7`は、MCP ServerがClientから受信したAccess Tokenを
下流APIへPass-throughしないことを求める。採用済みstable v1.0の固定Revisionで、
要件本文とC10.2 Researchの要件別Threat、Verification、Gapsを確認した。
これは最新のMCP仕様や製品機能への追従を意味しない。

Researchは、受信Tokenを下流ResourceへRelayする設計を、権限混同と過大な下流Accessを
招く失敗として扱い、下流向けに別途取得した短命・限定的なCredentialを例示する。
以下のProperty、境界、試験条件はRepository interpretationである。Researchが挙げる
Token Exchangeや特定製品を唯一の適合方式にせず、製品・統計・事件の記述を適合根拠として
そのまま採用しない。

## Interpretation

MCP ClientからMCP Serverへ提示されたAccess Tokenは、そのMCP ServerというResourceに
AccessするためのCredentialである。MCP Serverが文書API、決済API、Cloud API等を呼ぶとき、
その受信Tokenを下流APIの`Authorization` Headerや別のCredential入力として使ってはならない。

利用者から委任されたIdentity・Scopeを下流へ維持することと、同じTokenを引き回すことは別である。
下流Accessが必要なら、対象Resource向けに別途取得・選択されたCredentialを使用する。
方式はToken Exchange、On-Behalf-Of、Workload Credential等に固定しない。元Tokenを正規の
Authorization ServerまたはCredential Brokerへ、定義された交換Protocolの入力として提示し、
対象Resource向けの別Credentialを得ることは、元Tokenを下流のBusiness APIのAccess Credential
としてPass-throughすることとは区別する。

## Security objective

一つのBearer Tokenが本来のAudienceを越えて複数Resourceの鍵として機能する状態を防ぎ、
MCP Server侵害、転送先すり替え、下流Log、Proxy、Telemetry等からのToken漏えいと、
下流側での権限混同・ReplayのBlast Radiusを制限する。

## Applicability

ClientからAccess Tokenを受信し、処理のために別のAPIまたはResource Serverを呼び出す
MCP Serverに適用する。直接呼出しだけでなく、Gateway、Proxy、SDK、Retry Worker、Queue Consumer、
Fallback経路を介する下流呼出しも対象とする。

### Non-applicability

Client Access Tokenを受信しない構成、またはMCP Serverが認証を要する下流APIを一切呼ばない
構成には、このPass-through禁止を評価する対象経路がない。stdioやLocal実行であることだけを
理由に対象外とはしない。Credentialを受け取り、別Resourceへ送れる経路があれば適用する。

## Scope and assumptions

- 「Client Token」は、ClientがMCP ServerへのAccess Credentialとして提示したTokenを指す。
- 「下流API」は、MCP Serverが処理のために呼ぶ別のResource Serverを指す。
- 正規のToken交換先は、信頼関係・許可先・Protocol・送信項目を定義したIdentity境界として
  評価する。任意URLへ元Tokenを送れる汎用ProxyはCredential Brokerとは扱わない。
- Tokenの文字列一致だけでなく、Header、Body、Query、Cookie、Metadata、例外、Trace等を
  通じて元Tokenが下流へ渡る経路を対象とする。
- 対象構成、下流一覧、Credential Flow、Fallback動作を検証前に固定する。未確認経路を
  安全と仮定しない。

## Assets, actors, identities, and trust boundaries

| 要素 | 本Controlでの役割 |
|---|---|
| MCP Client | MCP Server向けAccess Tokenを提示するCaller。 |
| MCP Server | 受信Tokenを検証し、必要に応じて下流操作を仲介する。 |
| Authorization Server / Credential Broker | 定義された交換により下流向けCredentialを発行し得るIdentity境界。 |
| Downstream API | MCP Serverとは別のAudience・Policy・資産を持つResource Server。 |
| Gateway / Proxy / SDK / Worker | HeaderやCredentialを暗黙に複製し得る中継要素。 |

主要なTrust Boundaryは、Client→MCP Server、MCP Server→Credential取得境界、
MCP Server→各下流APIである。決定論的なEnforcement Pointは、下流要求を組み立てるEgress経路と、
そこへCredentialを注入する機構に置く。

## Required security properties

Security Invariantは守るべき性質、Enforcement Pointはそれを実際に強制する場所を指す。

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Clientから受信したAccess Tokenを、下流APIに対するAccess Credentialとして送信しない。 |
| SP-2 | 下流Accessには、対象下流Resource向けに別途取得または選択したCredentialを使う。Credentialを取得できない場合は元TokenへFallbackせず、安全に失敗する。 |
| SP-3 | Direct呼出し、Proxy、Redirect、Retry、Queue、Error処理を含む全対象Egress経路でSP-1を維持する。 |
| SP-4 | 下流向けCredentialの取得・注入は、Model出力やClient入力が任意の送信先・Credential Source・Header転送を指定できない決定論的な境界で行う。 |

## Scope calibration and adjacent assurance

本Controlの直接のPass/Failは、Client Tokenが下流APIのCredentialとして転送されるかで決まる。
別TokenであってもAudience、Scope、Tenant、Subject、期限が不適切なら危険だが、それだけで
C10.2.7のToken Pass-throughが発生したとは限らない。下流Credentialの最小権限、委任元の
権限範囲維持、個別Tool・引数の認可、Tokenの現在性は隣接する保証として別に評価する。

同様に、元TokenのLog出力やModel Contextへの露出は重大なCredential漏えいだが、下流APIへの
Pass-throughとは別のFailureである。ただし、Logging AgentやTelemetry EndpointがTokenを
Credentialとして受理・利用する設計なら本Controlの対象になる。

## Threat and failure-mode rationale

MCP Serverや共通HTTP ClientがInbound `Authorization` Headerをそのまま複製すると、別Audienceの
APIへBearer Tokenが露出する。下流がAudienceを厳密に検証しない場合は不正Accessへ直結し、
検証して拒否する場合でも、下流Logや観測基盤に再利用可能なTokenを残し得る。攻撃者は
Tool引数、URL、Redirect、Plugin設定、障害時Fallbackを操作し、自身のEndpointへTokenをRelay
させる可能性がある。

このControlでは、追加の外部脅威IDを採用するだけの技術的Mapping評価をまだ行っていない。
失敗経路を具体化し、`threat_mappings`は空とする。MappingはSourceの固定版と関係の強さを
別途評価した場合にのみ追加する。

## Verification

### Architecture and configuration review

Client Tokenの受信から破棄までと、各下流Credentialの取得・注入・破棄までをCredential Flowで
追跡する。下流一覧、Audience、Credential Source、Egress Client、Proxy、Redirect Policy、
Retry/Fallback、Queue、Telemetryを確認する。FrameworkやSDKがInbound Headerを下流へ自動転送
しないことを、設定だけでなく実装または実行結果で確かめる。

正規のToken交換を使う場合は、交換先が固定・許可され、元TokenがBusiness APIではなく定義済みの
Identity境界へ交換入力としてのみ送られ、返されたCredentialが対象下流向けに区別できることを
確認する。

### Positive verification

模擬のClient Tokenで許可されたMCP操作を実行し、下流APIには別の下流向けCredentialが提示されて
正常完了することを示す。Credential方式がService Identity等でClient Tokenを下流へ伝えない場合も、
採用した認可Modelどおりの正常動作を確認する。

### Negative and abuse-case verification

許可された試験環境と模擬Tokenを用い、下流側のMockまたはEgress観測点でTokenのRaw値を永続化せず、
一方向Fingerprintや試験用Markerにより転送有無を判定する。

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Client Tokenを持つ正常要求から下流APIを呼ぶ | 下流のHeader、Body、Query、Cookie、Metadataに元Tokenがなく、下流向けCredentialで成功する。SP-1, SP-2 |
| N-2 | 下流Credential取得・交換を失敗させる | 元Tokenや共通CredentialへFallbackせず、下流操作を実行しない。SP-2 |
| N-3 | Tool引数やModel出力で下流URL、Redirect先、`Authorization` Headerを攻撃者Endpointへ変更させる | 許可されない送信先・Header転送を拒否し、元Tokenを送らない。SP-3, SP-4 |
| N-4 | Retry、非同期Worker、Queue Consumer、Error処理、Proxy経由で同じ操作を実行する | すべての経路で元Tokenを送らない。SP-3 |
| N-5 | Inbound Headerを一括複製するSDK・Middleware設定を有効化する | TestまたはPolicy Gateが転送を検出して失敗し、本番構成では有効化できない。SP-1, SP-3 |
| N-6 | 許可されていないToken交換先を指定する | 元Tokenを送信せず拒否する。SP-4 |

### Failure conditions

次の観測は本ControlのFailを裏付ける。

- Client Tokenが下流APIの`Authorization` Headerまたは他のCredential入力に現れる。
- 下流Credential取得失敗時にClient Tokenを転送して処理を継続する。
- 一つでも対象Egress経路がCredential注入境界を迂回し、元Tokenを送信できる。
- Client入力またはModel出力が、元Tokenの送信先や転送Headerを自由に決められる。

対象経路が不明、試験未実施、下流観測不能の場合はPassを裏付ける証拠不足であり、
実証済みの転送と区別する。別Credentialの過大権限だけを本ControlのFailへ読み替えない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Credential Flowと下流一覧 | MCP・Identity・API管理者 | Clientから全下流Egressまで | 構成、Identity、下流、SDK変更後 | Revision・承認者を保持。実Tokenを記載しない | 各境界のAudience、Credential Source、注入点、Fallbackが追跡可能 |
| Egress実装・設定Review | 開発者と検証者 | Direct、Proxy、Worker、Queue、Retry | 関連Code・設定変更後 | 対象RevisionとReview結果を保持 | Inbound Credentialの汎用転送がなく、単一の強制点を迂回できない |
| 正常・拒否試験結果 | Test Harnessと下流Mock | N-1〜N-6と採用構成 | 関連変更後、定期回帰時 | 模擬Tokenのみ使用。Raw Tokenを保存せず試験ID・Fingerprintを保護 | 正常系は別Credentialで成功し、失敗・悪用系は元Token非送信を観測 |
| Runtime Egress証跡 | GatewayまたはAPI観測基盤 | 対象下流とCredential種別 | Release後の代表期間、Incident時 | Token値を収集せず、Audience・Issuer・Credential種別等を最小限記録 | 想定外AudienceへのClient Token利用を示す事象がない |

本Repositoryには期待値のみを置き、本番Evidence、Secret、Token、顧客情報は保存しない。
設定の存在だけでなく、正常・失敗時の実際のEgress結果を採用構成へ対応付ける。

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C5.1.2` | Agent用Tokenの短命性、最小Scope、署名を扱う。別Tokenであるだけではこれらを保証しない。 |
| `v1.0-C9.5.2` | 利用者の委任Contextを下流まで維持・強制する。C10.2.7は同じTokenのPass-throughを禁止する。 |
| `v1.0-C9.5.4` | Runtime CredentialをModel Contextから隔離する。非転送でもModelに見えるなら別の重大なFailureである。 |
| `v1.0-C10.2.2` | MCP Serverが受信TokenのIssuer、Audience、期限、Scopeを検証する。受信時の検証と下流への非転送は別である。 |
| `v1.0-C10.2.5` | 各Toolと引数値を認可する。正しい下流Credentialでも不正な操作を許可し得る。 |
| `v1.0-C10.3.5` | Client–Server間TokenのSender Constraintを扱う。盗難耐性があってもPass-throughを正当化しない。 |

## Known limitations and uncertainty

本Controlは、下流向けCredentialが最小権限であること、委任Scopeが拡大しないこと、下流APIが
認可を正しく実施すること、Tokenが他経路で漏えいしないことを単独では保証しない。
Token Exchange、On-Behalf-Of、Workload Identityのどれを採用すべきかは、Identity Provider、
利用者代理の有無、下流Resource、監査要件に依存する。

ResearchはToken Exchangeや製品例を示すが、AISVS要件本文は交換方式、Scope削減方式、
Credential形式を規定していない。本Controlは非転送を必須とし、隣接する最小権限や委任保証を
暗黙のPass条件へ拡張しない。

`verifiable`は本Artifactに解釈・脅威・検証・証拠期待値が揃った状態を表す。
製品試験の実施、製品適合、学習完了を意味しない。Engineering PatternとMappingは独立して
評価し、その存在を本Controlの成熟条件にしない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-02-Authentication-Authorization.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-23 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |
