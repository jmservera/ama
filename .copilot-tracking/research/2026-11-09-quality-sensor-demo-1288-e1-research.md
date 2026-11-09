---
title: Quality sensor demo 1288 E1 research
ms.date: 2026-11-09
---

Written 2026-11-09T08:40Z, before any E1 source edit. Refs #1288, #107. No closing claim. Research disposition: executed (new investigation of current source) plus reused (C1-C8 records, unchanged).

## Authority and cycle count

* Owner grant 2026-11-09: https://github.com/jmservera/ama/issues/1288#issuecomment-6735179415 (up to five additional correction cycles for currently exhausted issues; C6-C7 grant exhausted). Cycle numbering: C1-C7 and the C8 recovery (fixture isolation, not a correction) are historical and unchanged. This is **E1, the first of up to five additional cycles: E1 used, 4 remain.**
* Base: frozen C8 candidate `1251c1dcbe97a50039cf134a9d54ed90164ec846` (tree `d3eb466231f8ae84ed114684ae768db5dcda7e7b`), main `b46a9ad9a`. No live model, Azure, deployment, cost, release or credential authority is added. PR #1301 (issue 1294 policy) merges first; this branch is not published.

## Original C7 independent findings: recovered

The coordinator brief said the exact report was missing. A durable copy exists in a sibling session: `/home/azureuser/.copilot/session-state/f751a4dc-045d-479c-8035-8588858e3b08/files/review-1288-391e-c7-functional/functional-findings.json` (verdict Revise, 5 High, 1 Medium, reviewed head `391e42f0d`). It is read-only evidence and is not copied into the repository. Its six findings (F1-F6) are used below as hypotheses; each is reproduced against current source before it is fixed. The issue comment summary is https://github.com/jmservera/ama/issues/1288#issuecomment-6728737055.

| ID | Sev | Original finding (summary) |
| --- | --- | --- |
| F1 | High | An expiring gate cannot order withdrawal against an in-progress physical send (stall or partial send after expiry; foreign provider receives the prompt after `gate()` with no transport check). |
| F2 | High | Direct SQL writes to `sensor_consumer_control` can commit a withdrawal while a dispatch is authorised; the trigger only drops the index marker. |
| F3 | High | A manual request for a different exact capture replaces an already serviced proactive Quality slot, so a later reading starts a second autonomous call. |
| F4 | High | `_adopt` reads five history rows; five newer manual or other-scope tasks hide the serviced task and an empty slot is persisted, silently treating an incomplete search as no history. |
| F5 | High | The coalescing quiet timer is measured from the last slot enqueue, not from the last observed change, so continuous readings re-open the replacement budget repeatedly. |
| F6 | Medium | A failed or withheld current capture (empty reading lists) is compared as if observed, so cited IDs are reported missing and `changed_since_capture` is true. |

## Current-source investigation (static, to be proven by failing tests)

* F1. `ai._gated_opener.check()` evaluates `gate()` once and a monotonic deadline per send. `Plain.send`/`Secure.send` call `check()` then `super().send(data)`; `sendall` is not bounded by the remaining deadline (TLS `sendall` re-arms the timeout per partial send), so a blocked or trickling send continues past database expiry. The deadline sits `HOLD_GRACE/2` (2.5 s) plus transaction time inside the database expiry, so a process suspension longer than that margin between the final check and the kernel call cannot be excluded in userland. New fact: the production wiring in `src/api/.../server.py` passes `AgentWorker(...).provider_call`; `Assistants._provider_honours_gate()` reads `__self__.honours_dispatch_gate` on the `AgentWorker`, which does not define it, so the real API path takes the foreign-provider branch (`gate()` once, no transport fence) although the wrapped `store.ai` is the gate-honouring `Ai`. Any foreign provider with captured readings is handed the prompt with only that single pre-call gate.
* F2. `ensure_control_guard` installs triggers that only `DELETE FROM sensor_consumer_index_state`. `configure()` coordinates with `assistant_dispatch_gate` in application code (`_dispatch_in_flight`) but a direct `UPDATE`/`DELETE` commits freely while a gate row is live. `_replace_controls` deletes and reinserts every control, so a database-level fence would also hit unchanged homes unless the write is diffed.
* F3. `_enqueue` calls `_occupy(..., touch=mode == "proactive")` for every mode, so a manual capture B overwrites scope, signature and task of the slot that holds serviced proactive task A.
* F4. `_adopt` pages once (`ADOPT_ROWS = 5`) and persists an empty slot when nothing qualifies in those five rows, with no distinction between exhausted history and an incomplete search. `eligible()` for change-only capabilities depends on `changed`, which is false for an unscoped slot.
* F5. `assistant_schedule.at` is the time of the last proactive enqueue. `_due` suppresses scans while `replaced >= 3` and `now - at < 300`; after 300 s it enqueues again and `_occupy` resets `replaced`, regardless of whether readings kept changing. The schedule holds no observed-evidence digest.
* F6. `review_flag` treats `current.sources.sensors` with `state` unavailable or consent-withheld (empty lists) as observed evidence.

## Bounded design chosen (details in the plan)

* F1: sends are chunked and each chunk is re-checked and bounded by the remaining send-by time (socket timeout shortened for the chunk and then restored); non-bytes request bodies fail closed. Captured readings are never dispatched to a provider whose transport is not fenced (`honours_dispatch_gate`) unless it declares `sends_no_bytes` (local double); the API wiring declares the real `store.ai` transport through a lazy `transport` hook. The residual (process or VM suspension longer than the margin between the last in-process check and the kernel send) cannot be closed in userland and is stated as unsupported, not as safe.
* F2: control triggers on both stores reject INSERT/UPDATE/DELETE that touch a home with a live gate row (database clock), keep deleting the marker, are upgraded in place from the C7 definitions, and `configure()` writes only the changed controls.
* F3: for `quality-evidence`, a person's request never occupies or rewrites the autonomous schedule slot.
* F4: history is searched in keyset-free offset pages up to a hard cap; if the cap is reached without a qualifying task the slot records an explicit `incomplete-history` marker that `_due` treats as changed (one bounded autonomous call, which then owns the slot), never as empty history.
* F5: the schedule gains a durable `seen` column (last observed full evidence signature). While the replacement limit is reached, a scan that observes a different signature records it with `at = now` and stays paused; resumption needs the same signature unchanged for the full quiet interval.
* F6: comparison runs only when the current capture state is `ok` or `no-readings`; otherwise it is `unknown` with no asserted missing IDs and a null newer count; the UI states that evidence could not be compared.
* Browser (AC7): the existing API browser harness patterns are reused for the smallest real check; Playwright and axe are verified absent before an isolated install.

## Dependencies and edges

* #1292 and #184 are not imported. Edges recorded for the coordinator: `assistants.py` and `sensor_consumer.py` schema creation (#1292 persistence), and the `store.ai`/`AgentWorker` transport (#184). The new `assistant_schedule.seen` column and gate-aware control triggers are additive.
* Live walkthrough (AC8) stays blocked on merged source and version, release admission, finite existing authority and the credential owner.

## Planning readiness

Ready. Unknowns carried: SQL Server trigger syntax and lock behaviour are proven only by the real disposable run; TLS partial-send behaviour is proven only on loopback plain HTTP and by unit test on chunk checks.
