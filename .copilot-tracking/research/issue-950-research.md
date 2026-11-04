---
title: Issue 950 research - seed constraints have empty proposed_by
ms.date: 2026-11-04
---

* Task: issue 950, follow-up from review of #895. Research disposition: executed (direct code read). No merged PR already delivered this fix.
* Evidence: `CANDIDATE_CONSTRAINTS` in `src/core/src/zava_forward/core/discovery_register.py` built five `Constraint` objects with the default `proposed_by=""`.
* Effect: `decide()` blocks only a validator equal to `proposed_by`; an empty proposer made that separation check vacuous for seed constraints.
* Slice: pure core, no persistence, API, security, infrastructure, SQL or deployment change. Focused tier. Owner decision authority is unchanged: seeds stay proposals, never findings.
* Planning readiness: Ready.
