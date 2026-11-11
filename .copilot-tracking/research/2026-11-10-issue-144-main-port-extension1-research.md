---
title: Issue 144 main-based slice A port research
description: Research for a minimal main-based selective port of the worker permit slice A with current main safeguards
ms.date: 2026-11-10
task_id: issue-144-main-port-extension1
---

## Scope and disposition

Research disposition: executed (read-only on main plus the preserved lineage). Planning Readiness: Ready. Root selected option 2: a minimal selective port of slice A onto fresh origin/main `6d4cd62475ba89a214055f761b8e3276ef063d44`, in worktree `issue-144-extension-main-1110`, branch `fix/demo-worker-permit-extension-144`. The old worktree (HEAD 564b78f4) stays clean and unmerged. This is E1 of the new finite five-correction grant; the old spent history and the unknown minimum 0 are preserved and not reset.

## Inputs consumed

* Plan 564b78f4 and the Core-only boundary record (`2026-11-10-issue-144-core-only-plan-revision-research.md` in the old worktree, plan revision handoff).
* Lineage Core diffs against base bb3a3b03: ai.py (+32), ai_consumption.py (+287/-84), assistants.py (+157), and the service-level permit tests of `test_ai_consumption_api.py`.
* Original clock fix (commit 3f813404d): the task-row UPDATE blocks first and the database time is read after it returns. This is preserved as existing behavior, not a new bug fix claim.
* Main safeguards read in `core/assistants.py`, `core/ai.py` and `core/ai_consumption.py`.

## Actual main contract

* `Ai.provider_body` is the only body serializer (static). `Ai.evidence` uses `self.fast` and temperature 0. There is no `_body` on main.
* Main `execute()` gates before a provider call: suspension, admission, epoch, release, `_sensors_granted` consent ("Monitoring consent is not granted now"), and `may_carry_captured_readings(self._carrier())` for captured sensor readings ("Captured sensor readings cannot be sent to a real AI model in this release"). It then runs under `call_context`, `captured_readings(captured)` and `send_fence(fence_send)`.
* `fence_send(attempt, capability)` is the last durable decision before a byte: `disabled(db, capability, capacity=False)`, the attempt row must be `reserved` or `sending` and live, then it restamps the attempt to `sending` for the bounded window; a refusal records `send-refused` and raises `DispatchWithdrawn`.
* `Ai._request` keeps the order: captured-readings withdrawal, `provider_body`, simulation verifier, data hold, size, meter, fence, reserve, `dispatch_check`, open, witness.

## Gap in the retained slice A

The lineage `issue_permit` checks suspension, admission, epoch, binding, release and source signature but not consent, captured readings or the send fence. A permit could therefore be issued for a task that main would hold or send nowhere. This is the blocker named in plan 564b78f4 and is resolved here by integrating the exact main gates, fail closed.

## Hunk decisions

* Port: `Consumption.reserve_in(min_window)`, `dispatch_window_ms`, an `_scope` helper and `complete_in` (the first completion wins, as `complete` does today); `reserve` and `complete` become thin wrappers with unchanged behavior.
* Port: `Ai.is_live` (same expression as main inline), `Ai.request_plan` built on `provider_body`.
* Port: `issue_permit` (fresh time after the blocking UPDATE), `_permit_block` (now with consent and captured-readings gates), `_refuse_attempt`, `_markers`, claim-time permitted-marker block, `complete_result` and `_settle_meter`.
* New integration (main safeguards on the permit path): consent, captured readings, and the send fence evaluated in the permit transaction, by sharing the `fence_send` logic through one helper so the two cannot drift.
* Deferred, not ported (speculative or B): `dispatch_check_request` hook (only PermitMeter implements it), `reconcile`, `settlement-conflict`, `_alert`, report `unresolved_liabilities`, `publisher`, `publish_pending`, routes, worker, queue and Date code, back-off, infra, real-SQL lock-crossing tests (no SQL authorized).

## Fail-closed semantics chosen (no new authority)

* Consent not granted: refuse with `consent-not-granted`, task goes to manual (state disabled), allowance refunded.
* Captured readings present: a permit authorizes a worker-side real provider send, and under the existing contract a real client never carries captured readings, so refuse with `captured-readings` to manual. Refusal does not depend on the in-process carrier.
* Fence unavailable (disabled, attempt not reserved or sending, or attempt expired): refuse with a fence reason, no reservation. On success the attempt is restamped to `sending`, the same step `fence_send` performs.
* No consent grant, live send, spend or deployment decision is made.

## Test closure

Service-level permit tests run on SQLite through `ConsumptionApi` (all imports are main-existing). The real-SQL clock regressions need MSSQL and are not authorized; the clock behavior is covered by a deterministic regression that advances database time only when the blocking task UPDATE executes. Real-SQL coverage stays unobserved and is reported as such.

## Unknowns

* Real-SQL behavior of the ported code (not run).
* Exact old corrective count (UNKNOWN, minimum 0; E1 of the new five is this cycle).
* Whether Root wants the digest hook in a later B step.
