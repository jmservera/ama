---
title: Issue 82 funding readers fail-closed changes (follow-up RV01)
ms.date: 2026-11-12
task_id: funding-readers-82-2250
---

## Changes

Base `dc9fb68e024f280c435b97accbae2a8becde2786`; prospective RPI evidence committed first as `c4fe717ef`. Refs #82 only.

| File | Change |
| --- | --- |
| `src/core/src/zava_forward/core/chat_case_answers.py` | `funding_ok` fact is "confirmed" only when `is True`. |
| `src/core/src/zava_forward/core/taskqueues.py` | Funding blocker raised unless `funding_ok is True`; `MEMBERSHIP_REVISION` 2 to 3 so persisted SQL `queue_blocked` flags recompute (critique CR-01). |
| `src/core/src/zava_forward/core/home_case.py` | `funding_confirmed` is `case.get("funding_ok") is True`: always a bool, no `KeyError`. |
| `src/core/tests/test_chat_case_answers.py`, `test_taskqueues.py`, `test_home_case.py` | One regression each, parameterised over `True`, `False`, `None`, `"yes"`, `"false"`, `1` and absent. |
| `src/core/tests/test_sqlqueues.py` | Stale revision-2 membership refreshes to blocked for non-boolean funding, with case rows and ledger head unchanged (CR-01). |
| `src/api/tests/test_home_case_api.py` | Absent `funding_ok` returns 200 and `funding_confirmed` `False` (CR-02). |

No change to `gates.py`, `store.py`, any gate, role, consent, safety or approval logic; no helper added. `True` stays confirmed.

## Evidence (under `.copilot-tracking/evidence/2026-11-12/funding-readers-82-2250/`)

* Before: `repro-before.out`; failing-first `tests-before-core.out` (13 failures, 2 errors in the 50 tests of the four modified core modules) and `tests-before-api.out` (1 failure).
* After: `repro-after.out`; `tests-after-core.out` 747 tests OK (165 skipped, opt-in SQL Server harness) over 13 core modules (the four modified modules plus `test_chat_case_funding_sources`, `test_sqlreads`, `test_gates`, `test_buildings`, `test_funding_automation_boundary`, `test_quality_procurement`, `test_resident_decisions`, `test_consultation_controls`, `test_bulk_edits`); `tests-after-api.out` 65 OK (`test_home_case_api`, `test_task_queue_api`, `test_mvp`, `test_content_standard`, `test_programme_screen`); `tests-final-core.out` 50 OK after the formatting fix.
* Lint: `lint-core.out` and `lint-api.out`: pinned ruff 0.17.1 check and format pass on touched files; mypy 2.4.0 on `src/core` passes (298 files). API mypy not run.
* Negative control: `negative-control-revision.out`: with `MEMBERSHIP_REVISION` reverted to 2 the new SQL regression fails (`[] != ['ZF-00001']`); restored to 3 afterwards. An earlier attempt of this control in the same session ran before the edit took effect and showed a pass; it is superseded by this run.

## Amendments, divergences and limits

* The first version of `test_sqlqueues` was over one line limit; reformatted (no behaviour change) and rerun.
* Environment: pip-only venv outside the repository, worktree editable installs, imported origin verified under this worktree; no `uv`, no source `PYTHONPATH` (test helper directories only for the API tests and the probe).
* Not run: complete local gate, SQL Server suites, browser harness, API mypy, hosted CI, other readers outside the write surface (`export_fields.py`, `resident_preview_fixture.py`, `ai_eval.py`).
* No publication, push, PR, issue, tick or approval. Not human review, resident or professional ratification.
