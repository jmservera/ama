"""Document, form-schema and field-candidate fixtures: determinism, split and seeded defects."""

import hashlib
import importlib
import json
import sys
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core.synthetic import provenance

ROOT = Path(__file__).resolve().parents[3]
GENERATOR = ROOT / "support/synthetic-data/retrofit-flow/zava-forward-year-one/generator"
sys.path.insert(0, str(GENERATOR))
gen = importlib.import_module("zf_documents")
controls = importlib.import_module("zf_document_controls")
COMMITTED = ROOT / "src/importer/evals/document_form_fixtures.json"
COMMITTED_CONTROLS = ROOT / "src/core/evals/document_control_fixtures.json"


# Pre-change generator output on the constructed register (seed 20260901), recorded in the C2 logs.
BASELINE = {
    "docs_whole": "c01bfa9d26a2ffc442309f88ee7aa07080a4afbc9987b424e6e9eda144522c87",
    "docs_content": "f959369fb2c1d417e695a092c82e2f397785361937c38d7524836a9274ec7cb8",
    "ctrl_whole": "63839fe0a3d7d9b40d817bea0248c842cf598f0e059c8f5e4edbd7e10d56360f",
    "ctrl_content": "0cb50e868809e11f00c05af26697e737ec94d5286a2e9b0cf830eb620ca1f79d",
}


def without_revision(out: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(
            {k: v for k, v in out.items() if k != "generator_revision"}, sort_keys=True
        ).encode()
    ).hexdigest()


def register() -> list[dict[str, Any]]:
    forms = ("apartments", "bungalow", "terrace", "semidetached_house", "detached")
    return [
        dict(
            synthetic_home_id=f"TEST-{i:05d}",
            building_form_osm=forms[i % 5],
            local_authority="Test Authority",
            synthetic_neighbourhood_cluster_id=f"CL-{i // 3}",
        )
        for i in range(900)
    ]


def check(f: dict[str, Any], schema: dict[str, Any]) -> set[str]:
    """Independent reference check of one family's observed fields; returns failing rule ids."""
    o, fails = f["observed_fields"], set[str]()
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
    data: dict[str, Any]
    families: list[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = gen.build(register(), 20260901)
        cls.families = cls.data["families"]

    def test_deterministic_and_labelled_synthetic(self) -> None:
        self.assertEqual(
            json.dumps(gen.build(register(), 20260901), sort_keys=True),
            json.dumps(self.data, sort_keys=True),
        )
        self.assertNotEqual(gen.build(register(), 1)["content_sha256"], self.data["content_sha256"])
        self.assertTrue(self.data["is_synthetic"] and self.data["form_schema"]["is_synthetic"])
        self.assertEqual(len(self.families), 120)
        for f in self.families:
            self.assertTrue(f["is_synthetic"])
            self.assertEqual(
                {d["kind"] for d in f["documents"]},
                {"Survey report", "EPC certificate", "Invoice", "Evidence photo"},
            )
            self.assertTrue(
                all(
                    d["is_synthetic"] and d["label"].startswith("SYNTHETIC") for d in f["documents"]
                )
            )
            self.assertEqual(len(f["gold_fields"]), 12)

    def test_split_is_fixed_and_independent(self) -> None:
        counts = {s: sum(f["split"] == s for f in self.families) for s, _ in gen.SPLITS}
        self.assertEqual(counts, {"tuning": 30, "calibration": 30, "held-out": 60})
        for key in ("synthetic_home_id", "neighbourhood_cluster_id"):
            seen: dict[str, str] = {}
            for f in self.families:
                self.assertEqual(seen.setdefault(f[key], f["split"]), f["split"])
            self.assertEqual(len(seen), 120)
        for split in counts:
            kinds = {
                f["seeded_defect"]["defect"]
                for f in self.families
                if f["split"] == split and f["seeded_defect"]
            }
            self.assertEqual(kinds, set(gen.DEFECTS))

    def test_seeded_defects_match_fixture_owned_expectations(self) -> None:
        schema = self.data["form_schema"]
        for f in self.families:
            fails = check(f, schema)
            d = f["seeded_defect"]
            if d is None:
                self.assertEqual(fails, set(), f["family_id"])
                continue
            self.assertEqual(fails, {d["rule_id"]}, f["family_id"])
            self.assertEqual(
                (d["expected_status"], d["blocks_reviewed_pack"], d["schema_version"]),
                ("fail", True, schema["version"]),
            )

    def test_dependency_manifest_partitions_fields(self) -> None:
        for f in self.families:
            for m in f["dependency_manifest"]:
                self.assertEqual(
                    set(m["affected_fields"]) | set(m["unaffected_fields"]), set(gen.FIELDS)
                )
                self.assertFalse(set(m["affected_fields"]) & set(m["unaffected_fields"]))

    def test_committed_fixture_is_current(self) -> None:
        committed = json.loads(COMMITTED.read_text())
        self.assertEqual(committed["generator_version"], gen.VERSION)
        self.assertEqual(len(committed["families"]), 120)
        self.assertTrue(
            all(f["split"] in dict(gen.SPLITS) and f["is_synthetic"] for f in committed["families"])
        )
        for f in committed["families"]:
            self.assertEqual(
                check(f, committed["form_schema"]),
                {f["seeded_defect"]["rule_id"]} if f["seeded_defect"] else set(),
            )

    def test_fresh_documents_output_records_source_revision_with_unchanged_payload(self) -> None:
        expected = provenance.source_revision([GENERATOR / "zf_documents.py"])
        first, second = gen.build(register(), 20260901), gen.build(register(), 20260901)
        self.assertEqual(first["generator_revision"], expected)
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))
        self.assertEqual(first["content_sha256"], BASELINE["docs_content"])
        self.assertEqual(without_revision(first), BASELINE["docs_whole"])


class DocumentControlGeneratorRevisionTests(unittest.TestCase):
    def test_fresh_controls_output_records_both_source_revision_with_unchanged_payload(
        self,
    ) -> None:
        expected = provenance.source_revision(
            [GENERATOR / "zf_document_controls.py", GENERATOR / "zf_documents.py"]
        )
        first, second = controls.build(register(), 20260901), controls.build(register(), 20260901)
        self.assertEqual(first["generator_revision"], expected)
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))
        self.assertEqual(first["content_sha256"], BASELINE["ctrl_content"])
        self.assertEqual(without_revision(first), BASELINE["ctrl_whole"])

    def test_historical_committed_fixtures_remain_unmodified_and_unrecorded(self) -> None:
        # Historically unrecorded (Unknown); stamping one now would fabricate provenance.
        for path in (COMMITTED, COMMITTED_CONTROLS):
            self.assertNotIn("generator_revision", json.loads(path.read_text()))

    # Unperformed future requirement (not active): once the committed fixtures are genuinely
    # regenerated from their original inputs, assert committed["generator_revision"] equals
    # the matching source_revision above.


if __name__ == "__main__":
    unittest.main()
