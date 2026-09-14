# C9.3.3：ToolのSecurity契約をManifestへ明示する

AISVS Verification Level: 2

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.3.3`。採用済み固定Revisionは
`78775233666a2022dcfb82037e5e029116955c00`。

> Verify that tool manifests declare required privileges, resource limits, and output validation requirements.

日本語訳：Tool Manifestが、必要な権限、資源制限、出力検証要件を宣言していることを確認する。[要件本文][normative]

Normativeは要件本文、Researchは補足である。文書変換Toolの例、保証境界、隣接要件との整理は
Repository interpretation、対話からの整理は学習上の洞察である。学習完了はControl成熟度や
製品適合を変更しない。

## 具体例と用語

Manifestは、Toolが何者で、何を必要とし、どのような契約で動くかを機械または管理者が確認できる形で
宣言した情報である。単なる名前、説明、入力Schemaだけでは、本Requirementが求めるSecurity契約に
ならない。

例えば文書変換Toolなら、少なくとも次のような情報をToolのVersionと対応付ける。

| 宣言するもの | 具体例 | 宣言から確認したいこと |
|---|---|---|
| 必要な権限 | 指定されたPDFのRead、一時領域へのWrite、外部Network接続なし | 暗黙の広い権限を必要能力として扱っていないか |
| 資源制限 | 実行30秒、Memory 512 MB、入力100 MBまで | 無制限な実行や資源消費を前提にしていないか |
| 出力検証要件 | 成功・失敗応答のSchema、最大Size、未知Fieldの拒否 | Consumerが何を検証してから出力を利用するか |

「安全なTool」「必要な範囲でFileへアクセスする」のような自然言語だけでは、欠落、矛盾、過剰要求を
機械的・一貫的に判定できない。標準Manifest形式が存在しなくても、Repository固有のSchemaや登録契約で
必要事項を表現できるため、形式が未標準であることは未宣言の理由にならない。[Research][research]

## 保証境界と隣接要件

資産は、採用判断と実行制限の基準になるToolのSecurity契約である。主なTrust Boundaryは、Tool作者の
自己申告と、Toolを採用・登録・実行する側との間にある。Security Invariant（守るべき性質）は、登録対象の
ToolとVersionについて、権限、資源上限、出力検証要件が欠落や曖昧さなく追跡できることである。

C9.3.3の直接的なEnforcement Point（強制点）は、ManifestのSchema検証、登録審査、Tool Registryへの
Admissionである。Runtimeで実権限を制限すること自体はC9.3.4の中心となる。

| Requirement | 主に問うこと |
|---|---|
| C9.3.1 | 実行時の権限や隔離が実際に最小化されているか |
| C9.3.2 | Tool出力を利用前にSchema検証しているか |
| C9.3.3 | 必要な権限・資源上限・出力検証要件がManifestに明示されているか |
| C9.3.4 | Manifestに宣言した制約をRuntimeが実際に強制しているか |

したがって、Manifestが完全でも、実行環境が宣言を無視すればSystemは安全ではない。反対にRuntime設定が
偶然正しくても、対応する宣言がなければ、採用審査、変更差分、回帰試験、構成Driftの検出を安定して行えない。

## 「署名済みManifest」が保証する範囲

Manifestへの署名は、誰が発行したか、署名後に改ざんされていないかを確認する手段になり得る。しかし、
署名は宣言内容の正しさや最小性を証明しない。過剰な権限を正直に宣言したManifestも署名できる。

このためC9.3.3単独の保証は限定的である。それでも明示的な契約には、次の用途がある。

- 採用前に必要能力をレビューする。
- Version更新時に権限・上限・出力契約の差分を検出する。
- 登録時に必須Fieldや許容Policyを機械検証する。
- 宣言からRuntime設定やNegative Testを生成・照合する。
- 宣言と実行構成のDriftを発見する。

**C9.3.3の本質は、宣言だけでToolを安全にすることではない。制限を強制・検証できるよう、Toolが必要とする能力を明文化することである。**

## 検証と対話の再構成

Negative Test（不正や失敗条件を意図的に試す検証）では、権限、資源、出力検証の各宣言を欠落させる、
Toolだけを更新してManifestのVersionを残す、Read-onlyとWriteを矛盾して記載する、上限を曖昧な自然言語に
置き換える、といった条件を試す。不完全なManifestが採用・登録段階で検出されることを確認する。

**問い：Manifestには名前、説明、入力Schemaしかない。一方、Runtimeでは管理者が権限、Timeout、
出力検証を正しく設定している。C9.3.3に適合するか。**

学習者：「No」

整理：そのとおり。Runtimeの制御が有効でも、必要な3種類のSecurity要件がManifestに宣言されていないため、
C9.3.3はFailとなる。Runtime制御の有効性と、契約の明示性を混同しない。

**問い：ManifestはNetwork接続なし、Memory 512 MB、実行30秒、出力Schemaを宣言する。しかしRuntimeは
Manifestを無視し、外部Network接続も許可する。C9.3.3とC9.3.4をどう評価するか。**

学習者：C9.3.3は適合し得るが、C9.3.4はFailと判断した。

整理：そのとおり。C9.3.3の宣言要件だけを見ればPass候補だが、C9.3.4のRuntime強制はFailであり、Systemは
安全ではない。「Manifestに書いてある」を「実際に制限されている」と読み替えてはいけない。

**問い：署名されたManifestでも宣言内容が正しいとは限らず、単独の制限が弱いのに、なぜこのRequirementが
存在するのか。**

整理：宣言は強制の代替ではなく、強制・審査・検証の入力となる契約だからである。契約がなければRuntimeや
管理者は必要制限を推測するしかなく、Version更新や構成Driftも追跡しにくい。一方、宣言だけを成熟の証拠に
するとCompliance appearanceへ陥るため、隣接する保証と組み合わせて評価する。

## 実装では一体化し、Controlでは境界を残す

学習者は、C9.3.3とC9.3.4を一緒に扱ってもよいのではないか、また活発に議論されているAISVSの今後の更新に
期待すると述べた。この感覚は実装・運用上妥当である。例えば次の一つのPipelineとして構築できる。

```text
Manifest登録
  -> 必須宣言の検証
  -> 採用Policyによる審査
  -> Runtime制約の生成・適用
  -> 宣言と実構成のDrift検出
```

ただしRepositoryのControl recordは、固定した上流RequirementへのTraceabilityを保つため分離する。
分離により、「宣言が欠落・曖昧」と「宣言はあるが強制されない」という異なるFailureを診断できる。
将来の学習マップやEngineering Patternでは、両者を「Tool契約を実行時制約へ結び付ける」という一つの設計問題として
扱える。上流が変わった場合は意味差分を確認してから反映し、現時点の推測でRequirementを統合しない。

## 洞察と設計レビューへの問い

- ManifestがToolの特定Version・実行物と結び付いているか。
- 権限、資源、出力検証の3領域を、欠落判定できる形で宣言しているか。
- 宣言された権限が必要最小限かを別途レビューしているか。
- 宣言からRuntime制約を生成または照合し、Driftを検出しているか。
- 署名を、宣言内容の正しさやRuntime強制の証拠と誤認していないか。
- C9.3.3だけのPassをSystem全体の安全性として報告していないか。

## References

- [AISVS v1.0 C9.3.3][normative]
- [対応Research][research]
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-03-Tool-and-Plugin-Isolation.md
