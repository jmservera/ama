"""Focused offline tests for tools/backlog-sync.py (Refs #1207). No live gh calls."""

import contextlib
import importlib.util
import io
import sys
import unittest
from pathlib import Path
from unittest import mock

TOOL = Path(__file__).with_name("backlog-sync.py")
spec = importlib.util.spec_from_file_location("backlog_sync", TOOL)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

OPTIONS = {"Todo": "o-todo", "In Progress": "o-prog", "Done": "o-done"}


def issue(n, state="OPEN", body="* [ ] a", title="t"):
    return {"number": n, "state": state, "title": title, "body": body, "url": f"https://x/{n}"}


def pr(n, text):
    return {"number": n, "title": text, "body": "", "headRefName": "b"}


def run(issues, board, open_prs=(), merged=(), argv=(), apply=False):
    """Run main() against mocked gh; return (output, write calls, exit message)."""
    items = [{"id": f"i{n}", "status": s, "content": {"number": n}} for n, s in board.items()]
    writes = []

    def fake_json(*a):
        if a[:2] == ("project", "field-list"):
            return {
                "fields": [
                    {
                        "name": "Status",
                        "id": "f",
                        "options": [{"name": k, "id": v} for k, v in OPTIONS.items()],
                    }
                ]
            }
        if a[:2] == ("project", "view"):
            return {"id": "p"}
        if a[:2] == ("project", "item-list"):
            return {"items": items}
        if a[:2] == ("issue", "list"):
            return list(issues)
        if a[:2] == ("pr", "list"):
            return list(open_prs) if "open" in a else list(merged)
        raise AssertionError(a)

    def fake_gh(*a, data=None):
        writes.append(a)
        return ""

    args = ["backlog-sync.py", *argv] + (["--apply"] if apply else [])
    out, exit_msg = io.StringIO(), None
    with (
        mock.patch.object(mod, "gh_json", fake_json),
        mock.patch.object(mod, "gh", fake_gh),
        mock.patch.object(sys, "argv", args),
        contextlib.redirect_stdout(out),
    ):
        try:
            mod.main()
        except SystemExit as exc:
            exit_msg = str(exc)
    return out.getvalue(), writes, exit_msg


def edited_options(writes):
    return {w[w.index("--id") + 1]: w[-1] for w in writes if w[:2] == ("project", "item-edit")}


class ParseTests(unittest.TestCase):
    def test_parse(self):
        self.assertIsNone(mod.parse_active(None))
        self.assertEqual(mod.parse_active("none"), set())
        self.assertEqual(mod.parse_active("79, #80,82"), {79, 80, 82})

    def test_invalid_entries_rejected(self):
        for raw in ("", "79,", "abc", "0", "-3", "79;80", "1.5"):
            with self.subTest(raw=raw), self.assertRaises(SystemExit):
                mod.parse_active(raw)


class ReconcileTests(unittest.TestCase):
    def test_reproduction_unverified_in_progress_is_not_demoted(self):
        issues = [issue(79), issue(80), issue(82)]
        board = {79: "In Progress", 80: "In Progress", 82: "In Progress"}
        merged = [pr(900, "earlier slice Refs #79 #80 #82")]
        out, writes, msg = run(issues, board, merged=merged, apply=True)
        self.assertIsNone(msg)
        self.assertEqual(writes, [])
        self.assertNotIn("-> Todo", out)
        self.assertIn("activity unverified", out)
        self.assertIn("[79, 80, 82]", out)

    def test_active_set_preserves_in_progress_with_merged_prs_and_no_open_pr(self):
        issues = [issue(79), issue(80), issue(82), issue(90)]
        board = {79: "In Progress", 80: "In Progress", 82: "In Progress", 90: "In Progress"}
        merged = [pr(900, "Refs #79 #80 #82 #90")]
        out, writes, msg = run(
            issues, board, merged=merged, argv=["--active", "79,80,82"], apply=True
        )
        self.assertIsNone(msg)
        self.assertEqual(edited_options(writes), {"i90": "o-todo"})
        self.assertNotIn("#79", out.split("review needed")[0])

    def test_active_promotes_todo_and_done_open_issue(self):
        issues = [issue(5), issue(6)]
        out, writes, _ = run(issues, {5: "Todo", 6: "Done"}, argv=["--active", "5,6"], apply=True)
        self.assertEqual(edited_options(writes), {"i5": "o-prog", "i6": "o-prog"})

    def test_active_audit_proposes_without_writing(self):
        out, writes, _ = run([issue(5)], {5: "Todo"}, argv=["--active", "5"])
        self.assertIn("#5 open: board Todo -> In Progress", out)
        self.assertEqual(writes, [])

    def test_active_none_is_explicit_demotion_evidence(self):
        out, writes, _ = run([issue(5)], {5: "In Progress"}, argv=["--active", "none"], apply=True)
        self.assertEqual(edited_options(writes), {"i5": "o-todo"})

    def test_unsupplied_activity_still_applies_other_rules(self):
        issues = [issue(1), issue(2), issue(3, "CLOSED", "* [ ] a"), issue(4)]
        board = {1: "Done", 2: "Todo", 3: "In Progress", 4: "Todo"}
        out, writes, _ = run(issues, board, open_prs=[pr(50, "fix Refs #2")], apply=True)
        self.assertEqual(edited_options(writes), {"i1": "o-todo", "i2": "o-prog", "i3": "o-done"})
        self.assertTrue(any(w[:2] == ("issue", "edit") for w in writes))

    def test_open_pr_keeps_in_progress_when_activity_supplied(self):
        out, writes, _ = run(
            [issue(7)],
            {7: "In Progress"},
            open_prs=[pr(60, "Refs #7")],
            argv=["--active", "none"],
            apply=True,
        )
        self.assertEqual(writes, [])

    def test_worktree_is_not_activity(self):
        self.assertFalse(hasattr(mod, "live_worktree_issues"))

    def test_invalid_active_issue_stops_before_any_write(self):
        for raw in ("999", "3", "abc"):
            with self.subTest(raw=raw):
                out, writes, msg = run(
                    [issue(5), issue(3, "CLOSED", "* [x] a")],
                    {5: "Todo", 3: "Done"},
                    argv=["--active", raw],
                    apply=True,
                )
                self.assertTrue(msg and "--active" in msg)
                self.assertEqual(writes, [])

    def test_review_needed_list_preserved(self):
        out, _, _ = run(
            [issue(8)], {8: "Todo"}, merged=[pr(70, "Refs #8")], argv=["--active", "none"]
        )
        self.assertIn("review needed (merged PRs reference them, criteria unticked): [8]", out)


if __name__ == "__main__":
    unittest.main()
