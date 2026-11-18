---
title: "Implementation Plan: Traceability AST Verification Caching (#218 c1)"
description: "Cache default verify_traceability_targets(None) in rai_control_plane.py to eliminate ~135ms per-request AST parsing on GET /api/assistants and fix PR #1807 case_journey_browser_check.py:1004"
author: "GitHub Copilot"
ms.date: "2026-11-15"
---

* Task ID: `issue-218-rai-release-discipline-c1`
* Task Slug: `rai-218-release-discipline-c1`
* Parent Task: `issue-218-rai-release-admission-hardening` (`rai-218-release-admission-hardening`)
* Planning Readiness: `Ready`
* Downstream Changes Path: `.copilot-tracking/changes/2026-11-15/rai-218-release-discipline-c1-changes.md`

## Executive Summary

This `c1` correction plan resolves the single `Source projects CI` failure on `PR #1807` (`src-api` `case_journey_browser_check.py:1004`, `"AI review count loading."`) caused by `Assistants.registry()` invoking `rai_control_plane.exercise_acceptance_report()` -> `traceability_summary(None)` -> `verify_traceability_targets(None)` on every `GET /api/assistants` request and re-parsing 16 test files (~135ms per call) via `ast.parse()`. Phase `P01` refactors `verify_traceability_targets` in `src/core/src/zava_forward/core/rai_control_plane.py` to cache the default `repo_root is None` scan once per process via an internal `@functools.lru_cache(maxsize=1)` helper returning an immutable tuple while reconstructing a fresh `dict` and `unresolved` list on every call and executing uncached whenever an explicit `repo_root` path is passed. Phase `P02` adds a focused regression test in `src/core/tests/test_rai_control_plane_218.py` proving single-scan caching, `<1ms` repeated latency, caller-mutation isolation, and uncached explicit `repo_root` evaluation, then runs `ruff check`, `ruff format --check`, `mypy`, and focused `unittest` suites across `src/core` and `src/api`.

## Sources

* Research synthesis: `.copilot-tracking/research/2026-11-15/rai-218-release-discipline-c1-research.md` (`C1`..`C8`)
* Prior Epic #218 artifacts: `.copilot-tracking/plans/2026-11-15/rai-218-release-discipline-plan.md`, `.copilot-tracking/plans/2026-11-15/rai-218-release-admission-hardening-plan.md`, `.copilot-tracking/reviews/logs/2026-11-15/rai-218-release-admission-hardening-review.md`

## User Decisions and Requirements

* Cache the default `verify_traceability_targets()` result when `repo_root is None` in `src/core/src/zava_forward/core/rai_control_plane.py` using `@functools.lru_cache(maxsize=1)` on an internal helper returning immutable tuples so callers cannot mutate cached state, while still running uncached when an explicit `repo_root` path is passed in tests (caller prompt item 1).
* Verify that `verify_traceability_targets(None)` takes `<1ms` on repeated calls, add a regression test in `src/core/tests/test_rai_control_plane_218.py`, and verify all Epic #218 core/API RAI release discipline tests and `src/api/tests/test_assistants.py` pass (caller prompt item 2 and follow-up prompt).
* Run `ruff check`, `ruff format --check`, and `mypy` in `src/core` and `src/api` (caller prompt item 3).
* Record dated `.copilot-tracking/` `c1` artifacts and commit cleanly on `feat/rai-218-release-discipline` with the `Co-authored-by` trailer without pushing or opening a PR (caller prompt item 4).

## Goals

* Reduce repeated `verify_traceability_targets(None)` latency from ~135ms to `<1ms` without altering return schemas or readiness semantics.
* Guarantee cached default state cannot be mutated by callers and explicit `repo_root` calls always run uncached against disk.
* Verify all targeted unit, type, lint, format, and browser-adjacent assistant suites across `src/core` and `src/api`.

## Scope and Non-Goals

* In scope:
  * `src/core/src/zava_forward/core/rai_control_plane.py` (`_scan_traceability_targets`, `_cached_default_traceability_targets`, `verify_traceability_targets`)
  * `src/core/tests/test_rai_control_plane_218.py` (cache hit, `<1ms` latency, mutation isolation, and explicit `repo_root` bypass regression test)
* Non-goals:
  * Modifying `src/api/checks/case_journey_browser_check.py` or `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`
  * Changing HTTP endpoint payloads or SQL release schemas
  * Pushing to `origin` or opening/updating pull requests

## Functional Requirements

* `FR-C01`: Extract strongly typed `_scan_traceability_targets(root: Path) -> tuple[bool, int, tuple[tuple[str, str, str], ...]]` in `src/core/src/zava_forward/core/rai_control_plane.py` returning `(all_resolved, verified_target_count, unresolved_triples)` with zero `Any` intermediate dictionaries (`PC-001`).
* `FR-C02`: Implement `@functools.lru_cache(maxsize=1)` on `_cached_default_traceability_targets() -> tuple[bool, int, tuple[tuple[str, str, str], ...]]` delegating directly to `_scan_traceability_targets(_default_repo_root())`.
* `FR-C03`: Update `verify_traceability_targets(repo_root: Path | None = None) -> dict[str, Any]` to call `_scan_traceability_targets(repo_root)` directly when `repo_root is not None` and `_cached_default_traceability_targets()` when `repo_root is None`, materializing a fresh `dict[str, Any]` and fresh `list[dict[str, str]]` on every call.

## Non-Functional Requirements

* `NFR-C01`: Repeated calls to `verify_traceability_targets(None)` after initial cache population must complete in `<1.0ms` (`time.perf_counter()`).
* `NFR-C02`: Pass `src/core` strict `mypy` (`strict = true`), `src/api` `mypy`, `ruff check`, and `ruff format --isolated --line-length 100 --check` across `src/core` and `src/api`.
* `NFR-C03`: Test Governance Lock — Test owner: `src/core/tests/test_rai_control_plane_218.py`; Exact removals: `none`; Maximum additions: `1` new test method (`0` new test files); Canonical target: `src/core/src/zava_forward/core/rai_control_plane.py`; Generated targets: `none`; Coverage split: semantic test `test_verify_traceability_targets_caches_default_root_immutably_under_one_ms` verifies single underlying AST scan on repeated `None` calls, `<1ms` warm-call latency, caller-mutation isolation on both top-level keys and `unresolved`, and uncached execution when `repo_root` is supplied; regression runs cover `test_rai_control_plane_218.py`, `test_rai_release_readiness_api_218.py`, `test_rai_release.py`, `test_rai_release_invalidation.py`, `test_rai_threshold_live_approval_guard.py`, `test_assistants.py`, and `test_assistant_release.py`.

## Acceptance Criteria

* `AC-C01`: Calling `verify_traceability_targets(None)` repeatedly invokes `_scan_traceability_targets` once, returns `{"all_resolved": True, "verified_target_count": ..., "unresolved": []}`, and executes repeated warm calls with both minimum and mean latency `<1.0ms` (`PC-002`).
* `AC-C02`: Mutating the `dict`, `unresolved` list, or non-empty `unresolved[0]` inner dict returned by `verify_traceability_targets(None)` does not affect subsequent `verify_traceability_targets(None)` calls (`PC-001`).
* `AC-C03`: Calling `verify_traceability_targets(repo_root=Path(...))` executes uncached on every call and continues to fail closed on missing test targets.
* `AC-C04`: `ruff check`, `ruff format --check`, `mypy`, and targeted `unittest` suites pass in `src/core` and `src/api` with zero errors.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Cache Default `verify_traceability_targets(None)` Immutably in `rai_control_plane.py`

* [x] `P01-T01`: Refactor `verify_traceability_targets` in `src/core/src/zava_forward/core/rai_control_plane.py` with typed `_scan_traceability_targets` and `@functools.lru_cache(maxsize=1)` `_cached_default_traceability_targets`.

<!-- rpi:phase id=P02 -->
### [x] P02: Add Regression Test and Run Focused `src/core` & `src/api` Validation

* [x] `P02-T01`: Add `test_verify_traceability_targets_caches_default_root_immutably_under_one_ms` in `src/core/tests/test_rai_control_plane_218.py`.
* [x] `P02-T02`: Run `ruff check`, `ruff format --check`, `mypy`, and `unittest` across `src/core` and `src/api` (plus direct `<1ms` timing probe).

## Dependencies

* `P01-T01` has no prerequisites.
* `P02-T01` depends on `P01-T01`.
* `P02-T02` depends on `P02-T01`.

## Follow-Up Items

* None.

## Critique Disposition

Single final-candidate critique executed at `.copilot-tracking/reviews/2026-11-15/rai-218-release-discipline-c1-plan-critique.md` (Execution: `Complete`, Verdict: `Revise`, `0` Critical, `0` High, `1` Medium, `1` Low):

* `PC-001` [Medium] (`direct_planner_correction` — Applied): Replaced untyped `dict[str, Any]` intermediate return with strongly typed `_scan_traceability_targets(root: Path) -> tuple[bool, int, tuple[tuple[str, str, str], ...]]` so `mypy --strict` verifies the 3-tuple structure without `Any`, and added a cached non-empty `unresolved[0]` inner-dict mutation check inside `test_verify_traceability_targets_caches_default_root_immutably_under_one_ms`.
* `PC-002` [Low] (`direct_planner_correction` — Applied): Updated `AC-C01` and `P02-T01` to sample 10 warm `verify_traceability_targets(None)` calls and assert both `min(samples_ms) < 1.0` and mean `< 1.0` ms alongside `call_count == 1` to avoid single-sample GC/preemption jitter on contended CI runners.

## Handoff

* Changes record target: `.copilot-tracking/changes/2026-11-15/rai-218-release-discipline-c1-changes.md`
* Mode continuation: Automatic RPI Agent correction loop transitions to `Implement` after the single final-candidate critique completes and any planner dispositions are applied.
