<!-- markdownlint-disable-file -->
# Issue 189 SQL/main integration phase details (2026-11-09)

Plan: [plan](../../plans/2026-11-09/sql-main-integration-189-plan.md).

## P2 Merge

* Preconditions: `git status --short` empty; `git rev-parse HEAD^` equals `0972a40cb73d8ee56ef99de69cd240ce6d1a5ffe` (HEAD is the frozen record commit); `git config --local user.email` equals `8036360+jmservera@users.noreply.github.com` (confirm with `gh api user`); `git fetch origin` then `git rev-parse origin/main` re-pinned (must be `8d6f029cac004506953f36606862168bbe9d9412`; if it moved, STOP before merging and report the new pin to the coordinator, no unreviewed newer main).
* Command: `git merge --no-ff origin/main` with a Conventional Commit message and the Copilot trailer. Read-only `git merge-tree --write-tree` already clean.
* Conflict rule: keep both intents; `server.py` (#1308 priority 409 handlers vs #189 GET prelude and POST hook) and `app.js` (`priorityPanel` vs simulator loader/route) are the only overlap files, in different regions. Record each hunk if conflicts appear.
* Prohibited: rebase, reset, stash, force, cherry-pick, sibling-branch import.

## P3 Pin differences

* `git diff --stat 0972a40cb HEAD -- src infra tools` equals main's delta from `9f9aacc8b` to `8d6f029ca` (core Store/SQL, `server.py`, `app.js`, `test_case_journey.py` and tests).
* #189-only `src/api` files (`simulator_admin.py`, `live_control.py`, `simulator-control.js`, `index.html`, `workbench.py`, the browser check and their tests) must be byte-identical to `0972a40cb`.
* Record merge commit, tree and parents.

## P4 Composition check (read-only)

* `grep -n` in the merged `server.py`: view-only gate before the simulator hook before the `CommittedReloadError` imports; no new mutating route bypasses the gate.
* `app.js`: `priorityPanel` and the `#/simulator` route are separate; `node --check` both web files.

## P4b Disclosed boundaries (critique 2, 3, 6)

* A control file that cannot be parsed is `invalid` with no Stop form and is fail-closed in `live_control`; Stop is offered for every parsed control (`3d8a7a012`). Confirm by reading the existing test and record; no behaviour change.
* The pre-existing `do_POST` malformed-body branch audits a rejected bulk edit request before the view-only gate. It is an audit-only record of rejected input, not an operational mutation; it is not changed here (removing it would silently drop a security audit) and is disclosed as a boundary of 'default-deny every mutation'.
* Simulator start/stop call `store.audit`, which may use SQL when the store is SQL; the #189 code has no SQL statement of its own and actual SQL behaviour stays unverified.

## P5 Checks

Environment: `src/api`, repository `.venv` bound to this worktree (print module paths first), owned `mktemp -d` directory named with `i189-sqlmain`, `unset ZF_RESIDENT_AZURE_TEST ZF_RESIDENT_MSSQL ZF_SQL_SERVER ZF_SQL_TASK_MANIFEST` (and record `env | grep -c ZF_` names only) so no inherited variable reaches a real database, producer exits written to files without pipes, `PYTHONPATH=tests:../core/tests:../agents/tests` (bare module names; `tests.<module>` fails on sibling imports).

* `python -m unittest test_simulator_admin test_live_control test_entra_authoritative test_auth test_content_standard test_design_system test_workspace_scripts test_case_journey -q` (split into separate producers for exit attribution).
* From `src/core`: `PYTHONPATH=tests python -m unittest test_priority_order test_resident_decisions -q`; actual-SQL cases skip without an owned container and are reported as unverified.
* Browser: `python -m checks.simulator_control_browser_check --axe <verified asset path>` (without `--axe` the runner prints NOT RUN and must not count as passed) with the pinned axe 4.10.3 asset whose sha256 is verified against `880970c0...8a68bb` before use. Missing prerequisite: BLOCKED.
* Heavy work (if a whole API run is ever justified) uses `flock -n /tmp/ama-rpi-heavy.lock` and is never queued; if busy do independent work.
* Web guidelines: refetch the source only if the integrated web region needs review; otherwise record that no #189 web file changed and `app.js` change is upstream #1308 (reviewed by its owner), and say what was not refreshed.

## P6 Evidence

Changes `changes/2026-11-09/sql-main-integration-189-changes.md`, review `reviews/2026-11-09/sql-main-integration-189-review.md`, state `rpi-sessions/2026-11-09/sql-main-integration-189-state.json`, handoff `handoff-189-sql-main-integration.md` in the coordinator session files directory. Raw logs stay out of the commit.

## Branch and gate reporting

Report clean exact HEAD, tree, base (`origin/main` pin), source/diff inventory, ordered RPI paths, test commands, counts, exits, skips and unverified SQL. Nothing is pushed; no `Closes`; AC ticks are the coordinator's.
