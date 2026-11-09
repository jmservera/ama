---
title: "Issue 86 formal-complaints adapter: review-correction critique"
description: One independent prospective critique of the review-correction research, plan and details, with dispositions, before implementation
ms.date: 2026-11-07
issue: jmservera/ama#86
rpi_phase: critique
task_slug: issue86-formal-complaints-review-corrections
parent_task_slug: issue-86-formal-complaints-adapter
---

Scope: jmservera/ama#86 only. One independent read-only critique pass (rubber-duck sub-agent) of the draft research, plan and details and the cited source, before any source or test edit. It is not repeated. Verdict returned: Revise (no blocker; four Significant and one Minor). It ran no test or service and edited nothing. The independent functional assessment it builds on (`approve_with_comments`, 0 critical, 0 high, 3 Medium, synthetic/unconfigured publication only) is preserved unchanged.

Checks with no finding, as reported: the outcome action is outside the public `RESIDENT_ACTIONS`; SQL replay reuses the supplied body; store classes appear weak-referenceable and hashable; no `src/api` consumer of formal-route status was found; retention already removes `resident_request_ref` and `requested_by`; no receiver activation or #144 edit is proposed.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Significant | The in-flight registration happens after `_operation` releases the lock, so a flagged retry can reserve and send in the gap. | Accepted. `_forward` holds the re-entrant `store.lock` continuously across the reservation commit, the exact-attempt lookup and the registration; receiver I/O stays outside. A flagged retry now blocks on the lock and is then refused as in flight. Details updated. |
| 2 | Significant | The binding regression appends attempt 2 only after the first caller is inside `submit`, so it cannot reproduce the defect, which sits between commit and lookup. The snapshot test changes the request after submission began. | Accepted. Both tests use a seam between the reservation commit and the lookup (a wrapper over `resident_decisions._operation` that, after the real reservation exits, commits the competing attempt or request change through the store as a second caller would). RED must be demonstrated against the current `attempts[-1]` code first. All blocking events are released in `finally` with timeouts. |
| 3 | Significant | `_identity` always carries `oid`, often `None`, so "every key present" is ambiguous and could reject genuine staff-list reviewers. | Accepted. Compare non-empty, case-folded identifiers only, require at least one compared, and fail on any compared mismatch. Tests: code-only, code plus oid, missing, changed code, changed oid, bound Entra actor. |
| 4 | Significant | The snapshot guard cannot guarantee freshness until `submit` returns. | Accepted. Documented as a point-in-time guard under the lock; the residual race (closure after the guard) is stated, not claimed away. No lock is held across receiver I/O. |
| 5 | Minor | The registry is per Store instance, not process-wide; separate instances in one process have separate keys. | Accepted. The guarantee is described as per Store instance, a test asserts the second-instance limit (misattribution never occurs; duplicates remain bounded by the explicit flag and the receiver's `idempotency_key`), and the weak-key mapping is kept (stop and report if a store is not weak-referenceable). |

## Residual risk accepted

Cross-instance or cross-process explicit retries can still send twice; only the reservation identifier prevents their outcomes from being misattributed. Receiver-side deduplication, a real receiver and a two-process proof are not implemented here. Whole-issue operational acceptance (residents reach independent human review and the formal route without detriment) remains unproven and unticked.
