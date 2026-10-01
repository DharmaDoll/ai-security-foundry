---
title: "用途に必要な文字だけを入力で許可する"
versioned_id: "v1.0-C2.1.5"
requirement_id: "C2.1.5"
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

# 用途に必要な文字だけを入力で許可する

AISVS Verification Level: 1

学習資料：[C2.1 Prompt Injection Defenses](../../../learning/c02-input-validation/v1.0-c2.1-prompt-injection-defenses.md)

## Upstream basis

AISVS `v1.0-C2.1.5`は、全入力について文字集合を制限し、**明示的に必要な文字のみ**を許すAllowlist方式を求める。
対応Researchは不可視文字、双方向制御文字、似た字形、Variation Selector等による検査回避を例示する。
また、構造化されたIDと自然言語の自由記述では妥当な文字集合が異なり、多言語入力をASCIIだけに狭めると
正常な利用を壊すと注意する。ResearchのNFKCや特定文字の除去は有用な検討例だが、Normative本文が
特定のUnicode正規化方式や一律の除去を義務付けたものではない。

## Interpretation

Modelへ届き得る各入力経路・Fieldについて、業務上必要な文字を言語、形式、用途に基づいて明示し、
その範囲外の文字が利用内容へ入らないようにする。商品ID等の構造化Fieldには狭い集合を、
日本語等の自然言語Fieldには実際に対応する文字・記号を含む集合を定義する。
「Unicodeならすべて可」や、未定義文字を暗黙に通す既定動作はAllowlistではない。

正規化・変換を採用する場合は、その結果をAllowlistで評価し、検査後の復号や別経路から
許可外文字が現れないことを確認する。用途上必要な不可視文字や結合文字まで機械的に禁止するのではなく、
必要性、処理時の意味、Renderer／Tokenizerとの差を記録して判断する。

## Security objective

不要な文字や表現差を利用して、入力検査・表示・Token化で異なる内容を見せる余地を減らす。
許可済みの文字だけでも悪意ある命令は書けるため、このControlはPrompt Injectionの意味的検出や
完全防止を保証しない。

## Applicability

User Message、Form、検索文書、Tool応答、Memory、MCP Content等、TextとしてModelや
その前処理に入る経路に適用する。Agent自身が生成したSummaryも、再投入されるなら入力である。
利用者が自由記述できる場合も対象外にはならず、その用途に必要な言語・記号を広く、しかし明示的に定義する。

### Non-applicability

画像・音声の生Byteに文字集合制限を直接当てることはできない。OCR、Transcription、Metadata、
Caption等としてText化された出口は対象になる。Binary固有の検査はC2.2.3等で別途扱う。

## Scope and assumptions

- 「全入力」は単一の共通Regexを意味しない。経路・Field・対応言語ごとの明示的なPolicyを意味する。
- 文字の許可は、Code Point、結合Sequence、正規化後のText、実際の表示のどれを評価するかで結果が異なり得る。
  Policyは評価単位と変換順序を示す。
- 不正なEncodingやDecoder Errorは「許可した文字」として黙認しない。安全な拒否または明示的な変換が必要。
- 制限の変更は正当な利用者へ影響するため、対応言語・アクセシビリティ・誤拒否を回帰試験する。

## Assets, actors, identities, and trust boundaries

保護対象は入力検査の有効性、Modelが受け取るTextの一貫性、正常な多言語入力の利用可能性。
攻撃者はUser欄だけでなく、外部文書やTool応答へ不可視・制御・似た字形の文字を入れ得る。
Trust Boundaryは非信頼TextがApplicationの検査境界からPrompt Builder、Tokenizer、Embedding等へ移る地点。
Enforcement Pointは各経路のText取込・変換後の検証と、最終利用前に拒否できる境界である。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | Model利用に至る各Text経路・Fieldに、用途上必要な文字のAllowlistと評価単位が定義されている。 |
| SP-2 | 許可外文字は最終利用前に拒否されるか、許可された明示的変換を経て再評価される。黙った削除で意味を変えない。 |
| SP-3 | 正規化、復号、組立て、Retry等で利用Textが変わる場合も、実際に利用するTextへPolicyが適用される。 |
| SP-4 | 対応を表明する言語・記号・アクセシビリティ上必要なTextは、Policy内で正常に受け付けられる。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| 商品IDが定めた英数字・記号だけを受け付け、不可視文字を拒否する | 該当FieldのPass根拠になり得る。他の経路も確認する。 |
| 日本語の自由記述をASCIIだけに限定する | Allowlistは存在しても、必要な文字を許さないためSP-4を満たさない。 |
| 全Unicode Code Pointを無条件に許可する | 明示的に必要な文字だけを許す制限とは言えず、Fail。 |
| 許可文字のみで書いた悪意ある命令が通る | 本Control単独の直接Failではない。C2.1.3等で意味的な検査を評価する。 |
| 予約特殊Tokenの文字列表現が構造的なMessage境界になる | C2.1.7の別保証。文字のAllowlistだけでは防げない。 |

## Threat and failure-mode rationale

不可視文字や似た字形を混ぜると、人が読む表示、Pattern検査、Tokenizerの解釈がずれる場合がある。
未定義文字を許した経路が残ると、別経路で検査したときと異なるTextをModelへ渡し得る。
一方で過度な制限は正常な言語・記号を壊し、回避的な入力方法を誘発する。
外部Threat IDとの厳密なMappingは未評価とし、Catalogの`threat_mappings`は空にする。

## Verification

### Architecture and configuration review

Modelへ至るText経路を列挙し、Field別Allowlist、対応言語、正規化・復号の順序、
判定位置、拒否時の挙動を確認する。Application、Retriever、Tool Adapter、Prompt Builder、
Retry／Fallbackのどこかで検査後にTextが変わるかを追う。Regexや設定の存在だけでなく、
最終利用を止められるかを確認する。

### Positive verification

各Fieldに必要なASCII、日本語等の対応言語、結合文字、Emoji、改行等を用途に応じて試し、
宣言したPolicyと一致して通ることを観測する。許可しない記号を必要な業務と誤認していないかも確認する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 商品IDへゼロ幅文字や双方向制御文字を混ぜる | Policy外として拒否され、Modelへ渡らない。SP-1, SP-2 |
| N-2 | RAG文書とTool応答へ、同じ許可外文字を置く | User欄以外も同じ方針で評価し、未検査経路を作らない。SP-1〜SP-3 |
| N-3 | 検査後にHTML Entity、Unicode Escape等を復号して許可外文字を出す | 復号後に再評価し、元のPassを流用しない。SP-2, SP-3 |
| N-4 | 許可外文字を黙って削ると意味が変わる入力を与える | 改変を成功入力として扱わず、明示的に拒否または合意済み変換を適用する。SP-2 |
| N-5 | 対応言語の通常文、必要な結合文字や改行を与える | 不当に拒否されず、宣言した対応範囲を維持する。SP-4 |
| N-6 | Retry／Fallbackで別の変換器を使う | 実際の利用Textを再評価し、経路変更で許可外文字を通さない。SP-3 |

### Failure conditions

対象となるText経路にPolicyがない、必要性を示せない文字を無条件で許す、
許可外文字が変換後にModelへ入る、または宣言した対応言語をPolicyが壊す場合はFail。
文字集合を定義しただけで適用経路と正常系が示せない場合もPassとはしない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Field別文字Policy | Application／Data Owner | 入力経路、Field、対応言語、変換順序 | 用途・言語追加時 | Revisionと承認理由を保持 | 必要な文字と不要な文字の境界が説明できる。 |
| Text FlowとEnforcement配置 | Application Owner | 取込からModel利用、Retry／Fallback | Topology変更時 | 機密Dataを含めずVersion保持 | 全対象経路に判定・拒否点がある。 |
| 正常系・Negative Test結果 | Test Harness | N-1〜N-6、対応言語 | Release・変換器変更時 | 合成入力、Policy Revisionを保持 | 許可外文字の拒否と必要文字の受入れを再現できる。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C2.1.1` | 正規化の時点を扱う。正規化後に何を許すかは本Controlで確認する。 |
| `v1.0-C2.1.2` | Encoding／表現Smugglingの検出・緩和。許可文字だけで構成したEncoded Payloadもあり得る。 |
| `v1.0-C2.1.3` | 指示誘導の検査と検知時遮断。文字集合は意味的な悪意を判定しない。 |
| `v1.0-C2.1.7` | 予約特殊TokenをLiteralとして扱う構造上の保証。 |

## Known limitations and uncertainty

Normativeの「all inputs」と「explicitly required」の粒度は具体化されていない。
本書はTextとして利用されるField別の必要性を判断単位とするが、自由記述の許可範囲には
Product Ownerの明示判断が要る。Code Point単位のAllowlistでも、見た目や意味の一致は保証できない。
Researchにある一律NFKCや除去は、言語や文字の意味を変える場合があるため、そのまま必須化しない。

`verifiable`はRepository Artifactの成熟度であり、実製品の適合やInjection防止を示さない。

## References

- [AISVS v1.0 C2 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md)
- [AISVS v1.0 C2.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md)
- [C2 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-29 | C2.1.5初版。Field別Allowlistと多言語入力の境界を整理 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
