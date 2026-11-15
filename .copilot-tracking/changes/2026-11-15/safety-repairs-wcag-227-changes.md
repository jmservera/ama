<!-- markdownlint-disable-file -->
# RPI Changes: Issue #227 Building Safety Lead and Repairs Hazard Screens WCAG 2.2

## Metadata

* Task ID: 2026-11-15-safety-repairs-wcag-227
* Related plan: .copilot-tracking/plans/2026-11-15/safety-repairs-wcag-227-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/safety-repairs-wcag-227-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`, `P01-T01`, `P01-T02`, `P01-T03`, `P02`, `P02-T01`, `P02-T02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P01-T03`, `P02`, `P02-T01`, `P02-T02`
* All remaining active-plan markers: None
* Status basis: All planned source, CSS, unit/conformance test, and #227 browser harness updates completed and verified under Focused-tier validation plus real Chromium + pinned axe-core 4.10.3 WCAG 2.2 AA verification and refreshed Web Interface Guidelines `file:line` review.

## Execution Summary

Delivered WCAG 2.2 AA keyboard jump navigation, `#/role/building_safety_lead` and `#/role/repairs` route aliases, word-first prototype-safe textual state labels and non-colour cue guidance, non-colour link/badge CSS affordances with `>= 24px` target height and heading `scroll-margin-top`, tightened conformance and keyboard unit tests, and verified zero violations across static analysis, unit tests, Chromium + pinned axe-core 4.10.3 (`safety_screens_browser_check.py`), and refreshed Web Interface Guidelines.

## Completed Work

### Delegated keyboard jump navigation, cross-home landmarks, and `#/role/...` aliases

* Related phase or task: `P01-T01`
* Files: `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/app.js`
* What changed and why: Replaced inline `onclick` / `href="#"` in `hazardJump` with real `#hazard-${key}-heading` links (`data-jump` and `data-jump-target`) paired with `screenPanel(title, { anchor: "hazard-" + key }, ...)` `<section id>` + `<h2 id tabindex="-1">` landmarks across both per-home (`hazardScreen`) and cross-home (`hazardQueue.summary`) views; extended the shared `a[data-jump]` click delegation with `?.focus?.()` and `?.scrollIntoView?.({ block: "start" })` while keeping the exact `event.preventDefault();\n    document.getElementById` substring; removed the duplicate `overview` argument inside unselected `selected` in `roleScreensView` so VDOM trees match real DOM without duplicating `#hazard-page-summary`; added `isRoleScreensDestination` in `app.js` and `ROLE_HASH_SCREENS` in `roleScreensView` so `#/role/building_safety_lead` -> `safety-lead` and `#/role/repairs` -> `hazard-triage` load `/role-screens.js`, preserve `?case=`/`?page=`, and block unauthorized roles with `"Screen unavailable"`.
* Completion evidence: `node --check` exit `0`; `test_safety_screen_wcag_keyboard.py`, `test_role_screens.py`, `test_asset_exec_screen_wcag.py`, `test_workspace_scripts.py`, and `safety_screens_browser_check.py` all pass.
* Validation: Passed

### Word-first, `Object.hasOwn`-safe textual state labels and non-colour cue prose

* Related phase or task: `P01-T02`
* Files: `src/api/src/zava_forward/api/web/role-screens.js`
* What changed and why: Standardized `hazardStep`, `hazardSafetyClock`, `hazardFollowUp`, `hazardEscalationState` (covering all `workflows.py:hazard_state` outputs including `* released`, `* active`, and `* needed`), `hazardClock`, `hazardHold`, cross-home `pause`, reported observation `urgency:`, and cross-home `Unavailable`/`Unknown`/`Mismatch` rows to lead with explicit state words (`Confirmed:`, `Waiting:`, `Action needed:`, `State:`, `Unknown:`, `Stop-work indicator:`), guarded prototype properties via `Object.hasOwn` and invalid date strings against `"Recorded Unknown"` / `"Service responded Unknown"`, added `HAZARD_STATE_KEY_COPY` prose in both per-home and cross-home panels, and kept zero banned `CopyAudit` words.
* Completion evidence: `test_safety_screens.py`, `test_safety_screen_wcag_keyboard.py`, `test_content_standard.py`, and `safety_screens_browser_check.py` all pass.
* Validation: Passed

### Non-colour CSS link underlines, 24px target sizing, heading scroll margin, and flag borders

* Related phase or task: `P01-T03`
* Files: `src/api/src/zava_forward/api/web/style.css`
* What changed and why: Updated `.screen-links a` to `display: inline-flex; align-items: center; min-height: 1.5rem; padding-inline: var(--sp-1); color: var(--brand-d); text-decoration: underline; text-underline-offset: .16em;` (preserving `.screen-links a[aria-current="page"]` `font-weight: 600; text-decoration-thickness: .2em` and `:focus-visible` two-tone ring with zero motion), added `scroll-margin-top: var(--sp-4)` on `.screen-evidence h2, .screen-evidence h3, .screen-record h2`, and added `border: 1px solid var(--soft-line)` on `.flag` plus `border-color: var(--warn)` on `.flag.danger`.
* Completion evidence: `test_accessibility_baseline.py`, `test_design_system.py`, `test_role_screens_conformance.py`, `test_safety_screen_wcag_keyboard.py`, and Chromium `getBoundingClientRect().height >= 24` + `axe-core` 4.10.3 pass.
* Validation: Passed

### WCAG unit tests, conformance tightening, browser harness alignment, and Focused-tier validation

* Related phase or task: `P02-T01`, `P02-T02`
* Files: `src/api/tests/test_safety_screen_wcag_keyboard.py`, `src/api/tests/test_role_screens_conformance.py`, `src/api/checks/safety_screens_browser_check.py`
* What changed and why: Removed the legacy `'h("a", { href: "#",' ` inline-onclick carve-out and forbade `href: "#"` in `test_role_screens_conformance.py`; updated `test_safety_screen_wcag_keyboard.py` (`0` deletions, `3` net new methods `<= 5` max, `TYPE_CHECKING` + `importlib.import_module("test_safety_screens")`) to verify delegated `a[data-jump]` click focus/scroll, `#/role/building_safety_lead` & `#/role/repairs` loader and view permissions, `Object.hasOwn` prototype-key & corrupt-timestamp safety, cross-home summary jump nav & `Stop-work indicator:` cues, and `.screen-links a` / `.flag` CSS rules; updated `checks/safety_screens_browser_check.py` to force `content-visibility: visible` on `.screen-record` panels during full-evidence text/axe scans and verify `#/role/...` navigation, `>= 24px` underlined jump links, and keyboard `Enter` focus movement in Chromium.
* Completion evidence: `mypy` (`0` issues across 285 files), `ruff check .` (`All checks passed!`), `ruff format --check .` (`201 files already formatted`), screen/WCAG/conformance unit suites (`OK`), and `ZF_AXE_JS=/tmp/axepk/package/axe.min.js python3 checks/safety_screens_browser_check.py` (`0` violations, `0` incomplete across all 4 axe runs) all exited `0`.
* Validation: Passed

### Refreshed Web Interface Guidelines `file:line` review

Fetched `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` immediately before reviewing changed web files:

```text
## src/api/src/zava_forward/api/web/role-screens.js

✓ pass

## src/api/src/zava_forward/api/web/app.js

✓ pass

## src/api/src/zava_forward/api/web/style.css

✓ pass
```

## Implementation-Time Plan and Detail Updates

### Deduplicate unselected `overview` VDOM child, add `.screen-record h2` `scroll-margin-top`, and align `safety_screens_browser_check.py` with `content-visibility: auto`

* Affected plan area or markers: `Scope and Non-Goals`, `P01-T03`, `P02-T01`, `P02-T02`
* What changed: Removed the redundant `, overview` argument inside unselected `selected` (`role-screens.js:159`) since `main` (`role-screens.js:164`) already mounts `overview` before `selected`; added `scroll-margin-top: var(--sp-4)` on `.screen-record h2` (`style.css:369`); and added `set_panel_rendering(page, True/False)` plus `#/role/...` and jump-link assertions in `src/api/checks/safety_screens_browser_check.py`.
* Why: Prevents duplicate `#hazard-page-summary-heading` IDs in VDOM tests, satisfies the refreshed Web Interface Guidelines `scroll-margin-top` rule on heading anchors, and ensures Chromium does not skip below-fold `content-visibility: auto` `.screen-record` subtrees during `inner_text()` and `axe.run()` in #227's browser check (matching `procurement_screens_browser_check.py`).
* Triggering evidence: `RoleScreensGlobalScope.test_role_hash_aliases_load_scripts_render_views_and_block_unauthorised_roles` VDOM inspection, refreshed `command.md` fetch, and live Chromium execution of `checks/safety_screens_browser_check.py`.
* User answer or decision: None required (immediately relevant current-state update preserving approved intent and locked `tests/test_*.py` bounds).
* Reconciliation performed: Reconciled `In Scope`, `P01-T03`, and `P02-T01` in `.copilot-tracking/plans/2026-11-15/safety-repairs-wcag-227-plan.md` and `P02` boundaries/targets in `.copilot-tracking/details/2026-11-15/safety-repairs-wcag-227-phase-details.md`.
* Planning and critique state: Not needed (`PC-001` through `PC-004` remain resolved; locked `0` new test files, `0` deletions, and `3 <= 5` net new unittest methods honored).

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `node --check` | `role-screens.js`, `app.js` | Passed | Exit `0` for both modified JS files |
| `mypy` | `src/api` (285 source files, strict) | Passed | `Success: no issues found in 285 source files` |
| `ruff check .` | `src/api` (`src`, `tests`, `checks`) | Passed | `All checks passed!` |
| `ruff format --check .` | `src/api` (201 files) | Passed | `201 files already formatted` |
| Targeted unit suites | `test_safety_screens.py`, `test_safety_screen_wcag_keyboard.py`, `test_role_screens.py`, `test_role_screens_conformance.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_design_system.py`, `test_asset_exec_screen_wcag.py`, `test_finance_screens_wcag_225.py`, `test_workspace_scripts.py` | Passed | All tests `OK` (verified both with and without `:tests` in `PYTHONPATH`) |
| Chromium + pinned `axe-core` 4.10.3 | `checks/safety_screens_browser_check.py` (`ZF_AXE_JS=/tmp/axepk/package/axe.min.js`) | Passed | `0` axe WCAG 2.2 AA violations and `0` incomplete items across per-home and cross-home views of `safety-lead` (`#/role/building_safety_lead`) and `hazard-triage` (`#/role/repairs`), 320px/1280px reflow, `>= 24px` underlined jump links, keyboard `Enter` heading focus, `0` writes, `0` JS errors |
| Web Interface Guidelines (`command.md`) | `role-screens.js`, `app.js`, `style.css` | Passed | Refreshed `command.md` and audited all changed web files: `✓ pass` |

## Pre-Review Reconciliation

* Plan markers and phase details: Current (`P01`, `P01-T01`, `P01-T02`, `P01-T03`, `P02`, `P02-T01`, `P02-T02` all `[x]` and reconciled with phase details)
* Completed-work evidence and handoff prose: Current
* Validation, blockers, remaining work, and follow-up items: Current
* Review readiness: Ready for `rpi-review`

## Blockers

* None for implementation or `rpi-review`.

## Remaining Work

* None inside `rpi-implement` scope (`P01` and `P02` complete; single local `git commit` executes immediately after `rpi-review` writes `.copilot-tracking/reviews/2026-11-15/safety-repairs-wcag-227-review.md` so all `.copilot-tracking/` artifacts are included cleanly in one commit).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/safety-repairs-wcag-227-plan.md, `## Follow-Up Items`
* Human assistive-technology and named safety-role user validation (#151, #155, #156) for `safety-lead` and `hazard-triage`: Outside automated CLI scope because repository accessibility governance (`docs/reference/research/ux/wcag-conformance-baseline.md`) requires manual screen-reader, magnification, and named safety-role walkthroughs before claiming full WCAG 2.2 AA conformance or closing #227. Owner: Human UX / Building Safety Lead reviewer.

## Return-to-Caller State

* Implementation execution status: Complete (Full plan)
* Declared scope and markers: Full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P01-T03`, `P02`, `P02-T01`, `P02-T02`; remaining: none
* Validation coverage: Focused tier (`node --check`, `mypy`, `ruff check .`, `ruff format --check .`, targeted `src/api` unit suites) + Chromium & pinned `axe-core` 4.10.3 (`safety_screens_browser_check.py`) + refreshed Web Interface Guidelines `file:line` review all passed
* Blockers: None
* Current plan and detail updates: Deduplicated unselected `overview` VDOM child (`role-screens.js`), added `.screen-record h2` `scroll-margin-top` (`style.css`), and aligned `safety_screens_browser_check.py` with `content-visibility: auto`
* Planning and critique state: Ready (`PC-001` through `PC-004` resolved; locked test bounds preserved)
* Follow-up items: Human AT and named safety-role validation (#151, #155, #156)
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent

