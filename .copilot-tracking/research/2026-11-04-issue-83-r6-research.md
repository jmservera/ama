---
title: Issue 83 r6 research
ms.date: 2026-11-04
---

## Scope

Check merged PRs for #83 and decide the next slice. Disposition: executed (GitHub and repository check).

## Evidence

* PR 311 delivered criteria 1 and 2 (return, reopen, distinct handoff states, accountable owner).
* PR 893 delivered core ageing and the exception feed. PR 1036 delivered the read-only GET /api/handoffs/unaccepted route with a caller-supplied max_age_hours that is never defaulted.
* Issue comment (owner) and the 2026-10-31 closure audit: criterion 3 needs approved escalation times (BG-010, OD-09). OD-09 is still listed as open in the BRD open decisions table and in docs/reference/log.md.

## Finding

Every remaining engineering step for criterion 3 (default thresholds, automatic escalation, out-of-hours routes) depends on a human decision by the Housing and repairs leads. Building it now would invent approved times. The staff screen is excluded by the owner note (resident_demo web files).

Planning Readiness: Ready for a docs-only record slice. No code slice is justified.
