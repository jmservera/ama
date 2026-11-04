---
title: Issue 130 nomination human review research
ms.date: 2026-11-04
---

## Prior delivery (merged PRs)

* #509: unverified referral and tenure intake (`nomination_record`, `nomination_correct`).
* #859: read-only nomination follow-up view. #1037: overdue next updates in the work queue.
* Issue closure audits (2026-10-31, 2026-11-04): C1, C6, C7, C12, C13, C15 ticked.

## Gap

* C3 needs a nomination-specific reviewer and outcome retained next to competing evidence. Today a correction only sets "Re-review required".
* C4/C11 need a prior review to go stale exactly when a correction lands, with history kept.

## Decision

Smallest coherent slice: a `nomination_review` resident action on the existing ledger. Acting staff member is the human reviewer, must differ from the recorder of the version under review, outcome is from a closed set, bound to the record version. A correction marks earlier reviews stale without deleting them. No priority, consent, sanction, hazard or eligibility change.

## Boundaries

* OD-41/OD-42 (validation and representative authority) stay open; no policy owner is appointed, so this is constructed staff-recorded review, not eligibility.
* C5 (hazard onward routing), C14 and resident participation evidence need owner or human evidence.
* Tier: focused. No security, infrastructure, SQL schema or deployment change.

Planning readiness: Ready.
