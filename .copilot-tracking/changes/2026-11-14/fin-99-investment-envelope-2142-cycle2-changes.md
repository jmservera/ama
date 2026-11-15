<!-- markdownlint-disable-file -->
# RPI Changes: Cycle-2 Fix for Issue #99 / PR #1739 `sys.modules` Test Bootstrap

## Metadata

* Task ID: fin-99-investment-envelope-2142-cycle2
* Related plan: .copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-cycle2-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-cycle2-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`
* All remaining active-plan markers: none
* Status basis: All planned tasks (`P01-T01`, `P01-T02`) and validation suites passed with exit code `0`.

## Completed Implementation Evidence

### P01-T01: Targeted `exposure_limits` Bootstrap and Store Identity Regression Test

* `src/core/tests/test_issue_99_acceptance.py`:
  * Replaced the module-import bulk `sys.modules` deletion loop (`for _mod in [m for m in sys.modules if m == "zava_forward" or m.startswith("zava_forward.")]: del sys.modules[_mod]`) with `_ensure_local_exposure_limits() -> None`.
  * `_ensure_local_exposure_limits()` prepends `str(_CORE_SRC)` to `sys.path` (calling `importlib.invalidate_caches()` on change), safely refreshes `zava_forward` and `zava_forward.core` `__path__` slices only when `list(pkg.__path__)[:1] != [pkg_dir]` (avoiding `.insert()` on PEP 420 `_NamespacePath`), leaves `sys.modules` completely untouched when `zava_forward.core.exposure_limits` is not yet loaded (`loaded is None`) or already resolves inside `_CORE_SRC`, and evicts **only** `zava_forward.core.exposure_limits` (plus `del core_pkg.exposure_limits` on `sys.modules.get("zava_forward.core")` and `importlib.invalidate_caches()`) when a pre-loaded module resolves outside `_CORE_SRC`.
  * Added `test_bootstrap_preserves_store_identity_and_evicts_only_foreign_module` to `EnvelopeIsApprovedInputTests`, verifying under `try ... finally` restoration that `zava_forward.core.store` and `store.ConflictError` keep exact object identity (`is`) across both the unloaded (`loaded is None`) and synthetic external-origin (`_CORE_SRC.parent / "foreign_fixture" / "exposure_limits.py"`) bootstrap branches while replacing the foreign `exposure_limits` module with `_CORE_SRC / "zava_forward" / "core" / "exposure_limits.py"`.
  * Implementation discovery classification (local judgment): Ruff `B009` and `B010` disallow `getattr`/`setattr` with constant attribute strings while `mypy --strict` disallows arbitrary attribute access on `ModuleType`; annotating dynamic module variables as `Any` (`store_before: Any`, `core_pkg: Any`) allowed direct attribute access (`store_before.ConflictError`, `core_pkg.exposure_limits = ...`, `del core_pkg.exposure_limits`) satisfying both `mypy --strict` and Ruff cleanly while preserving approved plan intent.
* `src/core/tests/test_exposure_limits.py`:
  * Replaced the identical module-import bulk `sys.modules` deletion loop with the matching `_ensure_local_exposure_limits()` helper before importing `zava_forward.core.exposure_limits` and `zava_forward.core.finance.FinanceMixin`.

### P01-T02: Static Analysis, Multi-Module Ordered `unittest`, Bare Worktree Isolation, and Full `src/core` Discovery

* Executed in `/home/azureuser/source/ama-demo-wt/feat-99-investment-envelope-2142/src/core`:
  * `python3 -m mypy` -> `Success: no issues found in 308 source files` (exit `0`).
  * `python3 -m ruff check .` -> `All checks passed!` (exit `0`).
  * `python3 -m ruff format --check .` -> `255 files already formatted` (exit `0`).
  * `PYTHONPATH=src:tests python3 -m unittest tests/test_bulk_edits.py tests/test_issue_99_acceptance.py tests/test_exposure_limits.py tests/test_taskqueues.py -q` -> `Ran 95 tests in 12.613s — OK` (exit `0`; reproduces the exact CI module load order where `test_bulk_edits` imports `store.ConflictError` before `test_issue_99_acceptance` and `test_exposure_limits`, followed by `test_taskqueues`).
  * `python3 -m unittest tests/test_issue_99_acceptance.py tests/test_exposure_limits.py -q` (without `PYTHONPATH=src`) -> `Ran 33 tests in 0.044s — OK` (exit `0`; confirms worktree-local `exposure_limits` resolution still works against editable installs in `~/.local`).
  * `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q` -> exit `0` across the entire `src/core` discovery suite.

## Amendments and Divergences

* Plan amendments: none.
* Divergences: none (local typing adjustment from `getattr`/`setattr` to `Any`-typed direct attribute access resolved Ruff `B009`/`B010` without altering behavior or plan intent).

## Blockers and Follow-Ups

* Blockers: none for `src/core` implementation or review readiness.
* Follow-ups carried forward unchanged:
  * Surface `liquidity` / `covenant` minimum floor findings (`f.minimum ?? f.maximum` in `panels.js` `exposureNotice`) and `pause_signal.decision_owner` in the web Finance workbench UI (`src/api`).
  * Record actual Zava North Homes Board-ratified capital envelope, liquidity/covenant thresholds, and downside tolerances (`OD-12`, `OD-15`; external human governance prerequisite, `Refs #99`).

## Review Readiness

* Ready for `rpi-review`: plan markers (`P01`, `P01-T01`, `P01-T02`), phase details (`completed`), changes evidence, validation results, blockers, and follow-ups are fully reconciled.
