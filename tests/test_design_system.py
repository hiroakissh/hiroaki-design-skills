import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from design_tokens import contrast, css, load, measurements


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


VALIDATION = module("skill_validation", "scripts/validate-skills.py")


class ColorTests(unittest.TestCase):
    def test_black_white_and_identical_reference_ratios(self):
        self.assertAlmostEqual(contrast("#000000", "#FFFFFF"), 21)
        self.assertEqual(contrast("#EAF3F6", "#EAF3F6"), 1)

    def test_user_palette_is_preserved_exactly(self):
        colors = load()["design_system"]["colors"]
        roles = ["background","surface","surfaceRaised","textPrimary","textSecondary","actionPrimary","onActionPrimary","accent","expressionPlum","expressionSky","outlineStrong","focus","success","warning","error"]
        expected = {
            "light": ["#EAF3F6","#FFFFFF","#F4F7F6","#20282B","#4F626B","#235F75","#FFFFFF","#D8F15A","#624D80","#87C6D8","#6A858C","#714994","#21614E","#7B4F00","#A82B41"],
            "dark": ["#221C2C","#302838","#3B3444","#F6F0EB","#CAC0D4","#B9A1DE","#221C2C","#D8F15A","#B9A1DE","#9ED8E5","#9A8BA8","#D8F15A","#95E0BD","#F8C77E","#FF94A5"],
        }
        for mode in expected:
            self.assertEqual(colors[mode], dict(zip(roles, expected[mode])))

    def test_declared_pairs_meet_unrounded_thresholds(self):
        failed = [row for row in measurements(load()) if row[3] < row[4]]
        self.assertEqual(failed, [])

    def test_lime_is_not_readable_small_text_on_light_background(self):
        colors = load()["design_system"]["colors"]["light"]
        self.assertLess(contrast(colors["accent"], colors["background"]), 3)

    def test_semantic_aliases_reference_existing_roles(self):
        output = css(load())
        self.assertIn("--color-on-accent: var(--color-text-primary)", output)
        self.assertIn("--color-on-accent: var(--color-on-action-primary)", output)
        self.assertNotIn("--color-disabled:", output)


class PackagingTests(unittest.TestCase):
    def test_every_skill_is_valid_when_copied_alone(self):
        catalog = json.loads((ROOT / "source/catalog.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            for skill in catalog["skills"]:
                target = Path(temporary) / skill["name"]
                shutil.copytree(ROOT / "skills" / skill["name"], target)
                self.assertEqual(VALIDATION.validate(target), [])
                self.assertEqual(json.loads((target / "assets/colors.json").read_text(encoding="utf-8")), load())

    def test_external_local_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "hiro-design-app"
            shutil.copytree(ROOT / "skills/hiro-design-app", target)
            with (target / "SKILL.md").open("a", encoding="utf-8") as file:
                file.write("\n[bad](../../source/profile.md)\n")
            self.assertTrue(any("external local reference" in error for error in VALIDATION.validate(target)))


if __name__ == "__main__":
    unittest.main()
