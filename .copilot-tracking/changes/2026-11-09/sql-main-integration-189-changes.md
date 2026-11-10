<!-- markdownlint-disable-file -->
# Issue 189 SQL/main integration changes (2026-11-09)

Plan: [plan](../../plans/2026-11-09/sql-main-integration-189-plan.md). Refs #189 only. Nothing pushed.

## Merge

* Frozen prospective-record commit `d05b98296` (child of `0972a40cb`) committed BEFORE the merge; `origin/main` re-fetched and still `8d6f029cac004506953f36606862168bbe9d9412` (#1308 squash).
* Ordinary `git merge --no-ff origin/main`: commit `105ea6cb5857cd26aa62f3fbd1d55456fa9f38ea`, tree `843679e6ff57cc9f8de0b28c566b48f19fef0efa`, parents `d05b98296` and `8d6f029ca`. No conflicts and no resolution edits. No rebase, reset, stash, force or sibling import. The first merge command failed on my flag (`-F -`) and changed nothing; rerun with `-m`.
* Source diff vs `d05b98296` (`src infra tools`): 12 files, all main's: `server.py`, `app.js`, `test_case_journey.py` (api); `README.md`, `pyproject.toml`, `continuity.py`, `mssqlstore.py`, `sqlstore.py`, `store.py`, `sqlguard.py`, `test_priority_order.py`, `test_resident_decisions.py` (core). The #189 files `simulator_admin.py`, `live_control.py`, `simulator-control.js`, `index.html`, `workbench.py`, the browser check, `test_simulator_admin.py`, `test_live_control.py`, `test_content_standard.py`, `src/api/README.md` are byte-identical to the pre-merge head.

## Composition (App, Store, admin)

`do_POST`: CSRF header gate, view-only gate (403 for every POST except logout, `server.py:1132`), `simulator_admin` hook (`:1134`), ordinary routes; #1308 `CommittedReloadError` handlers (`:1246-1272`) are after both gates. `do_GET` simulator prelude (`:407`). `app.js` `#/simulator` route (`:425`) and loader (`:345`) are separate from `priorityPanel` (`:679`); `pending` and `checkHistory` are local to each panel. `node --check` passes for `app.js` and `simulator-control.js`. Existing controls are unchanged: no source edit was needed or made.

## Selected checks (owner demo-targeted tier)

`src/api` with the worktree `.venv` (modules resolve under this worktree), `PYTHONPATH=tests:../core/tests:../agents/tests`, producer exit written to files in the owned `/tmp/i189-sqlmain-8RYMV6` (raw logs not committed), `ZF_*` variables unset (count 0 on entry), no pipe on producers.

| Check | Exit | Result |
|---|---|---|
| test_simulator_admin | 0 | 27 OK |
| test_live_control | 0 | 34 OK |
| test_entra_authoritative | 0 | 36 OK |
| test_auth | 0 | 41 OK |
| test_content_standard | 0 | 18 OK |
| test_design_system | 0 | 8 OK |
| test_workspace_scripts | 0 | 5 OK |
| test_case_journey (carries #1308 priority route and app.js DOM harness) | 0 | 31 OK |
| core test_priority_order | 0 | 142 run, 77 pass, 65 skipped ("opt-in owned loopback SQL Server") |
| core test_resident_decisions | 0 | 256 run, 163 pass, 93 skipped (opt-in SQL/Azure decorators at lines 3232 and 4159) |
| simulator_control_browser_check with `--axe` (4.10.3, sha256 `880970c0...8a68bb` verified) | 0 | 0 violations in every state: unavailable, rejected, permitted, stop, expired, invalid window, already stopped (and repeat), stale, write error, manual route not writable, view-only administrator |

A first browser invocation with an invented `--out` flag exited 2 (usage error, no checks run); it is an invocation error, rerun correctly, not a product failure. The heavy lock was not needed: nothing queued or taken.

Unverified, not passed: the 65 + 93 skipped actual-SQL/Azure cases (no owned SQL Server: #189 has no SQL statement of its own; simulator start/stop call `store.audit`, which SQL stores may persist), the whole API suite (prior exact-head capture `8ab64519c` preserved: exit 0, 2105 tests, 365 skips, not rerun, since this integration changed no #189 file and the composition and selected checks show no integration risk), ruff/mypy (no source edit), web-guidelines refetch (no #189 web file changed; the upstream `app.js` priority change belongs to #1308), matrix, SMB, cloud, models, budget alert, release.

## Disclosed boundaries (from critique)

Unparseable control file: no Stop form, fail-closed (Stop is offered for every parsed control). Pre-existing malformed bulk-edit audit entry precedes the view-only gate on main (audit-only, unchanged). Both are not new defects and are not fixed here.

## Unchanged

Original independent Functional review and adverse findings, C1 records, source-level approve 0 on `8ab64519c`, historical F3 cause UNKNOWN, capture 2105/365 producer 0, preparation records `current-main-prep-189-*`. C1 is one of five total cycles spent, four remain; none spent or reset. No confirmed new defect.
