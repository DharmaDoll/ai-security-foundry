# C9.5.6：開始時の許可を、現在の許可と混同しない

AISVS Verification Level: 3

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.5.6`。採用済みAISVS v1.0、固定Revision
`78775233666a2022dcfb82037e5e029116955c00`を使用する。

> Verify that long-running agent sessions re-evaluate current backend authorization policy on every privileged action.

日本語訳：長時間実行されるAgent Sessionが、特権操作のたびに現在のBackend認可Policyを再評価することを確認する。
[要件本文][normative]

Normativeは各特権操作での現在Policyの再評価を要求する。Researchは期限内Token、既存接続、Queueや再開処理に
古い権限が残る問題と検証方法を補足する。[対応Research][research]
以下の業務例と構成案はRepository interpretation、取引確定や運用上の考察は対話からの洞察である。
学習完了はControl成熟度・製品適合を変更しない。

## 具体例と用語

```text
09:00 Aliceに請求書の更新権限あり。Agentが作業開始
10:00 管理者がAliceの更新権限を取消し
10:05 Agentが次の請求書を更新しようとする
```

特権操作は、この例では保護された請求書の変更。実際の対象はSystemごとに定義する。
Policyは許可条件、Cacheは照会結果等の一時保存、Queueは後から実行する仕事の待機場所である。
攻撃者が取消し前のTokenや継続Sessionを使い、失った更新権限を行使する経路を考える。
資産は現在の認可状態と請求書。Trust BoundaryはPolicy正本・Cache・長時間実行基盤・操作APIの間にある。

Security Invariantは、期限内Token・既存接続・再開を理由に失効済みの許可を使い続けないこと。
Enforcement Pointは各特権操作の実行前の認可処理。
Tokenの署名・期限検証だけでは発行後の権限変更を知れない。C9.4.3の資格情報の定期更新とも異なる。

## 対話：Tokenの期限が残っている場合

問い：Tokenは12時まで有効。10時に更新権限を取り消したが、署名と期限だけを検証し、発行時のwrite権限で
10時5分の更新を許可する。

学習者：「No」

整理：正しい。Tokenの有効性と、今も操作を許可されていることを混同している。

## 対話と説明の訂正：Queue登録と取引確定

問い：9時に認可してQueueへ登録し、10時の権限取消し後、10時5分にWorkerが再評価して拒否する動作は要件に沿うか。

学習者：「はい。ただし要件による。許可を認めた時間が取消し前なら、その限りではない場合がある。」

訂正：問いはQueueへ何を登録したかを明確にすべきだった。

- 未実行の依頼なら、これから利用者の権限で行う操作を現在Policyで評価する。
- 受付時に取引が確定し、後続がその履行なら、利用者の権限取消しで取引を取り消すかは業務仕様による。

後者は、後続処理の主体・権限・確定時点を明示し、現在Policyで履行を許可する必要がある。
「以前許可した」という理由だけで前者を確定済み扱いにしない。

> 権限の取消しと、確定済み取引の取消しは同じではない。

## セッション管理が必要ということか

学習者：「Tokenに基づく認可だけでなく、セッション管理をどこかで行う認識でよいか？」

整理：必要なのは発行後の権限・失効状態の変化を実行時判断へ反映すること。従来型のSession管理は一つの方法だが、
Sessionが有効なまま更新権限だけ取り消されることもある。「まだログイン中」と「今この操作をしてよい」は別である。

## 権限変更を反映する具体的な方法

学習者：「発行後の変更を実行側へ届ける仕組み。具体的には何？」

### 実行時に問い合わせる

管理者が権限DBを更新し、APIが各操作でそのDBや認可サービスへ照会する。
TokenはAliceの識別に使い、現在のPolicyで対象請求書への更新を評価する。
JWT自体を変更したりAgentへ取消しを通知したりする必要はない。

Token Introspectionは認可サーバへTokenの現在の有効状態などを問い合わせる標準方式である。
ただし権限変更が発行側の状態へ反映されていなければ、照会しても有効のままになり得る。
active=trueだけで対象Resourceへの操作が許可されるとも限らない。[RFC 7662][introspection]

### 変更を通知する

```text
権限DBを更新 → 変更イベントを配信 → APIの古い許可Cacheを無効化 → 次の操作で再評価
```

OpenID CAEPはShared Signals Framework上でSession失効・Token属性変更等のイベントを定義する。[CAEP 1.0][caep]
通知が遅延・欠落すれば古い許可が残るため、受信状態・再同期・現在性が不明なときの拒否を設計する。
通知方式というだけで即時反映を主張しない。

## 可用性と性能のトレードオフ

学習者：「両方やるに越したことはないが、可用性やパフォーマンスを考えた実装が現実的か。」

整理：必要な変更反映速度を決める。ただし方式を二つ入れるだけで安全になるわけではなく、状態の不一致や
通知漏れへの対応も増える。例えば通知をCache無効化・Session停止の早期化、実行時照会を最終判断に使う分担がある。
通知漏れを照会で補える一方、照会先障害時は特権操作の保留・拒否という可用性への影響が残る。

「性能のため古いAllowを5分使う」と「現在Policyを再評価する」は同じではない。
短いCache期限は影響時間を減らすが、それだけで今回の保証を満たしたとはいえない。
Cacheを使う場合は現在性を確認できる条件と実測した伝播遅延を明示する。

> 認可の設計では、誰に何を許すかに加えて、権限変更がいつ実行へ反映されるかを決める。

## 検証・限界・レビューへの問い

Positive Testは、継続中のAgentが現在も許可されている操作を成功させること。
Negative Testでは期限内Tokenを保ったまま権限を取り消し、次の特権操作が拒否されるか確認する。
Queue、再開、既存接続も同じ観点で試し、通知停止や認可基盤障害で古いAllowへFallbackしないか検証する。

既に確定した操作の取消しや、全Systemで遅延ゼロの失効まで本要件だけで保証しない。
検査から実行までの競合も、実際の更新境界と整合性設計で評価する。

- 取消しを確定する場所と、実行前に確認する場所はどこか。
- 権限変更はCacheやWorkerへいつ反映されるか。
- 現在性を確認できない場合に何を停止するか。
- Queue登録は未実行依頼か、確定済み取引の履行か。

## References

- [AISVS v1.0要件本文][normative]、[対応Research][research]
- [OAuth Token Introspection：RFC 7662][introspection]
- [OpenID CAEP 1.0][caep]
- [C9 Family overview](../README.md)
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-05-Agent-Authorization-Delegation.md
[introspection]: https://www.rfc-editor.org/rfc/rfc7662.html
[caep]: https://openid.net/specs/openid-caep-1_0.html
