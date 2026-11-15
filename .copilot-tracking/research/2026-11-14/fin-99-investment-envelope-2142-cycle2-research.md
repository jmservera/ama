<!-- markdownlint-disable-file -->

# Task Research: fin-99-investment-envelope-2142-cycle2

| Field              | Value                                                                                        |
|--------------------|----------------------------------------------------------------------------------------------|
| Date               | 2026-11-14                                                                                   |
| Researcher / agent | rpi-research (via RPI Agent)                                                                 |
| Status             | Complete                                                                                     |
| Artifact path      | .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-cycle2-research.md     |

## Research Brief

* What to research: Root cause of the 40 downstream `src-core` CI `unittest discover` errors/failures introduced by Cycle-1's `sys.modules` bootstrap in `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py`, plus PEP 420 namespace package caching semantics when isolating `zava_forward.core.exposure_limits` to the local worktree `src/`.
* Why it matters: In `src-core` CI (`python -m unittest discover -s tests -v`), test discovery imports test modules alphabetically before running test cases. Evicting all `zava_forward.*` modules when `exposure_limits` is not yet imported splits module and exception class identity (`zava_forward.core.store.ConflictError`, etc.) across earlier and later test modules (`test_bulk_edits.py`, `test_taskqueues.py`, etc.).
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` in the Cycle-2 automatic RPI fix loop for Issue #99 / PR #1739.
* Scope: `src/core/tests/test_issue_99_acceptance.py`, `src/core/tests/test_exposure_limits.py`, `src/core/src/zava_forward/core/finance.py`, `src/core/tests/` `sys.modules` usage, and `.github/workflows/src-ci.yml`.
* Non-goals: Modifying `exposure_limits.py` domain logic (already conformant in Cycle-1), modifying shared `~/.local` editable installs, modifying `src/api`, or pushing to remote.
* Criteria: Zero bulk eviction of `zava_forward.*` modules; preserve `zava_forward.core.store` and class identities across multi-file `unittest` discovery; still resolve `zava_forward.core.exposure_limits` to `_CORE_SRC` under both `PYTHONPATH=src:tests` and bare `python3 -m unittest` in a multi-worktree environment; pass `mypy`, `ruff check`, `ruff format --check`, and ordered multi-module `unittest`.
* Requested outputs: Converged surgical bootstrap design for `test_issue_99_acceptance.py` and `test_exposure_limits.py` plus regression test strategy.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                      |
|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Which files perform bulk `sys.modules` eviction, why did `_loaded is None` break `unittest discover`, and how does Python 3.12 PEP 420 import resolution cache `exposure_limits`? |
| Codebase scope                       | `src/core/`, `.github/workflows/src-ci.yml`, `.copilot-tracking/`                                                          |
| External scope                       | none                                                                                                                       |
| Initial internal candidate areas     | `src/core/tests/test_issue_99_acceptance.py`, `src/core/tests/test_exposure_limits.py`, `src/core/src/zava_forward/core/finance.py` |
| Initial external candidate areas     | none                                                                                                                       |
| Research posture                     | focused                                                                                                                    |
| Posture provenance                   | default (bounded CI regression fix with exact failing snippet, named files, and reproduction command)                      |
| Explicit limits / deadline           | Scoped to `src/core/tests/` and `.copilot-tracking/`; commit on `feat/fin-99-investment-envelope-2142`; do not push        |
| Posture-specific completion basis    | focused scope and materiality                                                                                              |
| Edits allowed during research?       | no, research-only                                                                                                          |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                       |
| Known constraints / excluded sources | Shared multi-worktree environment: do not alter `~/.local` site-packages; do not invent company thresholds (`Refs #99`)    |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                     | Match and provenance                              | Scoped authority or output contract                     | Selected / skipped reason                                              |
|---------------------|-------------------------------|---------------------------------------------------|---------------------------------------------------------|------------------------------------------------------------------------|
| Instruction         | AMA Repository Instructions   | `applyTo: "**"` matches `src/core` and tracking   | Governs focused validation tier, commit rules, `Refs #99` | Selected: governs validation, evidence retention, and branch safeguards |
| Skill               | `python-foundational`         | Python 3.12 import/testing match                  | Optional Python guidance                                | Skipped: `src/core/pyproject.toml` defines exact `mypy` and `ruff` gates |
| Research specialist | `hve-core-all:rpi-researcher` | Host-registered general research worker           | Delegated research lane artifact                        | Skipped (inline): <=5 direct file reads and runtime probes cover scope |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                   | Answers / unanswered     | Resulting decision or selected further research                        |
|------------------|-----------------------------------------------------------------------------------------|--------------------------|------------------------------------------------------------------------|
| Intake           | Non-interactive automatic RPI fix session with exact CI failure diagnosis and commands  | No interaction available | Proceed in focused convergence mode                                    |
| Direction change | Grep confirmed `test_exposure_limits.py` has the identical bulk `sys.modules` eviction  | No interaction needed    | Fix both `test_issue_99_acceptance.py` and `test_exposure_limits.py`   |
| Convergence      | Contrarian Python 3.12 probe uncovered parent-package attribute cache and `_NamespacePath` behavior | No interaction needed | Stop research after Cycle 1 with Planning Readiness `Ready` |

## Scope and Success Criteria

* Scope: Module-import bootstrap and regression tests in `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py`, plus Cycle-2 RPI tracking artifacts.
* Assumptions: `zava_forward` and `zava_forward.core` are PEP 420 namespace packages without `__init__.py` files (verified directly).
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Remove bulk `zava_forward.*` `sys.modules` eviction from `src/core/tests/test_issue_99_acceptance.py`, check and fix `src/core/tests/test_exposure_limits.py` as well, record Cycle-2 RPI artifacts including `.copilot-tracking/{changes,reviews}/`, validate with `mypy`, `ruff`, and ordered `unittest` (`test_bulk_edits.py` before `test_issue_99_acceptance.py` and `test_exposure_limits.py`), and commit cleanly without pushing.
* Inferred research questions: Whether any other test file evicts `zava_forward.*` from `sys.modules`, whether `finance.py` or `store.py` imports `exposure_limits` eagerly, and how `from zava_forward.core import exposure_limits` behaves when evicting only `zava_forward.core.exposure_limits`.
* Caller constraints and non-goals: Do not push; preserve existing behavior and Cycle-1 RPI artifacts.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|---------------------|---------------------------------------------------|
| narrow                                                   | Restrict code changes to `src/core/tests/` bootstrap and regression coverage | User prompt (Intake) | Preserves `exposure_limits.py` implementation unchanged |
| exclude                                                  | Never delete `zava_forward.core.store` or unrelated `zava_forward.*` modules; do not push | User prompt (Intake) | Prohibits bulk `sys.modules` deletion and remote push |

## Research Questions

|  # | Sub-question | Type (depth / breadth / straightforward) | Priority | Status |
|---:|--------------|------------------------------------------|----------|--------|
| Q1 | Which files in `src/core` manipulate `sys.modules` for `zava_forward`? | straightforward | H | answered |
| Q2 | Why did `_loaded is None` trigger mid-discovery `sys.modules` eviction after `test_bulk_edits.py` ran? | depth | H | answered |
| Q3 | What exact operations are required to ensure `from zava_forward.core import exposure_limits` resolves to `_CORE_SRC` in both clean and pre-imported states without touching other `zava_forward.*` modules? | depth | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-research.md`, `.copilot-tracking/changes/2026-11-14/fin-99-investment-envelope-2142-changes.md`, `.copilot-tracking/reviews/logs/2026-11-14/fin-99-investment-envelope-2142-review.md`, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`.
* Reused (verified) findings: Bare `python3` in a secondary worktree resolves `zava_forward.core` to `/home/azureuser/source/ama/src/core/src/zava_forward/core` via `~/.local` editable install unless worktree `src/` precedes it on `sys.path`.
* Superseded / stale: Cycle-1's bootstrap assumed deleting all `zava_forward.*` entries when `_loaded is None` was harmless; Cycle-1 only ran `test_exposure_limits.py` + `test_issue_99_acceptance.py` in isolation and missed test modules loaded earlier in alphabetical `unittest discover` order (`test_bulk_edits.py`).

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow to `src/core/tests/`; exclude bulk `sys.modules` deletion and remote push
* Active research posture and completion basis: focused; focused scope and materiality
* Explicit limits or deadline effect: Changes bounded to `src/core/tests/` and `.copilot-tracking/`

#### Wave 1: Wider

* Plan and independent lanes: Search `src/core/tests` and `src/core/src` for `sys.modules`, `__path__`, and `exposure_limits` references, and inspect `.github/workflows/src-ci.yml`.
* Worker evidence relationships or inline fallback: Inline (`Q1 -> C1, C2, C3, C4`).
* Reflection: Exactly two files (`test_issue_99_acceptance.py` and `test_exposure_limits.py`) contain the bulk `del sys.modules[_mod]` loop (`C1`, `C2`). No module in `src/core/src` imports `exposure_limits` at module import time; `finance.py` imports it lazily inside `FinanceMixin.exposure_signal` (`C3`).

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Reproduce the CI failure order (`test_bulk_edits.py` -> `test_issue_99_acceptance.py` -> `test_exposure_limits.py` -> `test_taskqueues.py`) and inspect module state after importing `zava_forward.core.store`.
* Plan and independent lanes: Inline reproduction and Python 3.12 namespace-package inspection.
* Worker evidence relationships or inline fallback: Inline (`Q2 -> C1, C2, C3, C5`).
* Reflection: Importing `zava_forward.core.store` loads `store` and `finance`, leaving `zava_forward.core.exposure_limits` unloaded (`_loaded is None`). When `unittest` subsequently imports `test_issue_99_acceptance.py` (and again in `test_exposure_limits.py`), `_loaded is None` is `True`, wiping `zava_forward.core.store` and splitting `ConflictError` class identity across modules (`C5`). Meanwhile, PEP 420 `_NamespacePath` on `zava_forward` and `zava_forward.core` automatically recomputes `list(zava_forward.core.__path__)[0]` to `_CORE_SRC / "zava_forward" / "core"` as soon as `str(_CORE_SRC)` is placed at `sys.path[0]` (`C6`).

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Test whether simply changing `if _loaded is None or not ...:` to `if _loaded is not None and not ...: del sys.modules["zava_forward.core.exposure_limits"]` and calling `_core_pkg.__path__.insert(0, ...)` works when `exposure_limits` WAS already imported from another worktree.
* Plan and independent lanes: Inline adversarial Python 3.12 probes against pre-imported `exposure_limits` and `_NamespacePath` mutation.
* Worker evidence relationships or inline fallback: Inline (`Q3 -> C6`):
  1. **Parent-package attribute cache trap**: In Python 3.12, `from zava_forward.core import exposure_limits as limits` checks `getattr(sys.modules["zava_forward.core"], "exposure_limits")` BEFORE importing from `sys.modules`. Deleting `sys.modules["zava_forward.core.exposure_limits"]` without `delattr(_core_pkg, "exposure_limits")` silently returns the stale module from `/home/azureuser/source/ama/...` (`C6`)!
  2. **`_NamespacePath.insert` trap**: PEP 420 `_NamespacePath` only exposes `.append()`, NOT `.insert()`. Calling `_core_pkg.__path__.insert(0, ...)` would crash with `AttributeError`. `_NamespacePath` updates automatically when `sys.path` changes; only if `list(_core_pkg.__path__)[:1] != [_core_dir]` (e.g., if `__path__` was replaced with a plain list) should `_core_pkg.__path__` be reassigned (`C6`).
* Reflection: Both contrarian findings prevented subtle bugs in the fallback eviction branch.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|----------------------------|
| Prepend `_CORE_SRC` to `sys.path` + `importlib.invalidate_caches()`, and do NOTHING to `sys.modules` when `_loaded is None` | C1, C2, C5, C6 | accepted | Preserves `zava_forward.core.store` and all sibling modules while PEP 420 `_NamespacePath` resolves `exposure_limits` from `_CORE_SRC` | Selected recommendation |
| When `_loaded is not None` and outside `_CORE_SRC`, evict ONLY `zava_forward.core.exposure_limits`, `delattr(_core_pkg, "exposure_limits")`, refresh `_core_pkg.__path__` via slice assignment only if `_core_dir` is not already first, and call `importlib.invalidate_caches()` | C3, C6 | accepted | Handles pre-imported cross-worktree `exposure_limits` cleanly without `AttributeError` or stale parent-attribute hits | Selected recommendation |
| Apply identical fix in both `test_issue_99_acceptance.py` and `test_exposure_limits.py` and add focused class-identity/eviction regression test | C1, C2, C5 | accepted | Eliminates both bulk eviction sites and guards against regression | Selected recommendation |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Exact root cause reproduced and replacement verified in Python 3.12 runtime probes across all import orders.
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: bounded two-file test-bootstrap regression reproduced and probed directly in <=5 targeted searches/commands.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | `test_issue_99_acceptance.py` deletes every `zava_forward` and `zava_forward.*` entry in `sys.modules` whenever `_loaded is None` or outside `_CORE_SRC` | `src/core/tests/test_issue_99_acceptance.py:13` | view | high | Lines 10-16 inspected |
| C2 | `test_exposure_limits.py` contains the identical bulk `del sys.modules[_mod]` loop when `_loaded is None` or outside `_CORE_SRC` | `src/core/tests/test_exposure_limits.py:14` | view | high | Lines 11-18 inspected; only other `del sys.modules` match in `src/core/tests` |
| C3 | `FinanceMixin.exposure_signal` lazily runs `from . import exposure_limits as el` at call time, so importing `zava_forward.core.store` loads `store` and `finance` while leaving `zava_forward.core.exposure_limits` absent (`None`) in `sys.modules` | `src/core/src/zava_forward/core/finance.py:360` | grep / view | high | Confirmed by runtime probe |
| C4 | Hosted CI `src-core` executes `python -m unittest discover -s tests -v`, which imports all `test_*.py` modules alphabetically before running tests | `.github/workflows/src-ci.yml:55` | grep | high | `test_bulk_edits.py` loads before `test_exposure_limits.py` and `test_issue_99_acceptance.py`, followed by `test_taskqueues.py` |
| C5 | Running `PYTHONPATH=src:tests python3 -m unittest tests/test_bulk_edits.py tests/test_issue_99_acceptance.py tests/test_exposure_limits.py tests/test_taskqueues.py -q` reproduces the `test_bulk_edits` errors caused by split `zava_forward.core.store` module/class identity | `src/core/tests/test_issue_99_acceptance.py:14` | bash | high | Reproduced directly prior to fix |
| C6 | Python 3.12 PEP 420 `_NamespacePath` auto-updates `zava_forward.core.__path__[0]` when `sys.path[0]` becomes `_CORE_SRC`, lacks `.insert()`, and caches bound submodule attributes on `sys.modules["zava_forward.core"]` across `del sys.modules["zava_forward.core.exposure_limits"]` unless `delattr` is also called | `src/core/pyproject.toml:23` | bash / view | high | Verified by Python 3.12 runtime probes (`namespaces = true`) |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* none

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | Both `test_issue_99_acceptance.py` and `test_exposure_limits.py` perform bulk `zava_forward.*` deletion; no other `src/core/tests` file does so | C1, C2 | high | Both files must be updated together |
| Q2 | `store` does not eagerly import `exposure_limits` (`_loaded is None`), so both test modules unconditionally wiped `zava_forward.*` mid-discovery after `test_bulk_edits.py` had already bound `store.ConflictError` | C1, C2, C3, C4, C5 | high | Never evict when `_loaded is None`, and never evict sibling `zava_forward.*` modules |
| Q3 | Prepending `_CORE_SRC` to `sys.path` + `importlib.invalidate_caches()` suffices when `_loaded is None`; when `_loaded` is non-`None` and outside `_CORE_SRC`, evicting `sys.modules["zava_forward.core.exposure_limits"]` + `delattr(_core_pkg, "exposure_limits")` + safe `__path__` slice check + `importlib.invalidate_caches()` isolates `exposure_limits` without touching `store` | C6 | high | Ready for implementation in `rpi-plan` |

## Key Discoveries

* `test_exposure_limits.py` has the exact same `if _loaded is None or ...: del sys.modules[_mod]` bug as `test_issue_99_acceptance.py`; fixing only `test_issue_99_acceptance.py` would still fail CI because `test_exposure_limits.py` would wipe `sys.modules` right after it (`C1`, `C2`).
* Deleting `sys.modules["zava_forward.core.exposure_limits"]` without removing the cached `exposure_limits` attribute on `sys.modules["zava_forward.core"]` causes `from zava_forward.core import exposure_limits` to return the stale pre-existing module (`C6`).
* PEP 420 `_NamespacePath` refreshes automatically from `sys.path` and raises `AttributeError` on `.insert()`, so `__path__` fallback refresh must check `list(_core_pkg.__path__)[:1] != [_core_dir]` and assign a list slice only if needed (`C6`).

### Complete Examples

```python
_CORE_SRC = Path(__file__).resolve().parents[1] / "src"
if sys.path[:1] != [str(_CORE_SRC)]:
    sys.path[:] = [str(_CORE_SRC), *(p for p in sys.path if p != str(_CORE_SRC))]
    importlib.invalidate_caches()
_loaded = sys.modules.get("zava_forward.core.exposure_limits")
if _loaded is not None and not Path(_loaded.__file__ or "").resolve().is_relative_to(_CORE_SRC):
    sys.modules.pop("zava_forward.core.exposure_limits", None)
    _core_pkg = sys.modules.get("zava_forward.core")
    if _core_pkg is not None:
        if hasattr(_core_pkg, "exposure_limits"):
            delattr(_core_pkg, "exposure_limits")
        _core_dir = str(_CORE_SRC / "zava_forward" / "core")
        if hasattr(_core_pkg, "__path__") and list(_core_pkg.__path__)[:1] != [_core_dir]:
            _core_pkg.__path__ = [_core_dir, *(p for p in _core_pkg.__path__ if p != _core_dir)]
    importlib.invalidate_caches()
```

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Replace bulk `zava_forward.*` `sys.modules` deletion in both `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py` with targeted single-module eviction of `zava_forward.core.exposure_limits` only when `_loaded is not None` and its resolved `__file__` is outside `_CORE_SRC` (clearing parent attribute `exposure_limits`, refreshing `__path__` safely if needed, and invalidating import caches), plus add a focused regression test verifying `zava_forward.core.store` and `ConflictError` identity preservation.
* Rationale: Preserves 100% module and exception identity across `unittest discover` in CI while maintaining worktree isolation under bare `python3 -m unittest` on multi-worktree hosts.
* Evidence refs: C1, C2, C3, C4, C5, C6
* Implementation impact: `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py`.
* Confidence: high: reproduced failure and verified Python 3.12 PEP 420 import mechanics directly.

File tree:

```text
src/core/tests/
  test_exposure_limits.py      (modify: targeted single-module eviction bootstrap)
  test_issue_99_acceptance.py  (modify: targeted single-module eviction bootstrap + store identity regression test)
```

### Alternative: Remove worktree `sys.path` bootstrap entirely and rely solely on `PYTHONPATH=src` or editable install

* Approach: Delete `_CORE_SRC` manipulation and import `from zava_forward.core import exposure_limits as limits` directly.
* Trade-offs: Simplest import header, but fails bare `python3 -m unittest discover -s tests -p 'test_*99*.py' -v` in secondary worktrees when `~/.local` editable install points to `/home/azureuser/source/ama/src/core/src` (`test_module_resolves_to_local_worktree_source` fails).
* Evidence refs: C1, C6
* Rejection rationale: Breaks bare-`unittest` worktree isolation established in Cycle-1.

### Alternative: Evict `sys.modules["zava_forward.core.exposure_limits"]` unconditionally even when `_loaded is None` or already under `_CORE_SRC`

* Approach: Always pop `zava_forward.core.exposure_limits` at the top of each test file.
* Trade-offs: Avoids wiping `store`, but needlessly reloads `exposure_limits` and splits `limits.LimitsError` identity between `test_exposure_limits.py` and `test_issue_99_acceptance.py` when both run in the same `unittest` process.
* Evidence refs: C1, C2, C6
* Rejection rationale: Evicting only when `_loaded is not None` and outside `_CORE_SRC` preserves `LimitsError` identity across both test files as well.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: none
* Follow-up: Surface `pause_signal.decision_owner` and `liquidity`/`covenant` minimum floor findings in `src/api` Finance workbench UI (`panels.js`), carried forward from Cycle-1.
* Residual uncertainty: none within `src/core` scope.

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------|-----------|--------------|--------------|
| Never delete `zava_forward` or sibling `zava_forward.*` modules from `sys.modules` in `test_issue_99_acceptance.py` or `test_exposure_limits.py` | confirmed | user / evidence | Prevents class-identity split (`ConflictError`, etc.) across `unittest discover` | C1, C2, C4, C5 | Fixes all 40 downstream `src-core` CI failures |
| Evict `zava_forward.core.exposure_limits` (and `delattr` on `zava_forward.core`) only when `_loaded is not None` and its resolved path is outside `_CORE_SRC` | confirmed | evidence | Preserves worktree isolation in shared environments and `LimitsError` identity across test files | C3, C6 | Works identically in CI (`PYTHONPATH` / clean venv) and bare multi-worktree runs |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Zava North Homes Board-approved `OD-12` / `OD-15` thresholds | Board / Finance Lead ratification outside repository code | Zava North Homes Board / Finance Lead | Required before closing Issue #99 (`Refs #99` only) | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Audit `src/api` Finance workbench UI rendering of floor findings | Prepares separate `src/api` UI slice | User selection in post-Review follow-up | deferred | Q1; C3 |

## Planning Readiness

* Status: Ready
* Decision state: Converged on targeted single-module `exposure_limits` bootstrap in `test_issue_99_acceptance.py` and `test_exposure_limits.py` with regression test coverage
* Evidence basis: C1, C2, C3, C4, C5, C6
* Preconditions met: CI failure reproduced locally; all `sys.modules` touchpoints in `src/core` inventoried; Python 3.12 PEP 420 parent-attribute and `_NamespacePath` semantics verified
* Blockers: none
* Smallest action to change readiness: none

## Closeout Record

| Field                            | Record                                                                                     |
|----------------------------------|--------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                   |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian                                                     |
| Lane evidence or inline fallback | inline: bounded two-file `src/core/tests` investigation completed directly                 |
| Research disposition             | executed                                                                                   |
| Planning Readiness               | Ready (C1, C2, C3, C4, C5, C6)                                                             |
| Blockers                         | none                                                                                       |
| Continuation owner and state     | confirmed automatic RPI Agent; automatic continuation to `rpi-plan`                        |

## Advisory Next Step

| Field                            | Record                                                                                     |
|----------------------------------|--------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                   |
| Planning Readiness               | Ready (C1, C2, C3, C4, C5, C6)                                                             |
| Output mode and planning support | convergence; yes, single recommended bootstrap fix selected with verified Python 3.12 behavior |
| Acting owner                     | confirmed automatic RPI Agent                                                              |
| Required gates or confirmations  | Research disposition recorded (passed); Planning Readiness Ready (passed); pre-transition state write (passed) |
| Continuation result              | automatic continuation to `rpi-plan`                                                       |
| Primary evidence file            | .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-cycle2-research.md   |
| Notes for planning or re-entry   | Plan single-phase update to `test_issue_99_acceptance.py` and `test_exposure_limits.py`, run single-pass plan critique, implement, validate, and review |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: Focused scope saturated with direct reproduction and runtime verification; further research is immaterial.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: All sections from Research Brief through Sources.
* Missing or limited sections: none
