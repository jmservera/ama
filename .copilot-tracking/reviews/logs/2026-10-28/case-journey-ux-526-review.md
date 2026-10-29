---
title: Case journey 526 independent post-implementation review
description: Original one-pass review record for the feature and continuation
ms.date: 2026-10-28
---

## Opening Review State

Task 526, stable slug case-journey-ux-526, automatic mode. Review the full
origin/main...working candidate, implementation 02e032cd plus continuation.
Evidence is reconciled and ready at the local constructed-data boundary.
Acceptance basis: issue #526, supplied design, original PC-001..005 dispositions,
and current continuation plan/details/changes. First comparison: retained
navigation/drafts, review authority, exact validation and local-runner parity.
Read-only source boundary: no .env, private datasets, Azure or source mutation.
Only this original Review record may be authored during this phase.

## Compared artifacts

* .copilot-tracking/research/2026-10-28/case-journey-ux-526-research.md
* .copilot-tracking/plans/2026-10-28/case-journey-ux-526-continuation-plan.md
* .copilot-tracking/details/2026-10-28/case-journey-ux-526-continuation-details.md
* .copilot-tracking/reviews/plans/2026-10-28/case-journey-ux-526-plan-critique.md
* .copilot-tracking/changes/2026-10-28/case-journey-ux-526-continuation-changes.md
* docs/reference/research/ux/employee-case-workspace-redesign.md
* External validation: /tmp/ama-526-continuation-1826

## Execution and outcome

Execution: Complete independent assessment. Outcome: Defects found.
Candidate not ready for the final full gate. Original verdict is retained
regardless of subsequent repairs.

## Findings and routing

| ID | Severity | File | Defect | Route |
| --- | --- | --- | --- | --- |
| RV-001 | High | tools/rpi-checks.py | Journey command has only safety PYTHONPATH; regulatory fixture import fails before the harness runs | Later rpi-implement |
| RV-002 | High | src/api/src/zava_forward/api/web/app.js | Successful action clears dirty state for the whole focused card, discarding other action drafts | Later rpi-implement |
| RV-003 | Medium | src/api/src/zava_forward/api/web/app.js | Synchronous field restoration precedes async proposal rendering; review edits disappear | Later rpi-implement |
| RV-004 | Medium | src/api/src/zava_forward/api/web/case-workspace.js | Document-read review insertion is outside count observers and emits no count event | Later rpi-implement |

Reviewer independently reproduced RV-001 with a bytecode-disabled import-only
probe (ModuleNotFoundError: regulatory_fixture). Shipped refresh closure
execution in a lightweight Node model demonstrated RV-002 clearing both submitted
and unrelated draft markers. Async loader/helper sequencing demonstrated RV-003
capturing two dirty review fields, restoring against no replacement controls,
then displaying a blank reason. Document read insertion establishes RV-004.

PC-001 remains incomplete for same-card and asynchronous review drafts; PC-002
remains incomplete for document counts. PC-003 retained assertions, PC-004
stacked fallback and PC-005 measured browser matrix are supported.
Native manual tabs, Back/heading focus, stage mapping/evidence exceptions,
case/login isolation and human/server authorization boundaries were assessed.
No demonstrated cross-case disclosure or authority expansion was identified.

Current results substantiate the executed unit/browser boundary, not the
unexecuted full gate. Fresh Web Interface Guidelines applied subject to Fluent,
ASCII and sentence-case standards. No blanket accessibility conformance.
Chat remains advisory with an explicit separately requested proposal-review path.
Screen-reader, real staff usability and post-deploy acceptance remain owner
residuals. No receipt, hosted-check or human acceptance approval is established.

## Final handoff

The user explicitly authorized all review defect repairs. RV-001..004 route to
the separately recorded later Implement invocation, not a repeated Review or
rewritten verdict. Preserve this artifact. After repair validation, commit the
candidate and require the complete gate, receipt/current-main verification and
independent exact-head assessment before topic push and PR.
