---
title: Issue 2304 assistants forecast did not answer on live data (Refs #2301, #440, #107)
description: Per-criterion proven or unproven record for issue 2304, with a live reproduction, a statement-count profile, the fix and the live re-check that could not be made
ms.date: 2026-11-23
ms.topic: reference
---

Scope: synthetic demo, desktop only. Owner decision 2026-11-18 authorises live Azure in resource group `ama` and waives billing reconciliation, DPO and Legal approval and person-run assistive technology testing. The live probe is read-only; no Azure resource was created or changed, so nothing needed deletion. Sign-in values were read at runtime by the probe and never printed; the stored JSON was checked for their absence. Tier: FULL for the `src/` change by classification; `rpi-checks.py --all` was not run by this worker, so no full receipt exists.

## Reproduction (live, revision 0000055)

Signed in as the test employee, `GET /api/assistants/forecast` (default period) ended at the probe's 200 second timeout with no response, while `/api/assistants` answered in 0.7 s and `/api/exceptions` in 0.2 s. Evidence: [live_probe_before.json](./issue-2304-live-2026-11-23/live_probe_before.json), script [live_probe.py](./issue-2304-live-2026-11-23/live_probe.py). The request was authorised (a refusal would be immediate), so the time is spent in the forecast itself.

## Where the time goes

`Assistants.forecast` evaluated every open case for each of five assistants with `snapshot` and `_due`, each issuing several statements (procurement meta, schedule slot, task by id, release and continuity records, adoption history, and for Quality the per-home sensor readings and consent index). A counting connection on an equivalent SQLite-backed store gave:

| Open cases | Statements before | Statements after |
| --- | --- | --- |
| seed set | 422 | 20 |
| seed set plus 40 | 3622 | 20 |

About 80 statements per extra open case before, none after; outputs were identical on both sets. On Azure SQL each statement is a round trip on one connection, so 443 open cases mean tens of thousands of round trips. The live statement trace itself was not captured: SQL has public access disabled and the host cannot reach it, so the cause is proven on the equivalent run and by the live symptom, not by a live trace.

## Fix

* `src/core/src/zava_forward/core/forecast_reads.py` (new): a read-through view of the forecast connection. Repeated reads are answered once; schedule slots, tasks (by primary key in chunks), adoption history (newest five by assistant and case, bounded) and per-home sensor reads come from a fixed number of bulk reads. A failed probe repeats its failure, so Quality still reports unavailable as before.
* `Assistants.forecast` uses it, with a 10 second budget (`FORECAST_BUDGET_SECONDS`). An overrun raises `ForecastTimeout`.
* `src/api/src/zava_forward/api/server.py` maps `ForecastTimeout` to HTTP 503 with `state: unavailable`, a plain message, "nothing was changed", and `Retry-After: 30`.
* `test_quality_sensors.py`: the history-scan guard now also allows an explicit `WHERE id IN` primary key read.

## Tests

* `test_assistants.ForecastStatements.test_statement_count_does_not_grow_with_open_cases` proves equal statement counts for the seed set and the seed set plus 40 open cases while the forecast totals grow.
* `test_forecast_names_an_unavailable_state_when_the_budget_is_spent` proves the named state.
* `test_assistants`, `test_quality_sensors` and `test_quality_sensors_e2`: 419 tests, OK (196 skipped for missing SQL Server), run sequentially. `ruff` clean and `mypy` unchanged against the baseline in `src/core` (3 existing import errors in other files) and clean in `src/api`.

## Per-criterion status

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Profile the live or an equivalent SQL-backed run and record where the time goes | Proven on an equivalent run; live trace unproven | Counting-connection table above; live symptom in `live_probe_before.json`; SQL unreachable from this host |
| 2 | Forecast answers within a stated bound (propose 10 s) on the demo data set, or returns a named state, never a silent hang | Proven in tests only | 10 s budget and named 503 state tested; the 443-case live timing is unproven (see 4) |
| 3 | A counting-connection test proves statements do not grow per open case | Proven | `test_statement_count_does_not_grow_with_open_cases` |
| 4 | Live re-check after deployment with the elapsed time recorded | Unproven | `az acr build` to `crcutovertestrzsrg` failed at registry login with 403 (run `dby`): the Premium registry has public access disabled and changing its network posture is out of scope; the revision was not changed |

## Limits

* The live data set may add per-home sensor reads for homes that have readings; those stay per-home reads, bounded by homes with data, not by open cases.
* The 10 second budget protects the client, not the database: a slow SQL server still ends in the named 503 state.
* The worker set the source edits aside once so the plan and implement-start witness calls saw a clean source tree; the witness still noted earlier drafting.
