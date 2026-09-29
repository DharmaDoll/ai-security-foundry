---
title: "Context上限を超える入力を切り詰めず拒否する"
versioned_id: "v1.0-C2.1.4"
requirement_id: "C2.1.4"
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

# Context上限を超える入力を切り詰めず拒否する

AISVS Verification Level: 1

学習資料：[C2.1 Prompt Injection Defenses](../../../learning/c02-input-validation/v1.0-c2.1-prompt-injection-defenses.md)

## Upstream basis

AISVS `v1.0-C2.1.4`は、入力長の制御でContentがContext Windowを超えないようにし、
Token上限を超える入力は切り詰めず**拒否**することを求める。
C2.1 Researchは、黙った切詰めで後方の指示や非信頼区分の境界が失われる失敗、
Model固有のToken数え方、SDK既定のTruncationを検証観点として示す。

Researchには長文内のInjection、出力Token上限、指示を文脈の両端に置く案もある。
これらは関連Risk・補助設計であり、C2.1.4の独立した必須条件を「長文攻撃の完全検出」や
「特定のPrompt配置」へ広げない。正規の範囲は固定版の要件本文で判断する。

## Interpretation

Modelへ送る入力のうち、受け入れたUser Message、履歴、取得文書、Tool結果、
System／Developer Message、Tool定義、Template等を実際の呼出し形に組み立てた時点で、
対象Modelの有効なContext上限を超えないよう制御する。上限を超えた入力は、
意味や指示の一部を黙って捨てて送るのではなく、明示的に拒否する。

事前に検索対象や履歴を選ぶ設計は、上限超過後に受け入れ済み入力を切り詰めることと異なる。
どの資料を採用したかが確定した後、その最終入力について上限を再確認する。
利用者に短縮・再選択を依頼することはできるが、ApplicationやProviderが密かに削った
Contentを、元の入力が検査・承認されたかのように扱わない。

## Security objective

Context上限に伴う暗黙の欠落で、指示、引用元、役割境界、非信頼Dataの区切りが失われ、
Modelが開発者や利用者の想定と異なる入力を処理することを防ぐ。
上限内の長文による注意の希薄化やPrompt Injectionそのものは、本Controlだけでは防げない。

## Applicability

Context Windowを持つModelへの入力経路に適用する。Chat、Agent、RAG、Tool利用、
長期履歴の再投入、要約後の再投入、Model切替、Retry、Fallbackを含む。
複数Modelを使う場合、各呼出し先の上限で評価する。

### Non-applicability

Modelへ入力を送らない純粋なStorage処理は直接対象外。ただし後からModelへ渡す時点で対象になる。
「APIが超過時にErrorを返すはず」という推測だけでは対象外にできない。実際の境界で
切詰めず拒否されることを観測できれば、EnforcementがProvider側にあっても評価可能である。

## Scope and assumptions

- Context Windowは対象Modelの入力と、必要に応じた出力予約分を含む利用可能枠として扱う。
  正確な計数単位と予約方法はModel／API仕様に依存し、上流要件自体は具体値を指定しない。
- 単純な文字数はToken数の代替にならない。Model、Tokenizer、Chat Template、Tool定義、
  Media変換の差を考慮する。正確な計数が得られない場合は検証済みの保守的な上限を用いる。
- 長さ判定と実送信の間で入力が変わる場合は再計数する。Streaming、Retry、Fallbackで
  同じ判定結果を無条件に流用しない。
- 入力選択・要約は許されるが、選択済み／承認済みの内容を上限超過後に無通知で削ることは別である。

## Assets, actors, identities, and trust boundaries

保護対象はModelが受け取る完全な入力、System／Developer指示、非信頼Contentの区切り、
利用者が依頼した処理の意味。攻撃者は大きな文書やTool結果を投入し、後半の境界や安全上
重要な情報を欠落させようとする。Application、Retriever、Prompt Builder、Tokenizer、
Model Gateway、SDK、Providerが関係する。

Trust Boundaryは「Applicationが検査・採用した入力」から「Providerが実際に処理する
Context」へ移る地点。決定論的なEnforcement Pointは、最終Payloadを確定する
Prompt Builder／Gateway、または切詰めず拒否することを検証済みのProvider APIである。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 対象Modelと実際の呼出し形式に対して、有効なContext上限と計数方法が定義されている。 |
| SP-2 | 最終的に採用した入力全体を送信前に評価し、上限を超える場合は明示的に拒否する。 |
| SP-3 | Application、SDK、Gateway、Providerのいずれも、超過入力を黙って切り詰めて正常応答として扱わない。 |
| SP-4 | 入力の追加・変換、Model変更、Retry／Fallbackで判定対象が変わるなら、変更後の入力と上限で再評価する。 |

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| RAGが検索段階で上限に収まる文書を選び、最終Payloadも上限内と確認する | 本Controlに適合し得る。採用前の選択は超過後の切詰めではない。 |
| 完成したPromptが超過したため、末尾や古い履歴を無通知で削る | Fail。削った場所が偶然無害でも変わらない。 |
| Providerが超過を明示Errorで拒否し、推論を開始しない | 境界全体で切詰めがないと確認できればPassの根拠になり得る。 |
| 上限内だが長文中のInjectionに従う | 本Controlの直接Failではない。C2.1.3／C2.1.6等で別途評価する。 |
| Toolの反復で総費用が膨らむ | C9.1の実行予算等の別保証。単発Context上限とは異なる。 |

## Threat and failure-mode rationale

攻撃者が大量の低信頼Contentを入力し、SDKの自動TruncationやApplicationの
末尾CutによってSystem指示、区切り、正しい引用元を落とすと、Modelは検査時と
異なるContextを読む。Researchはこれを単なる可用性の問題ではなく、
入力境界の意味が変わるSecurity Failureとして扱う。

外部Threat IDとの厳密なMappingは未評価。Catalogの`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

Model／TokenizerのVersion、Context上限、出力予約、Serialization Overhead、
Tool定義、履歴、RAG、Image／Audioの扱いを確認する。Prompt Builderの計数位置、
SDK／Gateway／ProviderのTruncation設定、Retry・Fallbackの上限を追う。
必要なら送信直前とProviderが処理した入力の対応を合成Dataで観測する。

### Positive verification

上限未満と境界ちょうどの合成入力を正常に処理し、選択した各Message・Tool定義が
期待どおり保持されることを確認する。事前の文書選択では、採用対象と不採用対象を
区別した後、完成入力で再判定する。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果・対応Property |
|---|---|---|
| N-1 | 上限を1 Token超える完成入力を送る | 明示拒否され、短縮版の推論が成功扱いされない。SP-1〜SP-3 |
| N-2 | RAG文書、Tool定義、履歴を後から追加して超過させる | 最終組立て後に再判定し、無通知で末尾を削らない。SP-2〜SP-4 |
| N-3 | System指示や非信頼Contentの終端を末尾に置いて超過させる | 境界が失われたPromptで推論を続けない。SP-3 |
| N-4 | 短いContextのModelへFallback／Retryする | 新Modelの上限で再評価し、超過なら明示拒否する。SP-4 |
| N-5 | 多言語・絵文字・特殊文字で文字数とToken数を乖離させる | 文字数だけに依存せず、検証済み計数方法に従う。SP-1, SP-2 |
| N-6 | SDKの自動Truncation設定を有効にして超過入力を送る | 設定で禁止するか、境界試験で黙ったCutがないと示す。SP-3 |

### Failure conditions

上限超過の入力が正常な短縮版として推論される、Provider側の暗黙のCutを把握していない、
最終組立て後やModel切替後の上限を評価しない場合はFail。上限設定ファイルの存在だけ、
または文字数制限だけではPassの証拠にならない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Model別Limit Contract | Model／Application Owner | Model、Tokenizer、Template、出力予約 | Model／SDK更新時 | Revisionを保持 | 実効上限と計数方法を再現できる。 |
| Prompt組立てData Flow | Application Owner | 履歴、RAG、Tool、Retry／Fallback | Topology変更時 | 実Dataを含めずRevisionを保持 | 最終判定と送信Payloadの対応を追える。 |
| 境界・超過試験 | Test Harness | N-1〜N-6 | Release・Model／SDK変更時 | 合成入力、結果、設定Revisionを保持 | 超過時の明示拒否、非Truncation、正常系維持を示す。 |

## Related requirements

| Requirement | 関係と境界 |
|---|---|
| `v1.0-C2.1.3` | 入力のInjection検査とFlag時遮断。Token上限内でも必要。 |
| `v1.0-C2.1.6` | 指示階層の維持。黙ったCutで境界が消えると実効性を失うが、長さ制御だけで階層は保証しない。 |
| `v1.0-C2.1.8` | Many-shot Jailbreakの検出。上限内の大量例示は長さ制御だけでは防げない。 |
| `v1.0-C9.1.2` | 一回のAgent実行全体の累積予算。単発Context Windowとは別。 |

## Known limitations and uncertainty

Model内部の実Token数やProvider側の前処理が不透明な場合、Applicationの計数と
実処理に差が残る。保守的なMarginと境界テストで差を管理し、未確認のProvider挙動を
適合根拠にしない。上限内のContextでも注意低下やInjectionは起こり得る。

本書の`verifiable`はRepository Artifactの成熟度であり、製品適合や
すべての長文攻撃への耐性を表さない。

## References

- [AISVS v1.0 C2 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md)
- [AISVS v1.0 C2.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md)
- [C2 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-29 | C2.1.4初版。超過拒否と事前選択の境界を整理 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
