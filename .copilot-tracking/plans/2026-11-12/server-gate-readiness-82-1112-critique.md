---
title: Issue 82 funding readiness fail-closed critique
ms.date: 2026-11-12
task_id: server-gate-readiness-82-1112
---

## Execution

One independent critique of the final candidate plan, executed before any code, by a separate read-only agent (explicit model Claude Sonnet 5.5). It was a source trace only; the agent could not run Python and did not run the failing-first or fixed behaviour. Not repeated for this task.

## Verdict

Conformant after fixes. No blocking issues; no scope or authority overreach.

## Confirmed by the critique

* The gap is real and distinct: `gate_reasons` reads `c["funding_ok"]` (KeyError when absent), reached from `status_line`, `detail` and `advance`; `server.py` maps KeyError to 404 "Case not found."; no existing test covers the store path (`test_gates.py` tests only `gates.booking_gates`).
* SQL stores keep the case as a JSON body, inherit `gate_reasons` without override; real writers store booleans. `is not True` matches `isinstance(funding, bool)` in `gates.booking_gates`, so no regression on real data.

## Findings and dispositions

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| CR-01 | Non-blocking | `None`/`False` already give the funding reason, and `"yes"` already denies `advance` via the booking gate; only absent (KeyError) and `"yes"` readiness/status/detail fail today. | Applied: details name absent as the failing `advance`/`detail` case and `"yes"` as the failing readiness case (`gate_reasons`, `status_line`, `detail["gate"]`); `None`/`False` stay unchanged-behaviour guards; `True` positive controls added. |
| CR-02 | Non-blocking | HTTP test construction undefined. | Applied: write a copy of `DATA` with ZF-3 `funding_ok` removed (ZF-3 is at final checks), sign in as Sam, POST advance; assert 409, funding reason, no 404, stage unchanged. |
| CR-03 | Suggestion | `home_case.py:156`, `taskqueues.py:295` read funding separately. | Applied: declared out of scope in the changes record; not edited. |
| CR-04 | Suggestion | For `"yes"` the denial wording changes from the booking-gate text to the legacy funding text. | Applied: recorded in the changes record; both are denials, nothing weakened. |

No finding conflicted with a confirmed owner decision. No significant or divergent issue required a user decision.
