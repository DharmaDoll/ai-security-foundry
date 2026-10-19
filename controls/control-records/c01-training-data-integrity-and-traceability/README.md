# C1 Training Data Integrity & Traceability

学習・追加学習に入るDataの必要性、来歴、完全性、Labelと品質を区別して保証する。
採用基準は[AISVS v1.0の固定Revision](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C01-Training-Data-Integrity-and-Traceability.md)。学習を行わないRAGへの適用は自動的には生じない。
[学習ガイド](../../learning/c01-training-data-integrity-and-traceability/README.md)の進捗とControl成熟度は独立している。

## Sectionの見取り図

| Section | 問うこと | できてはいけないこと |
|---|---|---|
| [C1.1 Training Data Origin & Data Security](#c11-training-data-origin--data-security) | 必要な項目だけを、出所・完全性・変更・利用帰属まで追えるか | 台帳やHash一つで五つの保証を済ませる |
| [C1.2 Data Labeling and Annotation Security](#c12-data-labeling-and-annotation-security) | Labelの権限・完全性・機密性を守れるか | 出所の確かなDatasetならLabelも安全とみなす |
| [C1.3 Training Data Quality and Security Assurance](#c13-training-data-quality-and-security-assurance) | 毒入れ・誤Label・偏り・禁止Contentを評価できるか | 改ざんがないことを元から安全なことと混同する |

<a id="requirement"></a>

## Requirement一覧

LevelはAISVS Verification Levelであり、製品適合やControl成熟度ではない。
C1.1〜C1.3の全13件を整備済み。各Controlの保証境界と検証を個別に確認する。

## C1.1 Training Data Origin & Data Security

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C1.1.1](v1.0-c1.1.1-purpose-bound-training-fields/README.md) | 1 | 学習項目をモデルの目的に必要なものへ限定するか。 | 目的に不要なFieldを既定の全列取込みで学習へ混ぜる。 |
| [C1.1.2](v1.0-c1.1.2-complete-training-source-inventory/README.md) | 2 | すべての学習データ源の台帳と加工履歴を維持するか。 | 未登録Sourceや六項目の欠落を見逃し、台帳完備とみなす。 |
| [C1.1.3](v1.0-c1.1.3-stored-and-transferred-training-data-integrity/README.md) | 2 | 保存・転送中の学習データの完全性を確かめるか。 | Dataと同じ権限で置換できるChecksumだけを信頼する。 |
| [C1.1.4](v1.0-c1.1.4-training-data-integrity-monitoring/README.md) | 2 | 学習データへの無断変更と破損を監視するか。 | 学習直前の単発照合だけで保存中の監視も済んだとみなす。 |
| [C1.1.5](v1.0-c1.1.5-dataset-watermark-attribution/README.md) | 3 | データセットのウォーターマークで利用を識別するか。 | Hashの存在だけで無断利用を識別できると主張する。 |

## C1.2 Data Labeling and Annotation Security

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C1.2.1](v1.0-c1.2.1-annotation-create-modify-approve-authorization/README.md) | 1 | 注釈の作成・変更・承認を権限で制限するか。 | 権限外のAPI操作を許す。 |
| [C1.2.2](v1.0-c1.2.2-labeling-artifact-cryptographic-integrity/README.md) | 2 | 注釈成果物の暗号学的完全性を検証するか。 | 変更したFileを検証済みとして読む。 |
| [C1.2.3](v1.0-c1.2.3-protect-sensitive-label-information-before-artifacts/README.md) | 2 | 機微なラベル情報を成果物に入れる前に保護するか。 | 署名とアクセス制限だけで平文の機微情報を残す。 |

## C1.3 Training Data Quality and Security Assurance

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C1.3.1](v1.0-c1.3.1-training-pipeline-poisoning-and-corruption-detection/README.md) | 2 | 学習経路で毒入れと偶発的な破損の疑いを検出するか。 | 署名やSchema検査だけで毒入れ検出済みとみなす。 |
| [C1.3.2](v1.0-c1.3.2-automatic-label-confidence-and-consistency-checks/README.md) | 2 | 自動ラベルへ確信度の閾値と整合性検査を適用するか。 | 閾値か整合性検査の片方だけで済ませる。 |
| [C1.3.3](v1.0-c1.3.3-bias-evaluation-for-security-decisions/README.md) | 2 | セキュリティ判断に使うモデルの偏りを評価するか。 | 全体精度だけで条件別の盲点を評価済みとする。 |
| [C1.3.4](v1.0-c1.3.4-remove-disallowed-content-before-training/README.md) | 2 | 禁止内容を検出して学習前に除外するか。 | 禁止とFlagした例を学習へそのまま流す。 |
| [C1.3.5](v1.0-c1.3.5-clean-label-poisoning-defenses/README.md) | 3 | 正しいラベルに紛れる毒入れへの防御を検証するか。 | 正しいLabelという理由だけで毒入れを否定する。 |

## 隣接する保証との違い

C1.1.3は保存・転送時の完全性、C1.1.4は変更監視、C1.1.5は利用帰属の識別。
受入れ時から汚染されたDataは完全性保護だけでは除けない。C1.2・C1.3を別に評価する。
C6の供給元評価、C12.5.1のLineage・Logも関連するが、同じ保証ではない。
Researchの製品例や数値は一律の必須条件へ昇格させない。

## References

- [AISVS v1.0 C1 正規要件](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C01-Training-Data-Integrity-and-Traceability.md)
- [AISVS v1.0 C1.1 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C01-Training-Data/C01-01-Training-Data-Origin-Traceability.md)
- [AISVS v1.0 C1.2 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C01-Training-Data/C01-02-Data-Labeling-Annotation-Security.md)
- [AISVS v1.0 C1.3 Research](https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/research/chapters/C01-Training-Data/C01-03-Training-Data-Quality-Security-Assurance.md)
- [C1 学習ガイド](../../learning/c01-training-data-integrity-and-traceability/README.md)
