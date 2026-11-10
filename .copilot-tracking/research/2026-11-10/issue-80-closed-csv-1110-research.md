<!-- markdownlint-disable-file -->
# Research: #80 Closed cases current-page CSV (issue-80-closed-csv-1110)

Research disposition: executed. Planning Readiness: Ready.
This file began as a stub written before the research-open witness (seq 2); the findings below were added after it.

## Scope

* Branch feat/demo-closed-page-csv-80-1110 from main fe59ef56a0084dd975fd7e5c342670bb8f788fb0, target main, Refs #80 only.
* Admitted initial slice: GET /api/closed-cases.csv plus native "Download this page for Excel" anchor on #/closed, consuming the exact progress.closed_cases(store, user, query) read.
* Owner DEMO FOCUSED tier. No push, PR, rebase, merge or GitHub edit.

## Lineage check (stop condition)

* Admission JSON: issue OPEN, 13 comments read in full, with the 2026-11-10 refill. Comments cover import/export history, form-schema CSV and its form-screen link (r8/r9), storage holds and Docker headroom. None names a Closed cases exporter attempt, failure or ownership.
* `git log --all -S"closed-cases.csv"` returned nothing; `git grep` for `closed-cases.csv` in the pinned tree returned nothing; `progress.js` has zero `download`/`.csv` matches. No worktree branch names it.
* Conclusion: initial, previously unprovided consumer. No STOP. The UNKNOWN old #80 corrective balance is not reset or consumed, and no automatic post-review correction follows.

## Source findings (pinned head)

* `progress.py` `closed_cases(store, user, query)`: `require_staff`, manager-only (`MANAGER_ROLES`), `parameters(query, {start,end,status,team,q,page,limit})` rejects unknown and repeated keys, `day` dates, `DateRangeError` when start is after end, page 1..1e9, limit 1..100 (default 20), `q` at most 200 characters. Candidates are closed and `synthetic(case)`; latest observed closure from `lifecycle(case)`; unknown closure excluded when either date is set; sorted by id; page clamped to the last page. Row keys: id, resident, address, town, postcode, hazard (bool), status, team, closed_on (ISO or None). Result also has total, page, pages, limit, facets, unknown_closure_dates.
* `server.py`: `get_kind("/api/closed-cases")` is `"cases"`, other unmapped paths are `"unknown"`. `do_GET` order: 401 without a user, `projection.allowed` 403, `LIST_EXPORTS`, then the `/api/progress`/`/api/closed-cases` block mapping `DateRangeError` to 400 with `reasons.fields`, `ValueError` to 400, `PermissionError` to 403.
* `core/list_export.py`: `safe_cell` (None to empty, bool to Yes/No, formula prefixes `= + - @ TAB CR` get an apostrophe) and `to_csv`, which writes no header for zero rows. A fixed-column encoder is therefore local to progress.py; the shared exporter is unchanged.
* `/api/cases.csv?report=progress` is a different dispatch over `core.progress.report` with other parameters. It stays unchanged.
* `web/progress.js` `closed()` uses `load()`, which returns data only on success. `values = query()` is the hash query; the filter form preserves `limit`.
* Tests: `test_progress_dashboard.py` has the synthetic fixture (ZF-1 closed, reopened then accepted 2026-10-07; ZF-3 Withdrawn 2026-10-04; ZF-4 unknown closure; ZF-5 unmarked and excluded), an `archive(**values)` helper, Store and Sqlite subclasses and an HTTP test. `test_role_endpoint_inventory.py` requires every server route string in `GET_ENDPOINTS`. `checks/progress_browser_check.py` runs the real server on a 24-closed-case fixture and needs the pinned axe asset.

## Prospective baseline (executed before any edit)

Owned venv `/tmp/ama-80-closed-venv-1110`: mypy 2.4.0, ruff 0.17.1, playwright 1.64.0, editable core, agents and api from this worktree (origins verified).

* Focused tests at the pinned head: test_progress_dashboard 45 OK, test_list_export_api 11 OK, test_role_endpoint_inventory 23 OK (`baseline-tests.log` in the root evidence folder).
* No link consumer: `grep -ci "download\|\.csv" progress.js` is 0.
* No CSV consumer: a live synthetic HTTP probe (`baseline-probe.log`) observed anonymous GET /api/closed-cases.csv as 401 JSON and manager Pam as 403 JSON ("Your role does not include this.") with no Content-Disposition, while the JSON path returned 200. The statuses were observed, not predicted; the path has no successful mapped CSV response.

## #96 source ownership comparison

`git diff fe59ef56..eaf93023 -- server.py` in worktree issue-96-held-download-1110 has hunks at the `form_export` import (line 17), the `held_download_enabled` helper (about line 51), the forms dispatch condition (about line 541) and the held-export handling in `_forms` (about line 1132). This work edits only `get_kind` (about line 188) and the progress/closed dispatch (about line 476), so no line is shared. #96 changes the last `GET_ENDPOINTS` line and adds a test near line 88 of the inventory test; this work edits the `/api/closed-cases` line and adds its own test elsewhere. A `git merge-tree` check against eaf93023 runs after the commit. #96 source is not edited. #153 is in `role-screens.js`, not `progress.js`.

## Decisions fed to Plan

* The CSV route reuses the JSON read and JSON error handling exactly; an attachment is sent only for a successful read.
* Fixed nine-column allowlist; blank closed_on stays blank (unknown, never inferred); booleans render Yes/No via `safe_cell`.
* The link is built from the current query with page and limit set from the response (the normalized page) and appears only after `load()` succeeds.
* No Store, SqlStore, importer, exception register, core lifecycle or schema change.

## Residual limits

SQLite and in-process HTTP only; no SQL Server. No human assistive-technology, WCAG or live acceptance. Closed does not mean works completed or approved. The web-design-guidelines source was fetched on 2026-11-10 before web edits; the design-taste skills are for public pages and are not applied to this dashboard link.
