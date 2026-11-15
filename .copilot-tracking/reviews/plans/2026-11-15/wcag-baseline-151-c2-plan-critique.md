<!-- markdownlint-disable-file -->
# RPI Plan Critique: Focused Cycle 2 Correction for Workbench WCAG 2.2 Baseline (#151)

## Metadata

* Task ID: 2026-11-15-wcag-baseline-151-c2
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/wcag-baseline-151-c2-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Focused Cycle 2 (`c2`) RPI correction on branch `feat/ux-151-wcag-baseline` for issue `#151` to (1) shrink `NO_SKIP_LINK` in src/api/tests/test_epic149_landmarks_skip_link_focus_order.py from `{"/", "/law.html"}` to `{"/law.html"}` following the `.skip-link` addition in src/api/src/zava_forward/api/web/welcome.html, (2) format src/api/tests/test_accessibility_baseline.py and src/api/tests/test_wcag_workbench_baseline_151.py with `python3 -m ruff format --isolated --line-length 100`, (3) run the three targeted `unittest` suites and `(cd src/api && python3 -m ruff check src tests)`, and (4) record Cycle 2 `.copilot-tracking/` `changes` and `reviews` artifacts and commit locally on `feat/ux-151-wcag-baseline` with the Copilot trailer without pushing.
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-c2-plan.md, .copilot-tracking/details/2026-11-15/wcag-baseline-151-c2-phase-details.md, src/api/tests/test_epic149_landmarks_skip_link_focus_order.py, src/api/tests/test_accessibility_baseline.py, src/api/tests/test_wcag_workbench_baseline_151.py, src/api/tests/test_epic149_form_error_summary_associations.py, src/api/src/zava_forward/api/web/welcome.html, src/api/pyproject.toml.
* Decisions, dependencies, and acceptance criteria considered: Focused validation tier; zero web runtime or src/api/pyproject.toml edits; preservation of historical Cycle 1 `.copilot-tracking/` artifacts; zero test additions or removals; local-only commit using `Refs #151, #119` (since manual AT/zoom walkthroughs and owner confirmation `O-1` remain open) with the Copilot trailer.
* Assessment boundary: Static evidence verification of the candidate Cycle 2 plan and phase details against the six supplied repository files and caller constraints. This critique does not execute test suites, mutate source files, or inspect git history beyond supplied read-only inputs.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Caller Req 1 (`NO_SKIP_LINK` shrink to `{"/law.html"}`) | Covered | Verified at src/api/src/zava_forward/api/web/welcome.html (lines 10 and 15 add `<a class="skip-link" href="#welcome-main">` and `<main id="welcome-main" ... tabindex="-1">`, with one `<header>` and no `<nav>`) and src/api/tests/test_epic149_landmarks_skip_link_focus_order.py (lines 29-30 and 160-163). Shrinking `NO_SKIP_LINK` to `{"/law.html"}` while keeping `NO_NAV = {"/", "/law.html"}` aligns all 14 tests in the module. |
| Caller Req 2 (`ruff format --isolated --line-length 100`) | Covered | Verified against src/api/pyproject.toml (lines 42-48 exclude `tests/test_accessibility_baseline.py` from default `ruff format`, whereas `--isolated` formats it), src/api/tests/test_accessibility_baseline.py (line 102 is 106 columns), and src/api/tests/test_epic149_form_error_summary_associations.py (line 120 asserts `"self.assertEqual(sites, 9," in BASELINE_TEST.read_text()`). Extracting `invalid_msg` keeps `self.assertEqual(sites, 9, invalid_msg)` at 47 columns so 100-column formatting preserves the cross-file invariant. |
| Caller Req 3 (Targeted `unittest` suites and `ruff check`) | Covered | `P01-T02` includes all four caller-specified commands verbatim plus coupled `test_epic149_*.py`, `ruff format --isolated --line-length 100 --check`, and `mypy`. |
| Caller Req 4 (Cycle 2 `.copilot-tracking/` artifacts and local commit) | Covered | Acceptance criteria, non-functional requirements, and `Implementation Context Record` preserve Cycle 1 artifacts untouched, assign `.copilot-tracking/changes/2026-11-15/wcag-baseline-151-c2-changes.md` to `rpi-implement` followed by Cycle 2 review evidence, and require a local no-push commit on `feat/ux-151-wcag-baseline` with `Refs #151, #119` and the Copilot trailer. |
| Locked Test Ownership and Bounds | Covered | Canonical targets match the exact three test files with `0` test removals and `0` new test methods. |
| P01 / P01-T01 (Baseline fix and isolated formatting) | Covered | Target files, boundaries, line-length mechanics, and `--check` verification are concrete and conflict-free with `ruff check` and `mypy` rules in src/api/pyproject.toml. |
| P01 / P01-T02 (Focused validation) | Covered | Depends on `P01-T01`, runs every caller-mandated and tightly coupled check, and verifies Cycle 1 tracking files remain unmodified before commit. |

## Verdict

* Verdict: Pass
* Rationale: Every requirement, file target, line-level assumption, cross-test invariant, and validation command in the Cycle 2 plan and phase details is directly verified against the supplied repository evidence. No actionable planning gaps or ungrounded assumptions exist.

## Findings

No actionable `PC-xxx` findings (`0` Critical, `0` High, `0` Medium, `0` Low).

## Strengths and Residual Risk

* Accurate root-cause and invariant analysis: The plan verifies both why `SkipLink.test_skip_link_gaps_are_recorded_and_shrink_only` failed (`"/"` remained in `NO_SKIP_LINK` after src/api/src/zava_forward/api/web/welcome.html gained `.skip-link`) and why `NO_NAV` must remain `{"/", "/law.html"}`.
* Proactive prevention of a secondary formatting regression: The plan catches that `--isolated` overrides `[tool.ruff.format] exclude` in src/api/pyproject.toml and would wrap line 102 of src/api/tests/test_accessibility_baseline.py, breaking `FormErrorAssociations.test_counted_baseline_is_unchanged_and_fully_mapped` in src/api/tests/test_epic149_form_error_summary_associations.py unless the message literal is extracted first.
* Residual risk (accepted, low): Because src/api/pyproject.toml remains out of scope, `tests/test_accessibility_baseline.py` stays listed in `[tool.ruff.format] exclude` until the `#199` exemption cleanup follow-up; `P01-T01` explicitly validates formatting with `ruff format --isolated --line-length 100 --check`, and `--isolated --line-length 100` matches the `[tool.ruff]` 100-column formatting behavior on non-excluded `test_wcag_workbench_baseline_151.py` and `test_epic149_landmarks_skip_link_focus_order.py`.
* Residual risk (accepted, orchestration boundary): `P01` covers implementation and validation (`rpi-implement` writes `wcag-baseline-151-c2-changes.md`); the active Cycle 2 RPI loop still owns executing `rpi-review` (`wcag-baseline-151-c2-review.md`) and verifying repository-local privacy-safe Git `user.email` configuration before creating the local no-push commit with the Copilot trailer.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Single-pass static critique bounded to the supplied plan, phase details, and six read-only repository files; runtime test execution and post-implementation review verification occur in `rpi-implement` and `rpi-review`.

## Recommended Next Action

* Highest-impact finding: none
* Action owner: planning_parent
* Smallest next action: Finalize the Cycle 2 plan from `candidate` status and proceed to `rpi-implement` (`P01-T01` and `P01-T02`) in the active RPI loop.
* User response required: no
