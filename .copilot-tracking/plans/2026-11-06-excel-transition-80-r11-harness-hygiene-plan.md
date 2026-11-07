---
title: Issue 80 r11 plan, harness hygiene and cleanup preservation
description: Plan and one-pass critique before any harness or test edit
ms.date: 2026-11-06
---

* Research: [research](../research/2026-11-06-excel-transition-80-r11-harness-hygiene-research.md). Details: [details](../details/2026-11-06-excel-transition-80-r11-harness-hygiene-details.md).
* [ ] Phase 1: two helpers and the pass-through in `design_system_browser_check.py`; focused unit test.
* [ ] Phase 2: light checks with external caches; production byte identity.
* [ ] Phase 3: preservation proof outside the checkout; pending manifest; no deletion.
* [ ] Phase 4: Changes, state, validation; then a separate later Review.

## Critique (executed once, before edits)

* Risk: changing a shared harness alters other checks. Mitigation: defaults unchanged when the new variables are unset; the unit test asserts the default scratch parent and the pass-through only when set.
* Risk: an unrunnable fix claimed proven. Mitigation: only helper behaviour is tested; the real run stays deferred.
* Risk: archive treated as deletion permission. Mitigation: manifest marked pending, root authorisation required.
* Risk: archiving tracking could follow symlinks. Mitigation: tar without dereference, readback compares member types.
* No conflict with confirmed decisions.
