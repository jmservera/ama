<!-- markdownlint-disable-file -->
# RPI Changes: Issue #99 Investment Envelope, Liquidity and Downside Tolerance Controls

## Metadata

* Task ID: fin-99-investment-envelope-2142
* Related plan: .copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`
* All remaining active-plan markers: none
* Status basis: Every task across `P01` and `P02` is implemented, reconciled, and verified against `mypy`, `ruff check`, `ruff format --check`, `test_*99*.py`, and `test_exposure_limits.py`.

## Execution Summary

Delivered the complete `src/core` engineering controls and acceptance suite for Issue #99 (`BG-008`, `RULE-011`, `RULE-012`, `OD-12`, `OD-15`). `exposure_limits.py` now validates strict `YYYY-MM-DD` ISO dates/timestamps and alias consistency, rejects unknown keys and integer-float overflows with `LimitsError`, records optional human-approved `annual_plan` ceilings and `liquidity`/`covenant` minimum headroom floors with zero invented company defaults, re-validates `limits` records inside `assess()`, separates non-negative upper-ceiling checks from signed finite minimum-floor checks so negative cash/covenant deficits report `Breach`, and emits deterministic `pause_signal` payloads (`paused=True`, `decision_required=True`, `decision_owner=restart_owner`, `automatic_cut=False`). Both `test_issue_99_acceptance.py` and `test_exposure_limits.py` use a PEP 420 namespace-safe, Ruff-clean worktree `src/` bootstrap, and `src/core/README.md` documents the module contract and governance boundaries.

## Completed Work

### Human-approved envelope, annual plan, and liquidity/covenant floor recording

* Related phase or task: `P01`, `P01-T01`
* Files: `src/core/src/zava_forward/core/exposure_limits.py`
* What changed and why: Added `_check_keys`, overflow-safe `_number`, `_iso_date`, `_iso_date_or_timestamp`, `_liquidity`, optional `envelope["annual_plan"]`, and keyword-optional `liquidity=None` in `record_limits` and `load_limits`, plus strict conflict checks when both `approved_by`/`approver` or `approved_at`/`approved_on` are supplied. Ensures limits exist strictly as attributed human-approved inputs with zero invented figures and 100% 3-argument caller compatibility.
* Completion evidence: `src/core/src/zava_forward/core/exposure_limits.py` passes strict `mypy`, `ruff check`, and unit/acceptance tests for recording, round-trip JSON loading, and refusal of missing/conflicting/compact-ISO/overflow/unknown-key inputs.
* Validation: Passed (`python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, `unittest`).

### Canonical `assess` validation and ceiling/floor breach pause-signal emission

* Related phase or task: `P01`, `P01-T02`
* Files: `src/core/src/zava_forward/core/exposure_limits.py`
* What changed and why: Updated `assess()` to re-validate `limits` canonically (returning `Held` on forged or unreadable dicts), normalize non-dict `exposure` safely, require `_non_negative_finite_observation` for upper ceilings (`envelope`, `annual_plan`, `tolerances`), accept signed `_finite_observation` for minimum floors (`liquidity`, `covenant` with explicit unit match) so negative deficits trigger `Breach`, preserve `"Over approved limit: ..."` for upper-only breaches while emitting `"Below approved minimum: ..."` for floor breaches, and attach `pause_signal` (`automatic_cut=False`).
* Completion evidence: `assess()` verified across upper breaches, floor breaches (positive shortfalls and negative deficits), combined breaches, forged dicts, negative ceiling observations, non-dict `exposure`, and within-limits non-acceleration.
* Validation: Passed (`python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, `unittest`).

### Worktree-isolated Issue #99 acceptance tests, unit regressions, and documentation

* Related phase or task: `P02`, `P02-T01`, `P02-T02`
* Files: `src/core/tests/test_issue_99_acceptance.py`, `src/core/tests/test_exposure_limits.py`, `src/core/README.md`
* What changed and why: Added PEP 420 namespace-safe worktree `src/` bootstrap in both test files, kept all existing tests (`0` removed), added `8` focused test methods (`5` in `test_issue_99_acceptance.py`, `3` in `test_exposure_limits.py`, within the `<= 12` cap), aligned canonical-attribution test construction in `test_exposure_limits.py`, and documented `exposure_limits` controls and `OD-12`/`OD-15` boundaries in `src/core/README.md`.
* Completion evidence: All 11 Issue #99 acceptance tests and all 21 `test_exposure_limits.py` tests pass against this worktree's `exposure_limits.py`.
* Validation: Passed (`python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, `python3 -m unittest discover -s tests -p 'test_*99*.py' -v`, `python3 -m unittest tests/test_exposure_limits.py tests/test_issue_99_acceptance.py -v`).

## Implementation-Time Plan and Detail Updates

None during implementation; all critique adjustments (`PC-001`..`PC-004`) were reconciled into the plan and phase details prior to implementation.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m mypy` | `src/core` | Passed | `Success: no issues found in 308 source files` |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` | Passed | `255 files already formatted` |
| `python3 -m unittest discover -s tests -p 'test_*99*.py' -v` | `src/core` | Passed | `Ran 11 tests in 0.003s — OK` (including worktree module-origin check) |
| `python3 -m unittest tests/test_exposure_limits.py tests/test_issue_99_acceptance.py -v` | `src/core` | Passed | `Ran 32 tests in 0.015s — OK` (alphabetical bare load order verified) |

## Pre-Review Reconciliation

* Plan markers and phase details: Current (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` all `[x]` / `completed`)
* Completed-work evidence and handoff prose: Current
* Validation, blockers, remaining work, and follow-up items: Current
* Review readiness: Ready for single-pass `rpi-review`

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-plan.md, `## Follow-Up Items`
* Surface `liquidity` / `covenant` minimum floor findings (`f.minimum ?? f.maximum` in `panels.js` `exposureNotice`) and `pause_signal.decision_owner` in the web Finance workbench UI (`src/api`): outside the `src/core`-scoped brief; owned by a subsequent UI slice under Issue #99.

## Return-to-Caller State

* Implementation execution status: Complete (full plan)
* Declared scope and markers: Full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`; remaining: none
* Validation coverage: `mypy`, `ruff check`, `ruff format --check`, `test_*99*.py` (11 tests), and `test_exposure_limits.py` (21 tests) all passed
* Blockers: none
* Current plan and detail updates: none during implementation
* Planning and critique state: Ready (`PC-001`..`PC-004` applied and verified)
* Follow-up items: Web Finance workbench UI floor-finding display (`src/api`)
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Parent confirmed automatic RPI Agent
