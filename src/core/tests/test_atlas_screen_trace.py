"""Atlas-to-screen trace completeness regressions (Refs #233)."""

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

    def test_hypothesis_label_required(self) -> None:
        doc = self.doc.replace("hypotheses", "findings").replace("hypothesis", "finding")
        doc = doc.replace("Hypothes", "Finding")
        gaps = trace.check(self.prd, self.atlas, doc)["gaps"]
        self.assertTrue(any("hypotheses" in g for g in gaps))

    def test_cli_exit_codes(self) -> None:
        self.assertEqual(trace.main(["--root", str(ROOT)]), 0)
        self.assertEqual(trace.main(["--root", str(ROOT / "missing")]), 2)


if __name__ == "__main__":
    unittest.main()
