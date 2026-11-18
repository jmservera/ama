---
title: "Implementation Plan: Live Release Admission & Readiness Hardening (#218 Child)"
description: "Close RV-001 and RV-002 from parent review by enforcing OQ-017 named-approval completeness at live dispatch and runtime-binding assessment in SQL readiness inspection"
author: "GitHub Copilot"
ms.date: "2026-11-15"
---

* Task ID: `issue-218-rai-release-admission-hardening`
* Task Slug: `rai-218-release-admission-hardening`
* Parent Task: `issue-218-rai-release-discipline` (`rai-218-release-discipline`)
* Planning Readiness: `Ready`
* Downstream Changes Path: `.copilot-tracking/changes/2026-11-15/rai-218-release-admission-hardening-changes.md`

## Executive Summary

This child plan resolves the two routed defects (`RV-001` and `RV-002`) identified during post-implementation review of Issue #218 without altering public API schemas or historical review evidence. Phase `P01` closes `RV-001` and `RV-002` in `src/core`: `rai_release.missing_binding` rejects `bool` expiry values and requires both `approved_by` and `named_approval_id` whenever either `OQ-017` key is supplied; `assistant_release.assessment(..., live=True)` populates missing `approved_by` and `named_approval_id` defaults (`None`) on SQL-loaded release rows so pre-existing or out-of-band SQL rows cannot bypass `OQ-017` at live dispatch; and `rai_control_plane._inspect_sql_live_releases` delegates read-only live verification to `assistant_release.assessment(..., live=True)` against current assistant `runtime_binding` and legacy `legacy_binding` values so drifted or unattested SQL rows are never counted as approved live tasks. Phase `P02` adds focused unit and API regression tests and executes the focused-tier validation suite (`unittest`, strict `mypy`, `ruff check`, and `ruff format --check`).

## Sources

* Parent review record: `.copilot-tracking/reviews/logs/2026-11-15/rai-218-release-discipline-review.md` (`RV-001`, `RV-002`)
* Child research synthesis: `.copilot-tracking/research/2026-11-15/rai-218-release-admission-hardening-research.md` (`C1`..`C9`)
* Parent plan and changes: `.copilot-tracking/plans/2026-11-15/rai-218-release-discipline-plan.md`, `.copilot-tracking/changes/2026-11-15/rai-218-release-discipline-changes.md`

## User Decisions and Requirements

* Ensure no live activation or live dispatch of an AI task succeeds without a non-empty named human approver (`approved_by` and `named_approval_id`, `OQ-017`), with audit record emission on rejected activation attempts (caller prompt AC 1; `RV-001`).
* Ensure exercise acceptance reports `rai_exercise_acceptance` separately from `real_ai_delivery_gate` and reflects actual live runtime-binding readiness rather than drifted or unattested SQL rows (caller prompt AC 3; `RV-002`).
* Preserve isolated bare-dict unit contracts in `src/core/tests/test_rai_release.py` and `src/core/tests/test_rai_threshold_live_approval_guard.py` while enforcing unconditional `OQ-017` checks on SQL-backed live dispatch (`C4`, `C5`, `C7`).
* Validate at the focused tier (`src/core` and `src/api` `unittest`, `mypy`, `ruff check`, `ruff format --isolated --line-length 100 --check`) without running `tools/rpi-checks.py` and without pushing or opening a PR (caller prompt).

## Goals

* Eliminate partial-key and stored-SQL-row `OQ-017` bypasses at live release selection and dispatch admission (`RV-001`).
* Align `real_ai_delivery_gate` SQL live release inspection with `assistant_release.assessment(..., live=True)` against current runtime and legacy bindings under read-only semantics (`RV-002`).
* Prove both fixes with focused regression tests while keeping all existing `src/core` and `src/api` suites, strict `mypy`, and `ruff` checks green.

## Scope and Non-Goals

* In scope:
  * `src/core/src/zava_forward/core/rai_release.py` (`missing_binding`)
  * `src/core/src/zava_forward/core/assistant_release.py` (`assessment`)
  * `src/core/src/zava_forward/core/rai_control_plane.py` (`_inspect_sql_live_releases`)
  * `src/core/tests/test_rai_control_plane_218.py` and `src/api/tests/test_rai_release_readiness_api_218.py`
* Non-goals:
  * Modifying parent `.copilot-tracking/` review artifacts
  * Changing HTTP response shapes or SQLite/MSSQL DDL
  * Running `tools/rpi-checks.py`, pushing branches, or opening pull requests

## Functional Requirements

* `FR-H01`: In `rai_release.missing_binding`, reject boolean `expires` values (`isinstance(expires, bool)`) and, when `live` is `True` and either `"approved_by"` or `"named_approval_id"` is present in `record`, require both `valid_named_human_approver(record.get("approved_by"))` and `valid_named_approval_id(record.get("named_approval_id"))`.
* `FR-H02`: In `assistant_release.assessment`, when `live` is `True`, ensure every record loaded from `releases(db, task)` carries `"approved_by"` and `"named_approval_id"` keys (`setdefault(..., None)`) prior to `invalidate_changed` and `rai_release.select` so stored or out-of-band SQL rows lacking `OQ-017` fields are deterministically denied for live dispatch.
* `FR-H03`: In `rai_control_plane._inspect_sql_live_releases`, import `assistants` via `_assistants: Any = assistants` alongside `_ai_registry: Any = ai_registry`, resolve `now_ts` from `assistants_service.now(cursor_db)` or `store._epoch_sql` (falling back to `time.time()`), and evaluate each enabled task inside `with _assistant_release.read_only():` via `_assistant_release.assessment(cursor_db, cap, binding, now_ts, live=True)` using `_assistants.runtime_binding(task_name, ai_obj)` when `task_name in _assistants.REGISTRY` and `_ai_registry.legacy_binding(task_name, ai_obj, dep)` with default-safe `route = str(_ai_registry.LEGACY[task_name]["route"]); dep = getattr(ai_obj, route, "") or ""` when `task_name in _ai_registry.LEGACY` (failing closed `False` otherwise), counting a task in `approved_live_tasks` only when `selected is not None and denied is None`.

## Non-Functional Requirements

* `NFR-H01`: Preserve strict read-only semantics during `exercise_acceptance_report` / `governance_view` / `registry` calls (`with _assistant_release.read_only():` prevents `invalidate_changed` from writing revocation rows or events).
* `NFR-H02`: Pass `src/core` strict `mypy` (`strict = true`), `src/api` `mypy`, `ruff check`, and `ruff format --isolated --line-length 100 --check` on touched files.
* `NFR-H03`: Test Governance Lock — Test owner: `src/core/tests/test_rai_control_plane_218.py` and `src/api/tests/test_rai_release_readiness_api_218.py`; Exact removals: `none`; Maximum additions: `<= 6` new test methods total across those two existing Epic #218 test files (`0` new test files); Canonical targets: `src/core/src/zava_forward/core/rai_release.py`, `src/core/src/zava_forward/core/assistant_release.py`, `src/core/src/zava_forward/core/rai_control_plane.py`; Generated targets: `none`; Coverage split: semantic tests verify partial-key `missing_binding` rejection, stored-SQL-row live dispatch denial without `OQ-017` fields, and drifted/unattested SQL row exclusion from `approved_live_tasks`, while regression runs verify existing `test_rai_release.py`, `test_rai_threshold_live_approval_guard.py`, `test_assistant_release.py`, and full focused `src/core`/`src/api` suites.

## Acceptance Criteria

* `AC-H01`: Calling `rai_release.missing_binding(..., live=True)` with only `approved_by` (omitting `named_approval_id`), only `named_approval_id` (omitting `approved_by`), or `expires=True` returns the corresponding missing-binding failure rather than `[]`.
* `AC-H02`: Persisting an active `actual` SQL row in `assistant_releases` with approved live monitoring thresholds and matching serving model—but without `approved_by` or `named_approval_id`—is denied by `assistant_release.assessment(..., live=True)` / `assistant_release.admission(..., live=True)` with `OQ-017` missing fields.
* `AC-H03`: Persisting an active `actual` SQL row in `assistant_releases` with valid `approved_by` and `named_approval_id` whose `prompt_version` or `serving_model` drifts from `store.ai` / `runtime_binding` leaves that task in `real_ai_delivery_gate.unapproved_live_tasks` (not `approved_live_tasks`) without mutating SQL rows during read-only inspection, while an attested matching row is listed in `approved_live_tasks`.
* `AC-H04`: Focused `unittest`, `mypy`, `ruff check`, and `ruff format --check` pass across `src/core` and `src/api` with zero failures, including `verify_traceability_targets()["all_resolved"] is True`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Harden Live Release Binding Selection and Read-Only SQL Readiness Assessment

* [x] `P01-T01`: Enforce partial-key `OQ-017` completeness and boolean-expiry rejection in `rai_release.missing_binding`, and enforce unconditional `OQ-017` key presence on SQL rows in `assistant_release.assessment(..., live=True)` (`RV-001`).
* [x] `P01-T02`: Replace raw SQL row field checks in `rai_control_plane._inspect_sql_live_releases` with read-only `assistant_release.assessment(..., live=True)` against current assistant and legacy runtime bindings (`RV-002`).

<!-- rpi:phase id=P02 -->
### [x] P02: Add Focused Regression Tests and Run Package Validation

* [x] `P02-T01`: Add focused unit and HTTP API regression tests in `src/core/tests/test_rai_control_plane_218.py` and `src/api/tests/test_rai_release_readiness_api_218.py` covering `AC-H01`, `AC-H02`, and `AC-H03`.
* [x] `P02-T02`: Run focused `unittest`, strict `mypy`, `ruff check`, and `ruff format --isolated --line-length 100 --check` across `src/core` and `src/api`.

## Dependencies

* `P01-T01` has no prerequisites.
* `P01-T02` depends on `P01-T01` because `_inspect_sql_live_releases` delegates `OQ-017` SQL-row checks to `assistant_release.assessment(..., live=True)`.
* `P02-T01` depends on `P01-T01` and `P01-T02`.
* `P02-T02` depends on `P02-T01`.

## Follow-Up Items

* None.

## Critique Disposition

Single final-candidate critique executed at `.copilot-tracking/reviews/2026-11-15/rai-218-release-admission-hardening-plan-critique.md` (Execution: `Complete`, Verdict: `Revise`, `0` Critical, `1` High, `1` Medium):

* `PC-001` [High] (`direct_planner_correction` — Applied): Updated `FR-H03` and `Task P01-T02` to import `assistants` via `_assistants: Any = assistants`, use `_ai_registry: Any`, branch explicitly with `if task_name in _assistants.REGISTRY:` / `elif task_name in _ai_registry.LEGACY:` / `else: has_valid_live = False`, resolve legacy deployment safely via `route = str(_ai_registry.LEGACY[task_name]["route"]); dep = getattr(ai_obj, route, "") or ""`, and resolve `now_ts` from `assistants_service.now(cursor_db)` or `store._epoch_sql` before falling back to `time.time()`.
* `PC-002` [Medium] (`direct_planner_correction` — Applied): Updated `AC-H04` and `Task P02-T01` to assert `verify_traceability_targets()["all_resolved"] is True` and to establish a positive live-endpoint `cls="actual"` baseline (`oq017_named_live_releases_recorded.passed is True`) in `test_rai_release_readiness_api_218.py` before mutating a SQL row (stripping `OQ-017` keys or drifting `prompt_version` / `expires=True`) to prove `passed` flips to `False`.

## Handoff

* Changes record target: `.copilot-tracking/changes/2026-11-15/rai-218-release-admission-hardening-changes.md`
* Mode continuation: Automatic RPI Agent child loop transitions to `Implement` once the single final-candidate critique completes and compatible planner dispositions are applied.
