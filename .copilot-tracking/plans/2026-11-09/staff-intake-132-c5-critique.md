---
title: Staff intake 132 C5 critique
ms.date: 2026-11-09
---

One critique, executed before any test or source change (rubber-duck sub-agent, read-only). Verdict: Revise, 2 blocking, 3 non-blocking. No second critique is run.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 Blocking | Receipts already stored with a staff code as the worker remain acceptable by that staff member | Accepted in part. `quality._independent` cannot change inside 132 ownership and no coordinator admission exists. The C4 head was never published or released, so persisted synthetic receipts exist only in disposable test data. The intake view already shows the independence blocker for them. Recorded as a named limit with the exact fix location (quality participant resolution); not claimed fixed for legacy data. New capture can no longer create such a record. |
| 2 Blocking | `decision_scope._discard()` does not take `dblock` | Accepted. Hold `store.dblock` (an RLock; lock order `store.lock` then `dblock` matches `save`) around `submit_quality` so the failed-write recovery cannot interleave with another thread on the same connection. Test conflict recovery then a normal capture on the same store. |
| 3 Non-blocking | Pre-existing token test cannot pass if detected only in outermost lock | Accepted. Check inside the capture lock and test the nested case by entering `store.lock`, installing a sentinel token, calling capture and asserting refusal and an untouched token. |
| 4 Non-blocking | Worker-name contract contradicts itself | Accepted. Reject identifier collisions (email, code, oid) with ANY registered staff identity; another staff member's NAME stays allowed because existing participant resolution binds the full identity, and the real accept route denies that person. Test both. |
| 5 Non-blocking | `_worker` is reused for replay and correction | Accepted. Staff identifier rejection applies to new capture only (`new=True`). Replay and correction compare against the stored receipt, so a later-registered identifier cannot break a retry. Test replay after an identifier is registered. |

No finding conflicts with a confirmed decision. No user decision is required.
