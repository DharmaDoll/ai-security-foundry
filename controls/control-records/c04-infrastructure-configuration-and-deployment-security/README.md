# C4 Infrastructure, Configuration & Deployment Security

AIの実行基盤から何ができるか、基盤側から何を読めるかを区別し、Model窃取・漏えい・Workload間混入を検証する。
採用基準は[AISVS v1.0固定Revision](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md)。1.01への移行ではない。
[学習ガイド](../../learning/c04-infrastructure-configuration-and-deployment-security/README.md)の進捗はControl成熟度・製品適合と独立している。

## Sectionの見取り図

| Section | 問うこと | できてはいけないこと |
|---|---|---|
| [C4.1 AI Workload Sandboxing & Validation](#c41-ai-workload-sandboxing--validation) | 実行の隔離、安全な読込み、環境証拠と実行中の重み保護を分けて検証するか | ContainerやModel署名だけで全保証を済ませる |
| [C4.2 AI Hardware Security](#c42-ai-hardware-security) | Firmware、TEE、各Workloadの証拠、メモリ引渡しと機器接続を保護するか | 機密計算という名称で機能・対象範囲を推定する |
| [C4.3 Edge & Distributed AI Security](#c43-edge--distributed-ai-security) | 端末の認証、配布、Runtimeと保存・復号を保護するか | 保存時暗号化だけで復号後の露出も防いだとする |

<a id="requirement"></a>

## Requirement一覧

C4.1〜C4.3の全14件を整備済み。各Controlの保証境界と検証を個別に確認する。
LevelはAISVS Verification Levelであり、文書成熟度や製品適合ではない。

## C4.1 AI Workload Sandboxing & Validation

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C4.1.1](v1.0-c4.1.1-isolated-sandbox-for-model-execution/README.md) | 1 | AIモデルを隔離されたサンドボックスで実行するか。 | 隔離内からホストの重要資源へ自由に作用する。 |
| [C4.1.2](v1.0-c4.1.2-safe-serialization-format-allowlist-at-model-loading/README.md) | 1 | モデル読込みで安全な保存形式の許可リストを強制するか。 | 危険なDeserializerへ渡してから形式を判定する。 |
| [C4.1.3](v1.0-c4.1.3-workload-attestation-before-model-loading/README.md) | 3 | モデル読込み前に実行環境のアテステーションを検証するか。 | Model署名を環境の正常性の証拠とする。 |
| [C4.1.4](v1.0-c4.1.4-protect-confidential-model-weights-during-runtime/README.md) | 3 | 機密推論中の重みを隔離環境で保護するか。 | 保存時暗号化だけで実行中の重み保護を主張する。 |

## C4.2 AI Hardware Security

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C4.2.1](v1.0-c4.2.1-pinned-signed-boot-attested-accelerator-firmware/README.md) | 2 | GPUファームウェアの版・署名・起動時証拠を確認するか。 | 署名だけで承認版・起動状態まで証明する。 |
| [C4.2.2](v1.0-c4.2.2-tee-hardware-isolation-encryption-and-integrity/README.md) | 3 | TEEの隔離・メモリ暗号化・完全性を別々に検証するか。 | 通信暗号化を常駐メモリの暗号化と呼ぶ。 |
| [C4.2.3](v1.0-c4.2.3-hardware-attestation-before-each-accelerator-workload/README.md) | 3 | 各ワークロード前にGPUの完全性を検証するか。 | Bootの過去結果だけで各Jobを開始する。 |
| [C4.2.4](v1.0-c4.2.4-accelerator-memory-partitioning-and-job-sanitization/README.md) | 3 | GPUメモリを分割しジョブ間で残留情報を消去するか。 | Memory Freeだけで次利用者への引渡しを済ませる。 |
| [C4.2.5](v1.0-c4.2.5-approved-accelerator-topologies-and-authenticated-endpoints/README.md) | 3 | GPU間接続を承認済み構成と認証した機器へ制限するか。 | 未認証Peerや未承認Routeへ接続する。 |

## C4.3 Edge & Distributed AI Security

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C4.3.1](v1.0-c4.3.1-strong-edge-device-authentication-to-central-infrastructure/README.md) | 1 | 端末を中央基盤で強く認証するか。 | 端末IDの自己申告だけで接続を認める。 |
| [C4.3.2](v1.0-c4.3.2-signed-packaging-and-on-device-model-verification/README.md) | 2 | モデルを署名して配布し端末の使用前に検証するか。 | Packaging署名だけで端末側の未検証読込みを許す。 |
| [C4.3.3](v1.0-c4.3.3-inference-process-memory-and-file-isolation/README.md) | 3 | 端末推論のプロセス・メモリ・ファイルアクセスを隔離するか。 | 別Process名だけでMemory・Fileも分離済みとする。 |
| [C4.3.4](v1.0-c4.3.4-hardware-backed-encryption-for-locally-stored-models/README.md) | 3 | 端末保存の重みと機密パラメータをハードウェア鍵で暗号化するか。 | Modelと同じPackageへ平文鍵を置く。 |
| [C4.3.5](v1.0-c4.3.5-packaged-model-encryption-and-trusted-runtime-decryption/README.md) | 3 | アプリ同梱モデルを暗号化し信頼境界内だけで復号するか。 | 復号したModelを抽出可能な一時Fileへ出す。 |

## 関連する洞察

個別要件の理解・設計レビューを助ける参照であり、追加要件や正式なMappingではない。

- [隔離は、誰から誰を守るかで意味が変わる](../../../docs/insights/isolation-has-a-direction.md)：対象 C4.1・C4.1.1・C4.1.4・C4.2・C4.2.2。誰から何を守る隔離かを明確にし、逆方向の保証と混同しない。
- [端末で推論できることと、重要操作を許可できることは別である](../../../docs/insights/local-inference-is-not-action-authority.md)：対象 C4.3・C4.3.1・C4.3.2・C4.3.5。端末上の推論・モデル保護と、重要操作を許す側の判断を分ける。
- [不要なAuthorityを消し、残る全経路を完全仲介する](../../../docs/insights/minimize-and-mediate-authority.md)：対象 C4.3。不要な能力を取り除き、残した操作経路で認可を迂回できないか確認する。
- [Dataは形を変えてもProtectionを失わない](../../../docs/insights/protected-data-survives-transformation.md)：対象 C4.3・C4.3.4・C4.3.5。要約・変換・復号後のデータにも、元の保護と認可が必要かを確認する。
- [共有資源の再利用は、次の利用者への安全な引渡しである](../../../docs/insights/resource-reuse-is-a-security-handoff.md)：対象 C4.2・C4.2.4。同時利用者の分離と、次の利用者へ状態を残さない条件を分ける。

## 隣接する保証との違い

C4.1.1はModelから基盤を守る方向、C4.1.4は基盤側の主体から重みを守る方向の隔離。
C4.1.2は読込み形式、C4.1.3は読込み前の環境証拠であり、互いを代替しない。
C3のModel変更管理やC5の認可、C11の振る舞いの耐性も別に評価する。
Researchの製品・版・推奨設定・数値を全製品に必須の原文条件として自動採用しない。

## References

- [AISVS v1.0 C4正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C04-Infrastructure.md)
- [AISVS v1.0 C4.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-01-Workload-Sandboxing-Validation.md)
- [AISVS v1.0 C4.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-02-Hardware-Security.md)
- [AISVS v1.0 C4.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C04-Infrastructure/C04-03-Edge-Distributed-Security.md)
- [C4学習ガイド](../../learning/c04-infrastructure-configuration-and-deployment-security/README.md)
