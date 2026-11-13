---
title: Issue 96 impact correction C3 plan (role-screen contract tests)
description: Prospective plan for one tests-only correction replacing two stale blanket assertions with precise discriminating contracts
ms.date: 2026-11-13
---

## Objective

Fix only the two tightly coupled contract regressions caused by the 96 saved-copy checker UI, with no product source change. Details: [details](../../details/2026-11-13/issue-96-impact-c3-0052-details.md). Research: [research](../../research/2026-11-13/issue-96-impact-c3-0052-research.md).

## Phases

* [ ] Phase 1 (done before this plan): failing-first reproduction of both failures on exact base `9085e85` in `rpi-96-impact-c3-0052`.
* [ ] Phase 2: independent critique once (rubber-duck, read-only); apply compatible findings.
* [ ] Phase 3: C3 implementation in `src/api/tests/test_role_screens.py` and `src/api/tests/test_role_screens_conformance.py` only.
* [ ] Phase 4: validation (RoleScreens + RoleScreenConformance once, FinanceGrantsScreens, ruff 0.17.1 and mypy 2.4.0 on the changed tests, held_copy browser 88 and role browser 47 under non-blocking heavy lock, pinned axe).
* [ ] Phase 5: freeze, original Review once, result file, STOP.

## Constraints

* One source-correction batch C3; at most one archive or env-only correction. No retry. New findings after C3 route to the root.
* No product source, CSS, HTML or helper edit; no 233 file; no waiver of the failed contracts.
