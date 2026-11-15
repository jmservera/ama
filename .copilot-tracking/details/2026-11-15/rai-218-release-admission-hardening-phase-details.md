---
title: "Phase Details: Live Release Admission & Readiness Hardening (#218 Child)"
description: "Evidence-grounded implementation details for child task rai-218-release-admission-hardening"
author: "GitHub Copilot"
ms.date: "2026-11-15"
---

* Task ID: `issue-218-rai-release-admission-hardening`
* Task Slug: `rai-218-release-admission-hardening`
* Plan Artifact: `.copilot-tracking/plans/2026-11-15/rai-218-release-admission-hardening-plan.md`
* Research Artifact: `.copilot-tracking/research/2026-11-15/rai-218-release-admission-hardening-research.md`

<!-- rpi:phase id=P01 -->
## Phase P01: Harden Live Release Binding Selection and Read-Only SQL Readiness Assessment

* Phase Goal: Close `RV-001` and `RV-002` in `src/core` while preserving isolated bare-dict unit test behavior and read-only SQL readiness semantics.
* Write Boundary: `src/core/src/zava_forward/core/rai_release.py`, `src/core/src/zava_forward/core/assistant_release.py`, `src/core/src/zava_forward/core/rai_control_plane.py`.

<!-- rpi:task id=P01-T01 -->
### Task P01-T01: Harden `rai_release.missing_binding` and `assistant_release.assessment(..., live=True)`

* Target Files:
  * `src/core/src/zava_forward/core/rai_release.py` (`missing_binding`)
  * `src/core/src/zava_forward/core/assistant_release.py` (`assessment`)
* Context and Evidence (`C1`, `C2`, `C4`, `C5`, `C7`):
  * In `rai_release.missing_binding`, update the expiry check so `isinstance(record.get("expires"), bool)` is rejected alongside non-numeric or expired timestamps.
  * Inside `if live and ("approved_by" in record or "named_approval_id" in record):`, remove the inner `"approved_by" in record and` and `"named_approval_id" in record and` guards so supplying either `OQ-017` key requires both `rai_control_plane.valid_named_human_approver(record.get("approved_by"))` and `rai_control_plane.valid_named_approval_id(record.get("named_approval_id"))`. Leaving the outer `("approved_by" in record or "named_approval_id" in record)` check intact preserves isolated 4-key unit dicts in `test_rai_threshold_live_approval_guard.py` and `test_rai_release.py`.
  * In `assistant_release.assessment(db, task, binding, now, live=False)`, immediately after `found = releases(db, task)` when `live` is `True`, ensure every `rec` in `found` sets `rec.setdefault("approved_by", None)` and `rec.setdefault("named_approval_id", None)` before `invalidate_changed` and `rai_release.select`. Every SQL-stored record evaluated for live dispatch or readiness inspection will therefore require both valid `OQ-017` fields.
* Completion Expectations:
  * Partial-key records fail `rai_release.missing_binding(..., live=True)`.
  * Pre-existing or direct-SQL `actual` rows without `approved_by` or `named_approval_id` fail `assistant_release.assessment(..., live=True)` with `OQ-017` missing items.
  * Existing `test_rai_release.py`, `test_rai_threshold_live_approval_guard.py`, and `test_assistant_release.py` remain green.

<!-- rpi:task id=P01-T02 -->
### Task P01-T02: Align `rai_control_plane._inspect_sql_live_releases` with `assistant_release.assessment(..., live=True)`

* Target File:
  * `src/core/src/zava_forward/core/rai_control_plane.py` (`_inspect_sql_live_releases`)
* Context and Evidence (`C3`, `C8`, `C9`, `PC-001`):
  * Import `assistants` and bind `_assistants: Any = assistants` alongside `_ai_registry: Any = ai_registry` so `src/core` strict `mypy` passes without untyped-call errors.
  * Inside `with _assistant_release.read_only():`, determine `ai_obj = getattr(store, "ai", None)` and compute `now_ts` from `float(assistants_service.now(cursor_db))` when `assistants_service is not None and getattr(assistants_service, "sql", False)`, else `float(cursor_db.execute(store._epoch_sql).fetchone()[0])` when `hasattr(store, "_epoch_sql")` (falling back to `time.time()` on exception).
  * For each `task_name in enabled_tasks`:
    * If `ai_obj is None`: `has_valid_live = False`.
    * Elif `task_name in _assistants.REGISTRY`: `cap = task_name`, `binding = _assistants.runtime_binding(task_name, ai_obj)`, and `selected, denied = _assistant_release.assessment(cursor_db, cap, binding, now_ts, live=True)`.
    * Elif `task_name in _ai_registry.LEGACY`: `cap = f"legacy:{task_name}"`, `route = str(_ai_registry.LEGACY[task_name]["route"])`, `dep = str(getattr(ai_obj, route, "") or "")`, `binding = _ai_registry.legacy_binding(task_name, ai_obj, dep)`, and `selected, denied = _assistant_release.assessment(cursor_db, cap, binding, now_ts, live=True)`.
    * Else: `has_valid_live = False`.
    * Set `has_valid_live = selected is not None and denied is None` on the two assessed branches.
  * Keep strict `mypy` clean (`strict = true` in `src/core`).
* Completion Expectations:
  * Active `actual` SQL rows with drifted bindings or `"unattested"` serving models are reported in `unapproved_live_tasks`, never `approved_live_tasks`, and read-only calls do not mutate `assistant_releases` or `assistant_events` in SQLite/MSSQL.

<!-- rpi:phase id=P02 -->
## Phase P02: Add Focused Regression Tests and Run Package Validation

* Phase Goal: Prove `AC-H01`..`AC-H04` with focused tests and package-level static/unit checks.
* Write Boundary: `src/core/tests/test_rai_control_plane_218.py`, `src/api/tests/test_rai_release_readiness_api_218.py`.

<!-- rpi:task id=P02-T01 -->
### Task P02-T01: Add Regression Tests for `RV-001` and `RV-002`

* Target Files:
  * `src/core/tests/test_rai_control_plane_218.py`
  * `src/api/tests/test_rai_release_readiness_api_218.py`
* Context and Evidence:
  * Stay strictly within `NFR-H03` (`<= 6` added test methods across existing `#218` test files, `0` new test files).
  * In `src/core/tests/test_rai_control_plane_218.py`:
    * Test `rai_release.missing_binding(..., live=True)` rejects partial `OQ-017` keys (only `approved_by` or only `named_approval_id`) and `expires=True`.
    * Test `assistant_release.assessment(..., live=True)` denies a directly-inserted active `actual` SQL row that has valid live monitoring thresholds and attested serving model but lacks `approved_by` / `named_approval_id`.
    * Test `exercise_acceptance_report` places a SQL task with a drifted `prompt_version` (or `"unattested"` model) in `unapproved_live_tasks` without mutating the SQL row's stored `"active"` status under `read_only()`, and places the task in `approved_live_tasks` once the runtime binding and serving model match.
  * In `src/api/tests/test_rai_release_readiness_api_218.py`:
    * First configure `self.store.ai.endpoint = "https://zava-live-openai.invalid"` and call `release_support.install(self.store, self.store.ai, cls="actual")` to establish the positive baseline where `/api/ai/report` reports `real_ai_delivery_gate.checks.oq017_named_live_releases_recorded.passed is True`. Then mutate a stored SQL release row (stripping `OQ-017` fields or drifting `prompt_version` / setting `expires=True`) and verify `/api/ai/report` flips `oq017_named_live_releases_recorded.passed` to `False` while `rai_exercise_acceptance.passed` remains `True` and SQL row status stays `"active"`.
* Completion Expectations:
  * All new tests would fail before `P01` and pass after `P01`, while `verify_traceability_targets()["all_resolved"]` remains `True`.

<!-- rpi:task id=P02-T02 -->
### Task P02-T02: Execute Focused-Tier Package Validation

* Commands:
  * `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest` on `test_rai_control_plane_218.py`, `test_rai_release_readiness_api_218.py`, `test_rai_release.py`, `test_rai_threshold_live_approval_guard.py`, `test_assistant_release.py`, and full focused `src/core` + `src/api` RAI/governance/contract suites
  * `cd src/core && python3 -m mypy`
  * `cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy`
  * `cd src/core && python3 -m ruff check .` and `cd src/api && python3 -m ruff check .`
  * `python3 -m ruff format --isolated --line-length 100 --check` on touched non-excluded files plus package `python3 -m ruff format --check .` in `src/core` and `src/api`
* Completion Expectations:
  * Zero unit-test, `mypy`, `ruff check`, or `ruff format` errors; `tools/rpi-checks.py` is not executed.
