# Changes: issue 232 housing officer and resident engagement screens (2026-11-01)

* Added: `resident-choice` read-only role screen appended to `src/api/src/zava_forward/api/web/role-screens.js` for resident-view roles.
* Added: `src/api/tests/test_resident_choice_screen.py` (3 node-vm tests).
* Validation: new, asset_board, role_screens, design_system, accessibility_baseline tests pass (role_screens need the core/agents PYTHONPATH per the api guide); ruff check, ruff format --check and mypy on touched files clean.
* Divergence: none. Browser and axe keyboard checks not run locally; CI is the evidence.

## Review-thread corrections (PR #652)

* Fixed: `role_screens_browser_check.py` default path tolerates installed screens (empty message or nav links) and registers the `232` scenario against the synthetic fixture.
* Fixed: paused or withdrawn panel keeps a stopped latest answer with an unresolved human review visible when a later scope change makes the current status Not recorded; shows the answer's own scope.
* Fixed: latest recorded answer cell shows its own scope, context revision and design version.
* Tests: two new node-vm assertions (version binding, stale stop with review). Unit, ruff and both browser selectors (parent, 232) pass locally.
* CI: merged origin/main for drift failures. `assistant_release.py` on main has a syntax error (lines 183-184, from #658); out of scope, so not changed here and verified locally with a temporary uncommitted workaround. The activation check failed on a GitHub API quota guardrail (transient).
