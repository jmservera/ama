<!-- markdownlint-disable-file -->
# RPI Plan Critique: Cycle-2 Fix for Issue #99 / PR #1739 `sys.modules` Test Bootstrap

## Metadata

* Task ID: fin-99-investment-envelope-2142-cycle2
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-cycle2-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-cycle2-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Cycle-2 RPI fix for Issue #99 / PR #1739 on branch `feat/fin-99-investment-envelope-2142` (target `feat/demo-233-same-home-tensions-0825`) in worktree `/home/azureuser/source/ama-demo-wt/feat-99-investment-envelope-2142`. Caller requires: (1) remove bulk `zava_forward.*` `sys.modules` deletion when `_loaded is None` in `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py`, evicting only `zava_forward.core.exposure_limits` when `_loaded is not None` and outside `_CORE_SRC` while refreshing `zava_forward.core` namespace state safely; (2) record the Cycle-2 fix in `.copilot-tracking/{changes,reviews}/`; (3) validate in `src/core` with `python3 -m mypy`, `python3 -m ruff check . && python3 -m ruff format --check .`, and `PYTHONPATH=src:tests python3 -m unittest tests/test_bulk_edits.py tests/test_issue_99_acceptance.py tests/test_exposure_limits.py tests/test_taskqueues.py -q`; and (4) commit cleanly on `feat/fin-99-investment-envelope-2142` with the `Co-authored-by` trailer without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-cycle2-research.md (`C1` through `C6` and Prior Knowledge Gate), .copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-cycle2-plan.md, .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-cycle2-phase-details.md, src/core/tests/test_issue_99_acceptance.py, src/core/tests/test_exposure_limits.py, src/core/pyproject.toml.
* Decisions, dependencies, and acceptance criteria considered: Confirmed decisions to never evict `zava_forward.core.store` or sibling `zava_forward.*` modules, evict `zava_forward.core.exposure_limits` (plus `delattr` on `zava_forward.core` and safe `__path__` slice refresh) only when `_loaded is not None` and outside `_CORE_SRC`, lock test scope to `<= 2` added regression tests and `0` removals, preserve Cycle-1 RPI records, follow AMA Repository Instructions for commit identity and `Refs #99` linkage, and defer external Board `OD-12` / `OD-15` threshold ratification.
* Assessment boundary: Read-only assessment of the supplied research, plan candidate, phase-details candidate, target test files, and `src/core/pyproject.toml`. No uninspected repository files (`test_bulk_edits.py`, `test_taskqueues.py`, `.github/workflows/src-ci.yml`, `finance.py`) or live test runs were executed during critique; conclusions about those modules rely strictly on supplied research evidence (`C1` through `C6`) and static inspection of the supplied files.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Req 1 / Research `C1`, `C2`, `C3`, `C6` (surgical `exposure_limits` bootstrap in both test files) | Covered | `P01-T01` updates both `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py` with `_ensure_local_exposure_limits()`, preserving `zava_forward.core.store` when `_loaded is None` and handling Python 3.12 parent-attribute and PEP 420 `_NamespacePath` rules when `_loaded` is outside `_CORE_SRC`. |
| Caller Req 2 / AC-4 (record Cycle-2 fix in `.copilot-tracking/{changes,reviews}/`) | Partial | Plan `Implementation Context Record` names `.copilot-tracking/changes/2026-11-14/fin-99-investment-envelope-2142-cycle2-changes.md`, but omits `.copilot-tracking/reviews/` stage ownership (`rpi-review`) and sequencing before the final commit (`PC-003`). |
| Caller Req 3 / Research `C4`, `C5` / `P01-T02` (`mypy`, `ruff`, multi-module `unittest` validation) | Partial | `P01-T02` specifies the right commands, but Plan NFR and AC-3 require bare `python3 -m unittest discover -s tests -v` and bare 4-file `python3 -m unittest tests/test_bulk_edits.py ...` without `PYTHONPATH=src:tests`, conflicting with `~/.local` editable-install resolution when earlier tests load `store` and `finance` first (`PC-001`). |
| Caller Req 4 / AC-4 (clean commit on `feat/fin-99-investment-envelope-2142` with `Co-authored-by`, no push) | Partial | Stated in `User Decisions and Requirements` and `Acceptance Criteria`, but lacks an explicit post-`rpi-review` closeout boundary and AMA privacy-safe local `user.email` safeguard so `rpi-implement` does not commit before `.copilot-tracking/reviews/` is written (`PC-003`). |
| `P01-T01` (regression test under `mypy --strict` and workspace hygiene) | Partial | `P01-T01` accesses `.ConflictError` directly on `importlib.import_module(...)` (`types.ModuleType`), which fails `mypy --strict` (`[attr-defined]`), and uses a `/tmp/...` path literal for `foreign.__file__` (`PC-002`). |

## Verdict

* Verdict: Revise
* Rationale: The core bootstrap algorithm (`_ensure_local_exposure_limits()`) directly solves the root cause identified in Research `C1` through `C6`, fixes both affected test files, and handles Python 3.12 PEP 420 caching traps accurately. However, three planner-owned issues require revision before implementation: (1) Plan NFR and Acceptance Criteria require bare multi-module and full-discovery `unittest` runs without `PYTHONPATH=src:tests` that mismatch `P01-T02` and break when earlier test modules pre-load `zava_forward.core.finance` and `store` from the primary checkout's `~/.local` editable install; (2) `P01-T01`'s regression-test pseudocode triggers `mypy --strict` `[attr-defined]` errors on `ModuleType` and embeds a `/tmp/...` literal; and (3) stage sequencing for `.copilot-tracking/{changes,reviews}/` and the final privacy-safe git commit is underspecified between `rpi-implement` and `rpi-review`.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Plan NFR and Acceptance Criteria require bare multi-module and full-suite `unittest` commands without `PYTHONPATH=src:tests` that conflict with `~/.local` import order and mismatch `P01-T02`

* Related IDs: Caller Req 3, Research `C1`, `C2`, `C3`, `C5`, NFR-1, AC-3, `P01-T02`
* Evidence: .copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-cycle2-plan.md, .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-cycle2-phase-details.md, .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-cycle2-research.md, src/core/tests/test_exposure_limits.py, src/core/pyproject.toml
* Concern: Plan Non-Functional Requirements require 100% pass rate on bare `python3 -m unittest discover -s tests -v` in `src/core`, and Plan Acceptance Criteria require bare `python3 -m unittest tests/test_bulk_edits.py tests/test_issue_99_acceptance.py tests/test_exposure_limits.py tests/test_taskqueues.py -q` (without `PYTHONPATH=src:tests`). By contrast, Phase Details `P01-T02` runs `PYTHONPATH=src:tests` for the 4-file ordered run and `discover -s tests -q`, scoping bare `unittest` only to `python3 -m unittest tests/test_issue_99_acceptance.py tests/test_exposure_limits.py -q`. Per Research (`Prior Knowledge Gate`, `C3`), bare `python3` in this secondary worktree resolves `zava_forward.core` to `/home/azureuser/source/ama/src/core/src/zava_forward/core` via `~/.local` editable install until `_CORE_SRC` is prepended to `sys.path`. When `test_bulk_edits.py` (or earlier discovery modules) runs before `test_issue_99_acceptance.py`, it loads `zava_forward.core.store` and `zava_forward.core.finance` from `/home/azureuser/source/ama/src/core/src`; because the Cycle-2 fix intentionally preserves already-loaded `zava_forward.core.*` modules, `src/core/tests/test_exposure_limits.py` (`from zava_forward.core.finance import FinanceMixin`) and stacked-branch tests bind to stale modules outside this worktree, and direct multi-file runs without `PYTHONPATH=src:tests` also omit `tests` from `sys.path` (`mypy_path = ["src", "tests"]` in `src/core/pyproject.toml`).
* Impact: `P01-T02` does not verify the bare commands written in Plan NFR and Acceptance Criteria, and executing those bare multi-module or full-discovery commands during `rpi-implement` or `rpi-review` can fail against stale `/home/azureuser/source/ama/src/core/src` modules (`FinanceMixin.exposure_signal` or stacked `feat/demo-233-same-home-tensions-0825` code) or missing `tests/` helper imports.
* Smallest useful change: Update Plan `User Decisions and Requirements`, `Non-Functional Requirements`, and `Acceptance Criteria` to match `P01-T02`: require `PYTHONPATH=src:tests python3 -m unittest tests/test_bulk_edits.py tests/test_issue_99_acceptance.py tests/test_exposure_limits.py tests/test_taskqueues.py -q` and `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q` for multi-module and full-suite runs, and scope bare `unittest` worktree-isolation verification to `python3 -m unittest tests/test_issue_99_acceptance.py tests/test_exposure_limits.py -q`.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: `fin-99-investment-envelope-2142-cycle2-plan.md` NFR and Acceptance Criteria list the exact `PYTHONPATH=src:tests` multi-module/discovery commands and bare two-file Issue #99 isolation command matching `P01-T02` in `fin-99-investment-envelope-2142-cycle2-phase-details.md`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: `P01-T01` regression-test specification uses `ModuleType.ConflictError` attribute access under `mypy --strict` and a `/tmp/...` path literal

* Related IDs: NFR-1, `P01-T01`
* Evidence: .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-cycle2-phase-details.md, src/core/pyproject.toml
* Concern: `P01-T01` specifies `store_before = importlib.import_module("zava_forward.core.store")`, `conflict_before = store_before.ConflictError`, and `importlib.import_module("zava_forward.core.store").ConflictError is conflict_before`, as well as binding `foreign` on `core_pkg` and setting `foreign.__file__ = "/tmp/foreign/zava_forward/core/exposure_limits.py"`. In `src/core/pyproject.toml`, `[tool.mypy]` sets `strict = true` and `test_issue_99_acceptance` is not in any `ignore_errors` override. Because `importlib.import_module(...)` returns `types.ModuleType`, accessing `.ConflictError` directly on `ModuleType` (or assigning `core_pkg.exposure_limits = foreign` rather than `setattr`) fails `python3 -m mypy` with `[attr-defined]`. In addition, embedding a `/tmp/...` path literal is unnecessary when a deterministic worktree-external path (`str(_CORE_SRC.parent / "foreign_fixture" / "exposure_limits.py")`) avoids `/tmp` references entirely.
* Impact: Following `P01-T01` literally produces avoidable `mypy --strict` failures during implementation and introduces a `/tmp/...` string literal into `src/core/tests/test_issue_99_acceptance.py`.
* Smallest useful change: Revise `P01-T01` in `fin-99-investment-envelope-2142-cycle2-phase-details.md` to retrieve `ConflictError` via `getattr(store_before, "ConflictError")` (and mutate `core_pkg` via `setattr` / `delattr`), and set `foreign.__file__` to `str(_CORE_SRC.parent / "foreign_fixture" / "exposure_limits.py")`.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: `P01-T01` in `fin-99-investment-envelope-2142-cycle2-phase-details.md` specifies `getattr(..., "ConflictError")`, `setattr` / `delattr` on `core_pkg`, and a non-`/tmp` synthetic foreign `__file__` path outside `_CORE_SRC`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Plan Acceptance Criteria require `.copilot-tracking/{changes,reviews}/` and a clean commit with empty `git status --short`, but stage sequencing and repository commit safeguards are omitted

* Related IDs: Caller Req 2, Caller Req 4, AC-4, `P01`
* Evidence: .copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-cycle2-plan.md, .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-cycle2-phase-details.md, .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-cycle2-research.md
* Concern: Caller Requirements 2 and 4 and Plan Acceptance Criterion 4 require recording Cycle-2 RPI artifacts in `.copilot-tracking/{changes,reviews}/` and committing cleanly on `feat/fin-99-investment-envelope-2142` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, no push, and an empty `git status --short`. However, `Phase Checklist` stops at `P01-T02` (test execution), and `Implementation Context Record` documents only `.copilot-tracking/changes/...` (`rpi-implement`) without recording `.copilot-tracking/reviews/` (`rpi-review` review log alongside this plan critique) or specifying that the git commit occurs after `rpi-review` writes its review artifact using the AMA Repository Instructions privacy-safe local email (`gh api user` -> `{id}+{login}@users.noreply.github.com` via `git config --local user.email`) and non-closing `Refs #99` reference.
* Impact: If `rpi-implement` commits immediately after `P01-T02`, subsequent `rpi-review` artifacts under `.copilot-tracking/reviews/` either leave `git status --short` dirty (violating AC-4) or force an extra commit because amending existing commits requires explicit owner permission.
* Smallest useful change: Document the stage-handoff boundary in `Implementation Context Record` (and `P01` boundaries/notes): `rpi-implement` completes `P01-T01` and `P01-T02` and writes `.copilot-tracking/changes/2026-11-14/fin-99-investment-envelope-2142-cycle2-changes.md` without committing prematurely; `rpi-review` writes the Cycle-2 review artifact in `.copilot-tracking/reviews/`; and post-review closeout verifies repository-local `{id}+{login}@users.noreply.github.com` via `gh api user` and creates one clean commit on `feat/fin-99-investment-envelope-2142` (`Refs #99` + `Co-authored-by` trailer, no push, `git status --short` empty).
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: `fin-99-investment-envelope-2142-cycle2-plan.md` `Implementation Context Record` and phase boundaries explicitly map `.copilot-tracking/changes/`, `.copilot-tracking/reviews/`, privacy-safe local `git config --local user.email`, and post-`rpi-review` single-commit closeout without push.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Catching `src/core/tests/test_exposure_limits.py` alongside `src/core/tests/test_issue_99_acceptance.py` prevents the exact same mid-discovery `sys.modules` wipe from recurring one test file later in `src-core` CI.
* Research `C6` and `P01-T01` accurately address both Python 3.12 PEP 420 failure modes in the foreign-origin fallback branch: clearing the cached `exposure_limits` attribute on `sys.modules["zava_forward.core"]` via `delattr` and avoiding `_NamespacePath.insert()` via slice reassignment only when `list(pkg.__path__)[:1] != [pkg_dir]`.
* Restoring `original_limits` in both `sys.modules["zava_forward.core.exposure_limits"]` and `zava_forward.core` inside `try ... finally` preserves `limits.LimitsError` class identity across subsequent tests in the same `unittest` process.
* Residual risk (accepted): In a multi-worktree developer shell without `PYTHONPATH=src:tests`, running unrelated test modules before `test_issue_99_acceptance.py` or `test_exposure_limits.py` still resolves those earlier modules' imports via the active `~/.local` editable install; CI (`src-core`) and `PYTHONPATH=src:tests` runs are unaffected once `PC-001` aligns the validation contract.

## Questions or Blocking Evidence Gaps

* None. All three findings are direct planner corrections resolvable from existing supplied evidence.

## Limitations

* Per `rpi-plan-critique` constraints, this critique evaluated only the supplied artifacts and target files without inspecting `src/core/tests/test_bulk_edits.py`, `src/core/tests/test_taskqueues.py`, `src/core/src/zava_forward/core/finance.py`, or `.github/workflows/src-ci.yml` directly, and without executing `mypy`, `ruff`, or `unittest`.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent (`rpi-plan`)
* Smallest next action: Apply direct planner revisions for `PC-001`, `PC-002`, and `PC-003` to the Cycle-2 plan and phase details, record their disposition, and finalize the plan for `rpi-implement` without re-running critique.
* User response required: no
