---
description: "RPI Plan: Map sensor browser regression"
ms.date: 2026-11-23
---

# RPI Plan: Map sensor browser regression

## Task Metadata

Task: `map-sensor-browser-regression`, automatic child of `lazy-map-sensors`.
Agent-owned decisions; no helper needed for this bounded trace.

## Executive Summary

Correct the employee acceptance observer to read the map count rather than
the nested sensor status. Local Chromium reproduced the hosted rosterless
failure in 124.5 seconds. Planning is complete and ready for implementation.

### What You May Not Know

No application change is needed. The expanded sidebar now contains multiple
status regions; hidden descendants still match DOM queries.

## Phase Checklist

P02 changes the employee browser observer and its existing regression suite;
no production connections change.

<!-- rpi:phase id=P02 -->
### [x] P02: Restore accurate employee map acceptance

Goals: The browser observer accepts correctly rendered maps and rejects
incorrect counts, while home sensor readings remain lazy.

Dependencies: Reproduced hosted failure and confirmed sidebar DOM structure.

Changes in the map: Employee observer and employee acceptance tests.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Scope map count selection

Goals: Nested sensor status cannot shadow or impersonate the map count.

Requirements: `FR-004`, `NFR-004`.

Details: Narrow the count selector to direct sidebar children. Add at most
one browser DOM regression method in the existing employee test file, with
positive and negative count controls. Remove no tests. Canonical code is the
employee browser script; there are no generated targets.

References:
* [src/api/checks/employee_acceptance_check.py](../../../src/api/checks/employee_acceptance_check.py)
* [src/api/tests/test_employee_acceptance_check.py](../../../src/api/tests/test_employee_acceptance_check.py)
* [.copilot-tracking/research/2026-11-23/map-sensor-browser-regression-research.md](../../research/2026-11-23/map-sensor-browser-regression-research.md)

Dependencies: None.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Validate failed acceptance and retained behavior

Goals: Reproduce the failed CI command successfully without changing its
semantic acceptance criteria.

Requirements: `FR-004`, `NFR-004`.

Details: Run the maintained employee browser entry point, focused lazy-map
and manifest/inventory tests, API lint/type checks and subsequent synthetic
browser commands where their prerequisites exist. The manifest recipe hash
binds `workbench_browser_check.py`, not the employee observer: retain that
unchanged hash and run both integrity test modules. Record unavailable,
skipped and pending checks explicitly. Use existing acceptance tests for
semantic browser coverage; no duplicated browser framework or gate bypass.

References:
* [.github/workflows/src-ci.yml](../../../.github/workflows/src-ci.yml)
* [src/api/README.md](../../../src/api/README.md)

Dependencies: `P02-T01`.

## User Decisions and Requirements

### Confirmed User Direction

* Fix the failed check merged in PR 2327.
* Preserve lazy selected-home readings and the opt-in stale/offline bulk
  filter from the parent task.
* Publishing the corrective branch requires separate permission.

### Planning Decisions and Feedback

| Group | Status | Owner | Decision or feedback item | Impact |
| --- | --- | --- | --- | --- |
| D3 | Settled | Agent | Count targeting: direct children exclude hidden card status; source DOM and local failure confirm cause. | P02-T01 preserves exact count equality. |
| D4 | Settled | Agent | Focused tier: selector repair preserves existing acceptance semantics and strengthens targeting; no workflow, permissions, packages, infrastructure, SQL or security-control change. Positive/negative controls confirm it. | P02-T02 focused local checks plus exact-head independent review and hosted CI. |

No unresolved material decision. No user walkthrough required.

## Planning Readiness and Next Step

Implementation complete, including `P02-T01` and `P02-T02`. All planned local
checks passed. Publication permission, independent exact-head review and
hosted checks remain outstanding.

## Functional Requirements

* `FR-004`: The employee observer checks the actual map count, list and
  markers; nested sensor status cannot substitute for the count.

## Non-Functional Requirements

* `NFR-004`: Preserve admission checks and lazy sensor behavior. Demonstrate
  the repaired hosted-browser command and focused regressions locally.

## Risks and Open Questions

| Risk | Task | Disposition |
| --- | --- | --- |
| Future sidebar nesting changes | P02-T01 | Regression makes count targeting explicit. |
| Later browser stages were not executed by failed hosted job | P02-T02 | Exercise locally where possible; hosted exact-head results remain necessary. |

## Sources

PR 2327 and Actions run 45216338816 job 137838807298; child research above.
No new business requirement, BRD/PRD or ADR decision: correction restores
the existing browser acceptance contract.

## Critique Disposition

Skipped by inherited child-task default, not reported as passed.

## Artifact Self-Check

Scope, semantic/regression ownership, no removals, maximum one added test,
canonical target, validation and publication boundaries recorded.

## Follow-Up Items

* None.

## Handoff

Automatic implementation may proceed. Independent publication assessment,
push permission, hosted checks and owner merge remain separate gates.
