---
title: "C2.1 Prompt Injection Defenses：検査した内容と利用する内容を一致させる"
document_kind: "section-learning-note"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
last_updated: "2026-09-27"
---

# C2.1 Prompt Injection Defenses

## Normative Requirements

AISVS v1.0を対象とする。[固定版の英語原文](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md)を正本とし、ここでは大量の原文転載を避け、日本語要約を示す。Levelは上流のVerification Levelであり、学習難易度やControl成熟度ではない。

| ID | Level | 日本語要約 |
|---|---:|---|
| v1.0-C2.1.1 | 1 | Token化・Embedding前に入力を正規化する。 |
| v1.0-C2.1.2 | 1 | Encoding・表現による隠蔽を検知し、許容された方法で対処する。 |
| v1.0-C2.1.3 | 1 | Modelを誘導し得る入力を信頼せず、Injection検査で検出した入力を遮断する。 |
| v1.0-C2.1.4 | 1 | Context上限超過を防ぎ、超過入力は切り詰めず拒否する。 |
| v1.0-C2.1.5 | 1 | 明示的に必要な文字だけを許可する文字集合制限を設ける。 |
| v1.0-C2.1.6 | 2 | User処理後も、System・Developer指示が信頼できない入力より優先される階層を維持する。 |
| v1.0-C2.1.7 | 2 | 予約済み特殊Tokenを通常の文字として扱い、Context構造へ注入させない。 |
| v1.0-C2.1.8 | 3 | Many-shot Jailbreakingを検知する。 |

## 文書の役割・Source separation

- Normative：上記IDの保証範囲は原文で確認する。
- Research：隠蔽、変換順序、検査経路、検知の限界を補足する。
- Repository interpretation：以下のScenario、対策、テストは実設計へ翻訳した例であり、唯一の適合方法ではない。
- Derived insight：対話で得た設計原則を独立して示す。

Control本文・Catalog・Mappingは今回作成・更新していない。[Family guide](../README.md)へ戻る。

## 位置づけと具体Scenario

取引先文書を取得して要約するAgentを考える。攻撃者は文書本文を書き換えられるが、アプリのSystem設定や認可Policyは変更できない。文書に隠した指示で、要約を変更したりTool操作へ誘導したりする。

Trust Boundaryは、取引先文書から取込処理、検査器からPrompt組立て、外部資料から信頼された指示、Modelの要求からTool実行の各境界にある。

保護対象は指示の優先順位、回答の完全性、接続先の機密情報や操作権限。C2.2は要求内容のPolicy違反、C7は出力、C5/C9は認可・行動を扱う。C2.1だけでこれらを保証しない。

## 用語

- 正規化：表記の差を決めた形式へそろえる。Unicode NFC/NFKC等を用途に応じて選ぶ。すべての似た文字が同じになるわけではない。
- Encoding／復号：Base64等の別表現へ変換し、元へ戻すこと。暗号化とは別。
- Token化：Modelが扱う単位へ入力を分割すること。
- Embedding：検索等に用いる数値表現へ変換すること。
- Context：Modelが一度に処理する指示、質問、文書等の全体。
- 指示階層：信頼された指示と外部資料の優先順位。文書が自称する役割は信頼しない。
- 特殊Token：Model固有のメッセージ境界等を表す予約済みの単位。
- Many-shot：大量の架空の問答で不正な振る舞いを模倣させる攻撃。連続投稿回数とは別。

## Security Invariant・対策・Negative tests

中心となるInvariantは「検査結果を検査した内容に結び付け、後続の変換・追加によって未検査内容を利用しない」。アプリの前処理、Prompt組立て、送信判定がEnforcement Pointになる。意味の検知精度は確率的でも、危険判定後の遮断はアプリで強制できる。

| 要件 | 対策例 | Negative testと期待結果 |
|---|---|---|
| 2.1.1 | 正規化後の内容を検査・Token化へ渡す。 | 全角等の表現差で、検査後に攻撃文が現れない。 |
| 2.1.2 | 復号出口で再検査。不要なEncodingは用途別Policyで扱う。 | Base64で隠した指示が未検査のまま次段へ流れない。 |
| 2.1.3 | User、RAG、Tool、Memoryの経路を検査し遮断へ接続。 | Tool出力の検知済み攻撃がLogだけ残して継続されない。 |
| 2.1.4 | 対象Tokenizerで組立て後の合計を計測。 | RAG追加による超過を、黙って削らず拒否する。 |
| 2.1.5 | 入力欄・言語・用途ごとに必要な文字を定義。 | 商品IDの許可外不可視文字を拒否し、正常な対応言語は通す。 |
| 2.1.6 | アプリが役割を決め、資料をSystemへ昇格させない。 | 文書の「新System指示」を構造・振る舞いの両面で評価。 |
| 2.1.7 | 使用するTokenizer・Templateで予約表現を通常の文字として扱う。 | 入力から新しいメッセージ境界が生成されない。 |
| 2.1.8 | 大量の不正問答の構造を評価。 | 攻撃問答を検知し、正常FAQへの誤検知も測定。 |

正規化はInjectionを完全除去しない。日本語をASCII限定にする等の乱暴な許可リストや、あらゆる入力の無制限な再帰復号は推奨しない。文字の正当性と業務用途を合わせて評価する。

## Pass／Failと保証境界

- Fail：検査後に復号した本文を、追加評価なしでModelへ送る。
- Passの例：変換後の利用内容を検査し、検出時に送信を停止する経路を実測できる。ただし、未知攻撃の完全検知は保証しない。
- Fail：社内SharePoint由来だからと本文検査を省略する。
- Fail：Context超過時に末尾を黙って削る。
- 別問題：必要文書を検索時に選んで上限内に構成することは、超過後の黙った切り詰めと同じではない。
- 別保証：指示階層・検査の存在を、送金認可や完全なInjection防止と扱わない。

## 対話の再構成

1. 問い：検査後に復号する構成は十分か。学習者：「Fail。検査はモデル送信直前で行います」。整理：直前という位置だけでなく、検査後に未検査の変換・追加が入らないことが本質。
2. 問い：正規SharePointから取得した文書は検査不要か。学習者：「No」。整理：取得元の認証と内容の信頼は別。
3. 問い：上限超過後に末尾を黙って削れるか。学習者：「no」。整理：事前の資料選択と区別する。
4. 所感：「一つ一つがnegative testに該当しそう。具体的対策例も欲しい」。整理：一要件一テストではなく、経路を変えて試し、正常系も対にする。
5. 問い：具体実装はEngineeringに置くか。整理：Controlは保証・検証、Engineeringは実システムの設計問題と実装・テスト、Learningは理解を扱う。ControlからPatternを機械的に生成しない。
6. 合意：実装計画を[Issue #4](https://github.com/DharmaDoll/ai-security-foundry/issues/4)へ登録。バックログは将来の作業候補であり、着手・期限・実装完了を意味しない。

## Derived insights・レビュー項目

> 検査の場所より、検査した内容と実際に使う内容の一致が本質。

> 攻撃を見抜けるかと、見抜いた攻撃を止められるかは、別の品質。

- 全入力経路と、その後の変換・追加処理を列挙したか。
- 同じ検査結果を変更後の内容へ流用していないか。
- 検知器の精度と遮断経路を別々にテストしたか。
- 正常な多言語入力も受け付けられるか。
- 検査を認可の代替にしていないか。

## References

- [C2.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md)
- [OWASP Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)：補助Guidance。製品の仕様や性能値はここでは採用しない。
