---
title: 本番投入時とモデル読込み時に署名を検証する
versioned_id: v1.0-C3.1.3
requirement_id: C3.1.3
verification_level: 2
family_id: C3
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-01-Model-Authorization-Integrity.md
last_verified: '2026-10-18'
maturity: verifiable
mapping_assessment_refs: []
---

# 本番投入時とモデル読込み時に署名を検証する

AISVS Verification Level: 2

[C3.1 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.1-model-authorization-and-integrity.md)

## Upstream basis

AISVS `v1.0-C3.1.3`は、本番への投入を許可する時点と、Modelの読込み時点の両方で暗号署名を検証する。
Researchは、Admissionの検証だけでは後から差し替わるArtifactや直接SDKからの読込みを保護できないこと、検証器の失敗結果を無視していないかNegative Testで確認することを重視する。ScannerやRuntime更新は有益な補強だが署名検証そのものの代替ではない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

本番投入を決める経路と、実際にModelを読む経路に検証点を置く。それぞれで実際に消費する内容と署名、許可した署名者を照合する。未署名・不一致・検証不能なら本番投入や読込みへ進ませない。可変URLを一度検証して別時点に再取得するだけでは、使用対象との一致を示せない。

## Security objective

投入後の差替えや検証を迂回する再起動・Fallbackから、未検証のModel一式が本番へ入ることを防ぐ。

## Applicability

Modelを本番へ導入する全経路と、起動・再起動・再取得・Cache・Fallback等で実際に読む経路を対象とする。API提供型ではProvider側のAdmissionとLoaderの責任分界・検証証拠を確認する。

### Non-applicability

対象境界でModel Artifactを管理・配備しない場合は責任分界を明示する。
外部Providerで内部が見えないことは、Provider側で要件が存在しない理由にはならない。
利用者が確認できない範囲は証拠不足として残し、対象外やPassへ読み替えない。

## Scope and assumptions

対象Deployment、Model一式、版、Provider、Registryと実際の読込み経路を評価開始時に特定する。
名前やAliasが可変なら実体の識別方法を明示する。試験は隔離環境の無害な模擬Artifactで行い、
本番Dataや実行可能な不正Payloadを持ち込まない。証拠の対象版と現在の配備が一致するか確認する。

## Assets, actors, identities, and trust boundaries

開発・外部保管から本番投入へ入る境界と、Artifact StoreからServing Processが内容を読む境界。資産はModel実体、署名と信頼Policy、検証結果。配備Controller、Loader、署名者、Store管理者が関わる。攻撃者による投入後の置換、既存Cacheの書換え、例外時の検証省略を想定する。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 本番投入を許可する前に対象Artifact一式の署名・内容・署名者の信頼条件を検証する。 |
| SP-2 | 実際の読込み時にも対象一式を検証し、再取得や再起動経路を未検証のまま通さない。 |
| SP-3 | 署名不一致・未署名・検証器エラーは投入／読込みを拒否する。検証結果を無視せず、検証した内容と消費する内容を同じものに保つ。 |

## Scope calibration and adjacent assurance

C3.1.2は全Artifactへ署名すること。存在する署名を実経路で検証し拒否へ結び付けるのが本Control。C3.2は署名されたModelの振る舞いを評価する。

## Threat and failure-mode rationale

Admissionを通過した後に可変保存先が置き換わると、一度の成功結果を信じるLoaderは不正な内容を使用する。検証関数が失敗していても戻り値を無視すれば同じ失敗が起きる。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

AdmissionとLoaderの呼出し箇所を別々に追う。検証Policy、対象Scope、戻り値・例外処理、Cacheの扱い、検証後から使用までの書込み権限を確認する。検証用Identityと実配備Identityで結果が違わないか点検する。

### Positive verification

権限ある主体が署名した模擬Model一式を本番相当環境へ投入し、投入時と読込み時のそれぞれの検証結果を観測する。再起動やCache経由でも同じ内容を検証して読めることを示す。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 署名のないModelや一Fileを改変した一式を投入する | Admissionで拒否し、本番配備へ進まない。SP-1、SP-3。 |
| N-2 | Admission後に保存先の設定・重みを差し替えて再起動する | 読込み時に不一致を検出し、差替えた内容を使用しない。SP-2、SP-3。 |
| N-3 | 検証器を失敗・Timeoutさせる、または無効な署名を返す | 戻り値や例外を無視せず拒否する。未検証Fallbackで継続しない。SP-3。 |
| N-4 | 検証成功後にFileを変更する経路を試す | 検証した内容と実消費の不一致を防ぐか、未達として検出する。SP-3。 |

### Failure conditions

投入時または読込み時の片方がない、検証結果を無視する、失敗時に許可する、検証したものと異なる内容を読む場合はFail。検証Logが出るだけでは拒否の実効性を示せない。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| Admission／Loaderの設定と実行記録 | 配備基盤とServing担当者 | 両検証点と全読込み経路 | 配備・起動時と検証実装変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 両方で実対象を検証したことを追える |
| 未署名・改変・障害の拒否試験 | 検証担当者 | 本番相当の配備・再起動・Cache経路 | 初回とLoader・Policy変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 拒否後に読込み・配備が進まないことを観測する |

## Related requirements

[C3.1.2](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.1.2-authorized-signatures-for-all-model-artifacts/README.md)は全Artifactへ署名すること。存在する署名を実経路で検証し拒否へ結び付けるのが本Control。C3.2は署名されたModelの振る舞いを評価する。
[C3 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

侵害された署名者による正当な署名やLoader自身の侵害は残る。全署名検証が通っても、ModelやRuntimeの脆弱性・危険な振る舞いが消えるわけではない。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C3 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [AISVS v1.0 C3.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-01-Model-Authorization-Integrity.md)
- [C3.1 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.1-model-authorization-and-integrity.md)
- [C3 Family概要](../README.md)

- [関連Insight：検査するのは入口の文字列ではなく、実際に利用される内容である](../../../../docs/insights/validation-must-cover-effective-payload.md)（Repositoryの横断的な考察。規範やMappingではない）

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
