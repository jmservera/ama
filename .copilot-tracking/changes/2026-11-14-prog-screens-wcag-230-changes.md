# Changes: Programme screens WCAG state clarity (Issue #230)

Plan: [plan](../plans/2026-11-14-prog-screens-wcag-230-plan.md)

## Files

* `src/api/src/zava_forward/api/web/role-screens.js`: `programme-queue` `render` now has a `.row` group of native `button.btn.alt` controls (State summary, Step states table, Journey stages, Not shown for this role) that move focus to `tabindex=-1` section wrappers; a "State summary in words" list prefixes each step with `Action needed:` or `Warning:` via `programmeStateLabel` (`Object.hasOwn` lookup, unknown falls back to `Warning`). Step table cells are unchanged. No new `screenPanel` titles (the connected-home panel inventory test pins them).
* `src/api/tests/test_programme_screen.py`: the two no-`button` assertions now expect exactly the four section-jump buttons (other controls still forbidden).
* `src/api/tests/test_programme_screen_wcag.py`: 5 focused tests (prefixes, no `Pass`, unchanged cells, documented classes and focus, no nav/controls).

## Divergences

* `renderProgrammeScreen` does not exist; the `programme-queue` screen's `render` was changed.
* `Pass:` is defined in the brief but not emitted, because every clear step is explicitly "not a pass".

## Divergence found by validation

* First draft used anchors with `onclick`; the full run caught `test_role_screens_conformance` (handlers only on native buttons). Switched to buttons.

## Validation

* Targeted: test_programme_screen_wcag, test_programme_screen, test_role_screens, test_design_system, test_connected_home_check, test_specialist_keyboard_check, test_case_journey: 99 OK.
* `ruff check`, `ruff format --check`, `mypy` in `src/api`: clean.
* Full `unittest discover` (3397 tests) ran before the button switch: one failure (the conformance test above, since fixed). The affected modules (programme, role_screens, conformance, design_system, connected_home, specialist_keyboard, case_journey, atlas_tensions, traceability, workspace_scripts, same_home_identity) were rerun after the fix and pass. The whole suite was not rerun after the fix.
* Not run: browser checks (`specialist_keyboard_browser_check.py` etc.), so keyboard behaviour is not browser-verified.
