#!/usr/bin/env python3
"""Validate skill structure and references, including isolated copied folders."""

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def validate(folder):
    errors = []
    main = folder / "SKILL.md"
    if not main.is_file():
        return [str(folder) + ": SKILL.md is missing"]
    content = main.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
    if not match:
        return [str(folder) + ": YAML frontmatter is missing"]
    name = re.search(r"^name: ([a-z0-9]+(?:-[a-z0-9]+)*)$", match[1], re.M)
    description = re.search(r'^description: (".*")$', match[1], re.M)
    if not name or name[1] != folder.name or len(name[1]) > 64:
        errors.append(str(folder) + ": name must match the folder and the skill naming rules")
    try:
        if not description or not 1 <= len(json.loads(description[1])) <= 1024:
            errors.append(str(folder) + ": a concise description is required")
    except ValueError:
        errors.append(str(folder) + ": malformed description")
    for path in [main] + sorted((folder / "references").glob("*.md")):
        body = path.read_text(encoding="utf-8")
        for link in re.findall(r"\]\(([^)]+)\)", body):
            if "://" in link or link.startswith("#"):
                continue
            target = (path.parent / link.split("#")[0]).resolve()
            if folder.resolve() not in target.parents or not target.is_file():
                errors.append(str(path) + ": missing or external local reference " + link)
    for asset in ("colors.json", "colors.yaml", "colors.css"):
        if not (folder / "assets" / asset).is_file():
            errors.append(str(folder) + ": missing color asset " + asset)
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    folders = [Path(path).resolve() for path in args.paths] if args.paths else sorted((ROOT / "skills").glob("*/"))
    if not folders:
        raise SystemExit("No skills found")
    errors = [error for folder in folders for error in validate(folder)]
    if errors:
        raise SystemExit("Skill validation failed:\n" + "\n".join(errors))
    print("Validated {} self-contained skills.".format(len(folders)))
