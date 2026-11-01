#!/usr/bin/env python3
"""Build self-contained skill folders and token exports, or check for drift."""

import argparse
import json
from pathlib import Path

from design_tokens import ROOT, css, load, report, yaml


def watch_guide_index(registry):
    """Publish our source notes, not copies of third-party documentation."""
    lines = [
        "# Watchの公式デザイン資料", "",
        "確認日: " + registry["checked_on"] + " / 原本の言語は各項目に記載。", "",
        registry["scope"], "",
        "本文を確認できた資料を日本語で要約し、適用範囲と取得上の制約を記録する。公式文書・図版・フォントの全文複製ではない。リンク先の改訂・SDK・機種の対応は実装時に再確認する。", "",
        "`design-guide` はデザイン資料、`implementation` は開発・操作資料、`overview` は概要、`boundary` は連携API等を設計ガイドと誤認しないための境界資料。`current` は現在の参照先として整理した資料で、記事内の全APIが最新という保証ではない。`legacy` は新規製品へ流用しない。`limited` は詳細の取得が不完全なため、その詳細を設計根拠にしない。", "",
        "## 取得・参照した資料", "",
    ]
    for item in registry["sources"]:
        lines += [
            "### " + item["id"] + " — " + item["ecosystem"], "",
            "[" + item["title"] + "](" + item["url"] + ") — " + item["publisher"], "",
            "- 分類: `" + item["kind"] + "` / 状態: `" + item["status"] + "` / 言語: " + item["language"],
            "- 確認日: " + item["checked_on"],
            "- 対象: " + item["scope"],
            "- 取り入れる判断: " + item["use"],
            "- 確認方法・制約: " + item["access"], "",
        ]
    lines += ["## 未取得の範囲と更新", "", registry["gaps"], "",
              "対象機種が追加されたら、メーカー名だけで共通化せずOS・画面用途・入力・表示方式を調べる。資料のURL、分類、確認日、取得範囲と適用先を更新し、スキルとサンプルを同じ変更で再確認する。", ""]
    return "\n".join(lines)


def expected_files(root=ROOT):
    catalog = json.loads((root / "source/catalog.json").read_text(encoding="utf-8"))
    palette = load(root)
    assets = {
        "colors.json": json.dumps(palette, ensure_ascii=False, indent=2) + "\n",
        "colors.yaml": yaml(palette),
        "colors.css": css(palette),
    }
    result = {"tokens/" + name: content for name, content in assets.items()}
    result["docs/color-contrast.md"] = report(palette)
    references = {
        "profile.md": "source/profile.md",
        "colors.md": "source/foundations/color-guidelines.md",
        "craft.md": "source/foundations/craft.md",
        "accessibility.md": "source/foundations/accessibility.md",
        "sources.md": "source/foundations/sources.md",
    }
    for skill in catalog["skills"]:
        name = skill["name"]
        base = "skills/" + name + "/"
        source = root / "source/skills" / name
        frontmatter = "---\nname: {}\ndescription: {}\nmetadata:\n  author: \"hiroakissh\"\n  version: {}\n  color-system: \"Atmospheric Graphite 1.0\"\n---\n\n".format(name, json.dumps(skill["description"], ensure_ascii=False), json.dumps(catalog["version"]))
        result[base + "SKILL.md"] = frontmatter + (source / "instructions.md").read_text(encoding="utf-8")
        interface = {"display_name": skill["title"], "short_description": skill["summary"], "default_prompt": skill["prompt"]}
        result[base + "agents/openai.yaml"] = "interface:\n" + "\n".join("  {}: {}".format(key, json.dumps(value, ensure_ascii=False)) for key, value in interface.items()) + "\n"
        for name, path in references.items():
            content = (root / path).read_text(encoding="utf-8")
            if name == "profile.md":
                content = content.replace("(foundations/color-guidelines.md)", "(colors.md)")
            result[base + "references/" + name] = content
        for path in sorted((source / "references").glob("*.md")):
            result[base + "references/" + path.name] = path.read_text(encoding="utf-8")
        for name, content in assets.items():
            result[base + "assets/" + name] = content
        for path in sorted((source / "assets").glob("*.json")):
            if path.name in assets:
                raise ValueError("Skill assets cannot override shared color assets: " + str(path))
            content = path.read_text(encoding="utf-8")
            result[base + "assets/" + path.name] = content
            if path.name == "watch-sources.json":
                guide = watch_guide_index(json.loads(content))
                result[base + "references/guide-index.md"] = guide
                result["docs/watch-design-guides.md"] = guide
    return result


def build(check=False, root=ROOT):
    files = expected_files(root)
    manifest = root / ".generated-files.json"
    previous = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else []
    expected_manifest = json.dumps(sorted(files), indent=2, ensure_ascii=False) + "\n"
    stale = []
    for name, content in files.items():
        path = root / name
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            stale.append(name)
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
    for name in set(previous) - set(files):
        path = (root / name).resolve()
        if root.resolve() not in path.parents or not (name.startswith("skills/") or name.startswith("tokens/") or name in ("docs/color-contrast.md", "docs/watch-design-guides.md")):
            raise ValueError("Refusing to remove an unmanaged generated path: " + name)
        if path.is_file():
            stale.append(name)
            if not check:
                path.unlink()
    if not manifest.is_file() or manifest.read_text(encoding="utf-8") != expected_manifest:
        stale.append(".generated-files.json")
    if not check:
        manifest.write_text(expected_manifest, encoding="utf-8")
    return stale


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = build(args.check)
    if args.check and stale:
        raise SystemExit("Generated files are stale:\n" + "\n".join(stale))
    print("Generated files are current." if args.check else "Built {} generated files.".format(len(expected_files())))
