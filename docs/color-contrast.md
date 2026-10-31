# Atmospheric Graphite v1.0 コントラスト検査

正本: `source/foundations/colors.json`。元の15色×2モードは変更せず、使用する組み合わせを検査する。

通常文字4.5:1、境界・フォーカス3:1を丸める前の値で判定する。下表は表示時のみ小数第2位まで丸めている。

| モード | 前景 | 背景 | 比率 | 基準 | 結果 |
| --- | --- | --- | ---: | ---: | --- |
| light | `textPrimary` | `background` | 13.32:1 | 4.5:1 | 合格 |
| light | `textPrimary` | `surface` | 15.00:1 | 4.5:1 | 合格 |
| light | `textPrimary` | `surfaceRaised` | 13.92:1 | 4.5:1 | 合格 |
| light | `textSecondary` | `background` | 5.67:1 | 4.5:1 | 合格 |
| light | `textSecondary` | `surface` | 6.38:1 | 4.5:1 | 合格 |
| light | `textSecondary` | `surfaceRaised` | 5.92:1 | 4.5:1 | 合格 |
| light | `actionPrimary` | `background` | 6.29:1 | 4.5:1 | 合格 |
| light | `actionPrimary` | `surface` | 7.08:1 | 4.5:1 | 合格 |
| light | `actionPrimary` | `surfaceRaised` | 6.57:1 | 4.5:1 | 合格 |
| light | `expressionPlum` | `background` | 6.45:1 | 4.5:1 | 合格 |
| light | `expressionPlum` | `surface` | 7.26:1 | 4.5:1 | 合格 |
| light | `expressionPlum` | `surfaceRaised` | 6.74:1 | 4.5:1 | 合格 |
| light | `success` | `background` | 6.47:1 | 4.5:1 | 合格 |
| light | `success` | `surface` | 7.28:1 | 4.5:1 | 合格 |
| light | `success` | `surfaceRaised` | 6.75:1 | 4.5:1 | 合格 |
| light | `warning` | `background` | 6.30:1 | 4.5:1 | 合格 |
| light | `warning` | `surface` | 7.09:1 | 4.5:1 | 合格 |
| light | `warning` | `surfaceRaised` | 6.58:1 | 4.5:1 | 合格 |
| light | `error` | `background` | 6.04:1 | 4.5:1 | 合格 |
| light | `error` | `surface` | 6.80:1 | 4.5:1 | 合格 |
| light | `error` | `surfaceRaised` | 6.31:1 | 4.5:1 | 合格 |
| light | `outlineStrong` | `background` | 3.49:1 | 3:1 | 合格 |
| light | `outlineStrong` | `surface` | 3.93:1 | 3:1 | 合格 |
| light | `outlineStrong` | `surfaceRaised` | 3.64:1 | 3:1 | 合格 |
| light | `focus` | `background` | 6.05:1 | 3:1 | 合格 |
| light | `focus` | `surface` | 6.81:1 | 3:1 | 合格 |
| light | `focus` | `surfaceRaised` | 6.32:1 | 3:1 | 合格 |
| light | `onActionPrimary` | `actionPrimary` | 7.08:1 | 4.5:1 | 合格 |
| light | `onAccent (alias)` | `accent` | 11.89:1 | 4.5:1 | 合格 |
| dark | `textPrimary` | `background` | 14.63:1 | 4.5:1 | 合格 |
| dark | `textPrimary` | `surface` | 12.50:1 | 4.5:1 | 合格 |
| dark | `textPrimary` | `surfaceRaised` | 10.55:1 | 4.5:1 | 合格 |
| dark | `textSecondary` | `background` | 9.45:1 | 4.5:1 | 合格 |
| dark | `textSecondary` | `surface` | 8.08:1 | 4.5:1 | 合格 |
| dark | `textSecondary` | `surfaceRaised` | 6.82:1 | 4.5:1 | 合格 |
| dark | `actionPrimary` | `background` | 7.25:1 | 4.5:1 | 合格 |
| dark | `actionPrimary` | `surface` | 6.20:1 | 4.5:1 | 合格 |
| dark | `actionPrimary` | `surfaceRaised` | 5.23:1 | 4.5:1 | 合格 |
| dark | `expressionPlum` | `background` | 7.25:1 | 4.5:1 | 合格 |
| dark | `expressionPlum` | `surface` | 6.20:1 | 4.5:1 | 合格 |
| dark | `expressionPlum` | `surfaceRaised` | 5.23:1 | 4.5:1 | 合格 |
| dark | `success` | `background` | 10.76:1 | 4.5:1 | 合格 |
| dark | `success` | `surface` | 9.20:1 | 4.5:1 | 合格 |
| dark | `success` | `surfaceRaised` | 7.77:1 | 4.5:1 | 合格 |
| dark | `warning` | `background` | 10.60:1 | 4.5:1 | 合格 |
| dark | `warning` | `surface` | 9.06:1 | 4.5:1 | 合格 |
| dark | `warning` | `surfaceRaised` | 7.65:1 | 4.5:1 | 合格 |
| dark | `error` | `background` | 7.90:1 | 4.5:1 | 合格 |
| dark | `error` | `surface` | 6.75:1 | 4.5:1 | 合格 |
| dark | `error` | `surfaceRaised` | 5.70:1 | 4.5:1 | 合格 |
| dark | `outlineStrong` | `background` | 5.22:1 | 3:1 | 合格 |
| dark | `outlineStrong` | `surface` | 4.46:1 | 3:1 | 合格 |
| dark | `outlineStrong` | `surfaceRaised` | 3.77:1 | 3:1 | 合格 |
| dark | `focus` | `background` | 13.10:1 | 3:1 | 合格 |
| dark | `focus` | `surface` | 11.20:1 | 3:1 | 合格 |
| dark | `focus` | `surfaceRaised` | 9.46:1 | 3:1 | 合格 |
| dark | `onActionPrimary` | `actionPrimary` | 7.25:1 | 4.5:1 | 合格 |
| dark | `onAccent (alias)` | `accent` | 13.10:1 | 4.5:1 | 合格 |

## 使用を制限する組み合わせ

- Lightの `accent` / `background` は 1.12:1。淡い面上の小さな文字や、単独で状態を伝える必須図形に使わない。
- Lightの `expressionSky` / `surface` は 1.89:1。装飾・区分に使い、通常文字や必須のグラフ線には流用しない。
- `outlineStrong` は境界用。通常文字の役割には使わない。
- `onAccent` は既存トークンへのエイリアスであり、新しい色値ではない。

## 検証の限界

この検査は列挙した不透明色のペアの計算である。全色の任意の組み合わせ、透過・画像との合成、OS実機、すべての状態、WCAG 2.2 AA全体の適合を証明しない。disabled・pressed・selectedなどの状態別トークンは未確定。

基準: [文字のコントラスト](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)、[非テキストのコントラスト](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)。
