"""Issue 80: formula-safe, values-only CSV for any list of rows."""

import csv
import io
import unittest

from zava_forward.core import list_export, quality


class ListExportTests(unittest.TestCase):
    def test_formula_prefixes_are_neutralised(self) -> None:
        for bad in ("=1+1", "+1", "-1", "@SUM(A1)", "\tx", "\rx"):
            self.assertEqual(list_export.safe_cell(bad), "'" + bad)
        self.assertEqual(list_export.safe_cell("plain"), "plain")
        self.assertEqual(list_export.safe_cell(None), "")
        self.assertEqual(list_export.safe_cell(False), "No")
        self.assertEqual(list_export.safe_cell(7), "7")

    def test_columns_are_union_in_first_seen_order_and_nested_values_are_text(self) -> None:
        rows: list[dict[str, object]] = [
            {"id": "A", "tags": ["x", "y"]},
            {"id": "=B", "extra": {"k": 1}},
        ]
        out = list(csv.reader(io.StringIO(list_export.to_csv(rows))))
        self.assertEqual(out[0], ["id", "tags", "extra"])
        self.assertEqual(out[1], ["A", '["x","y"]', ""])
        self.assertEqual(out[2], ["'=B", "", '{"k":1}'])

    def test_empty_list_gives_empty_file_not_an_error(self) -> None:
        self.assertEqual(list_export.to_csv([]), "\r\n")

    def test_checklist_rows_are_stable_fields_over_every_check(self) -> None:
        rows = quality.checklist_rows()
        self.assertEqual(sum(len(v["items"]) for v in quality.CHECKLISTS.values()), len(rows))
        for row in rows:
            self.assertEqual(list(row), ["measure", "version", "step", "check"])
        self.assertEqual(rows[0]["step"], 1)
        self.assertEqual(rows[0]["version"], quality.CHECKLISTS[rows[0]["measure"]]["version"])


if __name__ == "__main__":
    unittest.main()
