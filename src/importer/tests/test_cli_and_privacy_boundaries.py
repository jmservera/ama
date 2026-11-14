"""Deterministic importer CLI, workbook-safety and synthetic-data privacy boundaries."""

from __future__ import annotations

import contextlib
import io
import runpy
import sqlite3
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from zava_forward.importer.export import compare, to_csv
from zava_forward.importer.mapping import CASE_LIST, build_preview, preview_bytes
from zava_forward.importer.xlsx import WorkbookError, read_workbook, safe_cell, write_workbook

SECRET_ADDRESS = "SYNTHETIC-SECRET-ADDRESS 12 Example Row"
SECRET_HEADER = "SYNTHETIC-SECRET-HEADER"
HEAD = ["Ref", "Property Address", "Post code", "Stage"]
CLEAN = [HEAD, ["ZF-1", SECRET_ADDRESS, "AB1 2CD", "Survey"]]
BAD_POSTCODE = [HEAD, ["ZF-2", SECRET_ADDRESS, "not-a-postcode", "Survey"]]
NO_REF = [[SECRET_HEADER, "Property Address", "Post code", "Stage"], ["x", "y", "AB1 2CD", "s"]]


def run_cli(*argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with (
        mock.patch.object(sys, "argv", ["importer", *argv]),
        contextlib.redirect_stdout(out),
        contextlib.redirect_stderr(err),
        self_exit() as raised,
    ):
        runpy.run_module("zava_forward.importer", run_name="__main__")
    return raised[0], out.getvalue(), err.getvalue()


@contextlib.contextmanager
def self_exit():  # type: ignore[no-untyped-def]
    code = [0]
    try:
        yield code
    except SystemExit as stop:
        code[0] = int(stop.code or 0)


class CliTests(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)

    def workbook(self, rows: list[list[str]], name: str = "cases.xlsx") -> Path:
        path = self.dir / name
        path.write_bytes(write_workbook({"Cases": rows}))
        return path

    def test_no_arguments_prints_version_only(self) -> None:
        code, out, _ = run_cli()
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("zava-forward-import "))

    def test_preview_clean_workbook_is_read_only_and_exits_zero(self) -> None:
        path = self.workbook(CLEAN)
        before = path.read_bytes()
        code, out, _ = run_cli("preview", str(path))
        self.assertEqual(code, 0)
        self.assertIn("ready=1 to_fix=0", out)
        self.assertEqual(path.read_bytes(), before)

    def test_preview_reports_row_problems_by_field_not_by_cell_value(self) -> None:
        code, out, _ = run_cli("preview", str(self.workbook(BAD_POSTCODE)))
        self.assertEqual(code, 0)
        self.assertIn("postcode looks wrong", out)
        self.assertNotIn(SECRET_ADDRESS, out)
        self.assertNotIn("not-a-postcode", out)

    def test_preview_blocks_on_missing_required_column(self) -> None:
        code, out, _ = run_cli("preview", str(self.workbook(NO_REF)))
        self.assertEqual(code, 1)
        self.assertIn("CONFLICT: Required column reference is missing", out)

    def test_preview_of_unreadable_input_exits_two(self) -> None:
        for name, data in (("missing.xlsx", None), ("bad.xlsx", b"not a zip")):
            path = self.dir / name
            if data is not None:
                path.write_bytes(data)
            with self.subTest(name=name):
                code, out, err = run_cli("preview", str(path))
                self.assertEqual((code, out), (2, ""))
                self.assertIn("Cannot import", err)

    def test_stage_then_refuse_duplicate_free_flow_never_echoes_cells(self) -> None:
        db = self.dir / "import.db"
        code, out, _ = run_cli(
            "stage", str(self.workbook(CLEAN)), "--db", str(db), "--staged-by", "Synthetic Steward"
        )
        self.assertEqual(code, 0)
        self.assertIn("status=staged", out)
        code, out, _ = run_cli(
            "stage", str(self.workbook(NO_REF)), "--db", str(db), "--staged-by", "Synthetic Steward"
        )
        self.assertEqual(code, 1)
        self.assertIn("Nothing staged", out)
        self.assertNotIn(SECRET_HEADER, out)

    def test_stage_requires_a_named_person(self) -> None:
        code, _, err = run_cli(
            "stage", str(self.workbook(CLEAN)), "--db", str(self.dir / "x.db"), "--staged-by", " "
        )
        self.assertEqual(code, 2)
        self.assertIn("Cannot import", err)

    def test_exceptions_diagnostic_is_read_only_and_hides_cell_values(self) -> None:
        db = self.dir / "import.db"
        run_cli("stage", str(self.workbook(NO_REF)), "--db", str(db), "--staged-by", "Pat")
        with mock.patch.dict("os.environ", {}, clear=False):
            code, out, _ = run_cli("exceptions", str(db))
        self.assertEqual(code, 0)
        self.assertIn("Nothing was retried, approved or changed.", out)
        self.assertNotIn(SECRET_HEADER, out)

    def test_exceptions_on_unusable_database_exits_two(self) -> None:
        bad = self.dir / "not-a-db.db"
        bad.write_bytes(b"this is not a sqlite database" * 20)
        code, out, err = run_cli("exceptions", str(bad))
        self.assertEqual((code, out), (2, ""))
        self.assertIn("Nothing was recorded", err)

    def test_stage_database_failure_exits_two_and_records_nothing(self) -> None:
        bad = self.dir / "not-a-db.db"
        bad.write_bytes(b"this is not a sqlite database" * 20)
        code, out, err = run_cli(
            "stage", str(self.workbook(CLEAN)), "--db", str(bad), "--staged-by", "Pat"
        )
        self.assertEqual((code, out), (2, ""))
        self.assertIn("Cannot stage", err)

    def test_transfer_reports_store_that_cannot_be_opened(self) -> None:
        db = self.dir / "import.db"
        run_cli("stage", str(self.workbook(NO_REF)), "--db", str(db), "--staged-by", "Pat")
        with (
            mock.patch.dict(
                "os.environ",
                {"ZF_STORE": "json", "ZF_DATA": str(self.dir / "no" / "dir" / "x.json")},
            ),
            mock.patch("zava_forward.core.factory.open_store", side_effect=OSError("synthetic")),
        ):
            code, out, err = run_cli("transfer", str(db))
        self.assertEqual((code, out), (2, ""))
        self.assertIn("Nothing was recorded", err)


class WorkbookSafetyTests(unittest.TestCase):
    def rewrite(self, part: str, text: str) -> bytes:
        src = write_workbook({"Cases": CLEAN})
        out = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(src)) as zin, zipfile.ZipFile(out, "w") as zout:
            for info in zin.infolist():
                data = text.encode() if info.filename == part else zin.read(info.filename)
                zout.writestr(info.filename, data)
        return out.getvalue()

    def test_entity_declarations_and_non_utf8_parts_are_refused(self) -> None:
        for text in ('<!DOCTYPE x [<!ENTITY a "b">]><x/>', "<!entity>"):
            with self.subTest(text=text), self.assertRaises(WorkbookError):
                read_workbook(self.rewrite("xl/workbook.xml", text))
        src = write_workbook({"Cases": CLEAN})
        out = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(src)) as zin, zipfile.ZipFile(out, "w") as zout:
            for info in zin.infolist():
                data = (
                    b"\xff\xfe" if info.filename == "xl/workbook.xml" else zin.read(info.filename)
                )
                zout.writestr(info.filename, data)
        with self.assertRaisesRegex(WorkbookError, "not UTF-8"):
            read_workbook(out.getvalue())

    def test_missing_parts_and_corrupt_archives_are_refused_with_generic_text(self) -> None:
        for data in (b"", b"PK\x03\x04garbage", self.rewrite("xl/workbook.xml", "<unclosed")):
            with self.subTest(size=len(data)), self.assertRaises(WorkbookError) as raised:
                read_workbook(data)
            self.assertNotIn("SYNTHETIC", str(raised.exception))
        out = io.BytesIO()
        with zipfile.ZipFile(out, "w") as zf:
            zf.writestr("hello.txt", "x")
        with self.assertRaisesRegex(WorkbookError, "not a valid .xlsx"):
            read_workbook(out.getvalue())

    def test_bounds_on_rows_columns_and_cell_references(self) -> None:
        sheet = (
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            "<sheetData>{}</sheetData></worksheet>"
        )
        cases = {
            "rows": '<row r="9999999"><c r="A1"><v>1</v></c></row>',
            "columns": '<row r="1"><c r="ZZZ1"><v>1</v></c></row>',
            "reference": '<row r="1"><c r="1"><v>1</v></c></row>',
        }
        for name, body in cases.items():
            with self.subTest(name=name), self.assertRaises(WorkbookError):
                read_workbook(self.rewrite("xl/worksheets/sheet1.xml", sheet.format(body)))

    def test_shared_and_numeric_cells_are_read_as_text(self) -> None:
        sheet = (
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<sheetData><row r="1"><c r="A1" t="s"><v>0</v></c><c r="C1"><v> 7 </v></c>'
            '<c r="D1" t="s"><v>5</v></c></row></sheetData></worksheet>'
        )
        shared = (
            '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            "<si><t>shared</t></si></sst>"
        )
        src = self.rewrite("xl/worksheets/sheet1.xml", sheet)
        out = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(src)) as zin, zipfile.ZipFile(out, "w") as zout:
            for info in zin.infolist():
                zout.writestr(info.filename, zin.read(info.filename))
            zout.writestr("xl/sharedStrings.xml", shared)
        self.assertEqual(read_workbook(out.getvalue())["Cases"], [["shared", "", "7", ""]])

    def test_negative_shared_string_index_is_refused(self) -> None:
        sheet = (
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<sheetData><row r="1"><c r="A1" t="s"><v>-1</v></c></row></sheetData></worksheet>'
        )
        with self.assertRaisesRegex(WorkbookError, "shared string"):
            read_workbook(self.rewrite("xl/worksheets/sheet1.xml", sheet))


class SyntheticDataBoundaryTests(unittest.TestCase):
    def test_formula_prefixes_are_neutralised_in_workbook_and_csv_exports(self) -> None:
        for value in ("=1+1", "+cmd", "-cmd", "@SUM(A1)"):
            self.assertEqual(safe_cell(value), "'" + value)
        self.assertEqual(safe_cell(None), "")
        text = to_csv(["=h"], [["=1+1", "plain"]])
        self.assertIn("'=h", text)
        self.assertIn("'=1+1", text)
        sheets = read_workbook(write_workbook({"S": [["=bad"]]}))
        self.assertEqual(sheets["S"], [["'=bad"]])

    def test_preview_bytes_refuses_content_that_fails_the_scan(self) -> None:
        with (
            mock.patch(
                "zava_forward.importer.mapping.LocalSignatureScanner.scan",
                return_value=("infected", "synthetic"),
            ),
            self.assertRaisesRegex(WorkbookError, "content scan"),
        ):
            preview_bytes("x.xlsx", write_workbook({"Cases": CLEAN}))

    def test_empty_or_missing_sheet_is_a_blocking_conflict(self) -> None:
        prev = build_preview(CASE_LIST, "x.xlsx", "0" * 64, {})
        self.assertTrue(prev.blocking)
        self.assertEqual(prev.rows, [])

    def test_blank_rows_are_skipped_and_duplicates_flagged(self) -> None:
        rows = [
            HEAD,
            ["ZF-1", "a", "AB1 2CD", "s"],
            ["", "", "", ""],
            ["ZF-1", "b", "AB1 2CD", "s"],
        ]
        prev = build_preview(CASE_LIST, "x.xlsx", "0" * 64, {"Cases": rows})
        self.assertEqual([r.row for r in prev.rows], [2, 4])
        self.assertTrue(prev.blocking)
        self.assertTrue(any("duplicate reference" in p for p in prev.rows[1].problems))

    def test_compare_is_read_only_and_reports_changes(self) -> None:
        current = {"a": {"stage": "Survey"}, "b": {"stage": "Design"}, "c": {"stage": "X"}}
        incoming = {"a": {"stage": "Design"}, "c": {"stage": "X"}, "d": {"stage": "New"}}
        result = compare(current, incoming)
        self.assertEqual(result.added, ["d"])
        self.assertEqual(result.removed, ["b"])
        self.assertEqual(result.changed, {"a": {"stage": ("Survey", "Design")}})
        self.assertEqual(result.unchanged, ["c"])
        self.assertEqual(current["a"], {"stage": "Survey"})

    def test_ledger_stores_no_cell_values_for_a_refused_workbook(self) -> None:
        from zava_forward.importer.exceptions import RefusalLedger, submit_file
        from zava_forward.importer.quarantine import QuarantineStore

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.xlsx"
            path.write_bytes(write_workbook({"Cases": NO_REF}))
            conn = sqlite3.connect(":memory:")
            store, ledger = QuarantineStore(conn), RefusalLedger(conn)
            store.create_schema()
            ledger.create_schema()
            result = submit_file(store, ledger, path, "Synthetic Steward", CASE_LIST)
            self.assertIsNone(result.batch)
            dump = "\n".join(str(r) for r in conn.execute("SELECT * FROM import_refusals"))
            self.assertNotIn(SECRET_HEADER, dump)
            conn.close()


if __name__ == "__main__":
    unittest.main()
