<!-- markdownlint-disable-file -->
# Issue 189 C3 type applicability plan (2026-11-09)

Research: [research](../../research/2026-11-09/type-applicability-189-c3-research.md). Details: [details](../../details/2026-11-09/type-applicability-189-c3-details.md). Critique: [critique](type-applicability-189-c3-critique.md). Refs #189 only. Cycle: C1, C2 spent; C3 authorised for type remediation only; two remain after.

## Objective

Remove the eight mypy diagnostics that #189 introduced in `tests/test_simulator_admin.py` and `checks/simulator_control_browser_check.py` with typed helpers only, so the maintained `mypy` command passes as it does on main.

## Phases

* [ ] P1 Commit research, plan, details, critique (one) and initial state before any source edit (frozen).
* [ ] P2 Edit only the two files; typed `Callable` aliases and a small `Protocol`; no `Any`, cast, ignore or config change.
* [ ] P3 Validate with the CI profile: `ruff check .`, `ruff format --check .`, `mypy`; `test_simulator_admin`, `test_live_control`; the browser/axe check and the delayed-write regression.
* [ ] P4 Changes record, one Review, final state, evidence commit, hashes, handoff.

## Owner-selected demo-targeted tier

Focused lint, format, mypy, control tests and the current browser and delayed-write checks. Not run: global matrix, `rpi-checks`, SQL, Azure, models, private data. Hosted checks and independent exact-head review remain required.

## Stop rule

A new diagnostic needing `Any`, a cast, an ignore, a config change or an unrelated correction is recorded and stops; no cycle is spent on it without authorisation.
