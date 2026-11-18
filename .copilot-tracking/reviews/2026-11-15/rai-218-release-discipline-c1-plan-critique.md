---
description: "Final-candidate RPI plan critique for Issue #218 c1 traceability AST verification caching"
---
<!-- markdownlint-disable-file -->

# RPI Plan Critique: Traceability AST Verification Caching (#218 c1)

## Metadata

* Task ID: issue-218-rai-release-discipline-c1
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/rai-218-release-discipline-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/rai-218-release-discipline-c1-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements:
  * Cache default `verify_traceability_targets()` results when `repo_root is None` in `src/core/src/zava_forward/core/rai_control_plane.py` via `@functools.lru_cache(maxsize=1)` on an internal helper returning immutable tuples so callers cannot mutate cached state, while keeping explicit `repo_root` calls uncached.
  * Prove repeated `verify_traceability_targets(None)` completes in `<1ms`, add a regression test in `src/core/tests/test_rai_control_plane_218.py`, and pass Epic #218 RAI release discipline tests plus `src/api/tests/test_assistants.py`.
  * Run focused validation (`ruff check`, `ruff format --check`, and `mypy`) in `src/core` and `src/api` without requiring `tools/rpi-checks.py`, branch push, or PR creation.
* Research and evidence considered:
  * `.copilot-tracking/research/2026-11-15/rai-218-release-discipline-c1-research.md` (`C1`..`C8`)
  * `.copilot-tracking/plans/2026-11-15/rai-218-release-discipline-c1-plan.md`
  * `.copilot-tracking/details/2026-11-15/rai-218-release-discipline-c1-phase-details.md`
  * `src/core/src/zava_forward/core/rai_control_plane.py`
  * `src/core/tests/test_rai_control_plane_218.py`
  * `src/core/pyproject.toml`
* Decisions, dependencies, and acceptance criteria considered:
  * Functional requirements `FR-C01`..`FR-C03`, non-functional requirements `NFR-C01`..`NFR-C03` (including the 1-method Test Governance Lock), acceptance criteria `AC-C01`..`AC-C04`, and linear task dependencies `P01-T01` -> `P02-T01` -> `P02-T02`.
* Assessment boundary:
  * Read-only verification of the supplied research, plan, phase details, `rai_control_plane.py`, `test_rai_control_plane_218.py`, and `src/core/pyproject.toml` lint/type configuration. No runtime execution of tests or modifications to source/plan files were performed during critique.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Req 1 / `FR-C01`..`FR-C03` / `P01-T01` | Partial | Default `None` caching and explicit `repo_root` bypass are sound and `ruff`/`mypy` decorator-safe, but `dict[str, Any]` return typing from `_verify_traceability_targets_uncached` leaves tuple construction untyped (`Any`) unless explicitly coerced (`PC-001`). |
| Caller Req 2 / `AC-C01` / `NFR-C01` / `P02-T01` | Partial | Warm-cache hit count (`call_count == 1`) and `<1.0ms` verification are planned, but timing a single call right after 16-file `ast.parse()` exposes CI runs to one-off cyclic GC or scheduler preemption spikes (`PC-002`). |
| Caller Req 2 / `AC-C02` / `NFR-C03` / `P02-T01` | Partial | Top-level dict and empty `unresolved` list mutation isolation are tested, but non-empty `unresolved` tuple freezing/unpacking executes zero loop iterations across all tests (`PC-001`). |
| `AC-C03` / `C8` / `P02-T01` | Covered | Explicit `verify_traceability_targets(repo_root=Path(tmp))` bypasses the cache (`call_count == 2`), fails closed, and leaves cached default state intact. |
| Caller Req 3 / `NFR-C02` / `AC-C04` / `P02-T02` | Covered | Commands cover `ruff check`, `ruff format --check` (including `--isolated --line-length 100`), `mypy` in `src/core` (`strict = true`) and `src/api`, and all required Epic #218 core/API and assistant suites without invoking `tools/rpi-checks.py` or git push. |

## Verdict

* Verdict: Revise
* Rationale: The architecture directly solves the ~135ms `GET /api/assistants` AST-parsing bottleneck (`PR #1807` `case_journey_browser_check.py:1004`) and complies with `src/core/pyproject.toml` `ruff` (`E, F, I, B, UP`) and `mypy` (`strict = true`) rules for `@functools.lru_cache(maxsize=1)` and `.cache_clear()`. Two bounded planner refinements are warranted before implementation: tightening static typing and runtime coverage on the non-empty `unresolved` freeze/materialize path (`PC-001`) and hardening the `<1.0ms` warm-latency assertion against single-sample GC/preemption jitter (`PC-002`).

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Non-empty `unresolved` tuple freezing and element-dict immutability are untyped via `Any` and unexecuted at runtime

* Related IDs: `FR-C01`, `FR-C02`, `FR-C03`, `AC-C02`, `NFR-C02`, `NFR-C03`, `P01-T01`, `P02-T01`
* Evidence: .copilot-tracking/plans/2026-11-15/rai-218-release-discipline-c1-plan.md, .copilot-tracking/details/2026-11-15/rai-218-release-discipline-c1-phase-details.md, src/core/src/zava_forward/core/rai_control_plane.py, src/core/tests/test_rai_control_plane_218.py, src/core/pyproject.toml
* Concern: `P01-T01` types `_verify_traceability_targets_uncached(root: Path) -> dict[str, Any]`, so indexing `result["all_resolved"]`, `result["verified_target_count"]`, and `result["unresolved"]` inside `_cached_default_traceability_targets()` yields `Any`. Under `mypy` (`strict = true`), a `tuple(Any, ...)` expression is silently accepted for `tuple[tuple[str, str, str], ...]` even if inner dicts are not converted to 3-tuples or a key name is mistyped. At runtime, `P02-T01` only exercises `verify_traceability_targets(None)` against the live repository where `unresolved` is `[]` (0 elements), while `repo_root=Path(tmp)` bypasses `_cached_default_traceability_targets()`. As a result, neither the tuple-freezing comprehension in `_cached_default_traceability_targets()` nor the dict-materializing comprehension in `verify_traceability_targets(None)` executes a single iteration in any test, and per-element dict mutation (`result["unresolved"][0]["reason"] = "mutated"`) is unverified.
* Impact: A key typo, swapped 3-tuple field order, or shallow inner-dict reference in the cached `unresolved` path would pass both `mypy --strict` and the full unit suite, surfacing only when a traceability check fails.
* Smallest useful change: In `P01-T01`, explicitly coerce `(bool(result["all_resolved"]), int(result["verified_target_count"]), tuple((str(item["id"]), str(item["target"]), str(item["reason"])) for item in result["unresolved"]))` (or have an internal typed scan helper return `tuple[bool, int, tuple[tuple[str, str, str], ...]]` directly). In `P02-T01`, within the single allowed test method `test_verify_traceability_targets_caches_default_root_immutably_under_one_ms` (respecting `NFR-C03`), add a sub-check that clears the cache, patches `rai_control_plane._default_repo_root` to `Path(tmp)` (clearing the cache again afterward), calls `verify_traceability_targets(None)` to cache non-empty `unresolved` entries, mutates `first_broken["unresolved"][0]["reason"] = "mutated"`, and verifies a second `verify_traceability_targets(None)` call hits the cache and preserves the original `"reason"` string.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` and `P02-T01` in `.copilot-tracking/details/2026-11-15/rai-218-release-discipline-c1-phase-details.md` specifying explicit `bool`/`int`/`str` tuple construction (or typed tuple helper) and cached non-empty `unresolved[0]` mutation isolation inside `test_verify_traceability_targets_caches_default_root_immutably_under_one_ms`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Low]: Single-sample `<1.0ms` wall-clock assertion immediately after 16-file `ast.parse()` risks CI GC or preemption flakes

* Related IDs: `NFR-C01`, `AC-C01`, `P02-T01`
* Evidence: .copilot-tracking/plans/2026-11-15/rai-218-release-discipline-c1-plan.md, .copilot-tracking/details/2026-11-15/rai-218-release-discipline-c1-phase-details.md
* Concern: `P02-T01` step 1 performs a cold 16-file `ast.parse()` scan that allocates tens of thousands of cyclic AST container nodes, and step 3 immediately asserts `(t1 - t0) * 1000.0 < 1.0` on a single warm `verify_traceability_targets(None)` call. Because `verify_traceability_targets(None)` allocates a fresh `dict` and `list`, Python's cyclic garbage collector or a single OS vCPU preemption on a contended hosted runner can sporadically push one sample past `1.0ms` even though warm cached execution takes `<0.05ms`.
* Impact: Potential intermittent false-negative test failures on shared CI runners despite a working cache (`call_count == 1`).
* Smallest useful change: Update `P02-T01` step 3 to measure repeated warm `verify_traceability_targets(None)` calls (for example, collecting 5 individual `time.perf_counter()` samples and asserting `min(samples_ms) < 1.0`, or asserting mean latency across 10-20 warm calls `< 1.0` ms, while verifying `call_count == 1` across all iterations). Uncached execution (~135ms per call) still fails both assertions deterministically.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P02-T01` step 3 in `.copilot-tracking/details/2026-11-15/rai-218-release-discipline-c1-phase-details.md` using multi-call warm timing (`min` or per-call mean `< 1.0` ms) alongside `call_count == 1`.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Root-cause precision (`C1`..`C7`): Research and plan accurately trace the `case_journey_browser_check.py:1004` `"AI review count loading."` failure to `Assistants.registry()` invoking uncached `verify_traceability_targets(None)` (~135ms across 16 test files / 43 targets) on `GET /api/assistants`, avoiding brittle Playwright timeout workarounds or `scenario-manifest.json` recipe churn.
* Static-analysis compatibility (`NFR-C02`): Checked against `src/core/pyproject.toml`:
  * `[tool.ruff.lint] select = ["E", "F", "I", "B", "UP"]` (`py312`, `line-length = 100`) does not enable `SLF001`, so accessing `_cached_default_traceability_targets.cache_clear()` and `_verify_traceability_targets_uncached` in `test_rai_control_plane_218.py` passes `ruff check`.
  * `@functools.lru_cache(maxsize=1)` on a module-level function satisfies `UP011` (requires parens/args), `UP033` (only flags `maxsize=None`), and `B019` (only flags instance/class methods).
  * Standard-library import additions (`functools` in `rai_control_plane.py`, `time` in `test_rai_control_plane_218.py`) preserve alphabetical `I001` sort order.
  * Under `mypy` `strict = true` (`disallow_untyped_decorators = true`, `disallow_untyped_calls = true`), typeshed's `functools.lru_cache` returns a typed `_lru_cache_wrapper[_T]` exposing `.cache_clear() -> None`, and `unittest.mock.patch.object(..., wraps=...)` yields a typed mock with `.call_count: int`.
* Accepted residual risk: Process-lifetime caching assumes `REQUIREMENT_TRACEABILITY` and repository test files on disk do not mutate within a running API server process (`C3`), while explicit `repo_root` paths remain uncached (`C8`).

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Critique was conducted strictly read-only against the supplied research, plan, phase-details, and `src/core` source/config inputs without executing test or linter commands or inspecting `src/api/pyproject.toml` beyond the supplied research/plan evidence.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: planning_parent
* Smallest next action: Apply direct planner updates to `P01-T01` and `P02-T01` in `.copilot-tracking/details/2026-11-15/rai-218-release-discipline-c1-phase-details.md` for `PC-001` (explicit typed 3-tuple freezing + cached non-empty `unresolved[0]` mutation assertion) and `PC-002` (multi-call warm `<1.0ms` timing), finalize disposition in `.copilot-tracking/plans/2026-11-15/rai-218-release-discipline-c1-plan.md`, and proceed to `Implement` without another critique pass.
* User response required: no
