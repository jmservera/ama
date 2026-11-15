<!-- markdownlint-disable-file -->
# RPI Plan Critique: Focused Cycle 3 Safety-Screen Table Header Remediation for PR #1802 (#151)

## Metadata

* Task ID: 2026-11-15-wcag-baseline-151-c3
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/wcag-baseline-151-c3-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Remediate the single `PR #1802` (`feat/ux-151-wcag-baseline`, Issue `#151`) `src-api` CI failure (`1` of `3,612` tests) in `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` at `src/api/tests/test_safety_screens.py:130` caused by `function screenTable(..., rowHeader = true)` at `src/api/src/zava_forward/api/web/role-screens.js:50`; execute Focused validation (`6` specified `src/api` `unittest` suites plus `ruff check .`, `ruff format --check .`, and `mypy` in `src/api`) without running `tools/rpi-checks.py`; persist dated `c3` `.copilot-tracking/` artifacts while preserving Cycle 1 and Cycle 2 artifacts; and commit locally with the Copilot trailer without pushing.
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-c3-plan.md, .copilot-tracking/details/2026-11-15/wcag-baseline-151-c3-phase-details.md, .copilot-tracking/research/2026-11-15/wcag-baseline-151-c3-research.md (`C1`-`C10`, `W1`), src/api/tests/test_safety_screens.py, src/api/src/zava_forward/api/web/role-screens.js, src/api/tests/test_wcag_workbench_baseline_151.py, docs/reference/research/ux/wcag-conformance-baseline.md, src/api/pyproject.toml.
* Decisions, dependencies, and acceptance criteria considered: Confirmed selection of Option 2 (update `test_safety_screens.py` table assertions rather than reverting `rowHeader = true` in `role-screens.js`), Locked Test Ownership and Bounds (`src/api/tests/test_safety_screens.py` only, `0` test removals, `0` new test methods/files), sequential dependency `P01-T01 -> P01-T02`, Focused validation command gates, immutable Cycle 1 and Cycle 2 `.copilot-tracking/` evidence, and local commit rules (`Refs #151, #119`, privacy-safe local Git email, Copilot trailer, no push).
* Assessment boundary: Evaluates plan and phase-detail credibility, semantic correctness, typing/lint compliance, regression blast radius, and governance alignment from supplied files only. Does not execute unit tests, linters, `tools/rpi-checks.py`, browser checks, or Git commands.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Option 2 selection (`C1`-`C8`, `W1`) | Covered | `src/api/src/zava_forward/api/web/role-screens.js:50,1183,1190,1233` confirms all three safety tables (`10`, `6`, and `13` columns) place unique row identifiers (`H-1`, `C-1 H-1`, `C-9`, `C-3`, `C-4`) in column `0`. Option 1 would crash `src/api/tests/test_wcag_workbench_baseline_151.py:527-542` (`querySelector("th")` returning `null`) and contradict `docs/reference/research/ux/wcag-conformance-baseline.md:54`. |
| `P01` / `P01-T01` (`test_safety_screens.py` header and cell alignment update) | Covered | `src/api/tests/test_safety_screens.py:118-134` currently calls `find_all(table, "th")` across the whole table and expects `len(find_all(row, "td")) == len(heads)`. `P01-T01` separates `(thead,) = find_all(table, "thead")` (`scope="col"`) from `(tbody,) = find_all(table, "tbody")` rows, verifying leading `<th scope="row">` with non-empty stripped `string_leaves(...)` plus `<td>` cells for `row["kids"][1:]` summing to `len(heads)`, matching the `h(...)`, `find_all(...)`, and `string_leaves(...)` helpers at `src/api/tests/test_safety_screens.py:18-20,97-115,311-313`. |
| Locked Test Ownership and Bounds | Covered | Constrains edits strictly to `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py` with `0` test removals and `0` added test methods or files, and `C9` confirms `test_safety_screens.py` is not SHA-256-pinned in `scenario-manifest.json`. |
| `P01-T02` (Focused validation gates and `C10` lint/type strictness) | Covered | Includes exact caller commands for the six `unittest` modules (`65` tests) and `(cd src/api && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy)`. `src/api/pyproject.toml:24-60` confirms `tests/test_safety_screens.py` is subject to `line-length = 100`, `ruff format`, and `mypy` `strict = true`, which `P01-T01` and `P01-T02` explicitly enforce while excluding `tools/rpi-checks.py`. |
| Cycle 3 artifact retention and local commit handoff | Covered | Scope, Non-Goals, Non-Functional Requirements, and Acceptance Criteria preserve Cycle 1 and Cycle 2 `.copilot-tracking/` files unchanged, require dated `c3` tracking records, retain `Refs #151, #119` (no conformance claim), and mandate a local commit on `feat/ux-151-wcag-baseline` with privacy-safe local `user.email` and the Copilot trailer without pushing. |

## Verdict

* Verdict: Pass
* Rationale: The candidate Cycle 3 plan and phase details accurately isolate and resolve the sole `PR #1802` `src-api` failure (`src/api/tests/test_safety_screens.py:130`). Selecting Option 2 is thoroughly justified by `wcag-baseline-151-c3-research.md` (`C1`-`C10`, `W1`), direct inspection of `role-screens.js:50,1183-1235`, `test_wcag_workbench_baseline_151.py:527-542`, and `wcag-conformance-baseline.md:54`. `P01-T01` specifies exact, type-safe assertions compatible with `test_safety_screens.py`'s existing AST helpers and `src/api/pyproject.toml`'s Ruff and strict Mypy rules, and `P01-T02` plus the plan acceptance criteria honor every caller validation, retention, and non-push constraint.

## Findings

* None (`Critical: 0`, `High: 0`, `Medium: 0`, `Low: 0`). No substantive planning gaps, contradictions, or missing evidence were identified within the supplied boundary.

## Strengths and Residual Risk

* Surgical scope and semantic fidelity: Updating `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` preserves WCAG 2.2 SC 1.3.1 `<th scope="row">` row headers across the `10`-, `6`-, and `13`-column safety referral tables and `16` peer `screenTable` call sites, avoids breaking `test_wcag_workbench_baseline_151.py:527-542`, and avoids churn to `role-screens.js` or `wcag-conformance-baseline.md`.
* Strengthened column-0 text check: Because `test_rendered_views_have_no_role_simulator_and_states_are_text` (`src/api/tests/test_safety_screens.py:311-313`) iterates `find_all(view, "td")` for non-empty text leaves, `P01-T01`'s explicit check for non-empty stripped `string_leaves(row["kids"][0]["kids"])` on each leading `<th scope="row">` ensures column `0` (`Item` / `Home and item`) retains non-empty text coverage across both `screen["tree"]` and `screen["summary"]` (including fallback unavailable/unknown/mismatch rows).
* Explicitly accepted residual risk (Focused local validation): Running the `6` caller-specified `unittest` suites (`65` tests) rather than all `3,612` `src/api` unit tests or `tools/rpi-checks.py` locally is explicitly directed by the caller and carries negligible regression risk because `src/api/tests/test_safety_screens.py` is the only code file modified and hosted `PR #1802` `src-api` CI already passed the remaining `3,611` tests.
* Explicitly accepted residual risk (human AT verification): Automated Node-VM and static checks do not establish screen-reader or zoom conformance; the plan properly retains `Refs #151, #119` and tracks manual walkthroughs (`#155`) as follow-up items.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* This critique is a read-only static evaluation of the supplied Cycle 3 artifacts and referenced repository files; test execution, Ruff/Mypy verification, and local Git state verification belong to `rpi-implement` (`P01-T02`), `rpi-review`, and parent closeout.

## Recommended Next Action

* Highest-impact finding: none
* Action owner: planning_parent
* Smallest next action: Finalize `.copilot-tracking/plans/2026-11-15/wcag-baseline-151-c3-plan.md` (`Planning status: finalized`, update `Latest critique` and `Critique Disposition` with this `Pass` verdict) and advance directly to `rpi-implement` (`P01-T01` and `P01-T02`).
* User response required: no
