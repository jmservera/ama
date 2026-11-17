# Research: Programme screens WCAG state clarity (Issue #230)

* Task: `prog-screens-wcag-230`; branch `feat/ux-230-prog-screens-wcag-1545`, stacked on PR #1639.
* Research disposition: executed (direct code inspection). Planning Readiness: Ready.

## Findings

* No function named `renderProgrammeScreen` exists. The programme role view is the `programme-queue` screen registered in `src/api/src/zava_forward/api/web/role-screens.js` (roles: Retrofit Programme Manager, Programme Support Officer, Retrofit Coordinator). Its `render(c, extra)` shows the per-home "Same-home step states" table (Technical, Resident, Delivery, Quality, Finance).
* State text in the table is already words ("Blocked", "Blocked: evidence missing", "No recorded blocker"), but carries no uniform prefix and no section navigation.
* Dependents that pin the exact state cells: `tests/test_programme_screen.py` (asserts `Blocked` absent from the clear render, no `button`/`form`/`input` tags), `checks/connected_home_browser_check.py` and `checks/role_screens_browser_check.py` (exact row cells, `startswith("Blocked")`), `checks/specialist_keyboard_browser_check.py` (region named "Same-home step states").
* `style.css` has a global `nav` rule with white links (header styling), so a `nav` element in the body is unsafe. Documented design-system classes `.row` and `.btn`/`.alt` (docs/reference/research/ux/design-system.md, component inventory) are available.
* App routing is hash based, so in-page `#fragment` links would navigate away; focus must move through `onclick`.
* No step state is a pass: every "No recorded blocker" row says "This is not a pass".

## Decisions

* Keep the table cells unchanged; add a "State summary in words" list with `Action needed:` / `Warning:` prefixes (dictionary lookup via `Object.hasOwn`; unknown states fall back to `Warning`, never `Pass`).
* Add a `.row` group of `a.btn.alt` links that focus the section targets (`tabindex=-1`); no buttons, forms or `nav`.
* Evidence limit: browser checks cannot be run here; engineering checks do not establish accessibility acceptance.
