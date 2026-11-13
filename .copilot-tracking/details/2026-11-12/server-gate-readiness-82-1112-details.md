---
title: Issue 82 funding readiness fail-closed details
ms.date: 2026-11-12
task_id: server-gate-readiness-82-1112
---

## Phase 2: tests then change

Production edit (one line) in `src/core/src/zava_forward/core/store.py`, `Store.gate_reasons`:

* from `if not c["funding_ok"]:` to `if c.get("funding_ok") is not True:`; reason text unchanged ("Funding has not been confirmed. Owner: ... Next action: check the funding and record it.").

Tests, added to `src/core/tests/test_gates.py` (class `FundingReadinessTests`) and `src/api/tests/test_mvp.py` (HTTP), per critique CR-01 and CR-02:

* Store, ZF-3 with `funding_ok` absent: `Store.gate_reasons`, `store.detail("ZF-3")` and `store.advance` do not raise `KeyError`; `advance` raises `GateError` mentioning funding and the stage is unchanged; `detail["gate"]` contains the funding reason.
* Store, `funding_ok` `"yes"`: `Store.gate_reasons` contains the funding reason, `Store.status_line(c)` is not "Ready", `detail["gate"]` contains it.
* Guards, unchanged behaviour: `None` and `False` give the funding reason; `True` gives no funding reason and `status_line` is "Ready" when nothing else blocks.
* HTTP: write a copy of `DATA` with ZF-3 `funding_ok` removed into a temporary store file, sign in as Sam, POST `/api/cases/ZF-3/advance`: 409 (not 404), `error` "Not ready yet.", reasons include "Funding has not been confirmed"; ZF-3 stage unchanged.

Failing-first: run the new tests before the change and keep the output at `.copilot-tracking/evidence/2026-11-12/server-gate-readiness-82-1112/tests-before.out`.

## Phase 3: validation (focused)

* New tests, `core/tests/test_gates.py`, `api/tests/test_mvp.py`, plus store tests that call `gate_reasons`/`detail`/`status_line` found by grep.
* ruff check and ruff format --check on touched files; mypy if the project configuration covers them.
* Use the venv at the session folder with worktree editable installs; verify imported package origin; actual exit codes recorded, no tailed runner masking.

## Narrow dependent callers

`gate_reasons` callers: `status_line`, `detail`, `advance` (all in `store.py`). Effect: a case with non-boolean/absent funding no longer reads as ready. The SQL store inherits the method; its suite is not run (declared limit).
