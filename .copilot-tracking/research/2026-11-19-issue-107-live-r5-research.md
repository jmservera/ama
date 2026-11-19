# Research: issue #107 fifth live pass (2026-11-19)

Disposition: reused. Planning Readiness: Ready (no build target).

Brief: implement the first unticked criterion that can be proven or built for the demo; otherwise state so and stop.

Unticked criteria in the issue (read with `gh issue view 107`):

1. Independent SQL connection/worker and race tests cover material mismatches, revocation and restart; old images and restarts cannot restore revoked approval or replenish finite allowances.
2. A matching approved exercise record permits bounded proposals only; delivered-build acceptance needs version-linked real AI, actual SQL and Azure evidence under CON-009/AC-057.

Evidence reused from HEAD (adb10ae6d lineage, includes the 2026-11-19 r4 pass):

* `src/api/tests/test_assistant_restart_non_replenishment.py` already holds the composite old-image/material-mismatch test and `MssqlAllowance`/`MssqlMaterialMismatch` classes. Re-run this session on SQLite: 30 tests, OK, 15 skipped (the actual-SQL classes need `ZF_TEST_MSSQL=1`).
* `docs/reference/research/issue-107-live-r4-criteria-2026-11-19.md` records the same file passing 30 tests with 0 skipped on a disposable local SQL Server 2022 container.
* Remaining gaps: old-image behaviour against Azure SQL and a pulled registry image (ACR is private; not needed for the demo), and an approved release record (OQ-017 holders unappointed; real AI not authorised). Neither is buildable as code or test.

Conclusion: no code or test can add proof; criterion 1 stays proven on local actual SQL, criterion 2 needs a human appointment and real-AI authority.
