# Watchの公式デザイン資料

確認日: 2026-11-01 / 原本の言語は各項目に記載。

世界の主要なWatchプラットフォームを横断した調査。Apple、Google、Samsung、Garmin、Huawei、Zepp、Xiaomi、Suunto、Pebbleとオープン環境を中心に、公式のデザイン・開発・操作資料を区別して整理した。全世界の全メーカー・機種の網羅や、全対象での実機検証を意味しない。

本文を確認できた資料を日本語で要約し、適用範囲と取得上の制約を記録する。公式文書・図版・フォントの全文複製ではない。リンク先の改訂・SDK・機種の対応は実装時に再確認する。

`design-guide` はデザイン資料、`implementation` は開発・操作資料、`overview` は概要、`boundary` は連携API等を設計ガイドと誤認しないための境界資料。`current` は現在の参照先として整理した資料で、記事内の全APIが最新という保証ではない。`legacy` は新規製品へ流用しない。`limited` は詳細の取得が不完全なため、その詳細を設計根拠にしない。

## 取得・参照した資料

### apple-watchos — watchOS

[Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos) — Apple

- 分類: `design-guide` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: watchOSアプリ・関連する情報面
- 取り入れる判断: 短い操作、Crown、浅い階層、独立した機能。
- 確認方法・制約: 公式のView Markdown本文を取得。HTML版はJavaScript描画。

### apple-always-on — watchOS

[Always On](https://developer.apple.com/design/human-interface-guidelines/always-on) — Apple

- 分類: `design-guide` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: Always On対応端末。watchOSに関係する部分
- 取り入れる判断: 秘匿、重要情報、位置の継続と控えめな更新。
- 確認方法・制約: 公式Markdown本文を取得。iPhone向け記述とは区別。

### apple-complications — watchOS

[Complications](https://developer.apple.com/design/human-interface-guidelines/complications) — Apple

- 分類: `design-guide` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: complicationのfamily・tinted表示・更新
- 取り入れる判断: familyに合う値、placeholder、deep link、WidgetKitの現行方針。
- 確認方法・制約: 公式Markdown本文を取得。旧ClockKit記述も含むため対応OSを確認。

### wear-design — Wear OS

[Design for wearables](https://developer.android.com/design/ui/wear/guides/get-started/design-for-wearables) — Google

- 分類: `design-guide` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: Wear OSの情報設計・各surface
- 取り入れる判断: 一目の確認、短い操作、丸型と電力への配慮。
- 確認方法・制約: 公式本文を確認。API詳細は別資料。

### wear-adaptive — Wear OS

[Adaptive design: Overview](https://developer.android.com/design/ui/wear/guides/foundations/adaptive-design) — Google

- 分類: `design-guide` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: Wear OSの丸型・画面サイズ・文字拡大
- 取り入れる判断: 小画面から設計し、外周余白を形状と大きさに合わせる。
- 確認方法・制約: 公式本文を確認。記載dp値を他OSへ一般化しない。

### wear-accessibility — Wear OS

[Accessibility on Wear OS](https://developer.android.com/training/wearables/accessibility) — Google

- 分類: `design-guide` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: 文字サイズ・回転・TalkBack・タッチ領域
- 取り入れる判断: 標準部品、読み順、回転入力とタッチ領域の文脈を確認。
- 確認方法・制約: 公式本文を確認。48dp推奨と限定的な40dp例外を区別。

### wear-ambient — Wear OS

[Always-on apps and system ambient mode](https://developer.android.com/training/wearables/always-on) — Google

- 分類: `implementation` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: Wear OSアプリのInteractive/Ambient遷移
- 取り入れる判断: 黒い領域、時刻、古い値のplaceholder、動きと更新の削減。
- 確認方法・制約: 公式本文を確認。OS世代で変わる入力・更新・焼き付き対策を実装時に再確認。

### samsung-faces — Samsung / Wear OS

[Watch Face Studio: Optimization tips](https://developer.samsung.com/watch-face-studio/user-guide/performance-tips.html) — Samsung

- 分類: `design-guide` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: Watch Face Studioで作成する文字盤
- 取り入れる判断: 暗い背景、更新・リソース・アニメーションの負荷を検討。
- 確認方法・制約: 公式本文を確認。ツール固有の値をアプリ全般へ流用しない。

### samsung-tizen — Samsung / Tizen

[One UI Watch Tizen: Principle](https://developer.samsung.com/one-ui-watch-tizen/principle.html) — Samsung

- 分類: `design-guide` / 状態: `legacy` / 言語: English
- 確認日: 2026-11-01
- 対象: Tizenベースの旧Galaxy Watch
- 取り入れる判断: 短い確認と操作の考え方のみ、旧製品の保守として参照。
- 確認方法・制約: 公式本文とTizenアプリ配布終了の告知を確認。Wear OSの現行仕様ではない。

### garmin-types — Garmin Connect IQ

[Developing the Concepts](https://developer.garmin.com/connect-iq/articles/user-experience-guidelines/Developing_the_Concepts.html) — Garmin

- 分類: `design-guide` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: Device App・Data Field・Watch Face・Glance等
- 取り入れる判断: 目的からアプリ種別を選び、最初に主情報を示す。
- 確認方法・制約: 公式UX記事の本文を取得。旧widget/API levelの記述を含み、最新API対応は再照合。

### huawei-entry — HarmonyOS / Huawei

[Wearables: Get started](https://developer.huawei.com/consumer/en/multidevice/wearables/get-started/) — Huawei

- 分類: `overview` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: Smart Wearable / Lite Wearable
- 取り入れる判断: 短い操作、Crown、電話との継続と対象ランタイムの区別。
- 確認方法・制約: 公式入門本文を確認。詳細な寸法ガイドではない。

### huawei-design — HarmonyOS / Huawei

[Wearable design overview](https://developer.huawei.com/consumer/en/doc/design-guides/wearable-overview-0000002197410498) — Huawei

- 分類: `design-guide` / 状態: `limited` / 言語: English
- 確認日: 2026-11-01
- 対象: Huawei入門から案内される詳細設計ガイド
- 取り入れる判断: 実装時の再取得先として保持。未取得の寸法・部品仕様は採用しない。
- 確認方法・制約: 公式入門からリンクを確認したが詳細取得はタイムアウト。本文未取得。

### zepp-touch — Zepp OS / Amazfit

[Screen touch control](https://docs.zepp.com/docs/designs/interaction/screen-touch-control/) — Zepp Health

- 分類: `design-guide` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: Zepp OS v3+のアプリ入力
- 取り入れる判断: 標準ジェスチャーの意味を保ち、独自操作と競合させない。
- 確認方法・制約: 公式本文を確認。物理キー・Crownと対象APIは機種ごとに確認。

### zepp-faces — Zepp OS / Amazfit

[Watchface](https://docs.zepp.com/docs/designs/customization/watchface/) — Zepp Health

- 分類: `design-guide` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: Zepp OS v3+の文字盤
- 取り入れる判断: 主情報の階層と外周の欠けを確認。
- 確認方法・制約: 公式本文を確認。記載px値はこの文字盤ガイドの範囲のみ。

### zepp-screen-off — Zepp OS / Amazfit

[Screen-off mode](https://docs.zepp.com/docs/designs/customization/screen-off-mode/) — Zepp Health

- 分類: `design-guide` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: Zepp OS v3+のscreen-off文字盤
- 取り入れる判断: 黒背景、秒を省略、通常表示との位置の一致。
- 確認方法・制約: 公式本文を確認。アプリ全体のAmbient仕様としては扱わない。

### xiaomi-shapes — Xiaomi Vela

[Multi-screen adaptation](https://iot.mi.com/vela/quickapp/en/guide/design/multi-screens.html) — Xiaomi

- 分類: `design-guide` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: Vela Quick Appの丸型・角型・カプセル型
- 取り入れる判断: 形状ごとに情報量・配置と曲面の安全な領域を変える。
- 確認方法・制約: 公式英語本文を確認。同ブランドのWear OS製品は別対象。

### honor-themes — HONOR

[Theme Center Business Overview](https://developer.honor.com/en/doc/guides/100782) — HONOR

- 分類: `overview` / 状態: `limited` / 言語: English
- 確認日: 2026-11-01
- 対象: テーマ・文字盤・AOD等の概要
- 取り入れる判断: 配布対象を把握する入口。詳細仕様やHuawei互換性は未確認。
- 確認方法・制約: 公式検索インデックスで概要を確認。本文は描画できず、包括的なHIGは未取得。

### suunto-sports — SuuntoPlus

[SuuntoPlus Sports Apps](https://apizone.suunto.com/suuntoplus-sports-apps) — Suunto

- 分類: `overview` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: 運動中のSports Appsの画面・ボタン・設定
- 取り入れる判断: 独立したワークアウト画面と、電話側の設定を分ける。
- 確認方法・制約: 公式本文を確認。汎用アプリのHIGではない。

### suunto-editor — SuuntoPlus

[SuuntoPlus Editor](https://apizone.suunto.com/suuntoplusEditor) — Suunto

- 分類: `overview` / 状態: `limited` / 言語: English
- 確認日: 2026-11-01
- 対象: Editorと同梱開発資料への案内
- 取り入れる判断: 実装時に同梱資料と実機を使って詳細を確認する。
- 確認方法・制約: 公式案内を確認。Editor同梱資料の全文は今回未取得。

### pebble-design — Pebble / Core Devices

[Recommended design and interaction](https://developer.repebble.com/guides/design-and-interaction/recommended/) — Core Devices

- 分類: `design-guide` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: Pebbleのボタン・メニュー・情報階層
- 取り入れる判断: 主要操作を先に置き、ボタンの意味と反応を示す。
- 確認方法・制約: 公開本文を確認。旧SDK由来の記述を含む。色だけの情報伝達は取り入れない。

### bangle-layout — Bangle.js

[Bangle.js Layout library](https://www.espruino.com/Bangle.js%20Layout) — Espruino

- 分類: `implementation` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: モデル別のLayout配置・更新
- 取り入れる判断: widget領域、最大文字幅、変更箇所の再描画を検討。
- 確認方法・制約: 公式本文を確認。共通HIGや電力検証結果ではない。

### infinitime-apps — PineTime / InfiniTime

[Applications](https://github.com/InfiniTimeOrg/InfiniTime/blob/main/doc/gettingStarted/Applications.md) — InfiniTime project

- 分類: `implementation` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: 既存アプリの操作と制約
- 取り入れる判断: ボタン・戻る・画面を離れた後の継続を対象版で確認。
- 確認方法・制約: 公式プロジェクトの本文を確認。操作マニュアルでありHIGではない。

### fitbit-checklist — Fitbit SDK

[Fitbit Publishing Checklist](https://dev.fitbit.com/static/publishing-checklist.pdf) — Fitbit

- 分類: `design-guide` / 状態: `legacy` / 言語: English
- 確認日: 2026-11-01
- 対象: 旧Fitbit SDK製品の公開前確認
- 取り入れる判断: 未取得・権限拒否・デバイス差の確認観点を参考にする。
- 確認方法・制約: 公式PDFの本文を確認。新規製品・配布の対応を保証しない。

### polar-boundary — Polar

[Polar BLE SDK](https://github.com/polarofficial/polar-ble-sdk) — Polar

- 分類: `boundary` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: 電話側からのBLE計測・連携SDK
- 取り入れる判断: Watch用HIGを取得した証拠と混同しない。
- 確認方法・制約: 公式公開READMEで概要を確認。Watch画面の設計ガイドは今回未取得。

### coros-boundary — COROS

[Submit an API Application](https://support.coros.com/hc/en-us/articles/17085887816340-Submit-an-API-Application) — COROS

- 分類: `boundary` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: Partner APIのデータ共有・申請
- 取り入れる判断: 連携APIとWatch上のUI設計を区別する。
- 確認方法・制約: 公式ヘルプの検索本文で概要を確認。Watch UIガイドは今回未取得。

### withings-boundary — Withings

[Withings Mobile SDK](https://developer.withings.com/sdk/) — Withings

- 分類: `boundary` / 状態: `current` / 言語: English
- 確認日: 2026-11-01
- 対象: iOS/Android側のデバイス連携
- 取り入れる判断: Mobile SDKをWatchアプリのデザイン仕様として扱わない。
- 確認方法・制約: 公式ページの検索本文で概要を確認。Watch UIガイドは今回未取得。

## 未取得の範囲と更新

HONORの詳細、Huawei詳細ページ、Suunto Editor同梱の詳細仕様には取得制限がある。Polar・COROS・Withingsは周辺APIの入口までで、Watch UIガイドは未取得。非公開のOEM/RTOS、地域限定ポータル、契約・ログインが必要な資料、ここにないメーカーは未調査として扱う。「公開資料が存在しない」とは断定しない。

対象機種が追加されたら、メーカー名だけで共通化せずOS・画面用途・入力・表示方式を調べる。資料のURL、分類、確認日、取得範囲と適用先を更新し、スキルとサンプルを同じ変更で再確認する。
