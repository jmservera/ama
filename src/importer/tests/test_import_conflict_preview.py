"""Regression slice for #80: staged import and comparison never touch the source workbook."""

import hashlib
import tempfile
import unittest
from pathlib import Path

from zava_forward.importer.export import compare
from zava_forward.importer.mapping import preview_file
from zava_forward.importer.quarantine import ImportError_, QuarantineStore
from zava_forward.importer.xlsx import write_workbook

HEADER = ["Ref", "Property Address", "Post code", "Stage", "Owner"]
CURRENT = [
    HEADER,
    ["ZF-1", "1 Synthetic Row", "AB1 2CD", "Survey", "Sam"],
    ["ZF-2", "2 Synthetic Row", "AB1 2CE", "Design", "Alex"],
    ["ZF-3", "3 Synthetic Row", "AB1 2CF", "Install", "Sam"],
]
INCOMING = [
    HEADER,
    ["ZF-1", "1 Synthetic Row", "AB1 2CD", "Survey", "Sam"],
    ["ZF-2", "2 Synthetic Row", "AB1 2CE", "Install", "Alex"],
    ["ZF-4", "4 Synthetic Row", "AB1 2CG", "Survey", "Sam"],
]


def fingerprint(path: Path) -> tuple[str, int, int]:
    stat = path.stat()
    return hashlib.sha256(path.read_bytes()).hexdigest(), stat.st_size, stat.st_mtime_ns


def keyed(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {r["reference"]: r for r in rows}


class ImportConflictPreviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = QuarantineStore.in_memory()
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)

    def workbook(self, name: str, rows: list[list[str]]) -> Path:
        path = Path(self.folder.name) / name
        path.write_bytes(write_workbook({"Cases": rows}))
        path.chmod(0o444)
        return path

    def test_source_bytes_survive_stage_approve_and_compare(self) -> None:
        src = self.workbook("incoming.xlsx", INCOMING)
        before = fingerprint(src)
        base = self.store.stage(preview_file(self.workbook("current.xlsx", CURRENT))[0], "Sam")
        self.store.approve(base.batch_id, "Priya")
        prev, data = preview_file(src)
        rec = self.store.stage(prev, "Sam")
        compare(keyed(self.store.rows(base.batch_id)), keyed(self.store.rows(rec.batch_id)))
        self.store.approve(rec.batch_id, "Priya")
        self.assertEqual(fingerprint(src), before)
        self.assertEqual(data, src.read_bytes())
        self.assertEqual(rec.source_sha256, before[0])
        self.assertEqual(
            sorted(p.name for p in Path(self.folder.name).iterdir()),
            [
                "current.xlsx",
                "incoming.xlsx",
            ],
        )

    def test_blocking_conflicts_refuse_staging_and_write_nothing(self) -> None:
        dup = self.workbook("dup.xlsx", [*INCOMING, INCOMING[1]])
        ambiguous = self.workbook("amb.xlsx", [["Ref", "Case ID", "Address", "Postcode"], ["1"]])
        for path in (dup, ambiguous):
            before = fingerprint(path)
            prev, _ = preview_file(path)
            self.assertTrue(prev.blocking)
            with self.assertRaises(ImportError_):
                self.store.stage(prev, "Sam")
            self.assertEqual(fingerprint(path), before)
        self.assertTrue(any("Duplicate" in c for c in preview_file(dup)[0].conflicts))
        self.assertEqual(self.store.history("case-list"), [])
        self.assertEqual(
            self.store.conn.execute("SELECT COUNT(*) FROM import_rows").fetchone()[0], 0
        )

    def test_row_problems_are_not_conflicts_but_need_acceptance(self) -> None:
        prev, _ = preview_file(
            self.workbook("fix.xlsx", [HEADER, ["ZF-9", "", "nope", "Survey", ""]])
        )
        self.assertFalse(prev.blocking)
        rec = self.store.stage(prev, "Sam")
        with self.assertRaises(ImportError_):
            self.store.approve(rec.batch_id, "Priya")
        self.assertEqual(self.store.get(rec.batch_id).status, "staged")
        self.assertEqual(
            self.store.approve(rec.batch_id, "Priya", accept_row_problems=True).status, "approved"
        )

    def test_comparison_classifies_changes_and_leaves_history_alone(self) -> None:
        base = self.store.stage(preview_file(self.workbook("current.xlsx", CURRENT))[0], "Sam")
        self.store.approve(base.batch_id, "Priya")
        rec = self.store.stage(preview_file(self.workbook("incoming.xlsx", INCOMING))[0], "Sam")
        history = self.store.history("case-list")
        current = self.store.current("case-list")
        out = compare(keyed(self.store.rows(base.batch_id)), keyed(self.store.rows(rec.batch_id)))
        self.assertEqual((out.added, out.removed, out.unchanged), (["ZF-4"], ["ZF-3"], ["ZF-1"]))
        self.assertEqual(out.changed, {"ZF-2": {"stage": ("Design", "Install")}})
        self.assertEqual(self.store.history("case-list"), history)
        self.assertEqual(self.store.current("case-list"), current)
        self.assertEqual(self.store.get(rec.batch_id).status, "staged")

    def test_supersession_keeps_prior_rows_and_rejection_supersedes_nothing(self) -> None:
        first = self.store.stage(preview_file(self.workbook("current.xlsx", CURRENT))[0], "Sam")
        self.store.approve(first.batch_id, "Priya")
        rejected = self.store.stage(preview_file(self.workbook("bad.xlsx", INCOMING))[0], "Sam")
        self.store.reject(rejected.batch_id, "Priya", "wrong file")
        self.assertEqual(self.store.get(first.batch_id).status, "approved")
        second = self.store.stage(preview_file(self.workbook("incoming.xlsx", INCOMING))[0], "Sam")
        self.store.approve(second.batch_id, "Priya")
        hist = self.store.history("case-list")
        self.assertEqual([h.status for h in hist], ["superseded", "rejected", "approved"])
        self.assertEqual(hist[0].superseded_by, second.batch_id)
        self.assertIsNone(hist[1].superseded_by)
        self.assertEqual(len(self.store.rows(first.batch_id)), 3)
        self.assertEqual(len(self.store.rows(second.batch_id)), 3)
        latest = self.store.current("case-list")
        assert latest is not None
        self.assertEqual(latest.batch_id, second.batch_id)


if __name__ == "__main__":
    unittest.main()
