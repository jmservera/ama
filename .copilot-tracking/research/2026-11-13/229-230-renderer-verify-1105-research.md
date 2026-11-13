# Research: #229/#230 renderer verification (229-230-renderer-verify-1105)

Base 3b05143179f83235c5b4e80e70aad99bdc44d83f. Refs #229, #230, #135, #149. Validation tier: Focused.
Disposition: executed (bounded read-only inspection). Planning Readiness: Ready.

## Findings

* Existing Node-VM tests: `src/api/tests/test_programme_screen.py` (PAGING_SCRIPT, 120 cases, page size 50; covers page 1, Next, Previous-at-start produces no fetch, Previous back to page 1, load failure), `test_data_operator_screen.py`, `test_data_operator_ai_state.py`, `test_exception_register_screen.py`, `test_exception_register.py`, `test_role_screens.py`, `test_role_screens_conformance.py`.
* `role-screens.js` `programmeQueue` (lines ~308-350): Previous/Next buttons (`#programme-prev`, `#programme-next`) carry only `class`, `type`, `id`, `onclick`. They have NO `disabled` and NO `aria-disabled` attribute at any boundary. Clamping is by onclick guard (`offset > 0`, `offset + items.length < total`), a silent no-op. The pager group is omitted entirely when `total <= first.length`.
* Gap: existing tests do not exercise the last page (offset 100, total 120), a middle page's two-way navigation, Next at the end boundary, or an empty queue (total 0).
* Not in scope: editing src/docs, manual AT/WCAG AC4 conformance, browsers.

## Decision

Verify with the existing modules plus an ad hoc Node VM harness (not committed to src), recording exact attributes. Report the absent disabled/aria-disabled as an observation for follow-up, not a fix.
