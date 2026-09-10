---
title: "Sensitive Data Retrieval Instead of Model Storage"
versioned_id: "v1.0-C5.2.3"
requirement_id: "C5.2.3"
verification_level: 2
family_id: "C5"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-02-AI-Resource-Authorization-Classification.md"
last_verified: "2026-09-08"
maturity: "verifiable"
mapping_assessment_refs: []
---

# Sensitive DataをModelへ固定せずRetrievalで扱う

AISVS Verification Level: 2

初めて読む方へ：[具体例・用語・対話を含む学習ノート](learning.md)。

## Upstream basis

AISVS `v1.0-C5.2.3`、Verification Level 2を解釈する。Sensitive DataをModelへ恒久保存
しないため、必要なDataをRetrieval Pipelineから取得することを求める。
固定RevisionのC5.2 Research（Last Researched: 2026-07-14）の該当行を確認した。
ResearchはTraining/Fine-tuning、Providerの利用設定、Feedbackからの再混入、Canary試験を補足する。
RetrievalはVector検索に限定されず、必要なDataを外部Sourceから取得する方式を含む。

以下は実務上の解釈であり、特定のDLP、RAG製品、契約文面を必須とはしない。

## Interpretation

**保護や更新が必要なSensitive RecordをModelの学習結果へ埋め込まず、
管理可能な外部Sourceに置き、必要時に取得する。**

社員の給与回答を作る場合、社員RecordをFine-tuningで覚えさせるのではなく、
HR API等から必要時に取得する。Base Modelを変えなくても、Adapterへ学習させれば
永続Model Artifactへの固定という問題は残る。AdapterはModelの挙動を調整する学習済みParameterである。

## Security objective

Modelへ固定されたDataについて、通常のRecord単位の訂正・削除・受取権限管理が難しくなること、
記憶された情報を推論から引き出されることを避ける。
本ControlはModelがあらゆる秘密を記憶していないという数学的証明を要求するものではない。

## Applicability

Sensitive Dataを扱うAI SystemのTraining、Fine-tuning、Adapter生成、Retrieval、
Providerへの入力、Prompt/ResponseからFeedback・再学習へ戻る経路を対象とする。

### Non-applicability

対象Data flowにSensitive Dataがない場合は、分類根拠と用途を示してN/Aを判断する。
アクセス制限付きDataすべてがSensitiveとは限らず、逆に全社員が読めても未公開戦略はSensitiveになり得る。
Sensitive Fine-tuningが業務上必要でも、本要件への適合とは呼ばない。
例外のData範囲、Modelの扱い、代替対策、訂正・削除の限界を別途記録する。

## Scope and assumptions

Sensitiveの判断は、漏えい・残存・目的外利用の影響、契約や組織の分類Policyによる。
原文は一律の分類体系を定めないため、Data Ownerと分類根拠を特定する。
分類、利用者の読取権限、Training利用可否は別軸である。利用同意だけでSensitiveという性質は消えない。

Modelへの恒久保存はWeight、学習済みAdapter、Checkpoint等を対象とする。
Prompt、Vector Index、Logへの保存は直ちにModel学習ではないが、再学習へ戻れば対象になる。
未知の由来やTraining可否を自動的に許可しないことは、境界を有効にするためのRepository解釈である。

## Assets, actors, identities, and trust boundaries

AssetsはSensitive Source、Dataset、Model/Adapter、Prompt/Feedback。
ActorsはData Owner、Dataset作成者、学習Job、Inference Service、Provider、利用者。
境界はSourceから取得、Datasetから学習、Providerへの入力、保存された会話から再学習である。
EnforcementはDataset/Job受付、ProviderのData-use制御、Feedback選別等に置く。
Policy文書やModelへの「学習しない」というPromptだけは強制機構にならない。

## Required security properties

| ID | 必要な性質 | 成立条件 |
|---|---|---|
| SP-1 | 対象Dataの特定 | Sensitive DataとTraining可否、その判断元を特定できる |
| SP-2 | Retrievalによる利用 | 必要なSensitive情報を外部Sourceから取得し、学習済み記憶に依存しない |
| SP-3 | 学習経路からの除外 | Training/Fine-tuning/Adapter、直接Job、Provider側利用で対象Dataを入れない |
| SP-4 | 循環経路の制御 | Prompt、Log、評価・Feedback等から対象Dataが再学習へ戻らない |

## Scope calibration and adjacent assurance

| 状況 | 評価 |
|---|---|
| Sensitive RecordをAdapterへFine-tuningする | Fail |
| Retrievalで使った会話が自動的に再学習Datasetへ入る | Fail |
| 外部APIから取得し、全学習経路から除外する | Pass候補 |
| Vector IndexへSensitive Chunkを保存する | 本要件単独でFailではない。Index認可・保持等は別途必要 |
| Provider Logへ保存するが学習に使わない | Model固定とは別。保持や第三者開示の評価は必要 |
| Training禁止文書はあるがJobが受け入れる | 不成立 |
| 識別子をMaskしただけで、Sensitiveな事実が残るDataを学習する | Fail。名称変更や形式変更で対象外にはならない |

再分類・匿名化等でSensitiveでなくなったと主張する場合、その判断根拠と残存リスクを確認する。
これは本Controlが匿名化の正しさまで保証するという意味ではない。

## Threat and failure-mode rationale

攻撃者は推論EndpointへQueryできる者、または低権限でFeedback等にDataを投入できる者とする。
Sensitive学習 → 記憶された情報の抽出、Retrieval → 会話保存 → 再学習という経路を考える。
Sourceを削除しても学習済みArtifactが残ることが、管理可能性を失う主な原因となる。
外部脅威IDのMappingは未確定で、記憶・抽出・再混入という具体的失敗を直接記述する。

## Verification

### Architecture and configuration review

Source分類、Dataset Snapshot、学習Job入力、Artifact由来、Provider設定と契約、
Log/Cache/Feedbackの行先を照合する。検証したService・Account・機能の範囲を明示する。
Provider全体の宣伝文句を、契約している経路の証拠として流用しない。

### Positive verification

模擬Sensitive Recordを外部Sourceへ置き、Retrieval経由で必要な回答が得られることを確認する。
同RecordがDataset選別・学習Jobでは除外され、対応する由来情報を追跡できることを確認する。

### Negative and abuse-case verification

| ID | 試験 | 期待結果 |
|---|---|---|
| N-1 | Sensitive RecordをDataset builderと直接Fine-tuning入口へ投入する | すべての対象学習経路で拒否または除外 |
| N-2 | Training可否・分類・由来を欠落/改ざんする | 判断不能なDataを許可にDefaultしない |
| N-3 | Sensitive会話を高評価Feedbackや評価Corpus経由で再投入する | 学習へ昇格しない |
| N-4 | 模擬固有CanaryをSourceだけに置き、Retrievalと関連Cacheを止める | Canaryが出ないことを確認。出た場合は他の残存経路と学習混入を調査 |
| N-5 | Sourceを更新/削除し、IndexとCacheの定めた反映期間後に再取得する | 古いDataへ依存しないことを確認。残存原因をModelと外部Storeに分ける |

Canaryは偶然出にくい模擬文字列である。不再現は非学習の証明ではなく補助試験。
再現しても直ちにWeight記憶と断定せず、Session、Cache、別Sourceを切り分ける。
N-5の外部Store削除不備は重要だが、それだけでModel学習を実証したことにはならない。

### Failure conditions

Sensitive Dataの学習投入や再混入、Retrieval-firstを名乗りながらModelへ固定する経路は不成立。
Providerの学習利用条件やDataset由来が未確認なら、Passを裏付ける証拠不足として記録する。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 分類・Training-use Policy | Data Owner | Sourceと派生Data | 分類/用途変更時 | Revision管理、実Data非公開 | 対象と判断元が特定できる |
| Dataset/Job/Model由来 | 学習管理者 | Training、Adapter、直接Job | 学習Runごと | Manifest/Artifact識別、秘密除外 | Sensitive入力が学習へ入らない根拠 |
| Provider利用条件 | 契約/Service Owner | 実Account・Endpoint・機能 | 契約/設定変更時 | 証拠は適切な内部保管先へ | 当該Dataが学習に利用されない条件を確認 |
| 経路・回帰試験 | Test Harness/検証者 | N-1〜N-5または同等 | 関連変更時・定期回帰 | 模擬Data、Build/Run記録 | 直接・循環経路で除外、残存原因を識別 |

## Related requirements

- `v1.0-C5.2.2`: Retrieval時の利用者認可。
- `v1.0-C5.2.4`: 推論後の受取権限制御。
- `v1.0-C5.2.7`: 派生物へ分類を伝えること。

## Known limitations and uncertainty

取得元を外部化しても、認可・暗号化・保持・削除・出力制御は自動的に成立しない。
由来不明の事前学習済みModelについて、試験だけでSensitiveな記憶の不存在を証明できない。
例外としてSensitive学習を採る場合、別の対策をもって本要件をPassへ置換しない。
本Artifactは検証可能な基準であり、製品適合やEngineering Mappingを主張しない。

## References

- [AISVS v1.0 C5 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [同RevisionのAISVS Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-02-AI-Resource-Authorization-Classification.md): 補足資料でありNormativeではない。

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-08 | 初版。解釈・適用境界・脅威・検証・証拠期待値を整備 | 固定RevisionのAISVS、Repository interpretation | 本文のSecurity Properties、試験、Evidence expectations。製品試験は未実施 |
