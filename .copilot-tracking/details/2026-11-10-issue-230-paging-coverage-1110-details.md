<!-- markdownlint-disable-file -->
# Details: issue 230 native browser paging proof

## Phase 1: checker design

* `paging_data()` private wrapper: `synthetic_data()` (read only import), align case 0 return as the existing story does, then deep-copy case 0 into extra cases so total is exactly 60 (>50): ids `ZF-PG-NNN`, `home.address` `SYN paging home NNN`; odd extras have `returns=[]` so the default scope hides them. No shared fixture edit.
* Checker flow per width in (1280, 320), fresh browser context each, role `pam@example.test`:
  1. Sign in (actual form), then attach `watch` (pageerror, non-GET requests); snapshot read-only `GET /api/cases/{id}` for the selected home and one id per page; read-only `GET /api/cases?view=all&limit=50&offset=0|50` to learn actual page membership (50 and 10 items, total 60, disjoint unique addresses).
  2. Open `#/screens?screen=programme-queue&case=ZF-1`; assert the page status text for cases 1 to 50 of 60, "this page only", "Not a portfolio total"; default-scope rows equal the permitted rows of page 1; no overflow.
  3. Previous at the start: no GET issued.
  4. Keyboard: focus the last control before the main region, Tab to `#programme-prev` then `#programme-next` by native order; select scope "All permitted cases on this page" by keyboard and Apply; status says `50 of 50 records on this page`; `scope=all` in the address.
  5. One constructed fault: `page.route` aborts the first `offset=50` GET (`times=1`). Next by Enter: status shows the failure text and "rows shown are unchanged"; rows, filter status and selected-home evidence text are identical; no page 2 row appears.
  6. Retry with Enter: status cases 51 to 60 of 60; rows are exactly the 10 page-2 ids and no page-1 id; scope `all` retained (filter is page-local, status `10 of 10 records on this page`); selected evidence unchanged.
  7. Next at the end: no extra GET. Reset by keyboard: default scope, page status unchanged (still 51 to 60), no `scope=` in the address, rows match permitted default rows of page 2.
  8. Previous by keyboard: cases 1 to 50 of 60, rows match page 1 default-scope rows, no page-2 ids; selected evidence unchanged.
  9. Final: observed paging GET sequence is exactly offsets `0, 50(aborted), 50, 0`; no writes; no pageerror; record snapshots equal; overflow checked after each state; no write controls inside the queue region (`input[type=submit]`, forms other than the Scope filter form).
* Provenance assertions inside the checker: concrete `__file__` for the checker, the fixture module, the harness; the served `/role-screens.js` SHA-256 equals the worktree file; the server executable is `sys.executable`.
* Honest labels printed: fault injection is a constructed transport failure; page membership comes from the real API; not WCAG/AT acceptance; axe is not run.

## Phase 2: execution

* Acquire `/tmp/ama-rpi-heavy.lock` with `flock -n` (non-queued) after confirming no holder; `timeout 300`; `ZF_BROWSER_SCRATCH` outside the checkout; env `PYTHONPATH` to this worktree's `src/*/src`; interpreter `/home/azureuser/venv-184/bin/python` (read only).
* Preserve first failure and raw logs externally in `/tmp/ama230logs` then copy to the root evidence directory.

## Phase 3: documentation and controls

* Add a short `python -m checks.programme_paging_browser_check` paragraph after story 230 in `src/api/README.md` stating scope, fault-injection label and non-claims.
* Static: Ruff 0.17.1 `check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`, `format --check`, mypy 2.4.0 strict on the new file via the project configuration.
* Controls: `test_programme_screen`, `test_role_screens`, `test_workbench`, `test_queue_empty_state`; core `test_needs_inventory`; registered recipe `src/api/checks/workbench_browser_check.py` git blob unchanged (N/A for changing the recipe SHA because the file is not touched).

## Phase 4: review and closure

* One review of the final diff against the plan and the adverse list; no repair after it.
* Commit in two scoped commits: coverage (checker plus README) and original RPI evidence; privacy-safe identity `8036360+jmservera@users.noreply.github.com`, Co-authored-by trailer.
