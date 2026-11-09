<!-- markdownlint-disable-file -->
# Issue 189 SQL/main integration research (2026-11-09)

Task `sql-main-integration-189`; parent `current-main-prep-189` (preparation HEAD `0972a40cb`, tree `cb8ec8afd...`). Refs #189 only. Research disposition: executed (prospective; read-only inspection, no source change).

## Pinned facts

* Fetched `origin/main` is `8d6f029cac004506953f36606862168bbe9d9412` (`fix(core): preserve priority ordering and serialize SQL index bootstrap (#1308)`); it contains the #1292 landing. The previous preparation merged `9f9aacc8b` (#1309 checkpoint); main has since advanced by two commits (`ba5cc74b8` rubric score, `8d6f029ca` #1308).
* Local branch `feat/demo-simulator-control-189-1109`, clean, HEAD `0972a40cb`; nothing pushed. Repository-local email `8036360+jmservera@users.noreply.github.com` already set (from `gh api user`).
* A read-only `git merge-tree --write-tree HEAD origin/main` is clean (exit 0). Observation only; no ref or index changed.
* #1308 changes under `src`: `src/api` `server.py` (POST `/api/ai/priority` and PUT priority resolve now map `CommittedReloadError` to 409), `web/app.js` (`priorityPanel` hold note, `pending`/`checkHistory` guards, `order_note`), `tests/test_case_journey.py`; `src/core` `store.py`, `continuity.py`, `sqlstore.py`, `mssqlstore.py`, `README.md`, `pyproject.toml`, `tests/sqlguard.py`, `tests/test_priority_order.py`, `tests/test_resident_decisions.py`.

## Composition analysis (App, Store, admin)

* `do_POST` order today: sign-in, `_user`, CSRF header gate, view-only gate (every POST except `/api/logout` is 403 for `view_only` administrators), then the #189 `simulator_admin.handles` hook, then the ordinary routes. The #1308 `CommittedReloadError` handlers are inside the ordinary `/api/ai/priority` branch, after both gates. Admin default-deny is therefore unaffected.
* `do_GET` simulator prelude (line ~407) and `app.js` `#/simulator` route are in different regions from `priorityPanel`; no shared state (`checkHistory`, `pending` are local to the priority panel).
* #189 files `simulator_admin.py`, `live_control.py`, `simulator-control.js`, the browser check and their tests are not edited by main: the preparation diff shows no main change to them.
* The #189 simulator and admin controls do not import `sqlstore`/`mssqlstore` or open a SQL connection (only `test_live_control` has a no-connect connector-selection test). No #189 code path depends on the SQL priority ordering change.

## SQL scope (decision from landed source)

* #1308 SQL behaviour is gated by `tests/sqlguard.py`, which admits only a task-labelled disposable loopback container with a manifest, a password digest, an age under 24 h and a Docker inspect check. That gate belongs to #1292. #189 has no SQL code to exercise and no owned SQL container is running; creating a SQL Server for an integration that does not touch SQL would add cost and risk and no #189 evidence.
* Decision: do NOT start SQL. Run the JSON/SQLite and fake-SQL parts of the priority/resident core and API tests that main declares; the actual-SQL cases skip and are reported as unverified, not passed. If any selected run shows an actual compositional dependency on SQL, stop and record it before any fix.

## Constraints carried

Historical records untouched: original independent Functional review and adverse findings, C1 records, source-level approve 0 on `8ab64519c`, historical F3 cause UNKNOWN, capture 2105 tests / 365 skips producer 0. C1 is one of five total cycles spent, four remain; an integration without a real fix neither resets nor consumes a cycle. A confirmed new defect records scope and count before any fix. No push, PR, board, issue tick, rebase, reset, stash, force, new feature, matrix, SMB, cloud, model, role grant or release action. Owner demo tier: targeted tests; no `rpi-checks --all`.

## Planning Readiness

Ready. Remaining unknowns are test outcomes, recorded prospectively as P4.
