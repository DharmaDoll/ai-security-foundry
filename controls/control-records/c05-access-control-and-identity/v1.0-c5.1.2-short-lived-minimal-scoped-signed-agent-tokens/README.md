---
title: "Short-lived Minimal-scoped Signed Agent Tokens"
versioned_id: "v1.0-C5.1.2"
requirement_id: "C5.1.2"
verification_level: 3
family_id: "C5"
source_key: "owasp-aisvs"
source_version: "1.0"
source_status: "stable"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
upstream_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md"
research_url: "https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-01-Identity-Management-Authentication.md"
last_verified: "2026-09-08"
maturity: "verifiable"
mapping_assessment_refs: []
---

# System間のAgent認証に使う短命・最小Scope・署名済みToken

AISVS Verification Level: 3

初めて読む方へ：[具体例・用語・対話を含む学習ノート](learning.md)。

## Upstream basis

AISVS `v1.0-C5.1.2`、Verification Level 3を解釈する。複数SystemまたはFederationで動く
AI Agentの認証に、短命、最小Scope、暗号学的署名を備えたTokenを要求する。
固定RevisionのC5.1 Research（Last Researched: 2026-07-14）の該当行を確認した。
ResearchはIssuerと鍵の結び付け、期限、対象System、Tenant、Replay等の確認を補足する。
一方、原文は特定のJWT形式、署名Algorithm、60秒等の時刻許容値、DPoPを指定しない。

以下は実用上の解釈である。JWTの場合の検証はRFC 8725（BCP、2020-02）、
OAuth JWT Access Tokenの場合はRFC 9068（Standards Track、2021-10）を補足として参照する。
確認日は2026-09-08。特定Protocolの採用を本Controlの必須条件にはしない。

## Interpretation

**Agentの認証Tokenが偽造・改ざんされず、使える期間と対象・操作が必要範囲に限られることを、
発行側と受信側の両方で成立させる。**

購買Agentが見積APIを呼ぶ例では、見積読取のために全社のWrite/Admin権限を渡さない。
短い期限を設定しても受信側が期限を検証しなければ短命とはいえない。
署名が正しくても、別のIssuerや別API向けのTokenを受理してよいわけではない。

## Security objective

Credentialの窃取・Agent侵害時に利用可能な時間と権限範囲を縮め、
偽造・改ざん・異なる信頼領域での誤受理を防ぐ。
短命であっても盗まれたBearer Tokenは期限内に使われ得るため、Replay完全防止とは表現しない。

## Applicability

異なるSystemやIdentity管理領域の間で認証するAgentと、そのToken発行・検証経路に適用する。
同一組織内のAgent、Tool、下流API間でも対象になり得る。
Federationは、異なるIdentity管理元の証拠を信頼関係に基づいて受け入れる構成を指す。

### Non-applicability

System間認証がない単一Component内の処理やHuman認証だけの範囲では、理由を記録してN/Aとする。
名称をService Accountと呼ぶだけで、Agentに代わるSystem間認証を対象外にしない。

## Scope and assumptions

- 短命の最大値をTask、漏えい時の影響、更新・運用要件から定義する。原文に一律のTTLはない。
- Scopeは操作だけでなく、実装上必要なResourceや信頼領域の制限も含めて評価する。
- Claim名は方式依存。AudienceやTenant条件が必要な境界では、同等の信頼できるBindingを検証する。
- 署名済みであることと、正しい主体・Issuer・用途向けであることを分けて検証する。
- 不透明なTokenであっても、署名済みTokenを使用する要求を満たす根拠を必要とする。
  Introspectionがあるだけで任意の不透明Credentialを署名済みと扱わない。

## Assets, actors, identities, and trust boundaries

AssetsはAgent Credentialと、それによって利用できるAPI/Data/操作。
ActorsはAgent、発行者、受信API、鍵管理者、必要に応じた代理User。
境界は発行者からToken、Agentから受信API、受信APIから下流System。
JWTは署名されたClaimを運ぶ形式、Claimは主体や期限等の属性である。
受信側のVerifierが証拠を検証し、PEPが許可範囲を実操作へ強制する。

## Required security properties

| ID | 必要な性質 | 成立条件 |
|---|---|---|
| SP-1 | 有限で短い有効期間 | TaskとRiskに対応する最大期間があり、期限後は受理しない |
| SP-2 | 必要最小限のScope | 発行と利用の両方で、必要な対象・操作へ権限を限定する |
| SP-3 | 署名と信頼元の検証 | 許可された署名方式、Issuerに対応する鍵、Claimの整合を確認する |
| SP-4 | 境界ごとの独立検証 | 各受信先で用途・主体・期限・Scopeを確認し、上流での成功だけに依存しない |
| SP-5 | 検証不能時の拒否 | 未知の鍵や改ざん、期限不明等を未検証のまま受け入れない |

## Scope calibration and adjacent assurance

| 状況 | 評価 |
|---|---|
| 署名済みだが期限なし、または不要な全社Admin権限 | Fail |
| Tokenは短命だがAPIが期限を検証しない | Fail |
| 署名は検証するが、別の発行者に属する鍵を混用して主体を誤認する | Fail |
| 短命・最小Scope・署名検証されたBearerが窃取され期限内にReplayされる | 本要件だけの不成立とは限らない。Sender constraint等の追加保証を検討する |
| 正規Agentが許可Scope内で不正送金を要求する | 操作認可・意図・承認の別問題。Tokenの性質だけで安全とはいえない |
| 短命Tokenを継続更新できる | 更新だけでFailではない。発行時のScope等は守る。特権の常時取得はC5.2.6で別評価 |

Nonceを付けるだけでは署名済みTokenの盗用を止められない。
DPoPやmTLSによる送信者へのBindingは方式に応じた追加保証であり、
本要件の一般的なPass条件へ機械的に加えない。

## Threat and failure-mode rationale

攻撃者はTokenを取得した者、低権限Agent、別Issuerの正規Tokenを持つ者とする。
期限を越えて利用、Scopeを改ざん、別APIへ転用、Verifierの鍵選択を誤らせる経路を検証する。
発行者の鍵そのものの侵害まで、このToken形式だけで防げるとは仮定しない。
本改訂では、外部脅威IDのMappingは確定せず、上記の具体的失敗を根拠とする。

## Verification

### Architecture and configuration review

各Hopについて、発行者、信頼鍵、許可Algorithm、Lifetime、Scope、対象、主体の決め方を列挙する。
更新・交換・代理実行の経路と、それぞれの受信側Verifierを確認する。

### Positive verification

模擬Agentへ必要な読取Scopeの短命Tokenを発行し、意図したAPIだけで正規操作が成功することを確認する。
鍵Rotationを採用する場合、信頼できる更新後の鍵で正規処理が継続することも検証する。

### Negative and abuse-case verification

| ID | 試験 | 期待結果 |
|---|---|---|
| N-1 | 期限切れ、期限欠落、上限を超えるTokenを提示する | 拒否。設定した時刻許容も含め実効期限を確認 |
| N-2 | 内容改ざん、署名欠落、許可外Algorithm、未知の鍵を提示する | 検証不能なTokenを拒否 |
| N-3 | 正規署名だが別Issuer・別受信先・別Tenant向けのTokenを転用する | 境界で必要なBinding不一致を拒否 |
| N-4 | 読取TokenでWriteや未許可Resourceへアクセスする | 発行側・Resource側の双方でScope拡大を拒否 |
| N-5 | 更新・交換で元の権限より広いScopeを要求する | 新たな正当な権限根拠なしに拡大しない |
| N-6 | 信頼鍵を取得・検証できない状態で代替経路を試す | 未検証受理に切り替わらない。有効な信頼済み鍵のCacheは別扱い |

各試験で実操作が起きなかったことを確認する。Secretや本番Tokenを試験記録へ保存しない。

### Failure conditions

SP-1〜SP-5に反する発行・受理・操作成功は不成立。
TTLやScopeの必要性を説明できない、受信側が未確認の場合はPassの証拠不足として記録する。

## Evidence expectations

| Evidence class | Producer | Scope | Freshness | Integrity and sensitivity | Acceptance criteria |
|---|---|---|---|---|---|
| Hop別認証表 | Identity/API Owner | 全System間経路 | 接続先/信頼設定変更時 | Revision管理 | 各Verifierと用途制限が明確 |
| 発行・検証Policy | 発行者/受信側 | Lifetime、Scope、鍵、Algorithm | Policy/鍵変更時 | 公開鍵と設定のみ、秘密鍵は除外 | 必要最小範囲と短命の根拠がある |
| 正常・異常試験結果 | Test Harness | N-1〜N-6または同等 | 関連変更時・定期回帰 | 模擬TokenとBuild識別 | 不正TokenでDataや副作用を取得できない |
| Rotation/更新結果 | Identity運用者 | 発行・更新・交換 | 方式変更時 | 鍵IDとPolicy Revisionを相関 | 更新後も範囲・検証条件を維持する |

## Related requirements

- `v1.0-C5.1.1`: 高Risk操作のStep-up。Token更新と再認証を分ける。
- `v1.0-C5.2.1`: Resourceアクセスの明示的許可。
- `v1.0-C5.2.2`: Service権限とEnd-user権限を分ける検索・組立の強制。
- `v1.0-C5.2.6`: 特権が存在する期間の制限。Token単体の期限とは別。

## Known limitations and uncertainty

最小Scopeの粒度はTaskとAPI設計に依存する。署名は暗号化ではなくClaimの秘匿を保証しない。
正規Client内の侵害は、署名済みTokenやSender constraintだけでは止まらない。
Human Intent、操作の安全性、保管中のCredential保護は隣接保証として残る。
`verifiable`はArtifact成熟であり、製品試験の成功やEngineering Mappingを意味しない。

補足仕様: [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725.html)、
[RFC 9068](https://www.rfc-editor.org/rfc/rfc9068.html)。JWT採用時の検証に用い、
各方式固有のClaim名を全実装の必須条件にはしない。

## References

- [AISVS v1.0 C5 normative chapter](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C05-Access-Control-and-Identity.md)
- [同RevisionのAISVS Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C05-Access-Control/C05-01-Identity-Management-Authentication.md): 補足資料でありNormativeではない。

## Changelog

| Date | Change | Source or maintainer | Evidence |
|---|---|---|---|
| 2026-09-08 | 初版。解釈・適用境界・脅威・検証・証拠期待値を整備 | 固定RevisionのAISVS、Repository interpretation | 本文のSecurity Properties、試験、Evidence expectations。製品試験は未実施 |
