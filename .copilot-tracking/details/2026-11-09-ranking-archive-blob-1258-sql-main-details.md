# Issue 1258 SQL main integration details (2026-11-09)

Refs #1258. Plan: `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-sql-main-plan.md`.

## Phase 1: prospective commit

Add only the sql-main research, plan, details and critique files. Author and committer `8036360+jmservera@users.noreply.github.com` (repo-local). `docs(rpi): ...` Conventional Commit with the Copilot trailer. No logs.

## Phase 2: merge

Re-fetch; require `git rev-parse origin/main` equal `8d6f029cac004506953f36606862168bbe9d9412`, else stop. `git merge --no-ff -m <Conventional Commit with trailer> 8d6f029cac004506953f36606862168bbe9d9412`. Verify author and committer on the merge. On conflict: record `git diff --name-only --diff-filter=U` and hunks, `git merge --abort` only, stop.

## Phase 3: validation

Scratch directory from `mktemp -d` (path in `/tmp/ama1258-sqlmain.path`), venv inside it, `pip install -e core -e agents -e api ruff mypy` from this worktree's `src`. Logs in the scratch directory. Run the plan selectors; record exact commands, counts, exits and skips. Also record `git diff --check` and tree identity of `ranking_archive_blob.py`, `ranking_publication.py`, `ranking_publication_runner.py` against `52f9b61b` (byte identity of the adapter).

## Phase 4: records

New unique paths with suffix `-sql-main`: changes, review, state JSON under `.copilot-tracking/rpi-sessions/2026-11-09/`. Stop rather than overwrite. Handoff `handoff-1258-sql-main-integration.md` in the coordinator session files directory. No push, PR, issue or board change.
