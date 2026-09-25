---
title: "stdio Transportを管理されたLocal環境だけに限定する"
versioned_id: "v1.0-C10.3.2"
requirement_id: "C10.3.2"
verification_level: 1
family_id: "C10"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-03-Secure-Transport.md"
last_verified: "2026-09-24"
maturity: "verifiable"
mapping_assessment_refs: []
---

# stdio Transportを管理されたLocal環境だけに限定する

AISVS Verification Level: 1

## Upstream basis

AISVS `v1.0-C10.3.2`は、stdio Transportを管理されたLocal環境でのみ許可することを求める。
採用済みstable v1.0の固定Revisionで要件本文とC10.3 Researchを確認した。

Researchは、stdioではClientがServerをSubprocessとして起動するため、Network-facingな設定API、
未信頼の`command`／`args`／`env`、Host権限の継承がCommand Executionへ直結する点を補足する。
以下の「管理されたLocal環境」の判定条件はRepository interpretationである。

## Interpretation

stdioは、同一の管理境界内でMCP Clientが承認済みServer Processを直接起動し、標準入出力を専用Channelとして
使用する場合だけ許可する。Server実行ファイル、引数、環境変数、Working Directoryを選べる主体を制限し、
Remote Userや未信頼ContentがProcess起動定義へ到達できないようにする。

「stdioという名前」「同じMachine」「Loopback」は管理された環境の証明ではない。HTTP APIやWeb UIから
任意のstdio定義を登録・試験できる設計は、Network RequestをLocal Command Executionへ変換する。

## Security objective

本来LocalなProcess間TransportをRemote Command Execution、権限継承、意図しないProcess起動の入口として
利用されることを防ぐ。

## Applicability

Desktop Agent、Developer Tool、Local Automation、Container Sidecar等がMCP Serverをstdio Subprocessとして
起動する構成と、その設定・導入・試験機能に適用する。

### Non-applicability

stdioを実装・有効化せず、Remote MCPをStreamable HTTPだけで提供する構成には直接適用しない。
一つでもLocal Server起動機能やstdio設定受付があれば、その経路は対象となる。

## Scope and assumptions

- 「Local」はNetworkから到達できないことだけでなく、起動元とProcessが同じ管理境界にあることを指す。
- 「Controlled」は起動定義の変更権限、承認済みExecutable、実行Identity、環境変数・Secretの範囲を説明できる状態である。
- C10.1.3のSandboxは重要な隣接保証であり、本ControlではTransportを置ける境界と起動入口を中心に評価する。
- Shell文字列を介さず引数配列を使うことは重要だが、許可されていないExecutable自体の実行を正当化しない。

## Assets, actors, identities, and trust boundaries

資産はHost上のFile、Credential、Environment、Network到達性、Process権限である。ActorはLocal User、MCP Client、
MCP Server Process、管理者、Remote User、未信頼Contentである。Trust Boundaryは設定入力からProcess Spawnへ、
ClientからChild Processのstdin／stdoutへ移る地点にある。Enforcement PointはServer Admission、起動設定管理、
Process Launcher、OS実行Identityである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | stdioは同一の管理されたLocal実行境界内の親子Process通信だけに使用する。 |
| SP-2 | Server Executable、Argument、Environment、Working Directoryを承認済み定義へ拘束する。 |
| SP-3 | Remote・低権限・未信頼入力がstdio起動定義を作成・変更・試験できない。 |
| SP-4 | stdio Serverが意図しないNetwork ListenerやRemote Bridgeとして公開されない。 |
| SP-5 | 起動定義の不明・未承認・検証不能時はProcessを生成せず、安全に失敗する。 |

## Scope calibration and adjacent assurance

C10.1.2は許可ServerのAdmission、C10.1.3はLocal ServerのSandboxとFile／Network／System Access制限を扱う。
本ControlがPassでも、承認済みServerに過大権限を与えればC10.1.3はFailになり得る。逆にSandboxがあっても、
Remote Userが任意Commandを選べるなら本ControlはFailである。

## Threat and failure-mode rationale

攻撃者はNetwork-facingな管理API、Project設定、未信頼Repository、Prompt／Tool入力等を通じて`command`、`args`、
`env`を変更し、MCP Clientの権限で任意Processを起動する。LocalだけのつもりのstdioをProxyやListenerで外部公開する
場合も、Remote Peerへ同じ権限を渡し得る。

外部脅威IDは別途Mapping評価していないため`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

全stdio Server定義、配置場所、所有者、変更可能主体、Executable解決、Launcher、Environment、Working Directory、
起動User、Network Listener、管理API／UIを列挙する。RepositoryやUser入力からSpawnまでのData Flowを追う。

### Positive verification

承認済みLocal User／Clientが固定されたServer定義を起動し、専用stdio Channelで通信できること、Processと設定変更の
Identity・監査記録が対応することを示す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | Remote API／UIからCanary Commandを含むstdio定義を登録・試験 | Process生成前に拒否する。SP-1, SP-3 |
| N-2 | 低権限Local Userまたは未信頼RepositoryでExecutable／args／envを変更 | 変更・起動を拒否する。SP-2, SP-3 |
| N-3 | PATH置換、相対Path、Symlinkで承認済み名を別Executableへ解決 | 実体検証で拒否する。SP-2 |
| N-4 | stdio ServerまたはBridgeを外部Interfaceへ公開 | Remote到達を許可せず、構成検査で検出する。SP-1, SP-4 |
| N-5 | 未登録・検証不能なServer定義で起動を要求 | AllowへFallbackせずProcessを生成しない。SP-5 |
| N-6 | Prompt、Tool Output、Documentから起動Commandを誘導 | Contentを起動Authorityとして扱わず拒否する。SP-2, SP-3 |

### Failure conditions

Remote Userが起動定義へ影響できる、任意Executable／Argumentを許可する、Network経由でstdioを公開する、
または未承認定義でProcessが生成される場合はFailを裏付ける。設定Inventoryがなく変更主体を説明できない場合は
Passの証拠不足とする。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| stdio Server inventory | Client／Platform Owner | 全Local Server定義 | 導入・設定変更時 | Revision・承認を保持 | 実体、引数、環境、所有者、変更者を特定可能 |
| Spawn Data Flow／Policy | Client／Security Owner | 設定入力からProcessまで | Launcher変更時 | 承認済み版を保持 | 未信頼・Remote入力がSpawnへ到達しない |
| Local-boundary Negative test | Test Harness | N-1〜N-6 | Release・設定機能変更後 | 無害なCanaryを使用 | 未許可Process・Listenerが生成されない |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C10.1.2` | 起動・接続を許可するMCP Server実体をAllowlistする。 |
| `v1.0-C10.1.3` | 許可されたLocal Serverを最小権限Sandboxで実行する。 |
| `v1.0-C10.3.1` | Network越しのRemote Serviceには認証・暗号化済みStreamable HTTPを使う。 |
| `v1.0-C10.4.7` | Local MCP Server導入時のUser Consentと取消しを扱う。 |

## Known limitations and uncertainty

管理されたLocal環境でも、承認済みExecutableの脆弱性・侵害、過大なHost権限、Secret継承は残る。
Enterprise管理外のDeveloper EndpointではInventoryと強制が難しい。「Controlled」の具体的な強度は資産・利用者・
実行基盤に応じて明示する必要がある。

`verifiable`はArtifactの成熟度であり、製品適合やLocal Processの無害性を意味しない。

## References

- [AISVS v1.0 C10要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-03-Secure-Transport.md)
- [C10全体分析](../../../docs/c10-landscape.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-24 | 解釈、適用境界、脅威、検証、証拠期待値、限界を整備 | AISVS固定Revision、Repository interpretation | 本書SP・N・Evidence expectations。製品試験は未実施 |
