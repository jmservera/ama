# Research: issue 104 first unmet engineering criterion

* Task: issue-104-live-r2. Disposition: executed (reuses docs/reference/research/issue-104-epic-audit-live-2026-11-18.md).
* Epic 104 unticked criteria: #440 checkpoint (owner decision, not engineering), all children closed or deferred (owner decision).
* First child criterion closable by engineering: #107 criterion "Independent SQL connection/worker and race tests ... Old images/restarts cannot restore revoked approval". Gap named in the audit: `test_old_image_cannot_reactivate_revoked_release_through_the_change_path` only runs on SQLite; no actual SQL Server case.
* Plan: add an MSSQL subclass of the restart/revocation tests using `MssqlFixture` (local disposable service only) in src/api/tests/test_assistant_restart_non_replenishment.py, run against a throwaway local container.
* Planning Readiness: Ready.
