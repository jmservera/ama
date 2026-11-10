<!-- markdownlint-disable-file -->
# Review: issue 1288 merged-main SQL contract verification

Written 2026-11-09T23:29Z. One review of the finished observation. Findings route to later work; no further review or implementation inside this task. Refs #1288 only.

## Outcome by contract

| Contract | Status | Basis |
| --- | --- | --- |
| Refusal event commits before the raise and is visible on a fresh connection (`fence_send`) | Proven at the merged source on SQL Server | H2a and H2b above, one run |
| Declined after expiry before meter, token and socket; slot and debit accounting after refusal | Proven for the exercised path (direct ticket and real `Ai.evidence`); slot release is in-process only | H2a/H2b |
| Sensor and flag source-ID persistence | Proven historically at `5827ebede` (unchanged `sensor_*`, `sqlstore`, `mssqlstore`) and refreshed on the merged tree by the existing restart-covering tests, which pass | 30 existing tests ok |
| Role projection (Retrofit Programme Manager and Quality Inspector allowed, others refused) | Existing `test_sensors_api_role_matrix` passes on SQL Server | existing test |
| Durable authorised sensor IDs and flag IDs identical across a fresh service over the same database | NOT proven by this run: H0 failed on flag status, cause unestablished | harness H0 |
| Duplicate/stale rejection | Existing `test_stale_proposal_is_not_a_flag` and A-B-A requeue tests pass on SQL Server | existing tests |

## Findings

1. Medium: H0 is inconclusive. Smallest repro is the external harness test; requirement is a fresh `Assistants` over the same SQL database that reports the same flag status and source IDs. Current owner is this verification (harness context), not production code. A rerun needs a new SQL admission with the restarted service built with the same release context as the fixture; it was outside the one authorised exercise.
2. Low: hosted CI does not run any Quality MSSQL class, so these contracts remain local-only evidence.
3. Informational: the lane is SQLite by design; the working store was SQL Server in H2b.

No source defect confirmed. No fake success, no waived skip. Whole #1288, #440 and the live-model criteria remain open.
