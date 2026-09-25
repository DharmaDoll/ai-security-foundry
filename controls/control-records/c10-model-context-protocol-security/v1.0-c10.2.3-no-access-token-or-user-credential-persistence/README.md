---
title: "MCP Resource ServerにAccess TokenやUser Credentialを永続化しない"
versioned_id: "v1.0-C10.2.3"
requirement_id: "C10.2.3"
verification_level: 1
family_id: "C10"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-02-Authentication-Authorization.md"
last_verified: "2026-09-24"
maturity: "verifiable"
mapping_assessment_refs: []
---

# MCP Resource ServerにAccess TokenやUser Credentialを永続化しない

AISVS Verification Level: 1

## Upstream basis

AISVS `v1.0-C10.2.3`は、OAuth 2.1 Resource Serverとして動くMCP ServerがAccess Tokenまたは
User Credentialを保存・永続化しないことを求める。採用済みstable v1.0の固定Revisionで要件本文と
C10.2 Researchを確認した。Researchの事件・製品例を適合条件として転記しない。

ResearchはLog、Cache、Prompt／Context履歴、Session Store、Crash Dump、Vector Store、Header Template
等をToken残存先として確認するよう補足する。以下のData Flowと試験条件はRepository interpretationである。

## Interpretation

MCP Serverは、受信したAccess Tokenや利用者のPassword・Refresh Token等を、Request処理に必要な短い
Memory上の期間を越えて保持しない。Database、File、Session Store、Queue、Log、Trace、Prompt、Memory、
Crash Dump、設定Template等へ書き込まず、再利用可能な形で残さない。

Resource Serverは提示されたAccess Tokenを検証してRequestを処理する立場であり、利用者Credentialの
保管庫にならない。別ResourceへのAccessが必要なら、C10.2.7の境界に従い、対象Resource向けCredentialを
Identity Service等から取得する。

## Security objective

MCP Server、Observability、Backup、Session、Model Context等の侵害・閲覧から、再利用可能なAccess Tokenや
User Credentialを窃取され、利用者になりすましてReplayされる経路を減らす。

## Applicability

OAuth 2.1 Resource ServerとしてAccess Tokenを受理するMCP Serverと、そのLog、Trace、Session、Queue、
Cache、Prompt／Memory、Crash Reporting、Backupを含むData Flowに適用する。

### Non-applicability

OAuth Access TokenやUser Credentialを一切受理しないMCP Serverは直接対象外になり得る。GatewayがTokenを
検証する構成でも、Serverまたは下流ObservabilityへTokenが渡るなら対象である。「暗号化Databaseへ保存」
は安全な保存方式の主張であり、本Requirementの非永続化を満たす理由にはならない。

## Scope and assumptions

- Request処理中の揮発Memory保持まで禁止すると検証自体ができないため、必要最小期間の一時保持と、
  Request／Session後にも残る再利用可能なStorageを区別する。
- TokenのHash／FingerprintもOffline照合や相関に使える場合がある。必要性、不可逆性、Retentionを評価する。
- AuditにはToken Raw値ではなく、非秘密のToken ID、Issuer、Subject別名、Decision、Request ID等を最小化して使う。
- Identity Service／Vaultが下流用Credentialを管理する場合、そのServiceのControlは別途必要である。

## Assets, actors, identities, and trust boundaries

資産はAccess Token、Refresh Token、Password、Session Credential、利用者権限である。ActorはClient、
MCP Resource Server、Gateway、Log／Trace／Crash／Backup基盤、Model、運用者、攻撃者である。Trust Boundaryは
Token受信→Verifier、Application→Observability、Application→Storage／Queue、Application→Model Contextにある。
Enforcement Pointは、Credential-aware logging redaction、Data classification／serialization、Session cleanup、
Storage schema、Context construction、Error handlingである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 受信Access TokenとUser Credentialを、Request処理に必要な最小期間・Memory範囲に限定する。 |
| SP-2 | Log、Trace、Metric、Error、Crash Dump、Database、File、Cache、Queue、Session、Backupへ再利用可能なCredentialを保存しない。 |
| SP-3 | Prompt、Model Context、Conversation履歴、RAG／Vector Store、Tool TranscriptへCredentialを入れない。 |
| SP-4 | Debug、障害、認証失敗、Session終了、Retry等の例外経路でもSP-1〜SP-3を維持する。 |
| SP-5 | Resource ServerがPasswordやRefresh Tokenを受理・保管する設計へ拡張しない。 |

## Scope calibration and adjacent assurance

Tokenを永続化しなくても、処理中Memoryの読取り、Token Pass-through、過大権限、長寿命TokenのRiskは残る。
C10.2.7、C5.1.2、Runtime Secret Isolationを別に評価する。逆に、LogへTokenを保存しているが下流へ転送
していない構成は、C10.2.7をPassし得てもC10.2.3ではFailする。

暗号化StorageやAccess Controlは漏えいRiskを下げるが、AISVS本文の非保存要求を保存許可へ変更しない。

## Threat and failure-mode rationale

正規TokenがDebug Log、Trace、Session Record、Prompt履歴へ混入すると、本来Tokenを扱わない運用者、分析者、
Model Provider、Backup Reader等が取得できる。短命Tokenでも有効期間中のReplayや、長期Credentialによる
継続Accessが可能になる。障害時だけ出力されるHeader Dumpは検出しにくい残存経路である。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Token受信から破棄までのData Flowを追い、Serializer、Log、APM、Trace、Error、Crash、Session、Cache、Queue、
Database、File、Prompt、Memory、Backup、Support Exportを列挙する。RedactionがExport前・Model投入前に行われ、
Raw Request HeaderのDefault Captureが無効であることを確認する。

### Positive verification

合成Tokenを使う正常Sessionを完了し、操作成功後にToken値や可逆表現が永続先へ存在せず、監査に必要な
非秘密Metadataだけが残ることを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 合成Tokenを正常・失敗・認証拒否Requestで送信 | Log、Trace、Error、Metric、Crash出力へ現れない。SP-2, SP-4 |
| N-2 | Debug／Verbose Mode、Header Capture、Support Exportを有効化 | Token Raw値を収集せず、危険設定を禁止またはRedactする。SP-2 |
| N-3 | Session、Queue、Cache、Database、Backup、Temp Fileを検索 | Tokenと可逆Encodingが残らない。SP-1, SP-2 |
| N-4 | Prompt、Tool Transcript、Memory／Vector Storeを検索 | CredentialがModel可視領域へ入らない。SP-3 |
| N-5 | Password／Refresh TokenをResource Serverへ提示 | 受理・保存せず、定義した認証Endpointへ誘導または拒否する。SP-5 |
| N-6 | Session終了、例外、Process Crashを発生 | Cleanup後も永続先へTokenが残らない。SP-4 |

### Failure conditions

受信Credentialが一つでも永続先・Model Context・運用Exportへ残る、Debug時だけ保存する、Resource Serverが
Refresh Token／Passwordを保管する、またはStorage Inventory不足で不存在を裏付けられない場合はFailまたは
Pass証拠不足となる。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Credential Data Flow／Storage inventory | MCP・Data Owner | 全永続・Export・Model経路 | Observability／Storage変更時 | Revisionを保持しToken値を含めない | Credentialが許可された揮発範囲外へ流れない |
| Logging／Redaction設定 | Platform／Observability Owner | Log、Trace、Crash、Support | Agent・SDK・APM更新時 | 設定変更を監査 | Raw Header／Credential Captureを防止 |
| Synthetic-token search | Test Harness | N-1〜N-6、全Backend | 関連変更後、定期回帰時 | 合成Tokenだけを使用し検索結果を保護 | Raw値・可逆表現が検出されない |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.2.6` | Session終了時にTokenを含むSession Artifactを除去する。C10.2.3はそもそもの永続化禁止を広く扱う。 |
| `v1.0-C10.2.7` | 受信Tokenを下流APIへCredentialとして転送しない。 |
| `v1.0-C9.5.4` | Runtime Secret／CredentialをModel Contextから隔離する。 |
| `v1.0-C5.1.2` | Agent Tokenの短命性・最小Scope・署名を扱う。 |

## Known limitations and uncertainty

Memory Dump、Core Dump、Swap、Runtime Instrumentation等、揮発Memoryが間接的に永続化される経路を完全に
列挙できない場合がある。Token ID等の監査MetadataもPrivacy／Correlation Riskを持つ。暗号化Channelや
短命TokenはDefense in Depthだが、非永続化の代替ではない。

`verifiable`はArtifactの成熟度であり、製品適合、学習完了、Memoryからの完全消去保証を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-02-Authentication-Authorization.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |
