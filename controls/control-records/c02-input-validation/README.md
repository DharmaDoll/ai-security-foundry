# AISVS C2 Input Validation

対象はAISVS v1.0の固定Revision `78775233666a2022dcfb82037e5e029116955c00`。
以下は[正規要件][normative]の代替ではなく、C2の保証範囲を辿るためのRepository interpretation。
[Section単位の学習資料](../../learning/c02-input-validation/README.md)は講義と対話を扱う。
Controlの成熟度は学習進捗とは独立して[Catalog](../../catalog.yaml)で管理する。

## この章で保証したいこと

入力を「Modelへ渡す前に一度見た」だけでは、実際に利用する内容の安全性は説明できない。
取得、正規化、復号、検査、構築、Token化、Embeddingの間で表現や内容が変わり得る。
C2は入力によるModelの振る舞いの誘導を扱い、用途に応じた検査・拒否を実際の利用経路へ結び付ける。
入力検査だけでPrompt Injectionの完全防止、Tool認可、出力の安全性を主張しない。

## Categoryで問うこと

| 問うこと | できてはいけないこと |
|---|---|
| Modelへ渡す入力の表現・内容・構造と、実際に利用する内容が検査の想定から外れていないか。 | 検査後の変換や新規入力経路によって、未検査の内容を信頼済みContextへ流す。 |

## Section

| Section | 問うこと | できてはいけないこと |
|---|---|---|
| C2.1 Prompt Injection Defenses | 隠蔽・過長・役割偽装・多数例による指示誘導を、入力境界で検出・制限できるか。 | 入力が表現やMessage境界を変えて検査をすり抜ける。 |
| C2.2 Content & Policy Screening | 禁止内容や非テキスト・複合入力を用途別Policyで扱えるか。 | テキストだけを検査し、他の入力から同じ禁止内容を通す。 |

## C2.1 Requirement

ResearchはUnicode隠蔽、変換順序、検出器回避、長文・多ターン攻撃を挙げるが、
これらはNegative Testの候補であり、研究上の提案すべてがAISVSの必須条件ではない。
隣接する要件の違いは次のとおり。Levelは上流の検証レベルであり、開発優先度ではない。

| ID | 固有の確認点 | これだけでは保証しないこと |
|---|---|---|
| C2.1.1 | Token化・Embedding前の正規化 | 全Encoding隠蔽の発見 |
| C2.1.2 | 表現Smugglingの検出・緩和 | 全Injectionの検出 |
| C2.1.3 | 全入力経路の検査と検知時遮断 | 検出器の完全性・Tool認可 |
| C2.1.4 | Context上限超過の拒否 | 全資源消費の制御 |
| C2.1.5 | 用途に必要な文字集合 | 有害な意味内容の発見 |
| C2.1.6 | 信頼できる指示の優先順位 | Modelだけによる決定論的認可 |
| C2.1.7 | 予約特殊Token表現のLiteral化 | 自然言語の役割詐称の完全防止 |
| C2.1.8 | Many-shot攻撃の検出 | 単発・少数ターンの攻撃検出全般 |

個別Controlが未作成の行は、未成熟の保証上の問いであって、Catalog登録済みControlではない。

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C2.1.1](v1.0-c2.1.1-normalize-input-before-tokenization-or-embedding/README.md) | 1 | 実際にToken化・Embeddingする入力を、その前に正規化しているか。 | 検査後の変換で別の表現へ変わり、未確認の内容を利用する。 |
| [C2.1.2](v1.0-c2.1.2-detect-and-mitigate-encoded-input-smuggling/README.md) | 1 | Encoding・表現の隠蔽を検出し、許可された方法で緩和するか。 | 隠した指示を復号して未検査のまま利用する。 |
| [C2.1.3](v1.0-c2.1.3-screen-and-block-model-steering-inputs/README.md) | 1 | Modelを誘導し得る全入力を検査し、検知時に遮断するか。 | 一部経路を素通しにする、または検知だけで継続する。 |
| [C2.1.4](v1.0-c2.1.4-reject-over-limit-input-without-truncation/README.md) | 1 | Context上限超過入力を切り詰めず拒否するか。 | 超過後に黙って末尾を捨て、意味や指示を変える。 |
| [C2.1.5](v1.0-c2.1.5-allowlist-required-input-characters/README.md) | 1 | 用途に必要な文字だけを許可するか。 | 不要な不可視・制御文字を無条件で受け取る、または必要な多言語文字を壊す。 |
| [C2.1.6](v1.0-c2.1.6-preserve-instruction-hierarchy-across-steps/README.md) | 2 | 信頼できる指示が後続の非信頼入力に上書きされないか。 | Userや文書が自称したRoleを上位指示として採用する。 |
| [C2.1.7](v1.0-c2.1.7-render-reserved-tokens-as-literal-content/README.md) | 2 | 予約特殊Tokenの文字列表現をLiteralとして扱うか。 | 入力文字列が実際のMessage境界になる。 |
| [C2.1.8](v1.0-c2.1.8-detect-many-shot-jailbreak-patterns/README.md) | 3 | Many-shot Jailbreakの構造を検出できるか。 | 大量の例示による誘導を未評価で通す。 |

## C2.2 Requirement

C2.2は学習済み。対応Researchを確認し、RequirementごとにControlを成熟させる。
最初のC2.2.1は、内容分類だけでなく閾値超過時のModel投入前制御までを扱う。

| ID | 固有の確認点 | これだけでは保証しないこと |
|---|---|---|
| C2.2.1 | 四区分の内容分類と閾値超過時の投入前制御 | 非対応言語での分類精度 |
| C2.2.2 | 非対応・不明言語での分類評価 | 全言語対応や評価後の一律拒否 |
| C2.2.3 | 非テキスト入力の隠蔽・攪乱・既知攻撃の検査 | 複数形式の関係性から成立する攻撃の遮断 |
| C2.2.4 | 複数形式にまたがる攻撃の検出と遮断 | 下流Actionの決定論的認可 |

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C2.2.1](v1.0-c2.2.1-screen-prompts-before-model-context/README.md) | 1 | 四つの内容区分で各PromptをScore化し、閾値超過を投入前に拒否・無害化するか。 | 閾値超過をLogだけに残して未処理のままModelへ渡す。 |
| [C2.2.2](v1.0-c2.2.2-evaluate-content-classification-for-unsupported-languages/README.md) | 1 | 非対応・不明言語での分類性能を実際のPrompt経路で評価するか。 | 英語での成功やProviderの対応表だけで多言語の有効性を主張する。 |
| [C2.2.3](v1.0-c2.2.3-check-non-text-inputs-for-hidden-attacks/README.md) | 2 | 非テキスト入力の隠蔽・攪乱と、変換後にModelが見る内容を検査するか。 | 元Fileや抽出Textだけを見て、未検査のMedia成分を検査済みと扱う。 |
| [C2.2.4](v1.0-c2.2.4-detect-and-block-cross-modal-attacks/README.md) | 3 | 異なる入力形式の組合せで成立する攻撃を検出・遮断するか。 | 各形式だけを個別に安全と判定し、合成後の攻撃をLogのみで通す。 |

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md

開発順序と進捗は[Controls計画](../../plan.md)を参照する。個別Controlでは対応する[Research C2.1](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md)または[Research C2.2](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-02-Content-Policy-Screening.md)を確認する。
