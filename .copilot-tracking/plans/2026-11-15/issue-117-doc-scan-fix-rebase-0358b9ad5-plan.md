<!-- markdownlint-disable-file -->
# RPI Plan: Issue #117 Document Scan Fix (`test_resident_decisions`) and Rebase onto 0358b9ad5

## Task Metadata

* Task ID: issue-117-doc-scan-fix-rebase-0358b9ad5
* Task slug: issue-117-doc-scan-fix-rebase-0358b9ad5
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-plan-critique.md

## Executive Summary

This plan executes a targeted correction and rebase RPI loop on `feat/demo-117-doc-scan` (`PR #1781`, starting at `5c5370a4a`) onto the latest parent branch `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f` atop `0358b9ad5`, adding PRs `#1775`, `#1777`, `#1778`, `#1779`, `#1780`, `#1782`, and `#1783` above `fa6f8d1dd`).

On `PR #1781`, 9/10 CI checks passed and `src-core` failed solely on `JsonResidentDecisions.test_resident_acceptance_never_clears_technical_or_hazard_gates` and `SqlResidentDecisions.test_resident_acceptance_never_clears_technical_or_hazard_gates` at `src/core/tests/test_resident_decisions.py:2526`. Research (`C3`–`C6`) proved that line 2522 constructs `dict(id=f"SYN-{kind}", kind=kind, generated=False)` without `scan` metadata solely as pre-state setup to reach `gate == []`, whereas `is_available_case_document` (`doc_controls.py:183`) rightly quarantines `generated=False` uploads lacking clean scan metadata (an invariant directly enforced by `test_technical_evidence_usability.py:29-67`). Implementation rebases cleanly onto `0358b9ad5` (`git merge-tree` exit `0`), updates `test_resident_decisions.py:2522-2524` to carry `scan=dict(status="clean", scanner="Synthetic metadata fixture")` matching `dataset.py:113-115` without weakening `is_available_case_document`, commits the fix, runs the caller's focused `src-ci.yml` validation across `src/core` and `src/api` plus full `src/core` `unittest discover`, reconciles `#117` tracking artifacts, completes single-pass `rpi-review`, and commits all `.copilot-tracking/` artifacts locally without pushing.

### User Decisions and Requirements Highlights

* Rebase `feat/demo-117-doc-scan` onto the latest parent branch `origin/feat/demo-164-chat-grounding-provenance-0900` (`0358b9ad5`).
* Fix `test_resident_acceptance_never_clears_technical_or_hazard_gates` (`JsonResidentDecisions` and `SqlResidentDecisions`) while keeping 100% of `#117` tests (`test_technical_evidence_usability.py`, `test_document_rescan.py`, `test_resident_documents.py`, `src/api/tests/test_document_controls.py`) passing.
* Run focused validation matching `src-ci.yml` in `src/core` and `src/api`.
* Update `.copilot-tracking/` RPI artifacts for `#117` and commit cleanly with the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer without pushing.

### What You May Not Know

* Read-only `git merge-tree --write-tree --messages 0358b9ad5 5c5370a4a` exits `0` with zero merge conflicts: upstream `#109` sensor non-authority guards in `doc_controls.py` and `#146` monitoring declarations in `assistants.py` auto-merge cleanly alongside `#117`.
* `src/core/tests/test_resident_decisions.py` is not in `src/core/pyproject.toml` format or `mypy` override exclusions, so the updated list comprehension must satisfy `ruff format --check` (100-char line limit) and `mypy --strict`.

### Unresolved Decisions or Blockers

* None. Root cause, canonical synthetic fixture contract, conflict-free rebase onto `0358b9ad5`, and `src-ci.yml` validation commands are verified from workspace evidence (`C1`–`C8`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop (`research` -> `plan` -> `implement` -> `review`) in `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan` on branch `feat/demo-117-doc-scan` (`PR #1781`) for Issue `#117` (caller prompt).
* Rebase `feat/demo-117-doc-scan` onto the latest parent branch `origin/feat/demo-164-chat-grounding-provenance-0900` (`0358b9ad5`) (caller Step 1).
* Fix `test_resident_acceptance_never_clears_technical_or_hazard_gates` (`JsonResidentDecisions` and `SqlResidentDecisions`) at `src/core/tests/test_resident_decisions.py:2526` while keeping `test_technical_evidence_usability.py`, `test_document_rescan.py`, `test_resident_documents.py`, and `src/api/tests/test_document_controls.py` passing 100%, preserving `#117`'s fail-closed missing-scan quarantine (caller Context & Step 2; research `C3`–`C6`).
* Run focused validation matching `src-ci.yml`:
  * `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_resident_decisions test_technical_evidence_usability test_document_rescan test_resident_documents -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy`
  * `cd src/api && PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_document_controls.py -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && PYTHONPATH=src:../core/src:../agents/src python3 -m mypy`
  (caller Step 3).
* Update `.copilot-tracking/` RPI artifacts for `#117` and commit cleanly with privacy-safe noreply git identity and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing, leaving a clean worktree for the coordinator (caller Step 4; repository instructions).

## Goals

* Rebase `feat/demo-117-doc-scan` cleanly onto `0358b9ad5` (`origin/feat/demo-164-chat-grounding-provenance-0900`) preserving all upstream (`#109`, `#189`, `#146`, `#104`, `#111`, `#128`) and `#117` invariants.
* Eliminate the 2 `test_resident_decisions` failures by supplying explicit clean synthetic scan metadata (`scan=dict(status="clean", scanner="Synthetic metadata fixture")`) on the pre-gate test setup stubs in `src/core/tests/test_resident_decisions.py`, without weakening `is_available_case_document` for missing/malformed scan statuses.
* Prove 100% conformance on the caller's `src-ci.yml` validation commands across `src/core` and `src/api` plus full `src/core` unit-test discovery and `test_role_endpoint_inventory.py`, and leave a clean, unpushed worktree after committing code and reconciled `.copilot-tracking/` artifacts.

## Scope and Non-Goals

### In Scope

* Configuring repository-local privacy-safe `user.email` via `gh api user` and rebasing `feat/demo-117-doc-scan` (`5c5370a4a`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0358b9ad5`).
* Updating the synthetic `Store.EVIDENCE` document list comprehension in `src/core/tests/test_resident_decisions.py` (`test_resident_acceptance_never_clears_technical_or_hazard_gates`) to include `scan=dict(status="clean", scanner="Synthetic metadata fixture")` formatted cleanly for `ruff format` and `mypy --strict`, and committing that targeted test fix.
* Running worktree-isolated module resolution verification, both caller `src-ci.yml` validation commands (`src/core` and `src/api`), full `src/core` `unittest discover -s tests -q`, `src/api/tests/test_role_endpoint_inventory.py`, and `python3 tools/rename-zava-tests.py`.
* Reconciling parent `#117` `.copilot-tracking/` records (preserving original `Residual work` / `RV-001` Review outcomes) and child `issue-117-doc-scan-fix-rebase-0358b9ad5` RPI artifacts, completing single-pass `rpi-review`, and committing finalized `.copilot-tracking/` files locally at parent `RPI Agent` post-Review closeout.

### Non-Goals

* Modifying `is_available_case_document`, `scan_status`, or any production module in `src/core` or `src/api` (including `server.py` HTTP routes).
* Running `tools/rpi-checks.py` or mutating shared `~/.local` editable `pip` installs.
* Pushing to `origin` or modifying GitHub pull requests.

## Functional Requirements

* **FR-FIX-01 (Conflict-Free Rebase onto `0358b9ad5`)**: `feat/demo-117-doc-scan` contains `0358b9ad5` in its ancestry (`git merge-base --is-ancestor 0358b9ad5 HEAD`), cleanly auto-merging `#109` sensor refusal in `doc_controls.py` and `#146` monitoring status in `assistants.py` alongside `#117` malware scan quarantine, with zero `server.py` route diffs.
  * Observable acceptance criteria: `git merge-base --is-ancestor 0358b9ad5 HEAD` and `git diff --check` exit `0`; `git diff 0358b9ad5..HEAD -- src/api/src/zava_forward/api/server.py` is empty.
* **FR-FIX-02 (Clean Synthetic Scan Fixture in `test_resident_decisions.py` Without Quarantine Weakening)**: `test_resident_acceptance_never_clears_technical_or_hazard_gates` in `src/core/tests/test_resident_decisions.py` constructs its pre-gate `Store.EVIDENCE` setup stubs with `scan=dict(status="clean", scanner="Synthetic metadata fixture")` (matching `dataset.py:113-115`), while `is_available_case_document` in `src/core/src/zava_forward/core/doc_controls.py` remains unchanged and fail-closed for `generated=False` documents lacking clean scan metadata.
  * Observable acceptance criteria: Both `JsonResidentDecisions` and `SqlResidentDecisions` pass `test_resident_acceptance_never_clears_technical_or_hazard_gates`, and `test_technical_evidence_usability.py`, `test_document_rescan.py`, `test_resident_documents.py`, and `src/api/tests/test_document_controls.py` pass 100%, committed cleanly on `feat/demo-117-doc-scan`.
* **FR-FIX-03 (Reconciled `#117` & Child Tracking Lineage)**: During `rpi-implement` (`P03-T01`), parent `#117` `.copilot-tracking/` changes, review, and state records (`issue-117-doc-scan-{changes,review,state}*`) are appended/updated with the `0358b9ad5` rebase base, fix commit SHA, and post-fix `src-ci.yml` validation results while preserving original `#117` `Residual work` (`RV-001`) Review outcomes, and child `issue-117-doc-scan-fix-rebase-0358b9ad5-changes.md` and `P01`–`P03` markers are reconciled for `rpi-review`. Immediately after single-pass `rpi-review` writes `-review.md` and parent `RPI Agent` transitions state to `Follow-up`, all 10 updated parent and child `.copilot-tracking/` artifacts are committed locally by parent `RPI Agent` closeout so `git status --short` is empty.
  * Observable acceptance criteria: Pre-Review (`P03-T01`), `python3 -m json.tool` passes on updated state JSON files, original `Residual work` (`RV-001`) outcome remains intact, and zero non-`.copilot-tracking/` paths are dirty; at parent `RPI Agent` post-Review closeout, `git status --short` is empty.

## Non-Functional Requirements

* **NFR-FIX-01 (Worktree-Isolated `src-ci.yml` Validation Parity)**: Unit tests, `ruff check`, `ruff format --check`, and `mypy` execute against `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan` without modifying shared `~/.local` packages.
  * Objective threshold or evaluation condition: Exit code `0` on `zava_forward.{core,agents,api}` worktree path assertion, caller's exact `src/core` and `src/api` validation commands (`unittest`, `ruff check src tests`, `ruff format --check src tests`, `mypy`), `ruff check . && ruff format --check .` in `src/core` and `src/api`, full `src/core` `unittest discover -s tests -q`, `src/api/tests/test_role_endpoint_inventory.py`, and `python3 tools/rename-zava-tests.py`.
  * Operating condition or verification approach: Direct CLI execution in `src/core` and `src/api` with worktree-prepended `PYTHONPATH`.
  * Observable acceptance criteria: Zero test failures, lint errors, formatting diffs, or `mypy` errors.
* **NFR-FIX-02 (Local Git Hygiene, Privacy-Safe Author, and No-Push Boundary)**: Repository-local `user.email` uses `{id}+{login}@users.noreply.github.com` resolved from `gh api user`, commits carry `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without `.copilot-tracking/` paths in commit messages, and zero remote writes occur.
  * Objective threshold or evaluation condition: At parent `RPI Agent` post-Review closeout, `git status --short` outputs empty string; `git log` shows `0358b9ad5` as ancestor, clean commits with noreply author and `Co-authored-by` trailer, and zero `git push`.
  * Operating condition or verification approach: Verified via `git status --short` and `git --no-pager log -n 5` at parent closeout.
  * Observable acceptance criteria: Clean local worktree ready for coordinator review and push.

## Acceptance Criteria

* AC1: `feat/demo-117-doc-scan` is rebased cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0358b9ad5`) with zero conflict markers and zero `server.py` route changes.
* AC2: `src/core/tests/test_resident_decisions.py` (`test_resident_acceptance_never_clears_technical_or_hazard_gates`) adds `scan=dict(status="clean", scanner="Synthetic metadata fixture")` to its synthetic `Store.EVIDENCE` setup stubs without modifying `is_available_case_document`, and is committed cleanly on `feat/demo-117-doc-scan`.
* AC3: Worktree-isolated `src-ci.yml` validation passes 100% (exit `0`) with `zava_forward.{core,agents,api}` verified under `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan/`: caller's `src/core` command (`test_resident_decisions`, `test_technical_evidence_usability`, `test_document_rescan`, `test_resident_documents`, `ruff check`, `ruff format --check`, `mypy`), full `src/core` `unittest discover -s tests -q`, caller's `src/api` command (`tests/test_document_controls.py`, `ruff check`, `ruff format --check`, `mypy`), `test_role_endpoint_inventory.py`, and `python3 tools/rename-zava-tests.py`.
* AC4: `P03-T01` reconciles parent `#117` records (preserving original `Residual work` / `RV-001` Review outcomes) and child pre-Review RPI artifacts (`python3 -m json.tool` and `git diff --check` exit `0`), and at parent `RPI Agent` post-Review closeout all 10 updated parent and child `.copilot-tracking/` artifacts are committed locally with noreply email and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leaving `git status --short` empty with no push.

## Test Ownership and Change Budget Lock

* Canonical production targets: `none` (`assistants.py` and `doc_controls.py` auto-merge during `git rebase` onto `0358b9ad5`; zero new production edits)
* Canonical test targets:
  * `src/core/tests/test_resident_decisions.py` (update 1 list comprehension in `test_resident_acceptance_never_clears_technical_or_hazard_gates`)
* Generated targets: `none`
* Exact test removals: `none`
* Maximum test files touched/added: `1` (`src/core/tests/test_resident_decisions.py`, 0 new test files added)
* Semantic vs regression coverage:
  * Semantic coverage: `test_resident_decisions.py` (`JsonResidentDecisions` and `SqlResidentDecisions` `test_resident_acceptance_never_clears_technical_or_hazard_gates`), `test_technical_evidence_usability.py` (missing/pending/failed/infected/malformed/conflicting scan fail-closed invariants), `test_document_rescan.py`, `test_resident_documents.py`, and `src/api/tests/test_document_controls.py`.
  * Regression coverage: Full `src/core` `unittest discover -s tests -q` (covering merged `#109` sensor refusal in `doc_controls.py`, `#146` monitoring declarations in `assistants.py`, `#76`, `#104`, `#111`, `#128`, and `#189`), `ruff check`, `ruff format --check`, and `mypy` in `src/core` and `src/api`, `src/api/tests/test_role_endpoint_inventory.py`, and `python3 tools/rename-zava-tests.py`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-plan.md                                 |
| Phase details                    | .copilot-tracking/details/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-phase-details.md                      |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-plan-critique.md (`Pass` / `Ready`; `0` findings) |
| Relevant research                | .copilot-tracking/research/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-research.md (`C1`–`C8`)              |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-changes.md is created by implement    |
| Planning execution and readiness | Complete; Ready for implementation                                                                                 |
| Continuation context             | Parent return to confirmed automatic `RPI Agent`                                                                   |

## Sources

* .copilot-tracking/research/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-research.md: Verifies `0358b9ad5` conflict-free rebase, `test_resident_decisions.py:2522-2526` fixture root cause, `dataset.py:113-115` clean synthetic scan metadata convention, `test_technical_evidence_usability.py` fail-closed missing-scan contract, and `pyproject.toml` strict formatting/typing rules (`C1`–`C8`).
* .copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md & .copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md: Parent `#117` artifacts reconciled post-rebase while preserving original `Residual work` (`RV-001`) Review outcomes.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Rebase onto 0358b9ad5 and Fix Synthetic Evidence Fixture in test_resident_decisions.py

* Intent: Configure repository-local privacy-safe git email, rebase `feat/demo-117-doc-scan` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f` atop `0358b9ad5`), update the pre-gate synthetic `Store.EVIDENCE` fixture in `src/core/tests/test_resident_decisions.py` with clean synthetic scan metadata without changing `is_available_case_document`, and commit the test fix cleanly.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Configure local privacy-safe git email and rebase feat/demo-117-doc-scan onto 0358b9ad5

* Requirement and evidence: `FR-FIX-01`, `NFR-FIX-02`; research `C1`, `C2`, `C7`
* Expected result: `feat/demo-117-doc-scan` replays cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f` atop `0358b9ad5`, `git merge-base --is-ancestor 0358b9ad5 HEAD` and `git diff --check` exit `0`) with untouched `server.py`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add clean synthetic scan metadata in test_resident_decisions.py and commit fix cleanly

* Requirement and evidence: `FR-FIX-02`, `NFR-FIX-02`; research `C3`, `C4`, `C5`, `C6`, `C8`
* Expected result: `src/core/tests/test_resident_decisions.py` (`test_resident_acceptance_never_clears_technical_or_hazard_gates`) adds `scan=dict(status="clean", scanner="Synthetic metadata fixture")` formatted cleanly for `ruff format` and `mypy --strict`, `doc_controls.py` is unchanged, and the test fix is committed with noreply author and `Co-authored-by` trailer.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Execute Worktree-Isolated Focused src-ci.yml Validation

* Intent: Verify module resolution points to `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan/` and run the caller's exact `src/core` and `src/api` `src-ci.yml` validation suites plus full `src/core` unit discovery, `test_role_endpoint_inventory.py`, and `tools/rename-zava-tests.py`.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Assert worktree module resolution and execute src/core and src/api validation suites

* Requirement and evidence: `FR-FIX-01`, `FR-FIX-02`, `NFR-FIX-01`; research `C3`–`C8`
* Expected result: Worktree path assertion for `zava_forward.{core,agents,api}`, caller's `src/core` command (`unittest`, `ruff check src tests`, `ruff format --check src tests`, `mypy`), full `src/core` `unittest discover -s tests -q` + `ruff check . && ruff format --check .`, caller's `src/api` command (`tests/test_document_controls.py`, `ruff check src tests`, `ruff format --check src tests`, `mypy`) + `ruff check . && ruff format --check .`, `test_role_endpoint_inventory.py`, and `python3 tools/rename-zava-tests.py` all exit `0`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Reconcile Pre-Review #117 and Child Tracking Artifacts

* Intent: During `rpi-implement`, append the `ad005cd5f` / `0358b9ad5` rebase base, fix commit SHA, and `src-ci.yml` validation evidence to parent `#117` records (preserving original `Residual work` / `RV-001` Review outcomes) and reconcile child `issue-117-doc-scan-fix-rebase-0358b9ad5` changes and plan markers for `rpi-review`, leaving the final 10-file `.copilot-tracking/` commit to parent `RPI Agent` post-Review closeout.
* Dependencies: P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Append 0358b9ad5 rebase/fix lineage to parent #117 records and reconcile child pre-Review RPI artifacts

* Requirement and evidence: `FR-FIX-03`, `NFR-FIX-02`; research `C7`, `C8`
* Expected result: Parent `#117` records (preserving original `Residual work` / `RV-001` outcomes) and child pre-Review RPI records are reconciled, pass `python3 -m json.tool` and `git diff --check`, and leave zero dirty non-`.copilot-tracking/` paths ahead of `rpi-review` and parent post-Review tracking commit.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-phase-details.md

## Dependencies

* Remote branch `origin/feat/demo-164-chat-grounding-provenance-0900` verified at `0358b9ad5`: Verified in research (`C1`).
* Tracked working tree clean before `git rebase`: Verified (`git diff --quiet` and `git diff --cached --quiet`; untracked child RPI artifacts do not collide with any tracked path in `fa6f8d1dd..0358b9ad5` or `5c5370a4a`).

## Critique Disposition

Single-pass `rpi-plan-critique` completed on 2026-11-15 with verdict **Pass (`Ready`)** and zero findings (`Critical: 0, High: 0, Medium: 0, Low: 0`). No plan revisions or user decisions were required, and no second critique runs.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 (`none`)           | pass        | Candidate plan and phase details verified as implementation-ready across `P01`–`P03` with zero `PC-xxx` findings; accepted residual ref-drift check remains guarded by `P01` ancestry validation. |

## Follow-Up Items

* Add direct `SqlStore.rescan_pending()` reopen persistence and `out["blocked"]` counter unit-test assertions in `src/core/tests/test_document_rescan.py` (`RV-001` from parent `#117` review).
* Provision Azure Storage Defender malware scanning tags and quarantine infrastructure wiring in Bicep/deployment workflows (ADR 0002).
* Deliver remaining Issue #117 retention schedule and legal-hold DPO/Legal governance sign-off and automated purge evidence.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-changes.md
* Ready phase or task: Full plan ready (`P01` -> `P02` -> `P03`)
* Remaining provisional question or blocker: none
