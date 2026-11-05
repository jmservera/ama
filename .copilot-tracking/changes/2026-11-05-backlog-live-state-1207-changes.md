# Changes: preserve confirmed active delivery in backlog sync (Refs #1207)

* tools/backlog-sync.py: new `--active N,N|none` (validated; `#N` accepted); open issues named there are In Progress even with merged PRs and no open PR; without `--active`, open In Progress issues with no open PR are kept and listed as "activity unverified"; the `issue-<N>` worktree heuristic is removed; malformed, unknown or closed numbers exit before any write. Closed -> Done with ticking, open-PR -> In Progress, Done-open -> Todo and the review-needed list are unchanged.
* tools/test_backlog_sync.py: 12 offline tests with mocked `gh`/`gh_json` (no live calls); confirmed to fail (10 failures, 8 errors) against the original tool.
* docs/reference/log.md: appended entry. Issue record: .copilot-tracking/github-issues/issue-1207.md.

Validation (reviewed base ead177ef90d24666557708ea344848a1be43bdf8, origin/main re-fetched, unchanged), PYTHONDONTWRITEBYTECODE=1, caches in /tmp:
* `python3 -m unittest discover -s tools -p test_backlog_sync.py` exit 0 (12 OK); `-p test_ci_affected.py` exit 0 (19 OK).
* `python3 tools/backlog-sync.py --active 'x,1'` exit 1 with an explicit message and no gh call.
* ruff check (CI options) on the test file clean; ruff format applied; mypy --ignore-missing-imports on both files clean. The tool has E501 long lines (10 pre-existing, 13 now) and is not in the CI lint list; not reformatted to keep the diff narrow.
* Not applicable or not run: rpi-checks gate, full suites (focused tier; #188 holds the shared lock), SQL, infrastructure, deployment, hosted CI. tools/test_backlog_sync.py is not yet wired into src-ci.yml. No live board run: acceptance on the real board is not claimed.

Coordinator update for #1204 (agent and schedules not modified here). Replace the reconcile sentence with:
"Reconcile the whole backlog at the start of every run and every scheduled check: first verify activity (`tmux ls` for running `rpi-<N>` sessions, plus issues holding a frozen unpublished local candidate), then run `python3 tools/backlog-sync.py --active <N,N,...>` (read-only audit; use `--active none` only after verifying nothing is running) and, if the audit is correct, the same command with `--apply`. Never run it without `--active`: unverified In Progress issues are then kept and listed, and a worktree or missing upstream is not activity."
