<!-- markdownlint-disable-file -->
# RPI Phase Details: Cycle-2 Fix for Issue #99 / PR #1739 `sys.modules` Test Bootstrap

## Metadata

* Task ID: fin-99-investment-envelope-2142-cycle2
* Task slug: fin-99-investment-envelope-2142-cycle2
* Related plan: .copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-cycle2-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-cycle2-research.md, src/core/tests/test_issue_99_acceptance.py, src/core/tests/test_exposure_limits.py, .github/workflows/src-ci.yml

## Phase Index

| Phase ID | Name                                                                                                                       | Status  | Detail sections       |
|----------|----------------------------------------------------------------------------------------------------------------------------|---------|-----------------------|
| P01      | Replace bulk `sys.modules` eviction with targeted `exposure_limits` bootstrap and validate multi-module `unittest` discovery | completed | P01, P01-T01, P01-T02 |

<!-- rpi:phase id=P01 -->
## P01: Replace bulk `sys.modules` eviction with targeted `exposure_limits` bootstrap and validate multi-module `unittest` discovery

### Context

Research (`C1`, `C2`, `C3`, `C4`, `C5`, `C6`) established that both `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py` currently run:
```python
_loaded = sys.modules.get("zava_forward.core.exposure_limits")
if _loaded is None or not Path(_loaded.__file__ or "").resolve().is_relative_to(_CORE_SRC):
    for _mod in [m for m in sys.modules if m == "zava_forward" or m.startswith("zava_forward.")]:
        del sys.modules[_mod]
```
Because `zava_forward.core.store` imports `finance` without eagerly importing `exposure_limits` (`C3`), `_loaded` is `None` when `unittest discover` reaches `test_issue_99_acceptance.py` (and would also have happened in `test_exposure_limits.py`). Deleting all `zava_forward.*` modules mid-discovery splits `zava_forward.core.store` and `ConflictError` identity between earlier test modules (`test_bulk_edits.py`) and later test modules (`test_taskqueues.py`), causing 40 downstream test errors/failures (`C5`).

### Intent

Replace the bulk eviction in both test files with a surgical single-module `exposure_limits` bootstrap that preserves every already-loaded `zava_forward.*` module, handles Python 3.12 PEP 420 parent-attribute and `_NamespacePath` rules accurately when `exposure_limits` was previously loaded from an external path, and proves full `src/core` `unittest` compatibility.

### Boundaries

* Included: `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py`
* Excluded: `src/core/src/zava_forward/core/exposure_limits.py`, `src/core/README.md`, `src/api/`, and `~/.local` site-packages

### Likely Targets

* src/core/tests/test_issue_99_acceptance.py: Targeted `_ensure_local_exposure_limits()` bootstrap + `test_bootstrap_preserves_store_identity_and_replaces_only_foreign_module` regression test.
* src/core/tests/test_exposure_limits.py: Matching targeted `_ensure_local_exposure_limits()` bootstrap.

### Dependencies

* none

### Validation Expectations

* `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, ordered `PYTHONPATH=src:tests python3 -m unittest tests/test_bulk_edits.py tests/test_issue_99_acceptance.py tests/test_exposure_limits.py tests/test_taskqueues.py -q`, and full `src/core` `unittest discover -s tests -q` pass cleanly.

### Completion Evidence

* Zero `del sys.modules[_mod]` bulk loops remain in `src/core/tests/`; all `src/core` unit and acceptance suites pass together in a single `unittest` process.

### Unresolved Items

* none

<!-- rpi:task id=P01-T01 -->
### P01-T01: Update module-import bootstrap in `test_issue_99_acceptance.py` and `test_exposure_limits.py` and add identity-preservation regression test

#### Context

Research `C6` uncovered two critical Python 3.12 PEP 420 subtleties for the fallback branch when `_loaded is not None` and outside `_CORE_SRC`:
1. `from zava_forward.core import exposure_limits as limits` checks `getattr(sys.modules["zava_forward.core"], "exposure_limits")` before importing `sys.modules["zava_forward.core.exposure_limits"]`, so `delattr(core_pkg, "exposure_limits")` is required alongside `sys.modules.pop("zava_forward.core.exposure_limits", None)`.
2. PEP 420 `_NamespacePath` objects auto-refresh when `sys.path` updates and do **not** implement `.insert()`, so any defensive `__path__` refresh on `zava_forward` or `zava_forward.core` must check `list(pkg.__path__)[:1] != [expected_dir]` and assign `[expected_dir, *(p for p in pkg.__path__ if p != expected_dir)]` rather than calling `.insert()`.
3. Checking `loaded_file = getattr(loaded, "__file__", None)` as `isinstance(loaded_file, str) and bool(loaded_file) and Path(loaded_file).resolve().is_relative_to(_CORE_SRC)` avoids `Path("").resolve()` depending on `Path.cwd()`.

#### Intent

Implement an identical, Ruff/mypy-clean `_ensure_local_exposure_limits()` helper at module import time in both `test_issue_99_acceptance.py` and `test_exposure_limits.py`, and add one focused regression test in `EnvelopeIsApprovedInputTests` (`test_issue_99_acceptance.py`) verifying both the `_loaded is None` case and the foreign-module `_loaded` case while `zava_forward.core.store` is loaded.

#### Boundaries

* Included: `src/core/tests/test_issue_99_acceptance.py`, `src/core/tests/test_exposure_limits.py`.
* Excluded: Removing any existing tests (`0` removals) or adding more than `<= 2` new test methods.

#### Likely Targets

* src/core/tests/test_issue_99_acceptance.py:
  * Import `importlib` and `ModuleType` (`from types import ModuleType`).
  * Define `_ensure_local_exposure_limits() -> None`:
    1. Ensure `sys.path[:1] == [str(_CORE_SRC)]`; if not, prepend `str(_CORE_SRC)` (deduplicating any later occurrence) and call `importlib.invalidate_caches()`.
    2. For `(pkg_name, pkg_dir)` in `(("zava_forward", str(_CORE_SRC / "zava_forward")), ("zava_forward.core", str(_CORE_SRC / "zava_forward" / "core")))`: if `pkg := sys.modules.get(pkg_name)` has `__path__` and `list(pkg.__path__)[:1] != [pkg_dir]`, assign `pkg.__path__ = [pkg_dir, *(p for p in pkg.__path__ if p != pkg_dir)]` (no-op in normal PEP 420 `_NamespacePath` state because step 1 already places `pkg_dir` first).
    3. Inspect `loaded = sys.modules.get("zava_forward.core.exposure_limits")`. If `loaded is None`, do **nothing** to `sys.modules`. If `loaded is not None`, check `loaded_file = getattr(loaded, "__file__", None)`; only when `not (isinstance(loaded_file, str) and bool(loaded_file) and Path(loaded_file).resolve().is_relative_to(_CORE_SRC))`, call `sys.modules.pop("zava_forward.core.exposure_limits", None)`, remove attribute `"exposure_limits"` from `sys.modules.get("zava_forward.core")` if present, and call `importlib.invalidate_caches()`.
  * Call `_ensure_local_exposure_limits()` immediately before `from zava_forward.core import exposure_limits as limits  # noqa: E402`.
  * Add `test_bootstrap_preserves_store_identity_and_evicts_only_foreign_exposure_limits` to `EnvelopeIsApprovedInputTests`:
    * Import `zava_forward.core.store` (`store_before = importlib.import_module("zava_forward.core.store")`, `conflict_before = getattr(store_before, "ConflictError")`) and capture `original_limits = sys.modules["zava_forward.core.exposure_limits"]` and `core_pkg = sys.modules["zava_forward.core"]` (strict `mypy`-safe dynamic attribute access without `ModuleType` `[attr-defined]` errors).
    * Inside `try ... finally` (which restores `sys.modules["zava_forward.core.exposure_limits"] = original_limits` and `setattr(core_pkg, "exposure_limits", original_limits)`):
      1. Simulate `_loaded is None` (`sys.modules.pop("zava_forward.core.exposure_limits", None)` and `delattr(core_pkg, "exposure_limits")` if `hasattr(core_pkg, "exposure_limits")`), run `_ensure_local_exposure_limits()`, re-import `zava_forward.core.exposure_limits`, and assert `sys.modules["zava_forward.core.store"] is store_before` and `getattr(store_before, "ConflictError") is conflict_before`.
      2. Simulate a foreign pre-loaded `exposure_limits` (`foreign = ModuleType("zava_forward.core.exposure_limits"); foreign.__file__ = str(_CORE_SRC.parent / "foreign_fixture" / "exposure_limits.py")` placed in `sys.modules["zava_forward.core.exposure_limits"]` and via `setattr(core_pkg, "exposure_limits", foreign)`), run `_ensure_local_exposure_limits()`, call `reloaded = importlib.import_module("zava_forward.core.exposure_limits")`, and assert `reloaded is not foreign`, `Path(reloaded.__file__ or "").resolve() == _CORE_SRC / "zava_forward" / "core" / "exposure_limits.py"`, and `sys.modules["zava_forward.core.store"] is store_before` with `getattr(importlib.import_module("zava_forward.core.store"), "ConflictError") is conflict_before`.
* src/core/tests/test_exposure_limits.py:
  * Import `importlib` and replace lines 14-21 with the identical `_ensure_local_exposure_limits()` helper and call before `from zava_forward.core import exposure_limits as limits  # noqa: E402` and `from zava_forward.core.finance import FinanceMixin  # noqa: E402`.

#### Dependencies

* none

#### Validation Expectations

* `mypy` and `ruff` pass on both modified test files; the new regression test passes and preserves `original_limits` identity for subsequent tests in the same process.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Run `src/core` static analysis, ordered multi-module `unittest`, and full `src/core` test discovery verification

#### Context

The CI `src-core` job runs `python -m unittest discover -s tests -v`, which failed when `test_bulk_edits.py` ran before `test_issue_99_acceptance.py` and `test_exposure_limits.py`. We must verify both the exact prompt validation commands and full `src/core` discovery.

#### Intent

Prove static type safety, lint/format compliance, ordered multi-file `unittest` execution, and full `src/core` `unittest discover` pass rates.

#### Boundaries

* Included: Local execution of `mypy`, `ruff`, and `unittest` in `src/core`.
* Excluded: Modifying global Python packages or pushing to GitHub.

#### Likely Targets

* Validation commands executed in `/home/azureuser/source/ama-demo-wt/feat-99-investment-envelope-2142/src/core`:
  * `python3 -m mypy`
  * `python3 -m ruff check . && python3 -m ruff format --check .`
  * `PYTHONPATH=src:tests python3 -m unittest tests/test_bulk_edits.py tests/test_issue_99_acceptance.py tests/test_exposure_limits.py tests/test_taskqueues.py -q`
  * `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q`
  * Bare `python3 -m unittest tests/test_issue_99_acceptance.py tests/test_exposure_limits.py -q` (confirming worktree isolation without `PYTHONPATH=src` also continues to pass)

#### Dependencies

* P01-T01

#### Validation Expectations

* Every command exits with code `0` and `OK`.
