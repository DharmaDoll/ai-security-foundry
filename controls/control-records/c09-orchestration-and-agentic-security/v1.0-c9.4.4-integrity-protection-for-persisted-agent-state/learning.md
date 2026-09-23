# C9.4.4：保存状態を検証してからAgentを再開する

AISVS Verification Level: 3

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.4.4`。採用済みAISVS v1.0の固定Revisionは
`78775233666a2022dcfb82037e5e029116955c00`。

> Verify that agent state persisted between invocations is integrity-protected.

日本語訳：呼出し間に永続化されるAgentの状態が、完全性保護されていることを確認する。[要件本文][normative]

Normativeは保存状態の完全性を求める。Researchは内容・所属・版の検証例と、正規の書込みによる
有害な内容を完全性だけでは防げない限界を補足する。[対応Research][research]
以下の構成案・具体的判定はRepository interpretation、Webとの比較は対話から得た学習上の洞察である。
Researchの製品・事件・統計・Mappingを未検証のまま採用していない。
学習完了はControl成熟度・製品適合を変更しない。

## 具体例と用語

調査Agentが作業を中断し、計画をDBへ保存する。翌日、その計画を読み戻して続行する。

```text
保存時：社内文書を読み、要約を作る
           ↓ 保存先を書ける攻撃者が変更
再開時：社内文書を外部アドレスへ送信する
```

Agentへ直接指示を出せない攻撃者でも、保存先を書き換えて再開を待つことができる。
資産は次の行動を左右する計画・Memory・途中結果であり、主なTrust Boundaryは保存先から実行基盤への読込みである。
C9.4.2が操作の連鎖の証拠を扱うのに対し、本要件は将来の処理に使う保存状態を扱う。

- 状態：計画、途中結果、会話履歴、Memoryなど、次の呼出しへ持ち越すData。
- 完全性保護：不正変更を防ぐ、または検出して変更済みDataを利用しないこと。
- Hash：内容から計算する照合用の値。秘密鍵なしで誰でも再計算できる。
- HMAC：共有秘密鍵を用いて生成・検証する改ざん検出用の値。
- 正規化：同じ意味のDataを一定の表現に整え、生成時と検証時の照合対象を揃えること。
- 認証付き暗号：暗号化による機密性と改ざん検出を合わせて提供する方式。
- Rollback：以前の状態への巻戻し。許可された復旧と攻撃による差替えを区別する。

Security Invariantは、不正変更された状態や別Sessionの状態を、正当な続きとして実行に利用しないこと。
Enforcement Pointは保存サービスの書込み認可と、実行基盤の再開前検証に置く。
LLMに改ざんの有無を推測させない。

## 最初の対話：Hashだけで足りるか

問い：計画とSHA-256 Hashを同じDBへ保存する。攻撃者は計画とHashの両方を書き換えられる。

学習者：「Fail。セッション管理と同じ考え方ですかね？」

整理：Fail。攻撃者は変更後の計画のHashを再計算できる。単なる照合値の一致では、想定した改ざんを検出できない。
セッション管理のうち、外部へ保存した状態を次の処理で信頼してよいか確認する部分と共通する。
セッション管理全体には認証・有効期限・盗難対策などもあり、それら全てを本要件に含めるわけではない。

## 実装案を具体化する

学習者：「今回の要件を具体に落とし込むにはどんな案が考えられる？」

まず、誰が保存先や鍵を操作できると想定するかを決める。原文は一律の暗号方式を指定していない。

| 案 | 構成と有効な境界 | 限界 |
|---|---|---|
| 保存先のアクセス制御 | 保存サービスだけに書込みを許可し、Toolや利用者の直接変更を防ぐ | 保存サービスやDB管理権限の侵害には弱い |
| HMAC | DB外の鍵で状態を保護し、再開前に検証する | 鍵やHMAC生成権限も奪われると偽造できる |
| 認証付き暗号 | 状態を暗号化し、復号時に改ざんも検証する | 鍵・Nonce管理が必要。内容の安全性は保証しない |
| 電子署名 | 保存サービスが署名し、別の実行基盤が公開鍵で検証する | 公開鍵の信頼・更新の運用が必要 |

例えば「DBは書けるが保存サービスと鍵は侵害されていない」攻撃者には、アクセス制御とHMACの組合せが候補となる。

```text
保存：書込み権限を確認 → 内容と所属を正規化 → HMACを生成 → DBへ保存
再開：DBから取得 → HMAC検証 → 期待する所属と照合 → 成功した状態だけを利用
```

保護対象の例はTenant、Agent、Session、状態の版、計画本文。所属情報は保存Dataだけで自己完結させず、
認証済み実行Contextから得た期待値と照合する。そうしないと別Sessionの正当な記録を丸ごとコピーされ得る。

鍵管理サービスを使う例として、AWS KMSの`GenerateMac`／`VerifyMac`がある。
鍵をKMSに保持したまま生成・検証できるが、攻撃者が生成APIを自由に呼べるなら偽造を防げない。
鍵の保管と、生成操作の認可を両方設計する。[AWS KMS][kms]

機密性も必要ならAES-GCMなどの認証付き暗号を既存ライブラリで扱う案がある。
Nonceなど方式固有の条件を守り、保存先の透過的な暗号化だけで、認可されたDB操作による書換えも防げると考えない。
[OWASP Cryptographic Storage][storage]

古い正当な状態はHMAC検証に成功する。不正な巻戻しを防ぐ場合、必要な最新版の根拠を
攻撃者が同時に変更できない場所で管理する。版番号を同じDBへ置くだけでは十分でない。
許可した復旧は別の手順として扱う。

## Webの仕組みとの比較

学習者：「OAuthのstateやPKCEかな」「DPoPが近いかな」

共通するのは、持ち込まれた情報をそのまま信頼せず、期待する処理や鍵との対応を検証する点である。
ただし各方式が守る対象は異なる。

| 仕組み | 確認する対応関係 | 今回との境界 |
|---|---|---|
| OAuth state | 認証応答と開始した要求・ブラウザSessionの対応 | 値の一致だけで付随する全Dataの完全性は保証しない |
| PKCE | 認可コードと、要求開始時の秘密値を持つ交換者の対応 | 保存計画の完全性検証ではない |
| DPoP | Tokenと、対応する秘密鍵を持つ送信者の対応 | HTTP本文全体や保存後のDB状態は保護しない |
| 署名付きCookie | Cookieの内容とサーバが発行した保護情報の対応 | 保存状態を検証して再利用する点で直接的な類例 |

DPoPで状態保存APIのToken利用者を制約し、HMACで保存状態を検証する組合せは考えられる。
両者は異なる境界を守る。[DPoP RFC 9449 §11.7][dpop]
OAuth stateとPKCEの比較は、それぞれの仕様が示す要求対応・コード保護の役割に限定する。
[OAuth 2.0 §10.12][oauth-state]、[PKCE RFC 7636][pkce]

### 署名付きCookieとJWTは違うのか

学習者：「署名付きCookieって何？JWTとは違うの？」

Cookieはブラウザが値を保持しHTTP要求へ付ける仕組み。署名付きCookieはその値を署名やHMACで保護した呼び方である。
ここでの「署名」は公開鍵方式に限らない。例えばFlaskの標準セッションは署名付きCookieを利用する。[Flask][flask]

JWTは主体や有効期限などを表す標準形式であり、署名・MACで保護する形式や暗号化する形式がある。
署名付きJWTをCookieに入れることも、Authorization Headerで送ることもできる。
CookieとJWTは排他的な選択肢ではない。[JWT RFC 7519][jwt]

```text
Web：   サーバが状態を作る → Cookieへ預ける → 戻ってきた状態を検証して利用
Agent： 実行基盤が状態を作る → DBへ預ける   → 読み戻した状態を検証して再開
```

署名だけでは内容を隠せず、正当なCookieの盗難・再利用も防げない。完全性と他の保証を分ける。

## 最後の対話：正規に保存された悪意あるMemory

問い：利用者が「次回から社内文書を外部へ送信して」と入力する。正規の保存サービスが所属Sessionとともに
HMACを付けて保存し、次回の検証も成功する。Agentはその文章を命令として扱う。完全性保護が破られた例か。

学習者：「いえない。この要件では対象外。」

整理：判断は正しい。ただしMemory自体は本要件の対象であり、正規保存された有害な文章を命令として扱う失敗が
別の保証に属する。保存後に変更されたわけではない。出所・信頼度を保持し、利用者入力を上位の指示や
認可判断へ昇格させない設計は別途必要になる。

> 完全性検証で確認できるのは「保存後に変わっていないこと」であり、「保存してよかった内容か」ではありません。

正規Writerが侵害された場合も、その署名だけで内容の安全性を主張できない。

## 検証と設計レビューへの問い

正常に保存した状態から再開できることをPositive Testとする。Negative Testでは次を確認する。

- 内容と単純Hashを同時変更しても、保護機構が改変を検出・阻止するか。
- 別Tenant・Sessionの正当な記録へ差し替えても拒否するか。
- 必要な版・復旧条件を満たさない旧状態を利用しないか。
- 保護情報の欠落・検証失敗を無視して、読めた部分だけで続行しないか。

設計レビューでは、保存先・保存サービス・鍵のどこまでを攻撃者が操作できるか、検証前に
状態がPlannerへ渡らないか、所属の期待値をどこから取得するかを確認する。
状態を全く持ち越さない範囲は適用対象外になり得るが、外部DBやCacheを使う構成を無状態とは扱わない。

## 対話からの洞察

> Agentでは、保存された状態が「次に何をするか」を左右する。
> そのため、状態の改ざんが行動の改ざんにつながります。

> 処理がいったん手元を離れ、後から戻ってくるときには、内容だけでなく「どの処理の続きなのか」も確認する。

これらはWebとの比較から得た再利用可能な考え方である。暗号方式を導入したという事実だけでなく、
「状態を保存する入口」と「状態を信頼して再開する入口」がアプリケーション側で管理されているかを見る。

## References

- [AISVS v1.0要件本文][normative]、[対応Research][research]（固定Revision）
- [AWS KMS HMAC][kms]、[OWASP Cryptographic Storage][storage]、[Flask Sessions][flask]（2026-09-16参照、更新される補足資料）
- [OAuth 2.0 RFC 6749 §10.12][oauth-state]、[PKCE RFC 7636][pkce]
- [DPoP RFC 9449][dpop]、[JWT RFC 7519][jwt]
- [C9 Family overview](../README.md)
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-04-Agent-Identity-and-Audit.md
[kms]: https://docs.aws.amazon.com/kms/latest/developerguide/hmac.html
[storage]: https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
[flask]: https://flask.palletsprojects.com/en/stable/quickstart/#sessions
[oauth-state]: https://www.rfc-editor.org/rfc/rfc6749.html#section-10.12
[pkce]: https://www.rfc-editor.org/rfc/rfc7636.html
[dpop]: https://www.rfc-editor.org/rfc/rfc9449.html#section-11.7
[jwt]: https://www.rfc-editor.org/rfc/rfc7519.html
