---
title: Issue 82 funding readers fail-closed details (follow-up RV01)
ms.date: 2026-11-12
task_id: funding-readers-82-2250
---

## Phase 2: tests then change

Production edits, one expression each:

* `src/core/src/zava_forward/core/chat_case_answers.py` line 79: `"confirmed" if detail["funding_ok"] is True else "not confirmed"`.
* `src/core/src/zava_forward/core/taskqueues.py` line 295: `if case.get("funding_ok") is not True:`; block text unchanged. Per critique CR-01, also bump `MEMBERSHIP_REVISION` from 2 to 3 (line 7) so persisted SQL `queue_blocked` flags recompute.
* `src/core/src/zava_forward/core/home_case.py` line 156: `"funding_confirmed": case.get("funding_ok") is True` so the value is always a bool and an absent key does not raise.

Regressions, in existing files, written once:

* `tests/test_chat_case_answers.py`: for `"yes"`, `1`, `"false"` and `None`, `case_facts({"funding_ok": value}, ...)["funding_ok"]` is "not confirmed"; for `True` it is "confirmed"; an absent key yields no fact.
* `tests/test_taskqueues.py` (`QueueDefinitions`): at stage "Final checks before ordering", `funding_ok` in `False`, `None`, `"yes"`, `1`, `"false"` and absent produce a "Final checks: funding" blocker that is a current stop; `True` produces none.
* `tests/test_home_case.py`: `home_case_view` for an absent key returns `funding_confirmed` `False` (no `KeyError`); `"yes"`, `1` and `None` give `False`; `True` gives `True`; run over the existing JSON and SQL store loop only where the helper already supports it.
* `tests/test_sqlqueues.py` (critique CR-01): a case at "Final checks before ordering" with `funding_ok` `"yes"`, a persisted revision-2 `queue_context` fingerprint and a stale `queue_blocked=0` flag; after reopening, the case is in the blocked queue and the case rows and ledger head are unchanged (modelled on `test_old_certified_memberships_refresh_without_case_or_audit_writes`).
* `src/api/tests/test_home_case_api.py` (critique CR-02): one assertion that an absent `funding_ok` returns 200 with `funding_confirmed` `False`.

Failing-first: run the new tests before the change, keep output at `.copilot-tracking/evidence/2026-11-12/funding-readers-82-2250/tests-before.out`.

## Phase 3: validation (focused)

* The four modified or impacted core test modules plus `test_gates.py`, `test_chat_case_funding_sources.py`, `test_buildings.py`, and `src/api` `test_home_case_api.py`, `test_task_queue_api.py`.
* ruff check and ruff format --check on touched source and test files, mypy on `src/core`, using a pip-only venv with worktree editable installs; imported package origin verified; no source `PYTHONPATH` workaround (tests directory only for test helpers); actual exit codes recorded, no tailed runner masking.

## Narrow dependent callers

`app.js:1344` renders `home.funding_confirmed` truthily, so a bool is compatible. `chat_case_answers._funding_missing` keys on the "not confirmed" string, unchanged. The SQL store reuses these readers; its MSSQL-backed suite is not run (declared limit).
