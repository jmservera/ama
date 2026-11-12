<!-- markdownlint-disable-file -->
# Changes: #80 browser-built exception-summary CSV (issue-80-exception-csv-1112)

Plan: [plan](../../plans/2026-11-12/issue-80-exception-csv-1112-plan.md). Details: [details](../../details/2026-11-12/issue-80-exception-csv-1112-details.md). Research: [research](../../research/2026-11-12/issue-80-exception-csv-1112-research.md). Critique: [critique](../../plans/2026-11-12/issue-80-exception-csv-1112-critique.md). Review: [review](../../reviews/2026-11-12/issue-80-exception-csv-1112-review.md).

Branch feat/demo-exception-summary-csv-80-1112, base 139176fa0382add781b1830b1ac9db785ed086fe. Local-only; nothing pushed.

## What was implemented

* `src/api/src/zava_forward/api/web/role-screens.js`: fail-closed projection (`exceptionSummaryRows`), CSV writer, a native "Download visible summary (CSV)" button with note (`aria-describedby`) and `role="status"` message, offered only for a clean, non-empty, `state: ok` list; Blob download with the object URL released after a delay and on failure.
* `src/api/tests/test_exception_register_screen.py`: node cases for exact bytes, excluded-field markers, `Unknown` cells (including `constructor` and `__proto__` kinds), non-matching ids, empty, roles-not-named, unreadable, failure paths, zero requests, parity with `list_export.safe_cell`; mocks gain `addEventListener`.
* `src/api/tests/test_data_operator_ai_state.py`: mock `addEventListener` only.
* `src/api/tests/test_exception_register.py`: one view adds exactly one ledger entry and leaves the data document unchanged (O3).
* `src/api/tests/test_role_screens_conformance.py`: the "no timers" guard now allows exactly the one `setTimeout` that releases the object URL; other animation and timer bans are unchanged.
* `src/api/checks/data_operator_browser_check.py`: the register "no controls" assertion became "exactly one control, the summary button"; added keyboard (Tab, Enter, Space), visible focus, saved-bytes-equals-JSON-projection, zero requests, one `/api/exceptions` request, URL release, reflow, and no-button checks for partly unreadable and inconsistent replies. Existing no-write and no-model request checks are unchanged.
* `src/api/README.md`: note beside the register section.

## Amendments and divergences

* Critique CR-001 to CR-006 applied before implementation. Divergence from the details text: the error message also gives a next step (from the fresh web guideline "errors include a fix"). The conformance timer guard was narrowed deliberately (above).
* No divergence from the PR1462 contract. PR1462 proposal files are unchanged.

## Not changed

No server, store, endpoint, producer, appointment, permission, importer, infra, workflow, dependency, docs/ or memory file. No second API call. No issue, board, PR or push. No acceptance tick. No Capacity C6, defaultfive or operational export approval.

## Validation performed (src/api, with the worktree `src/*/src` on PYTHONPATH)

* `unittest discover -s tests` for `test_exception_register*.py` (59 tests), `test_data_operator*.py` (16), `test_role_screens*.py` (19), `test_workspace_scripts.py` (10), `test_connected_home_check.py` (13): OK.
* `ruff check .` clean; `ruff format --check tests` clean (`checks/` is format-excluded by repo config); `mypy` on the three changed test modules: no issues.
* `python3 -m checks.data_operator_browser_check` (real loopback server, Chromium): rc 0, 122 PASS, axe SKIPPED (no `ZF_AXE_JS`), result PARTIAL for axe only.
* Not run: full local gate, `tools/rpi-checks.py`, axe, Firefox or WebKit, `test_role_endpoint_inventory` (needs a different PYTHONPATH and no endpoint changed), hosted CI.
