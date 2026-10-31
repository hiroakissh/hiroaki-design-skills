# サンプルの作成・更新

## 目的と現在の形式

READMEから、スキルの適用結果を見て選べるようにする。スキルを変えたら、毎回同じ依頼文とデータで作り直し、Light/Darkの表示を確認する。

現在の6用途は、各スキルの判断に沿って作成したHTML実装例。アプリはブラウザ用UIプロトタイプ、調査レポートとスライドはHTMLであり、ネイティブ実機・PDF・PPTXの検証済み成果物ではない。形式を拡張するときは、その成果物と実際の書き出しも検証する。

## ファイルの対応

```text
samples/
├── index.html                    # ローカルで開く一覧
├── catalog.json                  # スキルとの対応と確認対象
├── freshness.json                # 確認時点の入力・成果物のハッシュ
├── shared/                       # サンプル共通のCSS・JavaScript
└── <skill-name>/
    ├── brief.md                  # 固定依頼文・条件
    ├── data.json                 # 必要な固定データ
    ├── template.html             # スキルの判断を反映する編集元
    ├── index.html                # 単体でも開ける生成HTML
    ├── preview-light.jpg         # 実際のブラウザ表示
    ├── preview-dark.jpg
    └── review.md                 # 適用内容・確認結果・制約
```

スライドには続きのページ、レビューには指摘一覧も保持する。サンプルの追加時は、成果物とプレビューをREADMEからたどれるようにする。

`catalog.json` の `inputs` は固定依頼文・データ・テンプレート・描画処理、`outputs` は実装・プレビュー・確認記録などを指定する。`artifact` は実装、`previews.light` と `previews.dark` は別々の画像を指定する。`preview` は一覧用の代表画像。

`status: prototype` は実スキル適用前の構成モック、`status: skill` は実スキルを適用したサンプル。実装済みスキルに構成モックのままの記録を対応させない。

## 毎回の手順

1. スキルと共通方針を変更し、配布物を再生成する。
2. 変更後のスキルを明示して固定依頼文を再実行する。現在の構成では、スキルの判断を `template.html` や共通実装に反映する。
3. HTMLを再生成する。**描画処理はスキル本文を解釈するAIではない**ため、コマンドの実行だけでスキル適用済みとしない。
4. Light/Darkを実際に表示し、必要な操作、狭い画面、日本語、図表などを確認する。
5. 実表示から画像を保存し、`review.md` に適用した判断、実施した確認、残る制約を記す。外観が変わらない場合も理由を残す。
6. 確認した時点の入力・成果物を記録し、検査を通してスキルと一緒に変更する。

```bash
python3 scripts/build-skills.py
python3 scripts/render-samples.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory samples
```

比較条件はデスクトップ幅1200 CSS px、モバイル確認幅390 CSS px。プレビューは内容に応じた全高を取得する。通常の更新ではこれらの条件を保ち、変更時は理由を記す。

画像の保存先は `samples/<skill-name>/preview-light.jpg` と `preview-dark.jpg`。ブラウザがPNGを出力する場合は拡張子と登録を合わせる。スライドは表紙だけでなく全ページを確認する。

```bash
python3 scripts/check-samples.py record hiro-design-app --note '適用した変更と確認した内容'

# 全件を再実行・確認した場合のみ
python3 scripts/check-samples.py record --all --note '共通方針の変更を全用途に適用して表示・操作を確認'
```

## 検査

ローカルとGitHub Actionsで同じ検査を行う。Pythonの標準ライブラリだけで実行できる。

- 配布スキルとトークンの生成漏れを検出する。
- HTML生成漏れ、色の使用ペア、単独配布時の参照を確認する。
- 個別スキルの変更は、対応するサンプルの更新を要求する。
- 共通方針・共通資料の変更は、登録済み全サンプルの更新を要求する。
- 実装スキルにサンプルがない、Light/Dark画像が欠けている、READMEリンクがない場合は失敗する。
- 入力や成果物が変わった後に `review.md` を更新せず記録だけ付け直すことを拒否する。

```bash
python3 scripts/build-skills.py --check
python3 scripts/render-samples.py --check
python3 scripts/check-colors.py
python3 scripts/validate-skills.py
python3 scripts/check-samples.py check
python3 -m unittest discover -s tests -v
```

ハッシュ・記録時刻・メモは更新の整合性を示す。適用の忠実さ、実表示の品質、操作の正しさ、アクセシビリティ全体は、成果物を見て確認する。
