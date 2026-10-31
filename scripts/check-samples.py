#!/usr/bin/env python3
"""Track reviewed sample inputs and artifacts; no third-party dependencies."""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


class SampleError(ValueError):
    pass


def local_path(root, name):
    if not isinstance(name, str) or not name or Path(name).is_absolute():
        raise SampleError("Expected a repository-relative path: {!r}".format(name))
    path = root / name
    if root.resolve() not in path.resolve().parents:
        raise SampleError("Path must stay inside the repository: " + name)
    return path


def files_under(root, name):
    path = local_path(root, name)
    if path.is_file():
        return [path]
    if not path.exists():
        return []
    files = []
    for child in sorted(path.rglob("*")):
        if "__pycache__" in child.parts or child.name == ".DS_Store":
            continue
        local_path(root, child.relative_to(root).as_posix())
        if child.is_file():
            files.append(child)
    return files


def load_catalog(root):
    document = json.loads((root / "samples/catalog.json").read_text(encoding="utf-8"))
    samples = document.get("samples")
    if not isinstance(samples, list) or not samples:
        raise SampleError("samples/catalog.json must contain a non-empty samples array")
    seen = set()
    for sample in samples:
        for key in ("id", "skill", "status", "title", "inputs", "outputs", "preview", "brief", "review"):
            if key not in sample:
                raise SampleError("Sample is missing field: " + key)
        for key in ("id", "skill"):
            if not isinstance(sample[key], str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", sample[key]):
                raise SampleError("Invalid sample or skill name: {!r}".format(sample[key]))
        if sample["id"] in seen:
            raise SampleError("Duplicate sample id: " + sample["id"])
        seen.add(sample["id"])
        if sample["status"] not in ("prototype", "skill"):
            raise SampleError("Invalid sample status: " + sample["id"])
        for key in ("inputs", "outputs"):
            if not isinstance(sample[key], list) or not sample[key]:
                raise SampleError("{} must be a non-empty array: {}".format(key, sample["id"]))
            for name in sample[key]:
                local_path(root, name)
        for key in ("preview", "brief", "review"):
            local_path(root, sample[key])
        if "previews" in sample:
            if set(sample["previews"]) != {"light", "dark"} or len(set(sample["previews"].values())) != 2:
                raise SampleError("Separate Light/Dark previews are required: " + sample["id"])
            for name in sample["previews"].values():
                local_path(root, name)
                if name not in sample["outputs"]:
                    raise SampleError("Theme previews must be tracked outputs: " + sample["id"])
        if "artifact" in sample:
            local_path(root, sample["artifact"])
            if sample["artifact"] not in sample["outputs"]:
                raise SampleError("Artifact must be a tracked output: " + sample["id"])
        if sample["preview"] not in sample["outputs"] or sample["review"] not in sample["outputs"]:
            raise SampleError("Preview and review must be tracked outputs: " + sample["id"])
        if sample["brief"] not in sample["inputs"]:
            raise SampleError("Brief must be a tracked input: " + sample["id"])
    return samples


def implemented_skills(root):
    result = set()
    for parent in ("source/skills", "skills"):
        base = root / parent
        if base.is_dir():
            for directory in base.iterdir():
                if directory.is_dir() and not directory.name.startswith("."):
                    if files_under(root, directory.relative_to(root).as_posix()):
                        result.add(directory.name)
    return result


def structure_errors(root, samples):
    errors = []
    implemented = implemented_skills(root)
    covered = {sample["skill"] for sample in samples}
    for skill in sorted(implemented - covered):
        errors.append("No sample registered for skill: " + skill)
    readme_path = root / "README.md"
    readme = readme_path.read_text(encoding="utf-8") if readme_path.is_file() else ""
    for sample in samples:
        prefix = sample["id"] + ": "
        if sample["skill"] in implemented and sample["status"] != "skill":
            errors.append(prefix + "apply the implemented skill and replace prototype status")
        if sample["status"] == "skill" and sample["skill"] not in implemented:
            errors.append(prefix + "skill status has no corresponding skill source")
        if sample["status"] == "skill" and ("previews" not in sample or "artifact" not in sample):
            errors.append(prefix + "skill samples need an artifact and separate Light/Dark previews")
        for name in sample["inputs"]:
            if not local_path(root, name).exists():
                errors.append(prefix + "missing input " + name)
        for name in sample["outputs"]:
            if not local_path(root, name).is_file():
                errors.append(prefix + "missing output " + name)
        for key in ("preview", "brief", "review"):
            name = sample[key]
            if not local_path(root, name).is_file():
                errors.append(prefix + "missing " + key + " " + name)
            if "](" + name + ")" not in readme:
                errors.append(prefix + "README must link to " + name)
        for name in list(sample.get("previews", {}).values()) + ([sample["artifact"]] if "artifact" in sample else []):
            if "](" + name + ")" not in readme:
                errors.append(prefix + "README must link to " + name)
    return errors


def digest_paths(root, names, extra=None):
    content = {"configuration": extra}
    for name in sorted(set(names)):
        path = local_path(root, name)
        if not path.exists():
            content[name] = {"missing": True}
        else:
            content[name] = {
                file.relative_to(root).as_posix(): hashlib.sha256(file.read_bytes()).hexdigest()
                for file in files_under(root, name)
            }
    encoded = json.dumps(content, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def fingerprints(root, sample):
    implicit = [
        "source/profile.md", "source/catalog.json", "source/foundations", "samples/shared",
        "source/skills/" + sample["skill"], "skills/" + sample["skill"],
    ]
    return {
        "inputsHash": digest_paths(root, sample["inputs"] + implicit, sample),
        "outputsHash": digest_paths(root, sample["outputs"]),
        "reviewHash": digest_paths(root, [sample["review"]]),
    }


def load_records(root):
    path = root / "samples/freshness.json"
    if not path.exists():
        return {"version": 1, "samples": {}}
    records = json.loads(path.read_text(encoding="utf-8"))
    if records.get("version") != 1 or not isinstance(records.get("samples"), dict):
        raise SampleError("Unsupported freshness record format")
    return records


def check(root):
    samples = load_catalog(root)
    errors = structure_errors(root, samples)
    records = load_records(root)["samples"]
    for sample in samples:
        previous = records.get(sample["id"])
        if not previous:
            errors.append(sample["id"] + ": no reviewed sample recorded")
            continue
        current = fingerprints(root, sample)
        if previous.get("inputsHash") != current["inputsHash"]:
            errors.append(sample["id"] + ": inputs changed; regenerate and review the sample")
        if previous.get("outputsHash") != current["outputsHash"]:
            errors.append(sample["id"] + ": artifacts changed; inspect and record the result")
        if not previous.get("note", "").strip() or not previous.get("reviewedAt"):
            errors.append(sample["id"] + ": review note and time are required")
    return errors


def record(root, ids, all_samples, note):
    if not note.strip():
        raise SampleError("Provide a concrete review note")
    samples = load_catalog(root)
    errors = structure_errors(root, samples)
    if errors:
        raise SampleError("\n".join(errors))
    selected = {sample["id"] for sample in samples} if all_samples else set(ids)
    if not selected:
        raise SampleError("Select sample ids or --all")
    unknown = selected - {sample["id"] for sample in samples}
    if unknown:
        raise SampleError("Unknown sample ids: " + ", ".join(sorted(unknown)))
    records = load_records(root)
    for sample in samples:
        if sample["id"] in selected:
            current = fingerprints(root, sample)
            previous = records["samples"].get(sample["id"])
            if previous and any(previous.get(key) != current[key] for key in ("inputsHash", "outputsHash")):
                if previous.get("reviewHash") == current["reviewHash"]:
                    raise SampleError(sample["id"] + ": update review.md with the rerun and visual checks before recording")
            records["samples"][sample["id"]] = dict(
                current,
                reviewedAt=datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
                note=note.strip(),
            )
    path = root / "samples/freshness.json"
    path.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return sorted(selected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check")
    recording = commands.add_parser("record", help="Record only after applying the skill and visually reviewing outputs")
    recording.add_argument("ids", nargs="*")
    recording.add_argument("--all", action="store_true", dest="all_samples")
    recording.add_argument("--note", required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        if args.command == "check":
            errors = check(root)
            if errors:
                print("Sample checks failed:\n- " + "\n- ".join(errors), file=sys.stderr)
                return 1
            print("All sample inputs, artifacts, coverage, and README links are current.")
        else:
            if args.all_samples and args.ids:
                raise SampleError("Use sample ids or --all, not both")
            selected = record(root, args.ids, args.all_samples, args.note)
            print("Recorded reviewed samples: " + ", ".join(selected))
    except (SampleError, OSError, ValueError, TypeError) as error:
        print("Sample check error: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
