---
title: "Research: issue #232 round 2 (remaining slice)"
ms.date: 2026-11-01
---
<!-- markdownlint-disable-file -->
Task: issue-232-housing-officer-screens-r2. Mode: manual-sequenced loop. Disposition: executed. Planning Readiness: Ready.

## Evidence

* PR #652 (merged) delivered the single-home `resident-choice` screen: measure and version choice, pause or withdrawal panel distinct from contact and access, linked update commitment with purpose, owner and safe route reference, no controls. Its body lists unmet: queue-level (cross-home) choice summary, and WCAG 2.2 keyboard/axe evidence.
* PR #487 closed unmerged; #496 delivered the role-screen foundation.
* Defect found: `src/api/src/zava_forward/api/web/role-screens.js` on origin/main (18a14eab) fails `node --check`. Five screens (hazard-triage, data-operator, contractor-job-pack, resident-choice, plus one) lost their closing `}` and `});` through parallel merges, so the whole specialist module cannot load and the #232 screen is unusable. Tightly coupled to the deliverable.
* The list endpoint projection does not carry measure decisions; a core/API change is out of the tight slice. Bounded client-side option: fetch detail for the 20 homes on the current page.

## Remaining slice

1. Repair the syntax breakage.
2. Add a read-only page-level choice and update summary (no contact, no controls, unavailable homes marked Unknown).
3. Unit tests outside the package.

## Not delivered or unproven

* Browser keyboard/axe evidence is CI only; no Azure-live work.
* Research is desk-based hypothesis, validation remains #155.

## Correction cycle (PR #715 review threads)

Two unresolved Copilot threads on `role-screens.js` queue rows: (1) the paused or withdrawn column showed only the measure name, dropping state, version, scope and human-review need when a pause is followed by a newer Waiting answer; (2) the measure column attached the current status (for example Not recorded) to the historical answer's version and scope. Planning readiness: Ready. Merge of origin/main was clean; `node --check` passes.
