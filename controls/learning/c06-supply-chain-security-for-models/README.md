---
title: "AISVS C6 Supply Chain Security for Models 学習ガイド"
document_kind: "family-learning-guide"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
current_section: "complete"
last_updated: "2026-10-22"
---

# AISVS C6 Modelの供給網をどう確かめるか

C6は、外部Model・Dataset・Adapterの取得から受入れまでの検査と、AI BOMによる構成・由来の追跡を学ぶ。
承認済みの取得元、署名、Scan陰性、振る舞い試験の合格、BOMの存在は、それぞれ別の保証である。

[共通学習方針](../README.md)に従い、C5.1.2の講義の深さを参考にしたSection単位の教材を用意した。
[Control概要](../../control-records/c06-supply-chain-security-for-models/README.md)と全7件のControl本文は、保証・検証・証拠・限界の正本である。

## Section一覧

| Section | Requirement数 | Level内訳 | 学ぶ主題 |
|---|---:|---|---|
| [C6.1 Model Artifact Integrity](v1.0-c6.1-model-artifact-integrity.md) | 4 | L1: 2、L2: 2 | Import前Scan、承認Source、完全性検証可能性、非開発環境への昇格前の受入合格 |
| [C6.2 AI BOM & Supply Chain Monitoring](v1.0-c6.2-ai-bom-and-supply-chain-monitoring.md) | 3 | L1: 1、L2: 2 | ModelとBOMの版対応、配備前署名、Metadata欠落時のBuild失敗 |

## 学習から得た洞察

- [AI BOMの技術構造と実構成を確かめるための証拠](../../../docs/insights/ai-bom-inventory-evidence-and-trust.md)：v1.0-C6.2.1〜C6.2.3の対話を起点に、必須項目・実構成・許可、署名の限界を整理。


## 軽量な学習進捗

C6.1・C6.2の講義と実際の対話を一巡した。C6.2では署名と情報充足、欠落時のBuild失敗、ハッシュ照合と記載漏れの検出、BOMの確認と問題調査の違いを扱い、学習者の理解と次へ進む意思を確認した。現在学習中のSectionはない。
チェックは教材の存在を表さず、Sectionを学習して本質・Pass／Fail・保証しない範囲を説明できた時に付ける。
Control成熟度、Mapping、製品適合とは独立している。

- [x] [C6.1の講義と理解確認](v1.0-c6.1-model-artifact-integrity.md)
- [x] [C6.2の講義と理解確認](v1.0-c6.2-ai-bom-and-supply-chain-monitoring.md)

## 一次資料

採用版はAISVS v1.0の固定Revisionであり、1.01の採用ではない。

- [C6 Normative（固定版）](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C06-Supply-Chain.md)
- [C6.1 Research（固定版）](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C06-Supply-Chain/C06-01-Model-Artifact-Integrity.md)
- [C6.2 Research（固定版）](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C06-Supply-Chain/C06-02-AI-BOM-Supply-Chain-Monitoring.md)
