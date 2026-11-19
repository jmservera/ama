# Research: issue #107 sixth live pass (2026-11-19)

Disposition: reused (r4 and r5 evidence at HEAD 7ea3a1ff6), with a fresh re-run. Planning Readiness: Ready (no build target expected).

Unticked criteria: (1) independent SQL connection/worker and race tests for material mismatches, revocation and restart; (2) matching approved exercise record permits bounded proposals only, with delivered-build real AI, SQL and Azure evidence.

Findings recorded below once the targeted tests have been re-run.

## Findings

* Re-run on SQLite from `src/api`: `python3 -m unittest tests.test_assistant_restart_non_replenishment tests.test_assistant_release -q` gave 95 tests, OK, 22 skipped (the actual-SQL classes need `ZF_TEST_MSSQL=1`), 290 s.
* The process-race, revocation, restart, non-replenishment and composite old-image/material-mismatch tests exist in both files and cover policy, prompt and permission changes (`check_changed_binding_process`). The actual-SQL run is recorded in `docs/reference/research/issue-107-live-r4-criteria-2026-11-19.md` (30 tests, 0 skipped on local SQL Server 2022).
* Criterion 1 residue: Azure SQL and a pulled registry image. Neither is needed for the demo; no missing test case was found.
* Criterion 2 needs an approved release record (OQ-017 holders unappointed, a human step) and real AI authority. Not buildable as code.

Conclusion: nothing remains that can be built or proven for the demo beyond the recorded evidence. Stop, no source change.
