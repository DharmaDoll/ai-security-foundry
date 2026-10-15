---
title: "AISVS C4 Infrastructure, Configuration and Deployment Security 学習ガイド"
document_kind: "family-learning-guide"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
current_section: "complete"
last_updated: "2026-10-15"
---

# C4 AIを動かす基盤を守る

モデルを動かす環境から何ができるか、そこで誰が情報を読めるかを学ぶ。C3のモデル変更管理と区別し、実行環境、AI用ハードウェア、端末上の配備を扱う。

講義と保存は[共通学習方針](../README.md)に従う。学習進捗はControl成熟度、Mapping、製品適合とは独立している。v1.01への追従と影響評価は[Issue #6](https://github.com/DharmaDoll/ai-security-foundry/issues/6)で扱い、本資料のv1.0参照を暗黙に変更しない。

| Section | 要件数 | 主な問い |
|---|---:|---|
| C4.1 AI Workload Sandboxing & Validation | 4 | モデルを隔離して動かし、安全に読み込み、実行環境を確認できるか |
| C4.2 AI Hardware Security | 5 | GPUなどの機器、メモリ、機器間の接続を保護できるか |
| C4.3 Edge & Distributed AI Security | 5 | 現場端末やモバイル端末に配備したモデルを保護できるか |

## 軽量な進捗

C4.1〜C4.3の講義と対話を一巡した。チェックは学習の進捗であり、Control成熟や製品適合を示さない。

- [x] [C4.1：AIの実行環境の隔離と検証](v1.0-c4.1-ai-workload-sandboxing-and-validation.md)
- [x] [C4.2：AIハードウェアの保護](v1.0-c4.2-ai-hardware-security.md)
- [x] [C4.3：端末・分散環境のAI保護](v1.0-c4.3-edge-and-distributed-ai-security.md)

## このFamilyから得られた横断的な洞察

- [隔離には方向がある](../../../docs/insights/isolation-has-a-direction.md)：C4.1・C4.2を起点に、モデルから基盤を守る境界と、基盤からモデルを守る境界を分ける。
- [共有資源の再利用は安全な引渡し](../../../docs/insights/resource-reuse-is-a-security-handoff.md)：C4.2.4を起点に、同時利用者との分離と次の利用者へ残さない条件を分ける。
- [変換後もData Protectionを保つ](../../../docs/insights/protected-data-survives-transformation.md)：C4.3.5の復号後の一時ファイルを起点に、平文が存在する場所を追う。
- [端末の推論と重要操作の認可](../../../docs/insights/local-inference-is-not-action-authority.md)：C4.3のスマホゲームとの比較を起点に、端末内での計算と最終判断の権限を分ける。

Insightは対話から得た再利用可能な整理であり、Control本文や正式なMappingではない。

## 一次資料

- [AISVS v1.0 C4正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md)
- [AISVS v1.0 C4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-Infrastructure.md)
