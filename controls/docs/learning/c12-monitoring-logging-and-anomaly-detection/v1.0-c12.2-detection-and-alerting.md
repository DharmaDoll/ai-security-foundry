---
title: "AISVS C12.2 Detection and Alerting 学習ノート"
document_kind: "section-learning-note"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
section_id: "C12.2"
requirements:
  - "v1.0-C12.2.1"
  - "v1.0-C12.2.2"
  - "v1.0-C12.2.3"
  - "v1.0-C12.2.4"
  - "v1.0-C12.2.5"
  - "v1.0-C12.2.6"
last_updated: "2026-09-26"
---

# C12.2 Detection and Alerting

## 1. 文書の役割とSource separation

本書はAISVS v1.0 C12.2の全6 Requirementを、AI Applicationに対する探索的な攻撃とAI APIの悪用を題材に学ぶ講義・対話の再構成である。製品適合の証拠やControl本文の代替ではない。

- **Normative:** 固定Revisionの下表のRequirement原文とVerification Level。
- **AISVS Research:** 既知Payload、複数Turnの探索、抽出Alert、Token帰属、Covert Channelの脅威と検証例を補足する。製品名、Benchmark値、Thresholdは適合条件にしない。
- **Repository interpretation:** 単発Content、Session行動、組織横断のCampaign、Network Egressを異なる観測単位として扱い、既存基盤と費用に合わせて組み合わせる。
- **Derived insight:** 学習者は、同一Userの時間窓内の質問回数、投稿内容、別Modelによる意味判定を組み合わせる案と、Alert調査にはUser情報と投稿内容が必要という点を挙げた。

## 2. Normative Requirements

| ID | Level | AISVS English | 日本語訳 |
|---|---:|---|---|
| `v1.0-C12.2.1` | 1 | Verify that the system detects and alerts on known jailbreak patterns, prompt injection attempts, and adversarial inputs. | 既知のJailbreak Pattern、Prompt Injectionの試行、敵対的な入力を検知し、Alertを出すことを確認する。 |
| `v1.0-C12.2.2` | 2 | Verify that behavioral anomaly detection identifies unusual conversation patterns, excessive retry attempts, or probing behaviors. | 行動異常の検知により、通常と異なる会話Pattern、過剰な再試行、探索的な行動を識別できることを確認する。 |
| `v1.0-C12.2.3` | 2 | Verify that custom rules detect AI-specific threat patterns for coordinated jailbreak attempts, prompt injection, and system prompt extraction attempts. | 個別に定義したRuleにより、協調したJailbreakの試行、Prompt Injection、System Prompt抽出の試行に関するAI固有の脅威Patternを検知できることを確認する。 |
| `v1.0-C12.2.4` | 2 | Verify that extraction-alert events include offending query metadata to support investigation. | 抽出に関するAlert Eventに、調査を支える問題のQueryのMetadataが含まれることを確認する。 |
| `v1.0-C12.2.5` | 2 | Verify that token usage is tracked at granular attribution levels including per user, per session, per feature endpoint, and per team or workspace. | Token使用量を、User、Session、機能Endpoint、TeamまたはWorkspaceの単位で帰属を追跡できることを確認する。 |
| `v1.0-C12.2.6` | 3 | Verify that LLM API traffic is monitored for covert-channel indicators and communication signatures to identify malware and command-and-control (C2) activity. | MalwareとCommand-and-Control（C2）活動を識別するため、LLM API通信を隠れた通信路の兆候や通信Signatureの観点で監視することを確認する。 |

正本は[固定RevisionのC12要件本文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md)である。

## 3. C12における位置づけと保証範囲

C12.1は後から処理を再構成する記録、C12.2は脅威や異常を見つけて調査へつなぐ検知である。両者は連続するが同義ではない。Eventを保存しただけでは検知できず、Alertを出しただけでは原因を辿れない。

```text
単発Inputで既知攻撃を発見                  C12.2.1
User／Sessionの時間変化を発見             C12.2.2
AI固有のCampaignや抽出試行をRule化       C12.2.3
抽出Alertを調査可能にする                 C12.2.4
消費を正しい主体・機能へ帰属させる         C12.2.5
AI APIを悪用した隠れた通信を発見          C12.2.6
```

C12.2は、攻撃が必ず阻止されることやAlertの正しさを無条件に保証しない。認可、Tool隔離、Egress制御、Incident Responseは隣接する別のSecurity Propertyである。C12.2.5のNormative本文は帰属追跡を求めるが、特定の予算上限や自動停止方式は指定しない。

## 4. Security ObjectiveとConcrete Scenario

複数Teamが使う社内RAG Assistantを考える。User Aが10分で20回、表現を少しずつ変えてSystem Promptを聞き出そうとする。各投稿は既知Signatureに一致しないため、単発Detectorは反応しない。一方、同じ頻度で文書を探す正規User Bもいる。さらに別の攻撃者は大量のQueryでModelの振る舞いを模倣しようとする。侵害された端末では、MalwareがLLM APIを指令の送受信に使う。

守りたいものは内部指示・Modelの知的資産・利用予算・調査可能性である。投稿者のIntentは直接観測できないため、観測可能な行動とContentの組合せから疑いを評価する。誤検知で正規業務を妨げることも損失として扱う。

## 5. 初見の用語

- **Jailbreak:** Modelの安全上の制約を破らせようとする入力。
- **Prompt Injection:** 信頼できない入力や取得Contentに指示を混入させ、ModelやAgentの振る舞いを乗っ取ろうとすること。
- **Probing:** 複数の試行でSystemの反応や境界を探る行為。一件の投稿だけでは見えにくい。
- **System Prompt extraction:** ApplicationがModelへ与えた内部指示を引き出そうとすること。Modelの振る舞いを大量のQueryで複製する**Model extraction**とは異なる。C12.2.3は前者を明示し、C12.2.4のResearchは後者も中心例に扱う。
- **Query Metadata:** Queryに関連する時刻、Request ID、Actor、Session、検知理由、Fingerprint、保護された本文への参照等。どのFieldが必要かは調査目的に応じて定める。
- **Covert Channel／C2:** 一見正規の通信経路へ情報や指令を隠して運ぶ方法／侵害端末に指令を与える通信。ここではLLM APIが通信経路に悪用される。
- **False Positive／False Negative:** 正規操作を攻撃と誤ること／攻撃を見逃すこと。

## 6. Threat ModelとAbuse Path

攻撃者は投稿内容、投稿時刻、複数SessionやAccountをControlできる。Indirect Injectionでは、外部文書・Webページ・Tool ResponseもControlできる場合がある。Malwareは侵害端末から外部AI APIへ接続できる前提を置く。

```text
投稿 → 単発Signatureの回避 → 複数TurnでSystem Promptを探る
大量Query → User／Session／Featureへの帰属欠落 → 抽出と正規利用を区別できない
抽出Alert → 問題のQueryへの参照なし → 調査者が原因・影響を再構成できない
侵害端末 → 許可外のAI API通信 → Malwareの指令・情報搬出が通常Trafficへ紛れる
```

主なTrust Boundaryは、外部入力→Application、Application→Telemetry／Detector、調査者→機微なQuery、端末／Workload→外部AI APIである。検知Modelを追加しても、入力や出力を信頼済みの認可判断へ昇格させてはならない。

## 7. Security InvariantとEnforcement Point

| 対象 | 守る性質 | 決定論的に設計できる地点と限界 |
|---|---|---|
| C12.2.1〜3 | 対象の入力・行動Eventが検知経路から抜けず、Ruleの一致や異常判定がAlertへ到達する。 | Ingress／Tool境界でのEvent生成、DetectorへのRoute、Rule評価と通知。Classifier自体の正誤は決定論的には保証できない。 |
| C12.2.4 | 抽出Alertから問題のQueryとそのContextを権限のある調査者が辿れる。 | Alert Schema、Request IDの相関、制限付きContent保管先の参照整合性。 |
| C12.2.5 | 使用TokenをUser、Session、Feature、Team／Workspaceへ正しく帰属させる。 | 認証済みIdentity Contextを使うGateway／Inference Adapterの計数と集計。Model生成のUser名を信頼しない。 |
| C12.2.6 | 対象WorkloadのLLM API通信が観測経路を通り、異常なDestination・Process・Timing等を評価できる。 | Egress Gateway／Network Telemetry／Endpoint Sensor。全通信の意味やC2該当性を完全判定できるわけではない。 |

## 8. Pass／FailとScope Calibration

| 観測 | 判定 | 理由 |
|---|---|---|
| 既知のInjection FixtureでDetectorがAlertを生成し、元Requestへ辿れる | C12.2.1 Pass候補 | 確認した既知Patternへの検知・Alert経路が実動する。未知の攻撃まで保証しない。 |
| 20回の言い換え試行を複数Sessionに分けたら、単発ScanだけでなくUserの時間窓で検知される | C12.2.2 Pass候補 | 単発入力に見えないRetry／Probingを識別する。 |
| System Prompt抽出を狙う複数UserのCampaignに個別Ruleがなく、単発Scanだけに依存する | C12.2.3 Fail候補 | 協調した攻撃に対するCustom Ruleがない。 |
| 「Model抽出疑い」というAlertにWorkspace名と総Token数しかない | C12.2.4 Fail候補 | 問題のQuery Metadataがなく調査不能。C12.2.5も四つの帰属軸を満たさない。 |
| User、Session、Feature Endpoint、Workspace別のTokenを正しいTrusted Identityへ帰属させる | C12.2.5 Pass候補 | 要件の各粒度を追える。ThresholdやBudget Capは追加の運用設計。 |
| 非AI Workloadから外部LLM APIへ繰り返す通信があるが、出口側に監視がない | C12.2.6 Fail候補 | Covert Channel／C2の兆候を評価できない。 |

投稿本文の全量をAlert Payloadへ載せることは、C12.2.4のNormative原文にはない。しかし、Hashだけで内容を復元できず、調査者が正規利用と抽出試行を区別できないなら、実効性にも限界がある。保護された本文へRequest IDから辿れる設計を候補とし、保管期間、権限、閲覧監査を明示する。

## 9. 実装候補と運用負荷

以下は2026-09-26時点に確認した補助候補であり、AISVSの指定製品でも自動的な適合証拠でもない。

1. 既存のLog／SIEM基盤で、User・Session別の時間窓、拒否後の再試行、Feature別のToken消費を集計する。OpenSearch AlertingはGroup-by Bucket単位の監視を提供する。既存基盤があれば専用Detection Platformを増やさない。
2. 投稿や信頼できない取得Contentの単発検査には、NVIDIA NeMo GuardrailsのInput／Retrieval RailsやMeta Prompt Guard 2等を評価できる。MetaのModel CardはPrompt Guard 2を既知の上書き試行を分類するBinary Classifierと説明し、512 Tokenの入力枠を示す。日本語や当該製品の業務文脈での精度は別に検証する。Meta Modelの利用条件も確認する。
3. 別LLMを使った意味判定は、文面の単純一致にない疑いを発見する補助にはなるが、費用、Latency、Privacy、Prompt Injection耐性、誤判定の課題がある。まず既知Patternと時間窓の計測を行い、追加Modelの価値を実データで比較する。
4. Promptfooは攻撃・正規入力のFixtureを使った回帰評価に使えるが、Production通信の監視器ではない。保守終了が明記されたLLM Guardは新規の既定採用先としない。
5. 検知件数だけを成果にせず、誤検知、見逃し、Alert対応時間、調査の再現性、Inference費用、Telemetry保管量を測る。弱い検知信号を即時の自動遮断条件にするなら、その副作用を別途評価する。

## 10. 対話の再構成

### 問い1：20回の段階的な質問をどう検知するか

**Scenario:** 同じUserが10分間に20回質問し、少しずつSystem Promptへ近づく。各投稿は既知Signatureに一致しない。

**学習者の判断:** 同じUserの、特定時間内での連続質問回数を見る。

**整理:** C12.2.2のRetry／Probingを捉える基本Signalである。ただし回数だけでは正規の文書検索も含む。拒否後の言い換え、対象の一貫性、Session間の連続性を合わせて判断する。複数Accountへ分散する場合はC12.2.3のCampaign Ruleも必要になる。

### 問い2：正規の高頻度利用と区別するには

**学習者の判断と疑問:** 投稿内容を見たい。Ruleベースだけでは限界があるので別LLMで「System Promptを引き出そうとしているか」を判定できないか。既知のOSSを使う方が自前実装より費用対効果がよさそう。

**整理:** Contentの意味は重要だが、単発の分類結果だけでIntentを確定しない。軽量なClassifierやGuardrails、既存SIEMの時間窓Rule、評価用Fixtureを別の役割として組み合わせる。検知器の追加は運用費、Dependency、License、誤検知対応を伴う。特定OSSを必須とせず、製品の日本語・業務Dataで測る。

### 問い3：Model抽出疑いのAlertをどう調査するか

**Scenario:** Workspaceの総Token急増でAlertが出たが、Workspace名と総数しか載っていない。

**学習者の判断:** User情報と投稿内容が必要。

**整理:** 誰のどのRequestかへの帰属はC12.2.5、問題のQueryへ辿れるMetadataはC12.2.4の要点である。投稿内容は調査に役立つが、広いAlert画面へ全文を載せるのが唯一の方法ではない。Request ID、User／Session、時刻、Feature、Model、Detector理由と、権限付きのQuery本文参照を分けられる。User情報はTrusted Identityから取得し、必要以上の個人情報をAlertに複製しない。

## 11. このSectionから得られた洞察

> 単発Contentは「何が書かれたか」を示し、時間窓とSessionの相関は「何を繰り返しているか」を示す。両方がなければ、探索行動と正規利用を区別しにくい。

> Alertの価値は検知数ではなく、必要な権限を持つ人が原因を再構成し、妥当な対処を選べることにある。

> 検知Modelは観測の補助であり、認可の境界ではない。検知の不確実性を、権限分離や実行制限で補う。

これらはSourceの直接引用ではなく、講義と対話から得たRepositoryの解釈である。

## 12. 設計レビューとNegative Test

- 既知のJailbreak／Injection Fixtureで、Input・外部文書・Tool Responseのうち対象とした各入口からAlertが上がるか。
- 既知の文面に一致しない複数Turnの言い換えを、User／Sessionの時間窓で発見できるか。正規の高頻度利用で誤検知を測るか。
- 複数Accountへ分散したSystem Prompt抽出CampaignをCustom Ruleが検知できるか。
- 抽出AlertのRequest IDから、問題のQuery Metadataと許可された場合のContentへ辿れるか。許可外RoleはContentを読めないか。
- 複数User、Session、Feature Endpoint、WorkspaceのToken使用量が正しく集計され、異なるWorkspaceへ混入しないか。
- 通常はAI APIを使わないWorkloadからの外部LLM API接続を検知できるか。正規のBase64や画像入力をC2と誤る率も測るか。
- Detectorが停止・TimeoutしたときのAlert欠落を観測できるか。これをModel側の認可結果と混同していないか。

## 13. References

- [AISVS v1.0 C12 Normative Requirements](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md)
- [AISVS v1.0 C12.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-02-Abuse-Detection-Alerting.md)
- [NVIDIA NeMo Guardrails Configuration Reference](https://docs.nvidia.com/nemo/guardrails/latest/configure-guardrails/configuration-reference)
- [Meta Llama Prompt Guard 2 Model Card](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M)
- [OpenSearch per-query and per-bucket monitors](https://docs.opensearch.org/latest/observing-your-data/alerting/per-query-bucket-monitors/)
- [Promptfoo Red Team Configuration](https://github.com/promptfoo/promptfoo/blob/main/site/docs/red-team/configuration.md)
- [LLM Guard archive notice](https://github.com/protectai/llm-guard)
