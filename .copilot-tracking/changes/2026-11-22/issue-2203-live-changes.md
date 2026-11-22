# Issue 2203 changes (2026-11-22)

Status: complete. Refs #2203. Not pushed, no PR.

## Files

* `src/core/src/zava_forward/core/assistants.py`: `_read_connection()` added; `forecast()` reads on a lock-free connection instead of `transaction()`.
* `src/api/tests/test_assistants.py`: `test_forecast_does_not_hold_the_write_lock` (fails with "locked" without the fix, passes with it).
* `docs/capstone/demo/runbook.md`: new "Live Demo Status (2026-11-22)" section, 21 November section kept as history, Quality scope row relabelled, anchors and `ms.date` updated; the `### The five homes` table is untouched.
* `docs/reference/research/issue-2203-runbook-live-2026-11-22.md` and `issue-2203-live-2026-11-22/` (probe scripts, results, screenshots).
* `docs/reference/README.md`, `docs/reference/log.md`: index and log.
* `.copilot-tracking/` research, critique, plan, details, changes, review, state for 2026-11-22.

## Validation

* `tests.test_assistants`: 142 OK, 61 skipped; `test_quality_sensors` and `_e2`: 271 OK, 133 skipped.
* `test_generated_dataset` (five-home parser): OK.
* `ruff check` on `assistants.py`: pass. `src/api` mypy: pass. `src/core` mypy: 3 errors, identical without the change (opentelemetry stubs, unused ignore in `device_provision.py`).
* Runbook and note relative links and anchors: scripted check, none broken.
* Sloptrim detector not found in this environment; prose written to the contract by hand, score not measured.
* Not run: `rpi-checks.py --all` (coordinator runs the gate).

## Tier

FULL, because `src/core` changed. Basis: source change in a store-access path used on MSSQL. Deployment is not done and not authorised for this worker, so the live app still shows the defect.

## Defect

`GET /api/assistants/forecast` took about 153 s live; during it `GET /api/map` returned 500 after 15 s. Cause: forecast ran in `transaction()`, which on MSSQL takes the replica-wide exclusive lock with SERIALIZABLE isolation. The fix removes cross-request blocking only; the forecast stays slow. Proven on SQLite only, not on Azure SQL. A link to the earlier "Home sensors unavailable" and chat error events is likely but not proven.

## Per-criterion table

| Criterion | Result | Evidence and reason |
| --- | --- | --- |
| Cohort, cadence, consent mix, resident checkbox, chat routing, charts and operator-triggered AI scope described with dated status | Proven for the runbook text; several live items unproven | Runbook 2026-11-22 section from probes. Cohort 5 stale and 16 withheld; simulator Succeeded every 5 min; checkbox grant and revoke HTTP 200; routing to three helpers; dual-axis chart; `/api/assistants` scope. Unproven: any fresh reading (receiver Failed, #2201, cause unreadable as logs are refused); staff view after a resident grant; employee chat answer; map gauges |
| Stale five-home table replaced or relabelled; links checked | Proven | Table kept as parser fixture, section labelled superseded and historical; scripted link check clean; parser test OK |
| Offline-sensor alert, role proof and hardening status included | Partly proven | Stale alert live on 25 homes; role Retrofit Programme Manager; hardening `enforced` as configuration. Unproven: 24 h offline state (no reading that old), wrong-role denial (one staff account), a container rejecting a write |
| Honest Observed vs Not verified wording | Proven | Every runbook row has both columns; unproven items listed above |
