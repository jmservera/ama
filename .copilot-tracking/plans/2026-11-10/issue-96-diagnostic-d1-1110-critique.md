---
title: Issue 96 diagnostic D1 critique
description: Single author critique of the D1 plan
ms.date: 2026-11-10
---

## Execution and verdict

Critique executed once by the author, no nested agent. Verdict: Revise; all findings are compatible with the brief and applied directly.

## Findings and dispositions

* PC-1: Moving `working_review` between tests could change test discovery. Applied: it moves verbatim into the fixture and the 14-test count is a gate.
* PC-2: A fixture class deriving `TestCase` with no tests is collected harmlessly; the repository already does this (`ProcurementApiFixture`). Accepted.
* PC-3: Patching `provider.name` could be a test-only trick. Applied: it drives the real handler and route, so the production guard is genuinely exercised; the unit call is removed only because the production function is unannotated and production edits are barred.
* PC-4: The probe saw only errors in one module, but mypy stops at the first duplicate-module error, so more can appear. Applied: Phase 3 runs the whole configured check and any new error that needs production or core change stops D1.
* PC-5: Ruff pins must match 0.17.1 before format claims. Applied in Phase 3.
* PC-6: The qualification must be additive; the parent artifacts stay byte-identical. Applied in Phase 5 and verified by `git diff` on those paths.
* PC-7: Browser run must use the actual-holder lock without queueing. Applied in Phase 4.
