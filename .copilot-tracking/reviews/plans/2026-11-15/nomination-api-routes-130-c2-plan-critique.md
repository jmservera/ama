<!-- markdownlint-disable-file -->
# RPI Plan Critique: Rebase Issue 130 Branch and Fix Refusal Feedback Focus-Blur Clearing

## Metadata

* Task ID: nomination-api-routes-130-c2
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c2-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Single-pass final-candidate critique for Issue #130 Cycle 2 (`nomination-api-routes-130-c2`) on open PR #1776 active branch `feat/ux-130-api-routes` targeting stacked parent `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`, PR #1639) under Focused Tier validation (targeted unit suites, `src/api/checks/case_journey_browser_check.py`, `ruff`, and `mypy`, with `tools/rpi-checks.py` and remote push explicitly prohibited).
* Research and evidence considered: .copilot-tracking/research/2026-11-15/nomination-api-routes-130-c2-research.md (`C1` to `C7`, `W1`), .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c2-plan.md, .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c2-phase-details.md, `src/api/src/zava_forward/api/web/panels.js` (`bindCaseMutationForm`, `nominationPanel`, `nominationPanel._routeForm`, `affectedChallengePanel`), `src/api/checks/case_journey_browser_check.py` (`mutation_reconstruction`), `src/api/tests/test_nomination_screen.py`, and read-only Git branch/diff state between merge-base `a1d0be5f6`, `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`), and `HEAD` (`2786009ee`).
* Decisions, dependencies, and acceptance criteria considered: Branch reuse of `feat/ux-130-api-routes` without rename or push; conflict-free rebase onto `6510b6fbc`; scoping `addEventListener("change", clearInvalid)` in `nominationPanel._routeForm` strictly to `<select>` controls (`isSelect: Boolean(options)`) while keeping `addEventListener("input", clearInvalid)` on all controls; locked test ownership (`0` removals, `1` deterministic Node regression test addition in `src/api/tests/test_nomination_screen.py`); static accessibility/content invariants (`9` `aria-invalid` sites, `14` tables, Epic #149 focus windows, `W1` polite live status preservation); Focused Tier command execution without `tools/rpi-checks.py`; and clean post-review local commit with privacy-safe email `8036360+jmservera@users.noreply.github.com`, `Refs #130`, and the Copilot `Co-authored-by` trailer.
* Assessment boundary: Evaluates completeness, causal accuracy, file/slice boundaries, rebase safety, and validation coverage from the supplied research, plan, phase details, and read-only repository verification; does not execute mutations, browser runs, `tools/rpi-checks.py`, or remote Git operations.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Research `C6`, `P01`, `P01-T01` (Rebase onto `6510b6fbc`) | Covered | Verified `git status --short --untracked-files=no` is empty, untracked `-c2-` files under `.copilot-tracking/` do not collide with any tracked path in `a1d0be5f6..6510b6fbc` or `a1d0be5f6..2786009ee`, and `src/api/src/zava_forward/api/web/app.js` is the sole shared file with disjoint hunks. |
| Research `C1` to `C5`, `C7`, `W1`, `P02`, `P02-T01` (`_routeForm` `<select>` listener guard) | Covered | Verified in `src/api/src/zava_forward/api/web/panels.js` (`lines 30-37`, `595-623`, `654-665`, `741-751`) that `options` is truthy if and only if the control is `h("select", ...)`, all `showWhen` predicates depend solely on `<select>` fields (`channel`, `raised_by`), and restricting `"change"` to `isSelect: Boolean(options)` prevents synchronous `status.focus()` blur on `#challenge-open-request` (`src/api/checks/case_journey_browser_check.py:456`) from wiping `mutation.message` while preserving Epic #149 invariants and `affectedChallengePanel` slice markers. |
| Research `C2`, `C3`, `C5`, `P02-T02` (Node focus-blur regression test) | Covered | `src/api/tests/test_nomination_screen.py` currently evaluates `panels.js` without active-element blur-to-`"change"` simulation; adding `1` regression test (`test_route_form_blur_change_preserves_refusal_message_while_input_and_select_clear`) satisfies locked test ownership (`0` removals, max `1` addition) and proves both refusal preservation on `<input>` blur `"change"` and clearing/visibility updates on `"input"` and `<select>` `"change"`. |
| Caller Focused Tier boundary, `P03`, `P03-T01` (Targeted unit, browser, lint, and type checks) | Covered | `P03-T01` runs all caller-specified `src/core` and `src/api` unit suites, coupled `test_case_journey.py` (with `src/core` on `PYTHONPATH` for `tests.test_mvp`), `test_content_standard.py`, `test_epic149_form_error_summary_associations.py`, rebased parent `test_programme_coordinator_wcag_230.py`, end-to-end `src/api/checks/case_journey_browser_check.py`, `ruff check`, `ruff format --check`, and `mypy`, while honoring the prohibition on `tools/rpi-checks.py` and remote push. |
| Local Git hygiene and Cycle 2 artifact preservation | Covered | Plan acceptance criteria preserve existing `.copilot-tracking/` files, keep `.copilot-tracking/` paths out of production/test code and commit messages, and defer the final local commit until all Cycle 2 artifacts are written so `git status --short` ends empty without push. |

## Verdict

* Verdict: Pass
* Rationale: Every requirement, causal link, rebase precondition, static accessibility guard, and Focused Tier validation command in `.copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c2-plan.md` and `.copilot-tracking/details/2026-11-15/nomination-api-routes-130-c2-phase-details.md` verified cleanly against `src/api/src/zava_forward/api/web/panels.js`, `src/api/checks/case_journey_browser_check.py`, `src/api/tests/test_nomination_screen.py`, and local Git ancestry, yielding `0` actionable `PC-xxx` findings.

## Findings

* None (`0` actionable findings).

## Strengths and Residual Risk

* Exact causal parity: Guarding `input.addEventListener("change", clearInvalid)` behind `isSelect: Boolean(options)` in `nominationPanel._routeForm` fixes both the synchronous `status.focus()` blur during `mutation_reconstruction` (`family == "challenge"`, `outcome == "refusal"`) and manual keyboard `Tab` blur on `<input type="text">`, `<input type="date">`, and `<textarea>`, while leaving `bindCaseMutationForm` and all `<select>` `showWhen` transitions intact.
* Implementation slice note for `P02-T02` (non-blocking): When constructing the Node `eval` harness in `src/api/tests/test_nomination_screen.py` for `panelOwned` + `bindCaseMutationForm` + `nominationPanel._routeForm`, slicing the header block from `const panelOwned` through the end of `bindCaseMutationForm` (`src/api/src/zava_forward/api/web/panels.js` lines `7-41`) naturally includes `const PANEL_SUPPORT` (`line 15`), which `nominationPanel._routeForm` references in its `catch` branch (`lines 744-745`).
* Accepted residual risk on remote publication: Rebasing `feat/ux-130-api-routes` onto `6510b6fbc` rewrites local commit SHAs `2215209cb` and `2786009ee`; owner-authorized `git push --force-with-lease` and hosted GitHub Actions verification on PR #1776 remain explicit post-review follow-ups outside the caller's no-push boundary.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Critique is strictly read-only on repository code and Git refs; live execution of `git rebase`, the Node unit regression test, and headless-Chromium `src/api/checks/case_journey_browser_check.py` belongs to `P01` through `P03` in `rpi-implement`.

## Recommended Next Action

* Highest-impact finding: none
* Action owner: none
* Smallest next action: Finalize planning status on `.copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c2-plan.md` and proceed directly to `rpi-implement` starting at `P01` (`P01-T01`).
* User response required: no
