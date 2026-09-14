# C9.2.10：行動連鎖の最も高い影響を承認へ反映する

AISVS Verification Level: 3

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.2.10`。採用済み固定Revisionは
`78775233666a2022dcfb82037e5e029116955c00`。

> Verify that approval gates for multi-step or multi-agent action chains enforce the highest-impact reversibility classification present anywhere in the chain.

日本語訳：複数段階または複数Agentからなる行動連鎖の承認Gateが、その連鎖のどこかに含まれる
最も影響の大きい可逆性分類を強制することを確認する。[要件本文][normative]

Normativeは要件本文、Researchは補足。具体例と動的計画への翻訳はRepository interpretation、
対話からの整理は学習上の洞察である。学習完了はControl成熟度や製品適合を変更しない。

## 具体例と位置づけ

「退職者アカウントを整理する」というTaskが、情報参照、記録保管、アカウントと保存Dataの
完全削除に分かれているとする。表面のTask名や前半の処理は低Riskに見えても、連鎖には
不可逆な削除が含まれる。連鎖全体を低い分類のまま承認させてはならない。

| Requirement | 問う範囲 |
|---|---|
| C9.2.4 | 個々の操作で、可逆性分類に応じた制限を強制するか。 |
| C9.2.10 | 多段・複数Agentの連鎖のどこかにある最大影響を、承認Gateへ反映するか。 |

高影響操作を無害なWrapperや子Taskへ隠す、または小さな操作へ分割することで、承認条件を
下げられないようにする。Researchは子操作への隠蔽、委任時の分類喪失、動的計画を補足する。
[Research][research]

## 脅威・信頼境界・強制

攻撃者や誘導されたAgentが、危険な操作を低RiskのTaskへ内包し、親Agentや承認者から見えなくする。
保護対象は計画、委任Context、操作分類、承認範囲と実際の副作用である。

Trust Boundary（信頼境界）は親子Agent、Orchestrator、Tool、承認Gateの間。
Security Invariant（守るべき性質）は、操作の分割・入れ子・委任・計画変更によって、連鎖に必要な
承認水準を下げられないこと。Enforcement Point（強制点）は、子操作を含む計画の分類を集約し、
承認範囲との一致を実行前に確認するOrchestratorと各実行境界である。

## 動的計画と検証

Agentが実行途中で次のStepを決める場合、開始時に未来の全操作を完全に把握できないことがある。
その場合は、許可可能な能力を先に限定し、高影響操作が追加された時点で実行前に停止・再評価・
再承認する。最初から全処理を最大水準で承認する方式だけが適合方法ではない。

Negative Test（不正や失敗条件を意図的に試す検証）では、低Risk Wrapper内の不可逆操作、
子Agentへ渡す分類の欠落・引下げ、承認後の高影響Step追加を試す。連鎖ID、子操作、分類、
承認対象、再評価時刻、実結果を対応付ける。

各操作の分類の最大値だけで、操作同士の組合せによる新しい影響を常に説明できるわけではない。
個別には可逆な二つの変更が、組合せによって復旧不能になる場合は、複合的な影響を別途評価する。

## 対話の再構成

**問い：読み取り中心の計画を承認した後、不可逆な削除を追加した。古い承認を使って削除まで
実行する構成は適合するか。**

学習者：「No」

整理：最大影響が変わった時点で、変更後の連鎖を再評価し、削除を正確に示して必要な承認が
得られるまで阻止する。

**問い：当初は読み取りだけを低い条件で開始した。途中で不可逆な削除が計画されたため、
その場で停止し、変更後の計画への高い承認を得て再開した。この動作は要件に沿うか。**

学習者：「Yes」

整理：そのとおり。未来の全Stepを開始時に予測することではなく、高影響操作を実行する前に
連鎖を再評価し、必要な承認へ引き上げることが重要。ただし、すでに実行した操作との組合せで
新しい危険が生じないかも確認する。

学習者は追加の質問をせず、次への進行を求めた。

## 洞察と設計レビューへの問い

個々の操作を正しく制御しても、連鎖として見ると高い影響を見落とすことがある。

- 親Task、子Agent、Tool呼出しを一つの連鎖として追えるか。
- 委任境界で分類や承認範囲が失われていないか。
- 承認後に計画が変わったとき、旧承認を流用していないか。
- 個々の可逆性だけでなく、操作の組合せが生む影響を確認したか。

## References

- [AISVS v1.0 C9.2.10][normative]
- [対応Research][research]
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-02-High-Impact-Action-Approval.md
