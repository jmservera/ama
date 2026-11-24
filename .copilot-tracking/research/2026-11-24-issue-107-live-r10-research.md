# Issue 107 live r10 research (2026-11-24)

Goal: explain why repeated live re-verification of #107 (and #1830, #435) yields no new proof, then name the missing code.

## Opening

* Unticked criteria: (1) independent SQL connection/worker and race tests for material mismatches, revocation and restart; (2) matching approved exercise record, delivered-build acceptance.
* Prior passes r2 to r9 re-ran the same unit classes and read-only live probes. Hypothesis: the evidence class is saturated, so a re-run cannot add proof; only new test coverage or a new evidence class can.
* Candidate gap: process-level (separate OS process) material-mismatch tests cover only policy, prompt and permissions variations; model, provenance and schema triggers have no process-level race test.

## Findings

* Research disposition: executed. Planning Readiness: Ready.
* Root cause 1 (evidence-class saturation): the criterion text names tests; those exist and pass (99 tests, 24 SQL Server classes skip without `ZF_TEST_MSSQL=1`, which CI sets and a local docker SQL Server 2022 satisfies). Every pass r2 to r9 re-ran the same classes plus read-only 401 probes, so a re-run cannot move the checkbox: the criterion is not closed by a repeated run but by new coverage or a new evidence class.
* Root cause 2 (the SQL fixture refuses Azure SQL by design): `MssqlFixture.setUp` raises unless `ZF_SQL_SERVER` is localhost, 127.0.0.1 or sql. Independent connections therefore cannot be proven against the live database from tests; live probes are limited to unauthenticated 401s, which prove nothing about revocation or restart.
* Root cause 3 (the compound criterion): the second unticked criterion needs a named approver and residual-risk holder (OQ-017); live re-verification cannot create one without fabricating authority.
* #1830 and #435 repeat the pattern: their unticked items need an external statement (mentor, owner, hosted CI on a pushed head) that a local rerun cannot supply.
* Real code gap: the OS-process race harness (`assistant_process_worker.py` VARIATIONS) varies only policy, prompt and permissions. The in-process separate-worker class (`MaterialMismatch.variations`) covers ten triggers. Model version, data and provenance mismatches have no separate-process test, on SQLite or SQL Server.
* Live probe: revision `ca-cutover-test-demo-api--0000060` (2026-11-24T08:11:30Z), Healthy; unauthenticated releases and health return 401. See `.copilot-tracking/evidence/107-live/live-probe-20261124T083552Z.txt`.
