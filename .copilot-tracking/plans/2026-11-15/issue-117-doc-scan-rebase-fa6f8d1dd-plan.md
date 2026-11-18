<!-- markdownlint-disable-file -->
# RPI Plan: Issue #117 Document Scan Rebase Continuation onto fa6f8d1dd

## Task Metadata

* Task ID: issue-117-doc-scan-rebase-fa6f8d1dd
* Task slug: issue-117-doc-scan-rebase-fa6f8d1dd
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan-critique.md

## Executive Summary

This plan executes the **rebase-continuation RPI loop** for `feat/demo-117-doc-scan` (candidate commit `4d91dae33`, anchored on `243764945`) onto the updated integration tip `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`, incorporating PR #1773 `36aeddae3`, PR #1768 `f71331d42`, and PR #1774 `fa6f8d1dd`).

Read-only `git merge-tree` verification confirmed that out of four overlapping files (`chat_case_answers.py`, `projection.py`, `store.py`, and `taskqueues.py`), three auto-merge cleanly and `src/core/src/zava_forward/core/store.py` (`Store.focus`) is the sole merge conflict. Implementation replays `4d91dae33` onto `fa6f8d1dd`, resolves `Store.focus` by preserving **both** `#76`'s `staff_list` + `self._open_safety_items(c, staff=staff_list)` safety projection and `#117`'s `is_available_case_document(d)` quarantine filter, runs focused validation (`ruff check .`, `ruff format --check .`, `mypy`, and the `#117` document malware scan quarantine unit tests plus `#76` and endpoint-inventory regression checks in `src/core` and `src/api` using worktree-local `PYTHONPATH`), updates `#117` tracking records, and commits the finalized `.copilot-tracking/` artifacts locally after single-pass `rpi-review` without pushing so `git status --short` is empty.

### User Decisions and Requirements Highlights

* Fetch `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`) and rebase `feat/demo-117-doc-scan` (`4d91dae33`) onto `origin/feat/demo-164-chat-grounding-provenance-0900`.
* Run focused validation (`ruff check .`, `ruff format --check .`, `mypy`, and the `#117` document malware scan quarantine tests in `src/core` and `src/api`) on the rebased HEAD.
* Leave `git status --short` empty and do not push.

### What You May Not Know

* Shared host user-site `pip` editable links point to another worktree (`feat-164-chat-revocation-0042`). Prepending worktree-local `PYTHONPATH` (and verifying `zava_forward.core.__file__` resolves inside `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan`) guarantees validation tests the rebased HEAD without overwriting concurrent worktrees' shared packages.
* Keeping tracked `#117` files unmodified until `git rebase --continue` succeeds avoids unstaged-tree rebase errors, and committing all `.copilot-tracking/` updates immediately after post-Review state persistence ensures `git status --short` exits completely empty without amending the rebased feature commit.

### Unresolved Decisions or Blockers

* None. All merge hunks, environment isolation paths, and focused validation commands are verified from workspace evidence (`C1`–`C8`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Continue the RPI loop (`hve-core-all:rpi-agent`) in `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan` on branch `feat/demo-117-doc-scan` for GitHub issue #117 starting from clean committed candidate `4d91dae33` (caller prompt).
* Fetch `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`) and rebase `feat/demo-117-doc-scan` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (caller Step 1).
* Resolve the single 3-way merge conflict in `src/core/src/zava_forward/core/store.py` (`Store.focus`) by preserving both `#76` open safety item projection (`self._open_safety_items`) and `#117` clean-document availability filtering (`is_available_case_document`) while keeping `server.py` HTTP routes untouched (research `C2`, `C3`; parent confirmed decisions).
* Run focused validation (`ruff check .`, `ruff format --check .`, `mypy`, and the `#117` document malware scan quarantine tests in `src/core` and `src/api`) on the rebased HEAD (caller Step 2).
* Leave `git status --short` empty and do not push (caller Step 2; repository privacy-safe noreply email and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` conventions).

## Goals

* Replay `4d91dae33` cleanly onto `fa6f8d1dd` (`origin/feat/demo-164-chat-grounding-provenance-0900`) preserving 100% of `#215` (#1773), `#76` (#1768), `#216` (#1774), and `#117` document malware scan quarantine semantics.
* Prove post-rebase conformance across `ruff check .`, `ruff format --check .`, `mypy`, and `#117` document malware scan quarantine unit tests (plus `#76` `Store.focus` safety clock/owner and endpoint-inventory regression checks) in `src/core` and `src/api`, isolated to this worktree.
* Record reconciled `#117` and child rebase-continuation `.copilot-tracking/` artifacts in a clean local tracking commit with privacy-safe noreply identity so `git status --short` is empty and nothing is pushed.

## Scope and Non-Goals

### In Scope

* Rebasing `feat/demo-117-doc-scan` (`4d91dae33`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`) and resolving `Store.focus` in `src/core/src/zava_forward/core/store.py` (plus adjusting import sorting in auto-merged `taskqueues.py` only if `ruff check .` flags `I001`).
* Running `ruff check .`, `ruff format --check .`, and `mypy` in both `src/core` and `src/api`, and running the `#117` document malware scan quarantine unit tests in `src/core` (`test_document_rescan.py`, `test_resident_documents.py`, `test_technical_evidence_usability.py`, `test_documents.py`) and `src/api` (`test_document_controls.py`, `test_role_endpoint_inventory.py`), plus `#76` `Store.focus` regression check (`test_hazard_safeguarding_clock_owner.py`) and `tools/rename-zava-tests.py`.
* Updating parent `#117` `.copilot-tracking/` changes, review, and state records with the rebased base (`fa6f8d1dd`) and rebased feature SHA, completing single-pass `rpi-review`, and committing all `.copilot-tracking/` updates locally.

### Non-Goals

* Adding or modifying HTTP routes in `src/api/src/zava_forward/api/server.py`.
* Running `tools/rpi-checks.py` or overwriting shared `~/.local` editable `pip` installs.
* Pushing to `origin` or mutating remote branches or pull requests.

## Functional Requirements

* **FR-REB-01 (Clean Rebase onto `fa6f8d1dd` & `Store.focus` Union Resolution)**: `feat/demo-117-doc-scan` contains `fa6f8d1dd` in its ancestry (`git merge-base --is-ancestor fa6f8d1dd HEAD`), auto-merges `chat_case_answers.py`, `projection.py`, and `taskqueues.py`, and resolves `Store.focus` in `src/core/src/zava_forward/core/store.py` so `open_h` uses `self._open_safety_items(c, staff=staff_list)` (`#76`) and `ev` filters `c["documents"]` with `is_available_case_document(d)` (`#117`).
  * Observable acceptance criteria: Rebased feature commit sits directly atop `fa6f8d1dd`, zero conflict markers remain (`git diff --check` exits `0`), and `server.py` has zero diff against `fa6f8d1dd`.
* **FR-REB-02 (Reconciled `#117` & Rebase Tracking Lineage)**: During `rpi-implement` (`P03-T01`), parent `#117` `.copilot-tracking/` changes, review, and state artifacts are appended/updated with the rebased base `fa6f8d1dd`, rebased feature commit SHA, and post-rebase focused validation evidence while explicitly preserving the original `#117` `Residual work` (`RV-001`) Review outcome, and child `issue-117-doc-scan-rebase-fa6f8d1dd-changes.md` and plan markers are reconciled cleanly for `rpi-review`. Immediately after single-pass `rpi-review` writes its review artifact and parent `RPI Agent` transitions state to `Follow-up`, all 10 updated parent and child `.copilot-tracking/` artifacts are committed locally by the parent `RPI Agent` closeout step so `git status --short` is empty.
  * Observable acceptance criteria: Pre-Review (`P03-T01`), `python3 -m json.tool` passes on both state JSON files, original `#117` `Residual work` (`RV-001`) outcome remains intact, and zero non-`.copilot-tracking/` files are dirty; at parent `RPI Agent` post-Review closeout, `git status --short` outputs empty string.

## Non-Functional Requirements

* **NFR-REB-01 (Worktree-Isolated Focused Validation)**: Static analysis and `#117` malware scan quarantine unit tests run against `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan` without mutating shared `~/.local` packages.
  * Objective threshold or evaluation condition: Exit code `0` on PEP 420 namespace `zava_forward.{core,agents,api}.__path__` worktree prefix assertion, `ruff check .`, `ruff format --check .`, and `mypy` in both `src/core` and `src/api` (inside an ephemeral `PYTHONNOUSERSITE=1` venv matching `src-ci.yml` editable layout), plus `#117` quarantine test suites (`test_document_rescan`, `test_resident_documents`, `test_technical_evidence_usability`, `test_documents`, `test_document_controls`), `#76` `Store.focus` suite (`test_hazard_safeguarding_clock_owner`), `test_role_endpoint_inventory`, and `tools/rename-zava-tests.py`.
  * Operating condition or verification approach: Direct CLI execution in `src/core` and `src/api` with ephemeral `PYTHONNOUSERSITE=1` venv / worktree-prepended `PYTHONPATH`.
  * Observable acceptance criteria: Zero test failures, lint violations, formatting diffs, or `mypy` errors.
* **NFR-REB-02 (Local Git Hygiene, Privacy-Safe Author, and No-Push Boundary)**: Repository-local `user.email` uses `{id}+{login}@users.noreply.github.com` from `gh api user`, commits carry `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without referencing internal tracking paths in commit messages, and zero remote writes occur.
  * Objective threshold or evaluation condition: At parent `RPI Agent` post-Review closeout, `git status --short` is empty; `git log` shows `fa6f8d1dd` followed by the rebased feature commit and clean tracking commit with noreply author and `Co-authored-by` trailer; no `git push` executed.
  * Operating condition or verification approach: Verified via `git status --short` and `git --no-pager log -n 3` at parent closeout.
  * Observable acceptance criteria: Clean frozen local branch ready for coordinator inspection.

## Acceptance Criteria

* AC1: `feat/demo-117-doc-scan` is rebased onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`), resolving `Store.focus` in `src/core/src/zava_forward/core/store.py` to retain both `self._open_safety_items(c, staff=staff_list)` and `is_available_case_document(d)` with zero `server.py` route changes.
* AC2: Worktree-isolated focused validation passes (exit `0`) on rebased HEAD (with `zava_forward.{core,agents,api}.__path__` verified under `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan/`): `ruff check .`, `ruff format --check .`, and `mypy` in `src/core` and `src/api`; `#117` quarantine tests in `src/core` (`test_document_rescan`, `test_resident_documents`, `test_technical_evidence_usability`, `test_documents`) and `src/api` (`test_document_controls`); plus `test_hazard_safeguarding_clock_owner`, `test_role_endpoint_inventory`, and `tools/rename-zava-tests.py`.
* AC3: `P03-T01` reconciles parent `#117` records (preserving original `Residual work` / `RV-001` Review outcomes) and child `issue-117-doc-scan-rebase-fa6f8d1dd` pre-Review artifacts with the rebased SHA, `fa6f8d1dd` base, and validation results (`python3 -m json.tool` and `git diff --check` exit `0`), ready for single-pass `rpi-review`.
* AC4: At parent `RPI Agent` post-Review closeout (after `rpi-review` writes `-review.md` and state transitions to `Follow-up`), all 10 updated parent and child `.copilot-tracking/` artifacts are committed locally with privacy-safe noreply email and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, `git status --short` is empty, and nothing is pushed.

## Test Ownership and Change Budget Lock

* Canonical production targets:
  * `src/core/src/zava_forward/core/store.py` (resolve single rebase merge conflict in `Store.focus`)
  * `src/core/src/zava_forward/core/chat_case_answers.py`, `src/core/src/zava_forward/core/projection.py`, `src/core/src/zava_forward/core/taskqueues.py` (git 3-way auto-merge during rebase; import-sort touch in `taskqueues.py` only if `ruff` requires it)
* Canonical test targets: `none` (existing `#117`, `#76`, and endpoint-inventory tests in `4d91dae33` and `fa6f8d1dd` carry no rebase conflicts and require zero edits)
* Generated targets: `none`
* Exact test removals: `none`
* Maximum test files touched/added: `0`
* Semantic vs regression coverage:
  * Semantic coverage: `#117` document malware scan quarantine tests (`test_document_rescan.py`, `test_resident_documents.py`, `test_technical_evidence_usability.py`, `test_documents.py` in `src/core/tests`; `test_document_controls.py` in `src/api/tests`) plus `#76` safety clock/owner tests (`test_hazard_safeguarding_clock_owner.py` in `src/core/tests`) exercising the merged `Store.focus` and `taskqueues.context` paths.
  * Regression coverage: `ruff check .`, `ruff format --check .`, and `mypy` in `src/core` and `src/api`, `test_role_endpoint_inventory.py` in `src/api/tests`, and `python3 tools/rename-zava-tests.py`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan.md                                     |
| Phase details                    | .copilot-tracking/details/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-phase-details.md                          |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan-critique.md (`Revise`; `PC-001` and `PC-002` applied directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-research.md (`C1`–`C8`)                  |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-changes.md is created by implementation   |
| Planning execution and readiness | Complete; Ready for implementation                                                                                 |
| Continuation context             | Parent return to confirmed automatic `RPI Agent`                                                                   |

## Sources

* .copilot-tracking/research/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-research.md: Verifies `243764945..fa6f8d1dd` commits, 4-file overlap, single `Store.focus` conflict in `store.py`, auto-merge orthogonality, shared-host `PYTHONPATH` isolation, and post-Review clean tracking commit (`C1`–`C8`).
* .copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md & .copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md: Parent `#117` artifacts rebased onto `fa6f8d1dd` and updated post-rebase.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Rebase Branch onto fa6f8d1dd and Resolve Store.focus Conflict

* Intent: Configure repository-local privacy-safe git email, replay `4d91dae33` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`), and resolve the single merge conflict in `src/core/src/zava_forward/core/store.py`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Configure local privacy-safe git email, rebase onto fa6f8d1dd, and resolve Store.focus in store.py

* Requirement and evidence: `FR-REB-01`, `NFR-REB-02`; research `C1`–`C6`
* Expected result: `feat/demo-117-doc-scan` sits cleanly atop `fa6f8d1dd` with `Store.focus` retaining both `self._open_safety_items(c, staff=staff_list)` and `is_available_case_document(d)`, zero conflict markers, and untouched `server.py`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Execute Worktree-Isolated Focused Validation

* Intent: Verify `ruff check .`, `ruff format --check .`, `mypy`, and the `#117` document malware scan quarantine unit tests (plus `#76` `Store.focus` and endpoint-inventory regression checks) in `src/core` and `src/api` against the rebased worktree HEAD.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Assert worktree module resolution and run ruff, mypy, and focused #117/#76/inventory unit tests

* Requirement and evidence: `FR-REB-01`, `NFR-REB-01`; research `C3`–`C8`
* Expected result: Worktree module path assertion, `ruff check .`, `ruff format --check .`, and `mypy` in `src/core` and `src/api`, `#117` quarantine tests in `src/core` and `src/api`, `test_hazard_safeguarding_clock_owner.py`, `test_role_endpoint_inventory.py`, and `tools/rename-zava-tests.py` all exit `0`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Reconcile Pre-Review #117 and Child Tracking Artifacts

* Intent: During `rpi-implement`, append post-rebase base (`fa6f8d1dd`), rebased feature commit SHA, and focused validation evidence to parent `#117` records (preserving original `Residual work` / `RV-001` Review outcomes) and reconcile child `issue-117-doc-scan-rebase-fa6f8d1dd` changes and plan markers for `rpi-review`, leaving the final 10-file `.copilot-tracking/` commit to parent `RPI Agent` post-Review closeout.
* Dependencies: P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Append post-rebase lineage to parent #117 records and reconcile child pre-Review RPI artifacts

* Requirement and evidence: `FR-REB-02`, `NFR-REB-02`; research `C7`, `C8`
* Expected result: Parent `#117` records (preserving original `Residual work` / `RV-001` outcomes) and child pre-Review RPI records are reconciled, pass `python3 -m json.tool` and `git diff --check`, and leave zero dirty non-`.copilot-tracking/` paths ahead of `rpi-review` and parent post-Review tracking commit.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-phase-details.md

## Dependencies

* Remote branch `origin/feat/demo-164-chat-grounding-provenance-0900` fetched at `fa6f8d1dd`: Verified in research (`C1`).
* Tracked working tree clean before `git rebase`: Verified (`git diff --quiet` and `git diff --cached --quiet`; untracked child RPI artifacts do not collide with any tracked path in `243764945..fa6f8d1dd` or `4d91dae33`).

## Critique Disposition

Single-pass `rpi-plan-critique` completed on 2026-11-15 with verdict **Revise** (`PC-001`, `PC-002`); both compatible planner corrections were applied directly without running a second critique.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 `PC-001` [Medium]  | resolved    | Separated `P03-T01` (`rpi-implement` pre-Review reconciliation preserving original `#117` `Residual work` / `RV-001` Review outcomes) from parent `RPI Agent` post-Review final local commit across all 10 updated parent and child `.copilot-tracking/` artifacts (`FR-REB-02`, `AC3`, `AC4`, `P03`, `P03-T01`). |
| Run 1 `PC-002` [Low]     | resolved    | Extended `NFR-REB-01`, `AC2`, and `P02` Validation Expectations with an explicit `python3 -c` assertion verifying `zava_forward.core.__file__`, `zava_forward.agents.__file__`, and `zava_forward.api.__file__` all resolve inside `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan/`. |

## Follow-Up Items

* Add direct `SqlStore.rescan_pending()` reopen persistence and `out["blocked"]` counter unit-test assertions in `src/core/tests/test_document_rescan.py` (`RV-001` from parent `#117` review).
* Provision Azure Storage Defender malware scanning tags and quarantine infrastructure wiring in Bicep/deployment workflows (ADR 0002).
* Deliver remaining Issue #117 retention schedule and legal-hold DPO/Legal governance sign-off and automated purge evidence.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-changes.md
* Ready phase or task: Full plan ready (`P01` -> `P02` -> `P03`)
* Remaining provisional question or blocker: none
