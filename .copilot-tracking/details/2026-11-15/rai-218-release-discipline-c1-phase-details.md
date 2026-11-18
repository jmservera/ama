---
title: "Phase Details: Traceability AST Verification Caching (#218 c1)"
description: "Evidence-grounded implementation details for correction task rai-218-release-discipline-c1"
author: "GitHub Copilot"
ms.date: "2026-11-15"
---

* Task ID: `issue-218-rai-release-discipline-c1`
* Task Slug: `rai-218-release-discipline-c1`
* Plan Artifact: `.copilot-tracking/plans/2026-11-15/rai-218-release-discipline-c1-plan.md`
* Research Artifact: `.copilot-tracking/research/2026-11-15/rai-218-release-discipline-c1-research.md`

<!-- rpi:phase id=P01 -->
## Phase P01: Cache Default `verify_traceability_targets(None)` Immutably in `rai_control_plane.py`

* Phase Goal: Eliminate ~135ms of repeated test-file disk reads and `ast.parse()` calls when `verify_traceability_targets(None)` is invoked on `GET /api/assistants`, `GET /api/governance`, and `GET /api/ai/report`, while keeping cached state immutable and explicit `repo_root` calls uncached.
* Write Boundary: `src/core/src/zava_forward/core/rai_control_plane.py`.

<!-- rpi:task id=P01-T01 -->
### Task P01-T01: Implement `_scan_traceability_targets` and `_cached_default_traceability_targets`

* Target File:
  * `src/core/src/zava_forward/core/rai_control_plane.py`
* Context and Evidence (`C1`, `C2`, `C3`, `C4`, `C8`, `PC-001`):
  * Add `import functools` in sorted standard-library import order (`ast`, `copy`, `functools`, `json`, `os`, `re`, `time`).
  * Extract `_scan_traceability_targets(root: Path) -> tuple[bool, int, tuple[tuple[str, str, str], ...]]` recording unresolved items directly as `(req_id, str(target), reason)` 3-tuples and returning `(not unresolved, verified_count, tuple(unresolved))` without any `Any`-typed intermediate dictionary.
  * Define `@functools.lru_cache(maxsize=1)` on `_cached_default_traceability_targets() -> tuple[bool, int, tuple[tuple[str, str, str], ...]]`, which returns `_scan_traceability_targets(_default_repo_root())`.
  * In `verify_traceability_targets(repo_root: Path | None = None) -> dict[str, Any]`:
    * Resolve `all_resolved, verified_count, frozen_unresolved = _scan_traceability_targets(repo_root) if repo_root is not None else _cached_default_traceability_targets()`.
    * Return a newly allocated dictionary `{"all_resolved": all_resolved, "verified_target_count": verified_count, "unresolved": [{"id": req_id, "target": target, "reason": reason} for req_id, target, reason in frozen_unresolved]}`.
* Completion Expectations:
  * Warm `verify_traceability_targets(None)` calls avoid both `Path.resolve()` and `ast.parse()`, completing in `<1ms`.
  * Mutating any returned dict, `unresolved` list, or inner `unresolved[i]` dict cannot corrupt subsequent calls.
  * Strict `mypy` (`strict = true`) passes with zero warnings.

<!-- rpi:phase id=P02 -->
## Phase P02: Add Regression Test and Run Focused `src/core` & `src/api` Validation

* Phase Goal: Prove `AC-C01`..`AC-C04` via unit test and static/runtime package checks.
* Write Boundary: `src/core/tests/test_rai_control_plane_218.py`.

<!-- rpi:task id=P02-T01 -->
### Task P02-T01: Add Caching, Latency, and Immutability Regression Test

* Target File:
  * `src/core/tests/test_rai_control_plane_218.py`
* Context and Evidence (`C4`, `C8`, `NFR-C03`, `PC-001`, `PC-002`):
  * Add `import time` to `src/core/tests/test_rai_control_plane_218.py` in sorted stdlib order.
  * Add `test_verify_traceability_targets_caches_default_root_immutably_under_one_ms(self) -> None` on `RaiControlPlane218Tests`:
    * Clear `_cached_default_traceability_targets.cache_clear()` at start and register `self.addCleanup(rai_control_plane._cached_default_traceability_targets.cache_clear)`.
    * Wrap `rai_control_plane._scan_traceability_targets` with `patch.object(rai_control_plane, "_scan_traceability_targets", wraps=rai_control_plane._scan_traceability_targets)` to prove:
      1. First `verify_traceability_targets()` (`None`) populates the cache (`call_count == 1`, `all_resolved is True`).
      2. Mutating the first returned dictionary (`first["all_resolved"] = False`, `first["verified_target_count"] = 0`, `first["unresolved"].append({"id": "FR-051", "target": "mutated", "reason": "mutated"})`) does not leak into subsequent calls.
      3. Sampling 10 warm `verify_traceability_targets(None)` calls with `time.perf_counter()` returns `all_resolved is True` and `unresolved == []` on each call, keeps `call_count == 1`, and completes with both `min(samples_ms) < 1.0` and `sum(samples_ms) / len(samples_ms) < 1.0` (`PC-002`).
      4. Calling `verify_traceability_targets(repo_root=Path(tmp))` increments `call_count` to `2` and fails closed (`all_resolved is False`) without disturbing the cached default result on a subsequent `verify_traceability_targets(None)` call (`call_count` stays `2`, `all_resolved is True`).
      5. Clearing the cache, patching `_default_repo_root` to `Path(tmp)` (inside `try ... finally: _cached_default_traceability_targets.cache_clear()`), calling `verify_traceability_targets(None)` to populate non-empty cached `unresolved` entries, mutating `broken_first["unresolved"][0]["reason"] = "mutated"`, and calling `verify_traceability_targets(None)` again hits the cache without extra scans and preserves the original `"reason"` string (`PC-001`).
* Completion Expectations:
  * Test fails without `P01` and passes deterministically with `P01`.

<!-- rpi:task id=P02-T02 -->
### Task P02-T02: Execute Focused Static, Unit, and Timing Checks

* Commands:
  * `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest` on `src/core/tests/test_rai_control_plane_218.py`, `src/api/tests/test_rai_release_readiness_api_218.py`, `src/api/tests/test_assistants.py`, `src/api/tests/test_assistant_release.py`, `src/core/tests/test_rai_release.py`, `src/core/tests/test_rai_release_invalidation.py`, and `src/core/tests/test_rai_threshold_live_approval_guard.py`
  * `cd src/core && python3 -m ruff check . && python3 -m ruff format --isolated --line-length 100 --check src/zava_forward/core/rai_control_plane.py tests/test_rai_control_plane_218.py && python3 -m ruff format --check . && python3 -m mypy`
  * `cd src/api && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=../core/src:../agents/src python3 -m mypy`
* Completion Expectations:
  * All unit tests, `ruff check`, `ruff format --check`, and `mypy` runs exit `0`, and warm `verify_traceability_targets(None)` measures `<1ms`.
