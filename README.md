# Hiroaki Design Skills

**静けさの中に、鮮明な意思を。**

自分のデザイン判断を一つのリポジトリで育て、用途ごとに個別導入するスキル集です。現在はWatch用を含む7スキル。共通のカラーシステム **Atmospheric Graphite v1.0** と、用途に合う情報設計・操作・検証の基準をまとめています。

## 用途から選ぶ

| 用途 | スキル | 主に扱うこと |
| --- | --- | --- |
| ネイティブアプリ | [hiro-design-app](skills/hiro-design-app/SKILL.md) | OSの慣習、画面の流れ、入力と状態 |
| Watch・バンド | [hiro-design-watch](skills/hiro-design-watch/SKILL.md) | OS別の小画面、形状、回転・物理入力、常時表示、各情報面 |
| Webアプリ | [hiro-design-webapp](skills/hiro-design-webapp/SKILL.md) | 表、検索、入力、データ量、作業のしやすさ |
| Webサイト | [hiro-design-website](skills/hiro-design-website/SKILL.md) | 内容に合う第一印象、読み順、次の行動 |
| 調査レポート | [hiro-design-report](skills/hiro-design-report/SKILL.md) | 結論、比較条件、図表、出典、限界 |
| スライド | [hiro-design-slides](skills/hiro-design-slides/SKILL.md) | 発表の筋道、主張、根拠、視認性 |
| デザインレビュー | [hiro-design-review](skills/hiro-design-review/SKILL.md) | 問題の場所、影響、根拠、修正案と優先順位 |

各フォルダに共通ガイドと色の資料を同梱しているため、必要なスキル一つだけで使えます。サンプル集のインストールは必要ありません。

## 個別に導入する

プロジェクトのディレクトリで実行します。[Vercel Labsのskills CLI](https://github.com/vercel-labs/skills)を使用します。CLIの実行には、そのバージョンが要求するNode.jsが必要です。

```bash
# アプリ用
npx skills add hiroakissh/hiroaki-design-skills --skill hiro-design-app -a codex

# Apple WatchなどWatch・バンド用（単独で導入できます）
npx skills add hiroakissh/hiroaki-design-skills --skill hiro-design-watch -a codex

# Webアプリ用
npx skills add hiroakissh/hiroaki-design-skills --skill hiro-design-webapp -a codex

# 調査レポート用
npx skills add hiroakissh/hiroaki-design-skills --skill hiro-design-report -a codex

# 複数をまとめて選ぶ
npx skills add hiroakissh/hiroaki-design-skills --skill hiro-design-website hiro-design-slides hiro-design-review -a codex

# 導入せず一覧を確認する
npx skills add hiroakissh/hiroaki-design-skills --list
```

全プロジェクトで使いたい場合は `-g` を追加します。Claude Codeを対象にする場合は `-a claude-code` に変更します。スキルの標準形式と、利用環境のツール・実行条件は別に確認してください。

```text
$hiro-design-app iOSの設定画面を、主要な状態も含めて設計してください。
$hiro-design-watch Apple Watchの集中タイマーを、開始・中断・常時表示も含めて設計してください。
$hiro-design-webapp この管理画面の検索と一括操作を改善してください。
$hiro-design-report この調査結果を、比較と根拠が追えるレポートに整えてください。
$hiro-design-review この画面の改善点を、理由と優先順位付きでレビューしてください。
```

## 実際の表示サンプル

各スキルの判断を適用して作った実装例です。画像はブラウザで表示した結果を保存したものです。クリックすると拡大できます。

| 用途 | Light | Dark | 実装・条件・確認 |
| --- | --- | --- | --- |
| アプリ | [![アプリ Light](samples/hiro-design-app/preview-light.jpg)](samples/hiro-design-app/preview-light.jpg) | [![アプリ Dark](samples/hiro-design-app/preview-dark.jpg)](samples/hiro-design-app/preview-dark.jpg) | [実装HTML](samples/hiro-design-app/index.html) / [依頼文](samples/hiro-design-app/brief.md) / [確認記録](samples/hiro-design-app/review.md) |
| Watch | [![Watch Light](samples/hiro-design-watch/preview-light.jpg)](samples/hiro-design-watch/preview-light.jpg) | [![Watch Dark](samples/hiro-design-watch/preview-dark.jpg)](samples/hiro-design-watch/preview-dark.jpg) | [操作できるHTML](samples/hiro-design-watch/index.html) / [依頼文](samples/hiro-design-watch/brief.md) / [確認記録](samples/hiro-design-watch/review.md) |
| Webアプリ | [![Webアプリ Light](samples/hiro-design-webapp/preview-light.jpg)](samples/hiro-design-webapp/preview-light.jpg) | [![Webアプリ Dark](samples/hiro-design-webapp/preview-dark.jpg)](samples/hiro-design-webapp/preview-dark.jpg) | [実装HTML](samples/hiro-design-webapp/index.html) / [依頼文](samples/hiro-design-webapp/brief.md) / [確認記録](samples/hiro-design-webapp/review.md) |
| Webサイト | [![Webサイト Light](samples/hiro-design-website/preview-light.jpg)](samples/hiro-design-website/preview-light.jpg) | [![Webサイト Dark](samples/hiro-design-website/preview-dark.jpg)](samples/hiro-design-website/preview-dark.jpg) | [実装HTML](samples/hiro-design-website/index.html) / [依頼文](samples/hiro-design-website/brief.md) / [確認記録](samples/hiro-design-website/review.md) |
| 調査レポート | [![レポート Light](samples/hiro-design-report/preview-light.jpg)](samples/hiro-design-report/preview-light.jpg) | [![レポート Dark](samples/hiro-design-report/preview-dark.jpg)](samples/hiro-design-report/preview-dark.jpg) | [実装HTML](samples/hiro-design-report/index.html) / [依頼文](samples/hiro-design-report/brief.md) / [確認記録](samples/hiro-design-report/review.md) |
| スライド | [![スライド Light](samples/hiro-design-slides/preview-light.jpg)](samples/hiro-design-slides/preview-light.jpg) | [![スライド Dark](samples/hiro-design-slides/preview-dark.jpg)](samples/hiro-design-slides/preview-dark.jpg) | [3ページの実装HTML](samples/hiro-design-slides/index.html) / [依頼文](samples/hiro-design-slides/brief.md) / [確認記録](samples/hiro-design-slides/review.md) |
| レビュー | [![レビュー Light](samples/hiro-design-review/preview-light.jpg)](samples/hiro-design-review/preview-light.jpg) | [![レビュー Dark](samples/hiro-design-review/preview-dark.jpg)](samples/hiro-design-review/preview-dark.jpg) | [修正前後のHTML](samples/hiro-design-review/index.html) / [指摘一覧](samples/hiro-design-review/findings.md) / [依頼文](samples/hiro-design-review/brief.md) / [確認記録](samples/hiro-design-review/review.md) |

スライドの続き: [2ページ目 Light](samples/hiro-design-slides/slide-2-light.jpg) / [Dark](samples/hiro-design-slides/slide-2-dark.jpg)、[3ページ目 Light](samples/hiro-design-slides/slide-3-light.jpg) / [Dark](samples/hiro-design-slides/slide-3-dark.jpg)。

Watchの常時表示: [Lightページ](samples/hiro-design-watch/aod-light.jpg) / [Darkページ](samples/hiro-design-watch/aod-dark.jpg)。Watch内は両方ともOLED向けの暗い表示で、Light/Darkは比較ページの外観です。

### 操作して確認する

このリポジトリを取得して、次のコマンドを実行します。

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory samples
```

[ローカルのサンプル一覧](http://127.0.0.1:8765/index.html)をブラウザで開いてください。HTMLは単体でも開けます。GitHub上のHTMLリンクはソース表示になるため、動作確認にはローカルのファイルまたは上のサーバーを使います。

- アプリ: 一覧と詳細、プロジェクトの切り替え、通常・空・読込・エラーの表示、作業追加。
- Watch: 角型・丸型・縦長の比較、開始・中断・再開・完了、回転入力の模擬操作、情報面と常時表示、単色表示。時刻は固定で、時間は「5分進める」で進みます。
- Webアプリ: 検索、状態の絞り込み、0件表示、選択、プロジェクト追加。
- Webサイト: 用途別リンクと、説明から次の行動へ進む読み順。
- 調査レポート: 比較図表、元の数値、結論と制約。数値は架空で、実際の調査結果ではありません。
- スライド: 3ページをボタンまたは左右キーで移動。
- レビュー: 同じ内容の修正前後と、場所・理由・優先順位のある指摘。

アプリとWatchの例はブラウザ用UIプロトタイプです。ネイティブ実装・実機・Watchの電池や焼き付きの検証済み成果物ではありません。レポートとスライドはHTML形式で、PDF・PPTXの検証済み成果物を示すものではありません。

## Watchの公式ガイド

**2026-11-01確認、26資料**を[公式資料一覧](docs/watch-design-guides.md)に整理しています。Watch用スキル単独にも、日本語の要約・判断基準と[出典一覧](skills/hiro-design-watch/references/guide-index.md)、[機械可読な資料台帳](source/skills/hiro-design-watch/assets/watch-sources.json)を同梱します。第三者文書・図版の全文ミラーではありません。

| 対象 | 取り入れる内容・資料の範囲 |
| --- | --- |
| Apple watchOS | HIG、complication、Always On。画面用途とWidgetKit/旧ClockKitを区別 |
| Google Wear OS / Samsung | 丸型のadaptive design、回転・TalkBack、Ambient、Watch Face Studio。旧Tizenは別扱い |
| Garmin / Suunto | Connect IQのApp・Glance・Data Field等の区別、SuuntoPlusの運動中の画面とボタン |
| Huawei / Zepp / Xiaomi | Smart/Lite Wearable、Zeppの入力・文字盤・screen-off、Velaの丸型・角型・カプセル型 |
| Pebble / Bangle.js / InfiniTime | 物理ボタンとメニュー、配置・更新、既存アプリの操作資料。HIGと実装資料を区別 |
| HONOR / Fitbit / 周辺API | HONOR詳細は取得限定、Fitbitは旧SDK。Polar・COROS・Withingsの連携APIはWatch UIガイドとして扱わない |

世界の主要な公開資料を横断した調査であり、全メーカー・全機種を網羅したものではありません。Huaweiの詳細ページ、HONOR、Suunto Editor同梱資料などの未取得範囲は一覧に記録しています。機種・SDK・公開要件は実装時に再確認します。

## Atmospheric Graphite v1.0

「08 Acid Graphite」「13 Sky Diary」「18 Plum Cinema」を統合した、指定されたオリジナルの色値を保持しています。

| 役割 | Light — Sky × Graphite | Dark — Plum × Electric |
| --- | --- | --- |
| Background | `#EAF3F6` | `#221C2C` |
| Surface | `#FFFFFF` | `#302838` |
| Text | `#20282B` | `#F6F0EB` |
| Primary | `#235F75` | `#B9A1DE` |
| Accent | `#D8F15A` | `#D8F15A` |

全カラートークン: [YAML](tokens/colors.yaml) / [JSON](tokens/colors.json) / [CSS変数](tokens/colors.css)。[カラーガイド](source/foundations/color-guidelines.md)と[コントラスト検査結果](docs/color-contrast.md)も参照できます。

- 色は役割を持つトークンで指定します。
- ライムはブランド表現に使い、成功・エラーに流用しません。
- 状態は文字・形・アイコンなどでも伝えます。
- Light/Darkを確認し、可読性と操作の理解を優先します。
- 75% / 20% / 5%は初期の目安であり、固定の面積規則ではありません。

文字、主操作、境界、フォーカス、意味色などの58組を数値検査しています。通常文字4.5:1、必要なUI図形3:1を基準にしていますが、WCAG 2.2 AA全体の適合や、任意の全色ペアの使用を保証するものではありません。淡い面上のライムやスカイには使用制限があります。

disabled・pressed・selectedなどの状態別トークン、個人の標準書体、余白・角丸・動きの固定値は未確定です。`onAccent` は既存色への実装用エイリアスで、新しいHEX値ではありません。

## スキルとサンプルを一緒に更新する

**スキルを変えたら、対応サンプルを毎回作り直し、Light/Darkを確認して、同じ変更に含めます。** 共通方針の変更時は影響する全サンプルを更新します。

```bash
# 元データから配布スキルとトークンを生成する
python3 scripts/build-skills.py

# 変更後のスキルを読み、サンプルのテンプレートへ反映してからHTMLを生成する
python3 scripts/render-samples.py

# 表示・操作を確認し、画像とreview.mdを更新した後に記録する
python3 scripts/check-samples.py record hiro-design-app --note '適用した変更と確認内容'

# 生成物・配色・参照・サンプル更新漏れを確認する
python3 scripts/build-skills.py --check
python3 scripts/render-samples.py --check
python3 scripts/check-colors.py
python3 scripts/validate-skills.py
python3 scripts/check-samples.py check
python3 -m unittest discover -s tests -v
node tests/watch-state.test.cjs
```

生成処理はスキル本文を解釈するAIではありません。スキルの適用と表示確認は作業する人・エージェントが行い、検査は入力と成果物の更新漏れを検出します。入力や成果物が変わった場合、確認記録を更新せずにハッシュだけ付け直すことはできません。

詳しくは[サンプル更新ガイド](docs/sample-workflow.md)と[AGENTS.md](AGENTS.md)を参照してください。

## 管理する場所

```text
source/profile.md       個人の方針と、決定済み・未確定の区別
source/foundations/     共通の知識とカラートークンの正本
source/skills/          用途別の編集元
skills/                生成した個別導入用スキル
tokens/                共有用YAML・JSON・CSSの生成物
samples/               依頼文・データ・実装・画像・確認記録
scripts/               生成・検査
evals/                 代表的な依頼と評価観点
docs/                  構想・運用・配色の検査結果
```

生成物を直接編集せず、元データを直して再生成します。ソースは一か所で管理し、配布スキルには必要な内容だけを含めます。

## 参考資料

[Emil KowalskiのSkills](https://github.com/emilkowalski/skills)のUIの細部・動きの判断、[Damir Sokolovskyのunslop](https://github.com/heydamir/unslop)の観察と段階的な改善、[Anthropicのfrontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design)の内容に沿う表現と自己評価を参考にしています。

参考元の意見をそのまま個人ルールにはせず、指定パレットと用途に合わせて整理しています。参考元・作者・参照コミットは[出典と取り入れ方](source/foundations/sources.md)に記載しています。第三者の画像や文書生成エンジンは同梱していません。
