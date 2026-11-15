"""Needs-inventory to phase-gate traceability and synthetic provenance regressions (Refs #165)."""

import json
import re
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from zava_forward.core.synthetic import live_readings, privacy, scale_fixture

ROOT = Path(__file__).resolve().parents[3]
PACK = ROOT / "docs/reference/research/retrofit-synthetic-data"
INVENTORY: dict[str, Any] = json.loads((PACK / "needs-inventory.json").read_text())
MANIFEST: dict[str, Any] = json.loads((PACK / "scenario-manifest.json").read_text())
README = (PACK / "README.md").read_text()
NEEDS: list[dict[str, Any]] = INVENTORY["needs"]
STATUSES = ("covered", "partial", "missing")
APPROVAL_CLAIMS = re.compile(r"\b(approved|ratified|signed[- ]off|accepted by owner)\b", re.I)
GATED_EPIC = re.compile(r"(#\d+) \(SN-(\d+)(?:, (\w+))?\)")


def gate_section() -> str:
    start = README.index("## Synthetic data needs inventory and phase gate")
    end = README.index("\n### ", start)
    return README[start:end]


class NeedCoverageTraceabilityTests(unittest.TestCase):
    def test_every_need_has_valid_status_and_no_unrecorded_gap(self) -> None:
        self.assertEqual(tuple(INVENTORY["coverage_values"]), STATUSES)
        for need in NEEDS:
            with self.subTest(need=need["id"]):
                self.assertIn(need["coverage"], STATUSES)
                gap = need["gap_closure"]
                if need["coverage"] == "covered":
                    self.assertIn(gap["kind"], ("delivered", "deferred"))
                else:
                    self.assertIn(gap["kind"], ("child", "deferred"))
                    self.assertTrue(gap["issues"] or gap["kind"] == "deferred")
                self.assertTrue(gap["note"])

    def test_readiness_summary_counts_match_inventory(self) -> None:
        section = gate_section()
        self.assertIn(f"lists {len(NEEDS)} needs", section.replace("\n", " "))
        self.assertIn("covered, partial or missing", section.replace("\n", " "))
        self.assertIn(f"version {INVENTORY['version']}", section.replace("\n", " "))
        self.assertEqual(INVENTORY["status"], "draft-awaiting-owner-review")
        self.assertIn("still draft awaiting owner review", section.replace("\n", " "))

    def test_gated_epics_in_summary_match_inventory_coverage(self) -> None:
        by_id = {need["id"]: need for need in NEEDS}
        summary = gate_section().replace("\n", " ")
        gated = GATED_EPIC.findall(summary)
        self.assertTrue(gated)
        for epic, number, status in gated:
            need = by_id[f"SN-{number}"]
            with self.subTest(epic=epic, need=need["id"]):
                self.assertIn(epic, need["consuming_issues"])
                if status:
                    self.assertEqual(need["coverage"], status)

    def test_non_covered_rows_require_owner_decision_under_gate_rule(self) -> None:
        rule = INVENTORY["gate_rule"]
        self.assertIn("partial or missing", rule)
        self.assertIn("recorded owner decision on volume and scope", rule)
        for need in NEEDS:
            if need["coverage"] != "covered":
                with self.subTest(need=need["id"]):
                    self.assertTrue(need["consuming_issues"])
                    self.assertTrue(need["volume"])

    def test_every_row_traces_to_manifest_review_and_open_items(self) -> None:
        review = MANIFEST["inventory"]
        self.assertEqual({n["id"] for n in NEEDS}, set(review["reviewed_rows"]))
        self.assertEqual(review["version"], INVENTORY["version"])
        for need in ("SN-03", "SN-08", "SN-09"):
            self.assertTrue(any(need in item for item in INVENTORY["open_items"]), need)


class OwnerApprovalBoundaryTests(unittest.TestCase):
    def test_owner_sign_off_is_never_fabricated(self) -> None:
        review = MANIFEST["inventory"]
        self.assertEqual(INVENTORY["status"], "draft-awaiting-owner-review")
        self.assertEqual(review["owner_review"], "pending")
        self.assertEqual(review["review_kind"], "automated-engineering-review")
        self.assertIn("not owner ratification", review["reviewer"])
        authority = MANIFEST["inventory_authority"]
        self.assertEqual(authority["owner_approval"], "not-established")
        self.assertEqual(authority["customer_approval"], "not-established")
        self.assertTrue(any("Owner approval" in item for item in INVENTORY["open_items"]))

    def test_no_row_claims_owner_approval(self) -> None:
        for need in NEEDS:
            with self.subTest(need=need["id"]):
                self.assertTrue(need["owner"].startswith("owner, via #"))
                self.assertIsNone(APPROVAL_CLAIMS.search(need["owner"]))
                self.assertNotIn("owner_approved", need)

    def test_readme_keeps_approval_boundary(self) -> None:
        section = " ".join(gate_section().split())
        self.assertIn("not owner ratification", " ".join(README.split()))
        self.assertIn("an automated review or a passing test cannot waive that gate", section)


class SyntheticProvenanceTests(unittest.TestCase):
    def test_public_pack_is_labelled_and_pattern_clean(self) -> None:
        self.assertIs(MANIFEST["is_synthetic"], True)
        self.assertIs(MANIFEST["contains_real_data"], False)
        self.assertEqual(privacy.public_issues(ROOT), [])

    def test_scale_fixture_records_stay_synthetic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "scale"
            scale_fixture.write(out, n=3, per_home=2)
            self.assertEqual(privacy.snapshot_issues(out, "scale"), [])
            for name in ("homes.jsonl", "households.jsonl", "events.jsonl"):
                rows = [json.loads(line) for line in (out / name).read_text().splitlines()]
                self.assertTrue(rows, name)
                for row in rows:
                    self.assertIs(row["is_synthetic"], True, name)
                    self.assertEqual(
                        privacy.pattern_issues(row, scale_home=name != "events.jsonl"), []
                    )

    def test_sensor_simulator_outputs_keep_synthetic_flags(self) -> None:
        generator = live_readings.Generator(seed=165)
        start = datetime(2026, 1, 5, 12, 0, tzinfo=UTC)
        for home in ("SYN-HOME-000001", "SYN-HOME-000002"):
            for step in range(4):
                reading = generator.reading(home, start + timedelta(minutes=30 * step))
                row = reading.row()
                with self.subTest(home=home, step=step):
                    self.assertEqual(row["source_type"], "SYNTHETIC")
                    self.assertIn("not a real device", row["label"])
                    self.assertTrue(reading.device_id.startswith("SYN-"))
                    self.assertEqual(privacy.emission_issues(row), [])
                    self.assertEqual(json.loads(reading.body()), row)


if __name__ == "__main__":
    unittest.main()
