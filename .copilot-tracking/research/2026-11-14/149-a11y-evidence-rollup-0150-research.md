<!-- markdownlint-disable-file -->
# Research: Epic #149 criterion 3 test-result rollup

* Disposition: executed. Planning Readiness: Ready.
* Existing suites: `test_accessibility_baseline` (13 tests), `test_content_standard` (29), `test_design_system` (9), `test_role_screens_conformance` (12), `test_safety_screens`, `test_safety_panel_ux` (#1530), `test_procurement_screens`, `test_resident_choice_screen`, `test_regulatory_chat_api`, `test_regulatory_ux_check`, `test_chat_widget_focus`, `test_production_ux_acceptance_protocol`.
* Finding: `test_ux_design_traceability` named in the brief does not exist on this base; it was not invented. Traceability (criterion 4) is out of scope.
* Sharding: `src/api/pyproject.toml` lists modules only for ruff and mypy overrides; tests run by unittest discovery (`test*.py`), so no registration is needed. The file is untouched (new module is fully typed and passes strict mypy).
* Human gates: `production-ux-acceptance-protocol.md` record cells are all `Not run`; `wcag-conformance-baseline.md` states automated checks are not conformance, AT (#155) or user validation. Docs under `docs/reference/research/ux/` are read only (open PR #1587 touches them).
