# Controls Learning Documentation

この文書は、AISVSのすべてのCategory／Familyで共通して使用する学習方法と、学習結果を
永続ドキュメントへ変換する方法を定める。

## Purpose

学習の目的は、Requirementを暗記することではなく、Security責任者として次を説明し、
設計判断へ使える状態にすることである。

- Requirementが守ろうとしているAssetとSecurity Property。
- 想定するPrincipal、Attacker Capability、Trust Boundary、Abuse Path。
- Security Invariantと、決定論的に守らせるEnforcement Point。
- 具体的なPass／Failと、その判定根拠。
- Requirementが保証する範囲と、隣接する保証の境界。
- Normative textを超えて推奨する設計と、それが追加保証である理由。

説明を平易にすることは、Security上の前提、攻撃者能力、例外、または保証範囲を省略
することではない。用語をかみ砕きながら、設計レビューに必要な厳密さを維持する。

## Boundaries

学習ドキュメントは、次のArtifactとは独立して扱う。

- `control-records/`のControl本文。
- `catalog.yaml`のControl maturity。
- `mappings/`のMapping assessment。
- 製品またはSystemの適合評価とProduction Evidence。

学習の完了によってControl maturityを上げてはならない。Controlが`verifiable`でも、
学習済みとはみなさない。学習中に得た洞察をControlへ反映する場合は、別のControl変更
としてSource、Scope、Verificationへの影響を確認する。

## Required sources

各Requirementの講義を作る前に、少なくとも次を読む。

1. `sources/registry.yaml`に登録されたSourceのVersionとStatus。
2. 固定RevisionのAISVS Normative Requirement。
3. 同じRevisionに対応するAISVS Research page。
4. Security-significantな解釈に必要なPrimary specificationまたは公式Guidance。

Normative Requirement、Research、Repository interpretation、学習から得た洞察を混同
しない。学習ノートでは次の役割を明示する。

- **Normative:** AISVSが実際に要求していること。
- **Research:** 脅威、検証例、実装上の注意、未解決事項を補足する情報。
- **Repository interpretation:** 現場のArchitecture Reviewへ適用するための解釈。
- **Derived insight:** 質疑や比較から得られた、Requirement外を含むSecurity上の洞察。

Researchの具体例や製品設定を、そのままNormativeなPass条件へ昇格させない。Currentな
製品、Protocol、Frameworkへ依存する主張はPrimary sourceで確認し、Draft、Rolling、
Stable等のStatusを必要に応じて記録する。

## Teaching stance

講義は、Security経験の浅い読者へ単語を説明しながら、Senior Product Security
EngineerがArchitecture Reviewを行う視座で構成する。

- 必ずRequirement原文から開始し、途中で学習対象を見失わせない。
- まずActor、Data、Actionが見える一つの具体Scenarioを最後まで追い、その後で
  Security Invariantへ抽象化する。抽象概念だけを先に提示して理解を要求しない。
- 数式、集合記号、略語、Protocol固有のClaim名を初めて使う前に、平易な言葉と
  Scenario内の具体例で意味を説明する。記号を使う場合も、同じ内容を自然言語で併記する。
- `sensitive`、`high-risk`、`appropriate`等、組織やContextによって境界が変わる用語は、
  例を列挙するだけで終わらせない。Upstreamが定義する範囲と定義していない範囲を示し、
  Repository interpretationとして実際のPass／Fail判断に使えるOperational definitionを
  置く。
- 「未認証の攻撃者」だけでなく、盗まれたSession、正規の低権限Tenant、侵害された
  Agent、悪意あるData、内部者など、Requirementに適したAttacker Capabilityを置く。
- Controlの存在ではなく、守るべきOutcomeが成立するかを説明する。
- ModelやAgentの判断を、決定論的なAuthentication／Authorization Boundaryとして
  扱わない。
- PassしたRequirementとSystem全体の安全性を同一視しない。
- AISVSが個別理由を示していない場合は、事実ではなくRepository上の推論と明記する。
- 学習者の疑問、誤答、判断不能は評価に使わず、講義またはScope説明の不足を発見する
  Signalとして使う。

## Learning workflow

Category／Familyごとに全Requirementへ一度触れる。一度に扱うのは一つのRequirement
だけとする。

1. Category全体の目的とRequirement一覧を確認する。
2. Normative Requirement、Research、必要なPrimary sourceを読む。
3. 下記の共通構造で講義する。
4. 原則2〜3問の短い対話で、本質または分かりにくい境界だけを確認する。
5. 有益な対話になった場合、Requirement単位の学習ノートへ永続化する。
6. Family guideのChecklistと次のRequirementだけを更新する。
7. Familyを一巡した後、再利用可能な洞察をControl、Template、AGENTS.md、または別の
   Guidanceへ反映すべきかを検討する。

すべてのSecurity PropertyやCaseを質問形式でなぞらない。理解の中心は講義本文に置く。
用語暗記やFramework自体の採点を目的にしない。

## Required lecture structure

各講義は必ず次の順で始める。

### 1. Normative Requirement

- Versioned Requirement ID。
- AISVS Verification Level。
- AISVSの英語原文。
- 意味を崩さない日本語訳。

短いRequirement単位の引用としてSourceと固定Revisionを示す。Research pageやChapterを
大量にコピーしない。

### 2. Categoryにおける位置づけ

Category全体の中で何を扱うRequirementか、隣接するAuthentication、Authorization、
Isolation、Integrity、Detection等とどう異なるかを説明する。

### 3. Security ObjectiveとScenario

保護対象、Principal、System、Data、Action、侵害時のImpactが見えるScenarioを一つ
以上示す。抽象的な「AI System」だけで説明しない。

### 4. 用語

初めて出る専門用語は、平易な日本語、正式な英語名、Scenario内の位置を示す。別の
Requirementで説明済みでも、学習ノート単独で理解するために必要なら再度説明する。

### 5. Threat ModelとAbuse Path

Attackerが何をすでにControlし、どのTrust Boundaryを越え、何を達成するかを示す。
単に「漏えいする」「改ざんされる」で終わらせない。

### 6. Security InvariantとEnforcement

誰が、何に対して、何をしてはならないかをSecurity Invariantとして表し、どの
Enforcement Pointが決定論的に守るかを説明する。

### 7. Pass／FailとScope Calibration

最低一つのPassとFailを示す。次を分けて扱う。

- Requirementを直接Pass／FailさせるObservation。
- Requirementを意味あるものにするSupporting condition。
- System上は重要だが、別Requirementまたは追加保証に属するFailure。

### 8. 保証範囲と隣接Property

Requirementが保証しない事項を明示する。Security best practiceとして推奨する内容を
NormativeなPass条件へ暗黙に追加しない。

### 9. 本質と短い対話

Security責任者として持ち帰る設計原則をまとめ、その後に原則2〜3問だけ行う。

## Persistent learning note

有益な学習セッションは、Chatの生Logではなく、単独で読める「講義＋対話の再構成」
として保存する。ただし、結論だけに圧縮して学習過程の価値を失わせない。

### Preserve

- 学習者が実際に疑問を持った点。
- 最初の判断と、その理由。
- 判断できなかった境界。
- Agent側の問いにScope混同や過剰な要求があった場合の訂正。
- 対話によって初めて明確になったSecurity Insight。
- NormativeなPass条件と、望ましい追加保証の違い。

### Omit or normalize

- 挨拶、進行確認、Tool実行等のChat metadata。
- 同じ説明の機械的な重複。
- 学習価値のない言い直し。
- 個人情報、Secret、内部Identifier、Production Evidence。
- 根拠を確認できなかった断定。

全文の順序そのものに学習価値がある場合は詳細に残してよい。通常は発言を忠実に
再構成し、`問い`、`学習者の判断`、`整理`、`訂正`を区別する。

### Minimum persistent structure

Requirementごとの永続ノートには、少なくとも次を含める。

1. 文書の役割とSource separation。
2. Normative Requirementと日本語訳。
3. Categoryにおける位置づけ。
4. Security Objectiveと具体Scenario。
5. 用語。
6. Threat ModelとAbuse Path。
7. Security InvariantとEnforcement Point。
8. Pass／FailとScope Calibration。
9. 保証しない範囲と隣接Property。
10. 対話の再構成。
11. このセッションから得られた洞察。
12. 後から使える設計レビュー項目。
13. Primary references。

Human／Agent比較、CSRF等の一般Securityとの比較、Verification Levelの理由、特定Protocol
の詳細などは、Requirementの理解に必要な場合だけ独立Sectionとして加える。すべての
RequirementへC5.1.1固有のSectionを機械的に複製しない。

## Derived insight rules

学習から得た洞察は、次の順に整理する。

1. AISVS原文から直接言えることか。
2. ResearchまたはPrimary sourceによる補足か。
3. Repositoryが現場向けに導いた解釈か。
4. Requirement外だがSystem Security上推奨する追加保証か。

一つのRequirementへのPassをSystem全体の安全性と表現しない。隣接PropertyのFailureを
見つけた場合、元のRequirementを無理にFailへせず、別のGapとして記録する。

誤った説明や問いが判明した場合は、最終ノートで訂正を隠さない。どのPropertyを混同
したかと、正しいScopeを残す。これにより、同じ誤りを後のCategoryで繰り返さない。

## Storage and naming

学習文書はAISVS Familyごとに一つのDirectoryへ配置する。

```text
controls/docs/learning/
├── README.md
└── cNN-family-slug/
    ├── README.md
    └── vX.Y-cN.N.N-descriptive-topic.md
```

- `controls/docs/learning/README.md`: 全Category共通の学習・永続化方針。
- Family `README.md`: Requirement一覧、現在位置、軽量なChecklist、Family固有Source。
- Requirement note: 一つの有益な学習セッションを再利用可能な講義として保存する。

Section単位のDirectoryや空のFamily placeholderを作らない。最初の学習Artifactができた
ときだけFamily Directoryを作る。Requirement IDとSource VersionをFilenameへ含め、
将来のVersionで過去の学習結果を上書きしない。

## Lightweight progress

Family guideで管理する進捗は次だけとする。

- 現在学習中のRequirement。
- 各Requirementを一巡したかのChecklist。
- 永続化したRequirement noteへのLink。

Session Log、Evidence、Reviewer identity、理解度Score、日付ごとのStatusは管理しない。
学習完了は、学習者が次を自分の言葉で短く説明できた時点とする。

- Requirementの本質。
- 具体的なPass／Failと理由。
- Requirementだけでは保証しない範囲。

## Quality check

永続ノートを完了する前に確認する。

- 冒頭にRequirement ID、Level、英語原文、日本語訳がある。
- Normative、Research、Interpretation、Derived insightを混同していない。
- Attacker Capability、Trust Boundary、Security Invariant、Enforcement Pointが具体的である。
- Pass／FailをComponentの有無ではなくOutcomeで説明している。
- Control Scopeを隣接するSecurity best practiceで広げていない。
- 初見の用語を説明している。
- Context依存の用語について、Source上の定義とRepositoryのOperational definitionを
  区別し、判定基準を示している。
- 具体Scenarioから抽象的な設計原則へ進み、抽象化した原則を別Scenarioにも適用できる
  ことを示している。
- 記号や略語だけでSecurity Propertyを表しておらず、平易な自然言語でも説明している。
- 対話中の迷いと重要な訂正を残している。
- 後の設計レビューに使える確認事項がある。
- Primary source、Version、Revision、Statusが必要な精度で示されている。
- Control maturity、Mapping status、製品適合を変更していない。
- Production Evidence、Secret、個人情報を含まない。

## Reference learning note

- [C5.1.1 Step-up Authentication：講義、対話、洞察](c05-access-control-and-identity/v1.0-c5.1.1-step-up-authentication.md)

このノートは共通方式の最初のReferenceである。内容を全Requirementへコピーするのでは
なく、Source separation、Security視座、対話の保存、Scope Calibrationの深さを参考に
する。
