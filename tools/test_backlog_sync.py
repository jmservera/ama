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
        if a[:2] == ("project", "item-add"):
            writes.append(a)
            return {"id": "new-" + a[a.index("--url") + 1].rsplit("/", 1)[1]}
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
        self.assertEqual(mod.parse_issues("79, #80,82", "--active"), {79, 80, 82})

    def test_invalid_entries_rejected_without_echo(self):
        for raw in ("", "79,", "abc", "0", "-3", "79;80", "1.5", "none", "secret-token"):
            with self.subTest(raw=raw), self.assertRaises(SystemExit) as ctx:
                mod.parse_issues(raw, "--inactive")
            message = str(ctx.exception)
            self.assertIn("--inactive", message)
            self.assertIn("expected", message)
            if raw:
                self.assertNotIn(raw, message)


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

    def test_active_subset_never_demotes_unlisted_issues(self):
        issues = [issue(79), issue(80), issue(82), issue(90)]
        board = {79: "In Progress", 80: "In Progress", 82: "In Progress", 90: "In Progress"}
        merged = [pr(900, "Refs #79 #80 #82 #90")]
        out, writes, msg = run(
            issues, board, merged=merged, argv=["--active", "79,80,82"], apply=True
        )
        self.assertIsNone(msg)
        self.assertEqual(writes, [])
        self.assertIn(
            "activity unverified (kept In Progress: no open PR and no --active or "
            "--inactive evidence): [90]",
            out,
        )

    def test_explicit_inactive_demotes_only_named_issue(self):
        issues = [issue(79), issue(90), issue(91)]
        board = {79: "In Progress", 90: "In Progress", 91: "In Progress"}
        out, writes, msg = run(
            issues, board, argv=["--active", "79", "--inactive", "90"], apply=True
        )
        self.assertIsNone(msg)
        self.assertEqual(edited_options(writes), {"i90": "o-todo"})
        self.assertIn("[91]", out)

    def test_active_promotes_todo_and_done_open_issue(self):
        issues = [issue(5), issue(6)]
        out, writes, _ = run(issues, {5: "Todo", 6: "Done"}, argv=["--active", "5,6"], apply=True)
        self.assertEqual(edited_options(writes), {"i5": "o-prog", "i6": "o-prog"})

    def test_active_audit_proposes_without_writing(self):
        out, writes, _ = run([issue(5)], {5: "Todo"}, argv=["--active", "5"])
        self.assertIn("#5 open: board Todo -> In Progress", out)
        self.assertEqual(writes, [])

    def test_unsupplied_activity_still_applies_other_rules(self):
        issues = [issue(1), issue(2), issue(3, "CLOSED", "* [ ] a"), issue(4)]
        board = {1: "Done", 2: "Todo", 3: "In Progress", 4: "Todo"}
        out, writes, _ = run(issues, board, open_prs=[pr(50, "fix Refs #2")], apply=True)
        self.assertEqual(edited_options(writes), {"i1": "o-todo", "i2": "o-prog", "i3": "o-done"})
        self.assertTrue(any(w[:2] == ("issue", "edit") for w in writes))

    def test_inactive_conflicting_with_open_pr_is_reported_not_written(self):
        for start in ("Todo", "In Progress"):
            with self.subTest(start=start):
                out, writes, msg = run(
                    [issue(7)],
                    {7: start},
                    open_prs=[pr(60, "Refs #7")],
                    argv=["--inactive", "7"],
                    apply=True,
                )
                self.assertIsNone(msg)
                self.assertEqual(writes, [])
                self.assertIn(
                    f"#7 conflict: --inactive contradicts open PR(s) [60]; status {start} left unchanged",
                    out,
                )
                self.assertNotIn("->", out)

    def test_observed_parent_stack_mention_does_not_promote_inactive_issue(self):
        parent = {
            "number": 1239,
            "title": "feat(ranking): publication runner (#79)",
            "body": "Parent of the #1231 and #80 stacks.",
            "headRefName": "feat/ranking-publication-runner-79",
        }
        numbers = (79, 80, 81, 86, 107, 108, 1231)
        board = dict.fromkeys(numbers, "In Progress") | {80: "Todo", 108: "Todo"}
        out, writes, msg = run(
            [issue(n) for n in numbers],
            board,
            open_prs=[parent],
            argv=["--active", "79,81,86,1231,107", "--inactive", "80,108"],
            apply=True,
        )
        self.assertIsNone(msg)
        self.assertEqual(writes, [])
        self.assertIn("#80 conflict: --inactive contradicts open PR(s) [1239]", out)
        self.assertNotIn("In Progress", out.replace("left unchanged", ""))

    def test_active_with_open_pr_stays_protected(self):
        _, writes, _ = run(
            [issue(7)], {7: "Todo"}, open_prs=[pr(60, "Refs #7")], argv=["--active", "7"], apply=True
        )
        self.assertEqual(edited_options(writes), {"i7": "o-prog"})

    def test_conflict_does_not_block_other_writes_or_add_missing_item(self):
        issues = [issue(7), issue(8), issue(9), issue(3, "CLOSED", "* [ ] a")]
        out, writes, msg = run(
            issues,
            {7: "In Progress", 8: "In Progress", 3: "In Progress"},
            open_prs=[pr(60, "Refs #7 #9")],
            argv=["--inactive", "7,8,9"],
            apply=True,
        )
        self.assertIsNone(msg)
        self.assertEqual(edited_options(writes), {"i8": "o-todo", "i3": "o-done"})
        self.assertIn("#9 conflict: --inactive contradicts open PR(s) [60]; status missing left unchanged", out)
        self.assertFalse(any(w[:2] == ("project", "item-add") for w in writes))
        self.assertTrue(any(w[:2] == ("issue", "edit") for w in writes))

    def test_missing_unreferenced_item_is_still_added(self):
        _, writes, _ = run([issue(9)], {}, argv=["--inactive", "9"], apply=True)
        self.assertTrue(any(w[:2] == ("project", "item-add") for w in writes))
        self.assertEqual(edited_options(writes), {"new-9": "o-todo"})

    def test_conflict_audit_writes_nothing(self):
        out, writes, _ = run(
            [issue(7)], {7: "Todo"}, open_prs=[pr(60, "Refs #7")], argv=["--inactive", "7"]
        )
        self.assertIn("#7 conflict", out)
        self.assertEqual(writes, [])

    def test_inactive_with_merged_reference_only_is_not_a_conflict(self):
        out, writes, _ = run(
            [issue(7)], {7: "In Progress"}, merged=[pr(70, "Refs #7")], argv=["--inactive", "7"], apply=True
        )
        self.assertEqual(edited_options(writes), {"i7": "o-todo"})
        self.assertNotIn("conflict", out)
        self.assertIn("review needed (merged PRs reference them, criteria unticked): [7]", out)

    def test_invalid_evidence_stops_before_any_write(self):
        cases = (
            ["--active", "999"],
            ["--active", "3"],
            ["--inactive", "3"],
            ["--active", "abc"],
            ["--inactive", "5", "--active", "5"],
        )
        for argv in cases:
            with self.subTest(argv=argv):
                out, writes, msg = run(
                    [issue(5), issue(3, "CLOSED", "* [x] a")],
                    {5: "Todo", 3: "Done"},
                    argv=argv,
                    apply=True,
                )
                self.assertTrue(msg and msg.startswith("--") or msg.startswith("invalid"))
                self.assertEqual(writes, [])

    def test_review_needed_list_preserved(self):
        out, _, _ = run([issue(8)], {8: "Todo"}, merged=[pr(70, "Refs #8")], argv=["--active", "8"])
        self.assertIn("review needed (merged PRs reference them, criteria unticked): [8]", out)


if __name__ == "__main__":
    unittest.main()
