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

各Sectionの講義を作る前に、少なくとも次を読む。

1. `sources/registry.yaml`に登録されたSourceのVersionとStatus。
2. 固定Revisionにある対象Sectionの全AISVS Normative Requirement。
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

Category／Familyごとに全Requirementへ一度触れるが、講義・保存・復習の単位は
RequirementではなくSection（`C.x`）とする。一度に扱うのは一つのSectionだけとし、
その中の全Requirementを共通Scenarioと保証軸の中で比較する。

1. Category全体の目的、Section一覧、各SectionのRequirement一覧を確認する。
2. 対象Sectionの全Normative Requirement、Research、必要なPrimary sourceを読む。
3. 下記の共通構造で、Section全体を一つの講義として扱う。
4. 各Requirementの直接の保証と相互の境界を説明する。数が多くても読み飛ばさない。
5. Section全体に対して原則2〜3問の短い対話を行い、本質または分かりにくい境界だけを確認する。
6. 有益な対話になった場合、Section単位の学習ノートへ永続化する。
7. Family guideのChecklistと次のSectionだけを更新する。
8. Familyを一巡した後、再利用可能な洞察をControl、Template、AGENTS.md、または別の
   Guidanceへ反映すべきかを検討する。

すべてのSecurity PropertyやCaseを質問形式でなぞらない。理解の中心は講義本文に置く。
用語暗記やFramework自体の採点を目的にしない。

## Required lecture structure

各Section講義は必ず次の順で始める。

### 1. Normative Requirements

- Section ID、Section title、対象Source version。
- Section内の全Versioned Requirement ID。
- 各RequirementのAISVS Verification Level。
- 各RequirementのAISVS英語原文。
- 各Requirementの意味を崩さない日本語訳。

短いRequirement単位の引用としてSourceと固定Revisionを示す。Research pageやChapterを
大量にコピーしない。

### 2. CategoryにおけるSectionの位置づけ

Category全体の中でSectionが何を扱い、Section内の各Requirementが保証をどう分担するか、
隣接するAuthentication、Authorization、Isolation、Integrity、Detection等とどう異なるかを説明する。

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

### 9. Sectionの本質と短い対話

Security責任者としてSection全体から持ち帰る設計原則をまとめ、その後に原則2〜3問だけ行う。
各Requirementを一問ずつ試験する方式には戻さない。

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

Sectionごとの永続ノートには、少なくとも次を含める。

1. 文書の役割とSource separation。
2. Section内の全Normative Requirement、Level、日本語訳。
3. CategoryにおけるSectionの位置づけと、Requirement間の分担。
4. Security Objectiveと具体Scenario。
5. 用語。
6. Threat ModelとAbuse Path。
7. Security InvariantとEnforcement Point。
8. Pass／FailとScope Calibration。
9. 各Requirementが保証しない範囲と隣接Property。
10. 対話の再構成。
11. このセッションから得られた洞察。
12. 後から使える設計レビュー項目。
13. Primary references。

Human／Agent比較、CSRF等の一般Securityとの比較、Verification Levelの理由、特定Protocol
の詳細などは、Sectionの理解に必要な場合だけ独立項目として加える。すべてのSectionへ
C5.1.1固有の構成を機械的に複製しない。

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

新しい学習ノートは、`docs/learning/`配下の版付きSection Directoryへ配置する。
複数Requirementの講義を一つに統合するが、Control本文と学習の役割は分ける。

```text
controls/
├── control-records/
│   └── cNN-family-slug/
│       ├── README.md
│       └── vX.Y-cN.N.N-descriptive-control-name/
│           └── README.md
└── docs/learning/
    ├── README.md
    └── cNN-family-slug/
        ├── README.md
        └── vX.Y-cN.N-section-slug/
            └── learning.md
```

- `controls/docs/learning/README.md`: 全Category共通の学習・永続化方針。
- `docs/learning/`のFamily `README.md`: Section一覧、現在位置、軽量なChecklist、Family固有Source。
- `control-records/`のFamily `README.md`: Category、Section、Requirementを「問うこと」と
  「できてはいけないこと」で辿り、個別Controlへ案内する俯瞰図。
- Control `README.md`: 解釈・適用範囲・検証・証拠・限界の正本。Catalogはここを参照する。
- Section `learning.md`: 一つのSectionと全Requirementを、有益な学習セッションから
  再利用可能な講義として保存する。関連Controlとは相互リンクし、内容や成熟度を一体化しない。

空のSection DirectoryやFamily placeholderを作らない。最初の実質的な学習Artifactが
できたときだけ必要なDirectoryを作る。Section IDとSource VersionをDirectory名へ含め、
将来のVersionで過去の学習結果を上書きしない。

学習ノートのために空のControl本文やCatalog行を作らない。ControlとSection noteの両方が
存在する時点で相互リンクを追加する。Control評価では本文と上流資料、学習ではSection noteと
対象要件・Researchを読み、学習からControlへの反映は独立した解釈・検証の変更として判断する。

旧方針で作成したC5/C9のRequirement単位`learning.md`は、対話と洞察を含む歴史的Artifactとして
そのまま維持する。通常作業のついでに移動・結合しない。Section単位へ統合する場合は、参照Link、
対話由来の洞察、Source versionを失わない明示的なMigrationとして行う。

### Family Control overview

FamilyのControlが実体を持ったら、`control-records/<family>/README.md`に次の三段階を
一つの文書で示す。

1. `C`：Category全体として何を保証したいか。
2. `C.x`：Sectionがどの保証軸を担当するか。
3. `C.x.y`：各Requirementが具体的に何を問うか。

各段階に「問うこと」と「できてはいけないこと」を置く。「できてはいけないこと」は、
そのRequirementを直接Failさせる代表的な失敗を短く示す。隣接RequirementのFailure、
推奨実装、特定製品を混ぜない。完全な解釈・適用境界・検証はControl本文、具体的な講義と
対話は`learning.md`へリンクし、Family READMEだけで適合判定しない。

この俯瞰図はAISVS原文の再掲ではなく、固定したSourceに対するRepositoryの学習用解釈である。
Source Versionを明示し、Requirementの追加・変更時には意味の差分を確認して更新する。
未整備Categoryへ空のFamily READMEを先行作成しない。
今後も俯瞰図は`control-records/<family>/README.md`へ配置し、
`docs/learning/<family>/map.md`は作成しない。

## Lightweight progress

Family guideで管理する進捗は次だけとする。

- 現在学習中のSection。
- 各Sectionを一巡したかのChecklist。
- 永続化したSection noteへのLink。

Session Log、Evidence、Reviewer identity、理解度Score、日付ごとのStatusは管理しない。
Section学習の完了は、学習者が次を自分の言葉で短く説明できた時点とする。

- Section全体の本質とRequirement間の違い。
- 代表的なPass／Failと理由。
- 各Requirementだけでは保証しない範囲。

## Quality check

永続ノートを完了する前に確認する。

- 冒頭にSection IDと、全RequirementのID、Level、英語原文、日本語訳がある。
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

## Family learning guides

- [C5：Access Control and Identity](c05-access-control-and-identity/README.md)
- [C8：Memory, Embeddings & Vector Database Security](c08-memory-embeddings-and-vector-database-security/README.md)
- [C9：Orchestration and Agentic Security](c09-orchestration-and-agentic-security/README.md)
- [C10：Model Context Protocol (MCP) Security](c10-model-context-protocol-security/README.md)

## Reference learning note

- [C8.1 Access Controls on Memory & RAG Indices：現行Section単位方式](c08-memory-embeddings-and-vector-database-security/v1.0-c8.1-access-controls-memory-rag-indices/learning.md)
- [C5.1.1 Step-up Authentication：講義、対話、洞察](../../control-records/c05-access-control-and-identity/v1.0-c5.1.1-step-up-authentication/learning.md)

C8.1は現行のSection単位方式のReferenceである。C5.1.1は旧Requirement単位方式だが、
Source separation、Security視座、対話の保存、Scope Calibrationの深さを引き続き参考にする。
