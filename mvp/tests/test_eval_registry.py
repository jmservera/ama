import json
import tempfile
import unittest
from pathlib import Path

from zavaforward_mvp import scale_fixture

MVP = Path(__file__).resolve().parents[1]
REG = json.loads((MVP / "evals" / "registry.json").read_text())


class RegistryTests(unittest.TestCase):
    def test_every_eval_file_is_registered_with_matching_version(self):
        reg = {Path(d["path"]).name: d for d in REG["datasets"] if d["path"].startswith("mvp/evals/")}
        files = {p.name for p in (MVP / "evals").glob("*.json")} - {"registry.json"}
        self.assertEqual(files, set(reg))
        for name, d in reg.items():
            self.assertEqual(json.loads((MVP / "evals" / name).read_text())["version"], d["version"])
            self.assertFalse(d["contains_real_data"])

    def test_entries_have_required_fields(self):
        for d in REG["datasets"]:
            for k in ("id", "path", "version", "owner", "purpose"):
                self.assertTrue(d.get(k), (d.get("id"), k))
        self.assertEqual(len({d["id"] for d in REG["datasets"]}), len(REG["datasets"]))

    def test_fixture_registry_matches_generator(self):
        d = next(x for x in REG["datasets"] if x["id"] == "stock-scale-fixture")
        self.assertEqual((d["version"], d["seed"]), (scale_fixture.VERSION, scale_fixture.SEED))
        self.assertEqual((scale_fixture.HOMES, scale_fixture.EVENTS), (60000, 600000))

    def test_data_dir_is_git_ignored(self):
        self.assertIn("/mvp/data/", (MVP.parent / ".gitignore").read_text())


class FixtureTests(unittest.TestCase):
    def test_reproducible_from_seed_and_seed_sensitive(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b, tempfile.TemporaryDirectory() as c:
            m1 = scale_fixture.write(a, n=500)
            m2 = scale_fixture.write(b, n=500)
            m3 = scale_fixture.write(c, n=500, seed=1)
            self.assertEqual(m1, m2)
            self.assertNotEqual(m1["sha256"], m3["sha256"])
            self.assertEqual((m1["homes"], m1["events"]), (500, 5000))
            self.assertEqual((Path(a) / "events.jsonl").read_bytes(), (Path(b) / "events.jsonl").read_bytes())

    def test_full_scale_counts(self):
        self.assertEqual(sum(1 for _ in scale_fixture.homes()), 60000)
        self.assertEqual(sum(1 for _ in scale_fixture.events()), 600000)


if __name__ == "__main__":
    unittest.main()
