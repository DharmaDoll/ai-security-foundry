---
title: "モデル変更の監査記録を後から書き換えられないようにする"
versioned_id: "v1.0-C12.5.3"
requirement_id: "C12.5.3"
verification_level: 2
family_id: "C12"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-05-Training-Data-Model-Lifecycle-Audit.md"
last_verified: "2026-10-04"
maturity: "verifiable"
mapping_assessment_refs: []
---

# モデル変更の監査記録を後から書き換えられないようにする

AISVS Verification Level: 2

学習資料：[C12.5 AIの材料と変更履歴](../../../learning/c12-monitoring-logging-and-anomaly-detection/v1.0-c12.5-training-data-and-model-lifecycle-audit.md)

## Upstream basis

AISVS `v1.0-C12.5.3`は、すべてのModel変更について、変更不能な監査記録を
生成することを求める。対応するAISVS Researchは、Model Registryの登録・
配備・Alias切替・廃止に加え、推論設定などRegistry外で起きる変更が記録から
抜けやすいと指摘する。変更者、時刻、対象ArtifactのDigest、変更内容を
結び付け、Registryの通常の編集権限とは別の監査境界で守る方法を提案する。

正規要件は特定のWORM製品、Cloudサービス、署名方式、保持年数やField名を
指定していない。Researchの実装例や他の規制の保持要件を、ここで一律の
適合条件へ変えない。

## Interpretation

評価対象のModelについて、何を「Model変更」とするかを先に定義する。
Model Artifactの作成・差替え、配備・Rollback・廃止、実際に使うVersionや
Aliasの切替など、Modelの状態または利用対象を変える操作が中心となる。
推論Parameters、System Prompt、Guardrail設定なども、評価対象のModelの
振る舞いを決める管理対象として扱う場合は変更経路に含める。単なる個々の
利用者Promptまで無条件に「Model変更」とはしない。

変更が行われるたびに、過去の記録を後から上書き・削除できない監査記録を
作る。例えば、配備先がModel AからBへ切り替わったら、「現在はB」という
画面だけでなく、AからBへの変更、対象の識別、時刻、信頼できる操作元を
辿れるようにする。誤記を直す場合も元記録を消さず、訂正を別の記録として
残す。署名やHashで改ざんを後から見つけられるだけの方式は、過去記録の
変更・削除を防ぐ仕組みと同じではない。

## Security objective

不審なModelの投入や、設定・配備先の無断変更が疑われた際、どの状態が
いつ誰によって変更されたかを再構成し、影響範囲を調べられるようにする。
Model変更者が同じ権限で証拠も消せる状態を避ける。ただし監査記録は
変更を防止するものでも、配備されたModelの安全性を証明するものでもない。

## Applicability

Model Artifact、Version、配備先、参照先、またはModelの動作を決める
管理設定を変更できる開発・運用環境に適用する。変更者が人、CI/CD、
自動Rollback、Providerのいずれでも、評価範囲内の実効的な変更経路を
確認する。外部Model APIを使う場合も、利用するModel IDやRoutingの
変更は利用側の評価対象になり得る。Provider内部の変更は責任境界と
入手できる証拠を分けて扱う。

### Non-applicability

評価範囲内にModel状態や利用対象を変更する経路が実際になく、対象の
責任主体も別である場合は、その範囲を明記して対象外とできる。
「自社では学習しない」「Registryを使わない」だけでは、Version・配備・
Routing・管理設定の変更が存在しないとは言えない。

## Scope and assumptions

- 変更対象をArtifact、Version、Alias、配備、Rollback、管理設定などに分け、
  本番の振る舞いへ効く経路を一覧にする。対象外とする設定は理由を残す。
- 監査記録の不変性は、定めた保持期間において、評価する変更者・管理者が
  過去の記録を編集・削除できないこととして確認する。保持期間の長さは
  本要件だけからは決まらない。
- `latest`などの可変名だけを記録しても、変更前後の実体を識別できない。
  Digestや変更不能なVersionなど、後から対象を特定できる方法を確認する。
- 監査記録の作成と保管の双方を評価する。管理画面の表示、Registryの
  現在値、同じDatabase内の編集可能な履歴だけで不変性を推定しない。
- 記録の完全性と不変性を分けて検証する。保護されたStoreに一部の変更だけ
  残っても「すべての変更を記録した」とは言えない。

## Assets, actors, identities, and trust boundaries

守る対象はModelの変更履歴、配備された実体との対応、事故調査の証拠である。
開発者、Model管理者、配備Pipeline、運用者、Provider、監査担当者が関わる。
侵害された管理者やPipelineが悪意あるModelを投入し、同じ権限で履歴を
消す可能性がある。

主な境界は、変更要求からRegistry・配備Controllerへ、変更の確定から
監査記録の生成へ、通常のModel管理権限から保護された監査保管先へ進む
ところである。Registry自身が侵害された場合、そのRegistryだけが編集
できる履歴を独立した証拠として扱えない。

## Required security properties

| ID | 必要な性質と確かめ方 |
|---|---|
| SP-1 | 定義したModel変更の全経路で、実効的な変更ごとに監査記録が生成される。 |
| SP-2 | 記録から変更対象、変更前後の状態、時期、信頼できる操作元を辿り、実際に利用されたModelや設定と結び付けられる。 |
| SP-3 | Model変更者や通常のRegistry管理者が、保持対象の過去記録を上書き・削除できない。訂正は元記録を残して追加する。 |
| SP-4 | 記録経路の欠落や障害があっても、その変更を記録済みと誤認せず、確認不能な範囲を特定できる。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| Model AからBへの変更が保護された記録に残り、実体と対応し、過去記録を編集・削除できない | Pass候補。別の変更経路も調べる。 |
| Registryの履歴はあるが、Model管理者が同じ権限で削除できる | Fail。不変な監査記録ではない。 |
| 署名付きの記録を同じ管理者が削除でき、欠落を防ぐ仕組みもない | Fail。署名があっても記録の存在と保持を保証できない。 |
| Artifactは変えていないが、Aliasや配備先を別Modelへ切り替えた | 評価範囲のModel変更。記録がなければFail。 |
| 記録は不変だが、推論設定の変更経路だけ監査から漏れる | その設定が管理対象のModel変更ならFail。境界を明示して評価する。 |
| 変更記録はあるが、Modelの署名検証や配備承認に不備がある | 本Controlの記録だけでは補えない。C3・C6等で別に評価する。 |
| 推論EventにModel IDが残るが、変更履歴はない | C12.1の実行時記録ではModel変更の監査記録を代替できない。 |

## Threat and failure-mode rationale

攻撃者がModelのVersionやAliasを切り替えた後、変更履歴も消せれば、
「どのModelがいつ使われたか」という調査の起点を失う。Researchは、
Registry侵害時には同じRegistryの履歴も信頼できないこと、設定変更が
Registry外で起きることを指摘する。本書はその失敗経路を検証対象にする。
外部の脅威IDとの厳密なMappingはまだ評価していない。

## Verification

### Architecture and configuration review

Registry、Pipeline、配備Controller、管理API、Provider設定で実際に変更
できる対象と権限を洗い出す。各変更の確定点から監査記録の生成・保管まで
辿り、誰が記録を編集・削除・保持設定変更できるか確認する。可変Aliasと
実体の対応、監査記録の保存期間、障害時の欠落検知も確認する。方式が
WORMか別の実装かではなく、過去記録を変えられない性質を検証する。

### Positive verification

合成したModel AとBで、新規登録、Alias切替、配備、Rollback、廃止を
模擬する。対象Scopeに含む推論設定も変更する。各操作について、操作元、
時刻、変更前後の状態、対象実体を記録から再構成できることを確認する。
訂正が必要なら、新しい記録を足しても元の記録は残ることを確かめる。

### Negative and abuse-case verification

| ID | 試すこと | 期待する確認結果 |
|---|---|---|
| N-1 | Registry管理者として過去の変更記録を編集・削除する | 保持対象の記録は変更・削除できず、元の内容を確認できる。SP-3。 |
| N-2 | Registry以外の管理APIや自動Rollbackから実効Modelを切り替える | 画面経由と同様に変更記録が残る。SP-1、SP-2。 |
| N-3 | 可変Alias `latest`の参照先をAからBへ変える | Alias名だけでなく、変更前後の実体を辿れる。SP-1、SP-2。 |
| N-4 | Model本体を変えず、対象Scopeの推論設定だけを変更する | 設定変更と適用対象が監査記録に残る。SP-1、SP-2。 |
| N-5 | 記録配送先を一時的に使えなくして変更を試みる | 変更と記録の対応が確認できないなら欠落を検出し、記録済みと扱わない。SP-1、SP-4。 |
| N-6 | 誤記の訂正を試みる | 元記録を上書きせず、訂正記録とのつながりを確認できる。SP-3。 |

### Failure conditions

対象の変更が監査に残らない、可変名しかなく変更した実体を特定できない、
または通常のModel変更権限で保持対象の過去記録を書換え・削除できる場合は
Fail。記録の改ざんを後で検出できるだけで過去記録の削除を許す場合も、
不変な記録としては不足する。Provider内部など証拠を確認できない範囲は、
根拠のないPassにせず、責任境界と未確認事項を残す。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 確認する時期 | 保護上の注意 | 合格の目安 |
|---|---|---|---|---|---|
| 変更経路と権限の一覧 | Model管理・配備担当者 | Artifact、Alias、配備、設定、Provider境界 | 経路追加・権限変更時 | 実Credentialを含めない | 実効的な変更経路と記録生成点が対応する。 |
| 合成した変更記録 | Registry・配備・監査基盤 | 新規登録、切替、Rollback、設定変更、訂正 | Release時・記録方式変更時 | 合成IDと非機密Modelを使用 | 変更前後の対象、時刻、操作元と実体を再構成できる。 |
| 不変性の試験結果 | 独立した試験担当者 | N-1、N-5、N-6と保持設定 | 権限・保管方式変更時 | 監査管理権限を限定 | 過去記録の編集・削除が防がれ、欠落を把握できる。 |

## Related requirements

| Requirement | 関係と違い |
|---|---|
| `v1.0-C12.5.1` | Datasetと加工の来歴。Modelの変更監査とは対象が異なる。 |
| `v1.0-C12.5.2` | ラベル付け活動のLog。同Sectionでも変更不能性を明示するのは本要件。 |
| `v1.0-C12.5.4` | 取込文書の書込み時Tag。Model変更の監査とは別の来歴。 |
| C3・C6 | Modelの承認、検証、Artifact Integrity等。変更の記録だけで安全な配備を保証しない。 |
| `v1.0-C12.1.3` | 推論EventのModel識別。実行時の記録と変更監査は相互に照合できるが、代替しない。 |

## Known limitations and uncertainty

不変な監査記録でも、記録生成前に変更が隠されると完全性は保証できない。
本番での実体と監査記録の結合、保管権限、保持期間、Providerの協力に
依存する。絶対的に誰にも削除できないという主張ではなく、定めた期間と
脅威モデルで記録を守る。推論設定やSystem PromptをどこまでModel変更に
含めるかは製品の管理境界で明示する。`verifiable`は本書の成熟度であり、
実製品の適合結果ではない。

## References

- [AISVS v1.0 C12 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md)
- [AISVS v1.0 C12.5 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C12-Monitoring-and-Logging/C12-05-Training-Data-Model-Lifecycle-Audit.md)
- [C12 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-04 | 初版。Model変更の範囲、記録の完全性と不変性、隣接保証を分けた | AISVS固定版と本Repositoryの解釈 | 本書の必要な性質・試験・証拠。実製品での試験は未実施 |
