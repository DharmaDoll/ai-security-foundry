---
title: AI実行部品を環境の境界ごとに分離する
versioned_id: v1.0-C3.4.1
requirement_id: C3.4.1
verification_level: 1
family_id: C3
source_key: owasp-aisvs
source_version: '1.0'
source_status: stable
upstream_revision: 78775233666a2022dcfb82037e5e029116955c00
upstream_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md
research_url: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-04-Secure-Development-Practices.md
last_verified: '2026-10-18'
maturity: verifiable
mapping_assessment_refs: []
---

# AI実行部品を環境の境界ごとに分離する

AISVS Verification Level: 1

[C3.4 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.4-secure-development-practices.md)

## Upstream basis

AISVS `v1.0-C3.4.1`は、開発・検証・本番等の環境を跨いでAI固有Runtime Componentを共有しないようにする。
ResearchはMCP Server、Agent Runtime等の共有が権限の橋渡しを生むことを扱う。特定Cloud AccountやSandbox製品を原文の唯一の必須実装とはしない。
採用基準は固定Revisionのv1.0。1.01への移行ではない。以下の具体的な検証条件はRepositoryの解釈である。

## Interpretation

環境ごとにAI固有の実行Instance、状態、接続・権限を分ける。別の環境名でも同じMCP ServerやOrchestration Instanceが本番権限を持って両方から使われるなら分離できていない。同じ製品や固定版のCodeを別Instanceで使うことと、実行部品・可変状態を共有することは区別する。

## Security objective

侵害されやすい開発・検証側から、共有AI部品とそのCredentialを通じて本番へ影響が届くことを防ぐ。

## Applicability

開発・検証・本番等の境界を持つAI Systemと、そのModel Serving、Agent Runtime、MCP Server等の実行部品を対象とする。環境を一つしか持たない場合も、同じInstance内の実験処理と本番処理を別名で混在させていないか確認する。

### Non-applicability

異なる環境を持たず、環境を跨ぐAI実行部品が存在しないなら構成を示して対象外とできる。名前だけの分離や共有Serviceを隠した単一環境という説明は根拠にしない。

## Scope and assumptions

対象Deployment、Model一式、版、Provider、Registryと実際の読込み経路を評価開始時に特定する。
名前やAliasが可変なら実体の識別方法を明示する。試験は隔離環境の無害な模擬Artifactで行い、
本番Dataや実行可能な不正Payloadを持ち込まない。証拠の対象版と現在の配備が一致するか確認する。

## Assets, actors, identities, and trust boundaries

各環境の実行Identity・Instance・状態・接続先の間の境界。資産は本番Tool、Data、Agent設定とRuntime状態。開発者、検証担当者、本番運用者、AgentとMCPのService Identityが関わる。攻撃者は開発Agentの入力や設定を操作し、共有Serviceに委任された権限を使う。

## Required security properties

| ID | 必要な性質 |
|---|---|
| SP-1 | 各環境のAI固有Runtime Componentを列挙し、別Instanceと状態・設定・接続先の対応を特定する。 |
| SP-2 | 環境を跨ぐ実行Instanceや可変状態の共有がなく、開発側から共有部品の本番権限を借りられない。 |
| SP-3 | 環境別の接続・Identityが強制され、任意の環境名の指定だけで本番Instanceを使えない。 |

## Scope calibration and adjacent assurance

C3.4.2は学習・Fine-tuning環境と本番の分離。本ControlはAI実行部品の環境間共有を扱い、一方のPassから他方を推論しない。C3.3.3の並行Model版の状態分離とも境界が異なる。

## Threat and failure-mode rationale

開発と本番のAgent自体を分けても、本番Toolを持つ共有MCP Serverが両者に呼ばれると、開発Agent侵害から本番操作へ繋がる。
外部脅威IDとの厳密なMappingは未評価。Research内のMappingを自動継承しない。

## Verification

### Architecture and configuration review

配備図だけでなくRuntime接続先、MCP登録、Agent設定、Credentialと可変状態の保存先を環境間で照合する。共通URLや共通Service Accountで同じInstanceへ到達しないか調べる。

### Positive verification

開発・本番の模擬Agentを別Runtime・別MCP Instanceへ接続する。各環境内の操作が成功し、開発の変更や呼出しが本番の状態・Toolへ作用しないことを実Identityで確認する。

### Negative and abuse-case verification

| ID | 試すこと | 期待結果 |
|---|---|---|
| N-1 | 両環境を本番権限付きの同じMCP Instanceへ接続する | 実行部品の共有を検出し、本要件のPassにしない。SP-1、SP-2。 |
| N-2 | 開発Agentが環境名やURLを本番へ書き換える | 実Identity・通信境界で拒否され、本番Instanceを借用できない。SP-3。 |
| N-3 | 別Instanceでも同じ可変Agent設定やSessionを編集させる | 環境間の状態共有を検出し、Instance名の違いだけで分離済みとしない。SP-2。 |

### Failure conditions

異なる環境が同じAI実行部品・可変状態を共有する、開発側から共有部品の本番権限を使える、環境名の自己申告だけで越境できる場合はFail。
観測できない境界や不足する証拠を記録し、有限の試験の成功を未観測経路へ広げない。

## Evidence expectations

| 証拠 | 作成元 | 対象 | 鮮度 | 完全性・機微性 | 受入れ条件 |
|---|---|---|---|---|---|
| 環境別のInstance・接続・権限表 | AI基盤運用者 | 全Runtime・MCP・状態保存先 | 構成・接続先変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 実部品の共有がなく対応を追える |
| 環境間越境と変更影響の試験 | 検証担当者 | 開発・検証・本番の実Identity | 初回とIdentity・境界変更時 | 変更履歴を保護し、鍵・本番Artifact・内部識別子を公開しない | 自己環境の成功と他環境への作用拒否を示す |

## Related requirements

[C3.4.2](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.4.2-training-and-fine-tuning-isolated-from-production/README.md)は学習・Fine-tuning環境と本番の分離。本ControlはAI実行部品の環境間共有を扱い、一方のPassから他方を推論しない。[C3.3.3](../../../../controls/control-records/c03-model-lifecycle-management-and-change-control/v1.0-c3.3.3-parallel-model-version-runtime-state-isolation/README.md)の並行Model版の状態分離とも境界が異なる。
[C3 Family概要](../README.md)から隣接Controlを確認する。Engineering Mappingは独立に評価する。

## Known limitations and uncertainty

環境を分けても共通管理基盤・供給元・管理者侵害のRiskは残る。分離は部品の安全性やTool操作の認可を単独では保証しない。固定した同じCodeの別配備は同一の実行Instance共有とは異なる。
`verifiable`は本書の成熟度であり、実製品での適合や試験完了を意味しない。

## References

- [AISVS v1.0 C3 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
- [AISVS v1.0 C3.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C03-Model-Lifecycle-Management/C03-04-Secure-Development-Practices.md)
- [C3.4 Section講義](../../../learning/c03-model-lifecycle-management-and-change-control/v1.0-c3.4-secure-development-practices.md)
- [C3 Family概要](../README.md)

## Changelog

| 日付 | 変更 | 根拠 | 証拠 |
|---|---|---|---|
| 2026-10-18 | 初版。要件固有の保証境界・性質・正負試験・証拠を定義 | 固定版AISVS v1.0と対応Research、Repository解釈 | 本文の検証設計。実製品試験は未実施 |
