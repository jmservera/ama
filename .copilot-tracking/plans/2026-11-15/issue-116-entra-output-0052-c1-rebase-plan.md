<!-- markdownlint-disable-file -->
# RPI Plan: Cycle 1 Rebase Continuation (`c1-rebase`) Onto Merged Parent Tip `0c1fa1da4` (`PR #1769`)

## Task Metadata

* Task ID: issue-116-entra-output-0052-c1-rebase
* Task slug: issue-116-entra-output-0052-c1-rebase
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-rebase-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-116-entra-output-0052-c1-rebase-plan-critique.md

## Executive Summary

This rebase continuation inside Cycle 1 (`c1-rebase`, spending no new correction cycle) rebases branch `feat/ai-116-entra-output-0052` (`7b882614d..e7d05fab4`, which already passed independent review on `7f83f4749`) onto the newly merged stacked parent tip `origin/feat/demo-164-chat-grounding-provenance-0900` (`d8cb35d25` after `PR #1770` merged directly atop `0c1fa1da4` from `PR #1769`).

In Phase `P01`, we configure the repository-local privacy-safe GitHub noreply email, temporarily archive untracked `c1-rebase` `.copilot-tracking/` files into a path-preserving `tar` archive in the session workspace so the worktree is clean, run `git fetch origin feat/demo-164-chat-grounding-provenance-0900` and `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, and resolve the single conflicting file `src/core/src/zava_forward/core/store.py` (two conflict blocks at `_queue_candidates` and `_work_context`) by preserving both `0c1fa1da4`'s handoff SLA cache-key and 4-argument `handoff_view(c, as_of=self.as_of, policy=..., staff=...)` changes (alongside `0c1fa1da4`'s `taskqueues.MEMBERSHIP_REVISION = 4` and `sqlstore._queue_fingerprint`) and `7b882614d`'s formatting and `#116` role-visibility changes, allowing `e7d05fab4` to replay cleanly atop `7b882614d'` before restoring the `c1-rebase` tracking files. In Phase `P02`, we run all Focused validation commands (mapping caller-referenced `src/api/tests/test_design_system_source_contract.py` to the repository's canonical `src/api/tests/test_design_system.py` with explicit disclosure, plus targeted `#83`/`#116` cross-feature regression suites with `src/api` on `PYTHONPATH`), update `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md` and `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md` to record the rebase onto `0c1fa1da4` while preserving `c1`'s original `Conformant` verdict, and reconcile `c1-rebase` changes/plan/details for single-pass `rpi-review`, after which the automatic RPI parent commits all tracking updates cleanly with the Copilot trailer without pushing (`git status --short` empty).

### User Decisions and Requirements Highlights

* Stay inside Cycle 1 as a rebase continuation (spend no new correction cycle) on `feat/ai-116-entra-output-0052` in `/home/azureuser/source/ama-demo-wt/feat-116-entra-output-0052`.
* Fetch `origin feat/demo-164-chat-grounding-provenance-0900` and rebase `7b882614d..e7d05fab4` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`), resolving the single conflict in `src/core/src/zava_forward/core/store.py` by preserving both `0c1fa1da4` handoff changes and `7b882614d` `MEMBERSHIP_REVISION` / role-visibility changes.
* Update `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md` and `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md` to record the rebase onto `0c1fa1da4`.
* Run the 4 caller Focused validation commands (`unittest`, `src/core` `ruff` + `mypy`, `src/api` `ruff`, and `tools/rename-zava-tests.py`), commit cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, do NOT push, leave `git status --short` empty, and exit without calling `ask_user`.

### What You May Not Know

* Diffing Ruff-formatted `0c1fa1da4` `store.py` against `7b882614d` `store.py` proves that `store.py` has only two conflict markers (`_queue_candidates` and `_work_context`), while `detail` (`d["handoff"] = handoff_view(...)`) auto-merges cleanly to `0c1fa1da4`'s 4-argument form, `taskqueues.MEMBERSHIP_REVISION = 4` and `sqlstore._queue_fingerprint` carry over untouched from `0c1fa1da4`, and `e7d05fab4` replays with zero conflicts because none of its 10 files were touched by `0c1fa1da4`.
* Creating a clean tracking-only commit atop rebased `e7d05fab4'` at post-`rpi-review` closeout (rather than amending `e7d05fab4'`) records the exact final rebased SHAs of `7b882614d'` and `e7d05fab4'` in `c1-changes.md` and `c1-review.md` without circular SHA invalidation or mutating the reviewed code commits.
* `src/api/tests/test_design_system_source_contract.py` referenced in Scope #4 does not exist in git history; the canonical design-system contract suite in this repository is `src/api/tests/test_design_system.py` (`PC-001`), which `P02-T01` executes directly with explicit filename-mapping disclosure.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI continuation loop (`rpi-research`, `rpi-plan`, `rpi-implement`, `rpi-review`) in `/home/azureuser/source/ama-demo-wt/feat-116-entra-output-0052` on branch `feat/ai-116-entra-output-0052` (currently at `e7d05fab4`) to rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`, after `PR #1769` merged) as a rebase continuation inside C1 with no new correction cycle spent (caller prompt).
* Run `git fetch origin feat/demo-164-chat-grounding-provenance-0900` and rebase `feat/ai-116-entra-output-0052` (`7b882614d..e7d05fab4`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) (caller prompt, Scope #1).
* Resolve the single conflict in `src/core/src/zava_forward/core/store.py` by preserving BOTH `0c1fa1da4`'s `handoffs` changes AND `7b882614d`'s `MEMBERSHIP_REVISION` / role-visibility changes (caller prompt, Scope #2).
* Update `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md` and `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md` to record the rebase onto `0c1fa1da4` (caller prompt, Scope #3).
* Run focused validation (`PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api/src:src/api/tests python3 -m unittest src/api/tests/test_ai_tasks.py src/api/tests/test_design_system_source_contract.py src/core/tests/test_data_protection.py -q`, `cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy`, `cd src/api && python3 -m ruff check . && python3 -m ruff format --check .`, and `python3 tools/rename-zava-tests.py`) (caller prompt, Scope #4).
* Commit cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, do NOT push, leave `git status --short` empty, and exit immediately without calling `ask_user` (caller prompt, Scope #5).

## Goals

* Rebase `feat/ai-116-entra-output-0052` (`7b882614d..e7d05fab4`) cleanly onto `0c1fa1da4` with zero loss of `#83`, `#164`, or `#116` behavior.
* Verify all Focused-tier unit, lint, formatting, type-checking, and migration checks plus cross-feature `#83`/`#116` regression suites.
* Record the `0c1fa1da4` rebase accurately in `c1-changes.md`, `c1-review.md`, and the `c1-rebase` RPI artifacts, committed cleanly on a spotless working tree without pushing.

## Scope and Non-Goals

### In Scope

* Fetching `origin feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) and rebasing `7b882614d..e7d05fab4` onto `0c1fa1da4`.
* Conflict resolution in `src/core/src/zava_forward/core/store.py` (`_queue_candidates` and `_work_context`), plus verification of auto-merged `detail` in `store.py`, `server.py`, and `test_role_endpoint_inventory.py`, and inherited `taskqueues.MEMBERSHIP_REVISION = 4` / `sqlstore._queue_fingerprint`.
* Focused validation across caller-specified suites and cross-feature `#83` / `#116` suites.
* Updating `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md` and `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md` (preserving `c1`'s original `Conformant` verdict) and recording `c1-rebase` RPI artifacts in one clean local commit atop rebased `e7d05fab4'`.

### Non-Goals

* Adding, removing, or modifying production behavior beyond mechanical conflict resolution in `store.py` during rebase.
* Running `tools/rpi-checks.py --all` or Docker builds.
* Pushing to `origin` or invoking interactive user prompts.

## Functional Requirements

* FR-1: Clean rebase of `7b882614d..e7d05fab4` onto `0c1fa1da4` preserving `#83` handoff SLA visibility and `#116` role-visibility projections
  * Observable acceptance criteria: `git merge-base --is-ancestor 0c1fa1da4 HEAD` exits `0`; in `src/core/src/zava_forward/core/store.py`, `_queue_candidates` includes `json.dumps(self.data.get("handoff_policy"), sort_keys=True)` in `key`, `_work_context` and `detail` call `handoff_view(c, as_of=self.as_of, policy=..., staff=...)`, `taskqueues.MEMBERSHIP_REVISION == 4` and `sqlstore._queue_fingerprint` include `policy`, all `7b882614d` role-visibility methods (`draft`, `_clean_doc_ai_metadata`, `add_document`, `read_document`, `ai_run`, `_rec_view`, `ai_priority`, `funding_draft`, `ai_live_report`) and `e7d05fab4` fixes (`data_protection.py`, `ai_tasks._record_view`, `test_ai_tasks.py`) remain intact, and zero conflict markers exist in tracked files.
* FR-2: Accurate C1 rebase-continuation evidence in tracking artifacts without altering original C1 review verdicts
  * Observable acceptance criteria: `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md` and `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md` record the rebase onto `0c1fa1da4` (`PR #1769`), the rebased SHAs `7b882614d'` and `e7d05fab4'`, the `store.py` conflict resolution, and post-rebase validation while preserving `c1-review.md`'s original `Outcome: Conformant`; `c1-rebase` implementation artifacts are reconciled before `rpi-review`, and at post-`rpi-review` closeout all tracking artifacts are committed cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` leaving `git status --short` empty.

## Non-Functional Requirements

* NFR-1: Focused validation, static analysis, formatting, and migration non-regression
  * Objective threshold or evaluation condition: `0` failures/errors across all Focused validation commands (mapping caller-referenced `src/api/tests/test_design_system_source_contract.py` to the existing canonical `src/api/tests/test_design_system.py`, with explicit filename-mapping disclosure in `c1-changes.md` and `c1-rebase-changes.md`) plus targeted `#83`/`#116` cross-feature regression suites (`test_handoff_escalation_83.py`, `test_handoff_escalation_api_83.py`, `test_role_endpoint_inventory.py`, `test_content_standard.py`, `test_human_review_effectiveness_223.py`).
  * Operating condition or verification approach, if needed: Executed directly on the rebased working tree using `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api/src:src/api/tests python3 -m unittest src/api/tests/test_ai_tasks.py src/api/tests/test_design_system.py src/core/tests/test_data_protection.py -q`, `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api:src/api/src:src/api/tests python3 -m unittest src/core/tests/test_handoff_escalation_83.py src/api/tests/test_handoff_escalation_api_83.py src/api/tests/test_role_endpoint_inventory.py src/api/tests/test_content_standard.py src/core/tests/test_human_review_effectiveness_223.py -q`, `cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy`, `cd src/api && python3 -m ruff check . && python3 -m ruff format --check .`, and `python3 tools/rename-zava-tests.py`.
  * Observable acceptance criteria: Every validation command exits `0` and leaves zero untracked build or cache files in `git status --short`.

## Acceptance Criteria

* `feat/ai-116-entra-output-0052` sits cleanly atop `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) with rebased commits `7b882614d'` and `e7d05fab4'` (followed at post-`rpi-review` closeout by a single clean tracking commit).
* `src/core/src/zava_forward/core/store.py` preserves both `0c1fa1da4`'s handoff changes (`handoff_policy` in `_queue_candidates` and 4-arg `handoff_view` in `_work_context` and `detail`) and `7b882614d`'s formatting and role-visibility changes, while `taskqueues.MEMBERSHIP_REVISION == 4` and `sqlstore._queue_fingerprint` remain intact from `0c1fa1da4`.
* All Focused validation commands (`test_ai_tasks.py` + `test_design_system.py` + `test_data_protection.py`, `src/core` `ruff` + `mypy`, `src/api` `ruff`, `tools/rename-zava-tests.py`) and the targeted `#83`/`#116` cross-feature regression suites pass with exit code `0`.
* `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md` and `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md` record the rebase onto `0c1fa1da4` (and disclose the `test_design_system_source_contract.py` -> `test_design_system.py` module mapping) while preserving `c1`'s original `Conformant` outcome.
* At post-`rpi-review` closeout, all tracking artifacts are committed locally with the Copilot trailer, `git status --short` is completely empty, and no `git push` has been executed.
* Test ownership and bounds lock:
  * Removals: `none` (`0` tests removed or weakened).
  * Canonical test targets: No test edits (`0` new test methods, `0` new test files, `0` generated files modified); existing suites verified: `src/api/tests/test_ai_tasks.py`, `src/api/tests/test_design_system.py`, `src/core/tests/test_data_protection.py`, `src/core/tests/test_handoff_escalation_83.py`, `src/api/tests/test_handoff_escalation_api_83.py`, `src/api/tests/test_role_endpoint_inventory.py`, `src/api/tests/test_content_standard.py`, `src/core/tests/test_human_review_effectiveness_223.py`, and `tools/rename-zava-tests.py`.
  * Semantic vs regression coverage: Existing `#83` suites (`test_handoff_escalation_83.py`, `test_handoff_escalation_api_83.py`) verify `handoff_policy` queue invalidation and 4-arg `handoff_view` semantics in `Store` and `SqlStore`; existing `#116` suites (`test_ai_tasks.py`, `test_data_protection.py`, `test_role_endpoint_inventory.py`, `test_content_standard.py`, `test_human_review_effectiveness_223.py`) verify `MEMBERSHIP_REVISION`/queue projections, post-provider role visibility, author `_record_view` retention, document derivative gating, and UI/design-system contracts (`test_design_system.py`).

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                             |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-rebase-plan.md                                       |
| Phase details                    | .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-rebase-phase-details.md                            |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/issue-116-entra-output-0052-c1-rebase-plan-critique.md (`Revise`; `PC-001`..`PC-003` resolved directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-c1-rebase-research.md                                |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-rebase-changes.md is owned by `rpi-implement`      |
| Planning execution and readiness | Complete; implementation-ready (`ready`)                                                                               |
| Continuation context             | Confirmed automatic RPI Agent parent continues directly to `rpi-implement`                                             |

## Sources

* `.copilot-tracking/research/2026-11-15/issue-116-entra-output-0052-c1-rebase-research.md`: Cycle 1 evidence (`C1`-`C6`) covering `0c1fa1da4` commit scope, `store.py` conflict hunks, Ruff-formatted diff verification, `e7d05fab4` clean replay, and host `python3` validation tooling.
* `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/sqlstore.py`, `src/core/src/zava_forward/core/taskqueues.py`: Rebase target and queue-membership dependencies.
* `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md`: Parent C1 artifacts updated per Scope #3.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Fetch Parent Branch and Rebase `7b882614d..e7d05fab4` Onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4` -> `d8cb35d25`)

* Intent: Rebase `feat/ai-116-entra-output-0052` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`d8cb35d25` / `PR #1770`, parent `0c1fa1da4` / `PR #1769`) and cleanly resolve `src/core/src/zava_forward/core/store.py` while preserving `#83`, `#133`, `#164`, and `#116` changes.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Fetch `origin feat/demo-164-chat-grounding-provenance-0900`, rebase `7b882614d..e7d05fab4` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4` -> `d8cb35d25`), and resolve `store.py` conflict

* Requirement and evidence: FR-1 (`C1`, `C2`, `C3`, `C4`)
* Expected result: Privacy-safe local git email is configured; untracked `c1-rebase` `.copilot-tracking/` files are backed up to the session workspace before rebase and restored immediately after; `7b882614d` and `e7d05fab4` replay cleanly onto `0c1fa1da4` with `_queue_candidates`, `_work_context`, and `detail` in `store.py` preserving `0c1fa1da4`'s `handoff_policy` and 4-arg `handoff_view(...)` alongside `7b882614d`'s formatting and role-visibility changes (`taskqueues.MEMBERSHIP_REVISION == 4` and `sqlstore._queue_fingerprint` intact).
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-rebase-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Focused Validation, C1 Tracking Updates, and Pre-Review Reconciliation

* Intent: Verify all Focused validation suites on the rebased tree, record the `0c1fa1da4` -> `d8cb35d25` rebase in `c1-changes.md` and `c1-review.md` plus `c1-rebase` changes evidence, and reconcile `c1-rebase` artifacts ready for single-pass `rpi-review` (with the final local tracking commit executed by the automatic RPI parent at post-`rpi-review` closeout).
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run Focused validation suites, update `c1-changes.md` and `c1-review.md` for `0c1fa1da4`, and reconcile `c1-rebase` artifacts for `rpi-review`

* Requirement and evidence: FR-1, FR-2, NFR-1 (`C3`, `C5`, `C6`, `PC-001`, `PC-002`, `PC-003`)
* Expected result: All Focused validation commands (`test_ai_tasks.py` + `test_design_system.py` + `test_data_protection.py`, cross-feature `#83`/`#116` unit suites with `src/api` on `PYTHONPATH`, `src/core` `ruff` + `mypy`, `src/api` `ruff`, and `tools/rename-zava-tests.py`) exit `0`; `issue-116-entra-output-0052-c1-changes.md` and `issue-116-entra-output-0052-c1-review.md` record the `0c1fa1da4` rebase, rebased commit SHAs, `store.py` resolution, and validation results while preserving `c1`'s original `Conformant` verdict; and `c1-rebase` plan/details/changes are reconciled ready for read-only `rpi-review` followed by the automatic RPI parent's single clean post-review tracking commit (`git status --short` empty, no `git push`).
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-rebase-phase-details.md

## Dependencies

* `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`): Merged parent branch tip incorporating `PR #1769` (`Refs #83`).
* Host `python3` (`3.12`) with `ruff`, `mypy`, `python-pptx`, and `Pillow` plus `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api:src/api/src:src/api/tests`.
* Session workspace archive path `/home/azureuser/.copilot/session-state/f0c59e3e-4b74-4f53-a238-646f1d96d6c1/files/c1-rebase-backup.tar` for path-preserving archive/restore of untracked `c1-rebase` `.copilot-tracking/` files across `git rebase`.

## Critique Disposition

Single-pass critique completed in `.copilot-tracking/reviews/plans/2026-11-15/issue-116-entra-output-0052-c1-rebase-plan-critique.md` (`Critique execution status: Complete`, `Verdict: Revise`). All three findings were planner-owned and resolved directly in one batch without a second critique pass:

* `PC-001` (`High`, `Applied directly`): Replaced non-existent `src/api/tests/test_design_system_source_contract.py` with the repository's canonical `src/api/tests/test_design_system.py` in `NFR-1`, `Acceptance Criteria`, and `P02`/`P02-T01` command #1, and added explicit filename-mapping disclosure for `c1-changes.md` and `c1-rebase-changes.md`.
* `PC-002` (`High`, `Applied directly`): Added `src/api` to `PYTHONPATH` (`PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api:src/api/src:src/api/tests`) in `NFR-1` and `P02`/`P02-T01` command #2 so `from tests.test_mvp import DATA` in `src/api/tests/test_handoff_escalation_api_83.py` resolves cleanly from the repository root.
* `PC-003` (`Medium`, `Applied directly`): Replaced the `**` flat-directory backup in `P01-T01` steps 2 and 6 with path-preserving `find .copilot-tracking -name 'issue-116-entra-output-0052-c1-rebase-*' -print0 | tar --null -cf .../c1-rebase-backup.tar -T -` + `tar -xf`, and separated `P02-T01` pre-review implementation completion from the automatic RPI parent's post-`rpi-review` tracking commit.

## Follow-Up Items

* Extract shared post-provider record-visibility scrubbing helper across `ai_tasks._record_view`, `Store._rec_view`, and `ChatIsolation.scrub_thread`: Carry-forward engineering-quality cleanup (`RV-001`) outside this C1 rebase continuation.
* Organisational control-owner confirmation of OD-14 / OD-19 (`ZF_REASON_ROLES`) and live Microsoft Entra B2B tenant configuration: External governance items on Issue #116 outside local repository scope.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-rebase-changes.md
* Ready phase or task: Implementation complete (`P01-T01`, `P02-T01`); ready for single-pass `rpi-review`
* Remaining provisional question or blocker: None
