<!-- markdownlint-disable-file -->
# RPI Plan: Scoped Stabilization Checkpoints for Epic #89 and Epic #100

## Task Metadata

* Task ID: delivery-89-100-epic-stabilization-checkpoints-2026-11-15
* Task slug: delivery-89-100-epic-stabilization-checkpoints
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-plan-critique.md

## Executive Summary

This plan executes and records the `#440` scoped stabilization checkpoints for **Epic #89** (*Provider capacity, work orders and quality acceptance*: closed children `#90`, `#91`, `#92`, `#132`, `#133`, `#1384`, `#1402`) and **Epic #100** (*Management insight, forecasting and evidence export*: closed children `#101`, `#102`, `#103` plus merged management AI tokenomics PRs `#911`, `#1169`, `#1792`). All feature child issues of both epics are closed on GitHub, leaving only the `#440` scoped stabilization checkpoint acceptance criterion unticked on `#89` and `#100`. Implementation executes focused local-first regression and integration suites across `src/core`, `src/api`, and repository documentation/audit guards, then appends two dated (`2026-11-15`) checkpoint sections to `docs/architecture/cutover-evidence-pack.md`, updates `docs/reference/README.md`, and appends an EOF entry to `docs/reference/log.md` before creating a clean local commit on `feat/epic-89-100-stabilization-checkpoints`.

### User Decisions and Requirements Highlights

* Run the full RPI loop in automatic/autopilot mode (`research`, `plan` with single-pass `plan critique`, `implement`, `review`) under `.copilot-tracking/*/2026-11-15/` for slug `delivery-89-100-epic-stabilization-checkpoints`.
* Operate under the Focused validation tier: run relevant `src/core` and `src/api` focused regressions plus `src/core/tests/test_live_doc_links.py` and `python3 tools/check-legacy-references.py`, and do NOT invoke `tools/rpi-checks.py`.
* Preserve all existing sections in `docs/architecture/cutover-evidence-pack.md` (including the historical 2026-11-03 partial Epic `#89` checkpoint), use `*` for unordered lists, plain ASCII punctuation, no em dashes, no bolded-prefix list items, append-only at EOF for `docs/reference/log.md`, and zero `.copilot-tracking/` references anywhere in `docs/` or `src/`.
* Stage and commit all `docs/` and `.copilot-tracking/` files locally on `feat/epic-89-100-stabilization-checkpoints` with `Refs #89`, `Refs #100`, `Refs #440` and the Copilot trailer; do NOT push or open a pull request.

### What You May Not Know

* **Git SHA Reconciliation (`C1`, `W1`, `W2`)**: `git cat-file -t` proves the 40-character strings cited in the dispatch brief (`7427320280f68fd91f91df37a108892c3e97101f` and `c1ef91e23df56947b6ce1313684b587ff03dc134`) do not exist in the repository object database. Actual worktree `HEAD` and live GitHub `PR #1641` (`feat/demo-164-chat-grounding-provenance-0900`) `headRefOid` is `74273202817f9068f9c55cb325b39df7879cba7b` (matching the 9-character prefix `742732028`, tree `545efe335ef470272cd61ac6cde573764186a737`), actual `origin/main` (and live GitHub `main`) SHA is `5e0c7f74432ffce73cfeaa672e4e40a605ca6274`, and `git merge-base HEAD origin/main` is `61e1917dd075a8307f0fd436c42cc41f47906846`. Both checkpoints will bind local test observations to the verified Git object IDs while explicitly disclosing the dispatch brief's unresolvable nominal strings.
* **Branch Ancestry Split (`C1`, `W16`)**: `HEAD` includes all primary child PRs merged to `main` at or before merge-base `61e1917dd075a8307f0fd436c42cc41f47906846` plus stacked `PR #1641` commits (`#1657`, `#1674`, `#1745`, `#1770`, `#1771`, `#1792`), whereas post-merge-base `origin/main` commit `4629e3e5c` (`PR #1666`, field escalation routing) and sibling-branch `feat/demo-233-same-home-tensions-0825` merges (`#1682`, `#1706`, `#1725`, `#1758`) sit outside `HEAD`'s tree until `PR #1641` rebases onto `main`. Recording that exact ancestry boundary prevents over-claiming local execution coverage.
* **BRD vs PRD `FR-*` Numbering Divergence (`C4`, `C5`) and `#432` Audit Guard (`C36`)**: BRD `v0.21.0` and PRD `v0.21.0` assign different meanings to `FR-016..FR-017`, `FR-020..FR-024`, `FR-029..FR-031`, and `FR-035`; every traceability row will therefore use document-qualified IDs (`BRD::...`, `PRD::...`, `ADR-...`) and flag the divergence explicitly. In addition, `tools/test_epic_child_disposition_audit.py` requires explicit residual wording near any mention of `#432` in `cutover-evidence-pack.md`, so `P01` and `P04` run that audit test alongside `test_live_doc_links.py` and `tools/check-legacy-references.py`.

### Unresolved Decisions or Blockers

* None blocking checkpoint execution. Normative live/operational approvals (`BRD v0.21.0` draft, `PRD v0.21.0` unsigned in-review, `ADR-0001`/`0002`/`0007` Proposed, `OD-51`/`OQ-027` tariff governance on `#432`, and Azure live environment checks on `#116`/`#136`/`#144`) remain open owner/human/Azure gates and are recorded honestly as residuals rather than treated as satisfied.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Execute the full RPI loop in order (`research`, `plan` with single-pass `plan critique`, `implement`, `review`) writing dated artifacts under `.copilot-tracking/` (`research/2026-11-15/`, `plans/2026-11-15/`, `details/2026-11-15/`, `reviews/plans/2026-11-15/`, `changes/2026-11-15/`, `reviews/logs/2026-11-15/`, and `rpi-sessions/2026-11-15/`) for task slug `delivery-89-100-epic-stabilization-checkpoints` (user prompt).
* Operate in worktree `/home/azureuser/source/ama-demo-wt/feat-89-100-epic-stabilization-checkpoints` on branch `feat/epic-89-100-stabilization-checkpoints` stacked on `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) (user prompt).
* Use the Focused validation tier (`docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md` + focused regression test execution for Epic `#89` and Epic `#100`) and do NOT invoke `tools/rpi-checks.py` (user prompt).
* Execute `#440` scoped stabilization checkpoints for Epic `#89` (`#90`, `#91`, `#92`, `#132`, `#133`, `#1384`, `#1402`) and Epic `#100` (`#101`, `#102`, `#103`) and record in `docs/architecture/cutover-evidence-pack.md`: (1) source and document provenance including pinned parent head, `origin/main` SHA, covered PRs/issues, exclusions, and Case Study / BRD / PRD / ADR paths, versions/dates, git blob SHAs, and honest draft/unsigned status; (2) document-qualified requirement-to-code/test/journey traceability and cross-cutting boundary verification (package/identity, persistence, auth/roles, resident consent, human review/approval, AI unavailable/failure and manual paths); (3) actual local-first regression and integration execution with exact commands, exit codes, test counts, skips, and verification classes (`local observed`, `implemented-unverified`, `deferred`, `blocked`); and (4) bug/refactoring disposition, authorized Azure-only/human residuals, and `continue` recommendation gating Epic `#89` and Epic `#100` closure (user prompt, `#440`).
* Preserve all existing sections of `docs/architecture/cutover-evidence-pack.md`, update `docs/reference/README.md`, and append an EOF entry to `docs/reference/log.md` (user prompt, `.github/copilot-instructions.md`).
* Follow repository Markdown and tracking rules: `*` for unordered lists in new content, plain ASCII punctuation, no em dashes, no bolded-prefix list items, and zero `.copilot-tracking/` references in `docs/` or `src/` (user prompt, `.github/copilot-instructions.md`).
* When `Review` reaches `Outcome: Conformant`, stage and commit all `docs/` and `.copilot-tracking/` changes locally on `feat/epic-89-100-stabilization-checkpoints` with `Refs #89`, `Refs #100`, `Refs #440` and the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer, without pushing or opening a PR (user prompt).

## Goals

* Execute and capture deterministic local-first unit, API, screen, browser-retry, dependency-rule, and documentation guard test results across `src/core`, `src/api`, and `tools/` for Epic `#89` and Epic `#100` without invoking `tools/rpi-checks.py`.
* Author complete, honest, evidence-backed `2026-11-15` `#440` scoped stabilization checkpoint sections for Epic `#89` and Epic `#100` in `docs/architecture/cutover-evidence-pack.md` while preserving all existing historical sections.
* Synchronize the knowledge base index (`docs/reference/README.md`) and append-only changelog (`docs/reference/log.md`) with zero broken relative links, zero legacy-reference violations, and zero `.copilot-tracking/` path leaks in `docs/`.
* Complete post-implementation review and leave a clean, privacy-safe local commit on `feat/epic-89-100-stabilization-checkpoints` ready for coordinator integration.

## Scope and Non-Goals

### In Scope

* Running focused local regression and integration suites in `src/core/tests/`, `src/api/tests/`, and `tools/` covering Epic `#89`, Epic `#100`, cross-cutting package/consent/RBAC/AI fallback boundaries, live documentation links, legacy references, and epic child disposition guards.
* Updating `docs/architecture/cutover-evidence-pack.md` (`ms.date: 2026-11-15` and appended Epic `#89` and Epic `#100` `2026-11-15` `#440` checkpoint sections).
* Updating `docs/reference/README.md` (`ms.date: 2026-11-15` and architecture evidence pack description) and appending one `[2026-11-15]` entry at EOF of `docs/reference/log.md`.
* Recording full RPI artifacts under `.copilot-tracking/*/2026-11-15/` and committing locally after `Outcome: Conformant` review.

### Non-Goals

* Modifying `src/` production or test files (unless a genuine regression defect is uncovered during `P01`, which research indicates is not expected; test removals: `none`, planned test additions: `0`).
* Running `tools/rpi-checks.py`, full Azure live deployments, or SQL container harnesses.
* Ticking criteria on or closing GitHub issues `#89`, `#100`, or `#440` before pull request review and merge to `main`.
* Pushing branches (`git push`) or opening/updating GitHub pull requests (`gh pr create`).

## Functional Requirements

* FR-1: Execute focused local regression and integration checks covering every Epic `#89` capability (`#90`, `#91`, `#92`, `#132`, `#133`, `#1384`, `#1402`), every Epic `#100` capability (`#101`, `#102`, `#103` and `#100` AI tokenomics management summaries), cross-cutting package/safety/consent boundaries, and documentation guards (`test_live_doc_links.py`, `tools/check-legacy-references.py`, `tools/test_epic_child_disposition_audit.py`).
  * Observable acceptance criteria: Every planned command runs against the worktree tree (`545efe335ef470272cd61ac6cde573764186a737`), and its exact command string, exit code, run count, skip count/reason, and verification class (`local observed`, `implemented-unverified`, `deferred`, or `blocked`) are captured verbatim.
* FR-2: Record Source and Document Provenance for both Epic `#89` and Epic `#100` in `docs/architecture/cutover-evidence-pack.md`.
  * Observable acceptance criteria: Both checkpoint sections record verified worktree/parent `PR #1641` head `74273202817f9068f9c55cb325b39df7879cba7b` (tree `545efe335ef470272cd61ac6cde573764186a737`), `origin/main` SHA `5e0c7f74432ffce73cfeaa672e4e40a605ca6274`, merge-base `61e1917dd075a8307f0fd436c42cc41f47906846`, an explicit disclosure reconciling the dispatch prompt's unresolvable nominal strings (`7427320280f68fd91f91df37a108892c3e97101f` and `c1ef91e23df56947b6ce1313684b587ff03dc134`), covered PRs and child issues, post-merge-base/sibling-branch exclusions (`PR #1666` on `origin/main`; `PRs #1682, #1706, #1725, #1758` on `feat/demo-233-same-home-tensions-0825`), and exact paths, versions/dates, git blob SHAs, and draft/unsigned approval statuses for `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/brds/agentic-retrofit-programme-brd.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, and `docs/adrs/0001..0007`.
* FR-3: Record Requirement-to-Code/Test/Journey Traceability and Cross-Cutting Boundary Verification for Epic `#89` and Epic `#100`.
  * Observable acceptance criteria: Traceability tables use document-qualified IDs (`BRD::...`, `PRD::...`, `ADR-...`), explicitly flag the BRD vs PRD `FR-*` numbering divergence, map every child issue and capability to concrete `src/core` and `src/api` modules, tests, observed journeys, and remaining backlog, and include an explicit verification matrix for package/identity boundaries, persistence, auth/roles, resident consent, human review/approval boundaries, and AI unavailable/failure and manual paths.
* FR-4: Record Bug/Refactoring Disposition, Authorized Residuals, and Closure Gate Recommendation, and update Knowledge Base index/changelog.
  * Observable acceptance criteria: Both checkpoints state explicitly whether any new defect or required refactoring was found, classify authorized Azure-only and human/legal/owner residuals on their owning tracking issues (`#116`, `#136`, `#144`, `#432`, `#440`), record the `continue` recommendation gating Epic `#89` and Epic `#100` closure upon merge and owner verification, update `docs/reference/README.md`, and append one dated `[2026-11-15]` entry at EOF of `docs/reference/log.md`.

## Non-Functional Requirements

* NFR-1: Documentation style, link integrity, and tracking-isolation compliance.
  * Objective threshold or evaluation condition: Zero unresolved relative links (`test_live_doc_links.py`), zero retired-path/package violations (`tools/check-legacy-references.py`), zero child-disposition regressions (`tools/test_epic_child_disposition_audit.py`), zero `.copilot-tracking/` substrings in changed `docs/` files, zero em dashes (`—` or `--` prose separators), zero bolded-prefix list items (`* **Label:**`), and `*` unordered bullets throughout new Markdown lines.
  * Operating condition or verification approach: Post-edit execution of `test_live_doc_links.py`, `tools/check-legacy-references.py`, `tools/test_epic_child_disposition_audit.py`, and deterministic regex checks over `git diff docs/`.
  * Observable acceptance criteria: All three Python checks exit `0` and regex diff checks over `docs/` report `0` matches.
* NFR-2: Non-destructive history preservation and privacy-safe Git commit hygiene.
  * Objective threshold or evaluation condition: Existing lines of `docs/architecture/cutover-evidence-pack.md` (aside from frontmatter `ms.date` and optional forward pointer note if needed; append-only preferred except `ms.date`) and all existing lines of `docs/reference/log.md` remain intact; Git commit author/committer uses `{id}+{login}@users.noreply.github.com` from `gh api user` and includes `Refs #89`, `Refs #100`, `Refs #440` plus the Copilot trailer; zero network push or PR creation occurs.
  * Operating condition or verification approach: Inspect `git diff`, `git status --short`, `git log -1 --format=fuller`, and `git status -sb`.
  * Observable acceptance criteria: `git status --short` is clean after the local commit and branch remains ahead of base locally with no remote push.

## Acceptance Criteria

* Focused local unit, API, screen, browser-retry, dependency-rule, and doc/audit guard tests for Epic `#89` and Epic `#100` execute cleanly without invoking `tools/rpi-checks.py`, with exact commands, exit codes, counts, skips, and verification classes recorded.
* `docs/architecture/cutover-evidence-pack.md` preserves all existing content, updates `ms.date: 2026-11-15`, and appends complete `2026-11-15` `#440` scoped stabilization checkpoints for Epic `#89` and Epic `#100` covering provenance (with verified Git SHAs, blob SHAs, and honest draft/unsigned statuses), document-qualified traceability (with BRD/PRD numbering divergence flagged), cross-cutting governance boundaries, observed test matrix, bug/refactoring disposition, authorized Azure/human residuals, and `continue` recommendation.
* `docs/reference/README.md` (`ms.date: 2026-11-15` and index entry) and `docs/reference/log.md` (append-only `[2026-11-15]` EOF entry) are updated and pass `test_live_doc_links.py`, `tools/check-legacy-references.py`, `tools/test_epic_child_disposition_audit.py`, and Markdown/tracking hygiene checks (zero `.copilot-tracking/` references, zero em dashes, zero bolded-prefix bullets, `*` unordered lists).
* Full RPI tracking artifacts (`research`, `plan`, `phase-details`, `plan-critique`, `changes`, `review`, and `state.json`) exist under `.copilot-tracking/*/2026-11-15/`, post-implementation `rpi-review` records `Outcome: Conformant`, and all changes are committed locally on `feat/epic-89-100-stabilization-checkpoints` (`Refs #89`, `Refs #100`, `Refs #440` + Copilot trailer) without pushing or opening a PR.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-plan.md                                                |
| Phase details                    | .copilot-tracking/details/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-phase-details.md                                     |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-plan-critique.md with Revise disposition (PC-001..PC-003 resolved directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-research.md                                         |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-changes.md is created by implementation              |
| Planning execution and readiness | Complete and Ready for implementation                                                                                                    |
| Continuation context             | Confirmed automatic RPI Agent parent continues directly to rpi-implement after single-pass critique dispositions                         |

## Sources

* `.copilot-tracking/research/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-research.md`: Primary evidence (`C1`..`C37`, `W1`..`W16`) covering Git SHAs, blob SHAs, live issue/PR states, BRD/PRD/ADR requirement mappings, module/test anchors, and contrarian ancestry/guard checks.
* `docs/architecture/cutover-evidence-pack.md`: Canonical `#440` stabilization evidence pack, including the partial `2026-11-03` Epic `#89` checkpoint (lines 2477-2558) and latest `2026-11-14` `#440` checkpoint (lines 8498-8558).
* `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/brds/agentic-retrofit-programme-brd.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, and `docs/adrs/0001..0007`: Normative baseline specifications, blob SHAs, and approval statuses.
* `docs/reference/README.md` and `docs/reference/log.md`: Canonical knowledge base index and append-only changelog.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Focused Local-First Regression and Integration Execution

* Intent: Run all focused `src/core`, `src/api`, and cross-cutting regression/integration suites for Epic `#89` and Epic `#100` locally (without invoking `tools/rpi-checks.py`) and capture exact commands, exit codes, test counts, skips, and defect observations.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Execute Epic #89 Focused Core, API, Screen, and Retry Suites

* Requirement and evidence: FR-1; research `C15`..`C22`, `C37`, `W6`..`W12`, `W16`
* Expected result: Exact execution output, exit code, run count, and skip count recorded (with `src/api` included on `PYTHONPATH` so `checks.*` imports resolve cleanly from repo root) for Epic `#89` core (`test_quality_procurement.py`, `test_consultation_controls.py`, `test_job_pack.py`, `test_aftercare.py`, `test_aftercare_intake.py`, `test_aftercare_store.py`), API/screen/browser-retry suites (`test_procurement_api.py`, `test_procurement_screens.py`, `test_technical_quality_screens.py`, `test_staff_intake_api.py`, `test_staff_intake_browser.py`, `test_aftercare_screen.py`, `test_aftercare_served.py`, `test_workspace_scripts.py`), and any companion test files introduced by stacked `PR #1641` commits `#1745` (`23b675164`) and `#1770` (`d8cb35d25`).
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Execute Epic #100, Cross-Cutting Boundary, and Baseline Doc Guard Suites

* Requirement and evidence: FR-1; research `C23`..`C30`, `C33`..`C37`, `W13`..`W16`
* Expected result: Exact execution output, exit code, run count, and skip count recorded for Epic `#100` core (`test_coordinator.py`, `test_progress_event_capture.py`, `test_progress_reports.py`, `test_list_export.py`, `test_scenario_manifest.py`, `test_needs_inventory.py`, `test_ai_consumption.py`, `test_ai_consumption_safety.py`, `test_ai_consumption_skill_breakdown.py`, `test_management_tokenomics_invariant_100.py`, plus any companion tests from stacked `#1657`/`#1674`), Epic `#100` API/screen (`test_coordinator_api.py`, `test_progress_dashboard.py`, `test_progress_report_api.py`, `test_list_export_api.py`, `test_list_export_inventory.py`, `test_ai_consumption_api.py`, `test_asset_board_screen.py`, `test_management_tokenomics_api_100.py`), cross-cutting package/consent/stage-gate invariants (`test_dependency_rule.py`, `test_safety_consent_exercise_scenarios_81.py`), and baseline doc/disposition guards (`test_live_doc_links.py`, `tools/test_epic_child_disposition_audit.py`, `python3 tools/check-legacy-references.py`).
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Author Epic #89 and Epic #100 Scoped #440 Stabilization Checkpoints

* Intent: Append dated (`2026-11-15`) `#440` scoped stabilization checkpoint sections for Epic `#89` and Epic `#100` to `docs/architecture/cutover-evidence-pack.md` and update its frontmatter `ms.date`, preserving all prior sections verbatim.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Append Epic #89 Scoped Stabilization Checkpoint (2026-11-15) to cutover-evidence-pack.md

* Requirement and evidence: FR-2, FR-3, FR-4, NFR-1; research `C1`..`C23`, `W1`..`W12`, `W16`
* Expected result: `docs/architecture/cutover-evidence-pack.md` updated with `ms.date: 2026-11-15` and a complete `Epic #89` (`Refs #89, Refs #440`) `2026-11-15` stabilization section superseding the open-child caveats of the preserved `2026-11-03` partial checkpoint, containing provenance, document-qualified traceability (flagging BRD vs PRD `FR-016`/`FR-017` numbering divergence), cross-cutting boundary verification, observed `P01` test rows, bug/refactoring disposition, authorized residuals, and `continue` recommendation.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Append Epic #100 Scoped Stabilization Checkpoint (2026-11-15) to cutover-evidence-pack.md

* Requirement and evidence: FR-2, FR-3, FR-4, NFR-1; research `C1`..`C11`, `C23`..`C30`, `C33`, `C36`, `W1`..`W5`, `W13`..`W16`
* Expected result: `docs/architecture/cutover-evidence-pack.md` appended with a complete `Epic #100` (`Refs #100, Refs #440`) `2026-11-15` stabilization section covering provenance, document-qualified traceability (flagging BRD vs PRD `FR-020..FR-024`, `FR-030`, `FR-035`, `FR-052`/`FR-061` numbering divergence), cross-cutting boundary verification, observed `P01` test rows, bug/refactoring disposition, authorized Azure/human/tariff (`#432` `OD-51`/`OQ-027` open/deferred) residuals, and `continue` recommendation.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Update Knowledge Base Index and Append-Only Change Log

* Intent: Update `docs/reference/README.md` to index the `2026-11-15` Epic `#89` and Epic `#100` `#440` stabilization checkpoints and append a dated EOF entry to `docs/reference/log.md`.
* Dependencies: P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Update docs/reference/README.md and Append EOF Entry to docs/reference/log.md

* Requirement and evidence: FR-4, NFR-1, NFR-2; research `C31`, `C32`
* Expected result: `docs/reference/README.md` updated (`ms.date: 2026-11-15` and architecture evidence index note covering Epic `#89` and Epic `#100` `2026-11-15` `#440` checkpoints) and one `[2026-11-15]` entry appended strictly at EOF of `docs/reference/log.md` with zero edits to earlier log entries and zero `.copilot-tracking/` references.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-phase-details.md

<!-- rpi:phase id=P04 -->
### [x] P04: Documentation Guard Verification and Changes Reconciliation

* Intent: Validate edited `docs/` files against live-link, legacy-reference, epic-child-disposition, and Markdown/tracking hygiene guards, and reconcile implementation evidence for `rpi-review`.
* Dependencies: P03

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Run Post-Edit Link, Legacy-Reference, Disposition, and Style Guards and Reconcile Artifacts

* Requirement and evidence: FR-1, NFR-1, NFR-2; research `C34`..`C37`
* Expected result: `test_live_doc_links.py`, `tools/test_epic_child_disposition_audit.py`, diff-scoped and full-file `check-legacy-references.py` link/reference checks over edited `docs/` (`0` link or `docs/`/`src/` reference violations; pre-existing `#201` `GUARD_FILES` gap in `tools/test_epic_*.py` documented and routed as follow-up), and diff style checks (zero `.copilot-tracking/` strings in `docs/`, zero em dashes, zero bolded-prefix bullets, `*` unordered lists, append-only `log.md`) all pass with exit code `0`, and `.copilot-tracking/changes/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-changes.md` plus plan markers are reconciled.
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-phase-details.md

## Dependencies

* Local Python 3.12 test environment (`/usr/bin/python3` and `/home/azureuser/.local/bin/pytest`) with `PYTHONPATH=src/api/src:src/api/tests:src/api:src/core/src:src/agents/src:src/core/tests:src/agents/tests` (or `src/core/src:src/agents/src:src/api/src:src/api:src/core/tests:src/agents/tests:src/api/tests` when `test_mssqlstore.py` is not imported alongside `test_buildings.py`): Required to execute `src/core` and `src/api` focused test suites (including `checks.*` helpers under `src/api/checks/`) cleanly from the repository root without mutating site-packages.
* Playwright Chromium availability in local runtime (if installed) for browser-backed checks (`test_staff_intake_browser.py`, `test_workspace_scripts.py`): If Playwright browser binaries are present, run and classify as `local observed`; if any individual browser test skips cleanly due to host prerequisites, record exact skip count and reason honestly without fabricating pass status.
* Authenticated `gh` CLI (`gh api user`): Required at post-review closeout to configure privacy-safe local `user.email` (`{id}+{login}@users.noreply.github.com`) before creating the frozen local commit.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass critique (`PC-001`, Medium) | Resolved | Added `src/api` to `PYTHONPATH` in `Dependencies` and `P01`/`P04` details so `from checks.asset_urls import asset_url` in `src/api/checks/script_retry.py` resolves when running `unittest` from the repository root. |
| Single-pass critique (`PC-002`, Medium) | Resolved | Added baseline doc/disposition guard runs (`test_live_doc_links.py`, `tools/test_epic_child_disposition_audit.py`, `python3 tools/check-legacy-references.py`) in `P01-T02` and locked zero-subsequent-edit post-doc re-verification in `P04-T01` so recorded rows in `cutover-evidence-pack.md` match final post-edit execution. |
| Single-pass critique (`PC-003`, Low) | Resolved | Updated `P01-T01` and `P01-T02` to inspect `git show --name-only` for stacked `PR #1641` commits `#1745` (`23b675164`), `#1770` (`d8cb35d25`), `#1657` (`4dc285ad2`), and `#1674` (`77c7bfb18`) and execute any companion test modules alongside the primary suites. |

## Follow-Up Items

* Add `tools/test_epic_legacy_path_retirement.py` and `tools/test_epic_parity_matrix_old_paths.py` to `GUARD_FILES` in `tools/check-legacy-references.py`: Pre-existing `#201`/`#203` tooling gap from `0999ce7bf` (`PR #1610`), outside this focused documentation-and-evidence scope; restoring repo-wide `check-legacy-references.py` exit `0` is a small, high-leverage tooling hygiene task.
* Rebase parent integration branch `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) onto latest `origin/main` (`5e0c7f74432ffce73cfeaa672e4e40a605ca6274`): Outside this stacked child branch's read-only lineage scope; owned by coordinator integration to unify post-merge-base `PR #1666` (`4629e3e5c`) with `PR #1770` and `PR #1792`.
* Owner and commercial sign-off on provisional AI tariff, spend limits, and alert owners (`BRD::OD-51`, `PRD::OQ-027`, `#432`): Governance decision outside engineering stabilization; remains explicitly `"Unknown"` / `UNPRICED_PROVISIONAL_TARIFF` until owner ratification.
* Post-merge Epic `#89` and Epic `#100` criterion tick and issue closure (`#89`, `#100`, `#440`): Owned by project owner / coordinator after this stabilization PR is independently reviewed and merged to `main`.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/delivery-89-100-epic-stabilization-checkpoints-changes.md
* Ready phase or task: Complete (all `P01`..`P04` markers complete; ready for `rpi-review`)
* Remaining provisional question or blocker: None
