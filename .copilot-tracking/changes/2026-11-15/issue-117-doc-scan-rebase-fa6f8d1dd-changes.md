<!-- markdownlint-disable-file -->
# RPI Changes: Rebase #117 Malware Scan Quarantine Onto fa6f8d1dd and Run Focused Validation

## Metadata

* Task ID: issue-117-doc-scan-rebase-fa6f8d1dd
* Related plan: .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01` -> `P02` -> `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01`
* All remaining active-plan markers: none
* Status basis: Rebased `feat/demo-117-doc-scan` (`4d91dae33` -> `e9c31f7fa051d5fd58795aa7feae7e404760433b`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`), resolved the sole `Store.focus` conflict in `src/core/src/zava_forward/core/store.py`, passed all worktree-isolated `ruff`, `mypy`, `#117` quarantine, `#76` `Store.focus`, route-inventory, and migration-regression checks across `src/core` and `src/api`, and reconciled pre-Review parent `#117` and child RPI tracking artifacts.

## Execution Summary

Completed all three planned phases (`P01`–`P03`) on `feat/demo-117-doc-scan`. Candidate commit `4d91dae33` replayed onto `fa6f8d1dd` (`origin/feat/demo-164-chat-grounding-provenance-0900`) as `e9c31f7fa051d5fd58795aa7feae7e404760433b` with one resolved merge conflict in `Store.focus` (`src/core/src/zava_forward/core/store.py`), retaining both `#76`'s `self._open_safety_items(c, staff=staff_list)` and `#117`'s `is_available_case_document(d)` fail-closed filter with zero `server.py` route changes. Worktree-isolated static analysis (`ruff check .`, `ruff format --check .`, `mypy`) and focused unit suites passed across `src/core` and `src/api`, and pre-Review tracking lineage was reconciled while preserving parent `#117`'s original `Residual work` (`RV-001`) Review outcome.

## Completed Work

### Rebase Onto fa6f8d1dd and Store.focus Conflict Resolution

* Related phase or task: `P01`, `P01-T01`
* Files: `src/core/src/zava_forward/core/store.py` (resolved during `git rebase`; auto-merged cleanly in `src/core/src/zava_forward/core/chat_case_answers.py`, `src/core/src/zava_forward/core/projection.py`, and `src/core/src/zava_forward/core/taskqueues.py`)
* What changed and why: Configured repository-local noreply `user.email` (`8036360+jmservera@users.noreply.github.com`) via `gh api user`, rebased `4d91dae33` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`), and resolved the single 2-line adjacency conflict in `Store.focus` so both `#76`'s `staff_list` / `self._open_safety_items(c, staff=staff_list)` and `#117`'s `{d["kind"] for d in c["documents"] if is_available_case_document(d)}` remain active.
* Completion evidence: Rebased commit `e9c31f7fa051d5fd58795aa7feae7e404760433b` sits directly atop `fa6f8d1dd`; `git grep` confirms zero conflict markers; `git diff origin/feat/demo-164-chat-grounding-provenance-0900..e9c31f7fa -- src/api/src/zava_forward/api/server.py` is empty.
* Validation: Passed (`ruff check .` and `ruff format --check .` verified before `git rebase --continue` and again post-rebase).

### Worktree-Isolated Focused Static Analysis and Quarantine Test Execution

* Related phase or task: `P02`, `P02-T01`
* Files: Read-only verification across `src/core`, `src/api`, and `tools/rename-zava-tests.py`
* What changed and why: Verified PEP 420 namespace package `__path__` isolation inside `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan/` using an ephemeral `PYTHONNOUSERSITE=1` venv (`pip install -e src/core -e src/agents -e "src/api[dev]"`, matching `.github/workflows/src-ci.yml` without modifying shared `~/.local`), then ran `ruff check .`, `ruff format --check .`, and `mypy` in both `src/core` and `src/api`, plus the `#117` malware scan quarantine tests, `#76` `Store.focus` tests, `test_role_endpoint_inventory.py`, and `tools/rename-zava-tests.py`.
* Completion evidence: Zero lint, format, type-check, or unit-test failures across all executed suites (`src/core` 346 mypy files + 64 unit tests OK `skipped=20`; `src/api` 297 mypy files + 44 unit tests OK; `tools/rename-zava-tests.py` 25 tests OK).
* Validation: Passed.

### Pre-Review Parent #117 and Child RPI Tracking Reconciliation

* Related phase or task: `P03`, `P03-T01`
* Files: `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md`, `.copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-state.json`, `.copilot-tracking/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan.md`, `.copilot-tracking/details/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-phase-details.md`, `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-changes.md`
* What changed and why: Appended post-rebase `fa6f8d1dd` -> `e9c31f7fa` lineage and focused validation results to parent `#117` changes, review, and state records while preserving original `Outcome: Residual work` (`RV-001`), checked `P01`–`P03` markers, and finalized pre-Review changes evidence ahead of single-pass `rpi-review` and parent `RPI Agent` post-Review local commit.
* Completion evidence: `python3 -m json.tool` passes on both state JSON files; `git diff --check` exits `0`; only `.copilot-tracking/` files appear in `git status --short` prior to post-Review commit.
* Validation: Passed.

## Implementation-Time Plan and Detail Updates

### Ephemeral PYTHONNOUSERSITE Venv and PEP 420 Namespace __path__ Verification

* Affected plan area or markers: `NFR-REB-01`, `AC2`, `P02` Validation Expectations
* What changed: Refined the module-origin assertion from `m.__file__` to PEP 420 namespace `m.__path__` and executed `ruff` and `mypy` inside a clean ephemeral `/tmp` `PYTHONNOUSERSITE=1` venv (`pip install -e src/core -e src/agents -e "src/api[dev]"`, cleaned up via `trap ... EXIT`) rather than `MYPYPATH=...:../agents/tests`.
* Why: `zava_forward.{core,agents,api}` are PEP 420 namespace packages (`__file__ is None`), and `src/api/tests/test_ai_consumption_api.py` relies on `zava-forward-agents` being installed as an untyped distribution (`# type: ignore[import-untyped]`) as in `.github/workflows/src-ci.yml` and `tools/rpi-checks.py` rather than added via `MYPYPATH`.
* Triggering evidence: Direct `P02-T01` execution output (`TypeError` on `NoneType` `m.__file__` and `unused-ignore` when `MYPYPATH` included `../agents/src:../agents/tests`).
* User answer or decision: none needed (immediately relevant current-state update preserving approved worktree-isolation intent without touching shared `~/.local`).
* Reconciliation performed: Updated `NFR-REB-01`, `AC2`, and `P02` Validation Expectations in plan and phase details.
* Planning and critique state: Ready (`PC-001` and `PC-002` remain resolved; no re-critique required).

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Namespace `__path__` worktree isolation check | `zava_forward.{core,agents,api}` | Passed | All 3 namespace `__path__` entries resolved under `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan/` in `PYTHONNOUSERSITE=1` venv |
| `python -m ruff check . && python -m ruff format --check .` | `src/core` | Passed | `All checks passed! 293 files already formatted` |
| `python -m mypy` | `src/core` | Passed | `Success: no issues found in 346 source files` |
| `python -m ruff check . && python -m ruff format --check .` | `src/api` | Passed | `All checks passed! 213 files already formatted` |
| `python -m mypy` | `src/api` | Passed | `Success: no issues found in 297 source files` |
| `python3 -m unittest tests/test_document_rescan.py tests/test_resident_documents.py tests/test_technical_evidence_usability.py tests/test_documents.py tests/test_hazard_safeguarding_clock_owner.py -v` | `src/core/tests` (`#117` + `#76`) | Passed | `Ran 64 tests in 15.600s — OK (skipped=20)` (live loopback MSSQL tests skipped) |
| `python3 -m unittest tests/test_document_controls.py tests/test_role_endpoint_inventory.py -v` | `src/api/tests` (`#117` + route inventory) | Passed | `Ran 44 tests in 115.890s — OK` |
| `python3 tools/rename-zava-tests.py` | repository migration regression | Passed | `Ran 25 tests in 0.501s — OK` |
| `python3 -m json.tool` & `git diff --check` | `.copilot-tracking/` JSON & whitespace | Passed | Valid JSON in parent and child state files; zero whitespace errors |
| `tools/rpi-checks.py` | full repository gate | Skipped | Caller explicitly requested focused validation (`ruff`, `mypy`, and `#117` quarantine tests in `src/core` and `src/api`) |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01` checked and `P02` venv/`__path__` detail synchronized)
* Completed-work evidence and handoff prose: Reconciled
* Validation, blockers, remaining work, and follow-up items: Reconciled
* Review readiness: Ready for single-pass `rpi-review`

## Blockers

* none

## Remaining Work

* none (`P01`–`P03` complete; parent `RPI Agent` post-Review closeout owns the final 10-file `.copilot-tracking/` local commit after `rpi-review` writes `-review.md` and state reaches `Follow-up`)

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-plan.md, `## Follow-Up Items`
* Add direct `SqlStore.rescan_pending()` reopen persistence and `out["blocked"]` counter unit-test assertions in `src/core/tests/test_document_rescan.py` (`RV-001` from parent `#117` review).
* Provision Azure Storage Defender malware scanning tags and quarantine infrastructure wiring in Bicep/deployment workflows (ADR 0002).
* Deliver remaining Issue #117 retention schedule and legal-hold DPO/Legal governance sign-off and automated purge evidence.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (`P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01` completed; none remaining)
* Validation coverage: Focused validation complete across `src/core` and `src/api` (`ruff check .`, `ruff format --check .`, `mypy`, 64 `src/core` unit tests, 44 `src/api` unit tests, 25 migration regression tests, JSON/diff checks)
* Blockers: none
* Current plan and detail updates: Refined `P02` module-path check to PEP 420 `m.__path__` inside an ephemeral `PYTHONNOUSERSITE=1` venv matching `src-ci.yml`
* Planning and critique state: Ready (`PC-001` and `PC-002` resolved)
* Follow-up items: 3 canonical items mirrored from plan
* Review readiness or no-handoff reason: Ready for single-pass `rpi-review`
* Continuation owner: parent confirmed automatic RPI Agent
