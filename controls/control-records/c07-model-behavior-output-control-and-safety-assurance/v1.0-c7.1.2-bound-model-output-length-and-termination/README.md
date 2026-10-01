---
title: "Model出力の長さと終了を制御する"
versioned_id: "v1.0-C7.1.2"
requirement_id: "C7.1.2"
verification_level: 1
family_id: "C7"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-01-Output-Format-Enforcement.md"
last_verified: "2026-09-30"
maturity: "verifiable"
mapping_assessment_refs: []
---

# Model出力の長さと終了を制御する

AISVS Verification Level: 1

学習資料：[C7.1 Output Format Enforcement](../../../learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.1-output-format-enforcement.md)

## Upstream basis

AISVS `v1.0-C7.1.2`は、Model生成出力を長さ制限と終了制御でBoundすることを求める。
対応Researchは、無制限な生成による資源消費と、上限到達・中断で切れた出力を
完成済みとして後続処理へ渡す危険を論じる。Token上限、Stop Sequence、
Providerの終了Reason、Streaming時の中断試験等は実装・検証の候補であり、
Normative本文は特定のAPIや固定数値を指定しない。

## Interpretation

Model呼出しごとに用途に見合う出力上限と終了条件を定め、長い生成が
設定したBoundを越えないことを実際の経路で確認する。Applicationは、
正常完了、設定したStop条件、出力上限への到達、中断・Error等を区別し、
後続が必要とする「完成した出力」かどうかを判断できる必要がある。

Repository interpretationとして、上限で切れたJSON、Tool引数、命令を
完成済みとみなし、欠けた部分を推測して実行することを安全な終了制御とは扱わない。
ただし、本Requirement自体は出力の**長さ・終了**を問う。形式のSchema適合は
C7.1.1、Tool実行の認可や累積Budgetは別の保証である。

Streamingも対象外ではない。断片ごとの受信・公開・利用の境界と、
最終的な終了Reasonが分かる時点を特定する。Streamingという方式だけで
Failとはしないが、出力上限を設定していても、途中の断片を無制限に
転送する、または終了不明の断片を完成済みのActionとして利用するなら
保証は成立しない。

## Security objective

Modelが際限なく出力してLatency・Cost・Memoryを消費する失敗と、
未完了の出力が完成済みのDataや命令として扱われる失敗を減らす。
Token数の制限だけで、下流のTool実行量や回答内容の安全性まで保証しない。

## Applicability

Model出力をUserへ表示、Tool／APIへ渡す、保存する、後続StepのContextへ含める
Applicationに適用する。同期応答、Streaming、Retry、Fallback、複数Providerの
各呼出し経路を対象にする。

### Non-applicability

Model生成出力を取得・利用しない決定論的処理は直接対象外。
短い出力しか期待しない用途であっても、上限と終了を実際に制御しているかは別に確認する。

## Scope and assumptions

- 出力上限は用途、Model、Provider、後続処理の受け入れ範囲に合わせて定義する。
  AISVSは普遍的な最大Token数、Byte数、Stop文字列を指定しない。
- Modelに「短く答えて」と依頼することは、決定論的な上限の代替ではない。
- Providerごとに終了ReasonとStop挙動が異なる場合がある。Applicationが
  実際に使う組合せで、完了・上限・中断を識別できることを確認する。
- 出力Token上限だけでは、短い出力をもとにした大きなQuery、Loop、
  Tool操作等の下流資源消費をBoundできない。そこは別途Budgetを設ける。

## Assets, actors, identities, and trust boundaries

保護対象は推論資源・運用Budget、後続Systemの処理整合性、Userに渡す
応答の完成状態。攻撃者はPromptで長文や反復出力を誘い、または
打切り直前の未完成なTool要求を生じさせ得る。Modelも意図せず途中で止まり得る。
Trust Boundaryは、生成を終了させるProvider／RuntimeからApplicationへ
出力と終了情報が渡り、Applicationがそれを公開・実行・保存する地点。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 利用するModel呼出し経路ごとに、用途に応じた出力長のBoundが設定され、実際の生成を制限する。 |
| SP-2 | 終了条件が設定され、正常完了、設定Stop、上限到達、中断・Errorを区別できる。 |
| SP-3 | 完成が必要な下流処理は、上限到達や中断による断片を完成済みとして扱わない。 |
| SP-4 | Streaming、Retry、Fallback等でも、制限と終了判定が実際に利用する出力へ適用される。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 最大出力Token数を設定したが、上限到達を正常完了と同一視する | 長さのBoundはあっても終了制御・利用判断が不十分。 |
| 出力が上限で切れ、部分的なTool引数を推測補完して実行する | SP-3の失敗。Schema適合・認可も別途確認する。 |
| Providerが正常終了を返し、出力がSchema不一致 | Schema検証はC7.1.1の保証。正常終了だけでは受け入れ不可。 |
| InputがContext Windowを超え、黙って切り詰められる | 入力側のC2.1.4。出力制御の証拠ではない。 |
| 短いModel出力が大規模なTool処理を指示する | 本Controlだけでは防げない。実行Budget・認可はC9等の別保証。 |
| Streamingで断片を表示し、終了後に全体を評価する | 表示の可逆性と断片の利用境界を確認する。Streaming自体をFailとはしない。 |

## Threat and failure-mode rationale

攻撃者が繰り返しや長文を生成させると、上限なしの推論は資源とLatencyを
消費する。また上限や切断による未完了出力は、ParserやToolが完成済みと
誤認すると処理を変え得る。Researchはこの二つを別の失敗として扱う。
外部Threat IDへの厳密なMappingは未評価とし、Catalogには追加しない。

## Verification

### Architecture and configuration review

全Model呼出し経路の出力上限、Stop条件、Provider終了Reason、Applicationでの
判定、Streaming Buffer／公開時点、Retry・Fallbackの再適用を追う。
設定値がProviderへ送られ、Model切替やSDK既定値で無効化されないことを確認する。

### Positive verification

上限内で正常に完成する文章と構造化出力を生成し、終了Reasonが正常完了として
識別され、正当な出力が用途どおり利用されることを確認する。
Stop条件を使う経路では、期待した境界で終了し、本文中の偶然の一致で
必要な内容を失わないかも試す。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 長文・反復の生成を促し、設定した上限に到達させる | 実際の生成がBoundされ、上限到達を正常完了と区別する。SP-1, SP-2 |
| N-2 | Structured OutputやTool引数を途中で打ち切る | 未完成の値を完成済みとして利用せず、推測補完して実行しない。SP-2, SP-3 |
| N-3 | Stop条件が出力本文中やChunk境界に現れる | 想定した終了挙動を再現し、誤った完成判定をしない。SP-2, SP-4 |
| N-4 | StreamingをCancelし、Client切断・Timeout・Provider Errorを起こす | 完了と中断を区別し、未完了のActionを実行しない。SP-2〜SP-4 |
| N-5 | Retry、Fallback、Model／Provider切替を行う | 各新規呼出しにも上限と終了判定が適用され、前回の完了状態を流用しない。SP-1, SP-2, SP-4 |
| N-6 | 短い出力が大量の下流Actionを要求する | 出力Boundの適合と下流Budgetの不足を分けて評価する。SP-1 |

### Failure conditions

利用する出力経路で長さ制限・終了条件がない、Modelへの自然言語指示だけで
長さを制限したと扱う、上限・中断を正常完了と識別できない、または
未完了の出力を完成済みとして実行する場合はFail。
上限設定の存在だけで、実経路での動作確認がない場合もPassとしない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Model呼出し設定一覧 | Application Owner | 経路、Model、Provider、上限、Stop条件 | 経路・Model変更時 | 設定Revisionを保持 | 全利用経路のBoundと終了条件を追える。 |
| 終了Reasonと利用判断の仕様 | Application Owner | 正常、Stop、上限、中断、Error、Streaming | SDK・Provider変更時 | 仕様と実装Versionを保持 | 未完了を完成として扱わない判断を確認できる。 |
| 経路試験結果 | Test Harness | N-1〜N-6、実際のProvider／Fallback | Release・設定変更時 | 合成Promptを使い敏感Dataを含めない | 上限・停止・未完了処理を再現できる。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C7.1.1` | Model出力のSchema適合と不一致拒否。本Controlは長さ・終了状態を扱う。 |
| `v1.0-C2.1.4` | Context Windowを超える入力の拒否。出力上限とは別。 |
| `v1.0-C9.1.1`／`v1.0-C9.1.2` | Tool／Agent実行の資源Budget。出力長制限だけでは下流CostをBoundしない。 |

## Known limitations and uncertainty

Token上限はProviderのToken化や応答Envelopeに依存する。Stop Sequenceは
Data中にも現れ得るし、Modelが上限前に不完全な内容を返すこともある。
そのため終了ReasonだけでSchema適合や業務上の完了を証明できない。
短い出力でも危険な副作用・大きな資源消費を起こし得るため、
下流のBudget、Schema検証、認可を別途維持する。
`verifiable`は本Artifactの成熟度であり、製品適合を示さない。

## References

- [AISVS v1.0 C7 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md)
- [AISVS v1.0 C7.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-01-Output-Format-Enforcement.md)
- [C7 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-30 | C7.1.2初版。出力Boundと終了状態を、Schema適合・下流Budgetから分離 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
