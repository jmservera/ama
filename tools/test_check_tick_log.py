"""Focused unit tests for tools/check-tick-log.py (Issue #1204)."""

from __future__ import annotations

import importlib.util
import json
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parent / "check-tick-log.py"
SPEC = importlib.util.spec_from_file_location("check_tick_log", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
SPEC.loader.exec_module(checker)


def tick(n: int, **overrides: object) -> dict[str, object]:
    row: dict[str, object] = {
        "tick": n,
        "counts": {"ready": 2, "running": 1, "unassessed": 3},
        "action": "launched review for PR 10",
        "evidence": "tmux list-sessions shows rpi-10",
    }
    row.update(overrides)
    return row


def rules(rows: list[dict[str, object]]) -> list[str]:
    return [v.rule for v in checker.check_ticks(rows)]


class TickLogTests(unittest.TestCase):
    def test_require_extended_rejects_legacy_rows_only_when_asked(self) -> None:
        self.assertEqual(rules([tick(1)]), [])
        strict = checker.check_ticks([tick(1)], require_extended=True)
        self.assertEqual([v.rule for v in strict], ["schema"])
        full = tick(
            1,
            closure_batch=["a"],
            approvals_granted=[],
            approvals_expired=[],
            reclassified=[],
            global_stop=False,
        )
        self.assertEqual(checker.check_ticks([full], require_extended=True), [])

    def test_clean_log_passes(self) -> None:
        self.assertEqual(rules([tick(1), tick(2)]), [])

    def test_malformed_counts_are_flagged_not_coerced_to_zero(self) -> None:
        for bad in (-1, True, "2", 1.5, None):
            counts = {"ready": bad, "running": 1, "unassessed": 0}
            self.assertEqual(rules([tick(1, counts=counts)]), ["count-value"], bad)
        counts = {"ready": -1, "running": 1.0, "unassessed": 0}
        self.assertEqual(rules([tick(1, counts=counts)]), ["count-value", "count-value"])
        self.assertEqual(rules([tick(1, counts={"ready": 0})]), [])
        self.assertEqual(rules([tick(1, counts="x")]), ["schema"])

    def test_missing_action_with_ready_work_is_flagged(self) -> None:
        self.assertEqual(rules([tick(1, action="", evidence="")]), ["no-progress"])

    def test_idle_with_full_capacity_or_no_work_is_allowed(self) -> None:
        idle = {"action": None, "evidence": None}
        full = tick(1, counts={"ready": 2, "running": 8, "unassessed": 0}, **idle)
        empty = tick(2, counts={"ready": 0, "running": 0, "unassessed": 0}, **idle)
        self.assertEqual(rules([full, empty]), [])

    def test_third_tick_after_two_no_progress_needs_recovery(self) -> None:
        idle = {"action": None, "evidence": None}
        full = {"ready": 1, "running": 8, "unassessed": 0}
        rows = [tick(1, counts=full, **idle), tick(2, counts=full, **idle), tick(3, counts=full)]
        self.assertEqual(rules(rows), ["recovery"])
        rows[2]["recovery"] = True
        self.assertEqual(rules(rows), [])

    def test_recovery_claim_needs_action_and_evidence(self) -> None:
        full = {"ready": 1, "running": 8, "unassessed": 0}
        claimed = tick(1, counts=full, action="", evidence="", recovery=True)
        self.assertEqual(rules([claimed]), ["recovery-claim"])
        self.assertEqual(rules([tick(1, counts=full, recovery=True)]), [])

    def test_closure_batch_bound_and_repeat(self) -> None:
        big = tick(1, closure_batch=list("abcdef"))
        again = tick(2, closure_batch=["a"])
        self.assertEqual(rules([big, again]), ["closure-batch", "closure-repeat"])

    def test_expired_approval_requires_scoped_reclassification(self) -> None:
        expired = [{"scope": "cap", "tasks": [5, 6]}]
        partial = [{"task": 5, "to": "human-blocked", "scope": "cap"}]
        self.assertEqual(
            rules([tick(1, approvals_expired=expired, reclassified=partial)]), ["approval"]
        )
        full = partial + [{"task": 6, "to": "human-blocked", "scope": "cap"}]
        self.assertEqual(rules([tick(1, approvals_expired=expired, reclassified=full)]), [])

    def test_unrelated_task_not_blocked_by_expiry(self) -> None:
        expired = [{"scope": "cap", "tasks": [5]}]
        moves = [
            {"task": 5, "to": "human-blocked", "scope": "cap"},
            {"task": 9, "to": "human-blocked", "scope": "cap"},
        ]
        self.assertEqual(
            rules([tick(1, approvals_expired=expired, reclassified=moves)]), ["approval"]
        )

    def test_granted_approval_becomes_ready_same_tick(self) -> None:
        granted = [{"scope": "send", "tasks": [7]}]
        self.assertEqual(rules([tick(1, approvals_granted=granted)]), ["approval"])
        moves = [{"task": 7, "to": "ready", "scope": "send"}]
        self.assertEqual(rules([tick(1, approvals_granted=granted, reclassified=moves)]), [])

    def test_duplicate_tick_number_is_flagged_once(self) -> None:
        self.assertEqual(rules([tick(1), tick(1), tick(2)]), ["duplicate-tick"])

    def test_same_tick_expiry_and_grant_conflict(self) -> None:
        both = [{"scope": "a", "tasks": [5]}]
        moves = [
            {"task": 5, "to": "human-blocked", "scope": "a"},
            {"task": 5, "to": "ready", "scope": "a"},
        ]
        found = rules([tick(1, approvals_expired=both, approvals_granted=both, reclassified=moves)])
        self.assertEqual(sorted(set(found)), ["approval-conflict"])

    def test_ready_after_expiry_without_grant_conflicts(self) -> None:
        expired = [{"scope": "a", "tasks": [5]}]
        moves = [
            {"task": 5, "to": "human-blocked", "scope": "a"},
            {"task": 5, "to": "ready", "scope": "a"},
        ]
        self.assertEqual(
            rules([tick(1, approvals_expired=expired, reclassified=moves)]), ["approval-conflict"]
        )

    def test_expiry_then_later_grant_across_ticks_is_clean(self) -> None:
        expired = [{"scope": "a", "tasks": [5]}]
        granted = [{"scope": "b", "tasks": [5]}]
        rows = [
            tick(
                1,
                approvals_expired=expired,
                reclassified=[{"task": 5, "to": "human-blocked", "scope": "a"}],
            ),
            tick(
                2,
                approvals_granted=granted,
                reclassified=[{"task": 5, "to": "ready", "scope": "b"}],
            ),
        ]
        self.assertEqual(rules(rows), [])

    def test_block_without_expiry_is_flagged_but_expiry_block_is_clean(self) -> None:
        move = {"task": "7", "to": "human-blocked", "scope": "s"}
        self.assertEqual(rules([tick(1, reclassified=[move])]), ["approval"])
        expired = {"scope": "s", "tasks": ["7"]}
        self.assertEqual(rules([tick(1, reclassified=[move], approvals_expired=[expired])]), [])

    def test_duplicate_id_inside_one_closure_batch_is_a_repeat(self) -> None:
        self.assertEqual(rules([tick(1, closure_batch=["a", "a"])]), ["closure-repeat"])

    def test_whitespace_action_is_no_progress_and_idle_stop_is_allowed(self) -> None:
        self.assertEqual(rules([tick(1, action="   ")]), ["no-progress"])
        drained = {"ready": 0, "running": 0, "unassessed": 0, "human_blocked": 4}
        self.assertEqual(rules([tick(1, counts=drained, global_stop=True)]), [])

    def test_global_stop_with_remaining_work_is_flagged(self) -> None:
        self.assertEqual(rules([tick(1, global_stop=True)]), ["global-stop"])

    def test_free_capacity_needs_closure_progress_only_on_extended_rows(self) -> None:
        self.assertEqual(rules([tick(1, closure_batch=[])]), ["closure-progress"])
        self.assertEqual(rules([tick(1, closure_batch=["188"])]), [])
        self.assertEqual(rules([tick(1)]), [])
        full = {"ready": 0, "running": 8, "unassessed": 3}
        self.assertEqual(rules([tick(1, counts=full, closure_batch=[])]), [])

    def test_sqlite_optional_columns_are_checked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "session.db"
            with closing(sqlite3.connect(db_path)) as db:
                db.execute(
                    "CREATE TABLE tick_log (id INTEGER PRIMARY KEY, ready_count INT,"
                    " running_count INT, dep_blocked_count INT, human_blocked_count INT,"
                    " unknown_count INT, action_taken TEXT, evidence TEXT,"
                    " closure_batch TEXT, global_stop INT)"
                )
                db.execute(
                    "INSERT INTO tick_log VALUES (1, 1, 1, 0, 0, 2, 'did work', 'ev', '[]', 1)"
                )
                db.commit()
            rows = checker.load_sqlite(db_path)
            self.assertEqual(rows[0]["closure_batch"], [])
            self.assertIs(rows[0]["global_stop"], True)
            self.assertEqual(sorted(rules(rows)), ["closure-progress", "global-stop"])

    def test_load_rows_rejects_non_object_rows_and_accepts_empty(self) -> None:
        self.assertEqual(checker.load_rows("  \n"), [])
        with self.assertRaises(ValueError):
            checker.load_rows("[1, 2]")
        with self.assertRaises(ValueError):
            checker.load_rows('"text"')

    def test_non_integer_tick_is_a_schema_violation(self) -> None:
        self.assertIn("schema", rules([tick("1")]))
        self.assertIn("schema", rules([tick(True)]))

    def test_session_sqlite_unreadable_inputs_raise_value_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            empty = Path(tmp) / "empty.db"
            with closing(sqlite3.connect(empty)) as db:
                db.execute("CREATE TABLE other (id INTEGER)")
                db.commit()
            with self.assertRaises(ValueError):
                checker.load_sqlite(empty)
            with self.assertRaises(ValueError):
                checker.load_sqlite(Path(tmp) / "absent.db")
            self.assertEqual(checker.main([str(empty)]), 2)

    def test_sqlite_extended_columns_decode_plain_text_and_null(self) -> None:
        self.assertEqual(checker._decode_column("closure_batch", "188"), ["188"])
        self.assertEqual(checker._decode_column("closure_batch", "  "), [])
        self.assertEqual(checker._decode_column("closure_batch", None), [])
        self.assertEqual(checker._decode_column("closure_batch", '["1"]'), ["1"])
        self.assertIs(checker._decode_column("global_stop", 0), False)

    def test_malformed_approval_entries_are_ignored(self) -> None:
        self.assertEqual(rules([tick(1, approvals_granted=["x", 3], reclassified=["y"])]), [])

    def test_ready_move_without_scope_or_grant_is_flagged(self) -> None:
        row = tick(1, reclassified=[{"task": "9", "to": "ready"}])
        self.assertEqual(rules([row]), ["approval"])

    def test_cli_exit_codes_and_json_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "good.jsonl"
            good.write_text("\n".join(json.dumps(tick(n)) for n in (1, 2)), encoding="utf-8")
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps([tick(1, global_stop=True)]), encoding="utf-8")
            self.assertEqual(checker.main([str(good)]), 0)
            self.assertEqual(checker.main([str(bad)]), 1)
            self.assertEqual(checker.main([str(Path(tmp) / "missing.json")]), 2)

    def test_session_sqlite_tick_log(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "session.db"
            with closing(sqlite3.connect(db_path)) as db:
                db.execute(
                    "CREATE TABLE tick_log (id INTEGER PRIMARY KEY, tick_time TEXT,"
                    " ready_count INT, running_count INT, dep_blocked_count INT,"
                    " human_blocked_count INT, unknown_count INT, action_taken TEXT,"
                    " evidence TEXT)"
                )
                db.executemany(
                    "INSERT INTO tick_log VALUES (?, 't', 1, 1, 0, 0, 0, ?, ?)",
                    [(1, "launched session", "tmux ls"), (2, "", "")],
                )
                db.commit()
            rows = checker.load_sqlite(db_path)
            self.assertEqual([r["tick"] for r in rows], [1, 2])
            self.assertEqual(rows[0]["counts"]["ready"], 1)
            self.assertEqual(rules(rows), ["no-progress"])
            self.assertEqual(checker.main([str(db_path)]), 1)
            self.assertEqual(checker.main([str(Path(tmp) / "none.db")]), 2)


if __name__ == "__main__":
    unittest.main()
