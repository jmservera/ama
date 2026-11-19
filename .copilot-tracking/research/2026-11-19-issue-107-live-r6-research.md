# Research: issue #107 sixth live pass (2026-11-19)

Disposition: reused. Planning Readiness: Ready (no build target).

Unticked criteria (`gh issue view 107`): (1) independent SQL worker and race tests for material mismatches, revocation and restart; (2) approved exercise record permits bounded proposals only, with delivered-build real AI, SQL and Azure acceptance.

Evidence at HEAD 7ea3a1ff6:

* `src/api/tests/test_assistant_restart_non_replenishment.py` holds the composite old-image and material-mismatch tests plus the actual-SQL classes. Re-run this session on SQLite: Ran 30, OK, skipped 15 (actual-SQL classes need `ZF_TEST_MSSQL=1`).
* `docs/reference/research/issue-107-live-r4-criteria-2026-11-19.md` records 30 tests, 0 skipped, on a disposable local SQL Server 2022 container.
* Not provable for the demo: old-image behaviour from the private ACR against Azure SQL (owner scoped out production changes); an approved release record (OQ-017 holders unappointed, real AI not authorised).

Conclusion: no further code or test can add proof. Criterion 1 stays proven on local actual SQL; criterion 2 needs a human appointment and real-AI authority.
