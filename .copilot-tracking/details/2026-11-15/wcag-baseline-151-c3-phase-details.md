<!-- markdownlint-disable-file -->
# RPI Phase Details: Focused Cycle 3 Safety-Screen Table Header Remediation for PR #1802 (#151)

## Metadata

* Task ID: 2026-11-15-wcag-baseline-151-c3
* Task slug: wcag-baseline-151-c3
* Related plan: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-c3-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/wcag-baseline-151-c3-research.md, src/api/tests/test_safety_screens.py, src/api/src/zava_forward/api/web/role-screens.js, src/api/tests/test_wcag_workbench_baseline_151.py, docs/reference/research/ux/wcag-conformance-baseline.md, src/api/pyproject.toml

## Phase Index

| Phase ID | Name | Status | Detail sections |
|---|---|---|---|
| P01 | Align Safety-Screen Table Header Test Assertions and Run Focused Validation | completed | P01, P01-T01, P01-T02 |

<!-- rpi:phase id=P01 -->
## P01: Align Safety-Screen Table Header Test Assertions and Run Focused Validation

### Context

In `PR #1802` (`feat/ux-151-wcag-baseline`), `src-api` CI executed `3,612` unit tests and reported `1` failure: `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py`. Cycle 1 changed `screenTable` in `src/api/src/zava_forward/api/web/role-screens.js` to default `rowHeader = true`, emitting `<th scope="row">` for column `0` (`Item` or `Home and item`) of every `<tbody>` row in `safety-lead` and `hazard-triage`. `test_safety_screens.py` previously searched `find_all(table, "th")` across the whole table and expected only `scope="col"` headers and `<td>`-only body rows. Cycle 3 research (`C1`-`C10`, `W1`) proved Option 2 is required so `<th scope="row">` semantics, `test_wcag_workbench_baseline_151.py`, and `docs/reference/research/ux/wcag-conformance-baseline.md` remain intact.

### Intent

Update `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py` to assert `<thead>` `<th scope="col">` column headers and `<tbody>` leading `<th scope="row">` row headers plus `<td>` data cells matching `len(heads)`, then prove clean execution across the required unit, lint, format, and type-check gates.

### Boundaries

* Included: `src/api/tests/test_safety_screens.py` and Cycle 3 `.copilot-tracking/` artifacts.
* Excluded: `src/api/src/zava_forward/api/web/*`, `docs/reference/*`, `tools/rpi-checks.py`, historical Cycle 1 and Cycle 2 `.copilot-tracking/` artifacts, and remote `git push`.

### Likely Targets

* src/api/tests/test_safety_screens.py: Update `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned`.

### Dependencies

* None.

### Validation Expectations

* All six caller-specified `unittest` modules (`65` tests) and `(cd src/api && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy)` exit `0`.

### Completion Evidence

* Surgical diff in `src/api/tests/test_safety_screens.py` and green validation command outputs recorded in `.copilot-tracking/changes/2026-11-15/wcag-baseline-151-c3-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Update SafetyScreens table header and column alignment assertions

#### Context

In `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned`, each rendered `<table>` in `safety-lead` and `hazard-triage` (`screen["tree"]` and `screen["summary"]`) contains one `<thead>` and one `<tbody>`. `<thead>` holds the column headers (`<th scope="col">`), while each `<tbody>` `<tr>` holds `[<th scope="row">, <td>, ...]` where the leading `<th scope="row">` names the hazard item (`H-1`) or home-and-item (`C-1 H-1`, `C-9`, `C-3`, `C-4`).

#### Intent

Replace the table-wide `find_all(table, "th")` check in `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` with explicit `<thead>` and `<tbody>` assertions verifying:
1. `(thead,) = find_all(table, "thead")`, non-empty `heads = find_all(thead, "th")`, and `all(t["attrs"] == {"scope": "col"} for t in heads)`.
2. `(tbody,) = find_all(table, "tbody")`, non-empty `rows = find_all(tbody, "tr")`, and for every `row`:
   * `row["kids"][0]["tag"] == "th"` with `row["kids"][0]["attrs"] == {"scope": "row"}` and non-empty stripped `string_leaves(row["kids"][0]["kids"])`,
   * `row_heads = find_all(row, "th")` has length `1`,
   * `data_cells = find_all(row, "td")` covers all remaining columns (`all(c["tag"] == "td" for c in row["kids"][1:])`), and `len(row_heads) + len(data_cells) == len(heads)`.

#### Boundaries

* Included: `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py`, formatted cleanly within `100` columns and strict Mypy typing.
* Excluded: Changing any other test method in `src/api/tests/test_safety_screens.py` or modifying `role-screens.js`.

#### Likely Targets

* src/api/tests/test_safety_screens.py

#### Dependencies

* None.

#### Validation Expectations

* `(cd src/api && PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m unittest tests/test_safety_screens.py -q)` passes all 14 tests in `test_safety_screens.py` and `python3 -m ruff format --check tests/test_safety_screens.py` exits `0`.

#### Completion Evidence

* Updated `test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Execute Focused unittest, Ruff, and Mypy validation

#### Context

The caller requires verifying all six accessibility and specialist-screen `unittest` suites alongside `ruff check .`, `ruff format --check .`, and `mypy` inside `src/api`, without running `tools/rpi-checks.py`.

#### Intent

Run the complete Focused validation command set and verify historical Cycle 1 and Cycle 2 `.copilot-tracking/` files remain unmodified.

#### Boundaries

* Included: Local execution of the six `unittest` suites, `ruff check .`, `ruff format --check .`, `mypy`, and `git status --short` verification.
* Excluded: `tools/rpi-checks.py` and `git push`.

#### Likely Targets

* `src/api/tests/` and `src/api/src/` validation runners.

#### Dependencies

* P01-T01.

#### Validation Expectations

* `(cd src/api && PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m unittest tests/test_safety_screens.py tests/test_wcag_workbench_baseline_151.py tests/test_accessibility_baseline.py tests/test_epic149_landmarks_skip_link_focus_order.py tests/test_housing_resident_wcag_232.py tests/test_role_screens.py -q)` exits `0` (`65` tests `OK`).
* `(cd src/api && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy)` exits `0`.

#### Completion Evidence

* Exact command results recorded in `.copilot-tracking/changes/2026-11-15/wcag-baseline-151-c3-changes.md`.

#### Unresolved Items

* None.
