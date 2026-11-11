---
title: Staff intake 132 C5 details
ms.date: 2026-11-09
---

## Files

* `src/core/src/zava_forward/core/staff_intake.py`: `_worker`, new `_read_dependency` context manager, `capture`.
* `src/api/tests/test_staff_intake_api.py`: red then green regressions.
* `src/api/README.md`, `src/core/README.md`: C5 notes.
* No change to `quality.py`, `procurement.py`, `sqlstore.py`, `server.py` or the screen.

## P1 tests

1. `test_worker_staff_code_is_rejected_and_unrelated_qa_accepts`: with real resident and safety prerequisites, `sam` captures `confirmed_by="PM-01"`; expect 400 and no record. Also email `pam@example.test`, code `qi-02` (case-insensitive) and contractor code `CON-1`. Then `sam` captures a plain unrelated worker name and `quil` accepts through `/api/cases/ZF-3/quality-accept` (positive control). Pam is denied by independence only when the worker is Pam by name.
2. `test_withdrawal_between_validation_and_save_conflicts_without_receipt`: `b = self.reopen_store()`; patch `staff_intake._binding` so that after the real call, `b.withdraw_work_order(manager, "WO-0001", "SYN")` commits. Capture returns 409, `quality` is empty in a fresh store read, and no audit entry for quality_submitted exists.
3. Same interleave with `reissue_work_order` (scope text changed) and a variant where nothing changes (success, one record).
4. A pre-set `procurement_validation` token causes refusal and is left untouched; token is None after success and after failure.

## P2 source

`_read_dependency(store, user, snapshot)`: for stores with `db`, build `dict(user=deepcopy(user), actor=change_provenance._actor(store, user), authority=None, cases={}, snapshot=snapshot, authorities=[], persisted=False)`, set `store.local.procurement_validation`, yield, restore previous in `finally`. For the JSON store yield without a token.

## Rollback and cleanup

Quality `decision_scope` discards pending state and reloads under `dblock` on any exception. `save` clears the token after COMMIT. The adapter's `finally` restores `None` on every path including thread exit by exception.

## Critique dispositions applied

* Hold `store.dblock` around `submit_quality` (SQL only).
* Refuse a pre-existing `procurement_validation` token inside the capture lock; nested test with a sentinel token.
* `_worker(..., new=True)` rejects email, code and oid collisions with any registered staff identity (`store._quality_staff()`); staff names stay allowed. Replay and correction use `new=False`.
* Legacy receipts stored with a staff code stay a named limit (quality participant resolution, outside 132 ownership).
