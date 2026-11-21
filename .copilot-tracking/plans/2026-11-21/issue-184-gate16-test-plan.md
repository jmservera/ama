---
title: Issue 184 gate run16 test fix plan
ms.date: 2026-11-21
---

# Plan

* [x] Phase 1: replace the `triggerType: 'Manual'` needle with the conditional expression, assert `param cronExpression string = ''` (default empty so manual) and the manual/schedule config selectors.
* [x] Phase 2: run test_live_control, the whole src/api suite sequentially, ruff and mypy.

Details: .copilot-tracking/details/2026-11-21/issue-184-gate16-test-details.md

## Critique (one pass)

* Verdict: proceed. Execution: done.
* Asserting the exact expression pins the Bicep behaviour without changing it; the default-empty param assertion proves the default stays manual.
* Rejected: rendering Bicep with az to prove manual output; unnecessary for a source-contract test and outside scope.
