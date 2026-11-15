"""Guard that the cut-over parity matrix leaves no open work on mvp/ or prototype/ for Issue #201 epics."""

import csv
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "docs" / "architecture"
AUDIT = ARCH / "cutover-parity-audit.tsv"
MATRIX = ARCH / "mvp-to-src-parity-matrix.md"
EVIDENCE = ARCH / "cutover-evidence-pack.md"

EPICS = ("#113", "#136", "#165", "#157", "#149")
SRC_PACKAGES = ("core", "agents", "api", "orchestrator", "importer")
PACKAGES = "|".join(SRC_PACKAGES)
PLACED = re.compile(rf"^(?:src/(?:{PACKAGES})/|src/[^/]+$|infra/|docs/)")
OLD_ROOT = re.compile(r"^(?:mvp|prototype)/")
NO_TARGET_OUTCOMES = {"retire", "archive"}
IN_SRC_STATUSES = {"destination-present", "partial-rebuild-not-deployed-worker"}


def audit_rows():
    with AUDIT.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def targets(row):
    return [part for part in row["actual_target"].split(";") if part and part != "-"]


def unplaced_rows(rows):
    """Return audit rows that still leave work on an old path or lack a placed target."""
    found = []
    for row in rows:
        name = row["historical_path"]
        if not OLD_ROOT.match(name):
            found.append(f"{name}: historical path is not under mvp/ or prototype/")
        elif row["outcome"] in NO_TARGET_OUTCOMES:
            if targets(row):
                found.append(f"{name}: {row['outcome']} row has a target")
        elif row["status"] not in IN_SRC_STATUSES:
            found.append(f"{name}: status {row['status']} is not placed")
        elif not targets(row):
            found.append(f"{name}: no actual target")
        else:
            found.extend(
                f"{name}: target {item} is not src/, infra/ or docs/"
                for item in targets(row)
                if not PLACED.match(item)
            )
    return found


def reopen_rows(text):
    section = text.split("## Issues to Reopen", 1)[1].split("\n## ", 1)[0]
    return [line for line in section.splitlines() if line.startswith("| [#")]


class ParityLogicTests(unittest.TestCase):
    def test_unplaced_rows_flags_old_path_targets_and_open_status(self):
        base = {
            "historical_path": "mvp/a.py",
            "outcome": "migrate",
            "status": "destination-present",
            "actual_target": "src/core/src/a.py",
        }
        self.assertEqual(unplaced_rows([base]), [])
        self.assertTrue(unplaced_rows([{**base, "actual_target": "mvp/a.py"}]))
        self.assertTrue(unplaced_rows([{**base, "status": "pending"}]))
        self.assertTrue(unplaced_rows([{**base, "actual_target": "-"}]))
        self.assertTrue(unplaced_rows([{**base, "outcome": "retire"}]))


class EpicParityMatrixTests(unittest.TestCase):
    def test_every_parity_row_is_placed_on_src_infra_or_docs(self):
        rows = audit_rows()
        self.assertGreater(len(rows), 100)
        self.assertEqual(unplaced_rows(rows), [])

    def test_open_rebuild_row_targets_src_packages_only(self):
        rebuilds = [row for row in audit_rows() if row["outcome"] == "rebuild"]
        self.assertTrue(rebuilds)
        for row in rebuilds:
            with self.subTest(path=row["historical_path"]):
                self.assertTrue(targets(row))
                self.assertTrue(all(PLACED.match(item) for item in targets(row)))

    def test_every_placed_target_exists_in_the_tree(self):
        for row in audit_rows():
            for item in targets(row):
                with self.subTest(target=item):
                    self.assertTrue((ROOT / item).is_file())

    def test_reopened_issue_dispositions_move_to_src_not_old_paths(self):
        rows = reopen_rows(MATRIX.read_text(encoding="utf-8"))
        self.assertTrue(rows)
        for row in rows:
            with self.subTest(row=row[:40]):
                disposition = row.rstrip("|").rsplit("|", 1)[1]
                self.assertRegex(disposition, r"\(M\d\)|`src/|`infra/|documentation")
                self.assertNotRegex(disposition, r"`(?:mvp|prototype)/")

    def test_cutover_record_names_all_five_epics_with_no_old_path_work(self):
        text = EVIDENCE.read_text(encoding="utf-8")
        row = next(
            line
            for line in text.splitlines()
            if "have no open work on old paths" in line
        )
        for epic in EPICS:
            with self.subTest(epic=epic):
                self.assertIn(epic, row)
        self.assertIn("none changes `mvp/` or `prototype/` paths", row)

    def test_old_roots_hold_no_tracked_files(self):
        for retired in ("mvp", "prototype"):
            with self.subTest(retired=retired):
                self.assertFalse((ROOT / retired).exists())


if __name__ == "__main__":
    unittest.main()
