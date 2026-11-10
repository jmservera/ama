---
title: Issue 86 formal-complaints adapter plan supplement (2026-11-06)
ms.date: 2026-11-06
---

Supplements, leaving unchanged, the original plan and details. Applies the dispositions in `.copilot-tracking/challenges/2026-11-06/issue-86-formal-complaints-adapter-critique.md`. Scope: issue86 only. Tier FULL (unchanged; full gate pending, not run).

## Revised design (replaces the single-step handler)

* `resident_action("service_forward")` is orchestrated, not a plain handler:
  1. Phase A, `_operation` with `_res_service_forward`: all validation, then append a `Pending` attempt (shared `route_key` uuid per request, `resident_request_ref`, requester identity, `reserved_at`). Committed before any send.
  2. Phase B, outside the lock: build the envelope from the committed request and call the receiver. Exceptions classify as Unconfigured (`NotConfigured`) or Failed; a bad acknowledgement is Failed.
  3. Phase C, `_operation` with internal `_res_service_forward_outcome` (not in `RESIDENT_ACTIONS`, no authority re-check because the send already happened): set status, receipt, reason, `outcome_at`. If phase C fails, the attempt stays Pending and a `ResidentCommittedError` explains it.
* Refusals in phase A: wrong route, closed request, already Acknowledged, any Pending unless `retry_unresolved` is true, missing `resident_request_ref`, stale version, actor not authorised. Independent review needs actor equal to the named reviewer plus `_require_independent_reviewer`; no manager bypass. Complaint needs the redress owner or a manager.
* Retention: `delete_resident_records` clears `resident_request_ref` and requester identity on attempts.
* Extra tests: outcome-phase failure leaves Pending and blocks silent resend; retry reuses `route_key`; non-reviewer manager refused on Independent review; retention clears the reference; SQL replay does not send.
