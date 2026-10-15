import hashlib
import sqlite3
import tempfile
import unittest
import zipfile
from pathlib import Path

from zava_forward.importer.export import compare, history_rows, to_csv, to_xlsx
from zava_forward.importer.mapping import CASE_LIST, build_preview, preview_file
from zava_forward.importer.quarantine import ImportError_, QuarantineStore
from zava_forward.importer.xlsx import WorkbookError, read_workbook, write_workbook

GOOD = [
    ["Ref", "Property Address", "Post code", "Stage", "Owner"],
    ["ZF-1", "1 Synthetic Row", "AB1 2CD", "Survey", "Sam"],
    ["ZF-2", "2 Synthetic Row", "AB1 2CE", "Design", "Alex"],
]
SYNTHETIC_BYTES = write_workbook({"Cases": GOOD})


def preview_of(rows: list[list[str]]):  # type: ignore[no-untyped-def]
    return build_preview(CASE_LIST, "demo.xlsx", "a" * 64, {"Cases": rows})


class XlsxTests(unittest.TestCase):
    def test_round_trip(self) -> None:
        self.assertEqual(read_workbook(SYNTHETIC_BYTES)["Cases"], GOOD)

    def test_formula_text_is_neutralised_on_write(self) -> None:
        data = write_workbook({"S": [["=1+1", "@x", "ok"]]})
        self.assertEqual(read_workbook(data)["S"], [["'=1+1", "'@x", "ok"]])

    def test_rejects_non_workbook_and_entities(self) -> None:
        with self.assertRaises(WorkbookError):
            read_workbook(b"not a zip")
        buf = Path(tempfile.mkdtemp()) / "x.xlsx"
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("xl/workbook.xml", '<!DOCTYPE x [<!ENTITY a "b">]><workbook/>')
            zf.writestr("xl/_rels/workbook.xml.rels", "<r/>")
        with self.assertRaises(WorkbookError):
            read_workbook(buf.read_bytes())


class PreviewTests(unittest.TestCase):
    def test_mapping_by_alias_and_ready_rows(self) -> None:
        prev = preview_of(GOOD)
        how = {c.field: c.how for c in prev.columns}
        self.assertEqual(how["reference"], "alias")
        self.assertEqual(how["status"], "unmapped")
        self.assertFalse(prev.blocking)
        self.assertEqual(prev.ready, 2)
        self.assertEqual(prev.rows[0].lineage["row"], 2)
        self.assertEqual(prev.rows[0].lineage["source_sha256"], "a" * 64)

    def test_conflicts_missing_required_and_duplicates(self) -> None:
        self.assertTrue(preview_of([["Ref", "Address"], ["1", "x"]]).blocking)
        dup = preview_of([*GOOD, ["ZF-1", "3 Synthetic Row", "AB1 2CF", "Survey", ""]])
        self.assertTrue(dup.blocking)
        self.assertTrue(any("duplicate" in p for p in dup.rows[-1].problems))
        both = preview_of([["Ref", "Case ID", "Address", "Postcode", "Stage"]])
        self.assertTrue(any("Several columns" in c for c in both.conflicts))

    def test_row_problems(self) -> None:
        prev = preview_of([GOOD[0], ["ZF-9", "", "nope", "Survey", ""]])
        self.assertEqual(prev.rows[0].problems, ["address is empty", "postcode looks wrong"])
        self.assertEqual(len(prev.to_fix), 1)

    def test_source_file_is_never_changed(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "demo.xlsx"
            path.write_bytes(SYNTHETIC_BYTES)
            path.chmod(0o444)
            before = (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns)
            prev, _ = preview_file(path)
            self.assertEqual(
                before, (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns)
            )
            self.assertEqual(prev.source_sha256, before[0])

    def test_scanner_blocks_marker_and_type_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            bad = Path(folder) / "bad.xlsx"
            bad.write_bytes(b"plain text, not a zip")
            with self.assertRaises(WorkbookError):
                preview_file(bad)
            marked = Path(folder) / "m.xlsx"
            marked.write_bytes(SYNTHETIC_BYTES + b"ZF-SYNTHETIC-MALWARE-TEST-MARKER")
            with self.assertRaises(WorkbookError):
                preview_file(marked)


class QuarantineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = QuarantineStore.in_memory()

    def test_stage_needs_clean_mapping_and_name(self) -> None:
        with self.assertRaises(ImportError_):
            self.store.stage(preview_of([["Ref"], ["1"]]), "Sam")
        with self.assertRaises(ImportError_):
            self.store.stage(preview_of(GOOD), " ")

    def test_human_approval_gate(self) -> None:
        rec = self.store.stage(preview_of(GOOD), "Sam")
        self.assertEqual((rec.status, rec.version), ("staged", 1))
        for who in ("", "AI", "system", "sam"):
            with self.assertRaises(ImportError_):
                self.store.approve(rec.batch_id, who)
        done = self.store.approve(rec.batch_id, "Priya", "checked")
        self.assertEqual((done.status, done.decided_by), ("approved", "Priya"))
        with self.assertRaises(ImportError_):
            self.store.approve(rec.batch_id, "Priya")

    def test_row_problems_need_explicit_acceptance(self) -> None:
        rec = self.store.stage(preview_of([GOOD[0], ["ZF-9", "", "AB1 2CD", "Survey", ""]]), "Sam")
        with self.assertRaises(ImportError_):
            self.store.approve(rec.batch_id, "Priya")
        self.assertEqual(
            self.store.approve(rec.batch_id, "Priya", accept_row_problems=True).status, "approved"
        )

    def test_supersession_history(self) -> None:
        a = self.store.stage(preview_of(GOOD), "Sam")
        self.store.approve(a.batch_id, "Priya")
        b = self.store.stage(preview_of(GOOD[:2]), "Sam")
        self.store.approve(b.batch_id, "Priya")
        hist = self.store.history("case-list")
        self.assertEqual([h.status for h in hist], ["superseded", "approved"])
        self.assertEqual(hist[0].superseded_by, b.batch_id)
        current = self.store.current("case-list")
        self.assertIsNotNone(current)
        assert current is not None
        self.assertEqual(current.version, 2)
        self.assertEqual(history_rows(hist)[0][8], 2)
        self.assertEqual(len(self.store.rows(a.batch_id)), 2)

    def test_reject_and_portable_sql(self) -> None:
        rec = self.store.stage(preview_of(GOOD), "Sam")
        self.assertEqual(self.store.reject(rec.batch_id, "Priya", "no").status, "rejected")
        with self.assertRaises(ImportError_):
            self.store.reject(rec.batch_id, "ai")
        import zava_forward.importer.quarantine as q

        text = Path(q.__file__).read_text(encoding="utf-8").upper()
        for banned in ("INSERT OR", "AUTOINCREMENT", "PRAGMA", "ON CONFLICT"):
            self.assertNotIn(banned, text)

    def test_unknown_batch(self) -> None:
        with self.assertRaises(KeyError):
            self.store.get("none")
        self.assertIsInstance(self.store.conn, sqlite3.Connection)


class ExportTests(unittest.TestCase):
    def test_csv_neutralises_formulas(self) -> None:
        self.assertEqual(to_csv(["a"], [["=cmd"]]).splitlines(), ["a", "'=cmd"])

    def test_xlsx_has_read_me_list_and_history_without_provider(self) -> None:
        store = QuarantineStore.in_memory()
        rec = store.stage(preview_of(GOOD), "Sam")
        store.approve(rec.batch_id, "Priya")
        sheets = read_workbook(to_xlsx("Cases", ["Ref"], [["ZF-1"]], store.history("case-list")))
        self.assertEqual(list(sheets), ["Read me", "Cases", "History"])
        self.assertIn("Read-only", sheets["Read me"][0][0])
        self.assertEqual(sheets["History"][1][3], "approved")
        self.assertEqual(sheets["History"][1][6], "Priya")
        self.assertNotIn("provider", " ".join(sheets["History"][0]).lower())

    def test_compare_is_read_only(self) -> None:
        cur = {"1": {"stage": "Survey"}, "2": {"stage": "Design"}, "3": {"stage": "Install"}}
        inc = {"1": {"stage": "Survey"}, "2": {"stage": "Install"}, "4": {"stage": "Survey"}}
        snapshot = {k: dict(v) for k, v in cur.items()}
        out = compare(cur, inc)
        self.assertEqual((out.added, out.removed, out.unchanged), (["4"], ["3"], ["1"]))
        self.assertEqual(out.changed, {"2": {"stage": ("Design", "Install")}})
        self.assertEqual(cur, snapshot)


if __name__ == "__main__":
    unittest.main()
