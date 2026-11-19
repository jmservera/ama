---
title: Issue 107 old-image SQL probe review
description: Single post-implementation review of the test-only older-image SQL probe
ms.date: 2026-11-17
---

## Execution

One review by the code-review agent over the untracked probe, worker, tests and README section. No second review was run.

## Findings and disposition

| Finding | Severity | Disposition |
| --- | --- | --- |
| Larger-allowance step could pass without observing a refusal (raised error, no task state check) | High | Fixed in the same candidate: the step now needs no raised error and the task disabled, else INSUFFICIENT; test added |
| Raised re-invoke counted as a violation | Medium | Fixed: now INSUFFICIENT; test added |
| A later failed control downgraded a real violation | Medium | Fixed: any observed violation is VIOLATED, insufficiencies are listed beside it; test added |
| Cleanup not exception-safe on docker timeout | Medium | Fixed: per-container try/except for timeout and OS errors, report still written |

The fixes were re-checked only by ruff, mypy strict and the new unit module (31 tests with the existing restart module, OK). They were not independently re-reviewed; the coordinator's exact-head review owns that.

## Outcome

Conformant for the stated bounded, test-only scope at lower fidelity. The actual older-image run, the disposable SQL container and the docker code path are unexecuted here, so the candidate stays ACTUAL OLD-IMAGE SQL EVIDENCE MISSING, NOT PUBLISHABLE.

## Routed follow-up

The coordinator runs the README continuation with the pinned image and a disposable SQL Server. The first real run may expose untested docker or MSSQL adapter defects, to be fixed as a separate bounded change.
