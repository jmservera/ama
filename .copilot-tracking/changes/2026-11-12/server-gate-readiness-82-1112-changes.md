---
title: Issue 82 funding readiness fail-closed changes
ms.date: 2026-11-12
task_id: server-gate-readiness-82-1112
---

## Summary

One initial increment, Refs #82 only. Base `cd81888e4a81cf4c712d50b357ca900fd5c8c06b`. Plan: [plan](../../plans/2026-11-12/server-gate-readiness-82-1112-plan.md); critique: [critique](../../plans/2026-11-12/server-gate-readiness-82-1112-critique.md) (conformant after fixes, CR-01 to CR-04 applied).

## Changes

* `src/core/src/zava_forward/core/store.py`, `Store.gate_reasons`: funding is confirmed only for an explicit `True` (`c.get("funding_ok") is not True`). Reason text unchanged. Effect: an absent `funding_ok` no longer raises `KeyError` (HTTP 404 "Case not found." on advance, a lookup failure on detail); a non-boolean value no longer reads as confirmed in `status_line`/`detail["gate"]`.
* `src/core/tests/test_gates.py`, class `FundingReadinessTests`: `True` positive control (no funding reason, status "Ready"); `None`, `False`, `"yes"`, `1` and absent each produce one funding reason, a non-"Ready" status, a matching `detail["gate"]` entry, a `GateError` on `advance` and an unchanged stage.
* `src/api/tests/test_mvp.py`: HTTP test, absent `funding_ok` on ZF-3 returns 409 "Not ready yet." with the funding reason and leaves the stage unchanged.

## Evidence (all in `.copilot-tracking/evidence/2026-11-12/server-gate-readiness-82-1112/`)

* [repro-before.out](../../evidence/2026-11-12/server-gate-readiness-82-1112/repro-before.out): probe before the change (absent: `KeyError`; `"yes"`: readiness `[]`).
* [tests-before.out](../../evidence/2026-11-12/server-gate-readiness-82-1112/tests-before.out): failing-first, exit 1 (1 error for absent, 2 failures for `"yes"` and `1`, HTTP `404 != 409`); the `True` control passed.
* [tests-after-focused.out](../../evidence/2026-11-12/server-gate-readiness-82-1112/tests-after-focused.out): `core/tests` `test_gates` 22 OK exit 0; `api` `tests.test_mvp` 22 OK exit 0.
* [core-tests-after.out](../../evidence/2026-11-12/server-gate-readiness-82-1112/core-tests-after.out) and [api-tests-after.out](../../evidence/2026-11-12/server-gate-readiness-82-1112/api-tests-after.out): broader discovery runs (exit 1, see limits). [after.out](../../evidence/2026-11-12/server-gate-readiness-82-1112/after.out) records import origin and exits.
* [lint.out](../../evidence/2026-11-12/server-gate-readiness-82-1112/lint.out), [lint-api.out](../../evidence/2026-11-12/server-gate-readiness-82-1112/lint-api.out): ruff check, ruff format --check, mypy on the touched test files.

## Actual limits

* Imported package origin verified: a session-folder venv with pip editable installs of this worktree's `src/core`, `src/agents`, `src/api`; `zava_forward.core.store` resolved to this worktree. The previously installed packages pointed at the primary checkout and were not used. No `PYTHONPATH` to source trees; only the documented test-directory path `../core/tests:../agents/tests` for api tests.
* Core discovery (3137 tests, exit 1): all 50 failures/errors are in `test_device_registry_azure`, caused by a missing `azure.iot.hub` dependency (`ModuleNotFoundError`); unrelated to funding and gates; not installed. API discovery (2825 tests, exit 1): 10 import errors, all `ModuleNotFoundError: No module named 'playwright'` for browser harness modules; unrelated. All other tests passed, including the new ones. Discovery ran before the test file was reformatted by ruff; the final files were re-run focused (exit 0).
* Lint: user-installed ruff 0.17.3 and mypy 2.4.1 (project pins 0.17.1 and 2.4.0). `store.py` is excluded from the project format check and lint (ADR 0006 legacy list) so only the test file was lint/type checked. `test_mvp.py` already failed `ruff format --check` at base (pre-existing, not reformatted); ruff check and mypy pass. Review RV-02 noted one blank line after the new `import copy` that ruff would add; it was added after Review (whitespace only) and the focused api test re-run OK (22 tests), not re-reviewed.
* Not run: complete local gate, SQL Server/MSSQL suite (the SQL stores inherit `gate_reasons`), browser harness, hosted CI, live or model execution. No push, PR, issue edit, tick or closure.

## Declared non-claims and out of scope

* `home_case.py` (reads `case["funding_ok"]`), `taskqueues.py` (`not case.get("funding_ok")`) and `chat_case_answers.py` (shows "confirmed" for any truthy value) are separate paths, not edited (CR-03, Review RV-01).
* For a non-boolean value the denial text on `advance` changes from the booking-gate wording ("Funding confirmed: no evidence recorded, so this cannot pass.") to the legacy funding wording; both are denials (CR-04).
* The `finance` gate kind still has no booking gate implementation; implementing one would be a new rule family needing a named authority and is not done.
* Rule records remain unreviewed exercise fixtures; criteria 1, 2 and 4 of #82 are not proven or ticked; no professional rule ratification or human approval is implied.
