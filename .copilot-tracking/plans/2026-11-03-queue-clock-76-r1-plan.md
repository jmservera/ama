---
title: Issue 76 round 1 plan
ms.date: 2026-11-03
---

Stacked slices for criterion 5: (1) this slice, hazard clock owner and deadline states; (2) later, a consent-governed safeguarding concern record with clock and named owner, needing a design decision and owner approval; (3) later, browser check evidence for owner-gap rows.

Slice 1 phases (details: [details](../details/2026-11-03-queue-clock-76-r1-details.md)):

* [x] Add `owner_named`, `owner_status`, `response_state`, `resident_update_state` to `hazard_clocks`.
* [x] Render the new text in the existing safety clock sentence.
* [x] Add core and web-fixture tests; run ruff and mypy.

Critique (executed once): compatible findings applied directly. Additive fields keep existing phrases, so current tests and the browser check still hold. No role projection change; contractors still receive no staff safety context.
