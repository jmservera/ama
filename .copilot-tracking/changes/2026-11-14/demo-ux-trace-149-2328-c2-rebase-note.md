# C2 rebase note (PR #1587, Issue #149)

Date: 2026-11-14

* Fetched `origin/main` (8924b501c6a24bacbf0f429b9e54f3e62fa5b223) and rebased the two branch commits cleanly; no conflicts.
* Preserved append-only `docs/reference/log.md` (4 added lines, 0 removed) and the single `docs/reference/README.md` index row change.
* Relative links in the added log lines resolve; 17 broken links reported in `docs/reference/log.md` are pre-existing historical entries on main (legacy `mvp/` and `capstone/` paths) and are untouched.
* `git diff --check` clean.
* `src/core/tests/test_scenario_manifest.py`: 8 passed, 57 subtests. `src/api/tests/test_ux_design_traceability.py`: 7 passed.
* Not pushed. Hosted CI and independent review remain pending.
