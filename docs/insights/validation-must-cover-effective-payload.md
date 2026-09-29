---
title: "検査するのは入口の文字列ではなく、実際に利用される内容である"
document_kind: "cross-cutting-insight"
status: "draft"
last_updated: "2026-09-29"
---

# 検査するのは入口の文字列ではなく、実際に利用される内容である

## 中心となる洞察

入力や出力を検査しても、その後の復号、正規化、要約、組立て、Streaming、Renderingで内容や意味が変われば、
検査結果をそのまま最終利用へ持ち越せない。重要なのは「検査器をどこへ置いたか」だけではなく、
検査したArtifactと、危険な境界を越えるArtifactが対応しているかである。

> 検査済みという属性は、検査後に変わったPayloadへ自動継承されない。

## 実用的なモデル

```text
Candidate input / output
  -> decode, normalize, retrieve, assemble, stream, render
  -> effective payload（実際にModel、API、Browser等が利用する内容）
  -> その境界に必要な検査・認可
  -> publish / execute / persist / egress
```

各変換について、誰が変更できるか、何が増えるか、どの時点で副作用が起きるかを記録する。
検査後に変わり得るなら、再検査するか、検査済みの不変Artifactだけを利用する仕組みが要る。
検査器の検知精度と、検知後に実際の利用を止める強制力も別々に測る。

この原則は単一の「全能なFilter」を要求しない。Schema、内容分類、権限確認、URL／Rendering制限には
異なる保証対象があり、それぞれ該当する境界の前で成立させる。

## 具体例

- **入力**：元Textだけを検査し、その後にHTML Entityを復号して埋め込まれた指示をModelへ渡す。
  検査したTextと実際のPromptが異なる。
- **Model出力**：Streamingの断片を画面へ表示した後で全文を分類する。BrowserがMarkdownの画像URLを
  既に取得していれば、後から拒否しても通信を取り消せない。
- **Tool応答**：JSON Schemaに適合した応答でも、本文の指示をModelが次の操作命令として扱えば、
  形式検査だけではその利用境界を守れない。

## 設計レビューとNegative Test

- 取得、復号、正規化、Chunk化、要約、Tool応答、Cache、Renderingまでの変換順序を描けるか。
- 検査後に別のContent、Field、Document、Tool定義が追加・差替えされたら拒否または再評価するか。
- Encoding隠蔽を検知したとき、最終Payloadは実際に遮断されるか。
- 完成前の出力や危険URLを、検証より先に公開・実行・自動取得していないか。
- 拒否した内容がRetry、Fallback、別Routeで復活しないか。正常な多言語・境界長の入力は通るか。

## 限界と隣接Insight

全てのPrompt Injectionを検知できると主張するものではない。検査を正しい場所へ置いても、
検出器の見逃しや許可範囲内の悪用は残る。認可は別の決定論的な境界で評価する。
[Data Protection](protected-data-survives-transformation.md)は変換後も保護すべき情報を追う。
本Insightは、変換後に**実際に利用するPayloadが検査・拒否の対象になっているか**を問う。

## Slide-ready summary

- 検査したものと、使うものを一致させる。
- 検知と遮断は別の品質である。
- 公開・実行・通信の後からは取り消せない。

## 起点となった学習記録

- [C2.1：Prompt Injection Defenses](../../controls/learning/c02-input-validation/v1.0-c2.1-prompt-injection-defenses.md)
- [C7.1：Output Format Enforcement](../../controls/learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.1-output-format-enforcement.md)
- [C7.3：Output Safety](../../controls/learning/c07-model-behavior-output-control-and-safety-assurance/v1.0-c7.3-output-safety.md)
- [C10.4：Schema, Message, and Input Validation](../../controls/learning/c10-model-context-protocol-security/v1.0-c10.4-schema-message-and-input-validation.md)

これは上記のAISVS要件を統合・拡張した新Requirementではなく、複数の対話で共通して現れたRepositoryの設計上の解釈である。
