"""Atlas-to-screen trace completeness regressions (Refs #233)."""

import tempfile
import unittest
from pathlib import Path

from zava_forward.core import atlas_screen_trace as trace

ROOT = Path(__file__).resolve().parents[3]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class AtlasScreenTraceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.prd = read(trace.PRD)
        self.atlas = read(trace.ATLAS)
        self.doc = read(trace.TRACE)

    def test_published_trace_is_complete(self) -> None:
        report = trace.check(self.prd, self.atlas, self.doc)
        self.assertEqual(report["gaps"], [])
        self.assertEqual((report["perspectives"], report["themes"]), (11, 5))

    def test_missing_perspective_is_reported(self) -> None:
        doc = "\n".join(
            ln for ln in self.doc.splitlines() if not ln.startswith("| Finance and Grants |")
        )
        gaps = trace.check(self.prd, self.atlas, doc)["gaps"]
        self.assertIn(
            "perspective not traced with confirms/changes/hypothesis: Finance and Grants", gaps
        )

    def test_theme_without_screen_or_deferral_is_reported(self) -> None:
        doc = self.doc.replace("Deferred: dispatch rehearsal", "Later: dispatch rehearsal")
        gaps = trace.check(self.prd, self.atlas, doc)["gaps"]
        self.assertIn("theme has neither screen nor deferral: Prevention through rehearsal", gaps)

    def test_walkthrough_must_not_reuse_existing_example_home(self) -> None:
        doc = self.doc.replace("EX-HOME-901", "EX-HOME-646")
        gaps = trace.check(self.prd, self.atlas, doc)["gaps"]
        self.assertTrue(any("one new home id" in g for g in gaps))

    def test_walkthrough_must_not_reuse_manifest_home_suffix(self) -> None:
        doc = self.doc.replace("EX-HOME-901", "EX-HOME-104")
        gaps = trace.check(self.prd, self.atlas, doc)["gaps"]
        self.assertTrue(any("one new home id" in g for g in gaps))

    def test_unknown_screen_id_is_reported(self) -> None:
        doc = self.doc.replace("`programme-queue`", "`not-a-screen`")
        gaps = trace.check(self.prd, self.atlas, doc)["gaps"]
        self.assertTrue(any("unknown screen id" in g and "not-a-screen" in g for g in gaps))

    def test_walkthrough_description_required(self) -> None:
        doc = self.doc.replace("Offered versus committed capacity", "")
        gaps = trace.check(self.prd, self.atlas, doc)["gaps"]
        self.assertTrue(
            any("description" in g and g.endswith("4. Coordinate ready work") for g in gaps)
        )

    def test_hypothesis_label_must_be_in_scope_section(self) -> None:
        scope = trace.section(self.doc, "Scope and evidence label")
        doc = self.doc.replace(scope, scope.replace("hypotheses", "findings"))
        gaps = trace.check(self.prd, self.atlas, doc)["gaps"]
        self.assertIn("atlas findings are not labelled hypotheses", gaps)

    def test_hypothesis_label_required(self) -> None:
        doc = self.doc.replace("hypotheses", "findings").replace("hypothesis", "finding")
        doc = doc.replace("Hypothes", "Finding")
        gaps = trace.check(self.prd, self.atlas, doc)["gaps"]
        self.assertTrue(any("hypotheses" in g for g in gaps))

    def test_truncated_trace_row_reports_gap_without_error(self) -> None:
        doc = self.doc.replace("| Finance and Grants |", "| Finance and Grants |\n| Orphan |", 1)
        result = trace.check(self.prd, self.atlas, doc)
        self.assertIn("verdict", result)

    def test_status_labels_match_registered_screens(self) -> None:
        js = read(trace.ROLE_SCREENS)
        self.assertEqual(trace.check(self.prd, self.atlas, self.doc, js)["gaps"], [])
        self.assertIn("finance-funding", trace.registered_screens(js))

    def test_status_drift_is_reported(self) -> None:
        js = read(trace.ROLE_SCREENS)
        doc = self.doc.replace("`data-operator` (main", "`ghost-screen` (main")
        gaps = trace.check(self.prd, self.atlas, doc, js)["gaps"]
        self.assertIn("labelled main but not registered: ghost-screen", gaps)
        doc = self.doc.replace("`data-operator` (main", "`data-operator` (unmerged")
        gaps = trace.check(self.prd, self.atlas, doc, js)["gaps"]
        self.assertIn("labelled unmerged but registered: data-operator", gaps)

    def test_cli_exit_codes(self) -> None:
        self.assertEqual(trace.main(["--root", str(ROOT)]), 0)
        self.assertEqual(trace.main(["--root", str(ROOT / "missing")]), 2)

    def test_missing_registry_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for rel in (trace.PRD, trace.ATLAS, trace.TRACE):
                dest = Path(tmp) / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(read(rel), encoding="utf-8")
            self.assertEqual(trace.main(["--root", tmp]), 2)


if __name__ == "__main__":
    unittest.main()
