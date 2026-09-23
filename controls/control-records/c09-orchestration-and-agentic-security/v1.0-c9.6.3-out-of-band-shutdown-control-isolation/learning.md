# C9.6.3：Agentが無効化できない経路から停止を強制する

AISVS Verification Level: 3

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.6.3`。採用済みAISVS v1.0の固定Revisionは
`78775233666a2022dcfb82037e5e029116955c00`。

> Verify that kill-switch commands are implemented through an out-of-band channel that is isolated from the agent runtime.

日本語訳：Kill-switchの指示が、Agent Runtimeから隔離されたOut-of-band経路を通じて実装されていることを確認する。
[要件本文][normative]

Normativeは停止指示経路の隔離を要求する。Researchは別資格情報・管理API・強制点を含む実効的な独立性と、
迂回経路の試験を補足する。[対応Research][research]
以下のContainer・Controller・SSFの例はRepository interpretation、対話から得た整理は学習上の洞察である。
特定製品やProtocolを必須にしない。学習完了はControl成熟度・製品適合を変更しない。

## 具体例と用語

Out-of-bandは、停止対象の通常実行経路から独立した管理経路を指す。
Agentが侵害・暴走した場合でも、Agent自身の協力を待たず、人が実行基盤側で停止を強制する。

```text
運用者 → 独立した管理API → 停止Controller → 実行基盤がAgentを停止
                                      ↑
                         Agentには管理権限を与えない
```

停止Controllerは停止指示を受けて基盤の強制点を操作するComponent、Control Planeは配置・権限・停止などを
管理する面、RuntimeはAgentが通常の仕事を実行する環境である。

攻撃者はAgent Runtimeを侵害し、自身の停止関数・Policy・資格情報・通信経路を無効化しようとする。
資産は人の停止権限と停止経路。Trust BoundaryはAgent Runtimeと管理経路・資格情報・基盤の強制点の間にある。
Security Invariantは、Agent Runtimeの権限だけでは停止命令を遮断・変更・偽装できず、Agentの協力なしに停止できること。
Enforcement PointはAgent Processの外側にある実行基盤、Network、Credential、Scheduler等の制御となる。

C9.6.1は推論と出力が実際に止まるかを問う。C9.6.3は、その停止指示と強制手段をAgentから守れるかを問う。
C9.1.3の対象はAgent群全体の停止範囲である。

## 対話：Containerを分けるだけでよいか

問い：停止Controllerは別Containerにあるが、Agentの管理TokenでControllerを削除し、停止Policyも変更できる。

学習者：「No」

整理：正しい。配置が別でも、Agentの実効権限で停止機構を無効化できるなら隔離されていない。
別UI、別Process、別Hostという見た目だけで判断せず、管理権限と到達可能な経路を確認する。

## 対話：独立した管理経路から停止する場合

問い：Controllerは独立した管理権限で動き、Agentは資格情報・設定・配置を変更できない。
通常のAgent APIが応答しなくても、運用者は別経路から実行基盤へ指示し、Agentの協力なしに停止できる。

学習者：「はい。Shared Signals Framework（SSF）を使うイメージでしょうか？」

整理：説明された構成は停止経路の独立性を満たし得る。SSFは複数SystemへSecurity Eventを配送する選択肢だが、
それ自体はProcessや推論を停止しない。

| 仕組み | 役割 |
|---|---|
| SSF | 協力するSystem間で署名されたSecurity Eventを配送する枠組み |
| CAEP | Session失効やToken属性変更など、継続的アクセス評価用Eventを定義するProfile |
| 停止Controller | Eventまたは管理指示を検証し、対象実行を基盤側で停止する実装 |

構成例は次のとおり。

```text
運用者がSessionを失効
  → SSFでCAEP Eventを配信
  → Agent外のControllerがEventを検証
  → 対象Sessionに対応する実行・出力・権限を停止
```

最後の対応付けと停止強制はSystem側で実装する。Token失効だけでは進行中の計算・Queue・委任済みWorkerが
止まらない場合がある。EventをAgent自身に渡して自主終了を期待する構成も、侵害Agentが無視できるため不足する。
[SSF 1.0][ssf]、[CAEP 1.0][caep]

一つの基盤内ならSSFを使わず、独立した管理APIから実行基盤へ直接停止を命じてもよい。
SSFは複数サービスへの失効情報の共有に向く選択肢であり、本要件の適合条件ではない。

> 停止Eventを届けることと、停止を強制することは別です。

## 検証と保証の境界

Positive Testでは、Agentの通常APIが応答しない状態でも、独立経路から対象の実行が停止することを観測する。
Negative Testでは、侵害Agent相当の権限から次を試す。

- 停止Controller、Policy、管理資格情報を取得・変更・削除する。
- 直接Tool、Queue、委任Worker、別Network経路から処理を継続する。
- 古いTokenやCache済み権限で停止後に再開する。
- Control Planeが受付済みと表示しても、最終的な強制点で止まっていない状態を作る。

Agentにそれらの変更権限がなく、迂回経路も停止または認可拒否されることを確認する。
停止受付時刻だけでなく、最も遅い強制点での停止時刻を測る。Event配送・失効伝播・Cacheには遅延があり、
Control Planeの応答時間を全体の停止時間として報告しない。

本要件だけで、管理者資格情報の侵害、管理基盤全体の障害、既に確定した外部副作用の取消しまで保証しない。
復旧・再開にも独立した認可を設け、Agentが自分で復旧できないことを確認する。

## 設計レビューへの問い

- Agent Runtimeを侵害した主体が、停止用の鍵・API・Policy・配置を変更できないか。
- 通常経路が妨害されても、別経路から最終強制点まで指示が届くか。
- Queue、委任先、別通信経路、Cache済み資格情報が停止後も残らないか。
- Eventの受領と実際の停止を別々に観測できるか。

## References

- [AISVS v1.0要件本文][normative]
- [対応Research][research]
- [OpenID Shared Signals Framework 1.0][ssf]
- [OpenID CAEP 1.0][caep]
- [C9 Family overview](../README.md)
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-06-Shutdown-Graceful-Degradation.md
[ssf]: https://openid.net/specs/openid-sharedsignals-framework-1_0.html
[caep]: https://openid.net/specs/openid-caep-1_0.html
