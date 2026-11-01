import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from design_tokens import contrast, load


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


BUILD = module("watch_build", "build-skills.py")
RENDER = module("watch_render", "render-samples.py")


class WatchPackagingTests(unittest.TestCase):
    def test_oled_canvas_adapter_keeps_used_content_legible(self):
        colors = load()["design_system"]["colors"]["dark"]
        for role, minimum in (("textPrimary", 4.5), ("textSecondary", 4.5), ("accent", 4.5), ("outlineStrong", 3), ("focus", 3)):
            self.assertGreaterEqual(contrast(colors[role], "#000000"), minimum, role)

    def test_source_records_keep_scope_status_and_verification_provenance(self):
        registry = json.loads((ROOT / "source/skills/hiro-design-watch/assets/watch-sources.json").read_text())
        date.fromisoformat(registry["checked_on"])
        self.assertTrue(registry["gaps"].strip())
        seen = set()
        for item in registry["sources"]:
            self.assertNotIn(item["id"], seen)
            seen.add(item["id"])
            self.assertIn(item["kind"], ("design-guide", "implementation", "overview", "boundary"))
            self.assertIn(item["status"], ("current", "legacy", "limited"))
            self.assertLessEqual(date.fromisoformat(item["checked_on"]), date.fromisoformat(registry["checked_on"]))
            for key in ("publisher", "ecosystem", "scope", "use", "access", "language"):
                self.assertTrue(item[key].strip(), (item["id"], key))
            url = urlparse(item["url"])
            self.assertEqual(url.scheme, "https")
            self.assertTrue(url.netloc)

    def test_source_registry_and_index_travel_with_watch_skill(self):
        source = ROOT / "source/skills/hiro-design-watch/assets/watch-sources.json"
        packaged = ROOT / "skills/hiro-design-watch/assets/watch-sources.json"
        self.assertEqual(source.read_bytes(), packaged.read_bytes())
        guide = BUILD.watch_guide_index(json.loads(source.read_text()))
        self.assertEqual(guide, (ROOT / "skills/hiro-design-watch/references/guide-index.md").read_text())
        self.assertEqual(guide, (ROOT / "docs/watch-design-guides.md").read_text())

    def test_domain_assets_cannot_replace_personal_palette(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            shutil.copytree(ROOT / "source", target / "source")
            (target / "source/skills/hiro-design-watch/assets/colors.json").write_text("{}")
            with self.assertRaisesRegex(ValueError, "cannot override shared color"):
                BUILD.expected_files(target)

    def test_watch_styles_and_simulation_do_not_leak_to_other_samples(self):
        files = RENDER.expected_files()
        watch = files["samples/hiro-design-watch/index.html"]
        self.assertIn("--watch-system-canvas", watch)
        self.assertIn("function initialState()", watch)
        for name, content in files.items():
            if name != "samples/hiro-design-watch/index.html":
                self.assertNotIn("--watch-system-canvas", content, name)
                self.assertNotIn("function initialState()", content, name)


if __name__ == "__main__":
    unittest.main()
