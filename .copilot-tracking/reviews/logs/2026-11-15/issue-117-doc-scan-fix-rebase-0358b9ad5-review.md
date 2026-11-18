<!-- markdownlint-disable-file -->
# Review: Issue #117 Document Scan Fix (`test_resident_decisions`) and Rebase onto 0358b9ad5

## Scope and Evidence

* Task ID: issue-117-doc-scan-fix-rebase-0358b9ad5
* Review date: 2026-11-15
* Review scope: full task (`P01`, `P02`, `P03`)
* Assessed boundary: Rebase of `feat/demo-117-doc-scan` (`PR #1781`) onto latest stacked parent `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f` atop `0358b9ad5`), surgical pre-gate synthetic scan metadata fix in `src/core/tests/test_resident_decisions.py` (`3efbe346a`) preserving fail-closed missing-scan quarantine in `doc_controls.py`, worktree-isolated `src-ci.yml` validation across `src/core` and `src/api`, and parent `#117` + child RPI tracking reconciliation.
* Plan: .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-research.md (`C1`–`C8`), .copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md, `git log ad005cd5f..HEAD`, `git show 3efbe346a`, `git diff ad005cd5f..HEAD --stat`.

## Opening Review State

* Interpreted review goal: Verify once against workspace and git evidence that `feat/demo-117-doc-scan` rebased cleanly onto the latest `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f` atop `0358b9ad5`), resolved both `test_resident_acceptance_never_clears_technical_or_hazard_gates` failures without weakening `#117` fail-closed malware scan quarantine, passed focused `src-ci.yml` validation in `src/core` and `src/api`, and reconciled parent `#117` and child RPI records cleanly.
* Review scope: full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; plan, phase details, single-pass plan critique (`Pass`, `0` findings), changes record, research (`C1`–`C8`), parent `#117` artifacts, and git commits (`058fcc3e8`, `a68ca54fe`, `3efbe346a`) are complete and reconciled.
* Acceptance basis: `FR-FIX-01`..`FR-FIX-03`, `NFR-FIX-01`..`NFR-FIX-02`, plan `## Acceptance Criteria`, single-pass critique disposition (`Pass`), and `.github/copilot-instructions.md` validation/git conventions.
* First comparison boundary: Git ancestry (`0358b9ad5` and `ad005cd5f` -> `058fcc3e8` -> `a68ca54fe` -> `3efbe346a`) and exact diff of `3efbe346a` (`src/core/tests/test_resident_decisions.py`) versus `doc_controls.py` and `server.py`.
* Active read-only boundaries: Write authority limited exclusively to `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-review.md`.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass review on 2026-11-15 across all `P01`, `P02`, and `P03` markers, git commits `058fcc3e8`..`3efbe346a`, validation outputs, implementation-time updates, and follow-up items.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01`, `P01-T02` | `P01: Rebase onto Latest Stacked Parent (P01-T01) and Synthetic Gate Fixture Fix (P01-T02)` | Reconciled | Rebased cleanly onto `ad005cd5f` (1 docs commit `#1783` atop `0358b9ad5`) and committed `3efbe346a` with noreply email and `Co-authored-by` trailer. |
| `P02`, `P02-T01` | `P02: Worktree-Isolated src-ci.yml and Regression Validation (P02-T01)` | Reconciled | Verified worktree namespace paths and passed `src/core` (`484` focused + `3,660` full tests, `ruff`, `mypy`), `src/api` (`44` tests, `ruff`, `mypy`), and `tools/rename-zava-tests.py` (`25` tests). |
| `P03`, `P03-T01` | `P03: Pre-Review #117 and Child RPI Tracking Reconciliation (P03-T01)` | Reconciled | Appended `ad005cd5f` / `0358b9ad5` + `3efbe346a` lineage to parent `#117` records without altering original `Residual work` (`RV-001`) verdict, and reconciled child RPI markers/JSON. |
| `Follow-Up Items` | `Follow-Up Items` (3 items inherited from parent `#117`) | Reconciled | Kept outside active `P01`–`P03` scope and mirrored identically in `plan.md` and `changes.md`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `.git/config`, `feat/demo-117-doc-scan` history | Configured `8036360+jmservera@users.noreply.github.com` locally and rebased `#117` commits onto latest `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f` atop `0358b9ad5`) with zero conflicts (`058fcc3e8`, `a68ca54fe`). | `git merge-base --is-ancestor 0358b9ad5 HEAD` & `ad005cd5f` exit `0`; `server.py` diff empty. | Passed (`git diff --check` exit `0`) | Reconciled |
| `P01-T02` | `src/core/tests/test_resident_decisions.py` | Added `scan=dict(status="clean", scanner="Synthetic metadata fixture")` to synthetic `Store.EVIDENCE` pre-gate setup stubs in `test_resident_acceptance_never_clears_technical_or_hazard_gates` while leaving `doc_controls.py` untouched; committed as `3efbe346a`. | `git show 3efbe346a` (+7/-1 lines, noreply author, `Refs #117`, `Co-authored-by` trailer, zero `.copilot-tracking/` references). | Passed (`JsonResidentDecisions` & `SqlResidentDecisions` 2/2 OK, `ruff`, `mypy`) | Reconciled |
| `P02-T01` | `src/core/**`, `src/api/**`, `tools/rename-zava-tests.py` (read-only verification) | Asserted `zava_forward.{core,agents,api}.__path__` inside current worktree and ran focused `src-ci.yml` suites plus full `src/core` unit discovery and rename regression checks. | Recorded command outputs and counts in `changes.md`. | Passed (`src/core` 484 focused + 3,660 full tests, `ruff`, `mypy`; `src/api` 44 tests, `ruff`, `mypy`; `rename-zava-tests.py` 25 tests) | Reconciled |
| `P03-T01` | `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md`, `.copilot-tracking/rpi-sessions/2026-11-15/issue-117-doc-scan-state.json`, child `plan.md`, `phase-details.md`, `changes.md` | Appended `ad005cd5f` / `0358b9ad5` rebase and `3efbe346a` fix lineage to parent `#117` records (preserving original `Residual work` / `RV-001` outcomes) and checked off child `P01`–`P03` markers. | `git status --short` shows only `.copilot-tracking/` paths; original `RV-001` preserved intact. | Passed (`python3 -m json.tool` & `git diff --check` exit `0`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `Executive Summary`, `P01`, `P01-T01`, `P03` | Recorded that `origin/feat/demo-164-chat-grounding-provenance-0900` advanced by 1 docs-only commit (`ad005cd5f`, `#1783`) atop `0358b9ad5` prior to `git fetch` in `P01-T01`. | Caller explicitly requested rebasing onto the latest parent branch `origin/feat/demo-164-chat-grounding-provenance-0900`; `ad005cd5f` has `0358b9ad5` as immediate parent and zero `src/` edits. | Synchronized `Executive Summary`, `P01`, `P01-T01`, `P03` in `plan.md` and `Implementation-Time Plan and Detail Updates` in `changes.md`. | Not needed (immediately relevant current-state update preserving confirmed user intent; critique `Pass` unaffected). | Reconciled |
| `P02-T01` (local validation execution note) | Included `tests` in `src/api` `PYTHONPATH` for `unittest tests/test_document_controls.py` and used a cleaned-up `/tmp` editable venv (`-e src/core -e src/agents -e src/api`) for `src/api` `mypy`. | Matches `.github/copilot-instructions.md` (updated in `ad005cd5f`) and `.github/workflows/src-ci.yml` editable install contract without mutating shared `~/.local`. | Documented in `changes.md` (`Implementation-Time Plan and Detail Updates` and `Validation Record`). | Not needed (local judgment matching `src-ci.yml`). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: Single-pass plan critique (`.copilot-tracking/reviews/plans/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-plan-critique.md`) returned Verdict `Pass` (`Ready`) with `0` findings (`0` Critical, `0` High, `0` Medium, `0` Low), recorded in `plan.md` (`## Critique Disposition`) and `state.json`.
* Material revisions: None. Both implementation-time notes were ordinary local judgment / immediately relevant current-state updates preserving exact caller intent.
* Dependent-work pause assessment: No dependent-work pause was required; execution proceeded in strict `P01` -> `P02` -> `P03` order.
* Justification assessment: Supported by git history (`058fcc3e8`..`3efbe346a` atop `ad005cd5f` / `0358b9ad5`) and passing `src-ci.yml` checks.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Direct `SqlStore.rescan_pending()` reopen persistence and `out["blocked"]` counter unit-test assertions in `src/core/tests/test_document_rescan.py` (`RV-001` from parent `#117` review) | Non-blocking test-depth hardening from parent `#117` review outside the `test_resident_decisions.py` CI fix and rebase scope. | Distinct follow-up (`src/core/tests/test_document_rescan.py`) | Open; routed as distinct follow-up item. |
| Azure Storage Defender malware scanning tags and quarantine infrastructure wiring in Bicep/deployment workflows (ADR 0002) | Cloud infrastructure provisioning outside `src/core` and `src/api` application gate scope. | Distinct follow-up (`infra/` Bicep & deployment backlog) | Open; routed as distinct follow-up item. |
| Issue #117 retention schedule and legal-hold DPO/Legal governance sign-off and automated purge evidence | Separate governance and lifecycle criteria on `#117` (`PR #1781` uses `Refs #117`, not `Closes #117`). | Distinct follow-up (DPO/Legal governance & retention backlog) | Open; routed as distinct follow-up item. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

None. Zero defects, decision gaps, evidence gaps, or new residual-work items were found within the `issue-117-doc-scan-fix-rebase-0358b9ad5` task boundary.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| none | none | None | Zero `RV-xxx` findings on this task; inherited `#117` follow-up items remain tracked in `Plan Follow-Up Assessment`. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* none newly introduced in this task (inherited `#117` follow-ups `RV-001`, Azure Storage Defender Bicep wiring, and `#117` retention/legal-hold governance remain tracked as distinct follow-up choices).

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none (`P01`, `P02`, and `P03` complete; parent `RPI Agent` owns the post-Review `.copilot-tracking/` commit without pushing).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `git merge-base --is-ancestor 0358b9ad5 HEAD && git merge-base --is-ancestor ad005cd5f HEAD && git diff --check` | `feat/demo-117-doc-scan` git lineage | Passed | Exited `0`; commits `058fcc3e8`, `a68ca54fe`, and `3efbe346a` sit cleanly atop `ad005cd5f` / `0358b9ad5` |
| `git --no-pager diff ad005cd5f..HEAD -- src/api/src/zava_forward/api/server.py` | `src/api` route inventory | Passed | Empty diff; zero HTTP routes added or modified |
| `PYTHONPATH=src:tests python3 -m unittest test_resident_decisions test_technical_evidence_usability test_document_rescan test_resident_documents -q && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy` | `src/core` (`src-ci.yml` focused) | Passed | `Ran 484 tests in 14.844s — OK (skipped=174)`; `ruff` clean (`297 files already formatted`); `mypy` clean (`351 source files`) |
| Full `src/core` `unittest discover -s tests -q` + editable `[dev]` venv on 4 CLI/IoT SDK modules + `ruff check . && ruff format --check .` | `src/core` (complete unit suite) | Passed | All `3,660` tests OK (`skipped=420`); `298 files already formatted` |
| Ephemeral editable venv (`-e src/core -e src/agents -e src/api`): `tests/test_document_controls.py` + `tests/test_role_endpoint_inventory.py` + `ruff check . && ruff format --check .` + `mypy` | `src/api` (`src-ci.yml` focused) | Passed | `test_document_controls` `18` tests OK, combined `44` tests OK; `ruff` clean (`213 files already formatted`); `mypy` clean (`297 source files`) |
| `python3 tools/rename-zava-tests.py` | repository migration check | Passed | `Ran 25 tests in 1.632s — OK` |
| `tools/rpi-checks.py` | full local gate | Skipped | Explicitly excluded (`Focused` validation tier per caller instructions) |

## Outcome

* Outcome: Conformant
* Outcome rationale: All planned phases (`P01`–`P03`), requirements (`FR-FIX-01`–`FR-FIX-03`, `NFR-FIX-01`–`NFR-FIX-02`), acceptance criteria, and focused `src-ci.yml` checks across `src/core` and `src/api` are satisfied with zero defects, intact fail-closed malware scan quarantine in `doc_controls.py`, untouched `server.py` route inventory, and preserved original parent `#117` Review records.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | none | Inherited parent `#117` follow-ups remain distinct ranked choices at the automatic `Follow-up` checkpoint |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused `src-ci.yml` tier complete (`src/core` 484 focused + 3,660 full tests, `ruff`, `mypy`; `src/api` 44 tests incl. `test_document_controls` & `test_role_endpoint_inventory`, `ruff`, `mypy`; `tools/rename-zava-tests.py` 25 tests; `tools/rpi-checks.py` skipped per Focused tier)
* Blockers: none
