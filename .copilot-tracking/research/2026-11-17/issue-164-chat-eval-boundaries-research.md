---
title: Issue 164 chat evaluation boundaries research
ms.date: 2026-11-17
---

## Scope

Issue #164, FOCUSED tier. Evidence and test only; no grounding or provenance code (#1641), no core mssqlstore (#1818).
Research disposition: executed. Planning Readiness: Ready.

## Measurements (base eb51af5c9)

* `src/agents/tests/test_chat_eval.py`: 60 tests OK (`PYTHONPATH=src:../core/src python3 -m unittest tests.test_chat_eval`, from `src/agents`).
* Ticked criteria are already covered by these tests, including the registered, disabled chat task with its accountable function.
* Unticked criteria (approved thresholds, actual-model binding, human exercises, finite real-call authority) need owner or human evidence and cannot be proved offline.

## Reproduced defects in `chat_eval.threshold_checks` / `enablement_decision`

Probe of `enablement_decision(report, thresholds)` with constructed thresholds:

| Input | Observed | Expected |
| --- | --- | --- |
| `minimum_rates={"abstention":"high"}` | uncaught `TypeError` | check outcome `insufficient` |
| `minimum_rates={"abstention":-1}` | `pass` | `insufficient` (invalid floor) |
| `maximum_critical_error_rate=True` | `pass` | `insufficient` |
| `maximum_critical_error_rate=5` | `pass` | `insufficient` (outside 0..1) |
| `approved_by="  "` | threshold checks applied as approved | treated as not approved |

Enablement stayed `insufficient`/`disabled` in every case, so no enablement leak; the defects are an unhandled crash and malformed thresholds recorded as `pass`.

## Selected approach

Validate threshold values and approver as strings with content before comparison; invalid values yield an `insufficient` check. Add regression tests. Leave the NaN case as is (already `fail`).
