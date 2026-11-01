# 手首で使う画面を設計する

Watchアプリ、文字盤上の情報、Tile・Glance・運動中のデータ表示を設計・実装・改善する。対象OS・機種と画面用途から始め、スマートフォンのUIを縮小しない。

[個人方針](references/profile.md) と [配色](references/colors.md) を使う。OSが制御する文字盤・単色表示・低電力表示ではプラットフォームの制約を優先し、ブランド色の対応と例外を記録する。書体・寸法をサンプルから個人の固定ルールへ昇格させない。

## 対象を決める

既存プロジェクトからOS、機種、最小画面、入力、表示方式、SDKを確認する。分からない点のうち実装方針を変えるものだけ確認する。

- **画面用途**: フルアプリ、文字盤、complication、Tile、Glance、data field、通知は別のAPI・制約。Apple Watch用に任意の全面文字盤を提供できると約束しない。
- **形状・表示**: 丸型、角型、縦長バンド、AMOLED/OLED、MIPや単色・少色表示を区別する。同じメーカーでもOSが違えば別設計として扱う。
- **入力・継続**: タッチ、Crown・ベゼル・回転、物理ボタン、読み上げ、電話との接続、画面を離れた後の継続を確認する。

[公式資料の索引](references/guide-index.md) から対象だけを読む。出典の状態が `legacy` なら新規環境の仕様に使わず、`limited` なら未取得の詳細を補って断言しない。寸法や更新頻度は対象SDKの現行資料で再確認し、pt・dp・pxを横断して一つの数値にしない。

出典を更新・再検証するときは [資料台帳](assets/watch-sources.json) の確認日・取得範囲も確認する。

## 対象別に読む

- Apple watchOS、Google Wear OS、現行Galaxy Watch: [watchOS / Wear OS](references/watchos-wearos.md)。Samsungの旧Tizen資料とは区別する。
- Huawei、Zepp/Amazfit、Xiaomi Vela、HONOR: [アジアのプラットフォーム](references/asia.md)。地域・機種・公開範囲を確認する。
- Garmin、Suunto、Pebble、Bangle.js、InfiniTime、旧Fitbit: [スポーツ・オープン環境](references/sports-open.md)。開発・操作資料をHIGと同一視しない。

## 制作と確認

一目で分かる主情報と主要操作を選ぶ。長い入力や初期設定を電話へ渡す場合も、Watch単独でできること・接続が必要なことを表示する。曲面の上下端へ文字や操作を詰めず、標準部品と対象OSの戻る・回転操作を尊重する。

通常・実行中・中断・完了と、必要な未取得・古いデータ・権限拒否・切断を設計する。色だけで状態を区別しない。常時表示では情報の鮮度、秘匿、省電力を別に検討する。単に不透明度を下げた画面をAODとして完成扱いしない。

実装に応じて [Watchの確認項目](references/watch-checks.md) と [共通アクセシビリティ](references/accessibility.md) を使う。最小画面、長い日本語、文字拡大、物理入力、通常表示と低電力表示の往復を確認し、変更理由・検証環境・未確認の実機項目を伝える。HTMLモックの確認から、電池寿命・焼き付き・実機入力・OS審査への適合を報告しない。
