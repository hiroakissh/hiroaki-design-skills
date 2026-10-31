"""Atmospheric Graphite exports and WCAG relative-luminance checks."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROLES = {
    "background", "surface", "surfaceRaised", "textPrimary", "textSecondary",
    "actionPrimary", "onActionPrimary", "accent", "expressionPlum", "expressionSky",
    "outlineStrong", "focus", "success", "warning", "error",
}


def load(root=ROOT):
    document = json.loads((root / "source/foundations/colors.json").read_text(encoding="utf-8"))
    system = document["design_system"]
    if set(system["colors"]) != {"light", "dark"}:
        raise ValueError("Both light and dark palettes are required")
    for mode, colors in system["colors"].items():
        if set(colors) != ROLES:
            raise ValueError("Unexpected color roles in " + mode)
        if any(not re.fullmatch(r"#[0-9A-F]{6}", value) for value in colors.values()):
            raise ValueError("Use six-digit uppercase HEX in the canonical palette")
    return document


def luminance(color):
    channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
    return sum(channel * weight for channel, weight in zip(linear, (0.2126, 0.7152, 0.0722)))


def contrast(first, second):
    darker, lighter = sorted((luminance(first), luminance(second)))
    return (lighter + 0.05) / (darker + 0.05)


def kebab(name):
    return re.sub(r"([a-z])([A-Z])", r"\1-\2", name).lower()


def css(document):
    def block(mode):
        lines = ["  --color-{}: {};".format(kebab(name), value) for name, value in document["design_system"]["colors"][mode].items()]
        role = "text-primary" if mode == "light" else "on-action-primary"
        lines += ["  --color-on-accent: var(--color-" + role + ");", "  color-scheme: " + mode + ";"]
        return "\n".join(lines)
    return "/* Generated from source/foundations/colors.json. State colors remain undecided. */\n:root, [data-theme=\"light\"] {\n" + block("light") + "\n}\n[data-theme=\"dark\"] {\n" + block("dark") + "\n}\n@media (prefers-color-scheme: dark) {\n  :root:not([data-theme]) {\n" + block("dark") + "\n  }\n}\n"


def yaml(document):
    def emit(value, depth=0):
        prefix = "  " * depth
        if isinstance(value, dict):
            lines = []
            for key, child in value.items():
                if isinstance(child, (dict, list)):
                    lines.append(prefix + key + ":\n" + emit(child, depth + 1))
                else:
                    lines.append(prefix + key + ": " + json.dumps(child, ensure_ascii=False))
            return "\n".join(lines)
        return "\n".join(prefix + "- " + json.dumps(child, ensure_ascii=False) for child in value)
    return emit(document) + "\n"


def measurements(document):
    rows = []
    for mode, colors in document["design_system"]["colors"].items():
        for role in ("textPrimary", "textSecondary", "actionPrimary", "expressionPlum", "success", "warning", "error", "outlineStrong", "focus"):
            minimum = 3 if role in ("outlineStrong", "focus") else 4.5
            for background in ("background", "surface", "surfaceRaised"):
                rows.append((mode, role, background, contrast(colors[role], colors[background]), minimum))
        rows.append((mode, "onActionPrimary", "actionPrimary", contrast(colors["onActionPrimary"], colors["actionPrimary"]), 4.5))
        on_accent = colors["textPrimary"] if mode == "light" else colors["onActionPrimary"]
        rows.append((mode, "onAccent (alias)", "accent", contrast(on_accent, colors["accent"]), 4.5))
    return rows


def report(document):
    rows = measurements(document)
    content = ["# Atmospheric Graphite v1.0 コントラスト検査", "", "正本: `source/foundations/colors.json`。元の15色×2モードは変更せず、使用する組み合わせを検査する。", "", "通常文字4.5:1、境界・フォーカス3:1を丸める前の値で判定する。下表は表示時のみ小数第2位まで丸めている。", "", "| モード | 前景 | 背景 | 比率 | 基準 | 結果 |", "| --- | --- | --- | ---: | ---: | --- |"]
    for mode, role, background, ratio, minimum in rows:
        content.append("| {} | `{}` | `{}` | {:.2f}:1 | {}:1 | {} |".format(mode, role, background, ratio, minimum, "合格" if ratio >= minimum else "要修正"))
    light = document["design_system"]["colors"]["light"]
    content += ["", "## 使用を制限する組み合わせ", "", "- Lightの `accent` / `background` は {:.2f}:1。淡い面上の小さな文字や、単独で状態を伝える必須図形に使わない。".format(contrast(light["accent"], light["background"])), "- Lightの `expressionSky` / `surface` は {:.2f}:1。装飾・区分に使い、通常文字や必須のグラフ線には流用しない。".format(contrast(light["expressionSky"], light["surface"])), "- `outlineStrong` は境界用。通常文字の役割には使わない。", "- `onAccent` は既存トークンへのエイリアスであり、新しい色値ではない。", "", "## 検証の限界", "", "この検査は列挙した不透明色のペアの計算である。全色の任意の組み合わせ、透過・画像との合成、OS実機、すべての状態、WCAG 2.2 AA全体の適合を証明しない。disabled・pressed・selectedなどの状態別トークンは未確定。", "", "基準: [文字のコントラスト](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)、[非テキストのコントラスト](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)。", ""]
    return "\n".join(content)
