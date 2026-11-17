---
title: Issue 122 research, service continuity, versioning and exportability
ms.date: 2026-11-17
---

## Scope

Assess issue #122 against main eb51af5c9 (evidence only, demo-first, desktop-only). 10 of 11 criteria are ticked; the open one is the witnessed authorized drill. Out of scope: #1818 and #1641 (core mssqlstore, chat grounding). Tier FOCUSED.

## Status

Research opened; measurements follow in this file.

## Measurements on main eb51af5c9 (2026-11-17, sequential, no heavy services)

| Check | Result |
| --- | --- |
| `src/api` test_operator_suspension.py | 18 tests OK |
| `src/api` test_continuity.py | 22 tests OK |
| `src/api` test_continuity_epoch_export.py | 77 tests OK, 39 skipped (owned local MSSQL opt-in; not run here) |
| `src/api` test_epic149_manual_fallback_continuity.py | 10 tests OK |
| `src/core` test_recovery.py, test_version.py | 15 and 3 tests OK |

No defect reproduced. Running `python3 -m unittest tests.<module>` from `src/api` without `tests` on PYTHONPATH fails to import `test_assistants`; that is a harness invocation quirk, not a product defect.

## Criteria assessment

* Criteria 1 to 3 and RAI criteria 1 to 7: covered by the tests above plus merged PRs cited in the issue comments (#269, #398, #1709, #1752, #1787). Constructed actors only.
* RAI criterion 8 (witnessed authorized drill): unmet. [operator-suspension-drill-protocol.md](../../../docs/reference/method/operator-suspension-drill-protocol.md) is a blank protocol that an agent must not complete; the continuity code states the drill is an owner activity. MSSQL-backed epoch tests are skipped without an owned local instance, so no SQL drill evidence was gathered here.

## Planning Readiness

Ready: evidence-only. No source fix is warranted because the measurement found no reproducible defect, so no regression test is added.
