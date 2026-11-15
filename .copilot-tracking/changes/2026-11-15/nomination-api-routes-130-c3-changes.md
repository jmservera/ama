<!-- markdownlint-disable-file -->
# RPI Changes: Pass Node Test Payloads via Stdin and Trim Redundant Nomination Panel Formatting

## Metadata

* Task ID: nomination-api-routes-130-c3
* Related plan: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c3-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full_plan
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01, P03, P03-T01
* All remaining active-plan markers: none
* Status basis: All planned phases and tasks (`P01`, `P02`, `P03`) completed with verified Focused Tier unit, WCAG 2.2 baseline, Epic #149, content-standard, 3-way merge, Ruff, and Mypy evidence.

## Execution Summary

Converted all 22 `subprocess.run` Node invocations in `src/api/tests/test_case_journey.py` from `-e <script>` on `argv` to `stdin` (`["node", "-"]` and `["node", "--unhandled-rejections=strict", "-"]` with `input=...`), added `test_node_stdin_handles_scripts_above_linux_max_arg_strlen` verifying clean execution above Linux's `131,072`-byte `MAX_ARG_STRLEN` ceiling, compacted `#130`-owned `nominationPanel` and `nominationPanel._routeForm` descriptors in `src/api/src/zava_forward/api/web/panels.js` (`66,477` -> `65,138` bytes, `-1,339` bytes) without altering runtime behavior or overlapping `origin/feat/demo-233-same-home-tensions-0825` (`50bd5acc0`), and passed all Focused Tier checks from `src/api`.

## Completed Work

### P01 / P01-T01 and P01-T02: Route Node Test Payloads over Stdin and Guard `MAX_ARG_STRLEN`

* Updated `evaluate()` and all 21 `CaseJourney` `subprocess.run` Node harnesses in `src/api/tests/test_case_journey.py` (including `test_quality_errors_and_manual_action_pending_siblings` and the `--unhandled-rejections=strict` harness) to pass JavaScript source via `input=...` on `stdin` with `"-"`, leaving `0` occurrences of `"-e"` in `src/api/tests/test_case_journey.py` while keeping `DOM`, `WEB`, and `shipped_helpers` module exports unchanged.
* Added `test_node_stdin_handles_scripts_above_linux_max_arg_strlen` to `CaseJourney` in `src/api/tests/test_case_journey.py`, padding `DOM + shipped_helpers() + ops.js + panels.js` past `131,072` UTF-8 bytes and verifying `["node", "-"]` executes shipped-helper assertions cleanly via `stdin`.

### P02 / P02-T01: Conciseness Trim in `panels.js` Nomination Helpers

* Extracted shared `assistedMediums` options and `nonDigitalRule` predicates across `ackForm` and `corrForm` inside `nominationPanel` and compacted verbose multiline descriptor objects inside `nominationPanel` and `nominationPanel._routeForm` in `src/api/src/zava_forward/api/web/panels.js`, reducing file size from `66,477` to `65,138` bytes (`-1,339` bytes) while preserving all copy literals, single-line `panelOwned(` calls, Epic #149 `±4`-line focus windows, `9` `aria-invalid` sites, slice boundary markers, and zero-conflict 3-way merge compatibility with `origin/feat/demo-233-same-home-tensions-0825` (`50bd5acc0`).

### P03 / P03-T01: Focused Tier Validation from `src/api`

* Classified as Focused Tier per D4 / `#1294` and caller instructions (test-harness `stdin` fix plus behavior-preserving formatting conciseness pass; no workflow, gate, dependency, Dockerfile, SQL, deployment, or security-control changes).
* Local Judgment Note: In this shared VM environment, editable `site-packages` points `zava_forward.api` at an absent sibling worktree, and `test_safety_panel_ux.py` / `test_challenge_non_retaliation_hazard_guard.py` use bare top-level sibling-test imports; prepending `src` (and `tests` when invoking bare-import test modules by path) on `PYTHONPATH` tests this worktree directly without mutating shared `pip` state.

## Implementation-Time Plan and Detail Updates

None.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `node --check src/api/src/zava_forward/api/web/panels.js` | P02-T01 | Passed | Exit 0 (`65,138` bytes, down from `66,477` bytes) |
| `git merge-file` 3-way merge dry run of `panels.js` against `origin/feat/demo-233-same-home-tensions-0825` (`50bd5acc0`) + `node --check` | P02-T01 | Passed | Exit 0 (`0` conflicts, `67,623` merged bytes) |
| `PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_case_journey.py tests/test_accessibility_baseline.py -v` (from `src/api`) | P03-T01 | Passed | 46 tests passed in 5.609s (`OK`), including `test_quality_errors_and_manual_action_pending_siblings` and `test_node_stdin_handles_scripts_above_linux_max_arg_strlen` |
| Coupled `test_nomination_screen.py`, `test_nomination_api_routes.py`, `test_epic149_form_error_summary_associations.py`, `test_content_standard.py`, `test_ux_design_traceability.py`, `test_safety_panel_ux.py`, `test_challenge_non_retaliation_hazard_guard.py` (from `src/api`) | P03-T01 | Passed | 72 tests passed across all 7 coupled suites (`OK`) |
| `python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy` (from `src/api`) | P03-T01 | Passed | `All checks passed!`, `211 files already formatted`, `Success: no issues found in 295 source files` (exit 0) |

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c3-plan.md, `## Follow-Up Items`
