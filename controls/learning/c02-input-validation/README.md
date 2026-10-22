---
title: "AISVS C2 Input Validation 学習ガイド"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
current_section: "complete"
last_updated: "2026-10-19"
---

# AISVS C2 Input Validation 学習ガイド

入力の形式・表現・指示・内容をModelへ渡す前に扱う。入力検査は認可、Tool実行制御、出力検査の代わりにならない。

全Category共通の[学習方針](../README.md)に従う。学習完了はControl成熟や製品適合を意味しない。

| Section | Requirement数 | Level内訳 | 主題 |
|---|---:|---|---|
| C2.1 Prompt Injection Defenses | 8 | L1: 5、L2: 2、L3: 1 | 検査対象と利用内容の整合性、指示階層、入力の隠蔽 |
| C2.2 Content & Policy Screening | 4 | L1: 2、L2: 1、L3: 1 | 禁止内容、多言語、非テキスト、組み合わせ攻撃 |

## このFamilyの学習から生まれた横断的Insight

- [検査するのは実際に利用されるPayload](../../../docs/insights/validation-must-cover-effective-payload.md)：C2.1の検査対象と最終利用のずれを、出力・Tool応答にも持ち運ぶ考え方。

これは学習の起点を示すLinkであり、ControlやPatternとの正式なMappingではない。


- [x] [C2.1 講義・対話](v1.0-c2.1-prompt-injection-defenses.md)
- [x] [C2.2 講義・対話](v1.0-c2.2-content-policy-screening.md)

各ノートは、原文と日本語訳、具体Scenario、用語、攻撃経路、要件ごとの正常系・Negative Test、
Pass／Failの境界、運用・Evidence、既存対話と追加演習を含む。
[学習ノートとControlの役割の違い](../README.md#boundaries)は維持し、説明を補強しても理解確認済みの範囲を自動的に増やさない。

実装計画は[Issue #4](https://github.com/DharmaDoll/ai-security-foundry/issues/4)。一要件一Patternではなく、実システムの設計問題から独立して開発する。

## Sources

- [Normative C2](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C02-Input-Validation.md)
- [C2.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md)
- [C2.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C02-User-Input-Validation/C02-02-Content-Policy-Screening.md)
