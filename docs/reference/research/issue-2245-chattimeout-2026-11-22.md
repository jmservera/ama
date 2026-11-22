---
title: Issue 2245 employee chat ask with no response within 120 s (2026-11-22)
description: Live probes of the demo employee chat ask latency, the write-lock explanation for stalls and 500s, the meter seeding fix and a per-criterion table for issue 2245
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop 1440x900 only, resource group `ama`, owner decisions of 2026-11-18. Sign-in values were read from the owner files at run time; each probe asserts that they are absent from its saved output. No Azure change was made and no throwaway resource was created. Probes and JSON results sit in [issue-2245-chattimeout-2026-11-22/](./issue-2245-chattimeout-2026-11-22/). This follows the [AI answers diagnosis](./issue-2245-live-2026-11-22.md) (open suspension SUS-1).

## What was measured

| Probe | Result |
| --- | --- |
| `probe_ask_latency.py`, revision 0000051, five runs, about 45 timed asks | 3.0 to 4.3 s per ask with no model call; first ask after idle took 56 s, 26 s and 6 s; none reached 120 s |
| Control: asks refused before admission | 3.07 s; hold-path asks about 4.1 s, so the admission and meter step adds about 1 s |
| `probe_ui_first_ask.py`, UI ask 0.4 s after the workbench started loading | answer visible after 6.6 s; slowest request 6.2 s |
| `healthz_poll.py` every 0.5 s during asks | 121 polls, no stall in the warm run; after 7 min idle (revision 0000052) 3 of 122 polls slow, worst 14.8 s |
| Same run after idle | one `POST .../ask` returned HTTP 500 after 19.4 s; container log shows `exc=ProgrammingError` |
| Direct Azure OpenAI call from the test principal | HTTP 401 PermissionDenied (no data action), so model latency cannot be timed from here |
| App Insights and Log Analytics queries | `InsufficientAccessError`; only the container console log was readable |

## Cause by candidate

* Azure OpenAI latency: excluded for the current state. Every ask answers `AI answers are on hold because an open suspension covers AI work, so no model was called`; the model is never reached. Not measurable when the hold is lifted.
* Suspension hold path: not the stall. It returns in about 4 s; its only added cost is the meter seeding below.
* Worker hang: not seen. `restartCount` is 0 and `/healthz` recovers after the stalls.
* SQL write lock: supported by code. `BEGIN IMMEDIATE` takes `sp_getapplock ... @LockTimeout = 15000` and `THROW 50002` on timeout (`mssqlstore.py`). The THROW appears as `ProgrammingError`, as in the 500s at 17:51, 18:01 and 18:48, and 19.4 s is about the 15 s lock wait plus a 4 s ask. The API holds `dblock` while waiting, and `/healthz` needs it, so probes disconnect during the wait. One ask runs several write transactions in sequence, so a busy database can compound the wait toward 120 s. Which other writer held the lock cannot be read without telemetry.
* Avoidable lock traffic: on the model path `chat_admission` calls `chat_demo_meter.ensure` before and after each call. Each call ran `price` and `authorize`, each opening a new SQL connection, taking the exclusive lock and rereading the whole ledger, even when the day's records already existed.

## Fix

`chat_demo_meter.ensure` now records the seeded day, configuration and limits on the ledger and returns early on a repeat. Failures are not cached, and a new day, configuration or limit reseeds. This removes two exclusive-lock transactions and two connection set-ups from every hold-path ask after the first, and four of each from every model-path ask (the check runs before and after the call). Suspension, lock timeout and release controls are unchanged. The regression test `test_repeated_admission_seeds_the_ledger_once_and_reseeds_on_new_settings` in `src/api/tests/test_continuity.py` fails without the change (3 price and 3 authorize calls instead of 1 and 1) and passes with it. The fix is not deployed; the live latency effect is unmeasured.

## Per-criterion table for issue 2245

| Criterion | Status | Evidence |
| --- | --- | --- |
| Reproduce the ask with no response within 120 s | Unproven | Five runs, no ask above 56 s; 500 after 19.4 s once |
| Find the cause among model, hold, worker, SQL | Partly proven | Model and hold excluded; worker excluded; SQL write-lock wait supported by code and the 19.4 s ProgrammingError, writer identity unknown |
| Fix the smallest cause with a regression test | Proven for the avoidable lock traffic only | Code change and failing-then-passing test; not deployed, the 120 s case is not shown fixed |
| First thread-create 500 cause | Unproven | Same `ProgrammingError` class; not reproduced in this run |
| Model call visible when the skill can use it, or banner states rules-only | Proven earlier (parent note, PR 2249); lifting SUS-1 needs an owner decision | [AI answers diagnosis](./issue-2245-live-2026-11-22.md) |
| Which skills and routes call the model | Proven earlier | Same note: rules-first intents never call the model |

## Open items

* Owner: grant read access to Log Analytics or App Insights, or provide a trace, so the lock holder during a stall can be named.
* Owner decision to close SUS-1 before the model path can be timed against a deployment.
