import csv
import tempfile
import unittest
from io import BytesIO
from pathlib import Path

from openpyxl import Workbook

from prototype.properwarm.imports import parse_workbook
from prototype.properwarm.storage import Store


HEADERS = [
    "candidate_id",
    "property_ref",
    "current_status",
    "owner",
    "locality",
    "archetype_id",
    "lead_supplier",
    "rag_status",
    "is_synthetic",
]


def workbook_bytes(headers: list[str], rows: list[list[object]]) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "cases"
    sheet.append(headers)
    for row in rows:
        sheet.append(row)
    output = BytesIO()
    workbook.save(output)
    workbook.close()
    return output.getvalue()


def valid_row(candidate_id: str, property_ref: str) -> list[object]:
    return [
        candidate_id,
        property_ref,
        "01 Identified",
        "PM-01",
        "Locality A",
        "ARC-01",
        "SUP-F1",
        "Green",
        True,
    ]


def write_source(source: Path) -> None:
    source.mkdir()
    with (source / "candidate-lifecycle.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADERS)
        writer.writerow(valid_row("CAND-SEED-0001", "SYN-PROP-SEED-0001"))
    with (source / "safety-holds.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(["candidate_id", "is_synthetic", "hold_status_in_tracker"])


class ImportTests(unittest.TestCase):
    def test_unknown_column_rejects_rows_and_reports_reasons(self) -> None:
        content = workbook_bytes(HEADERS + ["resident_ref"], [valid_row("CAND-IMPORT-0001", "SYN-PROP-IMPORT-0001") + ["R-SYN-1"]])

        preview = parse_workbook(content, "unknown.xlsx", set())

        self.assertEqual(len(preview.accepted), 0)
        self.assertEqual(len(preview.rejected), 1)
        self.assertTrue(any("unmapped columns" in issue for issue in preview.rejected[0]["issues"]))

    def test_duplicate_rows_and_unmapped_values_are_visible_as_rejected(self) -> None:
        content = workbook_bytes(
            HEADERS,
            [
                valid_row("CAND-IMPORT-0001", "SYN-PROP-IMPORT-0001"),
                valid_row("CAND-IMPORT-0001", "SYN-PROP-IMPORT-0001"),
                [
                    "CAND-IMPORT-0002",
                    "SYN-PROP-IMPORT-0002",
                    "Future status",
                    "PM-01",
                    "Locality A",
                    "ARC-01",
                    "SUP-F1",
                    "Green",
                    False,
                ],
            ],
        )

        preview = parse_workbook(content, "rows.xlsx", set())

        self.assertEqual([row["source_row"] for row in preview.accepted], [2])
        self.assertEqual([row["source_row"] for row in preview.rejected], [3, 4])
        self.assertTrue(any("duplicated" in issue for issue in preview.rejected[0]["issues"]))
        self.assertTrue(any("unmapped value" in issue for issue in preview.rejected[1]["issues"]))
        self.assertTrue(any("is_synthetic must be true" in issue for issue in preview.rejected[1]["issues"]))

    def test_conflicting_id_formula_and_source_immutability(self) -> None:
        content = workbook_bytes(
            HEADERS, [valid_row("CAND-SEED-0001", "SYN-PROP-SEED-0001")]
        )
        original = content
        preview = parse_workbook(content, "same-id.xlsx", {"CAND-SEED-0001"})

        self.assertEqual(content, original)
        self.assertEqual(preview.accepted, [])
        self.assertTrue(any("already exists" in issue for issue in preview.rejected[0]["issues"]))

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "cases"
        sheet.append(HEADERS)
        sheet.append(valid_row("CAND-IMPORT-0003", "SYN-PROP-IMPORT-0003"))
        sheet["B2"] = '=CONCAT("SYN-PROP-","IMPORT-0003")'
        output = BytesIO()
        workbook.save(output)
        workbook.close()
        formula_preview = parse_workbook(output.getvalue(), "formula.xlsx", set())
        self.assertTrue(any("Formula cells" in issue for issue in formula_preview.rejected[0]["issues"]))

    def test_commit_revalidates_conflicts_atomically_and_keeps_source_row(self) -> None:
        content = workbook_bytes(
            HEADERS,
            [
                valid_row("CAND-IMPORT-0004", "SYN-PROP-IMPORT-0004"),
                valid_row("CAND-IMPORT-0005", "SYN-PROP-IMPORT-0005"),
            ],
        )
        preview = parse_workbook(content, "lineage.xlsx", set())
        self.assertEqual(
            [record["source_row"] for record in preview.accepted], [2, 3]
        )

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            write_source(source)
            store = Store(root / "data" / "prototype.sqlite3", source)
            competing_record = dict(preview.accepted[1])
            store.import_cases(
                [competing_record], "competing.xlsx", "1" * 64, 0, "Local reviewer"
            )
            with self.assertRaisesRegex(ValueError, "nothing was imported"):
                store.import_cases(
                    preview.accepted,
                    "lineage.xlsx",
                    preview.digest,
                    len(preview.rejected),
                    "Local reviewer",
                )
            self.assertIsNone(store.get_case("CAND-IMPORT-0004"))

            imported = store.get_case("CAND-IMPORT-0005")
            self.assertEqual(imported["source_row"], 3)
            self.assertEqual(imported["source_file"], "competing.xlsx")


if __name__ == "__main__":
    unittest.main()
