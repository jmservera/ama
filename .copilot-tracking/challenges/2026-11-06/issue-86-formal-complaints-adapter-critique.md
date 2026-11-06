---
title: Issue 86 formal-complaints adapter prospective critique and dispositions (2026-11-06)
ms.date: 2026-11-06
---

Scope: issue86 only. Independent critic: `rubber-duck` agent, read-only, run once on the original plan, details and research before any source edit. One critique only; no repeat. Verdict: 2 blockers and 5 significant findings, all accepted as compatible (none conflicts with a confirmed decision), no user decision needed. Dispositions are by the author.

| # | Severity | Finding (critic) | Disposition |
| --- | --- | --- | --- |
| 1 | Blocker | Send precedes SQL validation; concurrent processes can both send | Accepted. Two-phase flow: a committed Pending reservation under the writer lock, send outside the lock, outcome recorded in a second committed step. A second reservation is refused while Pending. Concurrency of two separate stores cannot be fully proven without a real receiver; the SQL validation replay now has no side effect. |
| 2 | Blocker | Per-attempt key does not give idempotency; save failure loses outcome | Accepted. One uuid `route_key` per request, reused by every attempt; Pending is retained if the outcome save fails; retry of an unresolved attempt needs explicit `retry_unresolved=true` and reuses the same key. Residual: receiver-side dedupe is unverified. |
| 3 | Significant | Manager bypass of reviewer authority | Accepted. Independent review: the actor must be the named reviewer and independent of `reviewed_identity`; no manager bypass. Complaint: redress owner or manager. |
| 4 | Significant | `resident_request_ref` not persisted | Accepted. Stored (max 100) on each attempt. |
| 5 | Significant | Free text can carry sensitive data despite key allow-list | Partly accepted. The envelope stays an exact allow-list of existing staff-entered fields; the substance is needed for a complaint. Unscreened free text is documented as a residual risk for the DPO/Legal decision a real receiver needs; no screening is invented. |
| 6 | Significant | Retention deletion misses new nested data | Accepted. `delete_resident_records` clears `resident_request_ref` and requester identity on attempts; receipt refs and statuses remain. |
| 7 | Significant | Receiver call under the lock | Accepted via the two-phase flow (send outside the lock). |

Adverse result preserved: the original single-step design was unsafe; the plan supplement replaces it. See `.copilot-tracking/plans/2026-11-06/issue-86-formal-complaints-adapter-plan-supplement.md`.
