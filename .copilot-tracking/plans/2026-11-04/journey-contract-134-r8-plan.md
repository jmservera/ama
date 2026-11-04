---
title: Issue 134 slice 4 plan
ms.date: 2026-11-04
---

* [x] Phase 1: add `perspective_walkthroughs` register and `check` (core). Details: [details](../../details/2026-11-04/journey-contract-134-r8-details.md)
* [x] Phase 2: tests (met rejected, missing profile/element, evidence not found, unknown profile, unmet reasons).
* [x] Phase 3: focused validation, ruff, mypy, review, PR with `Refs #134`.

Critique (single pass, self): the register must never record `met`, must tie to manifest IDs and PRD names, and must fail on missing evidence files. Applied directly.
