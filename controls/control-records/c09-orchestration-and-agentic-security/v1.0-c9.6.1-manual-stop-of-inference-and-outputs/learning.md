# C9.6.1：停止した対象と、その証拠を確認する

AISVS Verification Level: 1

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.6.1`。採用済みAISVS v1.0、固定Revision
`78775233666a2022dcfb82037e5e029116955c00`を使用する。

> Verify that a manual kill-switch mechanism exists to immediately halt AI model inference and outputs.

日本語訳：AIモデルの推論と出力を直ちに停止する、手動のKill-switch機構が存在することを確認する。
[要件本文][normative]

Normativeは推論と出力の手動停止を要求する。Researchは表示だけの停止との違い、遅延の計測、安全状態を補足する。
[対応Research][research] 以下のチャット・外部Provider例はRepository interpretation、証拠の区別は学習上の洞察である。
学習完了はControl成熟度・製品適合を変更しない。

## 具体例と用語

Agentが機密情報を回答へ出し始めたとする。権限のある運用者が異常を認識したら、生成と配信を止めて被害を限定したい。
Kill-switchは人が作動させる緊急停止機構、推論はモデルが回答等を生成する処理、Streamは結果を逐次配信する経路を指す。

```text
人が停止を指示 → 実行基盤が推論を中断 → 出力配信も遮断
```

攻撃者がモデルを有害な出力へ誘導した場合でも、停止をモデルの同意や「停止してください」というPromptに依存させない。
保護対象は推論の実行と出力先。Trust Boundaryは停止操作からRuntime、外部Provider、各配信先への制御にある。
Security Invariantは、停止指示後も対象の推論・出力を通常完了まで継続させないこと。
Enforcement Pointは実行制御・取消し処理と出力配信処理である。

「直ちに」の一律の秒数は本文にない。用途の危険分析から目標を定め、実際の停止遅延を負荷・部分障害下でも測る。
機密性だけでなく、異常な生成の継続による影響を人が止めるための保証である。

## 対話：画面だけ停止する場合

問い：停止ボタンでブラウザの回答表示は止まるが、Backendは生成・保存を続け、別の購読先にも配信する。

学習者：「No」

整理：正しい。表示が止まっただけで、推論も出力配信も継続している。
UIの変化ではなく実行状態と全対象出力経路を確認する。

## 対話：外部Providerの推論停止が分からない場合

問い：外部LLM APIへの接続を切り、以後の出力を全て遮断する。ただしProvider側の推論終了を確認できない。
完全に要件を満たしたと断定できるか。

学習者：「No」

整理：正しい。出力遮断の証拠はあるが、推論停止は未確認である。
「推論が続いていると実証されたFail」と「停止を裏付ける証拠不足」を区別して残す。
Providerの取消し仕様・実行状態・責任分界を確認し、単なる接続切断から終了を推測しない。

> 停止ボタンの存在ではなく、停止した対象と、その証拠を確認する。

## 検証と保証の境界

Positive Testでは、実行・配信中に正規の停止を行い、指示時刻、最後の出力、推論終了時刻、停止後の状態を観測する。
Negative Testでは表示だけの停止、別配信先の継続、停止依存先の障害を確認する。
停止したと思った処理が自動再試行で再開しないことも確認する。

C9.1.3はAgent群全体の停止、C9.6.3は停止指示経路の隔離を扱う。
本要件の停止機構があることだけで、その経路の侵害耐性まで証明しない。
下流へ既に送った操作の取消しや確定済み副作用の復旧も、推論停止と同じ保証ではない。
Researchの依存処理取消し・安全状態の確認は運用上の補足として扱い、成立した範囲を明示する。

## 設計レビューへの問い

- 人が押したとき、推論とどの出力経路が止まるか。
- 接続切断とProvider側の実行終了を混同していないか。
- モデルが応答しなくても停止できるか。
- 停止遅延と未確認範囲を証拠として示せるか。

## References

- [AISVS v1.0要件本文][normative]
- [対応Research][research]
- [C9 Family overview](../README.md)
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-06-Shutdown-Graceful-Degradation.md
