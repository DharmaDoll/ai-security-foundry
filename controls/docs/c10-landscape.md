# AISVS C10：保証範囲と段階的なControl整備

- 調査日：2026-09-10
- 対象：採用済みOWASP AISVS v1.0、C10 Model Context Protocol (MCP) Security
- 固定Revision：`78775233666a2022dcfb82037e5e029116955c00`（C5/C9と同じ）
- 状態：章の分析と代表要件の選定。個別Controlは未着手。

本資料は採用済みSnapshotを分析する。AISVSやMCPの最新版への追従を宣言するものではない。
要件本文を正本とし、Researchの章概要と全4節の要件別Verification・Gapsを参照した。
Researchが列挙する製品、事件、統計の真偽・最新性を一括認定せず、製品推奨を転記しない。

## 1. この章で保証したいこと

社内AgentがMCP Server経由で文書APIを呼ぶ場合、利用者の権限を正しく判定していても、
接続先がすり替わる、導入したローカルServerが秘密を読む、受信Tokenを別APIへ流用する、
承認後のツール説明が変わる、といった失敗が残る。

C10は、MCPを通じて外部の機能・データを利用するとき、許可した接続先と構成要素だけを使い、
各要求の認証・認可、通信とメッセージの検証を行うことを扱う。導入後の変更や不正な応答に
よって、意図しない権限行使やデータ露出が起きる経路を制限する。[要件本文][normative]

このRepositoryでは、次の問いへ翻訳して理解する。

- 導入・接続するServerは許可したもので、出所と改変の有無を確認できるか。
- ローカルで起動したServerが、必要以上にファイル・ネットワーク・システムへアクセスできないか。
- 接続できたことだけを信頼せず、要求ごとに利用者と操作・引数の権限を確認しているか。
- MCP Server用に受け取った資格情報を、別の下流APIへそのまま渡していないか。
- 通信相手や要求先を確認し、不正な形式・過大なメッセージ・再送された応答を扱えるか。
- ツール定義や応答をモデルへ渡す前に検査し、定義変更後は再承認まで呼び出しを止められるか。

これらは章全体の保証対象を理解するための問いであり、各要件の適用範囲やLevelを置き換えない。
出所の確認や応答検査ができても、部品の無害性やPrompt Injectionの完全防止まで保証するものではない。

Trust Boundary（信頼境界）は、相手から受け取った情報・要求をそのまま信頼せず、
検証や認可を必要とする境目である。C10では次を区別する。

- 配布元・設定ファイル → MCP Hostによる導入・プロセス起動。
- MCP Client → MCP Serverの通信・認証・認可。
- MCP Server → 下流APIの別の資源・権限。
- MCP Serverの定義・応答 → ClientのモデルContextと次の行動。

### C5/C9の次にC10を扱う理由

C5のIdentity・資源認可、C9のAgent行動制御に続き、Protocolと接続部品の保証を深める
順序が有用と判断した。これはRepositoryの優先順位であり、すべての製品でC8より重要という意味ではない。

## 2. 全4節の見取り図

固定要件本文には23件ある。LevelはAISVSの検証レベルであり、Control成熟度ではない。
表の保証対象はRepositoryによる要約。[要件本文][normative]

| 節 | ID範囲・件数 | Level内訳 | 保証対象 |
|---|---|---|---|
| C10.1 Component Integrity | 10.1.1–10.1.3：3件 | L1：1、L2：2 | 配布元・暗号的検証、許可したServerの利用、ローカルServerの最小権限隔離。 |
| C10.2 Authentication & Authorization | 10.2.1–10.2.7：7件 | L1：3、L2：4 | 毎要求のToken検証、発行者・宛先・期限・Scope、Token非永続化、ツール一覧と呼び出しの認可、Session終了処理、下流へのToken転送禁止。 |
| C10.3 Secure Transport | 10.3.1–10.3.5：5件 | L1：2、L2：2、L3：1 | 遠隔通信とローカルstdioの適用境界、Origin/Host検証、Protocol最低版、送信者に結び付いたToken。 |
| C10.4 Schema, Message, and Input Validation | 10.4.1–10.4.8：8件 | L1：3、L2：4、L3：1 | 応答形式とInjectionの検査、入力と通信量の制限、署名応答の再送検知、導入同意、ツール定義変更の再承認。 |

計L1：9件、L2：12件、L3：2件。節名だけでは、導入同意や定義変更もC10.4に含まれることを
見落としやすい。配置を変えるのではなく、個別Controlで対象境界を明記する。

## 3. Researchから引き継ぐ問いと解釈上の注意

以下はResearchを踏まえた検討方針。補足的な試験案をすべての要件の必須条件にはしない。

- **導入境界**：許可したServer名が同じでも、実行ファイル、引数、配布元、接続先が
  変わっていないかを調べる。暗号的検証は出所・改変の確認であり、コードの安全性そのものを
  証明しない。ローカル起動はClientと同じ権限での実行になっていないかを確認する。[R1][r1]
- **認可境界**：最初の接続成功やSession IDだけで後続要求を通さない。
  ツール一覧から隠すことと、直接呼び出しを拒否することを分ける。
  Tokenの宛先一致だけでTenantや個別文書の認可を証明したことにはならない。[R2][r2]
- **Session終了**：切断と終了を同一視せず、終了条件、残存物、Replica・Queueを含む
  消去範囲を定義する。監査用に保持する情報と再利用可能なSession状態の境界は個別解釈で詰める。[R2][r2]
- **通信境界**：HTTPS、Origin、Hostは異なる確認である。Originは要求元Web Origin、
  Hostは要求先Hostを表す。Proxyで書き換わる値と信頼する経路を明示する。
  stdioは標準入出力によるローカル子プロセス通信であり、それ自体が隔離を提供するわけではない。[R3][r3]
- **内容境界**：Schema（データ形式の契約）が正しくても、内容に悪意ある指示は入る。
  C10.4.2の検査を完全なInjection防止と表現しない。署名された応答にも危険な内容は入り得る。[R4][r4]
- **変更境界**：ツール定義のSnapshotと実際の呼び出し時の定義を比較する。
  通知を受けることと再承認前に実行を止めることは別である。定義不変でもServer内部の
  実装は変わり得るため、C10.4.8だけで挙動の不変性を保証しない。[R4][r4]

AISVSの要求、MCP仕様の規範、Researchで提案する拡張を区別する。特に応答署名、
送信者制約Token、定義の再承認などについて、AISVSの要求をそのまま「MCP標準機能」と呼ばない。
個別ControlでProtocol挙動を根拠にする際は、その時点で使用する公式MCP仕様の版・状態を
直接確認する。Research内の版や製品対応表から現在の対応可否を推定しない。

## 4. 最初の代表要件：v1.0-C10.2.7（Level 2）

要旨は、Clientから受け取ったAccess TokenをMCP Serverが下流APIへそのまま渡さないこと。
Token passthroughは、この受信Tokenの透過的な転送を指す。[要件本文][normative]

最初に選ぶ理由は、Client → MCP Server → 文書APIという短い経路で、
「利用者の委任を引き継ぐこと」と「同じ資格情報を引き回すこと」の違いを具体化できるため。
C9.5.2の委任Context伝播と比較でき、MCP固有の要求範囲も明確になる。
初期Golden ControlであるC5.2.5は維持する。

| 検討項目 | 次の個別Controlで深める内容 |
|---|---|
| 保証特性 | 受信したClient Tokenが下流APIへの資格情報として転送されない。 |
| 具体例 | 文書APIには別途取得した対象API用の資格情報を使う。その取得方式を一方式に固定しない。 |
| 強制点 | MCP Serverの下流呼び出し経路と資格情報取得境界。 |
| 正常試験 | 正規利用者の許可された要求が、下流用の資格情報で成功する。 |
| 拒否・悪用試験 | 受信Tokenの転送を要求する入力、交換失敗後の元TokenへのFallback、別APIへの宛先変更を試す。下流観測で転送がないことを確認する。 |
| 証拠 | 資格情報フロー、下流呼び出し実装の確認、合成Tokenを使った試験結果。実Tokenを監査ログへ保存しない。 |
| 限界 | 別Tokenでも過大権限は起こる。非転送だけで委任元の制限維持、引数認可、認可の最新性まで保証しない。 |

比較候補はC10.2.5（L2）、C10.1.2（L2）、C10.4.8（L3）。C10.2.5はC9.5.1との
違いを整理する価値があるが、初手は新たな資格情報境界を選ぶ。C10.1.2とC10.4.8は
導入時・変更時の別の保証を扱うため、後続の代表要件とする。これはRepositoryの選定判断である。

## 5. 段階的な進め方

1. **今回：全体像と初手の確定。** 本資料に4節の境界と解釈上の注意を残す。
2. **次：C10.2.7。** 正確な本文と対応Researchを再確認し、既存Templateで解釈・適用範囲・
   脅威・正常/拒否試験・証拠期待値・限界を整備してCatalogへ追加する。
3. **各境界の代表：C10.1.2 → C10.3.3 → C10.4.8。** Serverの許可、HTTP境界、定義変更を
   一件ずつ整備する。各件で独立したVerificationとEvidenceを具体化する。
4. **残る要件。** C10.2の認証・認可・Session、C10.1の出所・隔離、C10.3のTransport、
   C10.4の形式・内容・再送・同意を順に深める。近接要件を一つへ吸収しない。
5. **章の整合確認。** 本文/Research/Repository解釈、ID・Level、重複と非保証範囲、
   Catalog・リンクを確認する。全件の成熟化を完了した時点で結果を報告する。

今回の分析ではCatalogの成熟度を進めない。学習は希望時に別の流れで行う。
Engineeringは独立に発見・開発し、両側が理解可能になってからMappingを評価する。

## 参照

- [固定RevisionのC10要件本文][normative]
- [Research章概要][overview]
- [R1：Component Integrity][r1]
- [R2：Authentication & Authorization][r2]
- [R3：Secure Transport][r3]
- [R4：Schema, Message, and Input Validation][r4]
- [Controls計画](../plan.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md
[overview]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-MCP-Security.md
[r1]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-01-Component-Integrity.md
[r2]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-02-Authentication-Authorization.md
[r3]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-03-Secure-Transport.md
[r4]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-04-Schema-Message-Validation.md
