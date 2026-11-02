"""Production UX acceptance protocol (#619): human-owned record rows, no fabricated result."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
UX = ROOT / "docs" / "reference" / "research" / "ux"
PROTOCOL = UX / "production-ux-acceptance-protocol.md"
TEXT = PROTOCOL.read_text()


def record_rows(section: str) -> list[list[str]]:
    body = TEXT.split("### " + section, 1)[1].split("\n#", 1)[0]
    rows = [line for line in body.splitlines() if line.startswith("|")][2:]
    return [[cell.strip() for cell in row.strip("|").split("|")] for row in rows]


class ProductionUxAcceptanceProtocol(unittest.TestCase):
    def test_every_record_cell_is_not_run_or_names_tester_and_date(self) -> None:
        rows = record_rows("Script A and B record") + record_rows("Script C record")
        self.assertGreaterEqual(len(rows), 4)
        for row in rows:
            for cell in row[1:]:
                if cell == "Not run":
                    continue
                self.assertRegex(cell, r"\d{4}-\d{2}-\d{2}", row[0])
                self.assertIn("tester", cell.lower(), row[0])

    def test_surfaces_and_assistive_technology_are_covered(self) -> None:
        for needle in (
            "Resident chat widget",
            "Employee chat widget",
            "Employee single case view",
            "NVDA with Firefox",
            "VoiceOver with Safari",
            "400 percent zoom",
            "consent before data use",
            "Not consent to works".lower(),
        ):
            self.assertIn(needle.lower(), TEXT.lower(), needle)

    def test_real_resident_approvals_are_required_and_no_conformance_is_claimed(self) -> None:
        self.assertIn("DPO and Legal", TEXT)
        self.assertIn("synthetic only", TEXT)
        self.assertNotRegex(TEXT, r"(?i)\bconforms to wcag|meets wcag 2\.2 aa\b")

    def test_baseline_links_to_protocol_and_issue_is_not_closed_by_keyword(self) -> None:
        baseline = (UX / "wcag-conformance-baseline.md").read_text()
        self.assertIn("production-ux-acceptance-protocol.md", baseline)
        self.assertIn("must not use a closing", TEXT)
        self.assertIsNone(re.search(r"(?i)\bcloses #619", TEXT))


if __name__ == "__main__":
    unittest.main()
