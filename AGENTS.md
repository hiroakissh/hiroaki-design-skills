# このプロジェクトの作業ルール

## 方針と配布

- 個人の配色は **Atmospheric Graphite v1.0**。正本は `source/foundations/colors.json`。指定の15色×2モードを保持する。
- 個人の標準書体と状態別の色、余白・角丸・動きの固定値は未確定。サンプルの実装値を個人ルールとして確定しない。
- 編集元は `source/`。配布物は `skills/`、共有する色は `tokens/`。生成物の手編集を避け、`python3 scripts/build-skills.py` で再生成する。
- 各スキルは単独導入できるようにする。配布フォルダの外へのローカル参照や、サンプル集への必須依存を持たせない。
- Watchの公式資料は `source/skills/hiro-design-watch/assets/watch-sources.json` に出典・確認日・対象・取得範囲を記録し、索引を生成する。現行・旧環境・取得限定と、デザイン資料・実装資料・周辺APIを区別する。
- READMEは日本語で書く。参考情報は出典と取り入れ方を残し、ユーザーの配色・依頼を優先する。

## サンプルの更新は必須

- スキルの本文・参考資料・スクリプト・資産を変えたら、対応サンプルを毎回再実行し、表示確認・画像・`review.md` を同じ変更に含める。
- `source/profile.md`、`source/foundations/`、共通サンプル実装の変更時は、影響する全サンプルを更新する。初期の検査は共通変更を全件の入力変更として扱う。
- 全実装スキルに最低1件のサンプルを登録する。`samples/catalog.json` に固定依頼文、実装、Light/Dark両方のプレビュー、確認記録を指定し、READMEからリンクする。
- 通常の更新では依頼文・データ・比較条件を保つ。変える必要があるときは理由を確認記録に残す。
- 自然言語のスキルは描画スクリプトだけでは適用されない。変更後のスキルを読み、サンプルのテンプレートや実装へ判断を反映してから再生成する。
- 画像は最終成果物を実際に表示して取得する。入力や成果物のハッシュを付け直すだけでは完了しない。
- 外観が同じ場合も再生成・再確認し、理由を `review.md` に記す。
- アニメーションや操作を扱うときは、必要な状態・操作も確認する。レビューの例では入力と修正前後、指摘の根拠を保持する。
- 静止モック、HTMLプロトタイプ、ネイティブ実装、PDF/PPTXなどの形式と確認範囲を区別する。実施していない動作検証やスキル適用を報告しない。

## 検証

```bash
python3 scripts/build-skills.py --check
python3 scripts/render-samples.py --check
python3 scripts/check-colors.py
python3 scripts/validate-skills.py
python3 scripts/check-samples.py check
python3 -m unittest discover -s tests -v
node tests/watch-state.test.cjs
```

確認を終えたサンプルだけを記録する。

```bash
python3 scripts/check-samples.py record hiro-design-app --note '再実行と表示確認の具体的な内容'
```

全件を確認した場合のみ `--all` を使う。検査は更新の整合性を確認するもので、デザイン品質やWCAG全体の適合を証明するものではない。手順は `docs/sample-workflow.md` を参照する。
