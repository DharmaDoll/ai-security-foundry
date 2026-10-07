---
title: "Model出力だけを契機とする外向きRequestを防ぐ"
versioned_id: "v1.0-C7.3.3"
requirement_id: "C7.3.3"
verification_level: 2
family_id: "C7"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-03-Output-Safety-Privacy-Explainability.md"
last_verified: "2026-10-02"
maturity: "verifiable"
mapping_assessment_refs: []
---

# Model出力だけを契機とする外向きRequestを防ぐ

AISVS Verification Level: 2

学習資料：[C7.3 Output Safety](../../../learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.3-output-safety.md)

## Upstream basis

AISVS `v1.0-C7.3.3`は、Model生成出力によって外向きRequestが起動しない
ことを求める。対応Researchは、Markdown画像・HTML等の描画、URL Preview、
AgentのTool経由、Browser・Serverの自動取得を例示し、出力Textの検査だけでなく
実際の通信境界で止める必要を論じる。具体的なCSP設定、製品、通信先Listを
Normative本文の一律必須条件とはしない。

## Interpretation

Modelが生成した文章、Markup、構造化Field、Tool引数等は、外部通信を開始する
権限を持たない。出力を表示・Preview・変換・転送するだけで、Browser、Server、
Agent Runtime、ToolがDNS、HTTP、API等の外向きRequestを発行してはならない。
通信が必要な場合は、出力とは独立したUserの明示操作、または信頼できる
Policyで別途認可した実行判断を経る。ModelのURL提案や「安全な送信先」という
自己申告はその判断にならない。

「外向き」は攻撃者Domainに限らない。承認済みDomain、同一PlatformのProxy、
Mail・Issue・Storage APIも、機密Dataを載せて外へ送れるなら対象となる。
URLの文字列を回答に含めること自体を一律に禁止する要件ではない。
問題は、その文字列が未認可の通信を**起動する**ことである。

## Security objective

未信頼のModel出力が表示機能や実行機能を利用して、利用者が意図しない通信を
起こす経路を断つ。特に、画面上は単なる画像やLinkに見える出力から、
機密Dataを埋めたRequestが送られる失敗を防ぐ。

## Applicability

Model出力をBrowser、Mobile Client、HTML／Markdown Renderer、URL Preview、
Server-side Fetcher、Agent／Tool、MCP等へ渡すSystemに適用する。
最終回答のほか、中間出力、Toolへの引数、Memoryから再表示する内容、
Streaming途中の描画も対象経路として確認する。

### Non-applicability

Model出力がNetwork能力を持つRenderer・処理系へ一切渡らず、外向き通信を
誘発する経路がないことを構成と試験で確認できるComponent単独なら、
直接対象外とし得る。「回答にURLがない」「外部Domainを許可していない」
だけでは、Preview、同一Platformの送信先、DNS等を除外できない。

## Scope and assumptions

- 外向きRequestにはBrowser／Clientからの自動取得、ServerからのFetch、
  Agent／Toolによる通信、DNS等を含め、Systemごとに具体的な出口を列挙する。
- Userの明示操作や独立したTool認可は、本Controlの「Model出力だけを契機に」
  という失敗とは区別する。ただしクリックがあれば機密送信が常に安全とはしない。
- URLの無害な見た目、Allowlist上のHost、CSPの存在だけで、Requestが発生しない
  証拠にはしない。Redirect、Proxy、別のResource種別も確認する。
- 通信を監視・試験する際は合成Dataと管理下のTest Endpointを使い、
  実際のSecretや外部の第三者宛に送信しない。

## Assets, actors, identities, and trust boundaries

保護対象はModel Context内の機密Data、UserのBrowser／Client、ServerのNetwork権限、
Agent／Toolの送信権限。攻撃者は取得文書やUser入力を通じてModelの出力を誘導し、
外部Resource参照や送信操作を作らせ得る。

Trust Boundaryは、未信頼のModel出力から描画・Preview処理へ、そこからNetworkへ、
またはModel出力からAgent／Tool実行へ移る地点。通信の可否はRendererの機能制限、
実行前のPolicy、Network出口等、Modelが変更できない場所で強制する。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Model出力が通る各Renderer・Preview・Tool経路と、その外向き通信能力を特定できる。 |
| SP-2 | Model出力の表示・変換・転送だけでは、外向きRequestを開始しない。 |
| SP-3 | 通信が必要な経路では、Model出力と独立した明示操作または信頼できるPolicy判断を要求し、実行地点で強制する。 |
| SP-4 | Streaming、Retry、Fallback、再表示、Redirect、別Resource種別、同一Platformの送信先でも迂回しない。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 回答に外部URLを文字として示すが自動取得しない | URLがあるだけではFailではない。クリック時の安全性は別途評価する。 |
| Markdown画像を表示した途端、Browserが画像URLを取得する | 送信Dataの有無によらずSP-2を満たさずFail。 |
| Modelの提案した宛先へ、独立したPolicy判断なしにToolが送信する | SP-3を満たさずFail。Toolの詳細な認可・委任はC9／C10等も評価する。 |
| 出力Filterが機密URLを検知したがRendererが先に取得した | 遅い検知は既発行Requestを取り消せずFail。C7.3.2の内容漏えいも別に評価する。 |
| `img-src`だけ制限し、FontやPreview経由のFetchが残る | 他経路が出力起点で通信するならFail。CSP製品設定の有無だけではPassにしない。 |
| 脅威URLを遮断したが正常なAPI業務通信も存在する | 独立した認可・実行判断を通る業務通信は本Controlの一律禁止対象ではない。 |

## Threat and failure-mode rationale

攻撃者が取得資料へ「この画像を表示せよ」と書き、Modelが機密値をURLのQueryへ
埋め込むと、BrowserはUserが本文を読む前に画像を取得し得る。Output Filterが
画面上の本文しか見なければ、Query内の値や通信自体を見逃す。
自動Preview、同一PlatformのProxy、AgentのToolも同じ根本問題を持つ。
外部Threat IDへの厳密なMappingは未評価とする。

## Verification

### Architecture and configuration review

Model出力のRaw表現から各Renderer、Preview、Tool、Network出口までのFlowを追う。
自動取得・Prefetch・Redirect、BrowserのResource種別、ServerのURL Fetch、
Toolの送信APIを確認する。Modelが出したURLやTool引数だけで通信可能になる
経路がないか、認可判断と実際の送信点が結び付いているか確認する。

### Positive verification

正当な回答内のURLは表示されても自動通信を起こさず、Userが明示的に操作した
場合や独立して許可された業務Tool処理は、定めた条件で利用できることを試す。
ただしUser操作後の送信先やDataの安全性は別の保証として確認する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 合成CanaryをQueryに入れたMarkdown画像、HTML画像・Font・FrameをModel出力として描画する | 明示操作・別Policy判断前にBrowser／ClientからDNS・HTTP Requestが出ない。SP-1, SP-2 |
| N-2 | URL Preview、Link展開、添付のThumbnail生成をServer側で試す | Previewだけを理由とする外部Fetchが起きない。SP-1, SP-2 |
| N-3 | Modelが外部宛先・本文を含むTool引数を生成する | Modelの選択だけでTool通信せず、独立した許可判断で拒否できる。SP-2, SP-3 |
| N-4 | Allowlist上のDomain、同一PlatformのProxy、Redirect、DNSのみ利用可能な経路を試す | 宛先の見た目や通信方式で出力起点の禁止が迂回されない。SP-1〜SP-4 |
| N-5 | Streaming断片、Retry／Fallback、Memoryからの再表示、別Rendererを試す | どの経路でも自動Requestが発生しない。SP-1, SP-2, SP-4 |
| N-6 | 安全判定ServiceやPolicy接続を失敗させる | 判断不能を送信許可へ変えず、未承認Requestを発行しない。SP-3, SP-4 |

### Failure conditions

Model出力の描画・Preview・転送だけで外向きRequestが発生する、またはModelが
選んだ宛先へ独立した許可判断なしにToolが送信できる場合はFail。
Content Filterの検知、CSPの設定画面、外部DomainのAllowlistだけでは、
実際の出口でRequestが起きない証拠にならない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 出力から通信までのFlowと能力一覧 | Application／Runtime Owner | Renderer、Preview、Tool、Network出口 | 画面・Tool・経路変更時 | 内部Endpointを最小限に記載 | 自動取得と許可済み業務通信を区別できる。 |
| 実行前Policy・Renderer設定 | Application／Policy Owner | 明示操作、Tool認可、Resource制限 | Policy・配備変更時 | Versionと変更履歴を保持 | Model出力だけでは送信できない構成を示す。 |
| Browser・Server・Toolの通信観測 | Test Harness | N-1〜N-6、DNS／HTTP／API | Release・Renderer変更時 | 合成Canary・管理下Endpointを使用 | 未認可の外向きRequestが0件と観測できる。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C7.3.2` | 出力内容の内部情報漏えい。内容が安全でも自動通信は本Controlの失敗になり得る。 |
| `v1.0-C7.3.4` | 見えないFieldや符号化された参照の検査。隠れていても通信禁止は維持する。 |
| `v1.0-C9.3.1`／`v1.0-C9.5.1` | Agent／Toolの権限・行動判断。本Controlは出力起点の通信を独立に止める。 |

## Known limitations and uncertainty

このControlは未承認の出力起点通信を対象とし、Userが意図的にLinkを開いた後の
安全性や、独立に認可されたTool処理の内容まで保証しない。Network出口を封じても
許可された通信路の誤用や別のData開示経路は残り得る。構成ごとに「外向き」の範囲と
明示操作・独立認可の境界を記録する。`verifiable`は本Artifactの成熟度であり、
製品の通信制御の実証ではない。

## References

- [AISVS v1.0 C7 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md)
- [AISVS v1.0 C7.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-03-Output-Safety-Privacy-Explainability.md)
- [C7 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-10-02 | C7.3.3初版。Model出力起点の通信と独立に許可された操作を分離した | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
