<!-- markdownlint-disable-file -->
# Changes: #80 Closed cases current-page CSV (issue-80-closed-csv-1110)

Status: COMPLETE (implementation finished; evidence under the root phase80-closed-csv-evidence-1110 directory).

Plan: [plan](../../plans/2026-11-10/issue-80-closed-csv-1110-plan.md). Details: [details](../../details/2026-11-10/issue-80-closed-csv-1110-details.md).

## Log

* Pre-implementation: no source edits at the time of the stub; the tree was at fe59ef56 plus tracking files only.
* Failing-first tests written; confirmed failing (no `closed_csv`, CSV route returned 403).
* `src/api/src/zava_forward/api/progress.py`: `CLOSED_EXPORT_FIELDS` and `closed_csv(result)` (header always, primitive-only cells, `safe_cell`). `closed_cases` unchanged.
* `src/api/src/zava_forward/api/server.py`: `get_kind` maps `/api/closed-cases.csv` to `cases`; progress/closed dispatch serves the CSV from the same read in the same try block (identical 400/403 mapping), attachment `closed-cases-page.csv`. `LIST_EXPORTS` untouched (its `to_csv` drops headers on zero rows).
* `src/api/src/zava_forward/api/web/progress.js`: native "Download this page for Excel" anchor and described note, only after a successful load, using the normalized page and limit plus current filters.
* `src/api/tests/test_progress_dashboard.py`: JSON/CSV parity, pages and limits, empty header, formula and awkward text, non-primitive TypeError, no mutation or audit, HTTP role/attachment/rejection parity. `test_role_endpoint_inventory.py`: route added.
* `src/api/checks/progress_browser_check.py`: keyboard Enter real download versus JSON page for first, page two, filtered, empty and reset; 503 read-error without link; nonmanager no link and 403 without attachment.
* `src/api/README.md`: one paragraph for the CSV route.

## Amendments and divergences

* Ruff E501 and format findings in `progress.py` and the browser check were fixed (ruff run 1 failed, kept in evidence history).
* Browser run 1 failed (programmatic focus is not focus-visible after a mouse click); a Shift key press now precedes `focus()`. Browser run 2 failed on a race (Reset re-render); the check now waits for "24 matching closed cases". Logs `browser-run-1.log` and `browser-run-2.log` are preserved; run 3 passed (58 PASS, exit 0). These were check defects, not product defects.
* No plan divergence in source scope.

## Validation (SQLite and local Chromium only; DEMO FOCUSED tier)

* test_progress_dashboard 57 OK, test_list_export_api 11 OK, test_role_endpoint_inventory 23 OK.
* Default `mypy` from `src/api` with no selectors: no issues in 213 files (mypy 2.4.0). `ruff check` and `ruff format --check` pass (ruff 0.17.1). Playwright 1.64.0.
* `git merge-tree` with #96 head eaf93023: clean, no conflict; #96 source untouched.
* No axe/AT/WCAG acceptance beyond the check's own pinned axe assertions; no SQL Server claim; no full gate.
