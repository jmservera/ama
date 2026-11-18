<!-- markdownlint-disable-file -->
# RPI Changes: Issue #117 Document Scan Fix (`test_resident_decisions`) and Rebase onto 0358b9ad5

## Metadata

* Task ID: issue-117-doc-scan-fix-rebase-0358b9ad5
* Related plan: .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01` -> `P02` -> `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`
* All remaining active-plan markers: none
* Status basis: All planned phases and tasks completed with zero source regressions, passing `src-ci.yml` validation across `src/core` and `src/api`, and reconciled pre-Review tracking records.

## Execution Summary

Rebased `feat/demo-117-doc-scan` onto the latest `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f6e1bdf8e7f56f545ded63af029b9ee6`, 1 documentation commit `#1783` ahead of `0358b9ad51435387057d08293a8a42846abd2cef`, replaying `#117` quarantine implementation cleanly as `058fcc3e8` and prior rebase tracking as `a68ca54fe` with zero conflicts), committed `3efbe346a7b8cb066a94b157271b6ac7ec39edd7` adding `scan=dict(status="clean", scanner="Synthetic metadata fixture")` to `test_resident_acceptance_never_clears_technical_or_hazard_gates` in `src/core/tests/test_resident_decisions.py` without changing `is_available_case_document` fail-closed missing-scan quarantine, verified 100% pass across `src/core` (`484` targeted + `3,660` full unit tests, `ruff`, `mypy`) and `src/api` (`44` targeted unit tests including `test_document_controls` and `test_role_endpoint_inventory`, `ruff`, `mypy`) plus `tools/rename-zava-tests.py` (`25` tests), and reconciled parent `#117` and child RPI tracking records ahead of `rpi-review`.

## Completed Work

### P01: Rebase onto Latest Stacked Parent (`P01-T01`) and Synthetic Gate Fixture Fix (`P01-T02`)

* Resolved authenticated GitHub noreply email (`8036360+jmservera@users.noreply.github.com`) via `gh api user` and configured repository-local `git config --local user.email` (`P01-T01`).
* Fetched `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f` atop `0358b9ad5`) and ran `git rebase origin/feat/demo-164-chat-grounding-provenance-0900` with clean tracked files; commits `e9c31f7fa` and `5c5370a4a` replayed cleanly with zero conflicts as `058fcc3e8` and `a68ca54fe`, `git merge-base --is-ancestor 0358b9ad5 HEAD` and `git merge-base --is-ancestor ad005cd5f HEAD` both exited `0`, `git diff --check` exited `0`, and `git diff ad005cd5f..HEAD -- src/api/src/zava_forward/api/server.py` remained empty (`P01-T01`).
* Updated `src/core/tests/test_resident_decisions.py` in `test_resident_acceptance_never_clears_technical_or_hazard_gates` (`JsonResidentDecisions` and `SqlResidentDecisions`) so the synthetic pre-gate `Store.EVIDENCE` setup comprehension carries `scan=dict(status="clean", scanner="Synthetic metadata fixture")`, matching `src/core/tests/dataset.py` (`supplied_resident_fixture`) while leaving `src/core/src/zava_forward/core/doc_controls.py` (`is_available_case_document`) untouched (`P01-T02`).
* Committed `src/core/tests/test_resident_decisions.py` as `3efbe346a7b8cb066a94b157271b6ac7ec39edd7` (`test(core): supply clean scan metadata in synthetic evidence gate fixture`) with `Refs #117` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` (`P01-T02`).

### P02: Worktree-Isolated `src-ci.yml` and Regression Validation (`P02-T01`)

* Verified `zava_forward.{core,agents,api}.__path__` resolved exclusively inside `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan/` (`P02-T01`).
* Ran the caller's exact `src/core` `src-ci.yml` command (`484` tests OK, `skipped=174`; `ruff check src tests` clean; `ruff format --check src tests` 297 files formatted; `mypy` 351 source files clean), full `src/core` unit discovery (`3,557` in bare `PYTHONPATH=src:tests` plus `84` editable-install/dev-dep CLI & Azure IoT SDK tests in ephemeral editable venv = all `3,660` tests OK, `skipped=420`; `ruff check . && ruff format --check .` 298 files formatted), `src/api` `src-ci.yml` validation in an ephemeral editable venv matching `.github/workflows/src-ci.yml` (`pip install --no-deps -e src/core -e src/agents -e src/api`, `tests/test_document_controls.py` `18` tests OK, `tests/test_role_endpoint_inventory.py` + `tests/test_document_controls.py` `44` tests OK, `ruff check . && ruff format --check .` 213 files formatted, `mypy` 297 source files clean), and `python3 tools/rename-zava-tests.py` (`25` tests OK) (`P02-T01`).

### P03: Pre-Review `#117` and Child RPI Tracking Reconciliation (`P03-T01`)

* Appended post-rebase/fix reconciliation notes (`ad005cd5f` / `0358b9ad5` base, `#117` commit `058fcc3e8`, test-fixture fix commit `3efbe346a`, and `src-ci.yml` validation counts) to `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md`, and `.copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-state.json` while preserving parent `#117` original `Outcome: Residual work` (`RV-001`) Review record (`P03-T01`).
* Checked off all plan markers (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`), updated `phase-details.md` Phase Index to `Complete`, and verified JSON syntax (`python3 -m json.tool`) and whitespace (`git diff --check`) ahead of `rpi-review` (`P03-T01`).

## Implementation-Time Plan and Detail Updates

* **Immediately relevant current-state update (`P01-T01`)**: Between research (`C1`) and `git fetch origin feat/demo-164-chat-grounding-provenance-0900` in `P01-T01`, the stacked parent branch advanced by 1 documentation-only commit (`ad005cd5f6e1bdf8e7f56f545ded63af029b9ee6`, `#1783` `docs(instructions,agents): apply chronicle recommendations via hve-builder`) directly atop `0358b9ad51435387057d08293a8a42846abd2cef` with zero `src/` changes. Rebased onto the latest `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f`), satisfying both `git merge-base --is-ancestor 0358b9ad5 HEAD` and `git merge-base --is-ancestor ad005cd5f HEAD`.
* **Localjudgment validation note (`P02-T01`)**: Matching `.github/copilot-instructions.md` (updated in `ad005cd5f`) and `.github/workflows/src-ci.yml`, `unittest tests/test_document_controls.py` in `src/api` requires `tests` on `PYTHONPATH` (`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`) so cross-test `import test_mvp` resolves, and `src/api` `mypy` requires editable package installation (`pip install --no-deps -e src/core -e src/agents -e src/api` in a cleaned-up ephemeral `/tmp` venv) so `zava_forward.agents.*` matches `src-ci.yml`'s `# type: ignore[import-untyped]` contract without mutating shared `~/.local`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `git merge-base --is-ancestor 0358b9ad5 HEAD && git merge-base --is-ancestor ad005cd5f HEAD && git diff --check` | `feat/demo-117-doc-scan` history | Passed | Both merge-base checks and whitespace check exited `0` (`058fcc3e8` -> `a68ca54fe` -> `3efbe346a` atop `ad005cd5f` / `0358b9ad5`) |
| `git --no-pager diff ad005cd5f..HEAD -- src/api/src/zava_forward/api/server.py` | `src/api` HTTP route inventory | Passed | Empty diff; zero HTTP routes added or modified |
| `zava_forward.{core,agents,api}.__path__` prefix check | worktree module resolution | Passed | All 3 namespace packages resolved exclusively under `/home/azureuser/source/ama-demo-wt/feat-117-doc-scan/` |
| `PYTHONPATH=src:tests python3 -m unittest test_resident_decisions test_technical_evidence_usability test_document_rescan test_resident_documents -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy` | `src/core` (`src-ci.yml` focused) | Passed | `Ran 484 tests in 14.844s — OK (skipped=174)`; `ruff check` passed; `297 files already formatted`; `mypy`: `Success: no issues found in 351 source files` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q` + ephemeral editable `[dev]` venv on 4 CLI/IoT SDK modules + `ruff check . && ruff format --check .` | `src/core` (full suite) | Passed | All `3,660` tests passed (`skipped=420`), including `84` CLI/Azure IoT SDK tests in editable `[dev]` venv; `ruff check .` passed; `298 files already formatted` |
| Ephemeral editable venv (`-e src/core -e src/agents -e src/api`): `tests/test_document_controls.py` + `tests/test_role_endpoint_inventory.py` + `ruff check . && ruff format --check .` + `mypy` | `src/api` (`src-ci.yml` focused) | Passed | `test_document_controls` alone `18` tests OK (`187.1s`), combined with `test_role_endpoint_inventory` `44` tests OK (`153.7s`); `ruff check .` passed; `213 files already formatted`; `mypy`: `Success: no issues found in 297 source files` |
| `python3 tools/rename-zava-tests.py` | repository migration guard | Passed | `Ran 25 tests in 1.632s — OK` |
| `tools/rpi-checks.py` | full local gate | Skipped | Explicitly excluded (`Focused` validation tier per caller prompt) |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01` checked in `plan.md`; `phase-details.md` Phase Index set to `Complete`)
* Completed-work evidence and handoff prose: Reconciled (`changes.md` and parent `#117` artifacts aligned with commits `058fcc3e8` and `3efbe346a` atop `ad005cd5f` / `0358b9ad5`)
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining items, 3 routed follow-ups preserved)
* Review readiness: Ready for `rpi-review`

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-plan.md, `## Follow-Up Items`
* Add direct `SqlStore.rescan_pending()` reopen persistence and `out["blocked"]` counter unit-test assertions in `src/core/tests/test_document_rescan.py` (`RV-001` from parent `#117` review).
* Provision Azure Storage Defender malware scanning tags and quarantine infrastructure wiring in Bicep/deployment workflows (ADR 0002).
* Deliver remaining Issue #117 retention schedule and legal-hold DPO/Legal governance sign-off and automated purge evidence.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`; remaining: none)
* Validation coverage: Focused `src-ci.yml` tier complete (`src/core` 484 focused + 3,660 full tests, ruff, mypy; `src/api` 44 tests incl. `test_document_controls` and `test_role_endpoint_inventory`, ruff, mypy; `tools/rename-zava-tests.py` 25 tests)
* Blockers: none
* Current plan and detail updates: Recorded parent tip `ad005cd5f` (#1783 docs commit atop `0358b9ad5`) and local `src/api` editable-venv `mypy` / `PYTHONPATH=tests` note
* Follow-up items: `RV-001` (`SqlStore.rescan_pending()` test), Azure Storage Defender Bicep wiring, `#117` retention/legal-hold governance
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (`confirmed automatic RPI Agent`)
