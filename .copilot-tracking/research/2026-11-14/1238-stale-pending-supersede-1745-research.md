---
title: Issue 1238 F3 stale Pending attempt research
ms.date: 2026-11-14
---

## Scope

Remaining criterion of #1238: `(low F3) Mark a stale Pending attempt superseded.`

## Evidence

* `src/core/src/zava_forward/core/resident_decisions.py`: `_res_service_forward` appends a new attempt on an explicit `retry_unresolved`; earlier `Pending` attempts are left untouched. `_res_service_forward_outcome` records `Acknowledged` with `receipt_ref` but never touches earlier attempts.
* A `Pending` attempt is created when an Acknowledged receipt could not be recorded. After a retry is Acknowledged, the earlier attempt stayed `Pending` indefinitely.
* `_res_service_supersede_authorize` already supersedes a `Pending` attempt only through two named approvers (owner decision Q6, "never age, never a resend"). That path is unchanged.
* `src/api` only routes the actions; no write or retry logic lives there. No change needed.
* Existing test `test_forward_in_flight...` asserted `["Pending", "Acknowledged"]` after retry.

## Decision

Supersede only on evidence, not age: when a later attempt is `Acknowledged`, earlier `Pending` attempts that are not in flight become `Superseded` with `superseded_from`, `superseded_at` and `superseded_by` (attempt number). Receipt, key and history are kept. `Unconfirmed` and `Failed` attempts are out of scope. Planning Readiness: Ready. Research disposition: executed.
