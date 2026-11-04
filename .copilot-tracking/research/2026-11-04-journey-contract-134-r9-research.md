---
title: Research for issue 134 slice 5 (building dependency control in the journey)
date: 2026-11-04
task_slug: journey-contract-134-r9
---

## Prior delivery (merged, not redone)

* #872 journey trace (slice 1); #1010 AC-034 to AC-043 register (slice 2); #1029 real-store journey test (slice 3); #1077 perspective walkthrough register (slice 4).
* Issue comment (closure audit): constructed-fixture labelling criterion already ticked.

## Remaining acceptance criteria

* Eleven perspectives with all five elements over linked records: unmet (18 cells unmet; needs screens).
* AC-034 to AC-043: 6 partial, 4 deferred; none proven.
* Same-home journey: partial (JSON store only; SQL store, API, screen not proven).
* Negative controls: sibling control proven in slice 3; building dependency isolation proven in test_buildings.py but not connected to the journey trace.
* Keyboard, text state, announcements: unmet (browser run needed).

## Chosen slice

Connect the building dependency negative control to the same-home journey (store plus trace). Existing evidence: buildings.blockers scoping, Store.advance gate. Planning readiness: Ready. Disposition: executed.
