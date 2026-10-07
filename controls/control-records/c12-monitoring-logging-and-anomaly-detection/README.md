# AISVS C12 Monitoring, Logging & Anomaly Detection

対象はAISVS v1.0の固定Revision `78775233666a2022dcfb82037e5e029116955c00`。
この一覧は[正規要件][normative]の代替ではなく、保証境界を辿るための
Repository interpretation。[Section単位の学習資料](../../learning/c12-monitoring-logging-and-anomaly-detection/README.md)と
Control成熟度は独立する。正規Metadataは[Catalog](../../catalog.yaml)を参照する。

## この章で保証したいこと

AI Systemが受け取り、検索し、判断し、出力し、変更したことを、事後に
再構成し、異常を検知・調査できるようにする。Logの存在だけで攻撃の阻止や
内容の正しさは保証されない。一方、全文の無制限な記録は機密情報を
新たな場所へ集めるため、調査可能性と閲覧権限・保存範囲を両方評価する。

## Sectionの境界

| Section | 問うこと | できてはいけないこと |
|---|---|---|
| C12.1 Request & Response Logging | 一回のAI処理をSession、推論、Policy判断、RAG検索へ辿れるか。 | Eventはあるが相関・必要項目がなく調査で再構成できない。 |
| C12.2 Detection and Alerting | 攻撃試行・異常行動・AI API悪用を検知し調査へ渡せるか。 | Log保存だけで検知・Alertできているとみなす。 |
| C12.3 Model, Data, and Performance Drift Detection | Inputや回答品質の変化を観測し、想定内と説明不能な変化を分けられるか。 | Drift Signalをそのまま侵害の確証やModelだけの問題とみなす。 |
| C12.4 Proactive Security Behavior Monitoring | Agent起動時のSecurity評価と重要操作・停止の監査を行えるか。 | Agentの自己申告や「操作なし」だけで判断過程を再構成したとする。 |
| C12.5 Training Data & Model Lifecycle Audit | Data・Label・Model・取込文書の来歴と変更を追えるか。 | 実行時Logだけで材料・変更履歴も監査できるとする。 |

## Requirement

個別ControlへのLinkがない行は、まだControlとして成熟させていない保証上の問い。
学習資料が存在することとCatalog登録・製品適合は別である。LevelはAISVSの
Verification Levelであり、Repositoryの成熟度ではない。

C12.1では、InteractionのSession相関（12.1.1）、Safety／Policy判断の詳細
（12.1.2）、推論Eventの共通Schema（12.1.3）、RAG検索のQuery・文書・Source
（12.1.4）を分ける。対応Researchは調査可能性と過剰なContent Captureの
緊張関係を指摘するが、特定のTelemetry製品やField名を一律に必須化しない。

| Requirement | Level | 問うこと | できてはいけないこと |
|---|---:|---|---|
| [C12.1.1](v1.0-c12.1.1-log-ai-interactions-with-session-context/README.md) | 1 | AI InteractionをSession ContextとAI固有Telemetryに結び付けて記録するか。 | 汎用Request数だけ残し、どのAI処理に属するか辿れない。 |
| [C12.1.2](v1.0-c12.1.2-log-safety-filter-and-policy-decisions/README.md) | 2 | Safety Filter・Policy判断を監査・調査できる詳細で記録するか。 | 拒否・許可の理由と対象Stageが分からない。 |
| [C12.1.3](v1.0-c12.1.3-structured-interoperable-inference-event-logs/README.md) | 2 | 推論Eventを指定の最低Fieldを持つ相互運用可能なSchemaで記録するか。 | ProviderやModel、Token数、Operationを再構成できない。 |
| [C12.1.4](v1.0-c12.1.4-log-rag-retrieval-queries-documents-and-sources/README.md) | 2 | RAG検索のQuery、取得文書、Knowledge Sourceを記録するか。 | 件数だけ残し、何を検索・取得したか分からない。 |
| [C12.2.1](v1.0-c12.2.1-detect-and-alert-on-known-adversarial-inputs/README.md) | 1 | 既知の攻撃的な入力を見つけ、調査できる通知を出すか。 | 入力の記録や遮断だけで、通知もできているとみなす。 |
| [C12.2.2](v1.0-c12.2.2-detect-unusual-conversation-and-probing-behavior/README.md) | 2 | 会話の流れや繰り返しから不自然な行動を見つけるか。 | 一件ずつの検査や単純な回数集計だけで、探り行動も見つけたとみなす。 |
| [C12.2.3](v1.0-c12.2.3-detect-ai-specific-attacks-with-custom-rules/README.md) | 2 | 協調した脱獄、不正な指示、内部指示の引き出しを、個別のルールで見つけるか。 | 単発の文面検査だけで、複数人に分かれた攻撃も見つけたとみなす。 |
| [C12.2.4](v1.0-c12.2.4-include-offending-query-metadata-in-extraction-alerts/README.md) | 2 | 抽出の通知から、問題の質問を調べられるか。 | 通知名や総数だけ残り、どの質問が問題か分からない。 |
| [C12.2.5](v1.0-c12.2.5-attribute-token-usage-by-user-session-feature-and-team/README.md) | 2 | AIのトークン使用量を利用者・会話・機能・チームまたは作業領域ごとに追えるか。 | 総量だけで、誰のどの機能の消費か分からない。 |
| [C12.2.6](v1.0-c12.2.6-monitor-llm-api-traffic-for-covert-c2-activity/README.md) | 3 | AI APIを不正な指令や情報の運び道に使う兆候を調べるか。 | 接続数だけを残し、通常利用に紛れた不正通信を評価できない。 |
| [C12.3.1](v1.0-c12.3.1-monitor-input-distribution-drift-by-data-type/README.md) | 1 | 入力の傾向の変化を、データの種類に合う方法で見つけるか。 | 件数だけ見て、質問などの構成の変化を見落とす。 |
| [C12.3.2](v1.0-c12.3.2-identify-and-flag-factually-wrong-contradictory-or-fabricated-outputs/README.md) | 2 | 誤り・矛盾・作り上げた情報を含む回答を見つけて印を付けるか。 | 自然な文章だから正しいとみなし、誤答を調べられない。 |
| [C12.3.3](v1.0-c12.3.3-track-hallucination-rate-over-time/README.md) | 2 | 誤答の疑いがある回答の割合を、時間を追って確認できるか。 | 印の件数だけ見て、検査した回答数や悪化の継続を見落とす。 |
| [C12.3.4](v1.0-c12.3.4-distinguish-unexplained-behavior-from-expected-drift/README.md) | 3 | 振る舞いの変化を、根拠のある想定内の変化と、説明できない変化に分けられるか。 | 同時期に変更記録があるだけで想定内と決める。 |
| [C12.4.1](v1.0-c12.4.1-evaluate-autonomous-action-triggers/README.md) | 2 | Agentが自ら行動を始める前に、行動の流れ・安全性・関係する脅威を評価するか。 | Scheduleが正規なら安全と決め、評価を飛ばす。 |
| [C12.4.2](v1.0-c12.4.2-audit-security-critical-proactive-actions/README.md) | 2 | 重要な自律操作の承認者・時刻・引数・判断結果を辿れるか。 | 「操作なし」だけを残し、拒否された提案を調べられない。 |
| [C12.4.3](v1.0-c12.4.3-log-kill-switch-activations-and-override-commands/README.md) | 2 | 緊急停止の発動と制限を上書きする指示を記録するか。 | 停止・再開の経緯が残らず、実際の停止とも混同する。 |
| [C12.5.1](v1.0-c12.5.1-record-complete-dataset-lineage/README.md) | 1 | Datasetと構成要素の変換・増強・結合を辿れるか。 | 最終Dataset名だけを残し、材料と加工が分からない。 |
| [C12.5.2](v1.0-c12.5.2-log-all-labeling-activities/README.md) | 1 | すべてのラベル付け活動を記録するか。 | 最終値だけを残し、付与・変更の経緯が分からない。 |
| [C12.5.3](v1.0-c12.5.3-immutable-audit-records-for-model-changes/README.md) | 2 | すべてのModel変更に変更不能な監査記録を作るか。 | Modelを変更した者が履歴も自由に書き換えられる。 |
| [C12.5.4](v1.0-c12.5.4-tag-ingested-documents-at-write-time/README.md) | 2 | 取込文書へ書込時にSource・Writer Identity・時刻を付けるか。 | 後付けの自己申告だけで文書の来歴を決める。 |

[normative]: https://github.com/OWASP/AISVS/blob/78775233666a2022dcfb82037e5e029116955c00/1.0/en/0x10-C12-Monitoring-and-Logging.md

開発順序は[Controls計画](../../plan.md)を参照する。各Controlを作成する際は、
正規要件と該当SectionのAISVS Researchを個別に確認する。
