---
title: Issue 188 local handover demo research
ms.date: 2026-11-01
---

* Task: `issue-188-local-handover-demo`; branch `feat/sensor-ingestion-store`; research disposition `executed`; Planning Readiness `Ready`.

## Question

What is left of #188 (live and backfill series queryable together, no discontinuity at handover, idempotent window re-run) after #587 and #645, and what is the smallest demo-ready slice?

## Evidence

* Core report `synthetic/sensor_consistency.py` (193 lines) and operator verifier `api/sensor_handover_verify.py` (`run`, `main`, `--replay-check`, exit 0/1/2) are on main.
* `src/api/tests/test_sensor_consistency.py` proves the composed path with actual CSV bytes, SDK `EventData` decode, #110 consumer, joint per-home query, zero-tolerance report and reopened whole-window replay. Re-run this session: 38 tests OK (SQLite; `ZF_SENSOR_MSSQL=1` selects local SQL Server through `checks/sensor_sql_check.py`).
* `src/api/README.md` ("Operator handover check for a live store") states the live Hub plus Azure SQL run remains owner-gated evidence.
* Dependencies #110, #183 and #186 and the stream/consumer code are present; #184 (live Hub streaming) is open and #110 has unmet infra criteria.
* No single command builds a store, ingests backfill plus streamed suffix, and prints the verifier verdict. The proof exists only inside a unit test, so a reviewer cannot run it as a demo.

## Acceptance criteria status (offline evidence only)

| Criterion | Offline evidence | Open |
| --- | --- | --- |
| Queryable together per home ID | joint ordered query, 2 homes, 24 readings | Azure SQL |
| No discontinuity within declared tolerance | zero-tolerance report passes; negative controls fail | live Hub data |
| Re-run idempotent | replay receipts, unchanged series, `--replay-check` | Azure SQL |

## Selected approach

Add `sensor_handover_demo.py` in `src/api/checks/`: builds a temporary SQLite store with constructed climate (same fixtures as the tests), writes the backfill, ingests the prefix, decodes and ingests the streamed suffix, then invokes the verifier with `--replay-check` and prints JSON. Keep it constructed and local; no cloud, no secrets. The #188 acceptance remains partly unproven, so the PR uses `Refs #188`.

## Rejected

* Azure SQL or Hub execution: owner-gated, not authorised here.
* Changing the verifier or core report: already reviewed and merged.
