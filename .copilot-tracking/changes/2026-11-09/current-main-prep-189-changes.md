<!-- markdownlint-disable-file -->
# Issue 189 current-main preparation changes (2026-11-09)

Plan: [plan](../../plans/2026-11-09/current-main-prep-189-plan.md). Review: [review](../../reviews/2026-11-09/current-main-prep-189-review.md). Refs #189 only. Local only; nothing pushed.

## Identities

* Start head `8ab64519ce17aed2b4565f4f185957ab79a270bf`; prospective records commit `9c4db2d8f9986b8d267c7f9bc822d83a94ad7790` (research, plan, details, critique, state; made before the merge).
* Fetched `origin/main` `9f9aacc8be6a1b0e9a10efd367d1ea8bd7520939`; merge base `df8e858b2`.
* Merge commit `81a61fd6427c46aca3f6ff7c7c8d27db68db5ea5`, tree `a69b04e82d81590f724158af0ea12fbe5282959c`, parents `9c4db2d8f` and `9f9aacc8b` (ordinary `--no-ff`, no conflicts, no resolution edits, no rebase, reset, stash or force).

## Source differences pinned (`git diff --stat 8ab64519c 81a61fd64 -- src infra tools`)

8 files, +1115/-51, all from main: `infra/README.md`, `src/agents/.../queue_azure.py` (new), `src/agents/tests/test_queue_azure.py` (new), `tools/capstone/Invoke-Capstone.ps1`, `Test-CostStatus.ps1`, `Test-DeckInsertion.ps1`, `test_render_preview.py`, `tools/cowork-native-recovery/Invoke-StoryReview.ps1`. `git diff 8ab64519c 81a61fd64 -- src/api` is empty: the 12 #189 `src/api` paths are byte-identical. No web file changed. Docs: `docs/reference/README.md` and `log.md` are main's versions; #189 adds no knowledge-base file. No #1292 content imported (`CommittedReloadError` absent from `src`).

## Selected checks (demo-targeted tier; no `rpi-checks --all`)

Run from `src/api`, `.venv` bound to this worktree (`zava_forward.api/core/agents` resolve under this worktree), `PYTHONPATH=tests:../core/tests:../agents/tests`, each producer exit recorded to files without pipes in an owned `mktemp -d` directory (`/tmp/i189-prep-zDbDEG`, raw logs not committed). A first attempt using `tests.<module>` failed on bare sibling imports (`test_auth` not found); it is an invocation error, rerun with the working form above, not a product failure.

| Check | Exit | Result |
|---|---|---|
| test_simulator_admin | 0 | 27 OK |
| test_live_control | 0 | 34 OK |
| test_entra_authoritative | 0 | 36 OK |
| test_auth | 0 | 41 OK |
| test_content_standard | 0 | 18 OK |
| test_design_system | 0 | 8 OK |
| test_workspace_scripts | 0 | 5 OK |
| simulator_control_browser_check.py with pinned axe 4.10.3 (sha256 `880970c0...8a68bb`) | 0 | 11 states, 0 violations (unavailable, rejected, permitted, stop, expired, invalid window, already stopped, stale, write error, manual not writable, view-only administrator) |
| src/agents test_queue_azure (informational, main's new file) | 0 | 24 OK |

Zero skips in these runs. The shared heavy lock `/tmp/ama-rpi-heavy.lock` was held by another lane; none of these jobs is heavy, none queued or waited on the lock, and none took it. Not run: whole `src/api` suite (prior exact-head capture `8ab64519c` preserved: exit 0, 2105 tests, 365 skips), SQL, ruff/mypy (no source file changed), web-guidelines refetch (no web file changed), full gate, live SMB, cloud, model, budget alert.

## Coverage mapping

Default-deny read-only-admin mutation: `test_simulator_admin`, `test_entra_authoritative`, browser view-only state. Stop in all readable writable states: browser expired, invalid window, already stopped, stale, permitted. Manual and disabled paths: browser manual route, unavailable.

## Unchanged

Original independent Functional review (source-level approve 0 findings on `8ab64519c`, original adverse findings), C1 records, F3 cause UNKNOWN, API capture 2105/365 producer 0: all untouched (`git diff 8ab64519c HEAD` shows no `simulator-control-189-*` change). C1 is one of five total cycles spent, four remain; none spent here.
