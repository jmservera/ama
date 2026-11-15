<!-- markdownlint-disable-file -->
# RPI Plan: Issue #225 Cycle-2 CI Conformance Fix

## Task Metadata

* Task ID: 2026-11-14-issue-225-c2-conformance-fix
* Task slug: issue-225-c2-conformance-fix
* Planning status: Ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/issue-225-c2-conformance-fix-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/issue-225-c2-conformance-fix-plan-critique.md

## Executive Summary

This Cycle-2 plan resolves the single `src-ci.yml` (`src-api`) failure on PR #1715 (`feat/ux-225-finance-screens-wcag-1745` targeting `feat/demo-233-same-home-tensions-0825`) for Issue #225. In Cycle 1, `screenJumpNav` in `src/api/src/zava_forward/api/web/role-screens.js` attached an inline `onclick:` handler to `<a href="#${id}">` jump links, tripping `RoleScreenConformance.test_interactive_controls_are_native_and_keyboard_operable`, which permits inline `onclick:` only on `h("button"` or `h("a", { href: "#"` controls.

Rather than adding `<button>` controls (forbidden on read-only finance screens) or weakening the cross-screen conformance test, `screenJumpNav` will delegate click focus through the existing document-level `a[data-jump]` handler in `role-screens.js` while retaining `href="#${id}"` and `data-jump-target="${id}"`. In parallel, the plan hardens test imports for direct `python3 -m unittest tests/...` runs without `:tests` on `PYTHONPATH` and adds behavioral delegated-click regression coverage in `src/api/tests/test_finance_screens_wcag_225.py`.

### User Decisions and Requirements Highlights

* Preserve every existing `.copilot-tracking/` artifact on `feat/ux-225-finance-screens-wcag-1745` and add Cycle-2 RPI artifacts under `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/`.
* Fix `role-screens.js` and finance WCAG test modules so `mypy`, `ruff check .`, `ruff format --check .`, and `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_role_screens_conformance.py tests/test_finance_screens_wcag_225.py -v` all pass cleanly.
* Commit locally on `feat/ux-225-finance-screens-wcag-1745` with a privacy-safe GitHub noreply email and the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer, and do not push.

### What You May Not Know

* The repository's migrated web asset directory is `src/api/src/zava_forward/api/web/role-screens.js` (not `static/role-screens.js`), and `role-screens.js` already provides a shared `document.addEventListener("click", ...)` handler for `a[data-jump]` used by `assetJumpNav`, `residentJumpNav`, and `procurementJumpNav` and pinned verbatim by `src/api/tests/test_asset_exec_screen_wcag.py`.
* Direct CLI execution of `python3 -m unittest tests/...` without `:tests` in `PYTHONPATH` omits `src/api/tests` from `sys.path`, whereas `mypy` registers `tests/` via `mypy_path` (`explicit_package_bases = true`); therefore test modules must keep canonical `mypy_path` static imports (`if TYPE_CHECKING:`) paired with runtime `sys.path` + `importlib.import_module` resolution rather than `tests.*` dual module names.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (research, plan, implement, review) for the Cycle-2 CI fix on Issue #225 (PR #1715) in `/home/azureuser/source/ama-demo-wt/feat-225-finance-screens-wcag-1745` on branch `feat/ux-225-finance-screens-wcag-1745` targeting `feat/demo-233-same-home-tensions-0825` (caller prompt).
* Preserve all existing `.copilot-tracking/` artifacts on the branch and record Cycle-2 artifacts under `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/` documenting root cause and fix (caller prompt).
* Resolve the `test_interactive_controls_are_native_and_keyboard_operable` failure caused by `screenJumpNav` inline `onclick:` in `src/api/src/zava_forward/api/web/role-screens.js` without breaking finance WCAG tests or read-only role-screen constraints (caller prompt; `.copilot-tracking/research/2026-11-14/issue-225-c2-conformance-fix-research.md` `C1`–`C8`).
* Ensure `cd src/api && python3 -m mypy`, `cd src/api && python3 -m ruff check . && python3 -m ruff format --check .`, and `cd src/api && PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_role_screens_conformance.py tests/test_finance_screens_wcag_225.py -v` all pass cleanly (caller prompt; `C9`, `C10`).
* Apply AMA Web Development Guidance: preserve Fluent 2 tokens, WCAG 2.2 AA baseline, plain British English content rules, native semantics, non-colour status prefixes, and read-only boundaries; load and apply `web-design-guidelines` before web edits and refresh before review (`.github/copilot-instructions.md`).
* Commit all Cycle-2 changes cleanly on `feat/ux-225-finance-screens-wcag-1745` with privacy-safe repository-local Git email and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and do not push (caller prompt; `.github/copilot-instructions.md`).

## Goals

* Eliminate the non-conformant inline `onclick:` handler on `screenJumpNav` anchors in `src/api/src/zava_forward/api/web/role-screens.js` while preserving SPA hash-route protection and programmatic section focus.
* Guarantee both `unittest discover -s tests` (CI) and direct `python3 -m unittest tests/test_role_screens_conformance.py tests/test_finance_screens_wcag_225.py -v` (caller verification) succeed with behavioral delegated-click test coverage, strict `mypy` typing, and clean `ruff` formatting/linting.
* Produce complete, reconcilable Cycle-2 RPI artifacts and a clean local commit on `feat/ux-225-finance-screens-wcag-1745` with existing `.copilot-tracking/` history preserved.

## Scope and Non-Goals

### In Scope

* Updating `screenJumpNav` in `src/api/src/zava_forward/api/web/role-screens.js` to emit `"data-jump": id` alongside `"data-jump-target": id` and omit inline `onclick:`.
* Making `src/api/tests/test_finance_screen_wcag.py` import-safe when invoked via either `unittest discover -s tests` or `python3 -m unittest tests/...` without `:tests` in `PYTHONPATH`.
* Creating `src/api/tests/test_finance_screens_wcag_225.py` to expose the `#225` WCAG suite at the caller-requested module path and add behavioral regression tests for delegated `a[data-jump]` click handling (`preventDefault()`, `.focus()`, missing-target safety, and absence of inline `onclick`).
* Creating Cycle-2 RPI artifacts under `.copilot-tracking/{research,plans,details,reviews/plans,changes,reviews,rpi-sessions}/2026-11-14/` and committing locally without pushing.

### Non-Goals

* Modifying `src/api/tests/test_role_screens_conformance.py`, `src/api/checks/finance_screens_browser_check.py`, CSS tokens, or the shared `a[data-jump]` listener lines pinned by `test_asset_exec_screen_wcag.py`.
* Adding `<button>` elements to read-only finance specialist screens.
* Pushing to `origin` or altering PR #1715 metadata on GitHub.

## Functional Requirements

* `FR-01`: `screenJumpNav` in `src/api/src/zava_forward/api/web/role-screens.js` renders `<nav class="row" aria-label="...">` containing native `<a href="#<id>" class="btn alt" data-jump="<id>" data-jump-target="<id>">Go to <text></a>` links with no inline `onclick` property.
  * Observable acceptance criteria: `RoleScreenConformance.test_interactive_controls_are_native_and_keyboard_operable` and `FinanceScreenWcagTests.test_jump_links_are_native_anchors_with_matching_targets` both pass.
* `FR-02`: Clicking a finance section jump link activates the shared `document` `"click"` listener for `a[data-jump]`, prevents default hash navigation (`event.preventDefault()`), moves focus to the matching `tabindex="-1"` section container (`#finance-queue`, `#finance-lines`, `#finance-economics`, `#grant-pack`, `#funding-summary`), and tolerates missing DOM targets without throwing.
  * Observable acceptance criteria: Behavioral Node VM test in `src/api/tests/test_finance_screens_wcag_225.py` dispatches clicks on rendered finance jump links and verifies `preventDefault()` count, focused target IDs, and no-throw missing-target handling.
* `FR-03`: Test modules `src/api/tests/test_finance_screen_wcag.py` and `src/api/tests/test_finance_screens_wcag_225.py` execute cleanly under both `python3 -m unittest discover -s tests -v` and `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_role_screens_conformance.py tests/test_finance_screens_wcag_225.py -v`.
  * Observable acceptance criteria: Both commands exit 0 and execute all conformance and `#225` WCAG tests.

## Non-Functional Requirements

* `NFR-01`: Static type and lint compliance across `src/api`.
  * Objective threshold or evaluation condition: 0 `mypy` strict errors, 0 `ruff check .` diagnostics, and 0 `ruff format --check .` diffs; valid JS syntax via `node --check`.
  * Operating condition or verification approach, if needed: Run from `src/api` using the installed Python 3.12 toolchain and Node.js.
  * Observable acceptance criteria: `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `node --check src/zava_forward/api/web/role-screens.js` all exit 0.
* `NFR-02`: Preservation of WCAG 2.2 AA, read-only specialist boundaries, and prior tracking evidence.
  * Objective threshold or evaluation condition: Zero `<button>`/form controls inside finance `.screen-evidence`, intact `a[data-jump]` listener lines for `test_asset_exec_screen_wcag.py`, zero findings on changed lines against fetched Web Interface Guidelines, and zero deletions/modifications of pre-existing `.copilot-tracking/` files.
  * Operating condition or verification approach, if needed: Cross-screen WCAG unit suite (`test_finance_grants_screens.py`, `test_finance_grants_screen_wcag.py`, `test_procurement_screen_wcag.py`, `test_asset_exec_screen_wcag.py`, `test_accessibility_baseline.py`) executed with worktree-local `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src:tests`, Web Interface Guidelines `file:line` review, pre-commit `git status --short` verification, and post-commit `git diff --name-status 75f4cdfff HEAD` verification.
  * Observable acceptance criteria: All sibling WCAG suites pass (exit 0), pre-commit `git status --short` and post-commit `git diff --name-status 75f4cdfff HEAD` show zero `M`/`D`/`R` entries on pre-existing `.copilot-tracking/` files and include only `role-screens.js`, `test_finance_screen_wcag.py`, `test_finance_screens_wcag_225.py`, and new Cycle-2 `.copilot-tracking/**/2026-11-14/issue-225-c2-conformance-fix-*` artifacts.

## Acceptance Criteria

* `AC-01`: `src/api/src/zava_forward/api/web/role-screens.js` contains no non-conformant `onclick:` in `screenJumpNav` and wires `"data-jump": id` alongside `"data-jump-target": id`.
* `AC-02`: `cd src/api && python3 -m mypy` exits 0 with 0 errors.
* `AC-03`: `cd src/api && python3 -m ruff check . && python3 -m ruff format --check .` exits 0.
* `AC-04`: `cd src/api && PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_role_screens_conformance.py tests/test_finance_screens_wcag_225.py -v` exits 0, covering semantic jump-link focus delegation from rendered VDOM trees and regression checks.
* `AC-05`: Existing sibling finance, procurement, asset-exec, and accessibility baseline unit tests pass with worktree-local `PYTHONPATH`, Web Interface Guidelines `file:line` review is recorded in the changes and review artifacts, all prior `.copilot-tracking/` files remain untouched (`75f4cdfff` baseline), and after `rpi-review` writes `.copilot-tracking/reviews/2026-11-14/issue-225-c2-conformance-fix-review.md` and reconciles session state, a single local commit is created on `feat/ux-225-finance-screens-wcag-1745` using privacy-safe `gh api user` noreply `user.email` and the Copilot trailer without pushing.

### Locked Test Ownership and Bounds

* Canonical production target: `src/api/src/zava_forward/api/web/role-screens.js` (generated targets: `none`).
* Test ownership: `src/api/tests/test_finance_screen_wcag.py` (existing import compatibility update) and `src/api/tests/test_finance_screens_wcag_225.py` (new Cycle-2 module).
* Exact test removals: `none`.
* Maximum test additions: 1 new test module (`src/api/tests/test_finance_screens_wcag_225.py`) containing at most 3 focused test methods (semantic delegated-click focus/preventDefault/missing-target behavior and regression guard against inline `onclick` on finance jump links, plus re-export of `FinanceScreenWcagTests`).

## Implementation Context Record

| Context item | Current artifact or record |
| --- | --- |
| Plan | .copilot-tracking/plans/2026-11-14/issue-225-c2-conformance-fix-plan.md |
| Phase details | .copilot-tracking/details/2026-11-14/issue-225-c2-conformance-fix-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-11-14/issue-225-c2-conformance-fix-plan-critique.md with Revise disposition (`PC-001`, `PC-002` directly resolved and closed) |
| Relevant research | .copilot-tracking/research/2026-11-14/issue-225-c2-conformance-fix-research.md |
| Changes-record role | .copilot-tracking/changes/2026-11-14/issue-225-c2-conformance-fix-changes.md is created by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for implementation |
| Continuation context | Confirmed automatic RPI Agent parent continues automatically to `rpi-implement` |

## Sources

* `.copilot-tracking/research/2026-11-14/issue-225-c2-conformance-fix-research.md`: Primary Cycle-2 research synthesis (`C1`–`C11`) proving root cause, cross-suite constraints, and CLI `PYTHONPATH` import behavior.
* `src/api/src/zava_forward/api/web/role-screens.js`: Defines `screenJumpTarget`, `screenJumpNav`, and the shared `a[data-jump]` document click listener.
* `src/api/tests/test_role_screens_conformance.py`: Static UX conformance suite that rejected inline `onclick:` on dynamic-`href` anchors.
* `src/api/tests/test_finance_screen_wcag.py` and `src/api/tests/test_finance_grants_screens.py`: Existing Issue #225 and finance screen unit tests.
* `src/api/checks/finance_screens_browser_check.py`: Read-only finance browser check prohibiting `<button>` inside `.screen-evidence`.
* `docs/reference/research/ux/wcag-conformance-baseline.md`, `design-system.md`, and `content-standard.md`: UX, WCAG 2.2 AA, and plain British English rules.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Delegate finance jump-link clicks and align WCAG regression tests

* Intent: Remove the non-conformant inline `onclick:` from `screenJumpNav` by wiring `data-jump` delegation, make `#225` test imports resilient without `:tests` in `PYTHONPATH`, and add focused Cycle-2 behavioral tests at `tests/test_finance_screens_wcag_225.py`.
* Dependencies: Web Interface Guidelines fetched via `web-design-guidelines` skill prior to editing `role-screens.js`.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Update `screenJumpNav` in `role-screens.js` to use `data-jump` delegation

* Requirement and evidence: `FR-01`, `FR-02`, `NFR-02`; research `C1`–`C8`.
* Expected result: `screenJumpNav` renders `h("a", { href: \`#${id}\`, class: "btn alt", "data-jump": id, "data-jump-target": id }, \`Go to ${text}\`)` with no inline `onclick:`, leaving the shared `a[data-jump]` listener untouched.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/issue-225-c2-conformance-fix-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Harden `test_finance_screen_wcag.py` imports and add `test_finance_screens_wcag_225.py`

* Requirement and evidence: `FR-02`, `FR-03`, `NFR-01`; research `C4`, `C9`, `C10`; critique `PC-001`.
* Expected result: `test_finance_screen_wcag.py` and `test_finance_screens_wcag_225.py` keep canonical `mypy_path` static imports (`if TYPE_CHECKING:`) paired with runtime `sys.path` + `importlib.import_module` resolution (avoiding `tests.*` duplicate-module `mypy` errors and `ruff` `F401`/`E402`), explicitly export `__all__ = ["FinanceScreenWcagTests", "FinanceScreenJumpDelegationTests"]`, and test delegated `a[data-jump]` click focus against targets wired from the rendered finance VDOM trees.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/issue-225-c2-conformance-fix-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Execute focused-tier validation, Web Interface Guidelines check, and review handoff

* Intent: Verify static types, formatting/linting, JS syntax, targeted and worktree-local cross-screen unit suites, Web Interface Guidelines `file:line` compliance, and pre-commit `git status --short` artifact preservation prior to `rpi-review` (with the single local `git commit` sequenced after `rpi-review` writes the review artifact).
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run `mypy`, `ruff`, `node --check`, targeted and worktree-local sibling unittest suites, and Web Interface Guidelines review

* Requirement and evidence: `AC-01`–`AC-05`, `NFR-01`, `NFR-02`; research `C2`–`C11`; critique `PC-002`.
* Expected result: Zero errors across `mypy`, `ruff check .`, `ruff format --check .`, `node --check`, caller's exact `unittest` command, and worktree-local `PYTHONPATH` sibling role-screen WCAG tests; refreshed Web Interface Guidelines `file:line` findings and pre-commit `git status --short` check recorded in `.copilot-tracking/changes/2026-11-14/issue-225-c2-conformance-fix-changes.md`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/issue-225-c2-conformance-fix-phase-details.md

## Dependencies

* `web-design-guidelines` live rule fetch (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`): Required by AMA Web Development Guidance before editing `role-screens.js` and refreshed before review.
* Installed editable distributions (`zava-forward-core`, `zava-forward-agents`, `zava-forward-api`) and Node.js runtime: Required by `mypy`, `ruff`, and Node VM screen unit tests.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
| --- | --- | --- |
| `PC-001` [High] (`P01-T02` `tests.*` import & bare re-export under `mypy --strict` / `ruff`) | Resolved | Updated Executive Summary, `P01-T02`, and Phase Details to use `if TYPE_CHECKING:` canonical `mypy_path` imports paired with runtime `sys.path` + `importlib.import_module`, explicit `__all__` export, and rendered-VDOM click target wiring in Node VM. |
| `PC-002` [Medium] (`P02` Web Interface Guidelines step, worktree `PYTHONPATH`, Git status/diff predicate, and post-review commit sequencing) | Resolved | Updated `NFR-02`, `AC-05`, `P02`, `P02-T01`, `Handoff`, and Phase Details to include post-edit `web-design-guidelines` `file:line` recording, worktree-local `PYTHONPATH`, `git status --short` + `git diff --name-status 75f4cdfff HEAD` verification, and single local commit with `gh api user` noreply email sequenced after `rpi-review` completes. |
| Residual risk (hosted CI & human UX/AT sign-off) | Accepted with risk | Hosted `src-ci.yml` runs only after owner-approved push (excluded here), and Issue #225 remains `Refs #225` pending human visual/AT review. |

## Follow-Up Items

* Standardise `data-jump` and `data-jump-target` attribute naming across specialist screen helpers: Outside immediate Cycle-2 CI fix scope because legacy finance tests filter on `data-jump-target` while shared delegation matches `a[data-jump]`; keep both attributes on `screenJumpNav` for zero-regression minimal scope (owner: future UX cleanup slice).
* Hosted `src-ci.yml` execution and human visual/assistive-technology acceptance for Issue #225: Requires owner push to PR #1715 and human review per `docs/reference/research/ux/wcag-conformance-baseline.md` (`Refs #225`).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/issue-225-c2-conformance-fix-changes.md
* Ready phase or task: P01 (`P01-T01`, `P01-T02`), followed by P02 (`P02-T01`), then `rpi-review` (`.copilot-tracking/reviews/2026-11-14/issue-225-c2-conformance-fix-review.md`) and single post-review local commit on `feat/ux-225-finance-screens-wcag-1745`
* Remaining provisional question or blocker: None
