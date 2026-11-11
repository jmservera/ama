---
title: Issue 80 capacity C4 plan
description: Plan for the C3-R1 checker fix and the stop on the unexplained line-571 failure
ms.date: 2026-11-10
---

Task `issue-80-capacity-c4-1110`. Plan written after the two diagnostic observations, per the [research](../../research/2026-11-10/issue-80-capacity-c4-1110-research.md).

## Objective

Fix C3-R1 in `src/api/checks/capacity_browser_check.py` only, and stop on the unexplained line-571 failure.

## Phases

1. [ ] Replace the direct `route.fulfill(status=503, body="Unavailable")` in the C3 branch of `hold_capacity_read` with `inject(route)`. `inject` defaults to 503, registers the request in `expected_failures` and fulfils the same non-JSON `Unavailable` body, so behaviour is identical except for the registration. No duplicate or general whitelist; the flag, exact endpoint match, held sibling, 401 release point, assertions and timeout are unchanged.
2. [ ] Focused validation: Ruff check and format on the checker, Node syntax on unchanged `ops.js`, API 11, static 60. Each with its direct exit.
3. [ ] No whole `capacity_browser_check --axe` run in C4. The cause of the line-571 failure is unknown (not reproduced in 7 isolated runs), so a whole run would be blind; Root excluded that. The whole-run requirement stays open for a later Root admission.
4. [ ] One native review after the implement-done marker; commit; handoff.

## Out of plan

Any correction for line 571, app or role change, timeout change, removed or skipped assertion, pre-release of the 401, widened accepted errors, a second observation round, a C5.
