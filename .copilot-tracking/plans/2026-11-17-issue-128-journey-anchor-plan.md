---
title: Issue 128 plan, resolve journey register design_ref anchors
ms.date: 2026-11-17
---

* [ ] Phase 1: derive `design_ref` anchor from the journey heading slug in `src/core/src/zava_forward/core/journey_register.py`.
* [ ] Phase 2: add a regression test in `src/core/tests/test_journey_register.py` resolving every anchor against `residents.md` headings.
* [ ] Phase 3: run targeted core tests, ruff format check, mypy for `src/core`; update `equity-journey-test-plan.md`, knowledge-base log.

Tier: FOCUSED (no SQL, security, infra or deployment). Details:
[details](../details/2026-11-17-issue-128-journey-anchor-details.md). Critique:
[critique](../critique/2026-11-17-issue-128-journey-anchor-critique.md).
