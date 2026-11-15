<!-- markdownlint-disable-file -->
# Details: UX design traceability matrix (issue 149)

## Phase 1: matrix

* File: `docs/reference/research/ux/design-system.md`, new section "Journey to requirement to design to test traceability" before "Verification".
* Table columns: Journey, Requirement IDs, UX design artefact, Web surface, Automated test evidence, Human evidence.
* Surface tokens: `screen:<id>`, `panel:<function>`, `route:<path>`, `web:<file>`. Test tokens: `path.py::Class::method`; browser checks as `src/api/checks/<file>.py`.
* Human column always begins `pending human test`.

## Phase 2: test

* `src/api/tests/test_ux_design_traceability.py`, unittest style like `test_design_system.py`.
* Cases: every row complete; referenced files exist; screens, panels and routes resolve in source; test classes and methods exist (AST); requirement IDs found in PRD or BRD; every registered role screen appears in the matrix; human column pending and no conformance claim words.

## Phase 3: validation

Run in `/tmp/venv-149-2328` (pip): the new test, `test_accessibility_baseline`, `test_content_standard` (src/api); `test_scenario_manifest`, `test_needs_inventory` (src/core); `ruff check`, `ruff format --check`, `mypy` in src/api.
