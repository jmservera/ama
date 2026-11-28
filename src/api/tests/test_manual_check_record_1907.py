"""Guard the manual assistive-technology check record (#1907).

The record in the WCAG baseline stays `Not run` for the demo (owner decision 2026-11-18).
These checks do not prove the criterion; they stop a cell being filled without a named
tester, date and technology, or a Result being claimed without keyboard and screen-reader runs.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOC = ROOT / "docs" / "reference" / "research" / "ux" / "wcag-conformance-baseline.md"
NOT_RUN = "Not run"
EXPECTED_ROLES = 8
ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
SCREEN_READER = re.compile(r"\b(NVDA|VoiceOver)\b")


def record_rows() -> list[list[str]]:
    text = DOC.read_text()
    section = text.split("## Manual check record", 1)[1].split("\n## ", 1)[0]
    rows: list[list[str]] = []
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] in ("Role workflow",) or set(cells[0]) <= {"-", " "}:
            continue
        rows.append(cells)
    return rows


def named_record(cell: str) -> bool:
    """A filled cell needs a tester (text before the first comma), an ISO date and a tool."""
    if cell == NOT_RUN:
        return True
    parts = [p.strip() for p in cell.split(",")]
    return len(parts) >= 3 and bool(parts[0]) and bool(ISO_DATE.search(cell))


class ManualCheckRecord(unittest.TestCase):
    def test_record_has_one_row_per_role_with_five_columns(self) -> None:
        rows = record_rows()
        self.assertEqual(len(rows), EXPECTED_ROLES)
        for row in rows:
            self.assertEqual(len(row), 5, row[0])

    def test_filled_cells_name_tester_date_and_tool(self) -> None:
        for role, *cells in record_rows():
            for cell in cells:
                self.assertTrue(named_record(cell), f"{role}: {cell!r}")

    def test_screen_reader_cells_name_supported_technology(self) -> None:
        for role, _keyboard, screen_reader, *_ in record_rows():
            if screen_reader != NOT_RUN:
                self.assertRegex(screen_reader, SCREEN_READER, role)

    def test_result_needs_keyboard_and_screen_reader_runs(self) -> None:
        for role, keyboard, screen_reader, _zoom, result in record_rows():
            if result != NOT_RUN:
                self.assertNotEqual(keyboard, NOT_RUN, role)
                self.assertNotEqual(screen_reader, NOT_RUN, role)

    def test_named_record_rejects_unnamed_claims(self) -> None:
        self.assertFalse(named_record("Pass"))
        self.assertFalse(named_record("A. Tester, 2026-12-01"))
        self.assertTrue(named_record("A. Tester, 2026-12-01, NVDA 2024.4 with Firefox 133, pass"))


if __name__ == "__main__":
    unittest.main()
