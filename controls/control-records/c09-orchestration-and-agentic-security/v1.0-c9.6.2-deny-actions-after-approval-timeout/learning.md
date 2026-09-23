# C9.6.2：期限切れの承認要求を復活させない

AISVS Verification Level: 2

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.6.2`。採用済みAISVS v1.0の固定Revisionは
`78775233666a2022dcfb82037e5e029116955c00`。

> Verify that when a human-approval gate is not satisfied within the defined approval time, the system blocks the pending action.

日本語訳：定められた承認時間内に人の承認条件が満たされない場合、Systemが待機中の操作を阻止することを確認する。
[要件本文][normative]

Normativeは期限内に承認されなかった操作の阻止を要求する。Researchは遅延承認・再試行・期限の正本を補足する。
[対応Research][research] 以下の返金・再申請はRepository interpretation、持ち帰る言葉は学習上の洞察である。
学習完了はControl成熟度・製品適合を変更しない。

## 返金要求の具体例

Agentが顧客への返金を提案し、人の承認を5分待つ。5分は例であり、要件が指定する時間ではない。
担当者が不在でも通知障害があっても、無応答を許可へ変えてはいけない。

```text
承認待ち → 期限内に有効な承認 → 他の実行条件も満たせば実行
         → 承認なく期限切れ   → 元の操作をブロック
```

承認Gateは承認が確認できるまで処理を止める関門。Timeoutは定めた待機時間の超過を指す。
資産は待機中の操作と承認状態。攻撃者が遅延承認・再送を利用して、停止済みの要求を実行へ戻す経路を考える。
Trust Boundaryは承認UI、承認サービス、Timer、Queue、実行処理の間にある。
Security Invariantは、期限内に承認されなかった元の要求を、遅れた承認や自動再試行で実行しないこと。
Enforcement Pointはアプリの期限・状態管理と、実行側の承認状態確認に置く。
モデルの「急ぎなので続行する」という判断で期限を無効にしない。

## 対話：古い通知から承認する場合

問い：5分で期限切れになった要求を、6分後に担当者が古い通知から承認する。
Systemは同じ要求を承認済みへ変更し返金する。

学習者：「No」

整理：正しい。期限切れの要求を遅延承認で復活させている。
期限を定めただけでなく、期限後に到着するイベントを受理する状態遷移まで制限する必要がある。

## 対話：新しい要求として再申請する場合

問い：元の要求はブロックしたまま再申請を案内し、新しい要求の内容・期限を確認して改めて承認を得る。
新しい承認までは返金しない。

学習者：「はい」

整理：成立する。再申請を許す業務仕様でも、古い承認を新しい要求へ流用しない。

> 無応答は承認ではない。遅れた承認で、期限切れの要求を復活させない。

## 検証・限界・レビューへの問い

Positive Testは、期限内の有効な承認により、対象の操作が他の認可条件も満たして実行されること。
Negative Testは無応答、期限後の承認、再送、自動再試行で副作用が起きないことを確認する。
期限切れ処理と承認の同時到着でも、定義した期限と受理順序を守ることを試す。

端末でボタンを押した時刻とサーバが承認を検証した時刻は同じではない。
起点、基準Clock、期限境界の判定を決め、クライアントの自己申告時刻だけで期限を回避させない。
待機・再開機能だけでは期限の強制にならない。

C9.2.1は高影響操作への承認、C9.2.8は承認と操作内容の結合・一回性を扱う。
本要件のTimeout制御だけでそれらを代替しない。

- 期限切れの元要求はどの状態になり、実行側がどう確認するか。
- 遅延承認・再試行・Queueから復活しないか。
- 再申請は新しい要求として扱い、古い承認を流用しないか。
- 期限境界の競合でも無承認の実行が起きないか。

## References

- [AISVS v1.0要件本文][normative]
- [対応Research][research]
- [C9 Family overview](../README.md)
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-06-Shutdown-Graceful-Degradation.md
