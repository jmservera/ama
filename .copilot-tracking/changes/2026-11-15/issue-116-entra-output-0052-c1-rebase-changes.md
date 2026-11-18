<!-- markdownlint-disable-file -->
# RPI Changes: Cycle 1 Rebase Continuation (`c1-rebase`) Onto Merged Parent Tip `0c1fa1da4` (`PR #1769`)

## Metadata

* Task ID: issue-116-entra-output-0052-c1-rebase
* Related plan: .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-rebase-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-rebase-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P02`, `P02-T01`
* All remaining active-plan markers: none
* Status basis: Both planned phases (`P01`, `P02`) and tasks (`P01-T01`, `P02-T01`) completed cleanly and passed every Focused-tier and cross-feature validation suite.

## Execution Summary

Configured repository-local privacy-safe git email (`8036360+jmservera@users.noreply.github.com` via `gh api user`), archived untracked `c1-rebase` `.copilot-tracking/` files to the session workspace, fetched `origin feat/demo-164-chat-grounding-provenance-0900` (which resolved to `d8cb35d25` from `PR #1770` `Refs #133`, direct child of `0c1fa1da4` from `PR #1769` `Refs #83`), and rebased `7b882614d..e7d05fab4` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`d8cb35d25`), producing rebased commits `fc44a697c` (`7b882614d'`) and `41091c2a0` (`e7d05fab4'`). Resolved the sole conflict file `src/core/src/zava_forward/core/store.py` (`_queue_candidates` and `_work_context`) preserving both `0c1fa1da4`'s `handoff_policy` cache-key entry and 4-argument `handoff_view(c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff"))` calls (alongside auto-merged `detail` and inherited `taskqueues.MEMBERSHIP_REVISION = 4` + `sqlstore._queue_fingerprint`) and `7b882614d`'s formatting and `#116` role-visibility projections (`draft`, `_clean_doc_ai_metadata`, `add_document`, `read_document`, `ai_run`, `_rec_view`, `ai_priority`, `funding_draft`, `ai_live_report`). Restored `c1-rebase` tracking files, ran all Focused validation commands (`115` caller unit tests, `174` cross-feature `#83` + `#133` + `#116` unit tests, `src/core` `ruff` + `mypy`, `src/api` `ruff`, and `25` `tools/rename-zava-tests.py` tests — all `exit 0`), updated `issue-116-entra-output-0052-c1-changes.md` and `issue-116-entra-output-0052-c1-review.md` (preserving `c1`'s original `Outcome: Conformant`), and reconciled all `c1-rebase` artifacts ready for single-pass `rpi-review`.

## Completed Work

### Parent Branch Fetch, Rebase Onto `0c1fa1da4` -> `d8cb35d25`, and `store.py` Conflict Resolution

* Related phase or task: `P01`, `P01-T01`
* Files: `src/core/src/zava_forward/core/store.py`
* What changed and why: Executed `git fetch origin feat/demo-164-chat-grounding-provenance-0900` (fetching `d8cb35d25` / `PR #1770` directly atop `0c1fa1da4` / `PR #1769`) and `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`. `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_role_endpoint_inventory.py`, and `Store.detail` auto-merged cleanly; `taskqueues.MEMBERSHIP_REVISION = 4` and `sqlstore._queue_fingerprint` carried over untouched from `0c1fa1da4`; `d8cb35d25` (`#133` aftercare neutral-text hardening) merged with zero file overlap; resolved the 2 conflict blocks in `src/core/src/zava_forward/core/store.py` (`_queue_candidates` and `_work_context`) to combine `7b882614d`'s multi-line Ruff formatting with `0c1fa1da4`'s `json.dumps(self.data.get("handoff_policy"), sort_keys=True)` and `handoff_view(c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff"))`, while preserving all `#116` role-visibility methods; `e7d05fab4` replayed cleanly as `41091c2a0` atop `fc44a697c` with zero conflicts.
* Completion evidence: Both `git merge-base --is-ancestor 0c1fa1da4 HEAD` and `git merge-base --is-ancestor origin/feat/demo-164-chat-grounding-provenance-0900 HEAD` exited `0`; `git diff d8cb35d25..HEAD -- src/core/src/zava_forward/core/taskqueues.py src/core/src/zava_forward/core/sqlstore.py` returned empty; zero conflict markers remained.
* Validation: Passed (`test_handoff_escalation_83.py`, `test_handoff_escalation_api_83.py`, `test_ai_tasks.py`, `test_data_protection.py`, `src/core` `ruff` + `mypy`, `src/api` `ruff`).

### Focused Validation, Parent `c1` Record Updates, and Pre-Review Reconciliation

* Related phase or task: `P02`, `P02-T01`
* Files: `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-116-entra-output-0052-c1-review.md`, `.copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-rebase-plan.md`, `.copilot-tracking/details/2026-11-15/issue-116-entra-output-0052-c1-rebase-phase-details.md`, `.copilot-tracking/changes/2026-11-15/issue-116-entra-output-0052-c1-rebase-changes.md`
* What changed and why: Executed all Focused validation suites on the rebased working tree (disclosing `test_design_system_source_contract.py` -> `test_design_system.py` per `PC-001` and adding `#133` aftercare suites alongside `#83` and `#116` cross-feature suites). Updated `c1-changes.md` and `c1-review.md` to record the rebase onto `0c1fa1da4` -> `d8cb35d25`, rebased SHAs `fc44a697c` and `41091c2a0`, `store.py` conflict resolution, and post-rebase validation while preserving `c1-review.md`'s original `Outcome: Conformant`. Reconciled `c1-rebase` plan, phase details, and changes record ready for single-pass `rpi-review`.
* Completion evidence: All 5 validation commands exited `0` (`115` + `174` unit tests, `ruff`, `mypy`, `25` migration tests) and all active `Pxx`/`Pxx-Txx` markers are checked.
* Validation: Passed (`0` errors across all executed suites).

## Implementation-Time Plan and Detail Updates

### Fetched Parent Tip Advance From `0c1fa1da4` (`PR #1769`) to `d8cb35d25` (`PR #1770`)

* Affected plan area or markers: `Executive Summary`, `P01`, `P01-T01`, `P02`, `P02-T01`
* What changed: Recorded that `git fetch origin feat/demo-164-chat-grounding-provenance-0900` fetched `d8cb35d25` (`PR #1770`, `Refs #133`), whose direct parent is `0c1fa1da4` (`PR #1769`, `Refs #83`), and included `#133`'s three test modules (`test_aftercare.py`, `test_aftercare_intake.py`, `test_aftercare_served.py`) in `P02-T01`'s cross-feature unit run.
* Why: Immediately relevant current-state update preserving caller intent — rebasing onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`d8cb35d25`) keeps `feat/ai-116-entra-output-0052` fast-forward aligned with the live parent branch tip while including `0c1fa1da4` as an immediate ancestor and introducing zero additional merge conflicts (`d8cb35d25` is 100% file-disjoint from `#116`).
* Triggering evidence: `git fetch origin feat/demo-164-chat-grounding-provenance-0900` output (`d8cb35d25445b19b0533e30aec39842e992474a3`, `git log 7f83f4749..d8cb35d25`).
* User answer or decision: none (immediately relevant current-state update per `rpi-implement` protocol).
* Reconciliation performed: Synchronized `Executive Summary`, `P01`, `P01-T01`, `P02`, `P02-T01`, `Phase Index`, `Completion Evidence`, and `Handoff` across `c1-rebase-plan.md`, `c1-rebase-phase-details.md`, and `c1-rebase-changes.md`.
* Planning and critique state: Not needed; preserves approved plan intent and `PC-001`..`PC-003` dispositions.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api/src:src/api/tests python3 -m unittest src/api/tests/test_ai_tasks.py src/api/tests/test_design_system.py src/core/tests/test_data_protection.py -q` | Caller primary `core` + `api` suites (`JsonTasks` & `SqlTasks` + design-system contract) | Passed | `Ran 115 tests in 41.074s — OK` (`src/api/tests/test_design_system_source_contract.py` is absent in repository history and mapped to canonical `src/api/tests/test_design_system.py` per `PC-001`) |
| `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api:src/api/src:src/api/tests python3 -m unittest src/core/tests/test_handoff_escalation_83.py src/api/tests/test_handoff_escalation_api_83.py src/core/tests/test_aftercare.py src/core/tests/test_aftercare_intake.py src/api/tests/test_aftercare_served.py src/api/tests/test_role_endpoint_inventory.py src/api/tests/test_content_standard.py src/core/tests/test_human_review_effectiveness_223.py -q` | Cross-feature `#83` + `#133` + `#116` regression suites | Passed | `Ran 174 tests in 61.017s — OK` |
| `cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy` | `src/core` lint, format, and static types | Passed | `All checks passed!`, `284 files already formatted`, `Success: no issues found in 337 source files` |
| `cd src/api && python3 -m ruff check . && python3 -m ruff format --check .` | `src/api` lint and format | Passed | `All checks passed!`, `197 files already formatted` |
| `python3 tools/rename-zava-tests.py` | Repository migration regression | Passed | `Ran 25 tests in 0.564s — OK` |
| `python3 tools/rpi-checks.py --all` / Docker builds | Full repository gate | Skipped | Outside caller Focused validation scope |

## Pre-Review Reconciliation

* Plan markers and phase details: Current (`P01`, `P01-T01`, `P02`, `P02-T01` checked and `Complete`)
* Completed-work evidence and handoff prose: Current
* Validation, blockers, remaining work, and follow-up items: Current
* Review readiness: Ready for single-pass `rpi-review`

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/issue-116-entra-output-0052-c1-rebase-plan.md, `## Follow-Up Items`
* Extract shared post-provider record-visibility scrubbing helper across `ai_tasks._record_view`, `Store._rec_view`, and `ChatIsolation.scrub_thread` (carry-forward engineering-quality cleanup outside `c1-rebase`).
* Organisational control-owner confirmation of OD-14 / OD-19 (`ZF_REASON_ROLES`) and live Microsoft Entra B2B tenant configuration (external governance items outside repository code).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (`P01`, `P02`); completed: `P01`, `P01-T01`, `P02`, `P02-T01`; remaining: none
* Validation coverage: `115` caller unit tests (`OK`), `174` cross-feature `#83`/`#133`/`#116` unit tests (`OK`), `src/core` `ruff` (`284` files) + `mypy` (`0` issues in `337` files), `src/api` `ruff` (`197` files), and `tools/rename-zava-tests.py` (`25` tests, `OK`)
* Blockers: none
* Current plan and detail updates: Recorded fetched parent tip advance (`0c1fa1da4` -> `d8cb35d25`, `PR #1770`) and added `#133` aftercare regression suites to cross-feature validation
* Planning and critique state: Ready (`PC-001`..`PC-003` satisfied)
* Follow-up items: Shared record-visibility helper extraction (`RV-001`); external OD-14/OD-19 and Entra tenant governance
* Review readiness or no-handoff reason: Ready for single-pass `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
