#!/usr/bin/env python3
"""Build self-contained skill folders and token exports, or check for drift."""

import argparse
import json
from pathlib import Path

from design_tokens import ROOT, css, load, report, yaml


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
        if root.resolve() not in path.parents or not (name.startswith("skills/") or name.startswith("tokens/") or name == "docs/color-contrast.md"):
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
