<!-- markdownlint-disable-file -->
# RPI Plan: Issue #76 C2 Rebase Continuation onto `#1641` (`36aeddae3`)

## Task Metadata

* Task ID: issue-76-c2-rebase
* Task slug: ux-76-hazard-clock-owner-c2-rebase
* Planning status: Ready for implementation
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-plan-critique.md

## Executive Summary

This plan rebases `feat/ux-76-hazard-clock-owner` (`PR #1768`: `6e9eb39de`, `8f8d85342`, `941806d9d`) in `/home/azureuser/source/ama-demo-wt/feat-76-hazard-clock-owner` from `08c36e4dc` onto the latest `origin/feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`, tip `36aeddae345426fdf8ee53565fef1540979de967` incorporating `PR #1772` / Issue `#154`, `PR #1766` / Issue `#116`, and `PR #1773` / Issue `#215`), stashing and restoring the untracked `2026-11-15` `c2-rebase` tracking files across the rebase, resolves the rebase conflicts in `src/core/src/zava_forward/core/projection.py` and `src/core/src/zava_forward/core/store.py` while preserving `#116` Entra/field-level visibility gating, `#215` regulatory alert and home chat boundary suites, and `#76` hazard and safeguarding clocks, named owners, and SQL Server row-order invariant staff resolution (`8f8d85342`), closes the cross-feature raw safeguarding visibility seam between `#116` and `#76` with a focused unit test, runs focused validation (`unittest`, `ruff check`, `ruff format --check`, and `mypy` in `src/core` and `src/api`), and commits locally with `Refs #76` and the Copilot trailer without pushing.

### User Decisions and Requirements Highlights

* Run `rpi-plan-critique`, `rpi-implement`, and `rpi-review` continuously from the `2026-11-15` research and plan artifacts, writing dated `c2-rebase` artifacts under `.copilot-tracking/` for Issue `#76` (`PR #1768`) onto parent `#1641` tip `36aeddae345426fdf8ee53565fef1540979de967`.
* Fetch `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`), stash and restore the untracked `2026-11-15` `c2-rebase` tracking files across the rebase, and rebase the checked-out `#76` branch (`feat/ux-76-hazard-clock-owner` in worktree `/home/azureuser/source/ama-demo-wt/feat-76-hazard-clock-owner`) onto `origin/feat/demo-164-chat-grounding-provenance-0900`.
* Resolve conflicts in `src/core/src/zava_forward/core/projection.py` and `src/core/src/zava_forward/core/store.py` preserving `#116` (`PR #1766` Entra/field-level visibility and document-derivative gating), `#215` (`PR #1773` regulatory alerts, home chat, and visit consent boundary suites), AND `#76` (`PR #1768` hazard and safeguarding clock and named owner + SQL Server row-order invariant fix `8f8d85342`).
* Run focused validation (`unittest`, `ruff check .`, `ruff format --check .`, and `mypy` in `src/core` and `src/api`; do NOT run `tools/rpi-checks.py`).
* Ensure zero uncommitted or untracked changes remain (`git status --short` clean) and commit locally with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without `git push`.

### What You May Not Know

* The active `#76` `PR #1768` branch checked out in `/home/azureuser/source/ama-demo-wt/feat-76-hazard-clock-owner` is `feat/ux-76-hazard-clock-owner` (not `feat/demo-76-hazard-clock-owner-1208`), and the flat core modules are `src/core/src/zava_forward/core/projection.py` and `src/core/src/zava_forward/core/store.py` (there is no `case_workbench/` subpackage or `test_*case_workbench*.py` test file; `-p "test_*case_workbench*.py"` runs `0` tests, so validation executes both the exact caller commands and the real `#76`, `#116`, and `#215` test modules).
* AST-normalized comparison proves `store.py` has zero semantic function overlap (`#116` edited AI/document methods while `ruff format` wrapped the 6 `#76` safety hunks). However, in `projection.py`, `#116`'s `project_case_visibility` and `withheld_scope_values` invoke `redact_staff_detail` -> `hold_notes` directly on raw `store.cases` dicts before `Store.detail()` runs `safeguarding_view()`, meaning raw standalone safeguarding dicts lacking `"item_kind"` and `"released"` require container-aware holding in `hold_notes` and high-sensitivity `summary` classification in `_is_high_sensitivity_path` so `#116` AI output rechecks withhold private safeguarding text for non-reason roles.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Resume from the `2026-11-15` research and plan artifacts and execute `rpi-plan-critique`, `rpi-implement`, and `rpi-review` continuously for Issue `#76` (`c2-rebase` onto latest parent `#1641` tip `36aeddae345426fdf8ee53565fef1540979de967`), writing `.copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-changes.md`, and `.copilot-tracking/reviews/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md` (`Caller intake brief`).
* Fetch `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`), stash and restore the untracked `2026-11-15` `c2-rebase` tracking files across the rebase, and rebase the `#76` branch in `/home/azureuser/source/ama-demo-wt/feat-76-hazard-clock-owner` (`feat/ux-76-hazard-clock-owner` for `PR #1768`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`Caller intake brief`, research `C1`).
* Resolve conflicts in `src/core/src/zava_forward/core/projection.py` and `src/core/src/zava_forward/core/store.py` by preserving `#116` (`PR #1766` Entra/field-level visibility), `#215` (`PR #1773` regulatory alerts, home chat, and visit consent boundary suites), AND `#76` (`PR #1768` hazard and safeguarding clock and named owner + SQL Server row-order invariant fix `8f8d85342`) (`Caller intake brief`, research `C2`–`C6`, critique `PC-001`).
* Run focused-tier validation in `src/core` and `src/api` (`unittest`, `ruff check .`, `ruff format --check .`, `mypy`) and do NOT run `tools/rpi-checks.py` (`Caller intake brief`, research `C8`).
* Leave `git status --short` clean and commit locally with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` using privacy-safe GitHub noreply author identity; do NOT `git push` (`Caller intake brief`, `.github/copilot-instructions.md`).

## Goals

* Rebase `feat/ux-76-hazard-clock-owner` (`6e9eb39de`, `8f8d85342`, `941806d9d`) cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`) while stashing and restoring untracked `2026-11-15` `c2-rebase` tracking files across the rebase.
* Preserve all `#116` Entra/role field-level visibility and document-derivative controls and `#215` regulatory alert/home-chat contracts alongside all `#76` hazard and safeguarding clock, named-owner, and SQL Server row-order invariant staff resolution projections, including raw standalone safeguarding item withholding across `#116`'s `project_case_visibility` and `withheld_scope_values`.
* Verify focused unit tests, `ruff check .`, `ruff format --check .`, and strict `mypy` across `src/core` and `src/api`, and close out with clean committed `c2-rebase` RPI artifacts locally without pushing.

## Scope and Non-Goals

### In Scope

* Fetching `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`), stashing/restoring untracked `2026-11-15` `c2-rebase` tracking files, and rebasing `feat/ux-76-hazard-clock-owner` onto it.
* Resolving `src/core/src/zava_forward/core/projection.py` and `src/core/src/zava_forward/core/store.py` conflicts in `ruff format`-compliant style while preserving `#116`, `#215`, and `#76` (`6e9eb39de`, `8f8d85342`, `941806d9d`).
* Hardening `projection.py` (`hold_notes` and `_is_high_sensitivity_path`) and adding 1 focused regression test method in `src/core/tests/test_hazard_safeguarding_clock_owner_76.py` for raw standalone safeguarding visibility under `#116` + `#76`.
* Running the exact caller focused validation commands plus targeted `#76`, `#116`, and `#215` `unittest` modules across `src/core` and `src/api`.
* Recording and committing `ux-76-hazard-clock-owner-c2-rebase-*` tracking artifacts locally (including `.copilot-tracking/reviews/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md`).

### Non-Goals

* Running `tools/rpi-checks.py` or pushing to `origin`.
* Renaming open `PR #1768`'s branch (`feat/ux-76-hazard-clock-owner`) or modifying unrelated `#154` / `#83` modules.

## Functional Requirements

* FR-1: Clean rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`).
  * Fetch `origin feat/demo-164-chat-grounding-provenance-0900`, stash untracked `2026-11-15` `c2-rebase` tracking files, replay `6e9eb39de`, `8f8d85342`, and `941806d9d` onto `36aeddae345426fdf8ee53565fef1540979de967`, and restore the stashed tracking files.
  * Observable acceptance criteria: `git merge-base --is-ancestor 36aeddae345426fdf8ee53565fef1540979de967 HEAD` exits `0`, all 3 prior `#76` commits (including `8f8d85342` SQL Server row-order invariant fix) replay cleanly in order while preserving `#116` and `#215` upstream files, and zero conflict markers exist anywhere in the repository.
* FR-2: Lossless `#116` + `#76` merge in `src/core/src/zava_forward/core/store.py`.
  * Preserve all `#116` AI output visibility and document-derivative methods (`_clean_doc_ai_metadata`, `_rec_view`, `_visible_cid`, `add_document`, `ai_live_report`, `ai_priority`, `ai_run`, `draft`, `funding_draft`, `publish`, `read_document`, `row`, `valid`) alongside all `#76` safety clock and named-owner methods (`_open_safety_items`, `gate_reasons`, `status_line`, `summary`, `_work_context`, `focus`, `counts`, `detail`, `require_safety_clear`) in `ruff format`-compliant formatting.
  * Observable acceptance criteria: `Store.gate_reasons`, `Store.status_line`, `Store.summary`, `Store._work_context`, `Store.focus`, `Store.counts`, `Store.detail`, and `Store.require_safety_clear` preserve `#76` hazard + standalone safeguarding clock/owner behavior while all `#116` store methods remain intact.
* FR-3: Unified `#116` + `#76` field-level visibility in `src/core/src/zava_forward/core/projection.py`.
  * Preserve `#116`'s `withheld_case_values`, `project_case_visibility`, `withheld_scope_values`, `contains_withheld_value`, and `redact_staff_detail` AI summary/funding-draft rechecks AND `#76`'s `hold_notes` holding of `("source", "job", "summary", "reason")` on safety dicts, extended to raw standalone safeguarding dicts in `c["safeguarding_items"]` and `c["safeguarding"]` (matching `taskqueues.SAFEGUARDING_ITEM_KEYS` without mutating passive note-only `{"note": "..."}` canaries or `documents[*]["summary"]`) plus high-sensitivity path detection for safety `summary` fields in `_is_high_sensitivity_path`.
  * Observable acceptance criteria: For non-reason staff roles (`not can_see_reason(user)`), `projection.project_case_visibility`, `projection.withheld_scope_values`, and `projection.redact_staff_detail` hold raw standalone safeguarding `summary`, `source`, `job`, `reason`, and `note` fields and replace AI document summaries / funding drafts containing them with `NOTE_HELD`, while reason-authorized roles retain permitted summaries and passive note-only canaries remain passive.

## Non-Functional Requirements

* NFR-1: Focused validation pass across `src/core` and `src/api` with locked test budget.
  * Objective threshold or evaluation condition: Exact test removals = `none`; maximum new test files = `0`; maximum added test methods = `1` focused cross-feature regression test in canonical `src/core/tests/test_hazard_safeguarding_clock_owner_76.py` (0 generated targets; semantic cross-feature coverage of `#116` + `#76` raw safeguarding visibility alongside regression coverage of existing `#76`, `#116`, and `#215` suites).
  * Operating condition or verification approach, if needed: Run both exact caller step-4 commands (`unittest discover -s tests -p "test_*case_workbench*.py" -q && ruff check . && ruff format --check . && mypy` in `src/core` and `src/api`) AND explicit `unittest` runs of `#76`, `#116`, and `#215` test modules (`test_hazard_safeguarding_clock_owner.py`, `test_hazard_safeguarding_clock_owner_76.py`, `test_data_protection.py`, `test_taskqueues.py`, `test_sqlqueues.py`, `test_dependency_rule.py` in `src/core`; `test_hazard_safeguarding_clock_owner_api_76.py`, `test_ai_tasks.py`, `test_task_queue_api.py`, `test_alert_chat_owner_clock_safe_action_215.py`, `test_alert_chat_visit_consent_boundary_215.py` in `src/api`).
  * Observable acceptance criteria: Every command exits `0` with zero `ruff` or `mypy` diagnostics.
* NFR-2: Clean local commit closeout with privacy-safe author identity and zero remote push.
  * Objective threshold or evaluation condition: Repository-local `user.email` matches `{id}+{login}@users.noreply.github.com` from `gh api user`; code/test hardening and dated `ux-76-hazard-clock-owner-c2-rebase-*` `.copilot-tracking/` artifacts commit locally with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`; `git status --short` is empty; no `git push` runs.
  * Operating condition or verification approach, if needed: Check `git config --local user.email`, `git log -n 5 --oneline`, and `git status --short`.
  * Observable acceptance criteria: Clean working tree (`git status --short` empty) atop `36aeddae345426fdf8ee53565fef1540979de967` with `Refs #76` and Copilot trailer on the new commit.

## Acceptance Criteria

* AC-1: `git merge-base --is-ancestor 36aeddae345426fdf8ee53565fef1540979de967 HEAD` exits `0` on `feat/ux-76-hazard-clock-owner` with zero conflict markers and all `#116`, `#215`, and `#76` (including `8f8d85342` SQL Server row-order invariant fix) behavior preserved.
* AC-2: Raw standalone safeguarding `summary`, `source`, `job`, `reason`, and `note` values are held in `projection.project_case_visibility`, included in `projection.withheld_scope_values`, and gated out of AI document summaries and funding drafts for non-reason staff roles (`FR-3`), verified by a focused regression test in `src/core/tests/test_hazard_safeguarding_clock_owner_76.py`.
* AC-3: Focused validation across `src/core` and `src/api` succeeds: `unittest discover -s tests -p "test_*case_workbench*.py" -q` confirms `0` matching files (`NO TESTS RAN` exit `5` in Python 3.12, matching `C8`), `ruff check . && ruff format --check . && mypy` exits `0` in both `src/core` and `src/api`, and targeted `#76`, `#116`, and `#215` `unittest` runs across `src/core` and `src/api` all exit `0`.
* AC-4: All `ux-76-hazard-clock-owner-c2-rebase-*` `.copilot-tracking/` artifacts (`research`, `plans`, `details`, `critique`, `changes`, `reviews/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md`, `state.json`) and post-rebase hardening changes are committed locally with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, `git status --short` is empty, and no `git push` occurred.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-plan.md                                      |
| Phase details                    | .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-phase-details.md                           |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-plan-critique.md (`Revise` applied)  |
| Relevant research                | .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-research.md                               |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-changes.md is created by `rpi-implement`   |
| Planning execution and readiness | Complete and ready for implementation (`PC-001` and `PC-002` applied directly)                                     |
| Continuation context             | Confirmed automatic RPI Agent parent continues directly to `rpi-implement` (`P01-T01`)                             |

## Sources

* .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-research.md: Merge-tree, AST per-function diff, and `#116` + `#76` raw safeguarding visibility analysis (`C1`–`C8`).
* .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-plan.md: Prior C1 rebase plan and lineage context.
* src/core/src/zava_forward/core/projection.py and src/core/src/zava_forward/core/store.py: Conflict and cross-feature visibility targets.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Rebase onto `#1641` (`36aeddae3`) and Unify `#116` + `#215` + `#76` Projection/Store Behavior

* Intent: Fetch `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`), stash and restore untracked `2026-11-15` `c2-rebase` tracking files across the rebase, rebase `feat/ux-76-hazard-clock-owner` resolving `projection.py` and `store.py` conflicts cleanly while preserving `#116`, `#215`, and `#76` (`6e9eb39de`, `8f8d85342`, `941806d9d`), and close the `#116` + `#76` raw standalone safeguarding visibility seam with a focused regression test.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Fetch `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae3`), stash/restore untracked `c2-rebase` files, rebase `feat/ux-76-hazard-clock-owner`, and resolve `projection.py` and `store.py`

* Requirement and evidence: FR-1, FR-2, FR-3, AC-1; research `C1`–`C5`, critique `PC-001`
* Expected result: `feat/ux-76-hazard-clock-owner` replays `6e9eb39de`, `8f8d85342`, and `941806d9d` cleanly atop `36aeddae345426fdf8ee53565fef1540979de967` with untracked `c2-rebase` tracking files stashed and restored cleanly, `ruff format`-clean conflict resolution in `projection.py` and `store.py`, `#116` + `#215` + `#76` preserved, and zero conflict markers.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Harden raw standalone safeguarding visibility in `projection.py` and add `#116` + `#76` regression test

* Requirement and evidence: FR-3, NFR-1, AC-2; research `C6`, `C7`
* Expected result: `projection.hold_notes` holds `("source", "job", "summary", "reason")` on raw standalone safeguarding dicts inside `safeguarding_items` / `safeguarding` (matching `taskqueues.SAFEGUARDING_ITEM_KEYS`), `projection._is_high_sensitivity_path` marks safety `summary` paths as high-sensitivity, and `test_hazard_safeguarding_clock_owner_76.py` proves `project_case_visibility`, `withheld_scope_values`, and `redact_staff_detail` withhold raw safeguarding fields from non-reason roles and gate AI document summaries / funding drafts containing them.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Focused Validation and Local `Refs #76` Commit Closeout

* Intent: Run both the exact caller validation commands and the targeted `#76`, `#116`, and `#215` `unittest` suites across `src/core` and `src/api`, reconcile RPI artifacts for `rpi-review`, and commit all changes and `c2-rebase` tracking artifacts locally with `Refs #76` and the Copilot trailer without pushing.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run focused validation (`unittest`, `ruff check .`, `ruff format --check .`, `mypy`) and targeted `#76`, `#116`, and `#215` suites in `src/core` and `src/api`

* Requirement and evidence: NFR-1, AC-3; research `C8`, critique `PC-001`
* Expected result: `-p "test_*case_workbench*.py"` discovery confirms `0` matching files (`NO TESTS RAN` exit `5` in Python 3.12), while `ruff check . && ruff format --check . && mypy` and the targeted `#76`, `#116`, and `#215` `unittest` runs in `src/core` and `src/api` exit `0` with zero lint, format, or `mypy` issues.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile RPI artifacts, complete `rpi-review`, and commit locally with `Refs #76` and Copilot trailer leaving `git status --short` clean

* Requirement and evidence: NFR-2, AC-4; `.github/copilot-instructions.md`, critique `PC-002`
* Expected result: Privacy-safe `user.email` (`{id}+{login}@users.noreply.github.com`) verified, `changes.md` and plan/detail checklist markers reconciled before `rpi-review`, and after `rpi-review` writes `.copilot-tracking/reviews/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md` + `state.json`, code/test hardening and `ux-76-hazard-clock-owner-c2-rebase-*` artifacts are committed locally with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leaving `git status --short` empty with no `git push`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-phase-details.md

## Dependencies

* `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`).
* Local Python 3.12 toolchain with `ruff`, `mypy`, and `unittest` across `src/core` and `src/api`.

## Critique Disposition

* Single one-pass final-candidate critique executed at `.copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-plan-critique.md` (execution: `Complete`, verdict: `Revise`, user response required: `No`):
  * `PC-001` (High, direct planner correction — applied): Updated target `#1641` parent SHA from `243764945` to `36aeddae345426fdf8ee53565fef1540979de967` (`PR #1773` / `#215`), added explicit stash/restore (`git stash push -u` / `git stash pop`) of untracked `2026-11-15` `c2-rebase` tracking files across `git rebase`, and added `#215` alert owner/clock and visit-consent API test verification (`test_alert_chat_owner_clock_safe_action_215.py`, `test_alert_chat_visit_consent_boundary_215.py`) to `P02-T01`.
  * `PC-002` (Low, direct planner correction — applied): Aligned review output path in `AC-4` and `P02-T02` to caller Required Step 3's `.copilot-tracking/reviews/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md` and enforced production-reference hygiene on commit messages.

## Follow-Up Items

* Push rebased `feat/ux-76-hazard-clock-owner` to `origin` (`PR #1768`) once authorized by the owner/coordinator and verify hosted GitHub Actions CI (including `mssql` `MssqlParity`) passes on the new head SHA.
* Optional hardening (`RV-001` from C1 review): sort `staff` before role-based fallback in `workflows._resolve_escalation_target` (`#83`).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-changes.md
* Ready phase or task: Implementation complete (`P01`, `P02`); ready for `rpi-review`
* Remaining provisional question or blocker: None
