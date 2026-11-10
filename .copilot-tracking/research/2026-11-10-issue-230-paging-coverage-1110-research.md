<!-- markdownlint-disable-file -->
# Research: issue 230 native browser paging proof (initial coverage)

* Status: OPENED, prospective stub. Substantive findings are appended after the witness research-open boundary is recorded.
* Branch: `test/demo-programme-paging-230-1110`; worktree `/home/azureuser/source/ama-demo-wt/issue-230-paging-coverage-1110`
* Base: main `736561ba0cccb9beb69eea3ae0d3a997bd0dd9bd`; target `feat/demo-ux-coverage-parent-149-1110`.
* Mode: manual-sequenced full loop by owner brief; Research disposition: `executed`.
* Scope: LOCAL ONLY, no push, no PR. NEW initial previously-undelivered native browser paging proof for already delivered paging; not a repair, relabel or fresh corrective budget. Historical numeric correction balance is UNKNOWN and no post-review repair is permitted.

## Research opened

* Witness `research-open` recorded as seq 2 (outcome ok, UTC 2026-11-10T06:45:43Z) after this stub and the state record existed. The substantive findings below were written after that boundary.
* Note: the brief names `freshadmission-230-issue-1110.json`; that file does not exist in the root. The present `admission-230-issue-1110.json` (issue snapshot) and `demo-source-admissions-226-227-230-1110.md` were read instead. Disclosed, not substituted silently.

## Sources read

* Root: `admission-230-issue-1110.json` (issue #230 body and comments), `demo-source-admissions-226-227-230-1110.md` (#230 section), `brief-230-paging-coverage-1110.md`.
* Project guidance: `docs/reference/README.md` (index), `docs/reference/memory.md` (context only), case-study original and addendum (scoped to the demonstrator boundaries), repository instructions (focused validation tier, branch/commit rules).
* Source: `src/api/src/zava_forward/api/web/role-screens.js` (programme queue lines 259-355, screen host 50-112, `programme-queue` registration ~500), `src/api/tests/test_programme_screen.py` (Node paging tests), `src/api/checks/role_screens_browser_check.py` (story 230, read only; owned by active #231), `role_screens_fixtures.py`, `design_system_browser_check.py` (harness `main`, `check`, `scratch_parent`, `child_env`), `server.py` `/api/cases`, `core/store.py` `page_cases`.

## Findings

* Delivered paging: the programme overview loads `/api/cases?view=all&limit=50&offset=N`, shows "Showing cases A to B of T permitted cases ... applies to this page only ... Not a portfolio total", and `#programme-prev` / `#programme-next` buttons (GET only). The pager is rendered only when `total > first page length`. On failure it says "That page could not be loaded. The rows shown are unchanged. Try again, ..." and keeps rows.
* Scope filter is page-local (`X of N records on this page shown ... Filtering changes the view only`), the scope is kept in the address (`scope=`), and Reset restores the default without changing the page or any record.
* Existing coverage: Node 120-case test of next/back/failed-page; browser story 230 covers filter/reset/focus/five gates for manager and coordinator on a single home. No browser check touches `programme-next`, `programme-prev` or `programme-page-status`; the tracked 2026-11-03 changes and review say browser/keyboard paging proof is open. Confirmed absent by search before this task.
* The screen host also renders a separate side "Choose a home" queue (limit 20, links named "Previous page"/"Next page"). The programme pager must therefore be addressed by id/button role, not by the link name.
* The overview renders alongside a selected home (`&case=`), so selected-home evidence can be asserted to persist across in-queue paging.
* Page membership is by ranking (`page_cases` urgent order), not insertion order. A checker must read the actual page-1/page-2 membership from the real read-only API rather than assume labels per page.
* Ordering of the harness: `design_system_browser_check.main(browser_check, data_factory)` owns a loopback server on a free port, a synthetic JSON store in scratch, password `synthetic-check`, a `child_env` without credentials, and `ZF_BROWSER_SCRATCH` outside the checkout. Reusable as is.
* Environments: default `python3` editable installs point at the primary checkout; `/home/azureuser/venv-184` has the canonical Playwright 1.64.0, Ruff 0.17.1, mypy 2.4.0 but editable installs of a foreign worktree. The harness prepends this worktree's `src/*/src` to the server `PYTHONPATH`; runs additionally set that path for the checker and verify concrete origins and the served `role-screens.js` hash. Existing envs are used read-only; no pip.
* Canonical tool versions required by the brief: Ruff 0.17.1, mypy 2.4.0. `python3` PATH has 0.17.3/2.4.1 and is not used for evidence. `/tmp/ama-rpi-heavy.lock` currently has no holder (lsof/fuser).

## Baseline (unchanged tree, HEAD `736561ba`)

* `test_programme_screen` + `test_role_screens`: 24 tests OK, including `test_queue_pages_reach_all_permitted_cases_with_get_only` and `test_queue_page_failure_keeps_rows_and_says_so` (log `/tmp/ama230logs/baseline-node-unit.log`).
* Story 230 browser baseline under a non-queued `flock -n` on the canonical heavy lock: exit 0, 62 PASS, axe SKIPPED (no `ZF_AXE_JS`; four views, printed `PARTIAL`), Chromium 156.0.8078.4 (log `/tmp/ama230logs/baseline-story230.log`).
* Baseline passes, so no stop condition. No product bug found.

## Design decisions

* One new file `src/api/checks/programme_paging_browser_check.py`: private fixture wrapper (60 permitted cases from `role_screens_fixtures.synthetic_data` plus deep copies with unique id and address labels `SYN paging home NNN`; alternate extras have no return so the filter is non-trivial), reuse of `design_system_browser_check.main`/`check`/`ROOT`. No change to shared fixtures, #231 files, #233 files, product JS, Core, schema, auth.
* Role: Retrofit Programme Manager `pam@example.test` only (the actual permitted role for all cases); widths 1280 and 320.
* Fault injection: exactly one `page.route(...offset=50, abort, times=1)` per run, labelled constructed transport failure; not a network incident and not backend proof.
* If a prerequisite cannot be met with existing helpers, stop with the exact unsupported contract; do not fake a staff roster.

## Planning Readiness

Ready. Research disposition: executed.

## Open items

* No axe file is available; axe is SKIPPED and not claimed. Human AT/WCAG acceptance remains unproven (#155).
