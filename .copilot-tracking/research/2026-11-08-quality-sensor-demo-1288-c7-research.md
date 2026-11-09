---
title: Quality sensor demo 1288 C7 research
ms.date: 2026-11-08
---

Written 2026-11-08T23:00Z, before any product or test edit. Refs #1288, #107. Base: frozen `4a1b42b8` / tree `edc8a286`, tracked clean (verified). Research disposition: executed (source reading plus the independent C6 report). Planning readiness: Ready.

## Authority and limits

* Owner authorised two bounded cycles after C5. C6 is done; this C7 is the last. No C8 exists. Consent, safety, independent review, release and live gates are not waived. FULL tier stays (SQL consent/control, security-sensitive projection).
* Light SQLite, loopback-transport and static tests on synthetic data only. No Docker, SQL Server, browser, FULL, real provider call, push, PR, cleanup, stash or rebase. #184 and #1292 overlap `assistants.py` and `sensor_consumer.py`; ordering belongs to the coordinator.

## Independent C6 findings, verified against `4a1b42b8`

Source: `/home/azureuser/.copilot/session-state/f751a4dc-045d-479c-8035-8588858e3b08/files/review-1288-4a1b-c6-functional/functional-findings.json` (request changes; findings 1-8 High, 9-10 Medium). All ten confirmed by reading the committed code.

* C7-1 High, expiry: `call()` writes a hold of timeout plus 5 s and then prepares the request (`reserve`, token, `dispatch_check`) before `urlopen`. Nothing re-authorises at the transport. A thread stalled past the expiry lets `configure` commit a withdrawal and the thread still sends. Confirmed in `assistants.py:1309-1331` and `ai.py:117`. The C6 test releases the mock inside the window.
* C7-2 High, fence: the hold primary key is (home, task) and cleanup deletes by (home, task). A retried attempt replaces the older one's hold, and the older attempt's `finally` deletes the newer hold. Confirmed.
* C7-3 High, C5 upgrade: C6 changed `CREATE TABLE IF NOT EXISTS assistant_schedule` only. A persisted C5 table has no `replaced` column and `migrate` never alters it, so `_occupy` and claim fail. Confirmed; the C6 legacy test builds its own new table.
* C7-4 High, adoption: `_adopt` adopts a prior task only when its coarse signature equals the current one, so a gap-free assessment or funding change A to B writes an empty slot, `_due` sees `scoped` false and never enqueues. Confirmed.
* C7-5 High, exhaustion: `claim` stops replacing after three, but the slot then points at a stale zero-attempt task, so `_due` reports not known and every scan creates another exact task. Confirmed by reading `_due`.
* C7-6 High, late manual: `_due` ORs `manual_requested` with the frozen dispatch trigger. A person's request during a proactive call makes the serviced slot look manual, so the next same-bucket reading enqueues another autonomous call. Confirmed.
* C7-7 High, global hold: `configure` counts every live hold. One home's provider call blocks another home's withdrawal. Confirmed in `sensor_consumer.py:367-400`.
* C7-8 High, adoption read: `fetchall()` then `rows[:20]`; order by `revision` is a mutation count, not dispatch order. All historical bodies of the case are read in the writer transaction. Confirmed.
* C7-9 Medium, SQL Server guard test: inherited regression drops `sensor_consumer_control_guard_upd` (SQLite only) and expects three triggers (SQL Server has one). Confirmed by reading `_schema` and the test.
* C7-10 Medium, comparison: `changed_since_capture` compares key sets only. A corrected row with the same key reports unchanged; an extra uncited row reports changed. Confirmed in `review_flag`.
* Coordinator Ruff: 13 E501 and a formatter failure in `tests/test_quality_sensors.py` (logs `/tmp/verify-1288-c6-quality-ruff-check.txt` and `-format.txt`). Real, in a non-excluded file; fix and run the project's check and format.

## Design research and tradeoffs

C7-1 and C7-2, physical-send ordering. The only honest ordering point is the first application byte. `urllib.request.urlopen` does DNS, connect and TLS before any request bytes, none of which is bounded by the hold. Chosen design:

* A per-attempt durable authorisation row `assistant_dispatch_gate (home_id, task_id, fence, expires_at)`, primary key (home, task, fence). It replaces the C6 hold table (a transient table; the unused C6 table is left in place and ignored, nothing is dropped).
* A dispatch gate callable lives in a context variable in `ai_consumption`. The real transport (`Ai._request`) uses a connection class whose first `send` invokes the gate, after DNS, connect and TLS and immediately before the first request byte. The gate checks current consent and writes its own fence row in ONE transaction, with expiry equal to database now plus timeout plus grace, and returns a local monotonic send-by deadline. Every `send` checks that deadline and refuses past it. Refusal raises a dedicated `DispatchWithdrawn` before any request bytes; `evidence()` reports `suspended-before-dispatch`.
* So: a withdrawal that committed earlier is seen by the gate and nothing is sent; a gate that committed first holds the withdrawal until the call ends or the row expires. A stall before the gate costs nothing (the gate runs afterwards); a stall after the gate longer than the send-by deadline is refused locally. The residual is a stall between the last monotonic check and the kernel `send` (microseconds) or a whole-process suspension that the monotonic clock does not see. That residual is reported as a documented limit, not claimed away.
* Providers that do not declare `honours_dispatch_gate` (test doubles, any future transport) run the same gate immediately before the call. For those, preparation inside the provider is not covered; they must not be used for real data. Real-transport coverage is tested through a loopback HTTP server that counts received bytes.
* Delete only the completing attempt's (home, task, fence) row. A retry or overlapping timed-out attempt has its own row, never replaces another's and is never released by another.
* Tradeoffs: withdrawal waits at most one timeout plus 5 s (bounded, explicit `SENSOR_DISPATCH_IN_FLIGHT` after 45 s, never silent). No global lock, readers unaffected. Not covered: a direct SQL write that bypasses `configure` (the guard trigger invalidates the marker; it cannot recall bytes in flight); SQL Server statements are written, not executed. If a gate row cannot be written, nothing is sent.

C7-7. `configure` reads the (at most 100) existing control rows inside the serialised write, compares each sensor's body with the replacement, and derives the changed set of homes (old and new home of any added, removed, changed or moved sensor). It waits only for live gate rows of those homes. A policy body change affects all homes and waits for every live row; that is the only fleet-wide case and is truthful because the exercise policy governs every home. Resident choice stays explicit: a timeout raises `SENSOR_DISPATCH_IN_FLIGHT`.

C7-3. Idempotent migration of the actual C5 schema: SQLite `PRAGMA table_info`, SQL Server `COL_LENGTH`; add `replaced INTEGER NOT NULL DEFAULT 0` only if absent, preserving rows. The same pattern adds `dispatched` to `assistant_tasks` (see C7-8). If a migration fails, assistants report `schema-unavailable` and stay disabled (fail closed), not a later crash. The legacy test now creates the genuine C5 DDL with data.

C7-8 and C7-4. Add `assistant_tasks.dispatched FLOAT NOT NULL DEFAULT 0`, set to the database clock at every claim, with index `ix_assistant_dispatched (capability, case_id, dispatched, revision)`. Adoption reads at most five rows (`ORDER BY dispatched DESC, revision DESC`, limit in SQL, `attempts>0`) so bodies of only those rows leave the database. Legacy rows have `dispatched = 0` and fall back to revision; that order is a stated approximation, applied only to pre-upgrade history. Adoption takes the newest relevant row of the current release and epoch that was not a person's request and records its OWN signature as the slot signature, so an assessment or funding change A to B is detected by `_due`. Unknown or manual history is never adopted as approval and never creates work beyond what `eligible` already allows. If none qualifies the empty slot is written once. The unresolved SQL Server query plan, lock duration and plan on representative histories is recorded for the admitted SQL stage.

C7-5. Persistent bounded coalescing in scan and claim. After `REPLACEMENTS` stale-before-claim replacements, `claim` sets a truthful reason ("Readings kept changing before the model ran; automatic review is paused briefly. Request review manually or wait.") and does not enqueue. `_due` treats an exhausted slot as not due until `COALESCE_QUIET` (300 s, one reading interval) has passed since the last enqueue, then allows exactly one recovery task. Rows per case are bounded to a replacement chain per quiet interval; the recovery task dispatches (counter reset) once evidence is stable. Survives restart because it is database state only.

C7-6. Serviced status follows the frozen dispatch of the attempt that ran: a dispatched task (`attempts>0`) is manual only when `dispatch.trigger == "requested"`; an undispatched task is manual when `manual_requested` is true (manual-before-claim). A late request during a proactive call is kept as `manual_requested` for a future retry but does not change the serviced bucket.

C7-10. Compare cited rows by canonical content. States: `match`, `changed` (any cited ID differing or missing from the current capture) and unknown (`None`, no current capture). Additional uncited current rows are reported separately as `additional_reading_count`. The UI wording distinguishes the two.

C7-9. Backend-neutral names and counts via the same service flag the other C6 helpers use.

## Plan boundaries and unresolved items

* Not claimed: real SQL, query plans, browser, axe, live model, assistive-technology acceptance, #184 or #1292 semantic integration.
* Owner decision needed? No: every fix stays within the approved contract. The residual physical-send limit is reported, not removed.
