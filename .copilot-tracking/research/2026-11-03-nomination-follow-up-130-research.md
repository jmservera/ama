---
title: Issue 130 nomination follow-up view research
ms.date: 2026-11-03
---

## Scope and disposition

Research disposition: executed (targeted). Planning Readiness: Ready for one small slice.

## Prior delivery (merged)

* PR #509 (feat(safety-consent): unverified referral and tenure intake, Refs #130, #131) delivered `nomination_record`, `nomination_correct` and `tenure_intake` in `src/core/src/zava_forward/core/resident_decisions.py`: original account, source, channel, named owner, staff acknowledgement, next update, non-digital route, append-only corrections, hazard refusal route, Unknown identity/support/risk, constructed wrong-identity, limited-representative and manual-channel tests.
* #418 delivered the generic retained-priority challenge and correction route; #220 the version-bound generic challenge dependency engine (`challenges.py`).
* Role queue integration for nominations is not present (`taskqueues.py` has no nomination item).

## Unmet criteria (from PR #509 evidence and issue)

* Nomination reviewer, outcome and eligibility disposition: blocked on OD-41/OD-42 human policy.
* Nomination-specific dependent re-review graph: no decision type is defined to depend on a nomination; speculative to add.
* Automatic hazard routing: not claimed.
* Representative participation and comprehension: needs authorized human evidence.
* Role-queue visibility (#76) of acknowledgement and overdue state: not delivered.

## Chosen slice

Read-only `follow_up` projection on each nomination record: route readiness (owner, acknowledgement, non-digital route; gaps listed), next-update overdue (Unknown when absent), correction re-review pending. No stored state, no SQL schema, no ranking, no authority change. Safe for the focused tier. Larger follow-ups (queue integration, reviewer/disposition after OD-41/42) are later stacked slices.
