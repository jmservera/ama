<!-- markdownlint-disable-file -->
# Review: Fix Node E2BIG Argument Limit in Case Journey Tests and Compact Nomination Panel Helpers

## Scope and Evidence

* Task ID: nomination-api-routes-130-c3
* Review date: 2026-11-15
* Review scope: full_plan (`P01`, `P02`, `P03`)
* Assessed boundary: Cycle 3 (`c3`) fix on `PR #1776` (`feat/ux-130-api-routes`, `Refs #130`) replacing `argv`-based `node -e <script>` payloads with `stdin` (`["node", "-"]` / `["node", "--unhandled-rejections=strict", "-"]` + `input=...`) across all 22 `subprocess.run` Node harnesses in `src/api/tests/test_case_journey.py`, adding a `>131,072`-byte `MAX_ARG_STRLEN` regression test, compacting `#130`-owned `nominationPanel` and `nominationPanel._routeForm` descriptors in `src/api/src/zava_forward/api/web/panels.js` (`66,477` -> `65,138` bytes) with zero behavioral change and zero merge overlap with `origin/feat/demo-233-same-home-tensions-0825` (`50bd5acc0`), refreshed Web Interface Guidelines compliance on changed web code, and Focused Tier validation from `src/api` (preserving `c1` and `c2` artifacts unchanged and not pushing remotely).
* Plan: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c3-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/nomination-api-routes-130-c3-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c3-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/nomination-api-routes-130-c3-research.md (`C1`–`C8`, `W1`), refreshed Vercel Web Interface Guidelines (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`), `git diff -- src/`, 3-way `git merge-file` verification against `origin/feat/demo-233-same-home-tensions-0825` (`50bd5acc0`), and Focused Tier `unittest`, `ruff`, and `mypy` runs from `src/api`.

## Opening Review State

* Interpreted review goal: Verify that Cycle 3 (`nomination-api-routes-130-c3`) permanently eliminates `OSError: [Errno 7] Argument list too long: 'node'` (`E2BIG` above `131,072` bytes) across `src/api/tests/test_case_journey.py`, trims `src/api/src/zava_forward/api/web/panels.js` cleanly without behavioral, WCAG 2.2, Fluent 2, plain-language, or merge regressions, passes all Focused Tier checks from `src/api`, and preserves all `c1` and `c2` `.copilot-tracking/` artifacts unchanged.
* Review scope: full_plan (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`)
* Evidence readiness: Ready; research, finalized plan, phase details, single-pass `Pass` critique, completed changes record, and live Git/validation evidence are present and reconciled.
* Acceptance basis: Approved plan functional/non-functional requirements and acceptance criteria, `Pass` critique disposition, AMA Web Development Guidance (`web-design-guidelines` `file:line` check + WCAG 2.2 / Fluent 2 / plain-language baseline), and Focused Tier validation rules.
* First comparison boundary: Plan checklist and phase details (`P01`–`P03`) versus `git diff -- src/` and `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c3-changes.md`.
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/logs/2026-11-15/nomination-api-routes-130-c3-review.md` and does not mutate production code, tests, research, plan, details, critique, or changes records.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass review on 2026-11-15 across all Cycle 3 artifacts, `git diff -- src/`, refreshed Web Interface Guidelines rules, 3-way merge verification with `origin/feat/demo-233-same-home-tensions-0825`, and Focused Tier validation outputs from `src/api`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` / `P01-T01`, `P01-T02` | Route Node Test Payloads over Stdin and Guard `MAX_ARG_STRLEN` | Reconciled | All 22 `subprocess.run` Node harnesses in `src/api/tests/test_case_journey.py` pass JavaScript via `input=...` on `stdin` with `"-"`; `0` occurrences of `"-e"` remain; `test_node_stdin_handles_scripts_above_linux_max_arg_strlen` added within locked test bounds (`0` removals, `1` addition). |
| `P02` / `P02-T01` | Conciseness Trim in `panels.js` Nomination Helpers | Reconciled | `src/api/src/zava_forward/api/web/panels.js` compacted inside `#130`-owned `nominationPanel` and `nominationPanel._routeForm` (`66,477` -> `65,138` bytes, `-1,339` bytes) with zero behavioral drift and clean 3-way merge against `50bd5acc0`. |
| `P03` / `P03-T01` | Focused Tier Validation from `src/api` | Reconciled | `test_case_journey.py` + `test_accessibility_baseline.py` (`46` tests), 7 coupled suites (`72` tests), `ruff check .`, `ruff format --check .`, and `mypy` all passed (`exit 0`) from `src/api`. |
| `## Follow-Up Items` | Canonical plan follow-up items | Reconciled | Owner remote push + hosted CI + independent exact-head review, optional `stdin` harmonization in smaller Node harnesses, and human governance (`OD-41`, `OD-42`) remain distinct follow-ups outside active scope. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01`, `P01-T01` | `src/api/tests/test_case_journey.py` | Replaced `-e <script>` on `argv` with `"-"` and `input=...` on `stdin` across `evaluate()` and all 21 `CaseJourney` `subprocess.run` Node calls (including `test_quality_errors_and_manual_action_pending_siblings` and the `--unhandled-rejections=strict` harness) while preserving `DOM`, `WEB`, and `shipped_helpers`. | `0` occurrences of `"-e"` in `src/api/tests/test_case_journey.py`; `test_safety_panel_ux.py` sibling import verified intact. | `test_case_journey.py`, `test_safety_panel_ux.py`, `ruff`, and `mypy` passed (`exit 0`). | Reconciled |
| `P01`, `P01-T02` | `src/api/tests/test_case_journey.py` | Added `test_node_stdin_handles_scripts_above_linux_max_arg_strlen` padding `DOM + shipped_helpers() + ops.js + panels.js` past `131,072` UTF-8 bytes and proving `["node", "-"]` executes via `stdin` without `OSError: [Errno 7]`. | Locked test bounds respected (`0` removals, `1` addition); formatted and strictly typed. | `test_case_journey.py` (`32` tests), `ruff check .`, `ruff format --check .`, and `mypy` passed (`exit 0`). | Reconciled |
| `P02`, `P02-T01` | `src/api/src/zava_forward/api/web/panels.js` | Shared `assistedMediums` and `nonDigitalRule` across `ackForm` and `corrForm` and compacted multiline descriptor formatting inside `nominationPanel` and `nominationPanel._routeForm`, saving `1,339` bytes (`66,477` -> `65,138` bytes) without touching copy strings, single-line `panelOwned(` calls, Epic #149 focus windows, `9` `aria-invalid` sites, slice boundaries, or `50bd5acc0` regions. | `node --check` exited `0`; 3-way `git merge-file` against `origin/feat/demo-233-same-home-tensions-0825` (`50bd5acc0`) exited `0` with `0` conflicts; Web Interface Guidelines check passed. | `test_accessibility_baseline.py`, `test_nomination_screen.py`, `test_nomination_api_routes.py`, `test_epic149_form_error_summary_associations.py`, `test_content_standard.py`, `test_ux_design_traceability.py`, and `test_challenge_non_retaliation_hazard_guard.py` passed (`exit 0`). | Reconciled |
| `P03`, `P03-T01` | No production file mutations (validation-only phase) | Executed Focused Tier `unittest`, `ruff check .`, `ruff format --check .`, and `mypy` suites from `src/api`. | Recorded in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c3-changes.md`. | All planned checks exited `0`. | Reconciled |

## Web Interface Guidelines Compliance (`file:line` Format)

Refreshed rules fetched from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` before reviewing changed web code:

```text
## src/api/src/zava_forward/api/web/panels.js

✓ pass
```

Native `<label for>`, `<select>`, `<textarea>`, `<input>`, `<button>`, `autocomplete="off"`, `aria-describedby`, `role="status"` + `aria-live="polite"` with `tabindex="-1"`, inline error + focus-first-invalid behavior, `panelOwned(...)` refusal recovery copy, `hasUnsavedChanges()` / `beforeunload` draft protection, reduced-motion, and forced-colours behavior are preserved unchanged.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| None (`P03-T01` local judgment only) | No plan or phase-detail revisions were needed; local `unittest` invocations from `src/api` prepended `src` (and `tests` when invoking bare sibling-importing suites by file path) on `PYTHONPATH` so shared VM `site-packages` remained untouched while loading this worktree's `zava_forward.api`. | Local judgment recorded in `-changes.md`; preserved approved scope and repository files unchanged. | Plan markers, phase-detail statuses, and `-changes.md` fully synchronized. | Single-pass critique (`Pass`, 0 `PC-xxx` findings) remained valid without re-critique. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: Single-pass critique (`.copilot-tracking/reviews/plans/2026-11-15/nomination-api-routes-130-c3-plan-critique.md`) returned `Pass` with `0` `PC-xxx` findings, and both implementation detail notes (`evaluate(expression: str)` 1-arg signature with `check=True`, and keeping `panelOwned(` calls single-line in `panels.js`) were honored directly in `P01-T01` and `P02-T01`.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: Execution followed `P01` -> `P02` -> `P03` strictly in dependency order with no early resumption or scope expansion.
* Justification assessment: Focused Tier classification and local judgment notes are evidence-backed and fully compliant with repository instructions.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Push `feat/ux-130-api-routes` to `PR #1776`, confirm green hosted GitHub Actions `src-api` (including `test_quality_errors_and_manual_action_pending_siblings` on `refs/pull/1776/merge`), and run independent exact-head review (`Refs #130`) | Caller explicitly instructed `Do NOT push from inside the session`; hosted CI on the new Cycle 3 local commit has not yet run on GitHub Actions. | Repository owner pushes branch, observes hosted CI on exact head, and runs independent exact-head review. | Distinct follow-up route |
| Optional cross-suite Node `stdin` harmonization in `test_safety_panel_ux.py`, `test_nomination_screen.py`, and `test_ux_design_traceability.py` | Those suites slice small substrings (`~3 KB–39 KB`, well under `131,072` bytes) and are outside `src/api/tests/test_case_journey.py` scope. | Optional future maintenance hygiene task if any sliced harness grows toward `MAX_ARG_STRLEN`. | Distinct follow-up route |
| Resolve governance open decisions `OD-41` and `OD-42` and record human representative comprehension sign-off before Issue `#130` closure (`Refs #130`) | Pre-existing human governance / lived-experience acceptance criteria outside executable code changes; keeps PR linkage at `Refs #130` rather than `Closes #130`. | Named human governance and accessibility reviewers. | Distinct follow-up route |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No `RV-xxx` defects, decision gaps, or material evidence gaps were found within the assessed Cycle 3 task boundary.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None | none | No corrective `rpi-implement`, `rpi-plan`, or `rpi-research` pass required for Cycle 3 | All `P01`–`P03` acceptance criteria satisfied |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Owner-controlled remote push (`git push origin feat/ux-130-api-routes`), exact-head hosted GitHub Actions `src-api` verification on `PR #1776`, independent exact-head review, optional cross-suite Node `stdin` harmonization, and human governance sign-off (`OD-41`, `OD-42`) remain outside this local no-push Cycle 3 boundary (`Refs #130`).

## Blockers and Remaining Work

* Blockers: None inside the Cycle 3 local implementation and Focused Tier validation boundary (hosted CI on the new local exact head has not run yet because pushing was explicitly prohibited by the caller).
* Remaining active work: None (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01` complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `node --check src/api/src/zava_forward/api/web/panels.js` | `src/api` web syntax | Passed | Exit 0 (`65,138` bytes, down from `66,477` bytes) |
| `git merge-file` 3-way merge check of `panels.js` against `origin/feat/demo-233-same-home-tensions-0825` (`50bd5acc0`) + `node --check` | Base-branch merge compatibility (`refs/pull/1776/merge`) | Passed | Exit 0 (`0` conflicts, `67,623` merged bytes) |
| `PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_case_journey.py tests/test_accessibility_baseline.py -v` (from `src/api`) | Required `test_case_journey.py` (`32` tests) + `test_accessibility_baseline.py` (`14` tests) | Passed | 46 tests passed in 5.609s (`OK`), including `test_quality_errors_and_manual_action_pending_siblings` and `test_node_stdin_handles_scripts_above_linux_max_arg_strlen` |
| Coupled `test_nomination_screen.py`, `test_nomination_api_routes.py`, `test_epic149_form_error_summary_associations.py`, `test_content_standard.py`, `test_ux_design_traceability.py`, `test_safety_panel_ux.py`, `test_challenge_non_retaliation_hazard_guard.py` (from `src/api`) | Coupled static/WCAG/nomination/sibling-import suites | Passed | 72 tests passed across all 7 suites (`OK`) |
| `python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy` (from `src/api`) | Required `src/api` lint, formatting, and static typing | Passed | `All checks passed!`, `211 files already formatted`, `Success: no issues found in 295 source files` (exit 0) |
| Hosted GitHub Actions CI (`src-api`) on new local exact head | Remote hosted workflow | Unavailable | Not yet run on the new Cycle 3 local commit because caller instructed `Do NOT push from inside the session` |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every Cycle 3 requirement and acceptance criterion (`P01` `stdin` conversion across all 22 `subprocess.run` Node calls in `src/api/tests/test_case_journey.py` + `>131,072`-byte `MAX_ARG_STRLEN` regression test, `P02` behavior-preserving `1,339`-byte conciseness pass in `src/api/src/zava_forward/api/web/panels.js` disjoint from `50bd5acc0`, refreshed Web Interface Guidelines compliance, preservation of all `c1` and `c2` `.copilot-tracking/` artifacts unchanged, and `P03` Focused Tier validation from `src/api`) is verified with zero defects.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct_follow_up | Owner remote push (`git push origin feat/ux-130-api-routes`), hosted CI verification, and independent exact-head review on `PR #1776` (`Refs #130`); optional cross-suite Node `stdin` harmonization; human governance sign-off (`OD-41`, `OD-42`) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused Tier local checks from `src/api` passed (`test_case_journey.py`, `test_accessibility_baseline.py`, 7 coupled nomination/WCAG/content-standard suites, 3-way `git merge-file` check against `50bd5acc0`, `ruff check .`, `ruff format --check .`, `mypy`, and refreshed `web-design-guidelines`); hosted CI unobserved pending owner push.
* Blockers: None for local Cycle 3 completion; remote publication/merge remains gated on owner push, hosted CI on exact head, independent exact-head review, and human governance (`OD-41`, `OD-42`).
