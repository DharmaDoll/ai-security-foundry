---
title: "AISVS C7 学習ガイド"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
current_section: "complete"
last_updated: "2026-09-28"
---

# AISVS C7 Model Behavior, Output Control & Safety Assurance 学習ガイド

Modelの出力を、形式・信頼性・有害性・出典の異なる軸で評価する。入力検査と出力検査は代替関係ではない。
[共通学習方針](../README.md)に従い、学習進捗とControl成熟・製品適合を分ける。

| Section | 要件数 | Level内訳 | 主題 |
|---|---:|---|---|
| C7.1 Output Format Enforcement | 2 | L1: 2 | Schema、長さ・終了制御 |
| C7.2 Hallucination Detection & Mitigation | 3 | L2: 2、L3: 1 | 信頼性評価と低信頼・高リスク時の扱い |
| C7.3 Output Safety | 4 | L1: 1、L2: 2、L3: 1 | 有害性・内部情報・外向き要求・隠蔽 |
| C7.4 Source Attribution & Citation Integrity | 4 | L1: 2、L2: 1、L3: 1 | 出典と主張の追跡、生成Media |

- [x] [C7.1 講義・対話](v1.0-c7.1-output-format-enforcement.md)
- [x] [C7.2 講義・対話](v1.0-c7.2-hallucination-detection-and-mitigation.md)
- [x] [C7.3 講義・対話](v1.0-c7.3-output-safety.md)
- [x] [C7.4 講義・対話](v1.0-c7.4-source-attribution-and-citation-integrity.md)

## このFamilyの学習から生まれた横断的Insight

- [検査するのは実際に利用されるPayload](../../../docs/insights/validation-must-cover-effective-payload.md)：C7.1・C7.3の検査後の公開・Renderingを考える。
- [再構成でき、保護されたSecurity Evidence](../../../docs/insights/security-evidence-must-be-reconstructable-and-constrained.md)：C7.4の出典から、主張と根拠の連鎖を辿る。
- [Security Artifactの保証範囲](../../../docs/insights/security-artifacts-have-bounded-claims.md)：C7.2のConfidenceやC7.4のCitationを過大評価しない。

これらは学習の起点を示すLinkであり、正式なMappingではない。

## Sources

- [AISVS v1.0 C7 Normative](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C07-Model-Behavior.md)
- [C7.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-01-Output-Format-Enforcement.md)
- [C7.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-02-Hallucination-Detection.md)
- [C7.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-03-Output-Safety-Privacy-Explainability.md)
- [C7.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C07-Model-Behavior/C07-04-Source-Attribution-Citation-Integrity.md)
