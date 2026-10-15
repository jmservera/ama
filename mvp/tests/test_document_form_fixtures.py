"""Document, form-schema and field-candidate fixtures: determinism, split and seeded defects."""
import importlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "support/synthetic-data/retrofit-flow/zava-forward-year-one/generator"
sys.path.insert(0, str(GENERATOR))
gen = importlib.import_module("zf_documents")
COMMITTED = ROOT / "mvp/evals/document_form_fixtures.json"


def register():
    forms = ("apartments", "bungalow", "terrace", "semidetached_house", "detached")
    return [dict(synthetic_home_id=f"TEST-{i:05d}", building_form_osm=forms[i % 5], local_authority="Test Authority",
                 synthetic_neighbourhood_cluster_id=f"CL-{i // 3}") for i in range(900)]


def check(f, schema):
    """Independent reference check of one family's observed fields; returns failing rule ids."""
    o, fails = f["observed_fields"], set()
    if o["home_id"] != f["synthetic_home_id"]:
        fails.add("RULE-DUP-001")
    if any(o.get(n) is None for n in gen.REQUIRED):
        fails.add("RULE-REQ-001")
    if "match funding" in str(o["eligibility_status"]) and o["match_funding_gbp"] is None:
        fails.add("RULE-COND-001")
    if o.get("floor_area_unit", "m2") != "m2":
        fails.add("RULE-UNIT-001")
    if f["currency"] != "GBP":
        fails.add("RULE-CUR-001")
    if abs(o["net_cost_gbp"] + o["vat_gbp"] - o["invoice_total_gbp"]) > 0.005:
        fails.add("RULE-CALC-001")
    if o["eligibility_status"] == "Unknown":
        fails.add("RULE-ELIG-001")
    if (o["match_funding_gbp"] or 0) > schema["match_budget_ceiling_gbp"]:
        fails.add("RULE-BUDGET-001")
    return fails


class DocumentFormFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = gen.build(register(), 20260901)
        cls.families = cls.data["families"]

    def test_deterministic_and_labelled_synthetic(self):
        self.assertEqual(json.dumps(gen.build(register(), 20260901), sort_keys=True),
                         json.dumps(self.data, sort_keys=True))
        self.assertNotEqual(gen.build(register(), 1)["content_sha256"], self.data["content_sha256"])
        self.assertTrue(self.data["is_synthetic"] and self.data["form_schema"]["is_synthetic"])
        self.assertEqual(len(self.families), 120)
        for f in self.families:
            self.assertTrue(f["is_synthetic"])
            self.assertEqual({d["kind"] for d in f["documents"]},
                             {"Survey report", "EPC certificate", "Invoice", "Evidence photo"})
            self.assertTrue(all(d["is_synthetic"] and d["label"].startswith("SYNTHETIC") for d in f["documents"]))
            self.assertEqual(len(f["gold_fields"]), 12)

    def test_split_is_fixed_and_independent(self):
        counts = {s: sum(f["split"] == s for f in self.families) for s, _ in gen.SPLITS}
        self.assertEqual(counts, {"tuning": 30, "calibration": 30, "held-out": 60})
        for key in ("synthetic_home_id", "neighbourhood_cluster_id"):
            seen = {}
            for f in self.families:
                self.assertEqual(seen.setdefault(f[key], f["split"]), f["split"])
            self.assertEqual(len(seen), 120)
        for split in counts:
            kinds = {f["seeded_defect"]["defect"] for f in self.families if f["split"] == split and f["seeded_defect"]}
            self.assertEqual(kinds, set(gen.DEFECTS))

    def test_seeded_defects_match_fixture_owned_expectations(self):
        schema = self.data["form_schema"]
        for f in self.families:
            fails = check(f, schema)
            d = f["seeded_defect"]
            if d is None:
                self.assertEqual(fails, set(), f["family_id"])
                continue
            self.assertEqual(fails, {d["rule_id"]}, f["family_id"])
            self.assertEqual((d["expected_status"], d["blocks_reviewed_pack"], d["schema_version"]),
                             ("fail", True, schema["version"]))

    def test_dependency_manifest_partitions_fields(self):
        for f in self.families:
            for m in f["dependency_manifest"]:
                self.assertEqual(set(m["affected_fields"]) | set(m["unaffected_fields"]), set(gen.FIELDS))
                self.assertFalse(set(m["affected_fields"]) & set(m["unaffected_fields"]))

    def test_committed_fixture_is_current(self):
        committed = json.loads(COMMITTED.read_text())
        self.assertEqual(committed["generator_version"], gen.VERSION)
        self.assertEqual(len(committed["families"]), 120)
        self.assertTrue(all(f["split"] in dict(gen.SPLITS) and f["is_synthetic"] for f in committed["families"]))
        for f in committed["families"]:
            self.assertEqual(check(f, committed["form_schema"]),
                             {f["seeded_defect"]["rule_id"]} if f["seeded_defect"] else set())


if __name__ == "__main__":
    unittest.main()
