# Issue 80 r8 plan: schema catalogue download on the finance funding screen

Research: [research](../research/2026-11-06-excel-transition-80-r8-schema-download-ui-research.md). Details: [details](../details/2026-11-06-excel-transition-80-r8-schema-download-ui-details.md).

* [x] Phase 1: add the "Form schema catalogue" panel with one semantic download link to `finance-funding` in `role-screens.js`, only when the form-review read succeeded.
* [x] Phase 2: add focused vm-harness tests in `test_finance_grants_screens.py` for present, absent (unreadable review) and nonconforming-review cases, and narrow the two no-anchor assertions to allow only this link.
* [x] Phase 3: run light checks (node --check, the finance, conformance, content, role-screens and loading-feedback API unit modules, Ruff, format, mypy) with external caches; record the future browser selector unrun.
* [x] Phase 4: write changes and state, commit. The final Review (after a refreshed guideline fetch and the final checks) is a separate later artifact and commit, recorded in its own file.

## Critique

Planned as one internal critique before implementation. Result: the main risk is showing a working link to an unauthorised role; mitigated by tying it to the successful `form-review` read, which uses the same `forms._actor`, instead of role names. The second risk is silently weakening the existing no-control tests; mitigated by allowing exactly one named href and still rejecting buttons, inputs and handlers. No conflict with confirmed decisions. Critique executed once, not repeated.

## Gates

FULL remains required and pending. Browser, SQL and heavy lanes are not run.
