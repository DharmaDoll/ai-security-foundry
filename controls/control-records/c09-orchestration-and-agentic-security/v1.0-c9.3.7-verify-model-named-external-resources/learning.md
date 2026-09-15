# C9.3.7：Modelが示した外部Resourceを利用前に確認する

AISVS Verification Level: 2

[Control本文：解釈・検証・証拠・限界](README.md)

## 要件と資料の位置づけ

対象は`v1.0-C9.3.7`。採用済み固定Revisionは
`78775233666a2022dcfb82037e5e029116955c00`。

> Verify that external resources named in model output are verified against an approved allow-list or registry before the agent installs or invokes them.

日本語訳：Model出力で名前を挙げられた外部Resourceが、AgentによってInstallまたは呼び出される前に、
承認済みAllow-listまたはRegistryと照合されることを確認する。[要件本文][normative]

Normativeは要件本文、Researchは補足である。承認単位、実体解決、Supply-chain保証との境界は
Repository interpretation、対話からの整理は学習上の洞察である。学習完了はControl成熟度や製品適合を変更しない。

## 平易な説明

LLMは、実在しないPackage、Tool、MCP Server、URLをもっともらしく生成することがある。AgentがModelの名前を
そのまま信じて取得・実行すると、攻撃者が同名Resourceを登録して待ち受ける、別Resourceへ誘導する、または
許可済みRunnerの引数から任意Codeを実行する経路になる。

AIが幻覚したPackage名を攻撃者が取得する攻撃は、一般に`slopsquatting`と呼ばれる。

**Modelが挙げたResourceは利用候補であって、利用許可ではない。**

## 存在、人気、承認、安全性を分ける

次の性質は同じではない。

```text
Public Registryに存在する
  ≠ Organizationが利用を承認した
  ≠ Publisherや実体が期待どおりである
  ≠ 脆弱性や悪意がない
```

Download数、Star数、検索順位、Package名の自然さも、安全性や承認の証明にならない。Public Registryを
承認Registryとして使うなら、そのRegistryのどの範囲を、誰が、何の粒度で承認したかを定義する。

## 対象となるResource

- npm、PyPI、Maven等のPackage
- Container Image、Model、Adapter
- Git Repository、Script、Binary
- Plugin、Agent Skill、MCP Server
- 外部API、URL、Endpoint
- Command Runnerの引数から取得・起動されるResource

Modelが候補を人へ表示するだけで、取得・接続・実行へ使われない範囲は本要件の対象外とできる。

## 推奨するArchitecture

```text
Modelが生成したResource名
  ↓ 非信頼境界
Resource Resolver
  - Ecosystem・Namespace・Publisher
  - Version・Digest
  - Registry・Endpoint
  - Redirect後の実体
  を必要な粒度で解決
  ↓
承認済みAllow-list／Registryと照合
  ↓ 許可された場合のみ
Install／接続／実行
```

Security Invariantは、Modelが任意のResource名やURLを生成しても、承認されていない実体をAgentの環境へ
導入・接続・実行できないことである。決定論的なEnforcement Pointは、実際の取得・接続・起動の直前にある
Package Manager Proxy、Artifact Registry、MCP Gateway、Egress Proxy、Runtime Policy等である。

## 何を承認単位にするか

名前、Namespace、Publisher、Version、Digest、取得元、Endpointの全てを一律に必須とはしない。
対象のRiskと運用に応じて、承認の意味を明示する。

例えば、Organizationが意図的に「PyPI上の`approved-parser`は全Versionを利用可」と定義しているなら、
名前だけの照合でもC9.3.7のPass候補になり得る。ただし、悪意ある新版やPublisher侵害を防ぐ
Supply-chain完全性は別途必要である。

一方、複数Registryの同名Package、似たNamespace、Redirect先等を区別できない粒度では、実際に利用する
Resourceを確認したとはいえない。

```yaml
resource:
  ecosystem: pypi
  name: approved-parser
  version: 2.4.1
  digest: sha256:abc123...
  source: https://packages.example.com/simple
```

上記は強い識別の一例であり、全Systemへ同じFieldを要求するものではない。

## Wrapperではなく最終Resourceを見る

`npx`、`pip`、`docker`、Shell等のRunnerだけをAllow-listに登録しても、その引数から任意Resourceを取得できれば
実効的な制限にならない。

```text
承認済み：npx
実際に取得・実行：attacker-package@latest
```

同様に、最初のURLだけが承認済みでも、Redirect先から別Fileを取得して実行すれば不成立である。

**照合するのは入口の文字列ではなく、最終的に取得・接続・実行されるResourceである。**

## C9.3.7が保証しないこと

```text
C9.3.7
  Modelが未承認Resourceを勝手に選ぶ経路を防ぐ

Supply-chain integrity
  承認済みResourceの提供者・版・内容・依存関係が期待どおりか

Sandboxing／least privilege
  Resourceが侵害されても被害を制限できるか
```

承認済みResourceにも脆弱性、悪意ある更新、依存先の侵害はあり得る。Allow-listは安全性証明ではない。

## 検証と対話の再構成

**問い：Coding Agentは、PyPIに存在しDownload数が一万件以上のPackageなら、Organizationの承認一覧と
照合せず最新版をInstallする。適合するか。**

学習者：「Fail」

整理：そのとおり。存在と人気はOrganizationの利用承認ではなく、最新版は承認した実体の固定にもならない。

**問い：OrganizationはPackage名だけをAllow-listに登録し、Version、Digest、Publisherを固定せずPyPIから
最新版を取得する。適合するか。**

学習者：「Fail」

整理：必ずしもFailではない。全Versionを許可するという承認の意味が明確で、実際の取得先と名前を照合するなら、
C9.3.7のPass候補になり得る。ただし、内容変更に対するSupply-chain Riskが残る。理想的なHardeningと、
Requirementが最低限問う保証を混同しない。

**問い：`npx`だけがAllow-listにあり、Agentが指定した`attacker-package@latest`を引数の検証なしで実行する。
適合するか。**

学習者：「はい」

整理：これはFailである。`npx`はRunnerにすぎず、確認すべき外部Resourceは引数で取得・実行されるPackageである。
引数の認可という面ではC9.5.1とも隣接する。

**問い：Agentが示したPackageは、Organizationが管理し審査済みVersionだけを格納する内部Registryからしか
取得できない。未登録ならFail closedで拒否される。適合するか。**

学習者：「Fail」

整理：内部Registryが承認済みResourceの集合として機能し、迂回不能ならPass候補である。Applicationが別の
Allow-listを重ねて持つ必要はない。ただし、Registry管理権限、取得元の強制、Dependencyの扱いは確認する。

**問い：最初のAllow-list済みURLだけを照合し、そのURLから未承認HostへRedirectした先のFileを実行する。
適合するか。**

学習者：「Fail」

整理：そのとおり。最初の名前ではなく、実際の取得先とResourceを確認しなければならない。

## Negative Test

- 未承認名、類似名、別Namespace、別Registryを指定し、Install・接続・実行前に拒否されることを確認する。
- 許可済みRunnerの引数へ未承認Package、Image、Scriptを指定し、Runner名だけでは許可されないことを確認する。
- 承認済みURLから未承認HostへRedirectし、最終取得先の照合を回避できないことを確認する。
- Registryを利用不能または応答不正にし、有効な承認根拠なしでFail openしないことを確認する。
- Cache、Alias、Dependency、Fallback Registryを通じた別Resourceへの切替えを試す。

## 洞察と設計レビューへの問い

- Modelが名前を出せるResourceの種類と、実際に利用できる経路は何か。
- 承認Registryは単なるPublicな存在確認になっていないか。
- Allow-listの一項目は名前、版、提供者、Digest、Endpointの何を承認するのか。
- Wrapper、Runner、Redirect、Alias、Dependencyの先にある最終Resourceを追えているか。
- Registryが利用不能・不正な場合にFail closedするか。
- C9.3.7の承認確認と、Supply-chain完全性、Sandboxingを区別して評価しているか。

## References

- [AISVS v1.0 C9.3.7][normative]
- [対応Research][research]
- [C9 Family overview](../README.md)
- [C9学習ガイド](../../../docs/learning/c09-orchestration-and-agentic-security/README.md)

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md
[research]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C09-Orchestration-and-Agents/C09-03-Tool-and-Plugin-Isolation.md
