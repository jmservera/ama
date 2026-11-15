<!-- markdownlint-disable-file -->
# RPI Plan Critique: Pass Node Test Payloads via Stdin and Trim Redundant Nomination Panel Formatting

## Metadata

* Task ID: nomination-api-routes-130-c3
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c3-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Single-pass final-candidate critique for Issue #130 Cycle 3 (`nomination-api-routes-130-c3`) on open PR #1776 active branch `feat/ux-130-api-routes` in worktree `/home/azureuser/source/ama-demo-wt/feat-130-api-routes`. On PR #1776 (`f53340e8f`), 9/10 CI checks passed and only `test_case_journey.CaseJourney.test_quality_errors_and_manual_action_pending_siblings` (`src/api/tests/test_case_journey.py` line 1040) failed with `OSError: [Errno 7] Argument list too long: 'node'` (`E2BIG`) when concatenated JavaScript exceeded Linux `MAX_ARG_STRLEN` (`131,072` bytes) on `argv`. Caller requires passing `script` via `stdin` (`["node", "-"]` and `["node", "--unhandled-rejections=strict", "-"]` with `input=...`) across `src/api/tests/test_case_journey.py`, trimming redundant comments/whitespace in `src/api/src/zava_forward/api/web/panels.js` without behavioral change, running Focused Tier verification (`unittest` on `tests/test_case_journey.py` and `tests/test_accessibility_baseline.py -v`, plus `ruff check .`, `ruff format --check .`, and `mypy`) from `src/api`, preserving all `c1` and `c2` `.copilot-tracking/` artifacts unchanged, and committing cleanly on `feat/ux-130-api-routes` with the Copilot `Co-authored-by` trailer without pushing.
* Research and evidence considered: `.copilot-tracking/research/2026-11-15/nomination-api-routes-130-c3-research.md` (`C1` to `C8`, `W1`), `.copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c3-plan.md`, `.copilot-tracking/details/2026-11-15/nomination-api-routes-130-c3-phase-details.md`, `src/api/tests/test_case_journey.py`, `src/api/src/zava_forward/api/web/panels.js`, `src/api/tests/test_nomination_screen.py`, `src/api/tests/test_epic149_form_error_summary_associations.py`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_content_standard.py`, `src/api/tests/test_ux_design_traceability.py`, `src/api/tests/test_challenge_non_retaliation_hazard_guard.py`, and read-only Git branch/diff state against `origin/feat/demo-233-same-home-tensions-0825` (`50bd5acc0`).
* Decisions, dependencies, and acceptance criteria considered: Uniform conversion of all 22 `subprocess.run` Node invocations in `src/api/tests/test_case_journey.py` from `-e <script>` on `argv` to `"-"` with `input=...` while preserving module exports (`DOM`, `WEB`, `shipped_helpers`) imported by `src/api/tests/test_safety_panel_ux.py`; locked test ownership (`0` removals, `1` deterministic `>131,072`-byte regression test addition `test_node_stdin_handles_scripts_above_linux_max_arg_strlen`); scoping `panels.js` conciseness edits strictly inside `#130` helpers (`function nominationPanel` through `\nfunction affectedChallengePanel`, disjoint from `50bd5acc0` edits in `actForm` and `residentPanel`); preserving Epic #149 (`9` `aria-invalid` sites, `±4`-line `input.focus()` window, `tabindex: -1`), slice markers, plain-language copy rules, and Web Interface Guidelines (`W1`); Focused Tier `PYTHONPATH` isolation (`PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests`); and clean local commit hygiene without remote push.
* Assessment boundary: Evaluates causal completeness, target/line-boundary accuracy, cross-test static invariants, merge disjointness, and Focused Tier validation sufficiency from supplied artifacts and read-only source inspection; does not mutate files, run test suites, or push commits.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Req 1a, Research `C1` to `C5`, `P01`, `P01-T01` (Convert all 22 `node -e` calls in `test_case_journey.py` to `stdin`) | Covered | Verified in `src/api/tests/test_case_journey.py` that exactly 22 `subprocess.run` calls invoke `node` (`evaluate()` at line 96 with `check=True`, 19 standard `["node", "-e", script]` calls including line 1040, 2 `timeout=30` / 2 `check=True` standard variants, and 1 `["node", "--unhandled-rejections=strict", "-e", script]` call at line 1169), while `test_safety_panel_ux.py:7` imports `DOM, WEB, shipped_helpers`. Passing `"-"` with `input=...` eliminates `execve` `MAX_ARG_STRLEN` (`131,072`-byte) failures across the entire module. |
| Caller Req 1a, Research `C1` to `C3`, `C6`, `P01-T02` (`>131,072`-byte `MAX_ARG_STRLEN` regression test) | Covered | Because standalone `HEAD` (`f53340e8f`) sits at `129,031` bytes (`2,041` bytes below `131,072` prior to merging `50bd5acc0`), padding `DOM + shipped_helpers() + ops.js + panels.js` past `131,072` UTF-8 bytes in `test_node_stdin_handles_scripts_above_linux_max_arg_strlen` directly reproduces and guards the CI merge-checkout failure boundary within locked test ownership (`0` removals, `1` addition) and does not affect `test_ux_design_traceability.py`. |
| Caller Req 1b, Research `C6` to `C8`, `W1`, `P02`, `P02-T01` (Behavior-preserving conciseness trim in `panels.js`) | Covered | Read-only `git diff HEAD...origin/feat/demo-233-same-home-tensions-0825` confirms `50bd5acc0` touches only `actForm` and `residentPanel` (hunks ending before line 315 on `HEAD`), completely disjoint from `function nominationPanel` (`line 316`) through `nominationPanel._routeForm` (`line 754`, immediately above `function affectedChallengePanel` on `line 756`). Scoping formatting and shared `assisted_channel` option extraction strictly inside that slice preserves all `test_nomination_screen.py` and `test_case_journey.py:684` slice markers, Epic #149 invariants, and `W1` accessibility semantics. |
| Caller Req 2, Research `C5`, `C7`, `C8`, `P03`, `P03-T01` (Focused Tier `unittest`, `ruff`, and `mypy` verification from `src/api`) | Covered | `P03-T01` executes `tests/test_case_journey.py` and `tests/test_accessibility_baseline.py -v`, coupled `test_nomination_screen.py`, `test_nomination_api_routes.py`, `test_epic149_form_error_summary_associations.py`, `test_content_standard.py`, and `test_safety_panel_ux.py`, plus `python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy` from `src/api` using worktree-local `PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests` without mutating shared `site-packages`. |
| Caller Req 3 (Preserve `c1`/`c2` tracking files, local commit on `feat/ux-130-api-routes`, no push) | Covered | `git status --short` confirms only new untracked `-c3-` artifacts exist on `feat/ux-130-api-routes`, all `-130-`, `-ci-fix-`, and `-c2-` tracking files remain untouched, and plan acceptance criteria enforce privacy-safe `gh api user` email configuration, `Refs #130`, the Copilot `Co-authored-by` trailer, and no remote push. |

## Verdict

* Verdict: Pass
* Rationale: `.copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c3-plan.md` and `.copilot-tracking/details/2026-11-15/nomination-api-routes-130-c3-phase-details.md` accurately diagnose the `MAX_ARG_STRLEN` (`131,072`-byte) CI merge-checkout failure on PR #1776, cover all 22 `subprocess.run` Node sites in `src/api/tests/test_case_journey.py` plus deterministic `>131,072`-byte regression proof, bound `panels.js` conciseness edits cleanly inside `#130`-owned nomination helpers away from `50bd5acc0`, and specify complete Focused Tier validation and Git safeguards, leaving `0` actionable `PC-xxx` findings.

## Findings

* None (`0` actionable findings).

## Strengths and Residual Risk

* Complete `E2BIG` elimination with standalone regression proof: Converting all 22 `subprocess.run` Node sites in `src/api/tests/test_case_journey.py` to `stdin` (`"-"`, `input=...`) and asserting `len(script.encode("utf-8")) > 131_072` in `test_node_stdin_handles_scripts_above_linux_max_arg_strlen` removes `argv` length sensitivity permanently across `ops.js`, `panels.js`, `app.js`, `assistants.js`, and `chat.js`.
* Implementation detail note for `P01-T01` (non-blocking): In `src/api/tests/test_case_journey.py:94`, `def evaluate(expression: str) -> Any:` takes a single `expression: str` parameter (reading `source = (WEB / "case-workspace.js").read_text()` internally) and passes `check=True` to `subprocess.run`; keep that exact 1-argument signature and `check=True` kwarg when replacing `"-e", source + ...` with `"-"`, `input=source + ...` (matching the `P01-T01` Context rule to preserve per-call kwargs).
* Implementation detail note for `P02-T01` (non-blocking): On current `HEAD`, `src/api/src/zava_forward/api/web/panels.js` lines `316` to `754` contain `0` inline `//` comments (`line 315` holds the single function doc comment above `function nominationPanel`), so conciseness savings come from sharing the repeated `assisted_channel` options/predicate across `ackForm` and `corrForm` and compacting expanded multiline field descriptors; also keep `panelOwned(` on the same source line as its message literal and `error.message` (`lines 727, 735, 744, 745`) so `test_content_standard.py` line-scoped `panelOwned(` checks continue to pass.
* Explicitly accepted post-session residual risk: Because remote push is prohibited inside this session, hosted GitHub Actions verification of `refs/pull/1776/merge` (`10/10` green checks with `50bd5acc0`), independent exact-head review, and governance items `OD-41`/`OD-42` remain owner follow-ups after Cycle 3 commits locally.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Critique is strictly read-only; live execution of the 22 converted Node `stdin` calls, the `>131,072`-byte regression test, and the `src/api` Focused Tier suites (`unittest`, `ruff`, `mypy`) occurs during `P01` through `P03` in `rpi-implement`.

## Recommended Next Action

* Highest-impact finding: none
* Action owner: none
* Smallest next action: Finalize planning status on `.copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c3-plan.md` (`Critique Disposition` and `Planning status: complete`) and advance directly to `rpi-implement` starting at `P01` (`P01-T01`).
* User response required: no
