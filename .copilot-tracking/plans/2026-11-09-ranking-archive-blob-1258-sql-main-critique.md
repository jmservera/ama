# Issue 1258 SQL main integration critique (2026-11-09)

One critique (rubber-duck), executed before merge and validation. Verdict: Revise. Never repeated. Three findings, all compatible and applied directly as an additive section below the plan's original text (the plan text is not rewritten).

* PC-SM-1 Blocking, applied: selector commands must put each project's `tests` directory on `PYTHONPATH` (core: `PYTHONPATH=tests`; API: `PYTHONPATH=tests:../core/tests:../agents/tests`). Without it all six named modules failed to import.
* PC-SM-2 Significant, applied: `ruff` already reports errors in `src/api/tests/test_ranking_publication_wiring.py` (10 at critique time, branch-side file, not part of main's delta). c5 linted only the adapter, core test and fixture. Disposition: run ruff on the changed files and record the result; classify any finding in a file unchanged by the merge as pre-existing on `52f9b61b`, confirm by running ruff on that file at `52f9b61b`, report it as an unclosed lint finding, and do not edit source (no cycle, no manual source authority). Findings in main-side files are merge-introduced and are stop conditions.
* PC-SM-3 Significant, applied: unset `ZF_RESIDENT_MSSQL`, `ZF_RESIDENT_AZURE_TEST`, `ZF_RANKING_ARCHIVE` and any `ZF_*MSSQL*`/connection variable for every validation command, so SQL Server, Azure and real archive paths cannot be opted in by an inherited shell.

Verified by the critique: the 12-path main delta and the clean merge-tree forecast match the research; `test_case_journey` has no ranking publish reference; wiring tests use mocked Blob publication with SQLite; real SQL Server stays untested, as stated.
