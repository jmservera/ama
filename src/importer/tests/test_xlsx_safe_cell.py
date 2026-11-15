"""Issue 80: the importer neutralises formula injection the same way as the shared list export."""

import unittest

from zava_forward.core import list_export

from zava_forward.importer import xlsx


class SafeCellTests(unittest.TestCase):
    def test_leading_whitespace_before_a_formula_prefix_is_neutralised(self) -> None:
        for bad in ("=1+1", "+1", "-1", "@SUM(A1)", "\tx", " =1+1", "  @SUM(A1)", " \t-1", "\n=1"):
            self.assertEqual(xlsx.safe_cell(bad), "'" + bad, repr(bad))

    def test_plain_text_is_unchanged(self) -> None:
        for ok in ("plain", "a =b", "", "1 - 2"):
            self.assertEqual(xlsx.safe_cell(ok), ok)
        self.assertEqual(xlsx.safe_cell(None), "")

    def test_matches_the_shared_list_export_for_text_cells(self) -> None:
        for text in ("=1", " =1", "\t+1", "  -x", "ok", " ok", "a@b"):
            self.assertEqual(xlsx.safe_cell(text), list_export.safe_cell(text), repr(text))


if __name__ == "__main__":
    unittest.main()
