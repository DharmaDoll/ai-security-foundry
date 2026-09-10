---
title: "Downstream Classification Label Propagation"
versioned_id: "v1.0-C5.2.7"
requirement_id: "C5.2.7"
verification_level: 3
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

# 派生Resourceへの分類ラベルの伝播

AISVS Verification Level: 3

初めて読む方へ：[具体例・用語・対話を含む学習ノート](learning.md)。

## Upstream basis

AISVS `v1.0-C5.2.7`、Verification Level 3を解釈する。原文は、分類ラベルが
Embedding、Prompt Cache、Model Output等の下流Resourceへ伝わることを求める。
特定のLabel名、Metadata形式、製品は指定しない。

固定RevisionのC5.2 Research（Last Researched: 2026-07-14）の該当行を確認した。
Researchは加工経路でのLabel欠落、派生物の追跡、元Label変更後の同期遅延を補足する。
Tenant、目的、保持期間等も例示するが、すべてを本要件の必須Fieldへ昇格させない。
以下の結合・再分類・間接参照・Freshnessの条件はRepository interpretationとして示す。

## Interpretation

**Dataの形が変わっても、そのDataに付いた分類の意味と対象との結び付きを失わない。**

Restricted（閲覧・取扱いを制限する分類）の人事文書をChunkへ分割し、Vector化する例では、
文書だけでなくChunk、Embedding、Cache、要約にも分類を結び付ける。
数値Vectorや新しい文章になったことを理由に、自動的に公開扱いにはしない。
分類は、誰が受け取ってよいかを判断する材料であり、それ自体がアクセスを拒否する機構ではない。

## Security objective

派生物の無分類化や無断の格下げによって、下流の処理が必要な保護を選べなくなることを防ぐ。
分類を使う認可・保存・二次利用の判断に、意味のある情報を渡し続ける。

## Applicability

分類対象Dataを取り込み、分割、変換、結合、生成、複製または保存するAI Pipelineに適用する。
Embedding、Cache、Model Outputに加え、対象Dataを含むExport、評価用Copy、Backup等も追う。
単なる性能カウンタ等、分類対象Dataを含まない情報にまで同じLabelを機械的に要求しない。

### Non-applicability

分類対象Dataもその派生物も扱わない範囲では、根拠と前提を記録してN/Aを判断する。
公開CorpusだけでなくUser入力、Tool結果、Session、Cache、Outputまで確認する。
正式なPublic Labelがあるなら、その伝播を検証する扱いも自然である。
Internet上で取得できることを、組織が公開を認めたことと同一視しない。

## Scope and assumptions

- Label体系と権威ある分類元を定める。AISVSはPublic/Internal等の階層を規定しない。
- Classificationは情報の保護区分、Lineageは由来、Tenantは所属、Retentionは保持条件であり別概念である。
- Labelを直接保存する方式と、明示的な分類Bindingを介して解決する方式を認める。
  後者では意味、解決先、有効条件、全Consumerでの解決、解決失敗時の扱いを検証する。
- 単なる由来IDだけでは分類の伝播を示さない。一方、Field名が `source_id` か
  `classification_ref` かだけで合否を決めない。保証はその参照の契約と実動作で判断する。
- 元分類の変更への追随範囲と最大遅延を定める。原文に一律の更新時間はない。
  既に外部へ渡したCopyを遡って更新できると仮定せず、管理できる範囲と残る依存を明示する。

## Assets, actors, identities, and trust boundaries

保護対象は派生Data、Label、DataとLabelの対応関係である。
ActorsはData Owner、取込処理、変換処理、Model、Store、下流Consumer、分類管理者。
信頼境界は外部Dataから取込、変換から保存、保存から下流利用、再分類要求から分類管理である。
Modelが生成した `Public` という文字列は、分類管理者による許可ではない。

## Required security properties

| ID | 必要な性質 | 成立条件 |
|---|---|---|
| SP-1 | 分類との結び付け | 各対象派生物の分類を、元Dataまたは承認された再分類へ追跡できる |
| SP-2 | 変換・結合で意味を保持 | 複数Sourceの必要な分類条件を、単純な上書き等で失わない |
| SP-3 | 無断の格下げ防止 | Model/Callerの自己申告でLabelや参照先を弱い分類へ変更できない |
| SP-4 | 欠落・変更の管理 | 必要なLabelの欠落や解決失敗をPublicとせず、定めた更新条件で再同期または無効化する |

ここでのEnforcementは、取込・変換・保存・ExportのGateが分類Bindingを確認し、
欠落した派生物の通常公開を拒否することである。隔離領域に保存する場合も、無分類のまま
通常Consumerへ渡さない。Labelに基づく利用者認可の強制は隣接Controlとして別に検証する。

## Scope calibration and adjacent assurance

| 状況 | 評価 |
|---|---|
| Restricted文書のEmbeddingがLabelも有効な分類Bindingも失う | Fail |
| Labelは正しく伝わるがAPIが無視して全員へ返す | 本ControlはPassし得る。認可は別途Fail |
| 公開と非公開の情報を結合し、公開のLabelだけを残す | Fail |
| 承認された再分類手順に従い、由来と変更根拠を残して新Labelを付ける | Pass候補。匿名化等の手順自体の有効性は追加評価 |
| 元分類が誤っているが、派生物へ忠実に伝わる | 伝播とは別の分類判断の問題 |
| Labelや参照の改ざんで、派生物が別の低い分類を指す | Fail。伝播の意味を保つための整合性が破れた |

結合の規則は組織Policyに従う。独立した分類軸を一つの最大値へ潰さず、
必要な条件を保持する。矛盾する条件は隔離や判断待ちとし、Modelに解決を任せない。
再分類は同じLabelを永久にコピーし続けることの例外として、AuthorityとRuleを明示する。

## Threat and failure-mode rationale

攻撃者は外部文書やModel出力を操作できる者、または低権限のData Producerとする。
悪意だけでなく、Chunking、Cache、Export実装がMetadataを落とす事故も対象とする。
悪用経路は、Restricted Source → Labelを失った派生物 → 低い保護を選ぶConsumerである。
Impactは未認可開示や不適切な二次利用だが、その成立にはConsumer側の挙動も関与する。
本改訂では外部脅威IDの有用なMappingを確定していないため、具体的な経路を直接記述する。

## Verification

### Architecture and configuration review

Sourceからすべての派生物へのData flow、分類元、結合規則、格下げ権限、保存時の検査を追う。
間接参照方式ではExport先を含むConsumerが同じ意味で解決できることを確認する。
Labelの更新Event、失敗時の再試行、古いCache/Backupの復元経路を列挙する。

### Positive verification

PublicとRestrictedの模擬文書を分割・Vector化・Cache・要約・Exportし、各派生物を追跡する。
単独Source、混合Source、承認済み再分類について、意図したLabelがConsumerで解釈できることを確認する。

### Negative and abuse-case verification

| ID | 試験 | 期待結果 |
|---|---|---|
| N-1 | ChunkやEmbeddingのLabel/Bindingを削除する | 通常Pipelineへの公開を拒否または隔離し、PublicにDefaultしない |
| N-2 | 参照先、Label、Versionを低権限Callerから変更する | 無断変更を拒否または検出して利用を止める |
| N-3 | PublicとRestrictedを結合し、ModelにPublicと申告させる | 信頼する結合規則が働き、自己申告で格下げしない |
| N-4 | 分類解決先を停止・不整合にする | 有効な分類を得られない派生物を通常の無分類Resourceとして公開しない |
| N-5 | 元Labelを強め、古いCacheやBackupを復元する | 定めた条件内で同期・無効化され、古い低分類が無期限に復活しない |
| N-6 | Export、評価用Copy、Output保存でMetadataを除去する | 全対象経路で分類Bindingを保持するか、未対応の経路を止める |

DataとLabelを同時に追う。Fieldが非NullかというSchema試験だけで完了しない。
認可成功/拒否の試験は伝播試験と分けて結果を報告する。

### Failure conditions

SP-1〜SP-4を破る欠落、意味の喪失、無断変更、定めた有効条件を超える古い分類は不成立。
経路や分類契約が未確認ならPassの証拠不足であり、直ちに情報漏えいの実証とはしない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 分類Policyと変換規則 | Data Owner/分類管理者 | 元分類、結合、再分類 | Policy変更時 | Revision管理、機密分類内容は公開しない | Labelの意味と変更Authorityが特定できる |
| 派生物の追跡結果 | Pipelineと検証者 | Chunk/Embedding/Cache/Output/二次Copy | Pipeline変更時 | 模擬Data、SourceとBuildを対応付ける | すべての対象派生物で有効なBindingを解釈できる |
| 改ざん・欠落試験 | Test Harness | N-1〜N-6または同等試験 | 関連変更時と定期回帰時 | 入力・結果・構成を記録 | 欠落や自己申告による格下げを通さない |
| 更新・復元結果 | 運用/分類管理者 | Cache、Index、管理下Copy | 同期・復元方式変更時 | 時刻とVersionを保持 | 最大遅延と復元後の分類が定義どおり |

本番Evidenceや顧客DataはRepositoryへ保存しない。

## Related requirements

- `v1.0-C5.2.1`: Resourceのアクセス制御。Labelの有無とは別。
- `v1.0-C5.2.2`: 検索・組立での利用者認可。分類はその入力になり得る。
- `v1.0-C5.2.3`: Sensitive DataのModelへの固定回避。LabelだけでTrainingを止められない。
- `v1.0-C5.2.4`: 出力の受取権限。Labelだけで自由文の全内容を保証しない。

## Known limitations and uncertainty

原文は参照形式、再分類方式、全分類軸の結合算法を規定しない。本書の条件は実務上の解釈である。
初期分類の正しさ、匿名化の有効性、認可、暗号化、保持・削除の実行は別途評価する。
ただし伝播中のLabel/Bindingの整合性は本Controlの成立に必要であり、完全に対象外にはしない。
既存学習ノートの「Source IDならFail」は、分類契約を持たない汎用IDの例として読む。
名前を変えるだけで保証が増えるわけではない。

Engineering Mappingは未評価。`verifiable`はArtifactの成熟であり、製品適合や学習進捗ではない。

## References

- [AISVS v1.0 C5 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [同RevisionのAISVS Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-02-AI-Resource-Authorization-Classification.md): 補足資料でありNormativeではない。

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-08 | 初版。解釈・適用境界・脅威・検証・証拠期待値を整備 | 固定RevisionのAISVS、Repository interpretation | 本文のSecurity Properties、試験、Evidence expectations。製品試験は未実施 |
