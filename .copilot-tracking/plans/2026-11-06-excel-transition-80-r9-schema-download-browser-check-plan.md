# Issue 80 r9 plan: executable schema download browser regression (not run)

Research: [research](../research/2026-11-06-excel-transition-80-r9-schema-download-browser-check-research.md). Details: [details](../details/2026-11-06-excel-transition-80-r9-schema-download-browser-check-details.md).

* [ ] Phase 1: add `src/api/checks/schema_download_browser_check.py` using the existing `main`/`check`/fixture helpers and real server authorization.
* [ ] Phase 2: static validation only (py_compile, Ruff isolated as CI does for checks, format, mypy via component config, existing finance-screen unit module); prove production files byte-identical to 1e56f44; document the command in `src/api/README.md`.
* [ ] Phase 3: write r9 changes and state, validate JSON and links; then the single final Review after a refreshed web-guidelines fetch; commit.

## Critique (once, before edits)

* Risk: an unrunnable test claimed as evidence. Mitigation: label unperformed everywhere; the module asserts only through real browser, keyboard, download and server responses, no string stand-ins.
* Risk: reusing the existing mocked-review story as proof. Mitigation: new module with no `page.route`; the research records why the old story is not evidence.
* Risk: a seeded schema bypassing registration. Mitigation: seed through the real POST as pam.
* Risk: touching the full runner or CI. Mitigation: no workflow, matrix or runner edit; manual documented command only.
* No conflict with confirmed decisions. Critique executed once and not repeated.

## Gates

Browser run, FULL, independent exact-head review and hosted CI remain pending. #188 owns the heavy lane.
