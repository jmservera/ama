<!-- markdownlint-disable-file -->
# Review: Rebase Issue 130 Branch and Fix Refusal Feedback Focus-Blur Clearing

## Scope and Evidence

* Task ID: nomination-api-routes-130-c2
* Review date: 2026-11-15
* Review scope: full_plan (`P01`, `P02`, `P03`)
* Assessed boundary: Rebase of `feat/ux-130-api-routes` (`PR #1776`, `Refs #130`) onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`, `PR #1639`), `<select>`-scoped `"change"` listener fix in `nominationPanel._routeForm` (`src/api/src/zava_forward/api/web/panels.js`), Node focus-blur `"change"` unit regression test in `src/api/tests/test_nomination_screen.py`, refreshed Web Interface Guidelines compliance on changed web code, and Focused Tier validation (explicitly excluding `tools/rpi-checks.py` and remote push).
* Plan: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c2-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/nomination-api-routes-130-c2-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c2-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/nomination-api-routes-130-c2-research.md (`C1`–`C7`, `W1`), refreshed Vercel Web Interface Guidelines (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`), `git diff 11867e8b1 -- src/`, `git merge-base --is-ancestor origin/feat/demo-233-same-home-tensions-0825 HEAD`, and Focused Tier test/browser/lint/typecheck runs.

## Opening Review State

* Interpreted review goal: Verify that Cycle 2 (`nomination-api-routes-130-c2`) cleanly rebases `feat/ux-130-api-routes` onto `6510b6fbc`, eliminates the synchronous blur-triggered `"change"` refusal-feedback wipe in `nominationPanel._routeForm` without regressing `<select>` change handling or WCAG 2.2 / Fluent 2 / content-standard invariants, satisfies Focused Tier validation, and preserves all prior `.copilot-tracking/` artifacts.
* Review scope: full_plan (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`)
* Evidence readiness: Ready; research, finalized plan, phase details, single-pass `Pass` critique, completed changes record, and live Git/validation evidence are present and reconciled.
* Acceptance basis: Approved plan functional/non-functional requirements and acceptance criteria, `Pass` critique disposition, AMA Web Development Guidance (`web-design-guidelines` `file:line` check + WCAG 2.2 / Fluent 2 / plain-language baseline), and Focused Tier validation rules.
* First comparison boundary: Plan checklist and phase details (`P01`–`P03`) versus `git log` ancestry, `git diff 11867e8b1 -- src/`, and `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c2-changes.md`.
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/logs/2026-11-15/nomination-api-routes-130-c2-review.md` and does not mutate production code, tests, research, plan, details, critique, or changes records.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass review on 2026-11-15 across all Cycle 2 artifacts, rebased Git ancestry (`6510b6fbc` -> `9b9f72eae` -> `11867e8b1` + Cycle 2 working tree), refreshed Web Interface Guidelines rules, and Focused Tier validation outputs.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` / `P01-T01` | Rebase onto Target Parent Branch | Reconciled | `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) fetched and confirmed ancestor of `HEAD`; prior `#130` commits replayed cleanly (`9b9f72eae`, `11867e8b1`) with zero conflicts and zero `.copilot-tracking/` deletions/overwrites. |
| `P02` / `P02-T01`, `P02-T02` | Fix `_routeForm` Focus-Blur Clearing and Add Regression Test | Reconciled | `panels.js` scopes `addEventListener("change", clearInvalid)` to `isSelect` (`Boolean(options)`); `test_nomination_screen.py` adds 1 Node regression test within locked test bounds (`0` removals, `1` addition). |
| `P03` / `P03-T01` | Focused Tier Validation | Reconciled | All targeted `src/core` and `src/api` unit suites, coupled static/WCAG guards, `case_journey_browser_check.py`, `nomination_browser_check.py`, `ruff`, and `mypy` passed (`exit 0`); `tools/rpi-checks.py` intentionally not run per caller rule. |
| `## Follow-Up Items` | Canonical plan follow-up items | Reconciled | Owner remote push + hosted CI + independent exact-head review and optional `nomination_browser_check.py` interactive scan remain distinct follow-ups outside active scope. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01`, `P01-T01` | Git ancestry of `feat/ux-130-api-routes` | Rebased `feat/ux-130-api-routes` onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) so `PR #1776` incorporates merged parent work (`#1784`) cleanly. | `git merge-base --is-ancestor origin/feat/demo-233-same-home-tensions-0825 HEAD` exited `0`; `9b9f72eae` and `11867e8b1` replayed cleanly. | `test_programme_coordinator_wcag_230.py` and `case_journey_browser_check.py` passed (`exit 0`). | Reconciled |
| `P02`, `P02-T01` | `src/api/src/zava_forward/api/web/panels.js` | Added `isSelect: Boolean(options)` to `nominationPanel._routeForm` field descriptors and guarded `if (isSelect) input.addEventListener("change", clearInvalid);` so `status.focus()` blurring a dirty `<input>` or `<textarea>` after a `409` refusal never wipes `mutation.message`, while `<select>` `"change"` and `<input>`/`<textarea>` `"input"` clearing remain intact. | Surgical 3-line net diff in `panels.js`; zero `.copilot-tracking/` references; zero banned words under `test_content_standard.py`; Web Interface Guidelines check passed. | `node --check`, `test_nomination_screen.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_epic149_form_error_summary_associations.py`, and `case_journey_browser_check.py` passed (`exit 0`). | Reconciled |
| `P02`, `P02-T02` | `src/api/tests/test_nomination_screen.py` | Added `test_route_form_blur_change_preserves_refusal_message_while_input_and_select_clear` modeling synchronous DOM blur -> `"change"` dispatch during `status.focus()` on `409` refusal, subsequent `"input"` clearing, and `<select>` `"change"` clearing + `showWhen` visibility toggling. | Locked test bounds respected (`0` removals, `1` addition); formatted with `ruff format`. | `unittest`, `ruff check`, `ruff format --check`, and `mypy` passed (`exit 0`). | Reconciled |
| `P03`, `P03-T01` | No production file mutations (validation-only phase) | Verified Focused Tier unit, Playwright + axe-core browser, Ruff, and Mypy checks end-to-end without running `tools/rpi-checks.py`. | Recorded in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c2-changes.md`. | All planned checks exited `0`. | Reconciled |

## Web Interface Guidelines Compliance (`file:line` Format)

Refreshed rules fetched from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` before reviewing changed web code:

```text
## src/api/src/zava_forward/api/web/panels.js

✓ pass
```

Native `<label for>`, `<select>`, `<textarea>`, `<input>`, `<button>`, `autocomplete="off"`, `aria-describedby`, `role="status"` + `aria-live="polite"` with `tabindex="-1"`, inline actionable `panelOwned(...)` refusal recovery guidance, `hasUnsavedChanges()` / `beforeunload` draft protection, reduced-motion, and forced-colours behavior are preserved.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| None (`P03-T01` local judgment only) | No plan or phase-detail revisions were needed; local runner invocation included `src/api:src/core` on `PYTHONPATH` and a temporary `FONTCONFIG_FILE` aliasing `sans-serif`/`system-ui`/`Segoe UI` to installed proportional `Liberation Sans` so VM font fallback (`Liberation Mono`) matched `ubuntu-latest` CI metrics during `case_journey_browser_check.py`. | Local judgment recorded in `-changes.md`; preserved approved scope and repository files unchanged. | Plan markers, phase-detail statuses, and `-changes.md` fully synchronized. | Single-pass critique (`Pass`, 0 `PC-xxx` findings) remained valid without re-critique. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: Single-pass critique (`.copilot-tracking/reviews/plans/2026-11-15/nomination-api-routes-130-c2-plan-critique.md`) returned `Pass` with `0` `PC-xxx` findings, and its implementation note (including `const PANEL_SUPPORT` when slicing `panels.js` in `P02-T02`) was honored directly in `src/api/tests/test_nomination_screen.py`.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: Execution followed `P01` -> `P02` -> `P03` strictly in dependency order with no early resumption or scope expansion.
* Justification assessment: Focused Tier classification and local judgment notes are evidence-backed and fully compliant with repository instructions.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Push rebased `feat/ux-130-api-routes` (`--force-with-lease`) to `PR #1776`, confirm green hosted GitHub Actions `src-api` and browser checks, and run independent exact-head review (`Refs #130`) | Caller explicitly instructed `do NOT push` in this session; hosted CI for the new rebased exact head has not yet run on GitHub Actions. | Repository owner pushes branch, observes hosted CI on exact head, and runs independent exact-head review. | Distinct follow-up route |
| Extend `src/api/checks/nomination_browser_check.py` to scan interactive dual-route nomination acknowledgement and correction disclosures with axe-core 4.10.3 | Optional browser-harness enhancement outside the Cycle 2 focus-blur bugfix and rebase scope. | Future bounded `rpi-research` / `rpi-plan` slice if prioritized. | Distinct follow-up route |
| Resolve governance open decisions `OD-41` and `OD-42` and record human representative comprehension sign-off before Issue `#130` closure (`Refs #130`) | Pre-existing human governance / lived-experience acceptance criteria outside executable code changes; keeps PR linkage at `Refs #130` rather than `Closes #130`. | Named human governance and accessibility reviewers. | Distinct follow-up route |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No `RV-xxx` defects, decision gaps, or material evidence gaps were found within the assessed Cycle 2 task boundary.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None | none | No corrective `rpi-implement`, `rpi-plan`, or `rpi-research` pass required for Cycle 2 | All `P01`–`P03` acceptance criteria satisfied |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Owner-controlled remote push (`git push --force-with-lease origin feat/ux-130-api-routes`), exact-head hosted GitHub Actions `src-api` verification on `PR #1776`, independent exact-head review, optional interactive `nomination_browser_check.py` expansion, and human governance sign-off (`OD-41`, `OD-42`) remain outside this local no-push Cycle 2 boundary (`Refs #130`).

## Blockers and Remaining Work

* Blockers: None inside the Cycle 2 local implementation and Focused Tier validation boundary (hosted CI on the new local exact head has not run yet because pushing was explicitly prohibited by the caller).
* Remaining active work: None (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01` complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `git merge-base --is-ancestor origin/feat/demo-233-same-home-tensions-0825 HEAD` | `P01-T01` rebase ancestry | Passed | Exit 0; `6510b6fbc` is ancestor of `HEAD` |
| `node --check src/api/src/zava_forward/api/web/panels.js` | `src/api` web syntax | Passed | Exit 0 |
| `PYTHONPATH=src/api:src/core:src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest discover -s src/core/tests -p "test_*nomination*.py" -q` | `src/core` nomination unit tests | Passed | 16 tests passed (exit 0) |
| `PYTHONPATH=src/api:src/core:src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest discover -s src/api/tests -p "test_*nomination*.py" -q` | `src/api` nomination API + screen unit tests | Passed | 13 tests passed including new focus-blur regression test (exit 0) |
| `PYTHONPATH=src/api:src/core:src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_resident_api.py src/api/tests/test_accessibility_baseline.py src/api/tests/test_case_journey.py src/api/tests/test_content_standard.py src/api/tests/test_epic149_form_error_summary_associations.py src/api/tests/test_programme_coordinator_wcag_230.py -q` | Coupled API, WCAG baseline, content standard, case journey, and rebased coordinator suites | Passed | All suites passed (exit 0) |
| `FONTCONFIG_FILE="$TMP_AXE_DIR/fonts.conf" PYTHONPATH=src/api:src/core:src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 src/api/checks/case_journey_browser_check.py --axe "$TMP_AXE_DIR/axe-4.10.3.min.js" --out "$TMP_AXE_DIR/case-journey-results"` | End-to-end Playwright + SHA-verified axe-core 4.10.3 case journey harness | Passed | Exit 0 across all checks including `mutation_reconstruction` (`challenge` `refusal`), reflow (320/390/1280/200% zoom), forced-colours, and fallback |
| `PYTHONPATH=src/api:src/core:src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 src/api/checks/nomination_browser_check.py --axe "$TMP_AXE_DIR/axe-4.10.3.min.js" --out "$TMP_AXE_DIR/nomination-results.json"` | End-to-end Playwright + SHA-verified axe-core 4.10.3 nomination screen harness | Passed | Exit 0 (`outcome: passed`, 0 axe violations) |
| `python3 -m ruff check src/core src/api && python3 -m ruff format --check src/core src/api` | `src/core` and `src/api` lint and formatting | Passed | All checks passed; 475 files formatted (exit 0) |
| `(cd src/core && python3 -m mypy) && (cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)` | `src/core` and `src/api` static typing | Passed | 0 issues in 317 `src/core` files and 295 `src/api` files (exit 0) |
| `tools/rpi-checks.py` | Repository local gate script | Skipped | Explicitly excluded by caller Focused Tier instructions |
| Hosted GitHub Actions CI (`src-api`) on new local exact head | Remote hosted workflow | Unavailable | Not yet run on the new rebased local commit because caller instructed `do NOT push` |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every Cycle 2 requirement and acceptance criterion (`P01` rebase onto `6510b6fbc`, `P02` `<select>`-scoped `"change"` listener fix + Node focus-blur regression test, refreshed Web Interface Guidelines compliance, preservation of all existing `.copilot-tracking/` artifacts, and `P03` Focused Tier validation including end-to-end `case_journey_browser_check.py` `mutation_reconstruction`) is verified with zero defects.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct_follow_up | Owner remote push (`--force-with-lease`), hosted CI verification, and independent exact-head review on `PR #1776` (`Refs #130`); optional interactive `nomination_browser_check.py` expansion; human governance sign-off (`OD-41`, `OD-42`) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused Tier local checks passed (`src/core` and `src/api` nomination unit tests, `test_resident_api.py`, `test_accessibility_baseline.py`, `test_case_journey.py`, `test_content_standard.py`, `test_epic149_form_error_summary_associations.py`, `test_programme_coordinator_wcag_230.py`, `case_journey_browser_check.py`, `nomination_browser_check.py`, `ruff check`, `ruff format --check`, `mypy`, and refreshed `web-design-guidelines`); `tools/rpi-checks.py` skipped per caller instruction; hosted CI unobserved pending owner push.
* Blockers: None for local Cycle 2 completion; remote publication/merge remains gated on owner push, hosted CI on exact head, independent exact-head review, and human governance (`OD-41`, `OD-42`).
