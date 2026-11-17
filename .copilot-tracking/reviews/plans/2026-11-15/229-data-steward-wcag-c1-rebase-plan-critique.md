<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #229 Cycle 1 Rebase onto Updated Parent (#1764)

## Metadata

* Task ID: 229-c1-rebase
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/229-data-steward-wcag-c1-rebase-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/229-data-steward-wcag-c1-rebase-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Rebase PR `#1764` (`Issue #229`, branch `feat/ux-229-data-steward-wcag` in `/home/azureuser/source/ama-demo-wt/feat-229-data-steward-wcag`) onto `origin/feat/demo-233-same-home-tensions-0825` after fetching parent and `#135` remote refs; preserve all `#232` (`#1763`) additions (`residentJumpNav`, `ROLE_HASH_SCREENS`, `screenRecordTable`, `stateCue`, `[tabindex="-1"]` / `.screen-record h2` focus helpers) alongside all `#229` (`data-operator` / exception register) WCAG jump nav, row headers, non-colour state cues, and `docs/reference/log.md` entries (including `#135` compatibility if present); run Focused validation tier (`unittest`, `ruff check`, `ruff format --check`, `mypy`); commit dated `.copilot-tracking/` Cycle 1 artifacts locally with Conventional Commit + Copilot trailer; do NOT push.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/229-data-steward-wcag-c1-rebase-research.md (`C1`–`C12`, `W1`), .github/copilot-instructions.md, src/api/src/zava_forward/api/web/role-screens.js, src/api/tests/test_data_steward_screen_wcag.py, src/api/tests/test_exception_register_screen.py, src/api/tests/test_data_operator_screen.py, src/api/tests/test_accessibility_baseline.py, docs/reference/log.md.
* Decisions, dependencies, and acceptance criteria considered: Option B convergence (rebase + `screenRecordTable` row headers on all 8 `#229` tables + `docs/reference/log.md` blank-line separation + coexistence unit tests), Focused validation commands, noreply git privacy, and no-push freeze.
* Assessment boundary: Evaluates plan credibility, merge/helper safety, test-baseline invariants, and git/tracking commit choreography from supplied repository and research evidence; cannot evaluate human assistive-technology (`#151`) or participant walkthrough (`#155`) acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern                                                                                                                               |
|------------------------------------------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| FR-01 / P01-T01                          | Covered  | Rebase topology (`5536c3907..321a22960`), safe `#135` ref check, and zero-diff guard on `#232` `app.js`/`style.css`/`test_housing_resident_screen_wcag.py` are well-grounded (`C1`–`C5`). |
| FR-02 / P02-T01 (`C3`, `C6`, `C8`, `C11`)| Partial  | `PC-001`: Plan explicitly locks `limit = Infinity` on the 2 `data-operator.summary` tables when switching to `screenRecordTable`, but omits that both `exceptionRegisterPanel` tables also pass `Infinity`. |
| FR-03 / P02-T02 (`C12`)                  | Covered  | Restores missing blank line between `#134` (and `#135` if merged) and `#229` `## [2026-11-15]` sections in `docs/reference/log.md` and aligns `customer-journeys/data.md`. |
| NFR-01 / P03-T01 (`C7`, `C8`)            | Covered  | Counted table baseline (`13` `h("table", {},` definitions in `test_accessibility_baseline.py`) is unaffected because `screenRecordTable` delegates to `screenTable`; singular `test_housing_resident_screen_wcag` is explicitly handled. |
| NFR-02 / P03-T01                         | Partial  | `PC-002`: Plan commits Cycle 1 artifacts in `P03-T01` before `rpi-review` writes `229-data-steward-wcag-c1-rebase-review.md` and final `Follow-up` state in `229-data-steward-wcag-c1-rebase-state.json`; closeout tracking commit/amend handling should be explicit so the frozen worktree ends clean. |

## Verdict

* Verdict: Revise
* Rationale: The rebase architecture, `#232`/`#229` helper convergence, and Focused validation coverage are sound and conflict-free, but two bounded planner-owned clarifications (`PC-001` preserving `Infinity` row limits on `exceptionRegisterPanel`'s two tables when switching to `screenRecordTable`, and `PC-002` explicitly folding post-Review `review.md`/`state.json` artifacts into the final frozen local commit so `git status` is clean) prevent silent truncation or dirty post-review tracking files.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Preserve `Infinity` row limit on both `exceptionRegisterPanel` tables when switching to `screenRecordTable`

* Related IDs: FR-02, `C3`, `C11`, P02, P02-T01
* Evidence: src/api/src/zava_forward/api/web/role-screens.js (`exceptionRegisterPanel` passes `Infinity` as the 4th argument on `"Exception items returned for you"` and `"Source conflicts with every returned value"`, while `screenRecordTable(label, headings, rows, limit = 50)` defaults `limit` to `50`).
* Concern: The candidate plan and `P02-T01` phase details explicitly remind implementers to preserve `Infinity` on the two `data-operator.summary` tables, which could mislead implementation into dropping `Infinity` on the two `exceptionRegisterPanel` tables and capping returned exception items at 50 rows.
* Impact: Truncating `exceptionRegisterPanel` at 50 rows would alter `#135`/`#229` exception-register behaviour for larger synthetic or server payloads.
* Smallest useful change: Update `Scope`, `Acceptance Criteria`, `P02-T01`, and `P02-T01` phase details to state that all 4 `Infinity`-unlimited `#229` tables (2 in `exceptionRegisterPanel` + 2 in `data-operator.summary`) retain `Infinity` as the 4th argument to `screenRecordTable`.
* Action owner: planning_parent
* Exact resolving evidence: Updated plan and phase details explicitly naming `Infinity` preservation on both `exceptionRegisterPanel` tables and both `data-operator.summary` tables, verified during implementation in `role-screens.js` diff.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Low]: Specify clean local tracking-artifact commit state across Implement and post-Review freeze

* Related IDs: NFR-02, P03, P03-T01
* Evidence: .copilot-tracking/plans/2026-11-15/229-data-steward-wcag-c1-rebase-plan.md (`P03-T01` and `Acceptance Criteria` require all 7 dated `.copilot-tracking/` Cycle 1 artifacts committed locally with a clean frozen worktree, while `reviews/logs/...-review.md` and final `rpi-sessions/...-state.json` are written during/after `rpi-review`).
* Concern: Without explicitly stating how the post-Review tracking files (`review.md` and final `state.json`) are committed into the local Cycle 1 commit candidate without touching production files or pushing, `git status` could remain dirty after `rpi-review` finishes.
* Impact: Violates the caller's requirement to *"Commit any dated `.copilot-tracking/` Cycle 1 rebase artifacts with Conventional Commit message and trailer ... Do NOT push; leave a clean frozen local candidate."*
* Smallest useful change: Clarify in `P03-T01` and `Handoff` that `P03-T01` commits the validated implementation and pre-review tracking files, and after the single `rpi-review` pass writes `review.md` and final `Follow-up` `state.json` (with zero production/source edits), those two tracking artifacts are folded into the local Cycle 1 commit so `git status --short` is empty.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P03-T01` plan/detail text and post-Review `git status --short` returning empty output with zero `.copilot-tracking/` mentions in `git log -1`.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Correctly identifies that `screenRecordTable` delegates to the single `screenTable` helper (`role-screens.js:51`), keeping `test_accessibility_baseline.py`'s exact `13`-table source count invariant untouched (`C8`).
* Properly accounts for the singular test module filename `src/api/tests/test_housing_resident_screen_wcag.py` introduced by `#1763` (`#232`), avoiding out-of-scope file duplication while still executing `#232`'s full WCAG test suite.
* Explicitly catches the silent missing-blank-line 3-way merge artifact in `docs/reference/log.md` (`C12`).
* Accepted residual risk: Human assistive-technology verification (`#151`) and participant walkthrough evaluation (`#155`) remain open repository-wide outside engineering scope.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Static plan/evidence critique only; runtime validation occurs in `P03-T01` during `rpi-implement`.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: `planning_parent`
* Smallest next action: Apply `PC-001` and `PC-002` directly to `.copilot-tracking/plans/2026-11-15/229-data-steward-wcag-c1-rebase-plan.md` and `.copilot-tracking/details/2026-11-15/229-data-steward-wcag-c1-rebase-phase-details.md`, record both dispositions in `## Critique Disposition`, mark planning status `Ready`, and proceed to `rpi-implement` without re-running critique.
* User response required: no
