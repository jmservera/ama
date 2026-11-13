---
title: Issue 82 funding readiness fail-closed review
ms.date: 2026-11-12
task_id: server-gate-readiness-82-1112
---

## Execution

One post-implementation Review, executed once on the uncommitted working diff over base `cd81888e4a81cf4c712d50b357ca900fd5c8c06b`, by a separate read-only agent (explicit model Claude Sonnet 5.5). It read the diff and the research, plan, details, critique, changes and evidence records, grepped callers, and re-ran `test_gates` (22 OK) and `tests.test_mvp` (22 OK) with the worktree-origin venv. It did not re-run the broad discovery suites. Not repeated for this task.

## Outcome

Conformant for the bounded increment. No open material finding. Assessed boundary: `Store.gate_reasons` funding condition and its two new tests; not the whole of #82.

* The change only adds denials; absent, `None`, `False`, `"yes"` and `1` give the same funding reason; safety, resident and booking gates still run after it; no new rule, gate family or approver.
* Tests are failing-first and non-tautological (`tests-before.out`); the `True` control passes before and after.
* Callers: `gate_reasons` has three callers, all in `store.py`; SQL and MSSQL stores inherit it and do not reference `funding_ok`; the only writer sets `True`.
* Recorded limits match the `.out` files.

## Findings and routing

| ID | Severity | Finding | Routing |
| --- | --- | --- | --- |
| RV-01 | Low | `chat_case_answers.py:79` shows "confirmed" for any truthy `funding_ok`, `taskqueues.py:295` treats truthy non-boolean as confirmed and `home_case.py:156` raises `KeyError` for an absent key. Display inconsistency; no gate is weakened. | Later user-selected work under #82 (Research first); `chat_case_answers.py` added to the declared non-claims in the changes record. |
| RV-02 | Very low | One blank line after the new `import copy` in `test_mvp.py` failed `ruff format`; the rest of the file's format failure is pre-existing. | Corrected after Review (whitespace only, focused test re-run OK), not re-reviewed; recorded in the changes record. |

## Independent gates still open

Independent exact-head assessment, human approval, hosted CI, the complete local gate, the SQL-backed suite, named professional rule review and criteria 1, 2 and 4 of #82 remain unproven. No tick or closure is implied.
