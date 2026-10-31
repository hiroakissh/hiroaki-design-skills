import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts/check-samples.py"
SPEC = importlib.util.spec_from_file_location("sample_checks", MODULE_PATH)
CHECKS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKS)


class FreshnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.samples = []
        links = []
        for name in ("app", "report"):
            folder = self.root / "samples" / name
            folder.mkdir(parents=True)
            for file, content in (("brief.md", "Fixed task"), ("data.json", "{}"),
                                  ("preview.svg", "<svg/>"), ("preview-dark.svg", "<svg/>"), ("index.html", "<html lang='ja'></html>"), ("review.md", "Visually reviewed")):
                (folder / file).write_text(content, encoding="utf-8")
            relative = "samples/" + name + "/"
            sample = {
                "id": name, "skill": name, "title": name, "status": "prototype",
                "inputs": [relative + "brief.md", relative + "data.json"],
                "outputs": [relative + "preview.svg", relative + "preview-dark.svg", relative + "index.html", relative + "review.md"],
                "preview": relative + "preview.svg", "brief": relative + "brief.md", "review": relative + "review.md",
                "previews": {"light": relative + "preview.svg", "dark": relative + "preview-dark.svg"},
                "artifact": relative + "index.html",
            }
            self.samples.append(sample)
            links += ["[{}]({})".format(key, sample[key]) for key in ("preview", "brief", "review")]
            links += ["[dark]({})".format(sample["previews"]["dark"]), "[artifact]({})".format(sample["artifact"])]
        self.save_catalog()
        (self.root / "README.md").write_text("\n".join(links), encoding="utf-8")
        self.record_all()

    def save_catalog(self):
        (self.root / "samples/catalog.json").write_text(json.dumps({"samples": self.samples}), encoding="utf-8")

    def record_all(self):
        CHECKS.record(self.root, [], True, "Regenerated and visually inspected fixture outputs")

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_reviewed_samples_pass(self):
        self.assertEqual(CHECKS.check(self.root), [])

    def test_creating_common_profile_invalidates_every_sample(self):
        self.write("source/profile.md", "New personal palette")
        errors = CHECKS.check(self.root)
        self.assertEqual({error.split(":")[0] for error in errors}, {"app", "report"})
        self.assertTrue(all("inputs changed" in error for error in errors))

    def test_new_shared_reference_invalidates_every_sample(self):
        self.write("source/foundations/typography.md", "Japanese type guidance")
        self.assertEqual(len(CHECKS.check(self.root)), 2)

    def test_skill_reference_change_invalidates_only_its_sample(self):
        self.write("skills/app/SKILL.md", "App guidance")
        self.write("skills/app/references/spacing.md", "Original spacing")
        self.samples[0]["status"] = "skill"
        self.save_catalog()
        self.write("samples/app/review.md", "Applied the app skill and inspected the generated artifact")
        self.record_all()
        self.write("skills/app/references/spacing.md", "Updated spacing")
        errors = CHECKS.check(self.root)
        self.assertEqual(len(errors), 1)
        self.assertTrue(errors[0].startswith("app: inputs changed"))

    def test_changed_artifact_needs_review(self):
        self.write("samples/app/preview.svg", "<svg><rect/></svg>")
        self.assertTrue(any("app: artifacts changed" in error for error in CHECKS.check(self.root)))

    def test_changed_brief_invalidates_its_sample(self):
        self.write("samples/report/brief.md", "A different comparison task")
        errors = CHECKS.check(self.root)
        self.assertEqual(len(errors), 1)
        self.assertTrue(errors[0].startswith("report: inputs changed"))

    def test_unregistered_new_skill_fails(self):
        self.write("source/skills/motion/instructions.md", "Motion guidance")
        self.assertIn("No sample registered for skill: motion", CHECKS.check(self.root))

    def test_prototype_cannot_cover_implemented_skill(self):
        self.write("skills/app/SKILL.md", "App guidance")
        self.assertTrue(any("replace prototype status" in error for error in CHECKS.check(self.root)))
        with self.assertRaises(CHECKS.SampleError):
            self.record_all()

    def test_missing_preview_fails(self):
        (self.root / "samples/app/preview.svg").unlink()
        self.assertTrue(any("missing output samples/app/preview.svg" in error for error in CHECKS.check(self.root)))

    def test_missing_readme_link_fails(self):
        (self.root / "README.md").write_text("No sample links", encoding="utf-8")
        self.assertTrue(any("README must link" in error for error in CHECKS.check(self.root)))

    def test_record_rejects_empty_note(self):
        with self.assertRaises(CHECKS.SampleError):
            CHECKS.record(self.root, ["app"], False, " ")

    def test_changed_inputs_cannot_be_recorded_without_review_update(self):
        self.write("source/profile.md", "Updated palette")
        with self.assertRaises(CHECKS.SampleError):
            self.record_all()
        self.write("samples/app/review.md", "Reran and inspected the app with the updated palette")
        CHECKS.record(self.root, ["app"], False, "Verified the app")
        errors = CHECKS.check(self.root)
        self.assertEqual(len(errors), 1)
        self.assertTrue(errors[0].startswith("report: inputs changed"))

    def test_paths_cannot_escape_repository(self):
        self.samples[0]["inputs"].append("../outside.md")
        self.save_catalog()
        with self.assertRaises(CHECKS.SampleError):
            CHECKS.check(self.root)

    def test_dark_preview_must_exist(self):
        (self.root / "samples/app/preview-dark.svg").unlink()
        self.assertTrue(any("missing output samples/app/preview-dark.svg" in error for error in CHECKS.check(self.root)))

    def test_two_modes_cannot_point_to_the_same_preview(self):
        self.samples[0]["previews"]["dark"] = self.samples[0]["previews"]["light"]
        self.save_catalog()
        with self.assertRaises(CHECKS.SampleError):
            CHECKS.check(self.root)


if __name__ == "__main__":
    unittest.main()
