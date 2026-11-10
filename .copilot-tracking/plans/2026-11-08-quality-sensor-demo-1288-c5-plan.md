---
title: Quality sensor demo 1288 C5 plan
ms.date: 2026-11-08
---

Written 2026-11-08T21:59Z after the C5 research and before any product or test edit. Refs #1288, #107. No closing claim.

## Phases

* [ ] P1 Red tests first in `src/api/tests/test_quality_sensors.py` (SQLite only); unique logs `/tmp/c5-red-*.txt` with exits.
* [ ] P2 C5-1 guard triggers and v2 marker.
* [ ] P3 C5-2/3/6 `assistant_schedule`, claim-time refresh, stale requeue.
* [ ] P4 C5-4 flag survives same-schedule newer readings.
* [ ] P5 C5-5 consent hold before dispatch (two points).
* [ ] P6 C5-7 as-of and freshness in request and flag; C5-8 future probe.
* [ ] P7 Green light suites, ruff, README, changes, one review, commit.

## Red/green scenarios

* R1 control body home changed with valid marker and index: consent withheld for the home, detail/list/export/sensors projections withheld; legacy v1 marker or missing triggers fail closed; `migrate()` repairs and is idempotent.
* R2 exact A-B-A (Quality and assessment-preparation): A queued, non-sensor change to B, claim A stales, scan B, revert to A; scan, forecast and manual invoke yield runnable work, within the call allowance.
* R3 sustained churn: five arrivals each followed by a claim attempt with no dispatch; one task only; a stable recovery dispatches once; restart (cursor reset) adds nothing; allowance use is 1.
* R4 returned proactive flag, then a same-bucket arrival (also during inference): flag stays `review-suggested` with newer-readings text, no second task, acceptance blocked; a new bucket enqueues fresh work.
* R5 withdrawal between claim and dispatch (barrier around `claim`): provider sees no request. A withdrawal during an already started call is projected withheld.
* R6 scale: 300 historical tasks for one case; scheduling issues only primary-key reads on `assistant_tasks` and the schedule table (statement trace and query plan); deduplication unchanged.
* R7 freshness: request carries `request_as_of` and `fresh`/`stale`/`unknown`; old-only readings are stale in prompt and flag; none is unknown.
* R8 future: 1-day boundary, 2-day and 40-day future rows report `future_dated_excluded` true and are never fresh.

## Critique (executed once, final candidate)

* Verdict: proceed with amendments. Amendment 1: refresh at claim only for proactive tasks and only when `scheduling_signature` is unchanged and the capture still fits the input bound. Amendment 2: stale requeue only while attempts are below the limit. Amendment 3: add the schedule table to both DDL lists (MSSQL unexercised, PENDING). Rejected: a new service or retention programme.

## Gates still pending after C5

* Actual SQL Server (trigger DDL, schedule table, plans), browser/axe, #184 semantic integration, FULL receipt, release and attestation, live walkthrough.
