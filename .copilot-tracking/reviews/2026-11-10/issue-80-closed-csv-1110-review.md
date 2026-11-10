<!-- markdownlint-disable-file -->
# Review: #80 Closed cases current-page CSV (issue-80-closed-csv-1110)

Execution: executed once, by the implementing worker, after implementation (author review; independent exact-head review is required from root before publication and is not claimed here).
Assessed boundary: working tree on fe59ef56 with the seven source files and the tracking artifacts listed in the changes log.
Outcome: Conformant to the admitted initial slice, with the limits below. No material finding is open.

## Evidence checked

* Scope: only `progress.py`, `server.py`, `web/progress.js`, `test_progress_dashboard.py`, `test_role_endpoint_inventory.py`, `progress_browser_check.py` and the README paragraph changed. No Store, SqlStore, importer, exception, core, schema, model or infra edits; #96 and #153 files untouched.
* Contract: the CSV reuses `closed_cases(store, user, query)` unchanged in the same try block, so validation, authorization (401/403), synthetic-only admission, filters and page normalization match JSON. Tests compare exact rows and columns with JSON.
* Safety: fixed nine-field allowlist, primitive cells, `safe_cell` escaping, header kept on zero rows, attachment only on success; denied and anonymous responses carry no attachment or content; no writes or audit events.
* UI: native anchor after a successful load, described by a note covering constructed demonstration data, current page only, read-only copy, unknown closure blank, Closed not completed or approved, and possible differences on a fresh read.
* Results: 57, 11 and 23 focused tests OK; default `mypy` (2.4.0) from `src/api` with no selectors, `ruff` 0.17.1 check and format pass; browser check 58 PASS (Playwright 1.64.0, real keyboard Enter download bytes versus JSON page).
* #96: `git merge-tree` of this tree against eaf93023 is clean.

## Limits and residual risks

* SQLite and local Chromium only; no SQL Server run and no full or `--changed` gate (DEMO FOCUSED tier). No AT, WCAG or live acceptance is claimed.
* The CSV is a fresh read and may differ from displayed rows; there is no snapshot guarantee (disclosed in the UI).
* Only the Closed cases list gains an export; #80 C2 is not complete for other lists. This change does not close #80.
* The author review is not independent; root exact-head review is still required.
* Browser check defects found during the work (focus-visible heuristic, Reset race) were fixed and the failed logs retained.

## Routed follow-ups

1. Root independent exact-head review before publication.
2. Other #80 C2 list exports, each as its own admitted slice.
3. Optional: broaden browser check to the scale fixture for the Closed page.
