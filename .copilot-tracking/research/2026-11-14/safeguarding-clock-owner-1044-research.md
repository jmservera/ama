---
title: Issue 76 research, safeguarding clock and named owner (demo slice)
ms.date: 2026-11-14
---

## Scope

Issue 76, unmet criterion: hazard and safeguarding items show a clock and named owner. Research disposition: reused plus bounded re-inspection.

## Evidence

* `gh issue view 76 --comments`: hazard clocks exist (PR 897); closure audits 2026-10-31 and 2026-11-05 and the 2026-11-12 demo comment record that safeguarding marker, named role, approved duration and visibility need owner and domain policy.
* Prior research: `.copilot-tracking/research/2026-11-04/safeguarding-clock-76-research.md` (no safeguarding case data, no approved duration).
* Code: `src/core/src/zava_forward/core/taskqueues.py` builds `work` context with `hazard_clocks`; `Store._work_context` passes `reason_ok = projection.can_see_reason(user)`; `src/api/src/zava_forward/api/web/app.js` `workSummary` renders it on queue rows and the case card.
* `data_protection.py` lists safeguarding among prohibited free-text, memory and AI fields.

## Findings

* Hazard clock and owner display already works in queue and case card; missing owners show Unknown.
* No safeguarding record exists on a case, so nothing can show a clock.
* A safeguarding display slice can be honest if it only renders recorded deadlines and named owner, derives no duration, copies no narrative field, and discloses nothing (not even presence) to roles outside the existing need-to-know projection.

## Planning readiness

Ready for a bounded engineering slice. Policy items (approved duration, named lead role, DPIA, who holds the marker) remain open human decisions, so the issue criterion must not be ticked.
