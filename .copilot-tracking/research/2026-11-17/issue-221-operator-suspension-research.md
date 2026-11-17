---
title: Issue 221 research, operator suspension, incident and restart record
ms.date: 2026-11-17
---

## Scope

Assess issue #221 against its six criteria on base eb51af5c9. Tier FOCUSED. No live drill, no invented approval.

## Evidence so far

* Criteria 1 to 4 are ticked on the issue; criteria 5 and 6 were restored to unchecked on 2026-11-16 (issue comments).
* `src/core/README.md` section "Operator incidents and constructed restart (#221)" states actual_hold stays true and no actual restart approval route exists while OD-35/RULE-020 evidence is unavailable.
* Criterion 5 needs an appointed human restart authority; criterion 6 needs a human-witnessed drill. Neither can be produced by code.

## Planning readiness

Pending measurement (targeted tests). Disposition: Research executed.

## Measurement (2026-11-17)

* `src/api` `python3 -m unittest test_operator_suspension -q` with worktree `src` paths on PYTHONPATH: 18 tests, OK, 43.6 s. The pip-installed packages point at the main checkout, so worktree paths were set explicitly.
* Existing tests already assert `actual_hold` stays true after constructed restart (test_operator_suspension.py:786, 924, 1040) and that default `restart_authority` begins `Unavailable` (line 969; continuity.py:439, 532).
* No defect reproduced. Criteria 5 and 6 are blocked on human actions (OD-35/RULE-020 appointment; witnessed drill), not code.

Planning Readiness: Ready. Smallest change: record this assessment; no source or test edit, since coverage exists.
