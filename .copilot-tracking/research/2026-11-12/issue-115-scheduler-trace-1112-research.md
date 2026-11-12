# Issue 115 scheduler trace research (2026-11-12, 1112)

* Task: `issue-115-scheduler-trace-1112`. Disposition: executed. Planning Readiness: Ready (one bounded slice).
* Pin: `origin/main` = `cd81888e4a81cf4c712d50b357ca900fd5c8c06b`, branch `research/ledger-scheduler-trace-115-1112`, worktree `issue-115-scheduler-trace-1112`. Primary checkout untouched.
* Authority: jmservera/ama#115 comment 6653800108 (2026-11-05) directs scheduler wiring and local trigger/error coverage to be verified as engineering, not blanket human-blocked. Owner retention duration, irreversible lock and second-person reconciliation stay distinct and unmet.
* Prior RPI read: 2026-10-15 base, 2026-10-18 anchor, 2026-11-03 r1, 2026-11-04 r2. r2 concluded "no further code slice"; it predates the 2026-11-05 comment and did not trace the trigger-to-exit path. `git log` since 2026-11-05 shows no commit touching `digest_blob.py`, the ledger job, or the ledger alerts, so the scheduler engineering was not delivered after the comment.
* PR #404, #916, #1156 (publisher, verifier, reconciliation) are not duplicated.

## Trace of one scheduled trigger: `ledgerVerify` job

| Step | Current anchor | Finding |
| --- | --- | --- |
| Trigger | `infra/modules/containerapps.bicep:428-453`, cron `0 2 * * *`, `replicaRetryLimit: 0`, `replicaTimeout: 900` | Wired; command `python -m zava_forward.orchestrator.digest_blob --publish` pinned by `infra/tests/test_bicep_policy.py:443`. |
| Entry | `digest_blob.py` `main()` | Publishes then verifies. Exit 2 when `ZF_DIGEST_ACCOUNT_URL` unset; exit 1 plus `LEDGER_DIGEST_ALERT` on mismatch or `DocumentStoreError`; exit 0 plus `LEDGER_DIGEST_OK`. Tested in `src/orchestrator/tests/test_digest_blob.py`. |
| Alert | `infra/main.bicep:586-635` | Immediate alert (hourly) matches only `LEDGER_DIGEST_ALERT`; its description claims "or the job run failed". Fallback alert fires only when no `LEDGER_DIGEST_OK` for 26 hours. |
| Failed-execution alert | `infra/modules/operationalMonitoring.bicep` | Candidate, disabled unless separately approved; not an acceptance path. |

## Demonstrated gap (existing scope, criterion 2)

* `main()` calls `open_store(env)` outside any handler and catches only `DocumentStoreError` around publish and verify. With `ZF_STORE=mssql`, SQL connection or query errors (not `DocumentStoreError`; the class is defined in `src/core/src/zava_forward/core/documents.py:34`) propagate as a traceback: exit 1 but no `LEDGER_DIGEST_ALERT` and no `LEDGER_DIGEST_OK`.
* Consequence: the hourly alert whose description promises job-failure coverage cannot fire; only the 26-hour missing-success alert detects it. No existing test covers an unexpected exception from the store.
* Minimal failing-first case: `main()` with a store whose `audit_entries` (and a case where opening raises) raises a non-`DocumentStoreError` must return 1 and print `ALERT_MARKER`, never `OK_MARKER`. Fails on current source (exception propagates).
* Secondary gap: no test binds the literal markers in `infra/main.bicep` alert queries to `digest_blob.ALERT_MARKER` and `OK_MARKER`; renaming either would silently disable alerting. Local static test, in scope.

## Boundaries

* Static source and local synthetic tests only. No hosted alert, retention duration, lock, second-person reconciliation or whole-issue acceptance claim. Both #115 criteria remain unticked.
* Validation tier: focused (non-gate, orchestrator tests plus a Bicep-policy marker test). If Bicep compilation needs a missing tool the infra test is reported blocked rather than substituted.
