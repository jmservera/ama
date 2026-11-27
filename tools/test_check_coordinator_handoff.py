"""Focused unit tests for tools/check-coordinator-handoff.py (Issue #1204)."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
SCRIPT_PATH = TOOLS_DIR / "check-coordinator-handoff.py"
# Catastrophic backtracking takes far longer; the margin keeps loaded hosts from failing.
LINEAR_TIME_BUDGET_S = 2.0

SPEC = importlib.util.spec_from_file_location("check_coordinator_handoff", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
SPEC.loader.exec_module(checker)


def _valid_handoff_markdown(
    *,
    observed_utc: str = "2026-11-15T12:00:00Z",
    written_utc: str = "2026-11-15T12:03:00Z",
    live_commands: str = (
        "`gh issue list --state open --limit 500`, "
        "`gh pr list --state open --limit 200`, "
        "`tmux list-sessions`, `git rev-parse HEAD origin/main`"
    ),
    open_issues: str = "3",
    open_prs: str = "2",
    active_sessions: str = "1/8 (`rpi-1204`)",
    head_sha: str = "f74e1bf1fd7d3e62048a69ade51a126704ebc556",
    origin_main_sha: str = "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678",
    base_sha: str = "f74e1bf1fd7d3e62048a69ade51a126704ebc556",
    table_rows: str = (
        "| #1200 | merged | PR #1630 | Closed on main |\n"
        "| #1204 | active session | PR #1641 | Monitor `rpi-1204` |\n"
        "| #1288 | human-blocked | "
        "https://github.com/jmservera/ama/issues/1288#issuecomment-10 | Await owner |\n"
        "| #1302 | dependency-blocked | PR #1641 | Start after parent merges |"
    ),
    summary_prose: str = (
        "What changed since last check: launched `rpi-1204`.\n"
        "What is waiting and why: #1288 awaits owner decision; #1302 awaits parent PR #1641."
    ),
) -> str:
    return (
        "# Coordinator Scheduled Check Status\n\n"
        f"* Observed UTC: {observed_utc}\n"
        f"* Written UTC: {written_utc}\n"
        f"* Live commands: {live_commands}\n"
        f"* Open issues: {open_issues}\n"
        f"* Open PRs: {open_prs}\n"
        f"* Active sessions: {active_sessions}\n"
        f"* HEAD SHA: {head_sha}\n"
        f"* Origin/main SHA: {origin_main_sha}\n"
        f"* Target/base SHA: {base_sha}\n\n"
        "| Issue | State | Blocker or evidence link | Next action |\n"
        "| --- | --- | --- | --- |\n"
        f"{table_rows}\n\n"
        f"{summary_prose}\n"
    )


class CoordinatorHandoffGuardTests(unittest.TestCase):
    def test_live_coordinator_agent_instructions_pass(self) -> None:
        agent_path = REPO_ROOT / checker.AGENT_RELATIVE_PATH
        violations = checker.check_agent_instructions(agent_path, root=REPO_ROOT)
        self.assertEqual(violations, [])

    def test_agent_instruction_guard_rejects_missing_contracts(self) -> None:
        baseline = (REPO_ROOT / checker.AGENT_RELATIVE_PATH).read_text(encoding="utf-8")
        mutations = (
            (
                "missing-frontmatter",
                baseline.replace("---\n", "", 1),
                "invalid-frontmatter",
            ),
            (
                "missing-ready-to-start-category",
                baseline.replace("ready to start", "actionable-later"),
                "missing-classification-category",
            ),
            (
                "missing-unverified-blocker-guard",
                baseline.replace("unverified blocker", "unconfirmed note"),
                "missing-unverified-blocker-guard",
            ),
            (
                "missing-tmux-live-command",
                baseline.replace("tmux list-sessions", "ps aux"),
                "missing-live-refresh-rule",
            ),
            (
                "missing-expect-open-issues-flag",
                baseline.replace("--expect-open-issues", "--legacy-open-count"),
                "missing-live-refresh-rule",
            ),
            (
                "missing-active-sessions-flag",
                baseline.replace("--active-sessions", "--legacy-session-names"),
                "missing-live-refresh-rule",
            ),
            (
                "missing-gh-api-paginate-saturation-rule",
                baseline.replace("gh api --paginate", "gh api --raw-field"),
                "missing-live-refresh-rule",
            ),
            (
                "missing-closure-batch-bound",
                baseline.replace("up to five", "all"),
                "missing-tick-liveness-rule",
            ),
            (
                "missing-closure-review-record",
                baseline.replace("`closure_review`", "`notes`"),
                "missing-tick-liveness-rule",
            ),
            (
                "missing-tick-log-record",
                baseline.replace("`tick_log`", "`ticks`"),
                "missing-tick-liveness-rule",
            ),
            (
                "missing-approved-actions-record",
                baseline.replace("`approved_actions`", "`approvals`"),
                "missing-tick-liveness-rule",
            ),
            (
                "missing-expired-approval-reconciliation",
                baseline.replace("expired approval", "old note"),
                "missing-tick-liveness-rule",
            ),
            (
                "missing-no-global-stop-clause",
                baseline.replace("never a success claim or a global stop", "a global stop"),
                "missing-tick-liveness-rule",
            ),
            (
                "inverted-global-idle-polarity",
                baseline.replace(
                    'never claim "nothing changed"', 'always claim "nothing changed"'
                ).replace('Never claim "nothing changed"', 'Always claim "nothing changed"'),
                "inverted-guard-polarity",
            ),
            (
                "inverted-single-section-idle-polarity",
                baseline.replace(
                    'Never claim "nothing changed"',
                    'Always claim "nothing changed"',
                    1,
                ),
                "inverted-guard-polarity",
            ),
            (
                "inverted-unverified-blocker-polarity",
                baseline + "\nScheduled checks may pause on an unverified blocker.\n",
                "inverted-guard-polarity",
            ),
            (
                "coordinated-conjunction-polarity-bypass-idle",
                baseline.replace(
                    'Never claim "nothing changed"',
                    'Never skip verification and always claim "nothing changed"',
                    1,
                ),
                "inverted-guard-polarity",
            ),
            (
                "coordinated-conjunction-polarity-bypass-unverified-blocker",
                baseline + "\nNever skip verification and pause on an unverified blocker.\n",
                "inverted-guard-polarity",
            ),
            (
                "broken-relative-link",
                baseline + "\nSee [missing doc](../../docs/does-not-exist-1204.md).\n",
                "broken-link",
            ),
        )
        with tempfile.TemporaryDirectory() as tmp:
            agent_dir = Path(tmp) / ".github" / "agents"
            agent_dir.mkdir(parents=True)
            for label, mutated_text, expected_rule in mutations:
                with self.subTest(case=label):
                    candidate = agent_dir / "ama-backlog-delivery-coordinator.agent.md"
                    candidate.write_text(mutated_text, encoding="utf-8")
                    violations = checker.check_agent_instructions(candidate, root=Path(tmp))
                    joined = "\n".join(violations)
                    self.assertIn(expected_rule, joined)

    def test_valid_active_and_multi_role_stacked_handoffs_pass(self) -> None:
        with self.subTest(case="multi-role-active-stacked-handoff"):
            doc = _valid_handoff_markdown(
                open_issues="2",
                active_sessions="2/8 (`rpi-1204-impl`, `rpi-1204-rev`)",
                table_rows=(
                    "| #1204 | active session | PR #1641 | Impl + review workers running |\n"
                    "| #1302 | dependency-blocked | PR #1641 | Stacked child merged into parent |"
                ),
                summary_prose="Active delivery continues across two tmux workers for #1204.",
            )
            self.assertEqual(checker.check_handoff_text("handoff.md", doc), [])

        with self.subTest(case="markdown-linked-issue-ids-and-concurrent-launch-lane-wait"):
            doc = _valid_handoff_markdown(
                open_issues="3",
                open_prs="2",
                active_sessions="1/8 (`rpi-1204`)",
                table_rows=(
                    "| [#1204](https://github.com/jmservera/ama/issues/1204) | active session | "
                    "PR #1641 | Impl worker running |\n"
                    "| [#1288](https://github.com/jmservera/ama/issues/1288) | "
                    "dependency-blocked | PR #1642 | Await hosted CI |\n"
                    "| [#1310](https://github.com/jmservera/ama/issues/1310) | ready to start | "
                    "none | Launch next |"
                ),
                summary_prose=(
                    "Launched rpi-1204; waiting for hosted CI on PR #1642 while starting #1310 "
                    "next."
                ),
            )
            self.assertEqual(
                checker.check_handoff_text("linked-active.md", doc, open_issues={1204, 1288, 1310}),
                [],
            )

        with self.subTest(case="multi-section-dated-checkpoint-pack"):
            sec_one = (
                "## Checkpoint 2026-11-14 Wave 1\n\n"
                "* Observed UTC: 2026-11-14T10:00:00Z\n"
                "* Written UTC: 2026-11-14T10:05:00Z\n"
                "* Live commands: `gh issue list --state open --limit 500`, "
                "`gh pr list --state open --limit 200`, "
                "`tmux list-sessions`, `git rev-parse HEAD`\n"
                "* Open issues: 1\n"
                "* Open PRs: 1\n"
                "* Active sessions: 1/8 (`rpi-1190`)\n"
                "* HEAD SHA: 1111111222222233333334444444555555566666\n\n"
                "| Issue | State | Blocker or evidence link | Next action |\n"
                "| --- | --- | --- | --- |\n"
                "| #1190 | active session | PR #1601 | Continue wave 1 |\n\n"
            )
            sec_two = (
                "## Checkpoint 2026-11-15 Wave 2\n\n"
                "* Observed UTC: 2026-11-15T12:00:00Z\n"
                "* Written UTC: 2026-11-15T12:04:00Z\n"
                "* Live commands: `gh issue list --state open --limit 500`, "
                "`gh pr list --state open --limit 200`, "
                "`tmux list-sessions`, `git rev-parse HEAD`\n"
                "* Open issues: 1\n"
                "* Open PRs: 1\n"
                "* Active sessions: 0/8\n"
                "* HEAD SHA: f74e1bf1fd7d3e62048a69ade51a126704ebc556\n\n"
                "| Issue | State | Blocker or evidence link | Next action |\n"
                "| --- | --- | --- | --- |\n"
                "| #1204 | dependency-blocked | https://github.com/jmservera/ama/pull/1641/checks "
                "| Await hosted CI auto-merge |\n"
            )
            violations = checker.check_handoff_text(
                "checkpoints.md",
                sec_one + sec_two,
                expect_head="f74e1bf1fd",
                expect_open_issues=1,
                active_sessions=set(),
            )
            self.assertEqual(violations, [])

    def test_valid_waiting_and_idle_summaries_pass_when_all_open_issues_classified(self) -> None:
        with self.subTest(case="hosted-ci-and-human-blocked-nothing-changed"):
            doc = _valid_handoff_markdown(
                open_issues="2",
                open_prs="1",
                active_sessions="0/8",
                table_rows=(
                    "| #1200 | merged | PR #1630 | Closed on main |\n"
                    "| #1204 | dependency-blocked | "
                    "https://github.com/jmservera/ama/pull/1641/checks | Await hosted CI |\n"
                    "| #1288 | human-blocked | #1288#issuecomment-42 | Await owner approval |"
                ),
                summary_prose=(
                    "Nothing changed since the last check; waiting on hosted CI for PR #1641 "
                    "and owner approval on #1288."
                ),
            )
            self.assertEqual(
                checker.check_handoff_text("idle-ok.md", doc, open_issues={1204, 1288}),
                [],
            )
            bare_pr_wait_doc = _valid_handoff_markdown(
                open_issues="2",
                open_prs="1",
                active_sessions="0/8",
                table_rows=(
                    "| #1204 | dependency-blocked | "
                    "https://github.com/jmservera/ama/pull/1641/checks | Await hosted CI |\n"
                    "| #1288 | human-blocked | #1288#issuecomment-42 | Await owner approval |"
                ),
                summary_prose="Waiting on #1641 and waiting on PR #1641 checks.",
            )
            self.assertEqual(
                checker.check_handoff_text(
                    "bare-pr-wait-ok.md", bare_pr_wait_doc, open_issues={1204, 1288}
                ),
                [],
            )

        with self.subTest(case="waiting-at-declared-session-cap-with-ready-queue"):
            doc = _valid_handoff_markdown(
                open_issues="2",
                open_prs="1",
                active_sessions="2/2 (`rpi-1204-a`, `rpi-1204-b`)",
                table_rows=(
                    "| #1204 | active session | PR #1641 | Running at 2/2 cap |\n"
                    "| #1310 | ready to start | none | Queued for next free slot |"
                ),
                summary_prose="Status: waiting on active session slot before launching #1310.",
            )
            self.assertEqual(checker.check_handoff_text("cap-wait.md", doc), [])

        with self.subTest(case="waiting-during-active-pr-drain-hysteresis"):
            doc = _valid_handoff_markdown(
                open_issues="1",
                open_prs="18 (draining until <= 15)",
                active_sessions="0/8",
                table_rows=("| #1310 | ready to start | none | Held during PR drain |"),
                summary_prose="Status: waiting on PR drain below 15 before starting new work.",
            )
            self.assertEqual(checker.check_handoff_text("drain-wait.md", doc), [])

            for drain_launch_prose in (
                "Waiting on PR #1641, and #1310 is starting now.",
                "Waiting on https://github.com/jmservera/ama/pull/1641; #1310 is starting now.",
            ):
                drain_launch_doc = _valid_handoff_markdown(
                    open_issues="2",
                    open_prs="18 (draining until <= 15)",
                    active_sessions="1/8 (`rpi-1204`)",
                    table_rows=(
                        "| #1204 | active session | PR #1641 | Running |\n"
                        "| #1310 | ready to start | none | Starting concurrently |"
                    ),
                    summary_prose=drain_launch_prose,
                )
                self.assertEqual(
                    checker.check_handoff_text("drain-launch.md", drain_launch_doc),
                    [],
                    msg=drain_launch_prose,
                )

        with self.subTest(case="below-capacity-coordinated-and-subject-first-launches"):
            for valid_concurrent_prose in (
                "Waiting on PR #1641 without force-pushing, and starting #1310 now.",
                "Waiting on PR #1641, and #1310 is starting now.",
            ):
                concurrent_doc = _valid_handoff_markdown(
                    open_issues="2",
                    open_prs="1",
                    active_sessions="1/8 (`rpi-1204`)",
                    table_rows=(
                        "| #1204 | active session | PR #1641 | Running |\n"
                        "| #1310 | ready to start | none | Starting concurrently |"
                    ),
                    summary_prose=valid_concurrent_prose,
                )
                self.assertEqual(
                    checker.check_handoff_text("concurrent-and.md", concurrent_doc),
                    [],
                    msg=valid_concurrent_prose,
                )

        with self.subTest(case="rv8-capacity-and-drain-next-check-timing-and-shared-lifecycle"):
            for cap_prose, cap_sessions in (
                (
                    "Waiting for a free worker session slot until the next check.",
                    "1/1 (`rpi-1204`)",
                ),
                (
                    "Waiting for a free slot until the next check.",
                    "2/2 (`rpi-1204-a`, `rpi-1204-b`)",
                ),
            ):
                cap_next_check_doc = _valid_handoff_markdown(
                    open_issues="2",
                    open_prs="1",
                    active_sessions=cap_sessions,
                    table_rows=(
                        "| #1204 | active session | PR #1641 | Running at cap |\n"
                        "| #1310 | ready to start | none | Queued for next free slot |"
                    ),
                    summary_prose=cap_prose,
                )
                self.assertEqual(
                    checker.check_handoff_text("cap-next-check.md", cap_next_check_doc),
                    [],
                    msg=cap_prose,
                )

            for drain_prose in (
                "Waiting on PR drain below 15 until the next scheduled check.",
                "Waiting for open PRs to drain below 10 until the next scheduled check.",
            ):
                drain_next_check_doc = _valid_handoff_markdown(
                    open_issues="2",
                    open_prs="18 (PR drain active)",
                    active_sessions="1/8 (`rpi-1204`)",
                    table_rows=(
                        "| #1204 | active session | PR #1641 | Running |\n"
                        "| #1310 | ready to start | none | Held under PR drain |"
                    ),
                    summary_prose=drain_prose,
                )
                self.assertEqual(
                    checker.check_handoff_text("drain-next-check.md", drain_next_check_doc),
                    [],
                    msg=drain_prose,
                )

            backtick_session_launch_doc = _valid_handoff_markdown(
                open_issues="2",
                open_prs="1",
                active_sessions="1/8 (`rpi-1204`)",
                table_rows=(
                    "| #1204 | active session | PR #1641 | Running |\n"
                    "| #1310 | ready to start | none | Starting `rpi-1310-no-push` |"
                ),
                summary_prose="Waiting on PR #1641 while starting `rpi-1310-no-push` now.",
            )
            self.assertEqual(
                checker.check_handoff_text("backtick-no-push.md", backtick_session_launch_doc),
                [],
            )

            for shared_lifecycle_prose in (
                "Waiting on PR #1641 CI and status checks.",
                "Waiting on PR #1641 and its hosted CI.",
                "Waiting on CI and status checks on PR #1641.",
                "Waiting on [CI and checks](https://github.com/jmservera/ama/pull/1641).",
                "Paused and waiting on PR #1641.",
            ):
                shared_doc = _valid_handoff_markdown(
                    open_issues="1",
                    open_prs="1",
                    active_sessions="1/8 (`rpi-1204`)",
                    table_rows="| #1204 | active session | PR #1641 | Running |",
                    summary_prose=shared_lifecycle_prose,
                )
                self.assertEqual(
                    checker.check_handoff_text("shared-lifecycle.md", shared_doc),
                    [],
                    msg=shared_lifecycle_prose,
                )

    def test_classification_table_rejects_invalid_states_duplicates_and_self_only_links(
        self,
    ) -> None:
        cases = (
            (
                "unknown-category",
                (
                    "| #1204 | unknown | investigating | inspect |\n"
                    "| #1288 | active session | PR #1641 | run |\n"
                    "| #1302 | ready to start | none | launch |"
                ),
                "invalid-classification-category",
            ),
            (
                "duplicate-issue-row",
                (
                    "| #1204 | active session | PR #1641 | run |\n"
                    "| #1204 | ready to start | none | duplicate |\n"
                    "| #1302 | ready to start | none | launch |"
                ),
                "duplicate-issue-row",
            ),
            (
                "human-blocked-missing-link",
                (
                    "| #1204 | active session | PR #1641 | run |\n"
                    "| #1288 | human-blocked | awaiting owner reply | ask |\n"
                    "| #1302 | dependency-blocked | PR #1641 | wait |"
                ),
                "missing-blocker-link",
            ),
            (
                "human-blocked-bare-self-issue-bypass",
                (
                    "| #1204 | active session | PR #1641 | run |\n"
                    "| #1288 | human-blocked | Blocked on owner in #1288 | ask |\n"
                    "| #1302 | dependency-blocked | PR #1641 | wait |"
                ),
                "missing-blocker-link",
            ),
            (
                "human-blocked-markdown-self-anchor-bypass",
                (
                    "| #1204 | active session | PR #1641 | run |\n"
                    "| #1288 | human-blocked | [self](#1288) | ask |\n"
                    "| #1302 | dependency-blocked | PR #1641 | wait |"
                ),
                "missing-blocker-link",
            ),
            (
                "dependency-blocked-bare-self-issue-bypass",
                (
                    "| #1204 | active session | PR #1641 | run |\n"
                    "| #1288 | human-blocked | https://example.com/gate | ask |\n"
                    "| #1302 | dependency-blocked | waiting on #1302 | wait |"
                ),
                "missing-blocker-link",
            ),
            (
                "markdown-linked-issue-id-url-mismatch",
                (
                    "| [#1288](https://github.com/jmservera/ama/issues/9999) | active session | "
                    "PR #1641 | run |\n"
                    "| #1204 | active session | PR #1641 | run |\n"
                    "| #1302 | dependency-blocked | PR #1641 | wait |"
                ),
                "invalid-issue-id",
            ),
            (
                "multi-issue-cell-rejected",
                (
                    "| #1204, #1205 | active session | PR #1641 | run |\n"
                    "| #1288 | human-blocked | https://example.com/gate | ask |\n"
                    "| #1302 | dependency-blocked | PR #1641 | wait |"
                ),
                "invalid-issue-id",
            ),
            (
                "markdown-linked-issue-id-bare-self-still-needs-blocker-link",
                (
                    "| #1204 | active session | PR #1641 | run |\n"
                    "| [#1288](https://github.com/jmservera/ama/issues/1288) | human-blocked | "
                    "Blocked in #1288 | ask |\n"
                    "| #1302 | dependency-blocked | PR #1641 | wait |"
                ),
                "missing-blocker-link",
            ),
            (
                "mismatched-blocker-markdown-link-label",
                (
                    "| #1204 | active session | PR #1641 | run |\n"
                    "| #1288 | human-blocked | https://example.com/gate | ask |\n"
                    "| #1302 | dependency-blocked | "
                    "[PR #999](https://github.com/jmservera/ama/pull/1641) | wait |"
                ),
                "mismatched-blocker-link",
            ),
            (
                "bare-self-github-issue-url-without-fragment",
                (
                    "| #1204 | active session | PR #1641 | run |\n"
                    "| #1288 | human-blocked | https://github.com/jmservera/ama/issues/1288 | ask |\n"
                    "| #1302 | dependency-blocked | PR #1641 | wait |"
                ),
                "missing-blocker-link",
            ),
            (
                "bare-self-markdown-issue-urls-and-self-fragment",
                (
                    "| #1204 | active session | PR #1641 | run |\n"
                    "| #1288 | human-blocked | "
                    "[#1288](https://github.com/jmservera/ama/issues/1288#1288) | ask |\n"
                    "| #1302 | dependency-blocked | [self](./issues/1302) | wait |"
                ),
                "missing-blocker-link",
            ),
        )
        for label, rows, expected_rule in cases:
            with self.subTest(case=label):
                doc = _valid_handoff_markdown(
                    open_issues="3",
                    table_rows=rows,
                    summary_prose="Active wave check completed.",
                )
                violations = checker.check_handoff_text("bad-table.md", doc)
                self.assertIn(expected_rule, "\n".join(violations))

    def test_idle_and_waiting_summaries_rejected_when_missing_or_after_table_or_unclassified(
        self,
    ) -> None:
        with self.subTest(case="nothing-changed-without-table"):
            doc = (
                "# Check\n\n"
                "* Live commands: `gh issue list --state open --limit 500`, "
                "`gh pr list --state open --limit 200`, "
                "`tmux list-sessions`, `git rev-parse HEAD`\n"
                "* Open issues: 2\n"
                "* Open PRs: 0\n"
                "* Active sessions: 0/8\n"
                "* HEAD SHA: f74e1bf1fd7d3e62048a69ade51a126704ebc556\n\n"
                "Nothing changed since last check.\n"
            )
            violations = checker.check_handoff_text("no-table.md", doc)
            self.assertIn("missing-classification-table", "\n".join(violations))

            blocked_no_table_doc = doc.replace(
                "Nothing changed since last check.\n",
                "Blocked on stakeholder approval.\n",
            )
            blocked_no_table_joined = "\n".join(
                checker.check_handoff_text("blocked-no-table.md", blocked_no_table_doc)
            )
            self.assertIn("unverified-blocker-pause", blocked_no_table_joined)
            self.assertIn("missing-classification-table", blocked_no_table_joined)

        with self.subTest(case="summary-before-classification-table"):
            doc = (
                "# Check\n\n"
                "* Live commands: `gh issue list --state open --limit 500`, "
                "`gh pr list --state open --limit 200`, "
                "`tmux list-sessions`, `git rev-parse HEAD`\n"
                "* Open issues: 1\n"
                "* Open PRs: 0\n"
                "* Active sessions: 0/8\n"
                "* HEAD SHA: f74e1bf1fd7d3e62048a69ade51a126704ebc556\n\n"
                "Nothing changed since the last check.\n\n"
                "| Issue | State | Blocker or evidence link | Next action |\n"
                "| --- | --- | --- | --- |\n"
                "| #1288 | human-blocked | https://example.com/1288 | Wait |\n"
            )
            violations = checker.check_handoff_text("late-table.md", doc)
            self.assertIn("summary-before-classification-table", "\n".join(violations))

        with self.subTest(case="open-issue-count-exceeds-classified-rows"):
            doc = _valid_handoff_markdown(
                open_issues="4",
                active_sessions="0/8",
                table_rows=(
                    "| #1288 | human-blocked | https://example.com/1288 | Wait |\n"
                    "| #1302 | dependency-blocked | PR #1641 | Wait |"
                ),
                summary_prose="Idle tick: nothing changed.",
            )
            joined = "\n".join(checker.check_handoff_text("unclassified-gap.md", doc))
            self.assertIn("unclassified-open-issues", joined)
            self.assertIn("unsupported-idle-unclassified", joined)

        with self.subTest(case="open-issue-wrongly-marked-merged"):
            doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="0/8",
                table_rows=(
                    "| #1302 | merged | PR #1641 | Merged into parent branch only |\n"
                    "| #1288 | human-blocked | https://example.com/1288 | Wait |"
                ),
                summary_prose="Nothing changed this tick.",
            )
            joined = "\n".join(
                checker.check_handoff_text("open-merged.md", doc, open_issues={1288, 1302})
            )
            self.assertIn("open-issue-marked-merged", joined)
            self.assertIn("unsupported-idle-unclassified", joined)

        with self.subTest(
            case="rv8-tableless-waiting-pause-emits-missing-table-and-unverified-pause"
        ):
            tableless_wait_doc = (
                "# Coordinator Scheduled Check Status\n\n"
                "* Observed UTC: 2026-11-15T12:00:00Z\n"
                "* Written UTC: 2026-11-15T12:03:00Z\n"
                "* Live commands: `gh issue list --state open --limit 500`, "
                "`gh pr list --state open --limit 200`, "
                "`tmux list-sessions`, `git rev-parse HEAD origin/main`\n"
                "* Open issues: 1\n"
                "* Open PRs: 1\n"
                "* Active sessions: 0/8\n"
                "* HEAD SHA: f74e1bf1fd7d3e62048a69ade51a126704ebc556\n"
                "* Origin/main SHA: a1b2c3d4e5f60718293a4b5c6d7e8f9012345678\n"
                "* Target/base SHA: f74e1bf1fd7d3e62048a69ade51a126704ebc556\n\n"
                "Status: waiting — blocked on stakeholder review.\n"
            )
            tableless_joined = "\n".join(
                checker.check_handoff_text("tableless-wait.md", tableless_wait_doc)
            )
            self.assertIn("missing-classification-table", tableless_joined)
            self.assertIn("unverified-blocker-pause", tableless_joined)

    def test_idle_and_waiting_summaries_rejected_for_ready_work_or_unverified_blockers(
        self,
    ) -> None:
        with self.subTest(case="nothing-changed-with-ready-to-start-issue"):
            doc = _valid_handoff_markdown(
                open_issues="2",
                active_sessions="2/2 (`rpi-1204-a`, `rpi-1204-b`)",
                table_rows=(
                    "| #1204 | active session | PR #1641 | Running |\n"
                    "| #1310 | ready to start | none | Launch next |"
                ),
                summary_prose="Nothing changed since last check.",
            )
            joined = "\n".join(checker.check_handoff_text("idle-ready.md", doc))
            self.assertIn("unsupported-idle-ready-work", joined)

        with self.subTest(case="waiting-below-capacity-with-ready-to-start-issue"):
            doc = _valid_handoff_markdown(
                open_issues="2",
                open_prs="2",
                active_sessions="1/8 (`rpi-1204`)",
                table_rows=(
                    "| #1204 | active session | PR #1641 | Running |\n"
                    "| #1310 | ready to start | none | Should launch now |"
                ),
                summary_prose="Status: waiting on human input before continuing.",
            )
            joined = "\n".join(checker.check_handoff_text("wait-ready.md", doc))
            self.assertIn("unsupported-waiting-ready-work", joined)

        with self.subTest(case="pause-on-unverified-blocker-phrase"):
            doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="0/8",
                table_rows="| #1288 | human-blocked | https://example.com/1288 | Wait |",
                summary_prose="Pausing schedule due to an unverified blocker in infra.",
            )
            joined = "\n".join(checker.check_handoff_text("unverified-phrase.md", doc))
            self.assertIn("unverified-blocker-pause", joined)

        with self.subTest(case="pause-citing-ready-issue-as-blocker"):
            doc = _valid_handoff_markdown(
                open_issues="2",
                active_sessions="2/2 (`rpi-1204-a`, `rpi-1204-b`)",
                table_rows=(
                    "| #1204 | active session | PR #1641 | Running |\n"
                    "| #1310 | ready to start | none | Eligible |"
                ),
                summary_prose="Paused on #1310 while waiting on upstream.",
            )
            joined = "\n".join(checker.check_handoff_text("cite-ready-blocker.md", doc))
            self.assertIn("unverified-blocker-reference", joined)

        with self.subTest(case="uncited-non-capacity-waiting-and-generic-url-blockers"):
            for uncited_prose in (
                "Paused the run for stakeholder approval.",
                "Waiting for stakeholder feedback.",
                "Status: waiting.",
                "Waiting on PR #1641 and pausing the run due to stakeholder approval.",
            ):
                uncited_doc = _valid_handoff_markdown(
                    open_issues="1",
                    active_sessions="0/8",
                    table_rows=(
                        "| #1288 | human-blocked | "
                        "https://github.com/jmservera/ama/pull/1641 | Await owner |"
                    ),
                    summary_prose=uncited_prose,
                )
                uncited_violations = checker.check_handoff_text("uncited-wait.md", uncited_doc)
                pause_hits = [v for v in uncited_violations if "unverified-blocker-pause" in v]
                self.assertEqual(len(pause_hits), 1, msg=uncited_prose)

            cap_wait_doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="1/1 (`rpi-1204`)",
                table_rows="| #1204 | active session | PR #1641 | Running |",
                summary_prose="Waiting for a free worker session slot at 1/1 capacity.",
            )
            self.assertEqual(
                checker.check_handoff_text("cap-wait.md", cap_wait_doc),
                [],
            )

            drain_wait_doc = _valid_handoff_markdown(
                open_issues="1",
                open_prs="18 (PR drain active)",
                active_sessions="1/8 (`rpi-1204`)",
                table_rows="| #1204 | active session | PR #1641 | PR drain active |",
                summary_prose="PR drain active (>15 open PRs); waiting for open PRs below 15.",
            )
            self.assertEqual(checker.check_handoff_text("drain-wait.md", drain_wait_doc), [])

            generic_url_ok_doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="0/8",
                table_rows="| #1288 | human-blocked | https://example.com/1288 | Await gate |",
                summary_prose="Waiting on https://example.com/1288.",
            )
            self.assertEqual(
                checker.check_handoff_text("generic-url-ok.md", generic_url_ok_doc),
                [],
            )

            generic_url_bad_doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="0/8",
                table_rows="| #1288 | human-blocked | https://example.com/1288 | Await gate |",
                summary_prose="Waiting on https://example.com/9999.",
            )
            self.assertIn(
                "unverified-blocker-reference",
                "\n".join(checker.check_handoff_text("generic-url-bad.md", generic_url_bad_doc)),
            )

        with self.subTest(case="rv8-uncited-wait-blocks-ready-work-without-tableless"):
            uncited_ready_doc = _valid_handoff_markdown(
                open_issues="2",
                open_prs="1",
                active_sessions="1/8 (`rpi-1204`)",
                table_rows=(
                    "| #1204 | active session | PR #1641 | Running |\n"
                    "| #1310 | ready to start | none | Ready |"
                ),
                summary_prose="Waiting for stakeholder approval.",
            )
            uncited_ready_joined = "\n".join(
                checker.check_handoff_text("uncited-ready.md", uncited_ready_doc)
            )
            self.assertIn("unsupported-waiting-ready-work", uncited_ready_joined)
            self.assertIn("unverified-blocker-pause", uncited_ready_joined)

    def test_fenced_code_blocks_and_negated_normative_prose_do_not_false_trigger(self) -> None:
        doc = _valid_handoff_markdown(
            summary_prose=(
                'Rule reminder: scheduled checks must never claim "nothing changed" or pause on '
                "an unverified blocker, and counts are never copied from previous ticks.\n\n"
                "```markdown\n"
                "Nothing changed.\n"
                "* HEAD SHA: TBD\n"
                "| Issue | State | Blocker |\n"
                "| --- | --- | --- |\n"
                "| #9999 | unknown | none |\n"
                "```"
            )
        )
        self.assertEqual(checker.check_handoff_text("fenced-ok.md", doc), [])

        with self.subTest(
            case="rv9-multi-token-and-colon-quoted-prohibitions-vs-negative-controls"
        ):
            ready_rows = (
                "| #1204 | active session | PR #1641 | Running |\n"
                "| #1310 | ready to start | none | Launching `rpi-1310` now |"
            )
            for quoted_neg_prose in (
                'Never say "we are waiting on stakeholder approval". Starting `rpi-1310` now.',
                (
                    'Do not report "Current status: paused" without a blocker link. '
                    "Starting `rpi-1310` now."
                ),
                'Do not report "Idle tick: nothing changed". Starting `rpi-1310` now.',
                'Note: "We never report waiting on stakeholder approval." Starting `rpi-1310` now.',
            ):
                qdoc = _valid_handoff_markdown(
                    open_issues="2",
                    open_prs="1",
                    active_sessions="1/8 (`rpi-1204`)",
                    table_rows=ready_rows,
                    summary_prose=quoted_neg_prose,
                )
                self.assertEqual(
                    checker.check_handoff_text("quoted-neg-ok.md", qdoc),
                    [],
                    msg=quoted_neg_prose,
                )

            self.assertTrue(
                checker._is_claim_negated(
                    'Never say "we are waiting on stakeholder approval".',
                    'Never say "we are waiting on stakeholder approval".'.index("waiting on"),
                )
            )

            for quoted_control_prose in (
                'Summary: "Never skip checks; status: paused."',
                'Never skip lint when saying "we are waiting on stakeholder approval".',
            ):
                qbad = _valid_handoff_markdown(
                    open_issues="1",
                    open_prs="1",
                    active_sessions="1/8 (`rpi-1204`)",
                    table_rows="| #1204 | active session | PR #1641 | Running |",
                    summary_prose=quoted_control_prose,
                )
                self.assertIn(
                    "unverified-blocker-pause",
                    "\n".join(checker.check_handoff_text("quoted-neg-bad.md", qbad)),
                    msg=quoted_control_prose,
                )

    def test_stale_counts_shas_timestamps_and_carry_forward_blocks_flagged(self) -> None:
        with self.subTest(case="missing-live-counts-and-provenance"):
            doc = (
                "# Handoff\n\n"
                "* HEAD SHA: f74e1bf1fd7d3e62048a69ade51a126704ebc556\n\n"
                "| Issue | State | Blocker or evidence link | Next action |\n"
                "| --- | --- | --- | --- |\n"
                "| #1204 | ready to start | none | Start |\n"
            )
            joined = "\n".join(checker.check_handoff_text("missing-live.md", doc))
            self.assertIn("stale-or-missing-counts", joined)
            self.assertIn("missing-live-provenance", joined)

        with self.subTest(case="carry-forward-copied-counts-phrase"):
            doc = _valid_handoff_markdown(
                summary_prose="Counts copied from previous handoff brief while session ran."
            )
            joined = "\n".join(checker.check_handoff_text("copied.md", doc))
            self.assertIn("stale-handoff-reference", joined)

        with self.subTest(case="active-sessions-zero-contradicts-active-row"):
            doc = _valid_handoff_markdown(active_sessions="0/8")
            joined = "\n".join(checker.check_handoff_text("sess-zero.md", doc))
            self.assertIn("stale-active-sessions-count", joined)

        with self.subTest(case="placeholder-and-conflicting-head-sha"):
            placeholder_doc = _valid_handoff_markdown(head_sha="TBD")
            self.assertIn(
                "invalid-or-placeholder-sha",
                "\n".join(checker.check_handoff_text("bad-sha.md", placeholder_doc)),
            )
            conflict_doc = (
                _valid_handoff_markdown()
                + "\n* HEAD SHA: 1234567890abcdef1234567890abcdef12345678\n"
            )
            self.assertIn(
                "stale-sha-conflict",
                "\n".join(checker.check_handoff_text("conflict-sha.md", conflict_doc)),
            )

        with self.subTest(case="stale-observed-timestamp-and-cli-expectations"):
            doc = _valid_handoff_markdown(
                observed_utc="2026-11-15T10:00:00Z",
                written_utc="2026-11-15T12:00:00Z",
            )
            joined = "\n".join(
                checker.check_handoff_text(
                    "old-ts.md",
                    doc,
                    expect_head="deadbeef1234",
                    expect_base="cafebabe5678",
                    expect_open_issues=9,
                )
            )
            self.assertIn("stale-snapshot-timestamp", joined)
            self.assertIn("stale-head-sha", joined)
            self.assertIn("stale-base-sha", joined)
            self.assertIn("stale-open-issues-count", joined)

        with self.subTest(case="live-active-sessions-identity-and-omitted-tokens"):
            matching_doc = _valid_handoff_markdown(active_sessions="1/8 (`rpi-1204`)")
            self.assertEqual(
                checker.check_handoff_text(
                    "sess-ok.md", matching_doc, active_sessions={"rpi-1204"}
                ),
                [],
            )
            stale_identity_doc = _valid_handoff_markdown(
                open_issues="2",
                active_sessions="1/8 (`rpi-1204`)",
                table_rows=(
                    "| #1204 | active session | PR #1641 | Running |\n"
                    "| #1310 | ready to start | none | Ready |"
                ),
            )
            stale_joined = "\n".join(
                checker.check_handoff_text(
                    "sess-stale-id.md", stale_identity_doc, active_sessions={"rpi-1310"}
                )
            )
            self.assertIn("stale-active-session-identity", stale_joined)
            self.assertIn("stale-session-classification", stale_joined)

            omitted_tokens_doc = _valid_handoff_markdown(active_sessions="1/8")
            self.assertIn(
                "stale-active-session-identity",
                "\n".join(
                    checker.check_handoff_text(
                        "sess-no-tokens.md", omitted_tokens_doc, active_sessions={"rpi-1204"}
                    )
                ),
            )

            unclassified_session_doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="1/8 (`rpi-999`)",
                table_rows="| #1204 | active session | PR #1641 | Running |",
            )
            declared_only_v = checker.check_handoff_text(
                "sess-declared-mismatch.md",
                unclassified_session_doc,
            )
            self.assertEqual(
                len([v for v in declared_only_v if "stale-session-classification" in v]),
                2,
                msg="\n".join(declared_only_v),
            )
            live_same_v = checker.check_handoff_text(
                "sess-live-mismatch.md",
                unclassified_session_doc,
                active_sessions={"rpi-999"},
            )
            self.assertEqual(
                len([v for v in live_same_v if "stale-session-classification" in v]),
                2,
                msg="\n".join(live_same_v),
            )

            mixed_missing_active_doc = _valid_handoff_markdown(
                open_issues="2",
                active_sessions="2/8 (`rpi-1302`, `maintenance`)",
                table_rows=(
                    "| #1204 | active session | PR #1641 | Unbacked active row |\n"
                    "| #1302 | active session | PR #1642 | Running |"
                ),
            )
            mixed_v = checker.check_handoff_text(
                "sess-mixed-unbacked.md",
                mixed_missing_active_doc,
            )
            self.assertTrue(
                any("stale-session-classification" in v and "#1204" in v for v in mixed_v),
                msg="\n".join(mixed_v),
            )

            non_issue_only_ok_doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="1/8 (`maintenance`)",
                table_rows="| #1288 | human-blocked | #1288#issuecomment-42 | Wait |",
                summary_prose="Maintenance helper session running; waiting on #1288#issuecomment-42.",
            )
            self.assertEqual(
                checker.check_handoff_text("sess-non-issue-ok.md", non_issue_only_ok_doc),
                [],
            )

    def test_cli_main_exit_codes_and_check_git_head(self) -> None:
        live_head = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        with tempfile.TemporaryDirectory() as tmp:
            valid_file = Path(tmp) / "valid-handoff.md"
            valid_file.write_text(_valid_handoff_markdown(head_sha=live_head), encoding="utf-8")
            out_ok = io.StringIO()
            with contextlib.redirect_stdout(out_ok):
                rc_ok = checker.main(
                    [
                        "--root",
                        str(REPO_ROOT),
                        "--handoff",
                        str(valid_file),
                        "--check-git-head",
                        "--expect-open-issues",
                        "3",
                        "--active-sessions",
                        "rpi-1204",
                    ]
                )
            self.assertEqual(rc_ok, 0)

            out_sess_mismatch = io.StringIO()
            with contextlib.redirect_stdout(out_sess_mismatch):
                rc_sess_mismatch = checker.main(
                    [
                        "--no-agent",
                        "--root",
                        str(REPO_ROOT),
                        "--handoff",
                        str(valid_file),
                        "--active-sessions",
                        "rpi-1310",
                    ]
                )
            self.assertEqual(rc_sess_mismatch, 1)
            self.assertIn("stale-active-session-identity", out_sess_mismatch.getvalue())

            bad_file = Path(tmp) / "bad-handoff.md"
            bad_file.write_text(
                _valid_handoff_markdown(head_sha="0000000", summary_prose="Nothing changed."),
                encoding="utf-8",
            )
            out_fail = io.StringIO()
            with contextlib.redirect_stdout(out_fail):
                rc_fail = checker.main(
                    ["--no-agent", "--handoff", str(bad_file), "--root", str(REPO_ROOT)]
                )
            self.assertEqual(rc_fail, 1)

            err_buf = io.StringIO()
            with contextlib.redirect_stderr(err_buf):
                rc_arg_err = checker.main(["--no-agent"])
            self.assertEqual(rc_arg_err, 2)

            err_sess_buf = io.StringIO()
            with contextlib.redirect_stderr(err_sess_buf):
                rc_sess_arg_err = checker.main(
                    ["--no-agent", "--handoff", str(valid_file), "--active-sessions", "bad name"]
                )
            self.assertEqual(rc_sess_arg_err, 2)

    def test_adversarial_rv001_handoff_bypasses_rejected(self) -> None:
        ready_table = (
            "| #1204 | active session | PR #1641 | Running |\n"
            "| #1310 | ready to start | none | Launch now |"
        )
        with self.subTest(case="later-clause-negation-does-not-mask-nothing-changed"):
            doc = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose="Nothing changed; do not launch anything.",
            )
            self.assertIn(
                "unsupported-idle-ready-work",
                "\n".join(checker.check_handoff_text("later-neg.md", doc)),
            )

        with self.subTest(case="earlier-colon-or-comma-negation-does-not-mask-claims"):
            colon_doc = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose="Do not launch anything: nothing changed.",
            )
            self.assertIn(
                "unsupported-idle-ready-work",
                "\n".join(checker.check_handoff_text("colon-neg.md", colon_doc)),
            )
            comma_wait_doc = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose="Cannot merge PR #1641 yet, waiting for stakeholder feedback.",
            )
            self.assertIn(
                "unsupported-waiting-ready-work",
                "\n".join(checker.check_handoff_text("comma-wait.md", comma_wait_doc)),
            )
            stale_clause_doc = _valid_handoff_markdown(
                summary_prose="Never skip git rev-parse; counts copied from previous handoff."
            )
            self.assertIn(
                "stale-handoff-reference",
                "\n".join(checker.check_handoff_text("stale-clause.md", stale_clause_doc)),
            )
            coord_and_idle = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose="Never skip verification and nothing changed.",
            )
            self.assertIn(
                "unsupported-idle-ready-work",
                "\n".join(checker.check_handoff_text("coord-and-idle.md", coord_and_idle)),
            )
            coord_and_wait = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose="Cannot merge PR #1641 yet and waiting for stakeholder feedback.",
            )
            self.assertIn(
                "unsupported-waiting-ready-work",
                "\n".join(checker.check_handoff_text("coord-and-wait.md", coord_and_wait)),
            )
            hold_before_start = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose="Waiting for stakeholder feedback before starting #1310.",
            )
            self.assertIn(
                "unsupported-waiting-ready-work",
                "\n".join(checker.check_handoff_text("hold-before-start.md", hold_before_start)),
            )
            clock_started_wait = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose="Check started at 12:00Z; waiting for stakeholder feedback.",
            )
            self.assertIn(
                "unsupported-waiting-ready-work",
                "\n".join(checker.check_handoff_text("clock-started.md", clock_started_wait)),
            )
            unlisted_pr_wait = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="0/8",
                table_rows="| #1288 | human-blocked | https://example.com/1288#999 | Wait |",
                summary_prose="Waiting on PR #999 before continuing.",
            )
            self.assertIn(
                "unverified-blocker-reference",
                "\n".join(checker.check_handoff_text("unlisted-pr-wait.md", unlisted_pr_wait)),
            )
            for qual_prose in (
                "Waiting for hosted CI on PR #999.",
                "Waiting on parent PR #999.",
                "Waiting on https://github.com/jmservera/ama/pull/999 before continuing.",
                "Waiting on PR #1641, and #999 before continuing.",
                "Waiting on PR #1641, and PR #999 check run.",
            ):
                qual_doc = _valid_handoff_markdown(
                    open_issues="2",
                    active_sessions="1/8 (`rpi-1204`)",
                    table_rows=(
                        "| #1204 | active session | PR #1641 | Running |\n"
                        "| #1288 | human-blocked | https://example.com/1288 | Wait |"
                    ),
                    summary_prose=qual_prose,
                )
                self.assertIn(
                    "unverified-blocker-reference",
                    "\n".join(checker.check_handoff_text("qual-pr-wait.md", qual_doc)),
                    msg=qual_prose,
                )

        with self.subTest(case="linear-time-prohibition-scanner-no-redos-and-possessive-guard"):
            t0 = time.perf_counter()
            failing_redos_doc = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose="Never claim " + ("idle or " * 80) + "and nothing changed.",
            )
            failing_violations = checker.check_handoff_text("redos-fail.md", failing_redos_doc)
            positive_redos_doc = _valid_handoff_markdown(
                summary_prose="Never claim " + ("idle or " * 80) + "nothing changed.",
            )
            positive_violations = checker.check_handoff_text("redos-ok.md", positive_redos_doc)
            elapsed = time.perf_counter() - t0
            self.assertLess(elapsed, LINEAR_TIME_BUDGET_S)
            self.assertIn("unsupported-idle-ready-work", "\n".join(failing_violations))
            self.assertEqual(positive_violations, [])

            ws_t0 = time.perf_counter()
            ws_doc_one = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose=(" " * 8000) + "nothing changed.",
            )
            ws_v_one = checker.check_handoff_text("ws-one.md", ws_doc_one)
            ws_doc_two = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose="only after" + (" " * 8000) + "x nothing changed.",
            )
            ws_v_two = checker.check_handoff_text("ws-two.md", ws_doc_two)
            ws_elapsed = time.perf_counter() - ws_t0
            self.assertLess(ws_elapsed, LINEAR_TIME_BUDGET_S)
            self.assertIn("unsupported-idle-ready-work", "\n".join(ws_v_one))
            self.assertIn("unsupported-idle-ready-work", "\n".join(ws_v_two))

            non_alpha_suffix_doc = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose="Only after #1204 nothing changed.",
            )
            self.assertIn(
                "unsupported-idle-ready-work",
                "\n".join(checker.check_handoff_text("non-alpha-suffix.md", non_alpha_suffix_doc)),
            )

            possessive_bypass_doc = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose="Never copy sessions' counts and ticks' nothing changed.",
            )
            self.assertIn(
                "unsupported-idle-ready-work",
                "\n".join(checker.check_handoff_text("possessive.md", possessive_bypass_doc)),
            )

        with self.subTest(case="historical-or-non-ready-launches-do-not-suppress-waiting-guard"):
            for bad_launch_prose in (
                "Previously launched rpi-1204; waiting on PR #1641.",
                "Previously started #1310; waiting on PR #1641.",
                "Started #1310 last tick; waiting on PR #1641.",
                "Started #1310 earlier; waiting on PR #1641.",
                "Starting #1310 next tick; waiting on PR #1641.",
                "Not starting #1310; waiting on PR #1641.",
                "Not actually starting #1310; waiting on PR #1641.",
                "Will start #1310; waiting on PR #1641.",
                "Will be starting #1310; waiting on PR #1641.",
                "Planning on starting #1310; waiting on PR #1641.",
                "Held off starting #1310; waiting on PR #1641.",
                "Launched rpi-1204; waiting on PR #1641.",
            ):
                bad_launch_doc = _valid_handoff_markdown(
                    open_issues="2",
                    table_rows=ready_table,
                    summary_prose=bad_launch_prose,
                )
                self.assertIn(
                    "unsupported-waiting-ready-work",
                    "\n".join(checker.check_handoff_text("hist-launch.md", bad_launch_doc)),
                    msg=bad_launch_prose,
                )

        with self.subTest(case="cli-double-dash-flags-preserve-same-clause-negation"):
            doc = _valid_handoff_markdown(
                summary_prose=(
                    "Rule reminder: never rely on `gh issue list --state open --limit 500` "
                    "counts copied from previous ticks."
                )
            )
            self.assertEqual(checker.check_handoff_text("cli-neg-ok.md", doc), [])

        with self.subTest(case="general-waiting-for-phrase-requires-table"):
            no_table_wait = (
                "# Check\n\n"
                "* Live commands: `gh issue list --state open --limit 500`, "
                "`gh pr list --state open --limit 200`, "
                "`tmux list-sessions`, `git rev-parse HEAD`\n"
                "* Open issues: 1\n"
                "* Open PRs: 0\n"
                "* Active sessions: 0/8\n"
                "* HEAD SHA: f74e1bf1fd7d3e62048a69ade51a126704ebc556\n\n"
                "Waiting for stakeholder feedback before starting the wave.\n"
            )
            self.assertIn(
                "missing-classification-table",
                "\n".join(checker.check_handoff_text("wait-for.md", no_table_wait)),
            )

        with self.subTest(case="split-classification-table-after-idle-summary-rejected"):
            split_doc = (
                "# Check\n\n"
                "* Live commands: `gh issue list --state open --limit 500`, "
                "`gh pr list --state open --limit 200`, "
                "`tmux list-sessions`, `git rev-parse HEAD`\n"
                "* Open issues: 2\n"
                "* Open PRs: 1\n"
                "* Active sessions: 0/8\n"
                "* HEAD SHA: f74e1bf1fd7d3e62048a69ade51a126704ebc556\n\n"
                "| Issue | State | Blocker or evidence link | Next action |\n"
                "| --- | --- | --- | --- |\n"
                "| #1288 | human-blocked | https://example.com/1288 | Wait |\n\n"
                "Nothing changed since the last check.\n\n"
                "| Issue | State | Blocker or evidence link | Next action |\n"
                "| --- | --- | --- | --- |\n"
                "| #1302 | dependency-blocked | PR #1641 | Wait |\n"
            )
            self.assertIn(
                "summary-before-classification-table",
                "\n".join(checker.check_handoff_text("split-table.md", split_doc)),
            )

        with self.subTest(case="cited-blocker-absent-from-table-and-standalone-blocked-on"):
            waiting_absent = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="0/8",
                table_rows="| #1288 | human-blocked | https://example.com/1288 | Wait |",
                summary_prose="Waiting on #999 before continuing.",
            )
            self.assertIn(
                "unverified-blocker-reference",
                "\n".join(checker.check_handoff_text("wait-absent.md", waiting_absent)),
            )
            standalone_blocked = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="0/8",
                table_rows="| #1288 | human-blocked | https://example.com/1288 | Wait |",
                summary_prose="Summary: blocked on #999.",
            )
            self.assertIn(
                "unverified-blocker-reference",
                "\n".join(checker.check_handoff_text("blocked-absent.md", standalone_blocked)),
            )

        with self.subTest(case="broken-local-anchor-and-digit-prefixed-anchor-rejected"):
            for bad_link in (
                "[details](#nonexistent-section)",
                "[bad](#999-nonexistent)",
                "[#1641](#missing-heading)",
            ):
                bad_anchor_doc = _valid_handoff_markdown(
                    open_issues="1",
                    active_sessions="0/8",
                    table_rows=f"| #1288 | human-blocked | {bad_link} | Wait |",
                    summary_prose="Active check.",
                )
                joined = "\n".join(checker.check_handoff_text("bad-anchor.md", bad_anchor_doc))
                self.assertIn("broken-blocker-anchor", joined)
                self.assertIn("missing-blocker-link", joined)

            valid_anchor_doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="0/8",
                table_rows="| #1288 | human-blocked | [ledger](#blocker-ledger) | Wait |",
                summary_prose="## Blocker Ledger\n\nOwner approval tracked in issue #1288.",
            )
            self.assertEqual(checker.check_handoff_text("ok-anchor.md", valid_anchor_doc), [])

        with self.subTest(case="gh-api-paginate-provenance-accepted"):
            paginated_doc = _valid_handoff_markdown(
                live_commands=(
                    "`gh api --paginate 'repos/jmservera/ama/issues?state=open&per_page=100' "
                    "--jq '.[] | select(.pull_request == null)'`, "
                    "`gh api --paginate 'repos/jmservera/ama/pulls?state=open&per_page=100'`, "
                    "`tmux list-sessions`, `git rev-parse HEAD origin/main`"
                )
            )
            self.assertEqual(checker.check_handoff_text("paginated-ok.md", paginated_doc), [])

        with self.subTest(case="rv001-linear-scaling-across-brackets-slashes-and-repeated-waits"):
            scale_t0 = time.perf_counter()
            for idx_case, adv_prose in enumerate(
                (
                    "[a" * 4000,
                    "[a](b" * 4000,
                    "a/b" * 4000,
                    "`" * 4000 + "x",
                    "waiting on #1641 " * 400,
                    "waiting on #1641; " * 400,
                    "Never claim " + ("waiting on #1641 " * 400),
                )
            ):
                adv_doc = _valid_handoff_markdown(summary_prose=adv_prose)
                self.assertEqual(checker.check_handoff_text(f"scale-{idx_case}.md", adv_doc), [])
            scale_elapsed = time.perf_counter() - scale_t0
            self.assertLess(scale_elapsed, LINEAR_TIME_BUDGET_S)

        with self.subTest(case="rv002-hard-wrapped-multiline-and-blockquote-summaries-rejected"):
            for wrapped_idle in (
                "Nothing\nchanged.",
                "> Nothing\n> changed.",
                "Rule reminder: never claim\n```text\nexample\n```\nnothing changed.",
            ):
                wrapped_idle_doc = _valid_handoff_markdown(
                    open_issues="2",
                    table_rows=ready_table,
                    summary_prose=wrapped_idle,
                )
                self.assertIn(
                    "unsupported-idle-ready-work",
                    "\n".join(checker.check_handoff_text("wrapped-idle.md", wrapped_idle_doc)),
                    msg=wrapped_idle,
                )

            wrapped_wait_doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="0/8",
                table_rows="| #1288 | human-blocked | https://example.com/1288 | Wait |",
                summary_prose="Waiting on\nPR #999.",
            )
            self.assertIn(
                "unverified-blocker-reference",
                "\n".join(checker.check_handoff_text("wrapped-wait.md", wrapped_wait_doc)),
            )

            wrapped_stale_doc = _valid_handoff_markdown(
                summary_prose="* Counts copied from\n  previous handoff."
            )
            self.assertIn(
                "stale-handoff-reference",
                "\n".join(checker.check_handoff_text("wrapped-stale.md", wrapped_stale_doc)),
            )

        with self.subTest(case="rv003-post-target-conditional-and-deferred-launches-rejected"):
            for post_deferred_prose in (
                "Waiting on PR #1641 while starting #1310 after approval.",
                "Starting #1310 once CI passes; waiting on PR #1641.",
                "Waiting on PR #1641 while starting #1310 if checks pass.",
                "Waiting on PR #1641 while #1310 is starting deferred.",
                "Waiting on PR #1641, and starting #1310 failed.",
            ):
                post_deferred_doc = _valid_handoff_markdown(
                    open_issues="2",
                    table_rows=ready_table,
                    summary_prose=post_deferred_prose,
                )
                self.assertIn(
                    "unsupported-waiting-ready-work",
                    "\n".join(checker.check_handoff_text("post-deferred.md", post_deferred_doc)),
                    msg=post_deferred_prose,
                )

        with self.subTest(case="rv004-long-spans-next-action-scoping-and-external-repo-blockers"):
            long_span_doc = _valid_handoff_markdown(
                open_issues="2",
                active_sessions="1/8 (`rpi-1204`)",
                table_rows=(
                    "| #1204 | active session | PR #1641 | Running |\n"
                    "| #1288 | human-blocked | #1288#issuecomment-42 | Wait |"
                ),
                summary_prose=(
                    "Waiting on PR #1641 " + ("across hosted check lanes " * 16) + "and PR #999."
                ),
            )
            self.assertIn(
                "unverified-blocker-reference",
                "\n".join(checker.check_handoff_text("long-span.md", long_span_doc)),
            )

            next_action_only_doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="0/8",
                table_rows=(
                    "| #1288 | human-blocked | #1288#issuecomment-42 | Unblocks #999 later |"
                ),
                summary_prose="Waiting on #999.",
            )
            self.assertIn(
                "unverified-blocker-reference",
                "\n".join(checker.check_handoff_text("next-action-only.md", next_action_only_doc)),
            )

            missing_blocker_col_link_doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="0/8",
                table_rows="| #1288 | human-blocked | awaiting owner | Follow up after #999 |",
                summary_prose="Active check.",
            )
            self.assertIn(
                "missing-blocker-link",
                "\n".join(
                    checker.check_handoff_text(
                        "missing-blocker-col-link.md", missing_blocker_col_link_doc
                    )
                ),
            )

            priority_col_doc = (
                "# Coordinator Scheduled Check Status\n\n"
                "* Observed UTC: 2026-11-15T12:00:00Z\n"
                "* Written UTC: 2026-11-15T12:03:00Z\n"
                "* Live commands: `gh issue list --state open --limit 500`, "
                "`gh pr list --state open --limit 200`, "
                "`tmux list-sessions`, `git rev-parse HEAD origin/main`\n"
                "* Open issues: 1\n"
                "* Open PRs: 1\n"
                "* Active sessions: 0/8\n"
                "* HEAD SHA: f74e1bf1fd7d3e62048a69ade51a126704ebc556\n\n"
                "| Issue | State | Blocker link | Priority |\n"
                "| --- | --- | --- | --- |\n"
                "| #1288 | human-blocked | #1288#issuecomment-42 | P1 #999 |\n\n"
                "Waiting on #999.\n"
            )
            self.assertIn(
                "unverified-blocker-reference",
                "\n".join(checker.check_handoff_text("priority-col.md", priority_col_doc)),
            )

            for external_cite in (
                "Waiting on octo/other#1641.",
                "Waiting on https://github.com/octo/other/pull/1641.",
                "Waiting on [PR #1641](https://github.com/octo/other/pull/1641).",
            ):
                ext_mismatch_doc = _valid_handoff_markdown(
                    open_issues="1",
                    active_sessions="1/8 (`rpi-1204`)",
                    table_rows="| #1204 | active session | PR #1641 | Running |",
                    summary_prose=external_cite,
                )
                self.assertIn(
                    "unverified-blocker-reference",
                    "\n".join(checker.check_handoff_text("ext-mismatch.md", ext_mismatch_doc)),
                    msg=external_cite,
                )

            verified_ext_doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="0/8",
                table_rows=(
                    "| #1288 | dependency-blocked | "
                    "https://github.com/octo/other/pull/1641 | Await upstream |"
                ),
                summary_prose=(
                    "Waiting on octo/other#1641 and "
                    "[PR #1641](https://github.com/octo/other/pull/1641)."
                ),
            )
            self.assertEqual(checker.check_handoff_text("ext-ok.md", verified_ext_doc), [])

        with self.subTest(case="rv6-subclause-launch-scale-multi-ready-and-label-spoof"):
            sub_t0 = time.perf_counter()
            many_subclauses_doc = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose=(
                    "Waiting on PR #1641 " + ("while will be starting #1310 " * 4000) + "."
                ),
            )
            many_sub_v = checker.check_handoff_text("many-subclauses.md", many_subclauses_doc)
            sub_elapsed = time.perf_counter() - sub_t0
            self.assertIn("unsupported-waiting-ready-work", "\n".join(many_sub_v))
            self.assertLess(sub_elapsed, LINEAR_TIME_BUDGET_S)

            two_ready_rows = (
                "| #1204 | active session | PR #1641 | Running |\n"
                "| #1310 | ready to start | none | Launch lane 1 |\n"
                "| #1311 | ready to start | none | Launch lane 2 |"
            )
            partial_launch_doc = _valid_handoff_markdown(
                open_issues="3",
                open_prs="19",
                active_sessions="1/8 (`rpi-1204`)",
                table_rows=two_ready_rows,
                summary_prose="Waiting on PR #1641 while starting #1310 now.",
            )
            partial_joined = "\n".join(
                checker.check_handoff_text("partial-ready.md", partial_launch_doc)
            )
            self.assertIn("unsupported-waiting-ready-work", partial_joined)
            self.assertIn("#1311", partial_joined)

            both_launched_doc = _valid_handoff_markdown(
                open_issues="3",
                open_prs="19",
                active_sessions="1/8 (`rpi-1204`)",
                table_rows=two_ready_rows,
                summary_prose=(
                    "Waiting on PR #1641 while starting #1310 now.\n\n"
                    "Also starting #1311 in an isolated worktree."
                ),
            )
            self.assertEqual(
                checker.check_handoff_text("both-ready.md", both_launched_doc),
                [],
            )

            single_slot_doc = _valid_handoff_markdown(
                open_issues="3",
                active_sessions="1/2 (`rpi-1204`)",
                table_rows=two_ready_rows,
                summary_prose="Waiting on PR #1641 while starting #1310 now.",
            )
            self.assertEqual(
                checker.check_handoff_text("single-slot.md", single_slot_doc),
                [],
            )

            spoofed_label_doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="0/8",
                table_rows=(
                    "| #1288 | dependency-blocked | "
                    "[PR #999](https://github.com/jmservera/ama/pull/1641) | Wait |"
                ),
                summary_prose="Waiting on PR #999.",
            )
            spoofed_joined = "\n".join(
                checker.check_handoff_text("spoofed-label.md", spoofed_label_doc)
            )
            self.assertIn("mismatched-blocker-link", spoofed_joined)
            self.assertIn("unverified-blocker-reference", spoofed_joined)

        with self.subTest(case="rv7-single-subclause-scale-multi-trigger-cap-and-self-urls"):
            single_sub_t0 = time.perf_counter()
            single_sub_hold_doc = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose=(
                    "Waiting on PR #1641; will not be " + ("starting #1310 " * 2500) + "."
                ),
            )
            single_sub_hold_v = checker.check_handoff_text(
                "single-sub-hold.md", single_sub_hold_doc
            )
            single_sub_non_curr_doc = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose=(
                    "Waiting on PR #1641; " + ("starting #1310 " * 2500) + "after approval."
                ),
            )
            single_sub_non_curr_v = checker.check_handoff_text(
                "single-sub-non-curr.md", single_sub_non_curr_doc
            )
            single_sub_elapsed = time.perf_counter() - single_sub_t0
            self.assertIn("unsupported-waiting-ready-work", "\n".join(single_sub_hold_v))
            self.assertIn("unsupported-waiting-ready-work", "\n".join(single_sub_non_curr_v))
            self.assertLess(single_sub_elapsed, LINEAR_TIME_BUDGET_S)

            for multi_trigger_prose in (
                "Waiting on PR #1641 because pausing the run for stakeholder approval.",
                "Blocked on #1641 while waiting on external vendor sign-off.",
                "Waiting on PR #1641 — blocked on owner approval.",
            ):
                multi_trigger_doc = _valid_handoff_markdown(
                    open_issues="1",
                    active_sessions="1/8 (`rpi-1204`)",
                    table_rows="| #1204 | active session | PR #1641 | Running |",
                    summary_prose=multi_trigger_prose,
                )
                self.assertIn(
                    "unverified-blocker-pause",
                    "\n".join(checker.check_handoff_text("multi-trigger.md", multi_trigger_doc)),
                    msg=multi_trigger_prose,
                )

            intro_prefix_ok_doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="1/8 (`rpi-1204`)",
                table_rows="| #1204 | active session | PR #1641 | Running |",
                summary_prose="Status: waiting — blocked on PR #1641.",
            )
            self.assertEqual(
                checker.check_handoff_text("intro-prefix-ok.md", intro_prefix_ok_doc),
                [],
            )

            for cap_spoof_prose in (
                "Waiting for stakeholder approval of the capacity plan.",
                "Paused for owner sign-off across all 8 sessions.",
                "Waiting for a free slot and owner approval.",
                "Waiting for a free slot for external vendor.",
            ):
                cap_spoof_doc = _valid_handoff_markdown(
                    open_issues="1",
                    active_sessions="1/1 (`rpi-1204`)",
                    table_rows="| #1204 | active session | PR #1641 | Running |",
                    summary_prose=cap_spoof_prose,
                )
                self.assertIn(
                    "unverified-blocker-pause",
                    "\n".join(checker.check_handoff_text("cap-spoof.md", cap_spoof_doc)),
                    msg=cap_spoof_prose,
                )

            drain_spoof_doc = _valid_handoff_markdown(
                open_issues="1",
                open_prs="18 (PR drain active)",
                active_sessions="1/8 (`rpi-1204`)",
                table_rows="| #1204 | active session | PR #1641 | PR drain active |",
                summary_prose="Waiting on PR review from owner during drain.",
            )
            self.assertIn(
                "unverified-blocker-pause",
                "\n".join(checker.check_handoff_text("drain-spoof.md", drain_spoof_doc)),
            )

            self_url_only_doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="0/8",
                table_rows=(
                    "| #1288 | dependency-blocked | "
                    "https://github.com/jmservera/ama/issues/1288 | Wait |"
                ),
                summary_prose="Waiting on https://github.com/jmservera/ama/issues/1288.",
            )
            self_url_only_joined = "\n".join(
                checker.check_handoff_text("self-url-cite.md", self_url_only_doc)
            )
            self.assertIn("missing-blocker-link", self_url_only_joined)
            self.assertIn("unverified-blocker-reference", self_url_only_joined)

            valid_self_comment_url_doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="0/8",
                table_rows=(
                    "| #1288 | human-blocked | "
                    "https://github.com/jmservera/ama/issues/1288#issuecomment-42 | Wait |"
                ),
                summary_prose=(
                    "Waiting on https://github.com/jmservera/ama/issues/1288#issuecomment-42."
                ),
            )
            self.assertEqual(
                checker.check_handoff_text("self-comment-url-ok.md", valid_self_comment_url_doc),
                [],
            )

            valid_ext_same_num_doc = _valid_handoff_markdown(
                open_issues="1",
                active_sessions="0/8",
                table_rows=(
                    "| #1288 | dependency-blocked | "
                    "https://github.com/octo/other/issues/1288 | Upstream |"
                ),
                summary_prose="Waiting on https://github.com/octo/other/issues/1288.",
            )
            self.assertEqual(
                checker.check_handoff_text("ext-same-num-ok.md", valid_ext_same_num_doc),
                [],
            )

            blocked_global_hold_doc = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose=("Blocked on PR #1641 before starting new work; starting #1310 now."),
            )
            self.assertIn(
                "unsupported-waiting-ready-work",
                "\n".join(checker.check_handoff_text("blocked-hold.md", blocked_global_hold_doc)),
            )

        with self.subTest(case="rv8-clause-raw-linear-budget-and-coordinated-uncited-waits"):
            single_clause_negated_doc = _valid_handoff_markdown(
                open_issues="2",
                table_rows=ready_table,
                summary_prose=("Waiting on PR #1641; never " + ("starting #1310 " * 4000) + "."),
            )
            t0 = time.monotonic()
            single_clause_violations = checker.check_handoff_text(
                "single-clause-neg.md", single_clause_negated_doc
            )
            single_clause_elapsed = time.monotonic() - t0
            self.assertIn("unsupported-waiting-ready-work", "\n".join(single_clause_violations))
            self.assertLess(single_clause_elapsed, LINEAR_TIME_BUDGET_S)

            coordinated_table = (
                "| #1204 | active session | PR #1641 | Running |\n"
                "| #1288 | human-blocked | #1288#issuecomment-42 | Await owner |\n"
                "| #1302 | dependency-blocked | PR #1642 | Await base PR |"
            )
            for coord_bypass_prose in (
                "Waiting on PR #1641 and stakeholder approval.",
                "Waiting on stakeholder approval and PR #1641.",
                "Waiting on PR #1641 or external vendor.",
                "Blocked on #1288 or owner sign-off.",
                "Waiting on a free slot and PR #1641.",
                "Waiting on PR #1641, stakeholder approval, and PR #1642.",
                "Waiting on stakeholder approval and waiting on PR #1641 checks.",
            ):
                coord_doc = _valid_handoff_markdown(
                    open_issues="3",
                    open_prs="2",
                    active_sessions="1/8 (`rpi-1204`)",
                    table_rows=coordinated_table,
                    summary_prose=coord_bypass_prose,
                )
                self.assertIn(
                    "unverified-blocker-pause",
                    "\n".join(checker.check_handoff_text("coord-bypass.md", coord_doc)),
                    msg=coord_bypass_prose,
                )

        with self.subTest(
            case="rv9-linear-bridge-and-custom-sessions-causal-pause-comma-and-lifecycle-chains"
        ):
            wide_ws_doc = _valid_handoff_markdown(
                open_issues="1",
                open_prs="1",
                active_sessions="1/8 (`rpi-1204`)",
                table_rows="| #1204 | active session | PR #1641 | Running |",
                summary_prose=(
                    "Waiting on PR #1641" + (" " * 20000) + "and waiting on PR #1641 checks."
                ),
            )
            t0 = time.monotonic()
            self.assertEqual(checker.check_handoff_text("wide-ws.md", wide_ws_doc), [])
            self.assertLess(time.monotonic() - t0, 0.15)

            n_sess = 1200
            custom_tokens = ", ".join(f"`worker-{k}`" for k in range(1, n_sess + 1))
            many_rows = "\n".join(
                f"| #{k} | active session | PR #1641 | Running |" for k in range(1, n_sess + 1)
            )
            many_sess_doc = _valid_handoff_markdown(
                open_issues=str(n_sess),
                open_prs="1",
                active_sessions=f"{n_sess}/{n_sess} ({custom_tokens})",
                table_rows=many_rows,
                summary_prose="All worker sessions active.",
            )
            t1 = time.monotonic()
            self.assertEqual(checker.check_handoff_text("many-custom-sess.md", many_sess_doc), [])
            self.assertLess(time.monotonic() - t1, 0.25)

            for causal_bad_prose in (
                "Waiting on PR #1641 because stakeholder approval is pending.",
                "Waiting on PR #1641 due to owner sign-off.",
                "Waiting on PR #1641 pending stakeholder approval.",
                "Waiting on PR #1641 and its hosted CI and stakeholder approval.",
                "Status: paused.",
                "Scheduled check paused.",
            ):
                causal_bad_doc = _valid_handoff_markdown(
                    open_issues="2",
                    open_prs="1",
                    active_sessions="1/8 (`rpi-1204`)",
                    table_rows=(
                        "| #1204 | active session | PR #1641 | Running |\n"
                        "| #1288 | human-blocked | #1288#issuecomment-10 | Await owner |"
                    ),
                    summary_prose=causal_bad_prose,
                )
                self.assertIn(
                    "unverified-blocker-pause",
                    "\n".join(checker.check_handoff_text("causal-bad.md", causal_bad_doc)),
                    msg=causal_bad_prose,
                )

            tableless_paused_doc = (
                "# Coordinator Scheduled Check Status\n\n"
                "* Observed UTC: 2026-11-15T12:00:00Z\n"
                "* Written UTC: 2026-11-15T12:03:00Z\n"
                "* Live commands: `gh issue list --state open --limit 500`, "
                "`gh pr list --state open --limit 200`, "
                "`tmux list-sessions`, `git rev-parse HEAD origin/main`\n"
                "* Open issues: 3\n"
                "* Open PRs: 1\n"
                "* Active sessions: 0/8\n"
                "* HEAD SHA: f74e1bf1fd7d3e62048a69ade51a126704ebc556\n"
                "* Origin/main SHA: a1b2c3d4e5f60718293a4b5c6d7e8f9012345678\n"
                "* Target/base SHA: f74e1bf1fd7d3e62048a69ade51a126704ebc556\n\n"
                "Status: paused.\n"
            )
            tableless_paused_joined = "\n".join(
                checker.check_handoff_text("tableless-paused.md", tableless_paused_doc)
            )
            self.assertIn("missing-classification-table", tableless_paused_joined)
            self.assertIn("unverified-blocker-pause", tableless_paused_joined)

            for valid_rv9_prose in (
                "Waiting on PR #1641 because #1288#issuecomment-10 is pending.",
                "Waiting on PR #1641, pending #1288#issuecomment-10.",
                "Waiting on PR #1641 because its hosted CI is running.",
                "Waiting on PR #1641 and its checks are pending.",
                "Waiting on PR #1641 because blocked on #1288#issuecomment-10.",
                "Waiting on PR #1641 and its hosted CI and status checks.",
                "Status: paused on PR #1641.",
                "Status: paused due to PR #1641.",
                "Status: paused pending #1288#issuecomment-10.",
            ):
                valid_rv9_doc = _valid_handoff_markdown(
                    open_issues="2",
                    open_prs="1",
                    active_sessions="1/8 (`rpi-1204`)",
                    table_rows=(
                        "| #1204 | active session | PR #1641 | Running |\n"
                        "| #1288 | human-blocked | #1288#issuecomment-10 | Await owner |"
                    ),
                    summary_prose=valid_rv9_prose,
                )
                self.assertEqual(
                    checker.check_handoff_text("valid-rv9.md", valid_rv9_doc),
                    [],
                    msg=valid_rv9_prose,
                )

            cap_comma_doc = _valid_handoff_markdown(
                open_issues="2",
                open_prs="1",
                active_sessions="1/1 (`rpi-1204`)",
                table_rows=(
                    "| #1204 | active session | PR #1641 | Running at 1/1 cap |\n"
                    "| #1310 | ready to start | none | Queued |"
                ),
                summary_prose="Waiting for a free worker session slot, until the next check.",
            )
            self.assertEqual(checker.check_handoff_text("cap-comma.md", cap_comma_doc), [])

            drain_comma_doc = _valid_handoff_markdown(
                open_issues="2",
                open_prs="18 (PR drain active)",
                active_sessions="1/8 (`rpi-1204`)",
                table_rows=(
                    "| #1204 | active session | PR #1641 | Running |\n"
                    "| #1310 | ready to start | none | Held under PR drain |"
                ),
                summary_prose=("Waiting for open PRs to drain below 10, pending the next check."),
            )
            self.assertEqual(checker.check_handoff_text("drain-comma.md", drain_comma_doc), [])


if __name__ == "__main__":
    unittest.main()
