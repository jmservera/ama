# Changes: parent73 CLI component integration with current main

Task `issue-73-cli-integration-1109`, date 2026-11-09. Plan: `.copilot-tracking/plans/2026-11-09/cli-integration-73-1109-plan.md`. `rpi-implement` activated after the single critique (Revise, all findings applied directly).

## Scope

Partial parent #73 / child #135 CLI component integration only. No source file was edited by this task; the only code-bearing change is the ordinary merge commit. #73 and whole #135 stay open and unmet; #80/#84/#122 dependencies are retained, not waived.

## P01 Pre-merge qualification (complete)

* cwd and branch `feat/demo-exception-workflows-73-1109`, HEAD `a4317567f806d9585db716d6ae5ad4af6bed5366`, local `origin/main` `3bc20719803a77490c704f985559720e23aa169d`; no tracked modification; only the named RPI artifacts untracked; no path collision with main; `user.email` is `8036360+jmservera@users.noreply.github.com`.
* Venv (outside repo): worktree-editable `zava-forward-core` and `zava-forward-import`, ruff 0.17.1, mypy 2.4.0. Resolved module paths under this worktree. Only the package index was used; no `PYTHONPATH`.

## P02 Merge (complete)

* `git merge --no-ff` of SHA `3bc20719...` by message with noreply identity and Co-authored-by trailer. Result commit `f83040d5d6d3a490db663766949840cb75ec4042`, tree `97ce8c10653e51413c58a35843c5aed10b6edb7f` (equals the predicted trial-merge tree), parents `a4317567...` and `3bc20719...`. No conflict, no rebase/force/reset/amend, no fetch.
* Path checks: `git diff --name-only a4317567..HEAD` equals main's own delta; `3bc20719..HEAD` has no path outside `src/importer` and `.copilot-tracking`; `git diff a4317567..HEAD -- src/importer` is empty; both pins are ancestors of HEAD.

## P03 Verification (complete, all green)

| Check | Result |
| --- | --- |
| Importer unittest (from `src/importer`) | 71 ran, OK, 0 skipped, exit 0 |
| Core `test_exception_feeds`, `test_exception_queue` | 23 ran, OK |
| `ruff format --check .`, `ruff check .` | 13 files formatted, all checks passed, exit 0 |
| `mypy` importer project (`src`, `tests`) | Success: no issues in 12 source files |
| Separate-process synthetic scenarios (11) | 11 PASS: persist/reopen (exit 1 twice, 1 row, hash of bytes), hashless oversized opaque `source:` identity, same basename distinct, replacement new refusal, same-bytes first reason one row, missing and permission-unreadable attempts distinct and hashless, DB open error exit 2, DB write error exit 2 with 0 rows, read-only viewer left DB and all source hashes unchanged with no sidecar, no steward gives `UNROUTED`, `items=0`, Unassigned (Unknown) |
| Static boundary | no `importer` reference under `src/api`; register `NOT_CONNECTED` still present; the only importer text match for replay is a docstring saying nothing is replayed; `feed_failed_imports` has no caller other than the importer |

Skips: SQL Server, browser, model, provider, network, Azure, full gate, hosted CI (none run by design). Core register tests were not run beyond exception feed/queue because no Core file changed on this side. Scenario script lived in the session scratch directory, uncommitted.

## Divergences, amendments, follow-ups

* No importer compat fix or README change was needed (no red repro, no overclaim found).
* Follow-ups unchanged: served queue, register/store hook, recovery, scoped operator access (#132 shared integration, whole #135); independent exact-head review, hosted CI and owner merge gate before any publication.
