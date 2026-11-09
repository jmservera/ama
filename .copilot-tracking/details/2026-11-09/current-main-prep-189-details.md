<!-- markdownlint-disable-file -->
# Issue 189 current-main preparation phase details (2026-11-09)

Plan: [plan](../../plans/2026-11-09/current-main-prep-189-plan.md).

## P2 Merge

* Preconditions: `git status --short` empty, `git rev-parse HEAD` is the prospective-record commit and `git rev-parse HEAD^` equals `8ab64519ce17aed2b4565f4f185957ab79a270bf`, `git config --local user.email` equals the repository-local noreply address of the authenticated account (already set; verify with `gh api user`).
* Command: `git merge --no-ff origin/main -m "<conventional message with trailer>"` (ref pinned to `9f9aacc8b`; verify `git rev-parse origin/main` first). Dry run already clean by `git merge-tree`.
* Conflicts: none expected. If any, keep both intents (main log/index entries and #189 content) and record each hunk.
* Prohibited: rebase, reset, stash, force, cherry-pick of #1292 content, merging `origin/fix/demo-recovery-1292-1109`.

## P3 Pin source differences

* `git diff --stat 8ab64519c HEAD -- src infra tools` must equal main's source list: `queue_azure.py`, `test_queue_azure.py`, `infra/README.md`, `tools/capstone/*`, `tools/cowork-native-recovery/Invoke-StoryReview.ps1`.
* `git diff 8ab64519c HEAD --` on the 12 #189 `src/api` paths must be empty.
* Record identities: merge commit, tree, parents.

## P4 Selected checks (from `src/api` with worktree `.venv`; create only if the venv is missing)

* Verify imports resolve to this worktree (`python -c` printing module paths) before running.
* `PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest tests.test_simulator_admin tests.test_live_control tests.test_entra_authoritative tests.test_auth tests.test_content_standard tests.test_design_system tests.test_workspace_scripts -q` with exit recorded to a file in an owned `mktemp -d` directory; no pipes on the producer.
* Browser: `src/api/checks/simulator_control_browser_check.py` (11 states, axe 4.10.3) and it must pass; if Chromium or the pinned axe asset is unavailable, record validation as BLOCKED (not passed) and report the prerequisite. It is lightweight, but use `flock -n` on the shared heavy lock if the existing convention requires it; if busy, do not queue.
* Informational: `test_queue_azure` from `src/agents` if importable.
* Not run: whole `src/api` discovery, SQL tests, ruff/mypy on untouched files (run ruff and mypy only if a source file changes).

## P5 Evidence

Changes record at `changes/2026-11-09/current-main-prep-189-changes.md` with commands, exits, counts, skips; review at `reviews/2026-11-09/current-main-prep-189-review.md`; state at `rpi-sessions/2026-11-09/current-main-prep-189-state.json`. Raw logs stay in the owned temp directory and out of the commit except short exit/count excerpts.

## Remaining #1292 integration (to be reported, not performed)

After #1292 is on actual main: normal merge of that main; expected textual regions in `server.py` (#1292 `/api/ai/priority` POST handlers vs #189 hooks) and `app.js` (`priorityPanel` vs simulator loader/route); re-run selectors: the P4 set plus `test_case_journey` priority tests, the priority/resident core tests as #1292 declares them, `app.js` DOM harness, 11-state browser check, and SQL tests as scoped by the landed #1292 changes and their owned gate; decide the SQL scope then from the actual source, not now. Then final independent exact-head review and hosted CI.
