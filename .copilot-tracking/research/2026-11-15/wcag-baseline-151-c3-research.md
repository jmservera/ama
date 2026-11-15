<!-- markdownlint-disable-file -->

# Task Research: wcag-baseline-151-c3

| Field                | Value                                                                 |
|----------------------|-----------------------------------------------------------------------|
| Date                 | 2026-11-15                                                            |
| Researcher / agent   | RPI Agent (`rpi-research`)                                            |
| Status               | Complete                                                              |
| Artifact path        | .copilot-tracking/research/2026-11-15/wcag-baseline-151-c3-research.md |
| Research disposition | executed                                                              |
| Planning Readiness   | Ready                                                                 |

## Research Brief

* What to research: Root cause, semantic trade-offs, and cross-suite impact of the `PR #1802` `src-api` CI failure in `src/api/tests/test_safety_screens.py::SafetyScreens::test_rendered_tables_are_labelled_focusable_and_aligned` (line 130), comparing Option 1 (restoring `rowHeader = false` default in `function screenTable(...)` in `src/api/src/zava_forward/api/web/role-screens.js`) against Option 2 (updating `test_safety_screens.py` `test_rendered_tables_are_labelled_focusable_and_aligned` to assert `<thead>` `<th scope="col">` and `<tbody>` `<th scope="row">` + `<td>` alignment).
* Why it matters: In `PR #1802` (`feat/ux-151-wcag-baseline`), `src-api` ran `3,612` tests with `3,611` passing and `1` failure in `test_safety_screens.py:130`. Remediating this defect in Cycle 3 (`c3`) must preserve WCAG 2.2 AA `1.3.1 Info and Relationships` row-header semantics, `docs/reference/research/ux/wcag-conformance-baseline.md` accuracy, and all `3,612` `src/api` unit tests plus `ruff` and `mypy`.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` in this confirmed automatic `c3` RPI loop, plus coordinator verification of `PR #1802` for Issue `#151`.
* Scope: `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/staff-intake.js`, `src/api/tests/test_safety_screens.py`, `src/api/tests/test_wcag_workbench_baseline_151.py`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_epic149_landmarks_skip_link_focus_order.py`, `src/api/tests/test_housing_resident_wcag_232.py`, `src/api/tests/test_role_screens.py`, `src/api/checks/role_screens_browser_check.py`, `src/api/checks/specialist_keyboard_browser_check.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, and `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`.
* Non-goals: Running `tools/rpi-checks.py`, pushing to a remote, altering historical Cycle 1 or Cycle 2 `.copilot-tracking/` artifacts, or claiming human assistive-technology conformance (`Refs #151`).
* Criteria: Select the option backed by WCAG 2.2 AA `1.3.1` semantics, codebase callers, documentation consistency, and regression guards; verify zero unintended side effects across `src/api/tests/`, `ruff check .`, `ruff format --check .`, and `mypy`.
* Requested outputs: Converged implementation recommendation for `rpi-plan` with exact `path:line` evidence.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                               |
|--------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1-Q4 covering `screenTable` callers and WCAG 1.3.1 semantics, `test_safety_screens.py` failure mechanics, Option 1 vs Option 2 side effects, and lint/type/manifest guards |
| Codebase scope                       | `src/api/src/zava_forward/api/web/`, `src/api/tests/`, `src/api/checks/`, `docs/reference/research/`                                |
| External scope                       | Vercel Web Interface Guidelines (`command.md`) and WCAG 2.2 SC 1.3.1 via `accessibility` skill                                      |
| Initial internal candidate areas     | `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_safety_screens.py`, `src/api/tests/test_wcag_workbench_baseline_151.py`, `docs/reference/research/ux/wcag-conformance-baseline.md` |
| Initial external candidate areas     | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`                                            |
| Research posture                     | focused                                                                                                                             |
| Posture provenance                   | caller-supplied single-test CI regression with bounded candidate remedies under the Focused validation tier                         |
| Explicit limits / deadline           | Focused validation tier (`src/api` unit tests + `ruff check .` + `ruff format --check .` + `mypy`); do NOT run `tools/rpi-checks.py` |
| Posture-specific completion basis    | focused scope saturation across all `screenTable` call sites, specialist test suites, baseline UX documentation, and CI linters     |
| Edits allowed during research?       | no, research-only                                                                                                                   |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                                |
| Known constraints / excluded sources | Preserve Cycle 1 and Cycle 2 `.copilot-tracking/` artifacts, keep human AT gates `Not run` (`Refs #151`), and leave a clean unpushed HEAD |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                         | Match and provenance                                 | Scoped authority or output contract                                   | Selected / skipped reason                                                       |
|---------------------|-----------------------------------|------------------------------------------------------|-----------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` matches workspace and evidence paths | Enforces WCAG baseline honesty, Focused tier rules, and commit format | Selected: mandatory repository contract                                         |
| Skill               | `rpi-research`                    | Active phase skill for Research                      | Three-wave research artifact and readiness contract                   | Selected: active RPI phase                                                      |
| Skill               | `accessibility`                   | Domain match on WCAG 2.2 SC 1.3.1 row/column headers | WCAG 2.2 table relationship semantics                                 | Selected: loaded at intake to evaluate Option 1 vs Option 2 table header model  |
| Skill               | `web-design-guidelines`           | Loaded per Web Development Guidance before web review | Fetched `command.md` semantic HTML `<table>` rules                    | Selected: loaded and fetched via `web_fetch` to verify semantic table rules     |
| Research specialist | `hve-core-all:rpi-researcher`     | Host-registered specialist for independent lanes     | Delegated subagent lane markdown                                      | Skipped: single tightly coupled invariant across 4 files inspected inline       |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                   | Answers / unanswered   | Resulting decision or selected further research                                 |
|------------------|---------------------------------------------------------------------------------------------------------|------------------------|---------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit caller root-cause summary, two candidate options, and validation commands | N/A (non-interactive) | Proceed autonomously in confirmed automatic RPI mode (`c3`) with `focused` posture and `convergence` output mode |
| Direction change | None; all findings stay strictly inside the caller-defined defect and candidate remedies                | N/A                    | Retain focused scope without widening                                           |
| Convergence      | Contrarian wave proved Option 1 breaks `test_wcag_workbench_baseline_151.py:537` and contradicts `wcag-conformance-baseline.md:54`, whereas Option 2 aligns `test_safety_screens.py` with the 10 peer specialist WCAG suites | N/A | Converge on Option 2 (`src/api/tests/test_safety_screens.py` update)            |

## Scope and Success Criteria

* Scope: `role-screens.js`, `staff-intake.js`, `test_safety_screens.py`, `test_wcag_workbench_baseline_151.py`, peer `test_*_wcag*.py` specialist suites, `role_screens_browser_check.py`, `specialist_keyboard_browser_check.py`, `wcag-conformance-baseline.md`, and `scenario-manifest.json`.
* Assumptions:
  * Either Option 1 or Option 2 could resolve `test_safety_screens.py:130`, so Cycle 1 must inspect every `screenTable` call site, every peer test suite, and `wcag-conformance-baseline.md` before choosing.
* Success criteria:
  * Every `screenTable` call site in `web/` is checked for first-column row-header validity under WCAG 2.2 SC 1.3.1.
  * Every side effect of Option 1 and Option 2 across tests, browser checks, and documentation is verified with `path:line` evidence.
  * Exact reproduction of the failure is confirmed before planning.

## Task Research Requests

* Explicit requests:
  1. Investigate `PR #1802` `src-api` CI failure in `src/api/tests/test_safety_screens.py` line 130 (`test_rendered_tables_are_labelled_focusable_and_aligned`) caused by `screenTable(..., rowHeader = true)` in `src/api/src/zava_forward/api/web/role-screens.js` line 50.
  2. Evaluate Option 1 (restore `rowHeader = false` default in `role-screens.js`) versus Option 2 (update `test_safety_screens.py` to inspect `thead` `th[scope="col"]` and `tbody` `th[scope="row"]` + `td` cells matching `len(heads)`).
  3. Prepare `rpi-plan` handoff for Focused validation (`test_safety_screens.py`, `test_wcag_workbench_baseline_151.py`, `test_accessibility_baseline.py`, `test_epic149_landmarks_skip_link_focus_order.py`, `test_housing_resident_wcag_232.py`, `test_role_screens.py`, `ruff check .`, `ruff format --check .`, and `mypy`).
* Inferred research questions:
  * Are the first columns of `safety-lead` / `hazard-triage` tables and the other `screenTable` call sites genuine row headers under WCAG 2.2 SC 1.3.1?
  * Would Option 1 break `test_wcag_workbench_baseline_151.py` or contradict `wcag-conformance-baseline.md`?
  * Does any other test in `test_safety_screens.py` or across the entire `src/api/tests/` suite fail with `rowHeader = true`?
* Caller constraints and non-goals: Do NOT run `tools/rpi-checks.py`; do NOT push to remote; preserve historical `.copilot-tracking/` artifacts.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint    | Effect on active brief, evidence, or revalidation                            |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|------------------------|------------------------------------------------------------------------------|
| narrow                                                   | Focused validation tier (`src/api` unit tests + `ruff` + `mypy`); exclude `tools/rpi-checks.py`         | Caller prompt / Intake | Keep validation strictly to requested unit suites, `ruff`, and `mypy`        |
| exclude                                                  | Do not push branch `feat/ux-151-wcag-baseline`; leave clean frozen HEAD                                 | Caller prompt / Intake | Commit locally with Copilot trailer only                                     |

## Research Questions

|  # | Sub-question                                                                                                                                          | Type            | Priority | Status   |
|---:|-------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | Do all `screenTable` callers in `role-screens.js` and `staff-intake.js` (especially `safety-lead` and `hazard-triage`) place a row-identifying key in column 0 under WCAG 2.2 SC 1.3.1? | depth           | H        | answered |
| Q2 | Why exactly does `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` fail at `test_safety_screens.py:130`, and how do peer specialist screen tests assert table headers? | depth           | H        | answered |
| Q3 | What downstream tests, browser checks, or UX baseline claims break under Option 1 (`rowHeader = false`) versus Option 2 (updating `test_safety_screens.py`)? | breadth         | H        | answered |
| Q4 | Is `test_safety_screens.py` subject to `scenario-manifest.json` SHA-256 pinning or special `ruff` / `mypy` exclusions in `src/api/pyproject.toml`?    | straightforward | M        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-15/wcag-baseline-151-research.md`, `.copilot-tracking/plans/2026-11-15/wcag-baseline-151-c2-plan.md`, `.copilot-tracking/rpi-sessions/2026-11-15/wcag-baseline-151-c2-state.json`, `docs/reference/research/ux/wcag-conformance-baseline.md`.
* Reused (verified) findings:
  * `scenario-manifest.json` hashes only `src/api/checks/workbench-manifest.json`, `src/api/checks/workbench_browser_check.py`, `src/core/tests/dataset.py`, and `src/api/tests/test_workbench.py` (`C9`).
  * Cycle 1 intentionally set `rowHeader = true` as the default in `role-screens.js:50` and documented in `wcag-conformance-baseline.md:54,150,156` that all 15 script-built table builders emit both `<th scope="col">` and `<th scope="row">` (`C5`).
* Superseded / stale:
  * Cycle 1 and Cycle 2 focused test runs checked `test_role_screens.py` and `test_housing_resident_wcag_232.py` without running `test_safety_screens.py`, leaving `test_safety_screens.py:129-133`'s legacy `all(t["attrs"] == {"scope": "col"} for t in find_all(table, "th"))` assumption unaligned with `rowHeader = true`.

## Research Cycle Log

### Cycle 1

* Active direction controls: Focused validation tier (`src/api` unit tests, `ruff`, `mypy`); no `tools/rpi-checks.py`; no remote push.
* Active research posture and completion basis: `focused`; complete inspection of all `screenTable` call sites, peer specialist WCAG test suites, browser checks, and UX baseline documentation.
* Explicit limits or deadline effect: None blocking; targeted reproduction completed in `3.8s`.

#### Wave 1: Wider

* Plan and independent lanes: Enumerate every `screenTable` and `screenRecordTable` call site across `src/api/`, locate all specialist screen table-header assertions across `src/api/tests/` and `src/api/checks/`, check `wcag-conformance-baseline.md` references to `screenTable` and `<th scope="row">`, and reproduce the exact failure across the 6 target test modules.
* Worker evidence relationships or inline fallback: Inline `grep`, `view`, and targeted `unittest` run establishing `C1`-`C6` and external rule reference `W1`.
* Reflection: `screenTable` has 19 direct call sites across `role-screens.js` (15) and `staff-intake.js` (4), plus 32 `screenRecordTable` call sites in `role-screens.js`. Across the 6 target test modules (`65` tests), `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` is the sole failure.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Inspect the exact column structures of the 3 safety-screen tables (`role-screens.js:1183,1190,1233`) and the remaining 16 direct `screenTable` call sites, inspect `test_safety_screens.py:118-135` and `test_safety_screens.py:302-316`, and compare how the 10 peer specialist screen WCAG test suites (`test_programme_screen_wcag.py`, `test_resident_choice_screen.py`, `test_housing_resident_wcag_232.py`, `test_technical_quality_screens_wcag.py`, `test_resident_service_screen.py`, `test_exception_register_screen.py`, `test_data_steward_screen_wcag.py`, `test_programme_coordinator_wcag_230.py`, `test_procurement_contractor_screen_wcag.py`, `test_finance_grants_screen_wcag.py`) and `role_screens_browser_check.py:293-310` validate table headers.
* Plan and independent lanes: Line-by-line inspection of `role-screens.js`, `staff-intake.js`, `test_safety_screens.py`, `test_finance_grants_screen_wcag.py`, `test_asset_board_screen.py`, `test_data_operator_screen.py`, and `role_screens_browser_check.py`.
* Worker evidence relationships or inline fallback: Inline inspection establishing `C2`, `C3`, `C4`, `C7`, `C8`.
  * All 3 safety-screen tables (`Hazard referrals for this home` with 10 columns starting with `Item` = `H-1`; `Scoped pause and release evidence` with 6 columns starting with `Item` = `H-1`; `Hazard referrals by home` with 13 columns starting with `Home and item` = `C-1 H-1`, `C-9`, `C-3`, `C-4`) use column 0 as the unique row-identifying label (`C2`). On 10- and 13-column tables, `<th scope="row">` on column 0 provides programmatic row context required by WCAG 2.2 SC 1.3.1 when navigating across status, timestamp, and owner cells.
  * All other 16 direct `screenTable` call sites (`Owner`, `Capability`, `Component`, `Measure`, `Home`, `Query`, `Input`, `Check`, `Step`, `Exception`, `Invoice line`, `Field`, `Grant`, `Event`, `Kind`) likewise place a row-identifying key in column 0 (`C3`).
  * `test_safety_screens.py:129-133` calls `find_all(table, "th")` across the entire `<table>` (mixing `<thead>` and `<tbody>`) and asserts every `<th>` has `{"scope": "col"}` and every `<tbody>` `<tr>` has `len(find_all(row, "td")) == len(heads)` (`C4`). In contrast, `role_screens_browser_check.py:299-302` and all 10 peer `test_*_wcag*.py` suites assert `<thead>` `<th>` cells have `scope="col"` and each `<tbody>` row begins with `<th scope="row">` followed by `<td>` cells (`C7`, `C8`).
* Reflection: Semantically and structurally, `rowHeader = true` in `role-screens.js:50` is right for every `screenTable` caller, especially the 10- and 13-column safety tables. Next, Wave 3 must challenge Option 1 and Option 2 for hidden regressions.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Test whether Option 1 (`rowHeader = false` in `role-screens.js:50`) is actually safe as suggested in the prompt's candidate note, and test whether Option 2 leaves any other assertions in `test_safety_screens.py` or `src/api/tests/` broken or weakened.
* Plan and independent lanes: Inspect `test_wcag_workbench_baseline_151.py:514-544`, `wcag-conformance-baseline.md:54,150,156`, `test_safety_screens.py:302-316`, and `src/api/pyproject.toml`.
* Worker evidence relationships or inline fallback: Inline contrarian audit (`C5`, `C6`, `C9`, `C10`) uncovered decisive counter-evidence against Option 1:
  1. **Option 1 directly breaks `test_wcag_workbench_baseline_151.py:527,537,542` (`C6`)**: Although the static check at `test_wcag_workbench_baseline_151.py:506` (`self.assertIn('scope: "row"', text)`) would still pass, the Node-VM runtime test at lines `527-542` calls `screenTable("Ready homes", ["Home", "Stage"], [["ZF-1", "Design"]])` with default `rowHeader` and evaluates `specialist.querySelector("tbody").querySelector("th").getAttribute("scope")`, asserting `["region", "Ready homes", "row"]`! Restoring `rowHeader = false` makes `querySelector("th")` return `null`, crashing the Node-VM check in `test_wcag_workbench_baseline_151.py`!
  2. **Option 1 contradicts `docs/reference/research/ux/wcag-conformance-baseline.md:54,150,156` (`C5`)**: Line 54 explicitly records `(screenTable in role-screens.js defaults rowHeader = true)` and lines 150 and 156 state all 15 builders emit `<th scope="row">`.
  3. **Option 2 preserves `test_safety_screens.py:311` and strengthens row-header verification (`C4`, `C10`)**: In `test_safety_screens.py:311`, `for cell in find_all(view, "td"):` checks non-empty leaves on remaining `<td>` cells (9, 5, and 12 per row) and already passes; updating `test_rendered_tables_are_labelled_focusable_and_aligned` (`lines 129-133`) to assert `(thead,) = find_all(table, "thead")`, `heads = find_all(thead, "th")` with `scope="col"`, and for each `<tbody>` row `row["kids"][0]` is `<th scope="row">` with non-empty text plus `<td>` cells for `row["kids"][1:]` summing to `len(heads)` makes the test strictly stronger than before while preserving `role-screens.js` and `wcag-conformance-baseline.md` unchanged.
  4. **Linter / type-checker coverage (`src/api/pyproject.toml`, `C10`)**: Unlike `test_accessibility_baseline.py`, `tests/test_safety_screens.py` is NOT excluded from default `ruff check .`, `ruff format --check .`, or `mypy` (`files = ["src", "tests", "checks"]`, `strict = true`, `line-length = 100`), so standard `ruff` and `mypy` enforce full strictness on `test_safety_screens.py`.
* Reflection: Contrarian wave decisively eliminates Option 1 and confirms Option 2 requires only a surgical 10-line update in `src/api/tests/test_safety_screens.py` with zero production JS or documentation churn.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition | Evidence-based rationale | Primary-artifact treatment |
|------------------|---------------------------------|--------------------|--------------------------|----------------------------|
| Option 2: Update `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py` to assert `<thead>` `<th scope="col">` and `<tbody>` leading `<th scope="row">` + `<td>` cells matching `len(heads)` | `C1-C10, W1` | accepted | Preserves WCAG 2.2 SC 1.3.1 row headers on 10- and 13-column safety tables, matches all 10 peer specialist WCAG suites and `role_screens_browser_check.py:300`, keeps `wcag-conformance-baseline.md:54` accurate, and keeps `test_wcag_workbench_baseline_151.py:527-542` passing | Selected recommendation for `rpi-plan` |
| Option 1: Restore `rowHeader = false` default in `function screenTable(...)` in `src/api/src/zava_forward/api/web/role-screens.js:50` | `C2, C3, C5, C6` | rejected | Breaks `test_wcag_workbench_baseline_151.py:527,537` (`null.getAttribute("scope")`), contradicts `wcag-conformance-baseline.md:54,150,156`, and removes `<th scope="row">` row headers from 19 multi-column specialist tables including `safety-lead` and `hazard-triage` | Recorded as rejected alternative |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Focused scope saturation — exact root cause, all 51 `screenTable`/`screenRecordTable` references, peer tests, baseline docs, and CI tool configs are verified.
* Revised brief or revalidation required: none
* Readiness effect: `Ready`

## Evidence Log

* Delegation: `inline: focused single-regression trace across role-screens.js, test_safety_screens.py, test_wcag_workbench_baseline_151.py, and wcag-conformance-baseline.md`

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | `screenTable` defaults `rowHeader = true` and emits `<th scope="row">` for column `0` of each `<tbody>` `<tr>` and `<td>` for columns `1..N-1` | `src/api/src/zava_forward/api/web/role-screens.js:50` | view | high | Lines `50-58` |
| C2 | `safety-lead` and `hazard-triage` render 3 multi-column tables (`Hazard referrals for this home` 10 cols, `Scoped pause and release evidence` 6 cols, `Hazard referrals by home` 13 cols) whose first column is the unique row identifier (`Item` `H-1` or `Home and item` `C-1 H-1`) | `src/api/src/zava_forward/api/web/role-screens.js:1183` | view | high | Also `role-screens.js:1190,1233` |
| C3 | All other 16 direct `screenTable` call sites across `role-screens.js` and `staff-intake.js` likewise place a row-identifying label (`Owner`, `Capability`, `Component`, `Measure`, `Home`, `Query`, `Input`, `Check`, `Step`, `Exception`, `Invoice line`, `Field`, `Grant`, `Event`, `Kind`) in column `0` | `src/api/src/zava_forward/api/web/role-screens.js:290` | grep / view | high | Also `role-screens.js:294,300,347,374,379,391,396,483,747,1902,1917,1957,2088,2141` and `staff-intake.js:80,81,153,159` |
| C4 | `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` queries `find_all(table, "th")` across both `<thead>` and `<tbody>`, failing at line 130 because `<tbody>` now contains `<th scope="row">`, and at line 133 expects `len(find_all(row, "td")) == len(heads)` | `src/api/tests/test_safety_screens.py:129` | view / bash | high | Lines `118-134`; reproduced via `unittest` |
| C5 | `wcag-conformance-baseline.md` explicitly records that all 15 script-built table builders emit `<th scope="col">` and `<th scope="row">` and states `(screenTable in role-screens.js defaults rowHeader = true)` | `docs/reference/research/ux/wcag-conformance-baseline.md:54` | grep / view | high | Also lines `150` and `156` |
| C6 | `test_wcag_workbench_baseline_151.py` invokes `screenTable("Ready homes", ["Home", "Stage"], [["ZF-1", "Design"]])` with default `rowHeader` in Node `vm` and asserts `specialist.querySelector("tbody").querySelector("th").getAttribute("scope") == "row"` | `src/api/tests/test_wcag_workbench_baseline_151.py:527` | view | high | Lines `527-542`; Option 1 would throw `TypeError` on `null` |
| C7 | Peer specialist WCAG unit suites validate `<thead>` `<th scope="col">` separately from `<tbody>` row-leading `<th scope="row">` | `src/api/tests/test_finance_grants_screen_wcag.py:73` | grep / view | high | Same pattern in `test_programme_screen_wcag.py:402-410`, `test_housing_resident_wcag_232.py:1117-1121`, `test_technical_quality_screens_wcag.py:549-556`, `test_data_steward_screen_wcag.py:706-713`, `test_procurement_contractor_screen_wcag.py:709-718` |
| C8 | Browser table-header contract `check_table_headers` enforces `tHead` `th.scope === "col"` and `tBodies[0]` `row.cells[0]` `<th scope="row">` | `src/api/checks/role_screens_browser_check.py:293` | view | high | Lines `293-309` |
| C9 | `scenario-manifest.json` SHA-256 bindings cover only `workbench-manifest.json`, `workbench_browser_check.py`, `dataset.py`, and `test_workbench.py`; `test_safety_screens.py` is unpinned | `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json:50` | view | high | No manifest digest churn |
| C10 | `src/api/pyproject.toml` includes `tests/test_safety_screens.py` in default `ruff check .`, `ruff format --check .` (`line-length = 100`), and strict `mypy` (`files = ["src", "tests", "checks"]`) | `src/api/pyproject.toml:25` | view | high | Full lint/format/type coverage applies automatically |

### External Evidence

| ID | Claim / finding | URL | Retrieved (`YYYY-MM-DD`) | Tool | Confidence | Notes |
|----|-----------------|-----|--------------------------|------|------------|-------|
| W1 | Vercel Web Interface Guidelines require semantic HTML `<table>` structure before ARIA so header-to-cell relationships are programmatically determinable | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` | 2026-11-15 | web_fetch | high | Supports WCAG 2.2 SC 1.3.1 `<th scope="col">` + `<th scope="row">` |

## Candidate Approaches and Recommendation

### Recommended Approach: Option 2 — Align `test_safety_screens.py` with Scoped Column and Row Headers

* Summary: Update `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py` (`lines 129-133`) to inspect `<thead>` `<th scope="col">` headers (`heads`) and verify that every `<tbody>` `<tr>` has a leading `<th scope="row">` cell (with non-empty string leaves) followed by `<td>` cells whose combined cell count equals `len(heads)`.
* Why selected:
  1. Preserves genuine WCAG 2.2 SC 1.3.1 `<th scope="row">` semantics across all 3 multi-column safety-screen tables (`10`, `6`, and `13` columns) and 16 other `screenTable` call sites (`C1`-`C3`, `W1`).
  2. Keeps `test_wcag_workbench_baseline_151.py:527-542` and `wcag-conformance-baseline.md:54,150,156` 100% consistent (`C5`, `C6`).
  3. Brings `test_safety_screens.py` into exact structural alignment with the 10 peer specialist screen WCAG suites and `role_screens_browser_check.py:293-309` (`C7`, `C8`).
* Files touched:
  * `src/api/tests/test_safety_screens.py` (modify `test_rendered_tables_are_labelled_focusable_and_aligned`)

### Alternative: Option 1 — Restore `rowHeader = false` Default in `role-screens.js`

* Approach: Change `function screenTable(..., rowHeader = true)` back to `rowHeader = false` at `src/api/src/zava_forward/api/web/role-screens.js:50`.
* Trade-offs: Makes `test_safety_screens.py:130` pass untouched, but breaks `test_wcag_workbench_baseline_151.py:527,537`, contradicts `wcag-conformance-baseline.md:54,150,156`, and strips `<th scope="row">` from 19 specialist data tables.
* Evidence refs: `C2`, `C3`, `C5`, `C6`
* Rejection rationale: Introduces an immediate regression in `test_wcag_workbench_baseline_151.py`, invalidates documented `#151` baseline claims, and weakens WCAG 2.2 SC 1.3.1 table semantics on 10- and 13-column safety tables.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Human screen-reader table-navigation verification remains a manual gate (`Not run`, `Refs #151`, `#155`).
* Follow-up: Existing ranked `#151` follow-ups remain valid (standalone `/law.html` skip link, Web Interface Guidelines `tabular-nums` / `Intl.NumberFormat` polish, and hosted runtime `a11y-runtime.config.json` probes).
* Residual uncertainty: none for this deterministic unit-test remediation.

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence IDs | Implications |
|----------|--------|----------------|-----------|--------------|--------------|
| Select Option 2: update `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py` to verify `<thead>` `<th scope="col">` and `<tbody>` `<th scope="row">` + `<td>` alignment | confirmed | Evidence / caller options | Preserves WCAG 2.2 SC 1.3.1 row headers, `test_wcag_workbench_baseline_151.py:527-542`, and `wcag-conformance-baseline.md:54` | `C1-C10, W1` | Zero web JS or KB markdown edits needed in `c3` |
| Preserve historical Cycle 1 and Cycle 2 `.copilot-tracking/` artifacts unchanged | confirmed | Repository governance | Original critique/Review records are immutable historical evidence | `C9` | Write separate `wcag-baseline-151-c3-*` artifacts |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Manual screen-reader table navigation sign-off | Named human tester walkthrough with NVDA/VoiceOver | Human tester / owner | Required before closing `#151` (`Refs #151` retained) | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Runtime Playwright `a11y-runtime.config.json` surface inventory across specialist role screens | Automates live-browser axe and focus-obscured probes in CI (`#155`) | Follow-up issue `#155` | deferred | `Q3; C8` |

## Planning Readiness

* Status: Ready
* Decision state: Converged on Option 2 (`src/api/tests/test_safety_screens.py` `test_rendered_tables_are_labelled_focusable_and_aligned` surgical update) with Focused validation (`unittest`, `ruff check .`, `ruff format --check .`, `mypy`).
* Evidence basis: `C1`-`C10`, `W1`
* Preconditions met: Failure reproduced (`1` failure out of `65` targeted tests), all `screenTable` call sites audited, contrarian check of Option 1 completed, lint/type config verified.
* Blockers: none
* Smallest action to change readiness: none (ready to transition to `Plan`).

## Closeout Record

| Field | Record |
|-------|--------|
| Research execution status | Complete |
| Completed waves | Cycle 1: Wider, Deeper, and Contrarian |
| Lane evidence or inline fallback | Inline across `role-screens.js`, `staff-intake.js`, `test_safety_screens.py`, `test_wcag_workbench_baseline_151.py`, peer `test_*_wcag*.py`, and `wcag-conformance-baseline.md` |
| Research disposition | executed |
| Planning Readiness | Ready (`C1`-`C10`, `W1`) |
| Blockers | none |
| Continuation owner and state | Confirmed automatic RPI Agent (`c3`); automatic continuation to `Plan` |

## Advisory Next Step

| Field | Record |
|-------|--------|
| Research disposition | executed |
| Planning Readiness | Ready (`C1`-`C10`, `W1`) |
| Output mode and planning support | `convergence`; yes — exact single-file test update and validation gates established |
| Acting owner | Confirmed automatic RPI Agent (`c3`) |
| Required gates or confirmations | Research disposition recorded (`passed`), Planning Readiness `Ready` (`passed`), 3 waves complete (`passed`), pre-transition state write (`pending -> Plan`) |
| Continuation result | Automatic continuation to `rpi-plan` |
| Primary evidence file | .copilot-tracking/research/2026-11-15/wcag-baseline-151-c3-research.md |
| Notes for planning or re-entry | Single implementation phase updating `test_safety_screens.py` lines `129-133`, running the 6 requested unit test suites plus `ruff check .`, `ruff format --check .`, and `mypy`, and executing one-pass `rpi-plan-critique`. |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: Focused scope saturated across all `screenTable` callers and specialist test suites.

## Sources

* Codebase: `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/staff-intake.js`, `src/api/tests/test_safety_screens.py`, `src/api/tests/test_wcag_workbench_baseline_151.py`, `src/api/tests/test_finance_grants_screen_wcag.py`, `src/api/checks/role_screens_browser_check.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`, `src/api/pyproject.toml`.
* External: Vercel Web Interface Guidelines (`W1`, retrieved 2026-11-15).

## Self-Check

* [x] Research Brief, Parameters, Extension Registry, Direction Controls, and Prior Knowledge Gate completed.
* [x] Cycle 1 completed Wider, Deeper, and Contrarian waves in order with explicit reflection and parent disposition.
* [x] Every codebase finding cites a workspace-relative `path:line` (`C1`-`C10`) and external source cites URL + retrieval date (`W1`).
* [x] Zero production/source/test files were edited during Research.
* [x] Planning Readiness (`Ready`) and Research disposition (`executed`) are recorded consistently.
