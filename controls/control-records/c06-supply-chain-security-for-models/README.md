# C6 Supply Chain Security for Models

外部Model・Dataset・Adapterを取得し、検査・照合・受入れする保証と、Model構成をAI BOMで追う保証を分ける。
基準は[AISVS v1.0固定Revision](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C06-Supply-Chain.md)。1.01への移行ではない。
C6.1・C6.2の全7件を整備済み。[学習ガイド](../../learning/c06-supply-chain-security-for-models/README.md)は講義と理解確認を扱い、Control成熟度と独立している。

## Sectionの見取り図

| Section | 問うこと | できてはいけないこと |
|---|---|---|
| [C6.1 Model Artifact Integrity](#c61-model-artifact-integrity) | Import前のCode検査、承認Source、完全性、非開発環境への昇格前の受入合格を確認するか | Source承認や署名で振る舞いも安全とみなす |
| [C6.2 AI BOM & Supply Chain Monitoring](#c62-ai-bom--supply-chain-monitoring) | 版対応した機械可読BOM、配備前署名、Metadata欠落時のBuild失敗を確認するか | Schema適合や署名だけで内容の完全性を保証する |

<a id="requirement"></a>

## Requirement一覧

LevelはAISVS Verification Levelであり、文書成熟度や製品適合ではない。

## C6.1 Model Artifact Integrity

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C6.1.1](v1.0-c6.1.1-malicious-code-scan-before-model-import/README.md) | 1 | モデルをImportする前に悪意あるコードを検査するか。 | Import後のScanを事前検査と呼ぶ。 |
| [C6.1.2](v1.0-c6.1.2-download-ai-artifacts-only-from-approved-sources/README.md) | 1 | 重み・データセット・Adapterを承認した取得元へ限定するか。 | 暗黙DownloadやRedirectで未承認Sourceを使う。 |
| [C6.1.3](v1.0-c6.1.3-integrity-verifiability-for-every-third-party-model-artifact/README.md) | 2 | すべての外部モデル構成物の完全性を検証可能にするか。 | Modelと一緒に置換できるHashだけを信頼する。 |
| [C6.1.4](v1.0-c6.1.4-behavioral-acceptance-before-any-nondevelopment-promotion/README.md) | 2 | 開発以外へ昇格する前に振る舞いの受入試験へ合格させるか。 | 本番以外なら未合格Modelを昇格させる。 |

## C6.2 AI BOM & Supply Chain Monitoring

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C6.2.1](v1.0-c6.2.1-versioned-machine-readable-ai-bom-for-every-model/README.md) | 1 | 各モデルに版管理された機械可読AI BOMを公開するか。 | 版・構成・由来を追えないBOMを提供する。 |
| [C6.2.2](v1.0-c6.2.2-cryptographically-signed-ai-bom-before-deployment/README.md) | 2 | AI BOMへ配備前に暗号署名するか。 | Model本体の署名をBOM署名と混同する。 |
| [C6.2.3](v1.0-c6.2.3-fail-build-on-missing-ai-bom-component-metadata/README.md) | 2 | AI BOMの構成Metadata欠落時にBuildを失敗させるか。 | Metadata不足でもBuildを成功させる。 |

## 隣接する保証との違い

C3は本番のModel変更と学習段階、C4は実行環境、C1は学習Dataを扱う。
C6の取得元承認・検査・検証可能性・受入合格は別の保証で、単一Artifactの存在を全体の安全性へ広げない。
Researchの複数Scanner、署名規格、固定版参照やProtocolの推奨は補強として評価し、原文の一律条件へ追加しない。

## References

- [AISVS v1.0 C6正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C06-Supply-Chain.md)
- [C6.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C06-Supply-Chain/C06-01-Model-Artifact-Integrity.md)
- [C6.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C06-Supply-Chain/C06-02-AI-BOM-Supply-Chain-Monitoring.md)
