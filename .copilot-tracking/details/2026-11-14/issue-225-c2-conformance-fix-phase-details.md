<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #225 Cycle-2 CI Conformance Fix

## Metadata

* Task ID: 2026-11-14-issue-225-c2-conformance-fix
* Task slug: issue-225-c2-conformance-fix
* Related plan: .copilot-tracking/plans/2026-11-14/issue-225-c2-conformance-fix-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/issue-225-c2-conformance-fix-research.md (`C1`–`C11`)

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Delegate finance jump-link clicks and align WCAG regression tests | Completed | P01, P01-T01, P01-T02 |
| P02 | Execute focused-tier validation, Web Interface Guidelines check, and review handoff | Completed | P02, P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Delegate finance jump-link clicks and align WCAG regression tests

### Context

`src-ci.yml` (`src-api`, run `43644186011`) failed `RoleScreenConformance.test_interactive_controls_are_native_and_keyboard_operable` because `screenJumpNav` in `src/api/src/zava_forward/api/web/role-screens.js` attached an inline `onclick:` handler to `<a href="#${id}">` links (`C1`, `C2`). Read-only finance screens forbid `<button>` elements (`C3`) and require `<a href="#<id>" data-jump-target="<id>">` (`C4`, `C5`). Meanwhile, `role-screens.js` already registers a document-level `"click"` listener for `a[data-jump]` (`C6`–`C8`). Direct CLI execution of the caller's `unittest` command also omits `:tests` from `PYTHONPATH` and targets `tests/test_finance_screens_wcag_225.py` (`C10`).

### Intent

Replace the inline `onclick:` in `screenJumpNav` with `"data-jump": id` delegation and provide strictly typed, import-safe `#225` regression tests that verify both VDOM structure and runtime delegated click behavior.

### Boundaries

* Included: `src/api/src/zava_forward/api/web/role-screens.js` (`screenJumpNav` helper), `src/api/tests/test_finance_screen_wcag.py` (import compatibility), and `src/api/tests/test_finance_screens_wcag_225.py` (behavioral delegated-click tests + suite alias).
* Excluded: Editing `test_role_screens_conformance.py`, `finance_screens_browser_check.py`, `style.css`, or the shared `a[data-jump]` listener pinned by `test_asset_exec_screen_wcag.py`.

### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: Remove inline `onclick:` in `screenJumpNav` and add `"data-jump": id`.
* `src/api/tests/test_finance_screen_wcag.py`: Support package-qualified fallback import when `tests/` is not directly on `sys.path`.
* `src/api/tests/test_finance_screens_wcag_225.py`: Add focused delegated-click and conformance-regression tests plus re-export `FinanceScreenWcagTests`.

### Dependencies

* Fetch current Web Interface Guidelines via `web-design-guidelines` skill before modifying `role-screens.js`.

### Validation Expectations

* `RoleScreenConformance` and `FinanceScreenWcagTests` pass alongside the new behavioral delegated-click tests; `mypy` and `ruff` report 0 issues.

### Completion Evidence

* Clean diff in `role-screens.js`, `test_finance_screen_wcag.py`, and `test_finance_screens_wcag_225.py`, verified by unit tests.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Update `screenJumpNav` in `role-screens.js` to use `data-jump` delegation

#### Context

`screenJumpNav` currently attaches `onclick: (event) => { ... }` on `h("a", { href: \`#${id}\`, class: "btn alt", "data-jump-target": id, ... })` (`C1`), failing `test_role_screens_conformance.py` (`C2`). `role-screens.js` already intercepts clicks on `a[data-jump]` via `event.target.closest?.("a[data-jump]")`, calls `event.preventDefault()`, and calls `document.getElementById(link.getAttribute("data-jump"))?.focus()` (`C6`).

#### Intent

Emit `h("a", { href: \`#${id}\`, class: "btn alt", "data-jump": id, "data-jump-target": id }, \`Go to ${text}\`)` inside `screenJumpNav` with no inline `onclick:` property.

#### Boundaries

* Included: `screenJumpNav` definition in `src/api/src/zava_forward/api/web/role-screens.js`.
* Excluded: Modifying `screenJumpTarget`, `screenPanel`, or the shared `document.addEventListener("click", ...)` block.

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: `screenJumpNav` helper.

#### Dependencies

* Load `web-design-guidelines` and fetch `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` before editing.

#### Validation Expectations

* `node --check src/zava_forward/api/web/role-screens.js` passes; `test_role_screens_conformance.py` passes all 12 conformance tests.

#### Completion Evidence

* `screenJumpNav` contains `"data-jump": id` and `"data-jump-target": id` with zero inline `onclick:` handlers.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Harden `test_finance_screen_wcag.py` imports and add `test_finance_screens_wcag_225.py`

#### Context

Running `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_role_screens_conformance.py tests/test_finance_screens_wcag_225.py -v` from `src/api` omits `tests/` from `sys.path`, whereas `mypy` registers `tests/` via `mypy_path = ["src", "tests", ...]` with `explicit_package_bases = true` and `strict = true` (`C9`, `C10`, `PC-001`). Importing `tests.test_finance_grants_screens` statically would trigger `mypy` duplicate-module errors, and a bare unused re-export would fail `ruff` `F401` and `mypy` `--no-implicit-reexport`. Additionally, `test_finance_screen_wcag.py` only inspects VDOM attributes (`C4`) and does not exercise the delegated `document` click handler.

#### Intent

In `test_finance_screen_wcag.py` and `test_finance_screens_wcag_225.py`, keep canonical `mypy_path` module names under `if TYPE_CHECKING:` for static typing while ensuring `str(Path(__file__).resolve().parent)` is present in `sys.path` before loading sibling test modules via `importlib.import_module` at runtime (without creating `tests/__init__.py` or triggering `ruff` `E402`/`F401`). Declare explicit `__all__ = ["FinanceScreenWcagTests", "FinanceScreenJumpDelegationTests"]` in `src/api/tests/test_finance_screens_wcag_225.py` (noting `unittest discover -s tests` intentionally runs the fast re-exported `TestCase` in both modules), and add `FinanceScreenJumpDelegationTests` (2 methods) verifying:
1. Rendered finance jump links in both `finance-invoices` and `finance-funding` carry matching `data-jump` and `data-jump-target` attributes and no inline `onclick` attribute.
2. Executing `role-screens.js` in Node VM with `document.addEventListener("click", ...)` and dispatching click events whose `target.closest("a[data-jump]")`, `link.getAttribute(...)`, and `document.getElementById(...)` resolve directly against the rendered `finance-invoices` and `finance-funding` VDOM trees calls `event.preventDefault()`, focuses every expected target ID, and does not throw when a target ID is absent.

#### Boundaries

* Included: `src/api/tests/test_finance_screen_wcag.py` and `src/api/tests/test_finance_screens_wcag_225.py`.
* Excluded: Adding `tests/__init__.py` or removing/weakening any assertion in `test_finance_screen_wcag.py`, `test_finance_grants_screens.py`, or `test_finance_grants_screen_wcag.py`.

#### Likely Targets

* `src/api/tests/test_finance_screen_wcag.py`: `TYPE_CHECKING` + runtime `sys.path` / `importlib.import_module` sibling loader.
* `src/api/tests/test_finance_screens_wcag_225.py`: Explicit `__all__` re-export of `FinanceScreenWcagTests` and VDOM-backed `FinanceScreenJumpDelegationTests`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Both `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src:tests python3 -m unittest discover -s tests -p "test_finance*.py" -v` and `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_role_screens_conformance.py tests/test_finance_screens_wcag_225.py -v` pass; `mypy` and `ruff` report 0 errors.

#### Completion Evidence

* Passing verbose test output from both invocation forms plus clean `mypy` and `ruff` checks.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Execute focused-tier validation, Web Interface Guidelines check, and review handoff

### Context

Under AMA repository validation rules, this Cycle-2 fix falls in the focused validation tier (web JS helper + unit tests only; no workflow, gate-tool, Dockerfile, SQL, dependency, or security-control edits). Web Development Guidance additionally requires refreshing `web-design-guidelines` and reviewing changed web files with `file:line` findings. Per `PC-002`, the single local `git commit` (using privacy-safe `gh api user` noreply `user.email` and Copilot trailer, without `git push`) must execute immediately *after* `rpi-review` writes `.copilot-tracking/reviews/2026-11-14/issue-225-c2-conformance-fix-review.md` and finalizes session state so no `--amend` or leftover untracked review artifact occurs.

### Intent

Run every required static, lint, syntax, unit (with worktree-local `PYTHONPATH`), and Web Interface Guidelines check, record exact command outputs and `file:line` review results in `.copilot-tracking/changes/2026-11-14/issue-225-c2-conformance-fix-changes.md`, and verify pre-existing `.copilot-tracking/` files remain untouched (`git status --short` against base `75f4cdfff`) before handing off to `rpi-review` and post-review local commit.

### Boundaries

* Included: Validation commands in `src/api`, refreshed Web Interface Guidelines `file:line` check on `role-screens.js`, changes-artifact recording, and `git status --short` preservation verification.
* Excluded: Premature `git commit` before `rpi-review` completes, and any `git push`.

### Likely Targets

* `.copilot-tracking/changes/2026-11-14/issue-225-c2-conformance-fix-changes.md`: Implementation, guideline review, and validation evidence log.

### Dependencies

* P01 (`P01-T01`, `P01-T02`).

### Validation Expectations

* `cd src/api && python3 -m mypy` -> 0 errors.
* `cd src/api && python3 -m ruff check . && python3 -m ruff format --check .` -> 0 errors.
* `cd src/api && PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_role_screens_conformance.py tests/test_finance_screens_wcag_225.py -v` -> OK.
* Sibling role-screen suites (`test_finance_screen_wcag.py`, `test_finance_grants_screens.py`, `test_finance_grants_screen_wcag.py`, `test_procurement_screen_wcag.py`, `test_asset_exec_screen_wcag.py`, `test_accessibility_baseline.py`) under worktree-local `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src:tests python3 -m unittest ... -v` -> OK.
* `node --check src/api/src/zava_forward/api/web/role-screens.js` -> exit 0.
* Refreshed `web-design-guidelines` rules checked against `src/api/src/zava_forward/api/web/role-screens.js` with `file:line` output recorded.
* `finance_screens_browser_check.py` executed locally with worktree `PYTHONPATH` if Playwright Chromium is installed, or explicitly disclosed if Chromium binary is absent.
* `git status --short` confirms zero modified or deleted pre-existing `.copilot-tracking/` files (and post-review commit verifies `git diff --name-status 75f4cdfff HEAD`).

### Completion Evidence

* Recorded exit-0 command outputs and Web Interface Guidelines `file:line` results in `.copilot-tracking/changes/2026-11-14/issue-225-c2-conformance-fix-changes.md` and reconciled plan task checkboxes.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run `mypy`, `ruff`, `node --check`, targeted and worktree-local sibling unittest suites, and Web Interface Guidelines review

#### Context

All three caller-mandated checks, worktree-local cross-screen WCAG unit checks, refreshed Web Interface Guidelines `file:line` review, and pre-commit `git status --short` artifact-preservation verification must pass together before `rpi-review`.

#### Intent

Execute the validation suite and Web Interface Guidelines check, verify zero unintended changes to pre-existing `.copilot-tracking/` files, and reconcile plan/detail completion state for `rpi-review` (followed post-review by `gh api user` noreply email setup and a single local commit without push).

#### Boundaries

* Included: Read-only validation runs, Web Interface Guidelines refresh + `file:line` review, and `.copilot-tracking/changes/2026-11-14/issue-225-c2-conformance-fix-changes.md` updates.
* Excluded: Full external `rpi-checks.py --all` release gate (not required for focused-tier UI slice fix per issue #1294 / D4) and premature `git commit` prior to `rpi-review`.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-14/issue-225-c2-conformance-fix-changes.md`: Validation results, Web Interface Guidelines `file:line` report, and file inventory.

#### Dependencies

* P01-T01 and P01-T02 completed.

#### Validation Expectations

* Every command and check listed in P02 Validation Expectations passes cleanly.

#### Completion Evidence

* Complete changes record ready for `rpi-review` assessment and subsequent single clean local commit.

#### Unresolved Items

* None.
