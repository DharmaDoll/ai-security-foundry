---
title: "Modelを誘導し得る入力を検査し、検知した入力を遮断する"
versioned_id: "v1.0-C2.1.3"
requirement_id: "C2.1.3"
verification_level: 1
family_id: "C2"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md"
last_verified: "2026-09-29"
maturity: "verifiable"
mapping_assessment_refs: []
---

# Modelを誘導し得る入力を検査し、検知した入力を遮断する

AISVS Verification Level: 1

学習資料：[C2.1 Prompt Injection Defenses](../../../docs/learning/c02-input-validation/v1.0-c2.1-prompt-injection-defenses.md)

## Upstream basis

AISVS `v1.0-C2.1.3`は、Modelの振る舞いを誘導し得る**すべての入力**を非信頼として扱い、
Prompt Injection検出のRulesetまたはClassifierで検査し、Flagされた入力を遮断することを求める。
これは検査器の設置だけでなく、検知結果が実際の利用経路へ反映されることを含む。

C2.1 Researchは、User Messageだけを検査しても、RAG文書、Tool／MCP Response、Webページ、
Form Field、Memory等からの間接注入を見逃す点を補足する。Researchが提案する特定製品、
全Promptの一括検査方法、周辺のMemory TTL・Sandbox・出力対策は、本要件の一律必須条件ではない。
Normative本文を境界の正本とする。

## Interpretation

Modelに与える情報のうち、振る舞いを変え得る各入力経路を特定し、Sourceの認証状態とは別に
内容を非信頼として検査する。Flagされた入力はModel Context、Memoryへの再投入、
Agentの次段判断など当該の利用から除外またはRequestを拒否する。AlertやLogだけを出して
同じ入力を使い続けてはならない。

検査対象は「UserがText欄へ直接入力した文」だけではない。取得した文書の本文、
Tool結果、会話履歴やSummary、外部Metadataなど、後からPromptへ組み込む内容も対象になる。
入力の合成・復号・抽出で検査済みの内容が変わる場合、元の判定を無条件に流用しない。

## Security objective

直接・間接のPrompt Injectionを、Modelへ影響する前に検知・遮断する機会を作り、
既知の攻撃が下流の行動や回答を誘導する経路を狭める。未知・適応的攻撃の完全検知、
Model自体の安全性、Tool実行の認可を保証するものではない。

## Applicability

外部入力を受けるLLM Application、RAG、Agent、MCP Client、長期Memoryを再利用する
System等に適用する。Text以外でも、OCR、文字起こし、抽出MetadataとしてText化して
Modelへ渡す経路は対象に含める。直接の非Text Payloadの検査はC2.2.3／C2.2.4との境界で扱う。

### Non-applicability

Modelへ渡らず、その振る舞いにも影響しない入力は直接対象外にできる。ただしCache、Summary、
Index、Tool結果経由で後からContextへ戻るなら対象である。固定された信頼済みSystem／Developer
Policyは「攻撃者入力」と同一視しないが、外部で編集できるTemplate部分や動的挿入値は検査対象から外さない。

## Scope and assumptions

- 「Flag」は使用中のRuleset／Classifierが攻撃疑いと判定した状態を指す。検知器の閾値と誤検知処理は用途別に定義する。
- 「Block」はFlag対象を当該Model利用から除外するかRequest全体を拒否すること。Logのみ、後で調査するだけでは足りない。
- 失敗時に検査を省略して継続する経路は、本要件の検査保証を失う。安全な縮退はRequest拒否または対象入力の除外として設計する。
- 検出精度は確率的であり、正常系と攻撃系の両方で評価する。ある攻撃が検知されなかった事実は品質問題だが、
  すべての未知Payloadを検知するという絶対的なPass条件は置かない。
- サービス自体が保持する固定Policyの真正性、Model Providerの内部実装は別の保証として扱う。

## Assets, actors, identities, and trust boundaries

保護対象はSystem／Developer指示の優先順位、回答の完全性、Agentが利用するData・Tool権限。
攻撃者はUser Message、文書、Webページ、Tool Response、Memoryの一部を編集し得る。
Application、Retriever、Tool Adapter、Prompt Builder、検出器、Model、Agent Runtimeが関係する。

Trust Boundaryは、各外部・派生ContentがApplicationへ入り、Contextへ組み込まれる地点。
決定論的なEnforcement Pointは、Modelへ渡す前の入力Gateと、その後にFlag対象を
使わせないPrompt／Memory／Tool結果の組立てGate。Modelが「危険だと思った」だけでは
遮断の証拠にならない。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Modelの振る舞いを誘導し得る全入力経路を列挙し、Sourceが認証済みでも内容を非信頼として分類する。 |
| SP-2 | 各対象入力を、その利用前にPrompt Injection検出RulesetまたはClassifierへ通し、判定と実際の利用対象を対応付ける。 |
| SP-3 | Flag対象をModel Contextや後続の再利用から除外するか、当該Requestを拒否する。Alertだけで継続しない。 |
| SP-4 | 検査後の追加・復号・抽出・再構築によって新しい未検査Textが生じたら、元のPassを流用せず再評価する。 |
| SP-5 | 検査器の失敗・Timeout・設定欠落で対象入力が無検査のまま通常処理へ進まない。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| RAG文書がFlagされ、Contextから除外され、下流でも利用されない | C2.1.3のPositive Evidence。Request全体の拒否までは必須でない。 |
| SharePoint由来なので検査しない | Source認証と内容の信頼を混同しておりFail。 |
| 検出器の精度が良いがFlag後もModelへ送る | 明確にFail。検出と遮断は別々に試験する。 |
| Unicode正規化やSmuggling検出だけを実装 | C2.1.1／C2.1.2の保証であり、Injection検査と遮断の代替にならない。 |
| Tool実行を認可しない、または機密Dataを外部へ出す | C5／C9等の別保証。本ControlがPassでも安全なActionは保証されない。 |
| 生の画像・音声に攻撃指示が隠れる | 非Text検査はC2.2.3／C2.2.4も評価する。抽出Textは本Controlの対象。 |

## Threat and failure-mode rationale

攻撃者は、正当なUserが開く文書やToolの返答へ「以前の指示を無視せよ」等を紛れ込ませる。
Applicationがそれを単なる資料として取得しても、Modelは次の行動を決める文として扱い得る。
一つのMessageだけを検査する構成や、Flagを記録しても入力を使う構成では、既知の攻撃が
同じ経路を通る。Researchはこうした間接入力とLog-onlyの失敗を強調する。

外部Threat IDは本作業で独立評価していないため、Catalogの`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

RequestからModelまでのData Flowを、User入力、RAG、Tool／MCP、Web、Memory、Metadata、
OCR／文字起こし、Retry／Streaming経路で追う。各経路のSource、検査位置、判定ID、
Flag後の停止点、検査失敗時の動作を確認する。検出器の管理画面だけでなく、
実際のPrompt組立てと下流再利用の制御を確認する。

### Positive verification

通常の質問と許可された文書を入力し、判定後に用途どおりModelへ渡ることを確認する。
合成したFlag対象を含む文書を混ぜ、正常な文書だけを使う設計ならFlag文書が除外されること、
Request拒否設計ならModel呼出し自体が起きないことを観測する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | User、RAG、Tool／MCP、Memory、Web、Metadataの各経路へ合成Injectionを入れる | どの経路も検査を迂回せず、Flag時は当該利用から除外／拒否される。SP-1〜SP-3 |
| N-2 | 検出器を常にFlagへ固定したTest Doubleで、Model／Tool呼出しを追う | Flag対象がModelへ渡らず、後続のMemoryやRetryにも残らない。SP-3 |
| N-3 | 検査後に文書追加、Summary生成、復号、OCR抽出を行う | 新しいTextへ古いPassを流用せず、利用前に再評価する。SP-2, SP-4 |
| N-4 | 検出器のTimeout・例外・設定不在を起こす | 未検査Contentを通常のContextへ入れない。SP-5 |
| N-5 | FlagされたRAG文書を直接Promptからは除外し、Cache／Summary／Memoryから再投入する | 同じ対象が別経路で使われない。SP-3, SP-4 |
| N-6 | 正常なFAQ、引用、セキュリティ教育文書を入力する | 不必要な拒否を測定し、用途別閾値や例外処理を確認する。SP-2 |

N-2は遮断経路を決定論的に試す。N-1とN-6は検知器の攻撃検出力と誤検知を評価する。
一つの成功例をもって検知器の完全性を主張しない。

### Failure conditions

対象経路が検査を通らない、Flag対象が同じ利用へ進む、Logだけで処理が継続する、
検査後の新TextへPassを流用する、または検査不能時に無検査Fallbackする場合はFail。
検出器が存在する、または単一の攻撃例を遮断しただけでは、全入力経路のPassにはならない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 入力経路InventoryとData Flow | Architecture／Application Owner | Contextに入る全経路と再投入先 | Topology変更時 | Revisionを保持。実Dataは最小化 | 経路ごとの検査・遮断点を追える。 |
| Ruleset／Classifier設定 | Security／Application Owner | 用途別閾値・対象型 | 検出器／Policy更新時 | Revisionと承認履歴 | 何をFlagとするか、誤検知処理が分かる。 |
| Flag強制試験 | Test Harness | N-2〜N-5、Retry・Cacheを含む | Release・経路変更時 | 合成Payloadと判定IDを保持 | Flag対象がModelへ渡らず、別経路で再投入されない。 |
| 精度と正常系の評価 | Security Test Owner | N-1／N-6の代表Corpus | Model・検出器更新時 | 機密Promptを保管しない | 検出漏れ・誤検知を把握し、適用範囲を限定できる。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C2.1.1` | Token化・Embedding前の正規化。Injection判定を代替しない。 |
| `v1.0-C2.1.2` | Encoding／表現Smugglingの検出・緩和。変換後の内容検査につながる。 |
| `v1.0-C2.1.6` | 信頼できる指示の優先順位を保つ。検査器を通過した入力でも必要。 |
| `v1.0-C2.2.3` | 生の非Text入力に隠れた攻撃の検査。 |
| `v1.0-C9.3.6` | 非信頼Tool出力の処理とAgent操作の構造的分離。 |

## Known limitations and uncertainty

Ruleset／Classifierは未知・適応的・多ターンの攻撃を見逃し得る。引用や教育目的の
攻撃文を誤検知する可能性もある。複数Contentを組み合わせて初めて意味が生じる攻撃は、
個別Chunkの検査だけでは見えにくい。組立て後の再評価を検討するが、信頼済みPolicy文を
非信頼入力と同一視して削除する必要はない。

本Controlの`verifiable`は記録の成熟度であり、製品適合、検知率、Prompt Injectionの
完全防止を意味しない。重要な操作は検査結果に依存せず、別の決定論的認可で守る。

## References

- [AISVS v1.0 C2 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md)
- [AISVS v1.0 C2.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md)
- [C2 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-29 | C2.1.3初版。入力経路の検査とFlag時遮断を分離して記録 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
