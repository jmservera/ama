---
title: Quality sensor demo 1288 C7 plan
ms.date: 2026-11-08
---

Written 2026-11-08T23:00Z after the C7 research and before any product or test edit. Refs #1288, #107. No closing claim.

## Phases

* [ ] P1 Red tests (SQLite, loopback transport) in `src/api/tests/test_quality_sensors.py`; logs `/tmp/c7-red-*.txt`.
* [ ] P2 C7-1/2/7 gate table, `ai_consumption` gate context, gated connection in `ai.py`, `assistants.call`, per-home `configure`.
* [ ] P3 C7-3/8/4 schema migration of C5 tables, `dispatched` column and index, bounded adoption by own signature.
* [ ] P4 C7-5/6 coalescing, serviced status from frozen dispatch.
* [ ] P5 C7-10 content comparison, UI wording (web guidelines refreshed before edit and before review).
* [ ] P6 C7-9 backend-neutral guard test; Ruff check and format on the changed non-excluded test file.
* [ ] P7 Green runs, changes, one original review, commit.

## Red/green scenarios (all synthetic)

* S1 loopback server counts request bytes. Gate barrier: consent granted, a barrier after the check and before the first byte, second connection withdraws. Red: bytes arrive. Green: withdrawal waits or the gate refuses; zero request bytes after a withdrawal that committed first.
* S2 hold expiry: the transport stalls past `expires_at`; withdrawal commits (expired row ignored); the local send-by deadline refuses, zero bytes. A stall before the gate (provider preparation past expiry) is harmless: the gate runs after it.
* S3 overlapping attempts: fence 1 times out and keeps running, fence 2 retries; both rows exist; fence 1 finishing removes only its row; withdrawal still waits for fence 2.
* S4 unrelated home: a live row for home A does not delay withdrawal for home B; same-home, batch replacement and sensor-to-home move do wait; policy change waits for all.
* S5 genuine C5 `assistant_schedule` DDL with rows (and pre-C7 `assistant_tasks` without `dispatched`): migrate adds columns, keeps rows, is idempotent, then manual invoke, forecast, scan, claim and restart succeed. A forced migration failure reports schema-unavailable and sends nothing.
* S6 legacy assessment and funding A to B with no missing-field gap: first scan enqueues exactly one new task; same-bucket Quality still throttles; release or epoch change enqueues.
* S7 sustained churn after exhaustion: many scan, arrival, claim cycles create a bounded number of rows and no provider call; truthful reason set; after a quiet interval one recovery task dispatches; restart keeps the bound.
* S8 late manual request during a proactive call: flag stays proactive; next same-bucket reading does not enqueue another autonomous call; manual-before-claim still occupies a non-Quality slot.
* S9 adoption reads at most five bodies (statement recorder) for a case with many historical tasks; newest by `dispatched`.
* S10 changed same-ID row value reports changed; extra uncited row reports match plus an additional count; no current capture reports unknown.
* S11 guard regression uses the backend's trigger name and count; MSSQL variants stay skipped.
* S12 Ruff check and format pass on `tests/test_quality_sensors.py`.
