---
title: Issue 128 research, journey register design_ref anchors
description: Assessment of #128 against main eb51af5c9 and one measured reproducible defect
ms.date: 2026-11-17
---

## Scope and disposition

* Issue #128, demo-first, desktop-only, evidence only. Disposition: executed.
* Base `origin/main` eb51af5c9ab0b1353ac380fc8960ee8dd96d17c4. Out of scope: #1818, #1641.
* Planning Readiness: Ready.

## Criteria status on main (no change expected from this task)

* Keyboard and screen reader testing: scripts exist (production UX acceptance protocol, WCAG baseline), no human run. Unmet, human-only.
* Missing data and incomplete appointments get human review: already ticked, `journey_register.human_review_route`.
* Research protocol agreed, aggregate only: draft only, no named agreement. Unmet, human decision.
* All 8 RAI cohort criteria already ticked (merged #1782 per issue comments).

## Measurement

* Each of J1-J6 and R1 in `customer-journeys/residents.md` states a non-digital equivalent (7 of 7, already tested by `test_resident_journey_design`).
* `journey_register.draft()` sets `design_ref` to `DESIGN_DOC#j1` .. `#r1`. The headings are `### J1: Choose each proposed measure` etc., so the GitHub anchors are `#j1-choose-each-proposed-measure`. Reproduced with a slug check: 0 of 7 `design_ref` anchors resolve.
* No test checks that `design_ref` resolves, so the defect is undetected.

## Selected gap

Dangling `design_ref` anchors in the journey ownership register (traceability from register row to the journey design that holds the manual alternative). Smallest fix: derive the anchor from the journey name and add a regression test that resolves it against the document headings.

## Not delivered by this task

Human screen reader and keyboard runs, owner assignment, protocol agreement. No criterion is newly proven; use `Refs #128`.
