<!-- markdownlint-disable-file -->
# Changes: aftercare hooks final correction (issue 133, C5)

Input: C4 HEAD 9efdeb0149a2945780dcc8e58208833000d10327 (tree 9e2e2cee6343480a47ba834abd3ef8286f245013), parent a05b7e6b. Main d52f20a5 not adopted; no input integration performed. Refs #133, #89, #134 only. C1 to C5 spent; no automatic C6. WAIT132 semantic exclusion unchanged. Raw logs: root `c5-repro-133-1110/` and `sql-133-hooks-c5-evidence-1110/`.

## Findings reproduced before any fix

* F1 (High): reproduced with a scratch script (`repro_f1.py/.out`): A's failed save, B commits during A's recovery read, A's restore erased B; a later save left only the later request durable.
* F2 (High): reproduced (`repro_f23.py/.out`): a real 401 on POST left no sign-in form and the stale form visible.
* F3 (Medium): reproduced: a cancelable beforeunload with an edited draft was not prevented.

## Changes

* `src/core/src/zava_forward/core/aftercare_store.py`: `update` now classifies a failed save and restores memory inside the same store lock that performed the save. If only the outermost lock exit fails, `_recover_after_exit` reacquires the lock first, then reads and restores. The mutator still runs once; reload failure stays `UnconfirmedWriteError` with the cause attached.
* `src/core/tests/test_aftercare_store.py`: new deterministic two-thread real-JSON regression (events, no sleeps). RED on C4 source (`red_f1_test.log`: "recovery must keep the store lock until it has restored"); GREEN after the fix (`green_f1_adapter_tests_first.log`). Typing fixes: typed mixin base under TYPE_CHECKING, typed `_first_home`, `int()` count.
* `src/api/src/zava_forward/api/web/aftercare.js`: per-view token and captured session; the submit continuation always persists draft, request id and outcome, but renders and focuses only when the session, newest view and mounted form still match. Lazy, once-only `beforeunload` guard that warns while the draft is edited (user input) or unresolved; cleared on confirmed receipt, sign-out and actor change through the existing draft lifecycle. No browser storage. `app.js` unchanged.
* `src/api/checks/aftercare_browser_check.py`: new browser regressions: real 401 keeps sign-in and shows no stale data; same-actor sign-in restores draft and request id and retry saves exactly once; late reply after a hash-route change does not overwrite; beforeunload warning for edited and unresolved drafts (including after a hash change), none for pristine or confirmed receipt; real tab-close dialog; sign-out discards. RED against C4 JS is the F2/F3 reproduction above; GREEN `browser7.log`.
* `src/api/tests/test_aftercare_served.py`: annotated for strict checking.
* `src/core/pyproject.toml`, `src/api/pyproject.toml`: removed the four C4 `ignore_errors` entries. Added only a narrow `disallow_untyped_calls = false` override for the two new test modules because they construct the existing untyped Store, SqlStore, MssqlStore and App; all other strict checks stay on and no baseline entry was touched.
* `src/core/README.md`, `src/api/README.md`: minimal corrections for recovery under lock, session/view ownership and the beforeunload guard.

## Validation (targeted tier; local engineering checks only)

* Core mypy (configured): Success, 286 files, includes adapter and the new test module. API mypy: Success, 214 files, includes the served tests and browser check.
* Core and API `ruff check` and `ruff format --check`: pass. `node --check` aftercare.js and app.js: pass.
* Core: test_aftercare_store (36 tests, 13 MSSQL skipped locally), test_aftercare_intake, test_aftercare, test_scenario_manifest, test_needs_inventory, test_generator_coverage: OK. Workbench recipe SHA unchanged; no manifest edit needed.
* API: test_aftercare_served (8), test_aftercare_screen, test_static_assets, test_workbench, test_role_endpoint_inventory, test_ui_support, test_auth, test_workbench_live_defaults, test_role_matrix: OK.
* Browser: aftercare_browser_check and workbench_browser_check exit 0.
* Real disposable MSSQL (task-owned, `flock -n`, root `sql-133-hooks-c5-evidence-1110`): test_aftercare_store 36 tests, OK, 0 skipped, runner exit 0, container removed, no leftover databases.
* Out-of-scope baseline failures reproduced unchanged and not repaired: API `test_simulator_admin` (1 failure, 1 error, expired 2026-11-10T10:00:00Z fixtures, PR1377); `employee_workspace_browser_check` missing ops exhaustion; `workspace_scripts_browser_check` `len(requests) == count`. Not a broad pass. Axe or keyboard observations are constructed, not assistive-technology, WCAG or human acceptance.
