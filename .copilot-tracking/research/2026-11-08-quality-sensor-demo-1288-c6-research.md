---
title: Quality sensor demo 1288 C6 research
ms.date: 2026-11-08
---

Written 2026-11-08T22:27Z, before any product or test edit. Refs #1288, #107. Base: frozen `5f89248b` / tree `437ce301`, tracked clean (verified). Research disposition: executed (source reading plus the independent C5 report). Planning readiness: Ready.

## Authority and limits

* Owner authorised two more bounded cycles for #1288 after C5 (C6 now, C7 reserved). Consent, safety, independent review, release and live gates are not waived. FULL tier stays (SQL consent/control, security-sensitive projection).
* Light SQLite and static tests on synthetic data only. No Docker, SQL Server, browser, FULL, provider call, push, PR, cleanup. #184 and #1292 overlap modules; ordering belongs to the coordinator.

## Independent C5 findings, verified against `5f89248b`

Source: `/home/azureuser/.copilot/session-state/f751a4dc-045d-479c-8035-8588858e3b08/files/review-1288-5f89248-functional/functional-findings.json` (request changes; 5 High, 3 Medium). All eight were confirmed by reading the committed code.

* C6-1 High, dispatch ordering (`assistants.py` `execute.call`): the last consent transaction commits, then the provider is invoked. A withdrawal by another connection between the two is not seen; data leaves after withdrawal. Withholding the later output does not retract disclosure. Confirmed; C5 documented it as residual.
* C6-2 High, in-place refresh (`claim`): the task keeps id `hash(A)` but stores capture B. A manual invoke of B computes `hash(B)`, misses the leased task and creates a second task (two dispatches, two allowance calls). A later exact return of A finds a row whose actual source is B. Confirmed.
* C6-3 High, schedule slot starts empty (`migrate`, `_due`): pre-upgrade tasks are not mapped to `assistant_schedule`. Assessment/funding changes after the last legacy result are not eligible because `scoped` is false; Quality same-bucket arrivals look unserviced and can double-call. Confirmed.
* C6-4 High, stale flag hidden: a same-bucket reading after a returned automatic flag makes the task stale; `assistants.js:226-230` puts every stale proposal in the collapsed history and `waiting` (`assistants.js` line 189 area, `case-workspace.js:19`) excludes it. Coarse slot suppresses a replacement, so no visible flag. Confirmed.
* C6-5 High, manual occupies the autonomous slot (`_enqueue`): `_occupy` runs for every mode, so a person's completed request makes later same-bucket scans treat the case as serviced; no autonomous flag until a new bucket. Confirmed.
* C6-6 Medium, SQL variants: `MssqlReadModel` and `MssqlHttp` inherit tests that call `json_set`/`json_remove`, `sqlite_master`, a SQLite trigger name and `set_trace_callback`, none valid on the SQL Server adapter. Confirmed by reading tests; not run on SQL Server.
* C6-7 Medium, flag UI omits the captured as-of: `reviewFlagBlock` shows only `source_time` (task creation). The flag API already carries `evidence_as_of`, `freshness`, `age_minutes`. Confirmed.
* C6-8 Medium, sensor panel claims identity: `ops.js:46-55` says the assistant reads "these same readings" and the table is "the same capture the assistant uses". False once any normal reading arrives after capture. Confirmed.

## Design research and tradeoffs

C6-1. Facts: `SensorConsumer.configure` is the only trusted consent writer; it replaces all controls in one `BEGIN IMMEDIATE` write; `assistants.transaction` is serializable on SQL Server. A consent check is only an ordering point if the withdrawal cannot commit between the check and transport start. Options:

* A. Re-check closer to transport. Rejected: still a gap; the reviewer's barrier lands in it.
* B. Hold an open DB transaction/lock across the provider call. Rejected: SQLite has one writer lock (global block of all writes); SQL Server row locks held for up to the provider timeout also block every reader of that home and risk lock escalation.
* C. Chosen: a durable per-dispatch hold row `assistant_dispatch_hold` (home, task, fence, `until` on the database clock). The dispatcher checks consent and inserts the hold in ONE transaction before transport; releases it in a second transaction when the provider call returns or fails. The consent writer (`configure`) checks for a live hold inside its own write transaction and refuses to commit while one exists, waiting with a bounded poll and then failing explicitly (`SENSOR_DISPATCH_IN_FLIGHT`). Both writers are serialised by the engine (SQLite `BEGIN IMMEDIATE`; SQL Server SERIALIZABLE range locks on the hold table), so either the withdrawal commits first and nothing is sent, or the hold commits first and the withdrawal commits only after the call has ended. This is genuine cross-process ordering around the transport.
* Tradeoffs: a withdrawal is delayed at most one provider timeout (default 20 s, max 40 s) plus a 5 s grace; the delay is bounded, visible (explicit retry-or-fail, never silent), per call not a global lock on readers, and a crashed dispatcher cannot block: `until` expires. `configure` replaces all controls, so it waits for any live hold; unrelated readers and writers are not blocked. The hold also fails closed: if it cannot be written, nothing is sent. A direct SQL write that bypasses `configure` is outside the trusted writer; the guard trigger still invalidates the index marker so later readers withhold, but it cannot recall an in-flight call (documented, not hidden). SQL Server statements are written but not executed (PENDING real SQL).

C6-2. Identity must be immutable. Chosen: remove refresh-in-place. At claim, an unrequested proactive task whose capture changed inside the same coarse schedule goes stale (event `superseded`) and the current exact capture is enqueued as a new proactive task (new id) in the same transaction, so a later manual invoke of B finds that exact task and A returns to its own row. Churn bound: a persisted `replaced` counter on the schedule slot stops replacement after 3 consecutive replacements for a coarse signature without a dispatch; the counter resets on a dispatch. After that the last task stays stale until a scan after stable evidence re-enqueues (scan-interval bounded). Provenance is frozen per claim as in C5.

C6-3. Lazy, per-case, idempotent backfill inside `_due` when no slot row exists: one indexed lookup of that case/capability's newest dispatched task (new index `ix_assistant_case`) adopted only when its release and epoch equal the current scope and its dispatch was not explicitly a person's request; unknown legacy provenance is adopted conservatively as serviced (it only throttles, never approves). Otherwise nothing is inferred and an explicit empty slot is written so the lookup happens once per case. No fleet scan in `migrate`.

C6-5. `_occupy` runs only for proactive enqueues. A slot is serviced only when its task was dispatched proactively (not stale-before-claim, not explicitly requested, not exact-evidence terminal manual). A person's request neither occupies nor suppresses; the next same-bucket arrival produces a new exact capture that is enqueued autonomously; calls stay bounded by the existing allowance and by the slot once an autonomous dispatch is recorded. A scan never re-labels or re-enqueues an existing row (`_due` false when the exact task row exists and is not requeueable).

C6-4. Chosen: UI only, no new model spend. A returned proactive `review-suggested` flag that is stale because of newer same-schedule readings stays in the main review path and counts in the waiting indicator, qualified as "captured as of T, stale, newer readings exist", with accept/verify still disabled (the API already makes it non-actionable). The list endpoint must carry `review_flag`.

C6-6. Backend-neutral tracing through a recording connection wrapper; backend-specific control mutation and guard-metadata helpers (SQLite json_set/sqlite_master; SQL Server JSON_MODIFY/sys.triggers) as overridable test helpers with explicit SQL Server bodies. SQL Server tests stay skipped without `ZF_TEST_MSSQL=1`; no SQL pass is claimed.

C6-7/8. `reviewFlagBlock` shows captured as-of, freshness (fresh/stale/unknown; unknown with its own wording) and age, separate from creation time and from the current panel. The sensor panel is renamed "current authorised capture" and states that a proposal's cited readings are the ones captured when it ran; the flag carries `changed_since_capture` and a count of newer readings so the change is visible.

## Risks

* Delay of a withdrawal up to the provider timeout is a product tradeoff inside the existing owner intent (finite spend, resident consent). Not an authority change; reported.
* Web files change: guidelines refreshed before edit and again before review.
