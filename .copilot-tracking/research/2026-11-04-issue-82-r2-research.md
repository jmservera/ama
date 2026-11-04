---
title: Issue 82 round 2 research
ms.date: 2026-11-04
---

Research disposition: reused (round 1 research plus code reading). Planning readiness: Ready.

* Merged work: PR #898 added `gates.py` (GateResult, check, transition_allowed, safety release gate). No other merged PR refs #82.
* Existing 'Ready to book' checks in `Store.advance` raise `GateError` reason lists for funding, safety and resident decision; they are not GateResult values and unknown evidence is not distinguished from fail.
* Smallest unblocked slice: express the funding, safety and resident booking gates as GateResult with rule records, and make `advance` fail closed on them.
* Still unmet after this slice: evidence, eligibility, authority, capacity, quality and finance gates as GateResult; API and UI exposure; named reviewer and rule-card links.
