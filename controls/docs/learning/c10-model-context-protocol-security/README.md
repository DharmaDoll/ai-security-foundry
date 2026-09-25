---
title: "AISVS C10 Model Context Protocol Security Learning Guide"
document_kind: "family-learning-guide"
source_key: "owasp-aisvs"
source_version: "1.0"
upstream_revision: "78775233666a2022dcfb82037e5e029116955c00"
current_section: "C10.2"
last_updated: "2026-09-25"
---

# AISVS C10 Model Context Protocol (MCP) Security 学習ガイド

## 目的

C10を、MCPの個別機能の暗記ではなく、次の四つのTrust Boundaryとして理解する。

1. 導入・実行するComponentを信頼してよいか。
2. Caller、Tool、引数、Credentialを正しく認証・認可できるか。
3. 通信相手とTransportを信頼できるか。
4. Tool定義、入力、応答、変更を利用前に検証できるか。

全Category共通の講義形式、Source separation、Section単位の保存、Quality checkは
[`../README.md`](../README.md)に従う。C10では23 Requirementを個別ファイルへ分けず、
C10.1〜C10.4の四つの講義として扱う。

[C10 Family overview](../../../control-records/c10-model-context-protocol-security/README.md)は
CategoryとSectionの保証境界、整備済みControlへの入口を示す。全Requirementの保証範囲と
着手順序は[C10全体分析](../../c10-landscape.md)を参照する。

## 進め方

C10.1から章順に進める。各講義では、そのSectionの全Requirementについて、ID、Level、
英語原文、日本語訳、直接の保証、隣接Requirementとの違いを確認する。共通Scenario、用語、
Threat Model、Security Invariant、Enforcement PointはSection全体で統合する。

質疑応答はSection全体に対して原則2〜3問とし、全Requirementを一問ずつ口頭試問しない。
有益な対話は、次の版付きSection Directoryに一つの`learning.md`として保存する。

```text
controls/docs/learning/c10-model-context-protocol-security/
├── README.md
├── v1.0-c10.1-component-integrity/learning.md
├── v1.0-c10.2-authentication-and-authorization/learning.md
├── v1.0-c10.3-secure-transport/learning.md
└── v1.0-c10.4-schema-message-and-input-validation/learning.md
```

実質的な講義と対話を保存するときにだけSection Directoryを作る。空ファイルは作らない。

## Section一覧

LevelはAISVS Verification Levelであり、学習難易度やControl maturityではない。

| Section | Requirement | Level内訳 | 学ぶ主題 |
|---|---:|---|---|
| C10.1 Component Integrity | 3 | L1：1、L2：2 | Componentの配布元・暗号的検証、Server allowlist、Local Serverの最小権限Sandbox |
| C10.2 Authentication & Authorization | 7 | L1：3、L2：4 | RequestごとのToken検証、Tool・引数認可、Session終了、下流Token境界 |
| C10.3 Secure Transport | 5 | L1：2、L2：2、L3：1 | Remote／Local Transport、Origin・Host、Protocol最低版、Sender-constrained Token |
| C10.4 Schema, Message, and Input Validation | 8 | L1：3、L2：4、L3：1 | Schema・内容・Size・Replay・導入同意・Tool定義変更の検証 |

## 軽量な進捗記録

現在学習中：`C10.2 Authentication & Authorization`。

- [x] [C10.1 Component Integrity](v1.0-c10.1-component-integrity/learning.md)
- [ ] C10.2 Authentication & Authorization
- [ ] C10.3 Secure Transport
- [ ] C10.4 Schema, Message, and Input Validation

C10.2.7について開始した説明は、独立したRequirement noteには保存しない。C10.2の講義時に、
Token Pass-throughと委任Contextの違いをSection全体の認証・認可Contextへ統合する。

## Sources

- [AISVS v1.0 C10 Normative Requirements](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C10-MCP-Security.md)
- [AISVS v1.0 C10 Research overview](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-MCP-Security.md)
- [C10.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-01-Component-Integrity.md)
- [C10.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-02-Authentication-Authorization.md)
- [C10.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-03-Secure-Transport.md)
- [C10.4 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C10-MCP-Security/C10-04-Schema-Message-Validation.md)

このGuideのChecklistは個人の学習Navigationである。Control maturity、Mapping、製品適合を
変更しない。
