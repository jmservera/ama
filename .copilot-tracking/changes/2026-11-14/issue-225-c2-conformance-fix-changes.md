<!-- markdownlint-disable-file -->
# RPI Changes: Issue #225 Cycle-2 CI Conformance Fix

## Metadata

* Task ID: 2026-11-14-issue-225-c2-conformance-fix
* Related plan: .copilot-tracking/plans/2026-11-14/issue-225-c2-conformance-fix-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/issue-225-c2-conformance-fix-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`
* All remaining active-plan markers: None
* Status basis: Completed `P01` production and test edits and verified all `P02` static, runtime, browser, Web Interface Guidelines, and Git preservation checks.

## Execution Summary

Delivered the full Cycle-2 CI conformance fix for Issue #225 (PR #1715). Removed the non-conformant inline `onclick:` handler from `screenJumpNav` in `src/api/src/zava_forward/api/web/role-screens.js` by wiring `"data-jump": id` alongside `"data-jump-target": id`, reusing the file's shared `a[data-jump]` document click listener. Hardened `src/api/tests/test_finance_screen_wcag.py` and created `src/api/tests/test_finance_screens_wcag_225.py` with `mypy_path`-safe `TYPE_CHECKING` imports plus runtime `sys.path`/`importlib` loading, explicit `__all__` re-exports, and VDOM-backed delegated-click behavioral tests.

## Completed Work

### Delegated finance jump navigation (`P01-T01`)

* Updated `screenJumpNav` in `src/api/src/zava_forward/api/web/role-screens.js` to emit `h("a", { href: \`#${id}\`, class: "btn alt", "data-jump": id, "data-jump-target": id }, \`Go to ${text}\`)` with zero inline `onclick:` handlers.
* Preserved `<a href="#<id>" data-jump-target="<id>">` semantics for read-only finance screens (`finance_screens_browser_check.py`, `test_finance_grants_screens.py`, `test_finance_screen_wcag.py`) and left the shared `document.addEventListener("click", ...)` block intact (`test_asset_exec_screen_wcag.py`).

### Strict-type-safe `#225` test imports and behavioral delegation coverage (`P01-T02`)

* Updated `src/api/tests/test_finance_screen_wcag.py` with `if TYPE_CHECKING:` canonical `mypy_path` imports and runtime `sys.path` + `importlib.import_module("test_finance_grants_screens")` resolution so both `unittest discover -s tests` and `:tests`-less `PYTHONPATH` CLI runs succeed without `mypy` duplicate-module errors or `ruff` lint violations.
* Created `src/api/tests/test_finance_screens_wcag_225.py` declaring `__all__ = ["FinanceScreenJumpDelegationTests", "FinanceScreenWcagTests"]` and adding two focused tests:
  * `test_jump_links_delegate_via_data_jump_without_inline_onclick`: verifies every rendered jump link in `finance-invoices` and `finance-funding` sets `data-jump == data-jump-target` and omits inline `onclick`.
  * `test_delegated_click_prevents_default_focuses_targets_and_tolerates_missing_node`: executes `role-screens.js` in Node VM, builds target maps directly from rendered `finance-invoices` and `finance-funding` `div[id][tabindex="-1"]` VDOM nodes, dispatches clicks against rendered `a[data-jump]` VDOM links, and verifies `preventDefault()` count (`7`), ordered focus targets (`finance-queue`, `finance-lines`, `finance-economics`, `grant-pack`, `funding-summary`, `finance-economics`), non-jump ignore behavior, and no-throw missing-target tolerance.

### Focused-tier validation, Web Interface Guidelines audit, and Git preservation (`P02-T01`)

* Verified `mypy`, `ruff check .`, `ruff format --check .`, `node --check`, caller's exact `unittest` command (19 tests), sibling WCAG discovery, all 301 screen tests, all 50 finance tests, and real Chromium `python3 -m checks.finance_screens_browser_check`.
* Refreshed Web Interface Guidelines from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` and audited changed web files in terse `file:line` format:
  * `## src/api/src/zava_forward/api/web/role-screens.js`
  * `✓ pass` (changed `screenJumpNav` uses native `<a href="#...">` navigation links, `<nav aria-label>`, delegated click focus without inline `onclick`, visible `:focus-visible` ring from `style.css`, and descriptive `"Go to ..."` labels; pre-existing layout has static `.top` header so non-sticky jump targets are never obscured).
* Verified `git status --short` shows zero modified or deleted pre-existing `.copilot-tracking/` files relative to `75f4cdfff` and removed temporary test directories created during interrupted full-suite probes.

## Implementation-Time Plan and Detail Updates

None.

## Validation Record

| Check | Scope | Status | Evidence or reason |
| --- | --- | --- | --- |
| `python3 -m mypy` | `src/api` (284 files) | Passed | `Success: no issues found in 284 source files` (exit 0) |
| `python3 -m ruff check .` | `src/api` | Passed | `All checks passed!` (exit 0) |
| `python3 -m ruff format --check .` | `src/api` (200 files) | Passed | `200 files already formatted` (exit 0) |
| `node --check src/zava_forward/api/web/role-screens.js` | `role-screens.js` | Passed | Exit 0 |
| `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_role_screens_conformance.py tests/test_finance_screens_wcag_225.py -v` | Conformance + `#225` WCAG | Passed | `Ran 19 tests in 0.839s — OK` (`RoleScreenConformance`: 12, `FinanceScreenWcagTests`: 5, `FinanceScreenJumpDelegationTests`: 2) |
| `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest discover -s tests -p "test_*screen*.py" -v` | All role-screen & WCAG unit suites | Passed | `Ran 301 tests in 20.112s — OK` |
| `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest discover -s tests -p "test_*finance*.py" -v` | All finance unit suites | Passed | `Ran 50 tests in 9.227s — OK` |
| `PYTHONPATH=.:../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m checks.finance_screens_browser_check` | Real Chromium browser check (`pam`, `support`, `grants`, `grants` with draft) | Passed (partial axe) | Exit 0: 320px/1280px reflow, Tab table reachability, read-only zero write controls, zero JS errors; `ZF_AXE_JS` unset locally (axe scan runs in hosted `src-ci.yml`) |
| Web Interface Guidelines (`web-design-guidelines` refreshed) | `src/api/src/zava_forward/api/web/role-screens.js` | Passed | `✓ pass` on changed web file (`file:line` review above) |
| Pre-commit `git status --short` preservation check | Worktree vs `75f4cdfff` | Passed | Zero modified/deleted pre-existing `.copilot-tracking/` artifacts |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01` checked; Phase Index set to `Completed`)
* Completed-work evidence and handoff prose: Reconciled
* Validation, blockers, remaining work, and follow-up items: Reconciled
* Review readiness: Ready for `rpi-review`

## Blockers

* None

## Remaining Work

* None within `rpi-implement` scope (single local `git commit` follows `rpi-review` artifact persistence per `PC-002` and `AC-05`).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/issue-225-c2-conformance-fix-plan.md, `## Follow-Up Items`
* Standardise `data-jump` and `data-jump-target` attribute naming across specialist screen helpers in a later cleanup slice.
* Run hosted `src-ci.yml` after owner push and collect human visual/assistive-technology acceptance evidence (`Refs #225`).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`, `P02`); completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`; remaining: none
* Validation coverage: `mypy` (284 files), `ruff check`, `ruff format --check`, `node --check`, caller `unittest` command (19 tests), screen suites (301 tests), finance suites (50 tests), Playwright `finance_screens_browser_check` (axe skipped locally; `ZF_AXE_JS` unset), refreshed Web Interface Guidelines (`✓ pass`), and `git status --short` preservation check
* Blockers: None
* Current plan and detail updates: Checked all `P01`/`P02` markers and marked Phase Index `Completed`
* Planning and critique state: Ready (`PC-001` and `PC-002` resolved; critique not repeated)
* Follow-up items: Attribute naming cleanup and hosted CI + human UX/AT sign-off
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent transitions directly to `Review`
