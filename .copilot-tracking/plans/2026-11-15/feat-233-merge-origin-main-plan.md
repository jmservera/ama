<!-- markdownlint-disable-file -->
# RPI Plan: Reconcile feat/demo-233-same-home-tensions-0825 with origin/main

## Task Metadata

* Task ID: pr-1639-feat-233-merge-origin-main
* Task slug: feat-233-merge-origin-main
* Planning status: implementation-ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/feat-233-merge-origin-main-plan-critique.md

## Executive Summary

This plan merges current `origin/main` (`45cd2bd00a593d28208f5b99053d854ababb5484`) into the parent integration branch `feat/demo-233-same-home-tensions-0825` (`a1d0be5f611eeb1f3b5bb88f996bb9448a6e72b0`, PR `#1639`) in `/home/azureuser/source/ama-demo-wt/feat-233-same-home-tensions-0825`, resolving all **10 conflicting files** through an additive, contract-preserving union. Completing this reconciliation lets PR `#1639` (Issue `#233` and its 17 completed child issues) merge cleanly with the four `origin/main` pull requests (`#1664`, `#1665`, `#1666`, `#1667`) and `#1672` without dropping any method, HTTP route, response field, audit entry, projection redaction rule, or WCAG 2.2 AA cue.

### User Decisions and Requirements Highlights

* **Continuous automatic RPI execution**: Complete `rpi-research`, `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` in one run with dated `.copilot-tracking/` artifacts, keeping all RPI artifacts inside the single local merge commit (`Refs #233` plus the Copilot `Co-authored-by` trailer) and **not pushing** to the remote.
* **Zero-drop dual-branch preservation**: Preserve every capability from `origin/main` (`#1664` determinism matrix, `#1665` allowlisted safeguarding clocks and raw `safeguarding_items` stripping, `#1666` advisory fieldwork variation routing, `#1667` structured `GateRule` refusal metadata) alongside `feat/demo-233-same-home-tensions-0825` (`#233` and all merged child commits including `#1682`/`#1725` non-instruction guards, `#1692` hazard clock accountable-owner cues, `#1757` cross-role exception recovery, and `#227`-`#232` WCAG 2.2 rebases).
* **Focused validation tier**: Validate with `src/core` and `src/api` unit test discovery (explicitly including `test_scenario_manifest.py` and `test_role_endpoint_inventory.py`), `mypy`, `ruff check`, and `ruff format --check`, without running `tools/rpi-checks.py`.

### What You May Not Know

* **Parallel implementations of `#132` and `#76` coexist across both branches**: Issue `#132` (fieldwork variation escalation) has active regression suites on both `HEAD` (`src/api/tests/test_fieldwork_variation_owner_guard.py`) and `origin/main` (`src/api/tests/test_staff_intake_api.py`), and Issue `#76` (safety and safeguarding clocks) has active suites on both `HEAD` (`src/api/tests/test_workbench_hazard_clock_owner.py`) and `origin/main` (`src/api/tests/test_safeguarding_clock_a11y.py` and `src/api/tests/test_safeguarding_detail_boundary.py`). The plan reconciles `job_pack.py`, `staff_intake.py`, `projection.py`, `store.py`, `app.js`, and `staff-intake.js` so both branches' unmodified API and UI tests pass together.
* **Live `origin/main` commit SHA**: GitHub REST API reports `origin/main` at `45cd2bd00a593d28208f5b99053d854ababb5484` (containing `#1664`-`#1667` plus `#1672` and producing the exact 10 conflicts named in scope); the parenthetically cited `89c8080cbfb1eb1c2b930c980cf3d73e0919c8e1` is not an existing commit on GitHub.
* **Single-commit artifact packaging without `git commit --amend`**: Staging the resolved merge and task-scoped tracking files during `rpi-implement` (`MERGE_HEAD` active, zero unmerged index entries), running `rpi-review` on the exact frozen staged merge tree to write `.copilot-tracking/reviews/2026-11-15/feat-233-merge-origin-main-review.md`, and finalizing `git commit` immediately afterward packages `research`, `plans`, `details`, `changes`, `reviews`, and `rpi-sessions` into the single merge commit cleanly without history rewriting.

### Unresolved Decisions or Blockers

* None blocking local merge reconciliation, focused validation, review, or local merge commit creation. Pushing PR `#1639` remains intentionally excluded per caller instruction.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop continuously in a single run (`rpi-research`, `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, `rpi-review`) without pausing after `rpi-plan`, writing dated artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `changes`, `reviews`).
* Work in `/home/azureuser/source/ama-demo-wt/feat-233-same-home-tensions-0825` on branch `feat/demo-233-same-home-tensions-0825` (`PR #1639` targeting `main`).
* Run `git merge --no-commit origin/main` (resolved against fetched live `origin/main` `45cd2bd00a593d28208f5b99053d854ababb5484` per `.copilot-tracking/research/2026-11-15/feat-233-merge-origin-main-research.md` `C1`).
* Resolve all 10 conflicting files (`src/api/README.md`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/staff-intake.js`, `src/api/tests/test_role_endpoint_inventory.py`, `src/core/README.md`, `src/core/src/zava_forward/core/job_pack.py`, `src/core/src/zava_forward/core/projection.py`, `src/core/src/zava_forward/core/staff_intake.py`, `src/core/src/zava_forward/core/store.py`, `src/core/tests/test_job_pack.py`), preserving both `origin/main` (`#1664`, `#1665`, `#1666`, `#1667`) and `feat/demo-233-same-home-tensions-0825` (`#233` and 49 merged child commits) functionality without dropping any methods, routes, or fields.
* Update `SCENARIO_MANIFEST_RECIPE_SHA256` in `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` if `workbench_DomChecks.mjs` or manifest-tracked files changed, and ensure `test_scenario_manifest.py` and `test_role_endpoint_inventory.py` pass.
* Validate at the Focused tier (`src/core` and `src/api` unit tests, `mypy`, `ruff check`, `ruff format --check`) and do NOT run `tools/rpi-checks.py`.
* Follow AMA Repository Instructions for web edits (`web-design-guidelines` skill loaded and live source fetched before editing `app.js` and `staff-intake.js`, then refreshed and audited before review closeout) and commit hygiene (repository-local privacy-safe `user.email` via `gh api user`, no `.copilot-tracking/` paths cited in the commit message text).
* Complete the local merge commit including the `.copilot-tracking/` RPI artifacts (`research`, `plans`, `details`, `changes`, `reviews`) with `Refs #233` and trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and do NOT push.

## Goals

* Reconcile `feat/demo-233-same-home-tensions-0825` with `origin/main` cleanly so all 10 merge conflicts are resolved without losing any capability, field, route, audit record, redaction boundary, or accessibility cue from either branch.
* Prove cross-branch compatibility across `#132` fieldwork variation escalations, `#76` hazard and safeguarding clocks, `#82` structured `GateRule` refusals, `#135` exception recovery inventory, `#227`-`#232` WCAG 2.2 AA baselines, and synthetic scenario manifest provenance under focused local validation.
* Produce a complete, auditable `.copilot-tracking/` RPI record (`research`, `plans`, `details`, `changes`, `reviews`, and `rpi-sessions` state) committed inside the single local merge commit without pushing.

## Scope and Non-Goals

### In Scope

* Initiating `git merge --no-commit origin/main` in `/home/azureuser/source/ama-demo-wt/feat-233-same-home-tensions-0825`.
* Resolving all 10 conflicting files across `src/core` and `src/api`.
* Verifying `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` against `src/core/src/zava_forward/core/synthetic/scenario_manifest.py` tracked sources and updating hashes only if a tracked source changed.
* Loading and fetching `web-design-guidelines` prior to editing `src/api/src/zava_forward/api/web/app.js` and `src/api/src/zava_forward/api/web/staff-intake.js`, and refreshing/reviewing those files during `rpi-review`.
* Running `src/core` and `src/api` unit test suites, `mypy`, `ruff check`, and `ruff format --check`.
* Authoring `.copilot-tracking/` RPI artifacts and completing the local two-parent merge commit with privacy-safe git author identity, `Refs #233`, and the Copilot trailer.

### Non-Goals

* Pushing any commit or branch to `origin` or mutating PR `#1639` on GitHub.
* Running `tools/rpi-checks.py` or generating an external full-gate receipt.
* Modifying non-conflicting production or test files unless focused validation exposes a genuine post-merge semantic integration defect caused by combining `HEAD` and `origin/main`.
* Rewriting git history (`rebase`, `commit --amend`, `reset --hard`, or `push --force`).

## Functional Requirements

* Fieldwork variation and concern escalation (`#132`) across `job_pack.py`, `staff_intake.py`, `projection.py`, and `staff-intake.js` preserves both branches' helpers, non-instruction guards, owner validation, persistence keys, audit actions, and UI behaviors.
  * Observable acceptance criteria: `job_pack` exposes `NON_INSTRUCTION_NOTICE`, `INSTRUCTION_CLAIMS`, `ADVISORY_NOTE`, `named_owner`, `assert_advisory`, `reject_instruction_claim`, and `escalation` returning both `note` and `contract_notice` plus `contract_instruction=False`, `is_contract_instruction=False`, and `acts_as_contract_instruction=False`; `staff_intake` exposes `escalation_destination`, `route_escalation`, `view` (including `"escalation": escalation_destination()`, `escalation_options`, `boundaries`, and deduplicated redacted `escalations` preserving `acts_as_contract_instruction`, `is_contract_instruction`, `contract_notice`, `raised_by_email`, and `raised_at` via `_view_escalation`, plus `field_escalations` compatibility), and `escalate` (validating instruction claims, open case/non-withdrawn order, placeholder/role-word/dotted-initial owners, configured env fallback with optional `contact`, and rejecting directory-member role mismatches when `owner["name"]` exists in `store._quality_staff()` without holding `owner["role"]`, persisting distinct dict copies to `escalations` and `field_escalations`, recording `field_escalation_raised` and `field_escalation_routed`, and returning both `"escalation"` and `#1682` compatibility keys); `test_job_pack.py`, `test_staff_intake_api.py`, and `test_fieldwork_variation_owner_guard.py` pass without error.
* Hazard clocks, safeguarding clocks, raw safeguarding detail stripping (`#76`), and structured `GateError` refusal rules (`#82`) compose cleanly across `projection.py`, `store.py`, and `app.js`.
  * Observable acceptance criteria: `projection.hold_notes` and `projection.redact_staff_detail` strip `safeguarding_items` while `hold_notes` matches `("kind" in c or "escalation_kind" in c)` advisory escalation dicts, replaces escalation `summary` with `NOTE_HELD`, and preserves both `note` and `contract_notice`; `Store.require_safety_clear` formats `taskqueues.accountable_owner(active.get("owner"))` and passes `[gates.BOOKING_RULES["safety"]]` to `GateError`; `app.js` `workSummary` renders both `(work.hazard_clocks || [])` (with `clock_text` and `accountable_owner`) and `(work.safeguarding_clocks || [])`; `test_workbench_hazard_clock_owner.py`, `test_safeguarding_clock_a11y.py`, `test_safeguarding_detail_boundary.py`, and `test_gates.py` pass.
* Role endpoint inventory, scenario manifest provenance, and module documentation reflect the combined `HEAD` + `origin/main` surface.
  * Observable acceptance criteria: `test_role_endpoint_inventory.py` includes both `("/api/workorders/WO-0001/field-escalate", {})` and `("/api/exceptions/recovery", {})` in `POST_ENDPOINTS` and passes; `test_scenario_manifest.py` and `test_generator_determinism_matrix.py` pass; `src/core/README.md` and `src/api/README.md` accurately describe the advisory non-instruction `field-escalate` contract with zero conflict markers.
* Frozen merge candidate staging and post-review local merge commit completion record the reconciled code and this task's RPI tracking artifacts in one merge commit without pushing.
  * Observable acceptance criteria: `rpi-implement` leaves `MERGE_HEAD` (`45cd2bd00a593d28208f5b99053d854ababb5484`) cleanly staged with verified `GIT_AUTHOR_IDENT` and `GIT_COMMITTER_IDENT` (`{id}+{login}@users.noreply.github.com`); after `rpi-review` writes `.copilot-tracking/reviews/2026-11-15/feat-233-merge-origin-main-review.md`, the parent loop stages this task's review and state artifacts and creates a single two-parent merge commit of `a1d0be5f611eeb1f3b5bb88f996bb9448a6e72b0` and `45cd2bd00a593d28208f5b99053d854ababb5484` containing `Refs #233` (zero closing keywords, even negated, and zero `.copilot-tracking/` path strings in the commit message) and the `Co-authored-by: Copilot` trailer, `git status --short` has zero modified/staged task files, and `git status -sb` shows the branch ahead of `origin/feat/demo-233-same-home-tensions-0825` by 1 unpushed commit.

## Non-Functional Requirements

* Zero unresolved git conflict markers or whitespace errors across the repository.
  * Objective threshold or evaluation condition: `git ls-files -u` returns empty output, `git diff --cached --check` returns exit code `0`, and conflict-marker regex search across `src/` and `docs/` finds `0` matches.
  * Operating condition or verification approach, if needed: Checked on staged merge index before validation and again before post-review `git commit`.
  * Observable acceptance criteria: Clean git index and resolved files with zero conflict markers.
* Static type safety, formatting, linting, WCAG 2.2 AA baseline counters, and plain-language content compliance.
  * Objective threshold or evaluation condition: Worktree-isolated `mypy` across `src/core` and `src/api` exits `0`; `ruff check` and `ruff format --check` across `src/core` and `src/api` exit `0`; `test_accessibility_baseline.py` (`aria-invalid` sites `== 9`, `h("table", {})` `== 14`), `test_epic149_form_error_summary_associations.py`, and `test_content_standard.py` pass; `web-design-guidelines` audit reports zero open violations on changed web lines.
  * Operating condition or verification approach, if needed: Executed directly with worktree-local `PYTHONPATH`/`MYPYPATH` using `/usr/bin/python3`, `/home/azureuser/.local/bin/mypy`, `/home/azureuser/.local/bin/ruff`, and Node v24.21.0 without mutating shared editable installs.
  * Observable acceptance criteria: Zero unit test failures, zero `mypy` errors, and zero `ruff` diagnostics across `src/core` and `src/api`.
* Test ownership and target lock (pre-critique invariant).
  * Objective threshold or evaluation condition: Canonical modified source targets are locked to the 10 conflicting files (plus `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` only if a tracked source digest changed, currently `0` digest changes expected per `C15`). Test removals: `none` (`0` test methods removed; all 5 methods in `src/core/tests/test_job_pack.py` and both route tuples in `src/api/tests/test_role_endpoint_inventory.py` retained). Maximum new test method additions: `2` focused cross-branch assertions in `src/core/tests/test_job_pack.py` if needed, `0` required when combined existing methods cover both semantic advisory/non-instruction contracts and regression boundaries. Generated targets modified: `none`.
  * Operating condition or verification approach, if needed: Verified via `git diff HEAD -- src/core/tests src/api/tests` and `git diff MERGE_HEAD -- src/core/tests src/api/tests`.
  * Observable acceptance criteria: Every pre-existing test method from both `HEAD` and `origin/main` remains present and passes (`semantic` coverage via `test_fieldwork_variation_owner_guard.py`, `test_staff_intake_api.py`, `test_safeguarding_clock_a11y.py`, `test_safeguarding_detail_boundary.py`, `test_workbench_hazard_clock_owner.py`; `regression` coverage via `test_role_endpoint_inventory.py`, `test_scenario_manifest.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, and full `src/core`/`src/api` discovery).

## Acceptance Criteria

* `git merge --no-commit origin/main` is reconciled across all 10 conflicting files with zero dropped methods, routes, or fields from either `origin/main` or `feat/demo-233-same-home-tensions-0825`.
* `test_job_pack.py`, `test_staff_intake_api.py`, `test_fieldwork_variation_owner_guard.py`, `test_workbench_hazard_clock_owner.py`, `test_safeguarding_clock_a11y.py`, `test_safeguarding_detail_boundary.py`, `test_role_endpoint_inventory.py`, `test_scenario_manifest.py`, `test_generator_determinism_matrix.py`, `test_accessibility_baseline.py`, and `test_content_standard.py` all pass within full `src/core` and `src/api` unittest discovery.
* `mypy`, `ruff check`, and `ruff format --check` exit `0` across `src/core` and `src/api`.
* `web-design-guidelines` rules are fetched before editing `app.js` and `staff-intake.js`, and refreshed/audited with `file:line` findings during `rpi-review`.
* Dated RPI artifacts exist under `.copilot-tracking/research/2026-11-15/`, `.copilot-tracking/plans/2026-11-15/`, `.copilot-tracking/details/2026-11-15/`, `.copilot-tracking/reviews/plans/2026-11-15/`, `.copilot-tracking/changes/2026-11-15/`, `.copilot-tracking/reviews/2026-11-15/`, and `.copilot-tracking/rpi-sessions/2026-11-15/`.
* A single local two-parent merge commit with privacy-safe git author/committer identity, `Refs #233` (no closing keywords, even negated, and no `.copilot-tracking/` path strings in the commit message), and the Copilot `Co-authored-by` trailer includes all resolved merge changes and this task's `.copilot-tracking/` artifacts, and remains unpushed.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/feat-233-merge-origin-main-plan.md                                                                    |
| Phase details                    | .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md                                                         |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/feat-233-merge-origin-main-plan-critique.md (Complete, Revise; PC-001 through PC-004 applied) |
| Relevant research                | .copilot-tracking/research/2026-11-15/feat-233-merge-origin-main-research.md                                                             |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/feat-233-merge-origin-main-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete; implementation-ready after applying single-pass critique findings PC-001 through PC-004                                        |
| Continuation context             | Confirmed automatic RPI Agent parent return: automatically advances to rpi-implement and rpi-review                                      |

## Sources

* .copilot-tracking/research/2026-11-15/feat-233-merge-origin-main-research.md: Primary 3-wave codebase evidence (`C1`-`C16`) covering branch divergence, all 10 diff3 conflict blocks, dual `#132` and `#76` test contracts, WCAG/content-standard invariants, scenario manifest hashes, and local runners.
* docs/case_study_48_original.md: Baseline business challenge and governance framing preserved across Zava North Homes role screens.
* docs/case_study_48_addendum.md: Validated human-approval, non-contract-instruction, safeguarding redaction, and WCAG 2.2 AA boundaries.
* docs/reference/research/ux/wcag-conformance-baseline.md: Non-colour status cue, keyboard, focus, and semantic structure baseline enforced by `src/api/tests/test_accessibility_baseline.py`.
* docs/reference/research/ux/content-standard.md: Plain-language named-owner/next-action error rules enforced by `src/api/tests/test_content_standard.py`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Initiate merge and reconcile `src/core` conflicts

* Intent: Start `git merge --no-commit origin/main` and resolve all 6 `src/core` conflicting files so `#132` fieldwork variation escalations, `#76` hazard and safeguarding redactions, and `#82` structured `GateError` safety rules satisfy both branches' contracts.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Start no-commit merge and verify the 10-file conflict boundary

* Requirement and evidence: Caller Scope item 1 and `.copilot-tracking/research/2026-11-15/feat-233-merge-origin-main-research.md` (`C1`, `C14`)
* Expected result: `git merge --no-commit origin/main` creates `MERGE_HEAD` (`45cd2bd00a593d28208f5b99053d854ababb5484`) with the exact 10 unmerged paths and clean auto-merges elsewhere.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Reconcile `job_pack.py`, `staff_intake.py`, `projection.py`, and `test_job_pack.py`

* Requirement and evidence: Caller Scope item 2 and `.copilot-tracking/research/2026-11-15/feat-233-merge-origin-main-research.md` (`C6`, `C7`, `C8`, `C10`, `C12`)
* Expected result: Unified advisory non-instruction escalation schema, owner validation (placeholder/role-word/dotted-initial rejection + configured env fallback + staff-directory role check), dual `escalations`/`field_escalations` persistence with held-summary projection and preserved `note`/`contract_notice`, `safeguarding_items` stripping, dual audit events, and all 5 `test_job_pack.py` test methods passing.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Reconcile `store.py` and `src/core/README.md`

* Requirement and evidence: Caller Scope item 2 and `.copilot-tracking/research/2026-11-15/feat-233-merge-origin-main-research.md` (`C5`, `C9`)
* Expected result: `Store.require_safety_clear` combines `taskqueues.accountable_owner(active.get("owner"))` with `[gates.BOOKING_RULES["safety"]]`, `src/core/README.md` documents the reconciled `field-escalate` contract, and all 6 `src/core` conflicts are staged cleanly.
* Detail section: P01-T03 in .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Reconcile `src/api` web, endpoint-inventory, and README conflicts

* Intent: Load `web-design-guidelines`, fetch its live rules, and resolve all 4 `src/api` conflicting files while preserving WCAG 2.2 AA baseline counters, plain-language error copy rules, Node-VM role-screen behavior, and endpoint inventory coverage.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Fetch `web-design-guidelines` and reconcile `web/app.js` and `web/staff-intake.js`

* Requirement and evidence: AMA Web Development Guidance, Caller Scope item 2, and `.copilot-tracking/research/2026-11-15/feat-233-merge-origin-main-research.md` (`C2`, `C3`, `C11`, `C12`, `C13`)
* Expected result: `app.js` renders both `hazard_clocks` (`clock_text` + `accountable_owner`) and `safeguarding_clocks`; `staff-intake.js` renders `Raise a variation or concern` with per-order input IDs, optional configured-owner fallback, `Owner status` field, and fail-closed `intakeNotInstruction` table without triggering `BLOCKED_WORDS` or changing `aria-invalid`/`table` counts.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile `tests/test_role_endpoint_inventory.py` and `src/api/README.md`

* Requirement and evidence: Caller Scope items 2 and 3 and `.copilot-tracking/research/2026-11-15/feat-233-merge-origin-main-research.md` (`C4`, `C5`)
* Expected result: `POST_ENDPOINTS` includes both `/api/workorders/WO-0001/field-escalate` and `/api/exceptions/recovery`, `src/api/README.md` documents the reconciled `field-escalate` behavior, and all 10 conflicted files are staged with `git ls-files -u` empty.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Verify scenario manifest, run focused validation suite, and stage frozen merge candidate

* Intent: Verify `scenario-manifest.json` provenance digests, execute the complete Focused validation tier (`src/core` tests, `src/api` tests, `mypy`, `ruff check`, `ruff format --check`) with worktree-local module isolation, configure and verify repository-local privacy-safe git author/committer identity, and stage the clean frozen merge candidate (`MERGE_HEAD` + task-scoped tracking files) for `rpi-review` and post-review local merge commit creation.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Verify `scenario-manifest.json` and execute worktree-isolated `src/core` + `src/api` unit tests, `mypy`, and `ruff`

* Requirement and evidence: Caller Scope items 3 and 4 and `.copilot-tracking/research/2026-11-15/feat-233-merge-origin-main-research.md` (`C14`, `C15`, `C16`)
* Expected result: `test_scenario_manifest.py`, `test_generator_determinism_matrix.py`, `test_role_endpoint_inventory.py`, full worktree-isolated `src/core` and `src/api` unittest discovery, `mypy`, `ruff check`, and `ruff format --check` all exit `0` with zero conflict markers (`git diff --cached --check` exits `0`).
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Configure privacy-safe git identity, finalize changes record, and stage frozen merge candidate for `rpi-review`

* Requirement and evidence: Caller Scope items 2 and 3 and AMA Branch and Pull Request Workflow instructions
* Expected result: Repository-local `user.email` (and `user.name` if unset) uses `{id}+{login}@users.noreply.github.com` from `gh api user`, verified via `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT`; `.copilot-tracking/changes/2026-11-15/feat-233-merge-origin-main-changes.md` is complete; only resolved merge files and this task's `feat-233-merge-origin-main-*` `.copilot-tracking/` files are staged on `MERGE_HEAD` with `git ls-files -u` empty and `git diff --cached --check` exiting `0`, ready for `rpi-review` to write `.copilot-tracking/reviews/2026-11-15/feat-233-merge-origin-main-review.md` and finalize the local unpushed merge commit.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/feat-233-merge-origin-main-phase-details.md

## Dependencies

* Fetched `origin/main` ref (`45cd2bd00a593d28208f5b99053d854ababb5484`): Supplies the incoming commits from `#1664`, `#1665`, `#1666`, `#1667`, and `#1672`.
* Local Python 3.12.3, Node v24.21.0, `mypy`, and `ruff`: Required to run unit tests (including Node VM harnesses in `src/api/tests/`), static typing, and formatting/linting checks.
* `web-design-guidelines` skill and live rules URL (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`): Required by AMA Web Development Guidance before editing `web/app.js` and `web/staff-intake.js` and again before `rpi-review`.
* Authenticated `gh` CLI (`gh api user`): Required to set repository-local privacy-safe `git config --local user.email` before creating the merge commit.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass critique (`PC-001` [High]: Dual-contract omissions across `staff_intake.py`, `staff-intake.js`, and `app.js`) | applied | Specified `"escalation": escalation_destination()`, `_view_escalation` preservation of `acts_as_contract_instruction`/`is_contract_instruction`/`contract_notice`/`raised_by_email`/`raised_at`, distinct-copy dual persistence + fallback deduplication, `escalation_kind` hold check in `projection.py`, exact `_quality_staff()` mismatch predicate + combined `escalate()` return keys, and null-safe `data.escalation` / `(work.hazard_clocks \|\| [])` expressions across Functional Requirement 1, `P01-T02`, and `P02-T01`. |
| Single-pass critique (`PC-002` [High]: Review output path mismatch against Caller Req 5) | applied | Updated all review artifact pointers in the plan and phase details to `.copilot-tracking/reviews/2026-11-15/feat-233-merge-origin-main-review.md`. |
| Single-pass critique (`PC-003` [High]: Stage-boundary inversion in `P03-T02` and staging/commit-hygiene gaps) | applied | Scoped `P03-T02` strictly to `rpi-implement` frozen-candidate staging (with `git diff --cached --check`, `GIT_AUTHOR_IDENT`/`GIT_COMMITTER_IDENT` verification, and task-scoped `feat-233-merge-origin-main-*` staging), leaving `.copilot-tracking/reviews/2026-11-15/feat-233-merge-origin-main-review.md` creation and final local `git commit` (`Refs #233`, zero closing keywords even negated, zero `.copilot-tracking/` message paths, Copilot trailer, no push) to the post-implementation `rpi-review` boundary. |
| Single-pass critique (`PC-004` [Medium]: Missing worktree-local `PYTHONPATH`/`MYPYPATH` isolation for `src/api`) | applied | Added explicit worktree-local `PYTHONPATH` and `MYPYPATH` invocations in `P02` and `P03-T01` so `src/api` unittest discovery and `mypy` evaluate the reconciled worktree rather than shared site-packages. |

## Follow-Up Items

* Push the reconciled merge commit on `feat/demo-233-same-home-tensions-0825` to `origin` (`PR #1639`) and observe hosted CI once the owner or coordinator requests remote publication (outside immediate scope per explicit `"Do NOT push to remote"` caller instruction; owner: repository owner / coordinator).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/feat-233-merge-origin-main-changes.md
* Review artifact: .copilot-tracking/reviews/2026-11-15/feat-233-merge-origin-main-review.md (followed immediately by post-review local merge commit of the frozen candidate without pushing)
* Ready phase or task: Complete (`P01`-`P03` checked; ready for `rpi-review`)
* Remaining provisional question or blocker: none
