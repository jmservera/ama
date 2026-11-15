<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #225 Cycle-2 CI Conformance Fix

## Metadata

* Task ID: 2026-11-14-issue-225-c2-conformance-fix
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/issue-225-c2-conformance-fix-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/issue-225-c2-conformance-fix-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Resolve the `src-ci.yml` (`src-api`) failure in `tests/test_role_screens_conformance.py` (`RoleScreenConformance.test_interactive_controls_are_native_and_keyboard_operable`, line 78) caused by inline `onclick:` on `screenJumpNav` anchors in `src/api/src/zava_forward/api/web/role-screens.js` on branch `feat/ux-225-finance-screens-wcag-1745` (targeting `feat/demo-233-same-home-tensions-0825`, PR #1715, Issue #225); preserve all pre-existing `.copilot-tracking/` artifacts; record Cycle-2 RPI artifacts under `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/`; ensure `mypy`, `ruff check .`, `ruff format --check .`, and `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_role_screens_conformance.py tests/test_finance_screens_wcag_225.py -v` pass cleanly; commit locally with privacy-safe repository-local Git email and Copilot trailer without pushing.
* Research and evidence considered: `.copilot-tracking/research/2026-11-14/issue-225-c2-conformance-fix-research.md`, `.copilot-tracking/plans/2026-11-14/issue-225-c2-conformance-fix-plan.md`, `.copilot-tracking/details/2026-11-14/issue-225-c2-conformance-fix-phase-details.md`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_role_screens_conformance.py`, `src/api/tests/test_finance_screen_wcag.py`, `src/api/tests/test_finance_grants_screens.py`, `src/api/tests/test_asset_exec_screen_wcag.py`, `src/api/checks/finance_screens_browser_check.py`, and `src/api/pyproject.toml`.
* Decisions, dependencies, and acceptance criteria considered: `FR-01` through `FR-03`, `NFR-01` through `NFR-02`, `AC-01` through `AC-05`, locked test ownership and bounds, AMA Web Development Guidance (`web-design-guidelines` pre-edit and pre-review checks), focused validation tier rules, and repository Git commit rules (`gh api user` noreply email, no `--amend` without owner permission, no `git push`).
* Assessment boundary: Read-only static credibility assessment of the supplied plan, phase details, research, and referenced `src/api` files. No production or test code was executed or modified during this critique, and hosted GitHub Actions re-execution remains outside local no-push scope.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| `FR-01`, `AC-01`, `C1`–`C8`, `P01-T01` (`screenJumpNav` `data-jump` delegation) | Covered | `src/api/src/zava_forward/api/web/role-screens.js` lines 29-37 is the sole non-conformant `onclick:` in the file; delegating via `"data-jump": id` while keeping `"data-jump-target": id` and `href: \`#${id}\`` reuses the shared `document` click listener at lines 274-280 without violating read-only zero-`<button>` or pinned asset-board listener checks. |
| `FR-02`, `FR-03`, `NFR-01`, `AC-02`–`AC-04`, `C9`, `C10`, `P01-T02` (test imports, re-export, and Node VM delegation test) | Partial | `PC-001`: `P01-T02` prescribes `from tests.test_finance_grants_screens import ...` (or `try/except` dual import) and an unqualified `FinanceScreenWcagTests` re-export, which conflict with `src/api/pyproject.toml` `mypy` (`mypy_path` includes `"tests"`, `explicit_package_bases = true`, `strict = true`, `follow_imports = "normal"`) and `ruff` (`F401`). |
| `NFR-02`, `AC-05`, `C11`, `P02`, `P02-T01` (focused validation, Web Interface Guidelines, artifact preservation, and local commit lifecycle) | Partial | `PC-002`: `P02-T01` omits the post-edit `web-design-guidelines` `file:line` check required by `AC-05`, `P02` sibling discovery omits worktree-local `../core/src:../agents/src:src` from `PYTHONPATH`, `NFR-02` uses an inaccurate `git diff --name-status HEAD` predicate, and `AC-05` does not sequence the single local `git commit` (and `gh api user` noreply email setup) after `rpi-review` writes `.copilot-tracking/reviews/2026-11-14/`. |

## Verdict

* Verdict: Revise
* Rationale: The core JavaScript fix (`P01-T01`) is minimal, evidence-backed, and satisfies every cross-screen WCAG, read-only, and conformance invariant. However, two substantive execution gaps require direct planner revision before implementation: (1) `P01-T02`'s proposed `tests.*` import/re-export pattern conflicts with `src/api/pyproject.toml`'s strict `mypy` and `ruff` configuration (`PC-001`), threatening `AC-02` and `AC-03`; and (2) `P02`/`AC-05`/`NFR-02` leave commit timing versus `rpi-review` artifact creation, `gh api user` email setup, post-edit `web-design-guidelines` verification, and worktree `PYTHONPATH` underspecified or contradictory (`PC-002`). Both findings are direct planner corrections requiring no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `P01-T02` `tests.*` import and bare re-export pattern conflicts with `pyproject.toml` `mypy --strict` and `ruff` (`F401`) rules

* Related IDs: `FR-02`, `FR-03`, `NFR-01`, `AC-02`, `AC-03`, `AC-04`, `C9`, `C10`, `P01`, `P01-T02`
* Evidence: `src/api/pyproject.toml` (lines 30-35 and 53-65), `src/api/tests/test_asset_exec_screen_wcag.py` (line 10), `src/api/tests/test_finance_screen_wcag.py` (line 6), `.copilot-tracking/plans/2026-11-14/issue-225-c2-conformance-fix-plan.md` (`FR-03`, `Locked Test Ownership and Bounds`), and `.copilot-tracking/details/2026-11-14/issue-225-c2-conformance-fix-phase-details.md` (`P01-T02`)
* Concern: `P01-T02` directs `test_finance_screen_wcag.py` to import `from tests.test_finance_grants_screens import ...` (with optional `try/except`) and directs `test_finance_screens_wcag_225.py` to re-export `FinanceScreenWcagTests`. In `src/api/pyproject.toml`, `mypy` runs with `strict = true`, `mypy_path = ["src", "tests", "../core/src", "../core/tests"]`, `explicit_package_bases = true`, `namespace_packages = true`, and `files = ["src", "tests", "checks"]`, and neither `test_finance_grants_screens` nor `test_finance_screen_wcag` is listed in `follow_imports = "skip"` (unlike legacy `tests.test_mvp` overrides). Because `"tests"` in `mypy_path` is a more specific package base than `src/api`, `mypy` registers `tests/test_finance_grants_screens.py` as module `test_finance_grants_screens`; importing `tests.test_finance_grants_screens` causes `mypy` to resolve the same file under two module names (`Source file found twice under different module names`), and a `try/except` dual import also triggers `mypy` `[no-redef]` errors. In addition, `pyproject.toml` enables `ruff` `F` (`F401` unused import) and `mypy` `strict = true` (`--no-implicit-reexport`), so re-exporting `FinanceScreenWcagTests` without explicit `__all__` or `as FinanceScreenWcagTests` fails both linters. Finally, because `test_finance_grants_screens.run()` builds plain `{tag, attrs, kids}` VDOM dictionaries rather than DOM `Element` nodes, `P01-T02` should explicitly require the Node VM click harness to wire `closest("a[data-jump]")`, `getAttribute(...)`, and `document.getElementById(...)` from the rendered finance VDOM trees rather than detached stubs.
* Impact: Implementing `P01-T02` as currently written would break `cd src/api && python3 -m mypy` (`AC-02`) and/or `cd src/api && python3 -m ruff check .` (`AC-03`), or risk a vacuous Node VM click test if stubbed outside rendered VDOM output.
* Smallest useful change: Revise `P01-T02` in the plan and phase details so that (a) static `mypy` analysis imports canonical `mypy_path` module names (`test_finance_grants_screens` / `test_finance_screen_wcag`) without dual `tests.*` static graph paths (for example via `if TYPE_CHECKING:` static imports paired with a typed runtime helper or `sys.path` setup before `importlib.import_module` when `tests/` is absent from `sys.path`, without adding `tests/__init__.py`), (b) `test_finance_screens_wcag_225.py` declares explicit re-export (`__all__ = ["FinanceScreenWcagTests", "FinanceScreenJumpDelegationTests"]` or `as` aliasing, noting that `unittest discover -s tests` intentionally executes the fast re-exported `TestCase` in both modules), and (c) the Node VM behavioral test constructs click targets and `document.getElementById` lookups directly from the rendered `finance-invoices` and `finance-funding` VDOM trees.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T02` specification in `.copilot-tracking/plans/2026-11-14/issue-225-c2-conformance-fix-plan.md` and `.copilot-tracking/details/2026-11-14/issue-225-c2-conformance-fix-phase-details.md` prescribing a `mypy --strict`- and `ruff`-clean (`F401`/`E402`/`I001`) import and explicit re-export strategy plus VDOM-backed Node VM click target resolution.
* Decision route: Direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Unsequenced post-review local commit boundary, omitted `P02-T01` Web Interface Guidelines step, and inaccurate `NFR-02` / `P02` verification commands

* Related IDs: `NFR-02`, `AC-05`, `P02`, `P02-T01`
* Evidence: Caller requirements 1, 2, and 4; `.copilot-tracking/plans/2026-11-14/issue-225-c2-conformance-fix-plan.md` (`NFR-02`, `AC-05`, `P02`, `P02-T01`, `Handoff`); and `.copilot-tracking/details/2026-11-14/issue-225-c2-conformance-fix-phase-details.md` (`P02`, `P02-T01`)
* Concern: Three execution gaps exist in `P02` and `NFR-02`/`AC-05`:
  1. Caller Requirement 2 requires Cycle-2 artifacts under `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/` and Caller Requirement 4 requires a clean local commit with the Copilot trailer and no push, while repository instructions require configuring repository-local `git config --local user.email "{id}+{login}@users.noreply.github.com"` from `gh api user` before committing and forbid `git commit --amend` without owner permission. Because `.copilot-tracking/reviews/2026-11-14/` is created during `rpi-review` after `rpi-implement`, committing prematurely inside `rpi-implement` (`P02`) would either leave the review artifact uncommitted or require a prohibited `--amend` / extra commit.
  2. `AC-05` and `P02` Context require refreshing `web-design-guidelines` and recording a `file:line` review of `role-screens.js`, but `P02-T01`'s task body omits executing and recording that check.
  3. `NFR-02` checks `git diff --name-status HEAD` for `A` on new files (which omits untracked files pre-stage and outputs nothing post-commit), and `P02` runs sibling WCAG test discovery with `PYTHONPATH=../core/tests:../agents/tests` (omitting worktree-local `../core/src:../agents/src:src`, which can import packages from another checkout rather than this worktree).
* Impact: Implementation and closeout could leave `.copilot-tracking/reviews/2026-11-14/` dirty after commit, omit mandatory `web-design-guidelines` `file:line` evidence or privacy-safe `user.email` setup, or validate sibling tests against non-worktree packages.
* Smallest useful change: Update `NFR-02`, `AC-05`, `P02`, `P02-T01`, and `Handoff` so that (a) `P02-T01` explicitly includes refreshing `web-design-guidelines` and recording `file:line` results in `.copilot-tracking/changes/2026-11-14/issue-225-c2-conformance-fix-changes.md`, (b) `P02` sibling WCAG discovery includes worktree-local `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src`, (c) `NFR-02` verifies pre-commit preservation via `git status --short` and post-commit completeness via `git diff --name-status <pre-cycle2-base-sha> HEAD` (confirming zero `M`/`D`/`R` entries on pre-existing `.copilot-tracking/` files), and (d) the single local `git commit` (with `gh api user` noreply `user.email` config, all Cycle-2 code/test/tracking files including `.copilot-tracking/reviews/2026-11-14/`, Copilot trailer, and no `git push`) is explicitly sequenced immediately after `rpi-review` completes.
* Action owner: planning_parent
* Exact resolving evidence: Updated `NFR-02`, `AC-05`, `P02`, `P02-T01`, and `Handoff` sections in `.copilot-tracking/plans/2026-11-14/issue-225-c2-conformance-fix-plan.md` and `.copilot-tracking/details/2026-11-14/issue-225-c2-conformance-fix-phase-details.md` reflecting post-`rpi-review` commit sequencing, `gh api user` email configuration, `web-design-guidelines` `file:line` recording, worktree `PYTHONPATH`, and accurate Git status/diff predicates.
* Decision route: Direct planner correction

## Strengths and Residual Risk

* Surgical root-cause fix (`P01-T01`): Replacing inline `onclick:` in `screenJumpNav` with `"data-jump": id` alongside `"data-jump-target": id` eliminates the sole failing `onclick:` in `src/api/src/zava_forward/api/web/role-screens.js` (lines 29-37) while reusing the existing delegated listener at lines 274-280 (`assetJumpNav`, `residentJumpNav`, `procurementJumpNav`) and preserving read-only zero-`<button>` finance invariants (`C1`–`C8`).
* Thorough contrarian research: `.copilot-tracking/research/2026-11-14/issue-225-c2-conformance-fix-research.md` (`C9`–`C11`) proactively caught the `web/` versus `static/` path history, the missing `tests/test_finance_screens_wcag_225.py` module entrypoint, the `:tests`-less `PYTHONPATH` in the caller's verification command, and `scrollIntoView` compatibility across all specialist screens.
* Explicitly accepted residual risk: Hosted `src-ci.yml` re-verification on PR #1715 cannot run until the owner pushes `feat/ux-225-finance-screens-wcag-1745` (push is explicitly prohibited by caller instructions), and human visual/assistive-technology acceptance remains required before closing Issue #225 (`Refs #225`).

## Questions or Blocking Evidence Gaps

* None. All supplied artifacts and referenced `src/api` files provide complete evidence to resolve `PC-001` and `PC-002` directly in planning without user input.

## Limitations

* This critique performed read-only static inspection of the supplied artifacts and referenced `src/api` source, test, check, and configuration files; runtime `mypy`, `ruff`, `unittest`, and Playwright browser execution belong to the implementation and review stages after plan finalization.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: planning_parent
* Smallest next action: Apply direct planner revisions for `PC-001` and `PC-002` in `.copilot-tracking/plans/2026-11-14/issue-225-c2-conformance-fix-plan.md` and `.copilot-tracking/details/2026-11-14/issue-225-c2-conformance-fix-phase-details.md`, record critique disposition, and finalize the plan without another critique pass so the automatic RPI parent can proceed to `rpi-implement`.
* User response required: No
