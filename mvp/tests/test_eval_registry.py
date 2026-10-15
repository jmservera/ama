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
            data = json.loads((MVP / "evals" / name).read_text())
            self.assertEqual(data.get("version", data.get("generator_version")), d["version"])
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
            self.assertEqual((m1["homes"], m1["households"], m1["events"]), (500, 500, 5000))
            self.assertEqual((Path(a) / "events.jsonl").read_bytes(), (Path(b) / "events.jsonl").read_bytes())

    def test_households_consent_and_representative_never_inferred(self):
        rows = list(scale_fixture.households(3000))
        self.assertEqual(len(rows), 3000)
        homes = {h["id"]: h for h in scale_fixture.homes(3000)}
        for r in rows:
            self.assertTrue(r["is_synthetic"])
            self.assertTrue(r["resident_ref"].startswith("R-SYN-"))
            self.assertEqual(r["priority_support"], homes[r["home_id"]]["priority_support"])
            self.assertIn(r["works_consent_state"], scale_fixture.CONSENT_STATES)
            self.assertIn(r["representative_state"], scale_fixture.REP_STATES)
            self.assertEqual(r["representative_ref"] is None, r["representative_state"] == "None recorded")
            self.assertEqual(r["works_consent_given_by"] is None,
                             r["works_consent_state"] in ("Not requested", "Pending"))
            if r["works_consent_given_by"] == "Representative":
                self.assertEqual(r["representative_state"], "Authorised - evidence on file")
        self.assertEqual({r["works_consent_state"] for r in rows}, set(scale_fixture.CONSENT_STATES))
        self.assertTrue(any(r["representative_state"] == "Claimed - unverified" for r in rows))
        self.assertFalse(any("@" in json.dumps(r) for r in rows))

    def test_full_scale_counts(self):
        self.assertEqual(sum(1 for _ in scale_fixture.homes()), 60000)
        self.assertEqual(sum(1 for _ in scale_fixture.households()), 60000)
        self.assertEqual(sum(1 for _ in scale_fixture.events()), 600000)


if __name__ == "__main__":
    unittest.main()
