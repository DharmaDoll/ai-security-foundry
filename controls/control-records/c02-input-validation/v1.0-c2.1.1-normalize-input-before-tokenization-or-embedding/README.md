---
title: "Token化・Embedding前に入力を正規化する"
versioned_id: "v1.0-C2.1.1"
requirement_id: "C2.1.1"
verification_level: 1
family_id: "C2"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md"
last_verified: "2026-09-28"
maturity: "verifiable"
mapping_assessment_refs: []
---

# Token化・Embedding前に入力を正規化する

AISVS Verification Level: 1

学習資料：[C2.1 Prompt Injection Defenses](../../../docs/learning/c02-input-validation/v1.0-c2.1-prompt-injection-defenses.md)

## Upstream basis

AISVS `v1.0-C2.1.1`は、入力の正規化をToken化またはEmbeddingより**前**に適用することを求める。
[固定版の要件本文](#references)が正規の範囲である。C2.1 ResearchはUnicodeの表記差、不可視文字、
双方向制御文字、正規化と検査の順序などを検討材料として示す。Researchの全対策例や特定の
Unicode方式をこの要件の一律必須条件へ引き上げない。

## Interpretation

対象となる各入力経路で、実際にToken化・Embeddingへ渡す表現へ至る変換を定義し、
選択した正規化をそれらの処理より前に適用する。正規化済み入力から作られた派生物だけが、
その正規化の保証を引き継げる。後続で文字列表現や抽出結果が変わる場合は、元の正規化済みという
事実だけで新しい内容まで保証しない。

これは「NFKCを必ず使う」「似た文字をすべて削る」という要求ではない。用途・対応言語・
Renderer／Tokenizerの差を踏まえた正規化Policyを定め、同じ処理経路で実際に適用したことが必要である。

## Security objective

表記差や不可視の表現差が、前処理の想定とModel／Embeddingが利用する内容の間にずれを作るのを抑える。
正規化だけでInjectionを検出・無害化したと主張しない。

## Applicability

外部・内部を問わず、TextがModelのToken化またはEmbeddingへ進む経路に適用する。
User入力、取得文書、Tool出力、Memory、OCR／音声文字起こし、Prompt組立ての各経路を調べる。
内部System文面も処理順序の確認対象だが、攻撃者による編集可能性は経路ごとに異なる。

### Non-applicability

Token化もEmbeddingも行わない純粋なBinary保存経路は、この要件の直接対象ではない。
後から抽出TextをModelへ送る場合、その抽出出口から適用対象になる。入力が「社内由来」だけでは対象外にしない。

## Scope and assumptions

- 正規化とは、定義した表現等価性に従い入力をCanonicalな形へ変換することを指す。
- 具体方式はデータの意味、言語、Parser、Tokenizerで変わる。NFC／NFKC、制御文字の扱いなどは選択理由を残す。
- 正規化が意味を変えることもあるため、元Textの監査目的での保持と、Modelへ渡すTextを区別する。
- 「Token化またはEmbeddingより前」は上流の明示条件。検査器より前の順序はC2.1.1の原文だけでは一律に要求されない。
  ただし検査対象と利用対象の同一性を示すには、検査前後の変換を追跡する必要がある。
- Model Provider内部の前処理が不透明な場合、Applicationが制御できる最後の境界まで確認し、
  不明部分を適合の証拠として推測しない。

## Assets, actors, identities, and trust boundaries

保護対象はModelに与える指示・資料の解釈、および検索用Embeddingに入るTextの完全性。
攻撃者は入力・取得文書・Tool結果等の一部を編集し得る。Application側のParser、Normalizer、
検査器、Prompt Builder、Tokenizer／Embedding呼出し、Providerが関係する。

主なTrust Boundaryは、外部表現からApplicationが採用するText、そこから検査対象Text、
そしてToken化・Embeddingへ渡すTextへの移行である。決定論的なEnforcement Pointは、
各経路に共通して通る前処理・Pipeline Gate。Model自身の「正規化したつもり」という回答ではない。

## Required security properties

| ID | 必要な性質と観測条件 |
|---|---|
| SP-1 | 各対象経路に正規化Policyと実行位置が定義され、Token化・Embeddingより前に実行される。 |
| SP-2 | 正規化後に同じ対象Textを使ってToken化・Embeddingする。後続変換が別Textを作る場合は、そのTextに対する正規化の扱いを再評価する。 |
| SP-3 | 正規化に失敗した入力が、未正規化のままFallback経路からToken化・Embeddingへ到達しない。 |
| SP-4 | 対応言語・用途の正常入力を過度に破壊せず、非対応の表現はPolicyに沿って明示的に扱う。 |

SP-4は上流が特定の許容文字を指定したという意味ではない。選んだ正規化が安全な利用経路として
実用に耐えるかを検証するためのRepositoryの品質条件である。

## Scope calibration and adjacent assurance

| 観測 | 本Controlでの扱い |
|---|---|
| Token化・Embedding前に正規化を実行し、利用Textとの対応を示せる | C2.1.1のPositive Evidence。 |
| Encoding済み指示を検出できない | 主にC2.1.2／C2.1.3の別保証。正規化だけではPassにしない。 |
| 検査後に復号したTextを無検査で送る | C2.1.2／C2.1.3の問題が中心。変換後Textの正規化も欠けるならC2.1.1でもFail。 |
| 危険なTool操作が実行される | 入力対策だけの保証外。C5／C9の認可・実行境界を別途評価する。 |

## Threat and failure-mode rationale

攻撃者は全角・互換文字、不可視文字、双方向制御文字等を混ぜ、Parser、検査器、
Tokenizer、Rendererが異なるTextとして扱う差を狙う。例えば後段で互換文字が別表現へ変換されると、
前段で見た値と実際のModel入力が一致しない。Researchはこうした差と処理順序を重点的に扱う。

外部Threat IDとの厳密なMappingは未評価。類似語だけでATLAS IDを付けず、Catalogの`threat_mappings`は空とする。

## Verification

### Architecture and configuration review

各入口からToken化／EmbeddingまでのData Flowを列挙する。文字抽出、Unicode処理、復号、
検査、Prompt組立て、Chunk化、SDK／Providerへの送信位置を示し、PolicyのRevisionと適用順序を追う。
既存の正常化ライブラリがあるだけでPassにしない。

### Positive verification

用途別の正常な日本語・英語・記号・結合文字を入力し、正規化後の値が意図した意味を保ったまま
実際のToken化／Embeddingに渡ることを、境界上のCaptureまたは合成テストで確認する。
同じ意味の許可された表記差は、定義したPolicyどおりに扱われる。

### Negative and abuse-case verification

| ID | 条件・操作 | 期待結果 |
|---|---|---|
| N-1 | User入力に全角・結合文字・不可視文字を混ぜる | 正規化後の値がToken化前に観測できる。未正規化の迂回なし。 |
| N-2 | 同じPayloadをRAG文書、Tool出力、Memory、OCR／音声Textから投入する | 対象となる各経路で同じ順序のGateを通る。 |
| N-3 | 正規化後に別の変換・連結・復号でTextを変える | 変更後Textを未正規化のままToken化・Embeddingしない。 |
| N-4 | 正規化処理を例外・Timeout・設定不在にする | 未正規化で継続せず、安全側に失敗する。 |
| N-5 | 正常な日本語、多言語、Emoji等を通す | Policyが対応を宣言する文字を不必要に削除・破壊しない。 |

N-1の存在は、全ての不可視文字の除去を必須とする意味ではない。危険な表現を拒否・保持・変換する
判断は用途別Policyと隣接要件を踏まえる。比較は表示画面だけでなく、実際に渡るCode Point列等で行う。

### Failure conditions

対象経路の一つがNormalizerを迂回する、正規化をToken化／Embedding後に行う、
正規化失敗で原文へFallbackする、または後続の変換後Textをそのまま利用して正規化の適用を
示せない場合はFail。選択方式がNFCかNFKCかだけではPass／Failを決めない。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| 入力経路・変換順序図 | Application／Data Owner | 全Token化・Embedding経路 | Pipeline変更時 | Revision付き、機密Textは含めない | Gateと利用Textの関係が追える。 |
| 正規化Policy | Security／Application Owner | 対応言語・入力型 | Policy変更時 | Revisionと承認履歴 | 方式、対象、例外時処理、正常入力の扱いを定義。 |
| 境界テスト | Test Harness | N-1〜N-5の合成入力 | Release・Tokenizer／Parser変更時 | 合成DataとTest Revisionを保持 | 迂回・未正規化Fallbackがなく、正常系も成立。 |

## Related requirements

| Requirement | 違い |
|---|---|
| `v1.0-C2.1.2` | Encoding／Representation Smugglingの検出と緩和。正規化の実行順序より広い。 |
| `v1.0-C2.1.3` | Modelを誘導し得る入力のInjection検査と、Flag時の遮断。 |
| `v1.0-C2.1.5` | 許可文字集合の制限。正規化とは別の制約。 |
| `v1.0-C8.2.4` | Retrieval操作用ContentのVectorization前検査。正規化のみでは満たせない。 |

## Known limitations and uncertainty

Unicode正規化でHomoglyph、隠れた命令、画像内Text、意図的な多段復号を完全には扱えない。
Font描画とCode Pointの差、Provider内部のToken化差も残る。入力を過剰に畳み込むと識別子・
多言語文書の意味が変わり得る。これらを説明したうえで別の検査・認可境界を組み合わせる。

本書の`verifiable`はRepository Artifactの成熟度であり、製品への適合や検出率を示さない。

## References

- [AISVS v1.0 C2 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md)
- [AISVS v1.0 C2.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md)
- [C2 Family概要](../README.md)

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-28 | C2.1.1の初期Controlを作成 | AISVS固定RevisionとRepository interpretation | 本書のSP・N・Evidence。製品試験は未実施 |
