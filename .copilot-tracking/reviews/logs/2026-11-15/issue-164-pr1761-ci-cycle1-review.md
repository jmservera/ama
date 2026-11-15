<!-- markdownlint-disable-file -->
# Review: Issue #164 PR #1761 Cycle 1 Hosted CI `src-api` Fix

## Scope and Evidence

* Task ID: issue-164-pr1761-ci-cycle1
* Review date: 2026-11-15
* Review scope: Full task (`P01` / `P01-T01`)
* Assessed boundary: Cycle 1 test-contract alignment in `src/api/tests/test_ai_consumption_api.py` (`test_manager_report_local_http_and_bad_period`) for `GET /api/ai/report` held-metering responses after Issue #164 added separate `chat_evaluation` reporting, validated under the focused tier without pushing or enabling live chat tasks (`state="disabled"`).
* Plan: .copilot-tracking/plans/2026-11-15/issue-164-pr1761-ci-cycle1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-164-pr1761-ci-cycle1-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/issue-164-pr1761-ci-cycle1-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-164-pr1761-ci-cycle1-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/issue-164-pr1761-ci-cycle1-research.md (`C1`–`C4`), Git diff in `src/api/tests/test_ai_consumption_api.py`, `src/api/src/zava_forward/api/server.py` (`GET /api/ai/report`), and focused `unittest`, `ruff`, and `mypy` validation in `src/api`.

## Opening Review State

* Interpreted review goal: Verify once with evidence that `P01-T01` resolves the hosted `src-api` CI failure on PR #1761 (`AssertionError: Items in the first set but not the second: 'chat_evaluation'`) while preserving `GET /api/ai/report` consumption-hold semantics, `enablement.state == "disabled"`, and `src/api` lint/format/type gates.
* Review scope: Full task (`P01`, `P01-T01`)
* Evidence readiness: Ready — plan markers, phase details, `Pass` plan critique, changes record, source diff, and focused `src/api` validation results are complete and reconciled.
* Acceptance basis: Plan `## Functional Requirements`, `## Non-Functional Requirements`, `## Acceptance Criteria`, `## Test Ownership and Evidence Matrix`, and `## Critique Disposition`.
* First comparison boundary: Plan-to-change reconciliation and exact diff verification on `test_manager_report_local_http_and_bad_period` in `src/api/tests/test_ai_consumption_api.py`.
* Active read-only boundaries: Write access limited strictly to `.copilot-tracking/reviews/logs/2026-11-15/issue-164-pr1761-ci-cycle1-review.md` (and parent RPI state transition after Review returns).
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass assessment on 2026-11-15 across `P01` (`P01-T01`), 1 modified test file (`src/api/tests/test_ai_consumption_api.py`), 112 executed unit tests (`test_ai_consumption_api.py` and `test_ai_tasks.py`), `ruff check src tests`, `ruff format --check src tests` (195 files), and `mypy` (single-file and full 221-file `src tests`).

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`) | `P01: Align Held Manager Report Test Contract and Validate src/api (P01-T01)` | Reconciled | Both markers `[x]`; `test_ai_consumption_api.py` diff and validation match plan and test-ownership matrix (`0` removals, `0` new test methods). |
| `Follow-Up Items` | `Follow-Up Items` (post-merge Issue #164 owner governance gates `RV-001`) | Reconciled | Preserved outside active `P01` completion claims while `enablement.state == "disabled"` is explicitly asserted. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/api/tests/test_ai_consumption_api.py` | Updated `test_manager_report_local_http_and_bad_period` so `set(held)` expects `{"evaluation", "chat_evaluation", "live", "registry", "consumption"}` and verified `held["chat_evaluation"]` key, `version`, and `enablement["state"] == "disabled"` parity during `"meter-capacity-reached"` and `"meter-evidence-invalid"` holds. | Git diff inspection and 112 passing unit tests across `tests/test_ai_consumption_api.py` and `tests/test_ai_tasks.py`. | `unittest` (112 OK), `ruff check`, `ruff format --check` (195 files), `mypy` (1-file and 221-file) Passed. | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` (local user editable links) | Restored `~/.local/lib/python3.12/site-packages` editable links (`-e src/core -e src/agents -e src/api`) after a pruned sibling worktree left broken `.pth` entries causing `mypy` `import-not-found` on `zava_forward.agents`. | Triggered by initial `mypy` run; local environment repair consistent with repository instructions requiring `pip` installation of `src/<project>` distributions, with zero tracked-file changes. | Recorded under `## Implementation-Time Plan and Detail Updates` in `.copilot-tracking/changes/2026-11-15/issue-164-pr1761-ci-cycle1-changes.md`. | Not needed (zero scope or plan divergence). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: Single-pass critique returned `Pass` with zero findings; downstream coordinator external-receipt refresh note preserved.
* Material revisions: None.
* Dependent-work pause assessment: Not applicable (`P01-T01` executed cleanly in one phase).
* Justification assessment: Supported by exact source diff and green `unittest`, `ruff`, and `mypy` evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Post-merge Issue #164 owner governance prerequisites (`RV-001` from parent task): non-implementer held-out dataset labelling, 4-part reviewer effort measurement vs case-card comparator, budget-authorized serving-model evaluation, and owner threshold sign-off | Requires human governance approval, independent labeller, and live model spend outside offline Cycle 1 CI repair; `chat-case-conversation` remains `disabled`. | Repository owner / Issue #164 governance workflow; push and hosted CI observation on PR #1761 owned by caller/coordinator. | Open distinct follow-up route (`RV-001` carried forward; non-defect). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Observe hosted `src-api` CI after coordinator push and retain Issue #164 post-merge human governance gates

* Related scope: `Follow-Up Items` (outside offline unpushed Cycle 1 fix scope)
* Evidence: Caller instruction explicitly prohibited `git push`; local `src/api` checks pass (`112` unit tests, `ruff`, and `mypy`), while hosted CI on the new Cycle 1 commit remains unobserved until pushed, and `held["chat_evaluation"]["enablement"]["state"] == "disabled"` preserves the Issue #164 owner threshold gate.
* Impact: Hosted branch-protection checks and human review/governance gates remain required before merge or live chat enablement.
* Destination: `follow_up`
* Smallest useful next action: Coordinator pushes the frozen branch head to PR #1761 to observe hosted `src-api` CI, while keeping `chat-case-conversation` `disabled` pending post-merge owner governance sign-off.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `follow_up` | Coordinator (push & hosted CI observation on PR #1761) and repository owner (Issue #164 post-merge governance gates) | Non-blocking operational/governance follow-up outside unpushed local Cycle 1 scope |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Coordinator push to PR #1761 to observe hosted `src-api` CI on the Cycle 1 head, plus existing Issue #164 post-merge owner governance prerequisites while `chat-case-conversation` remains `disabled`.

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none (`P01` / `P01-T01` complete)

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=src:tests:../core/src:../agents/src:../orchestrator/src:../importer/src:../core/tests:../agents/tests python3 -B -m unittest tests/test_ai_consumption_api.py tests/test_ai_tasks.py` | `src/api` | Passed | 112 tests OK |
| `python3 -m ruff check src tests` | `src/api` | Passed | All checks passed |
| `python3 -m ruff format --check src tests` | `src/api` | Passed | 195 files already formatted |
| `python3 -m mypy tests/test_ai_consumption_api.py` | `src/api` | Passed | 0 issues in 1 source file |
| `python3 -m mypy src tests` | `src/api` | Passed | 0 issues in 221 source files |
| Hosted CI (`src-api`) on Cycle 1 commit | GitHub Actions | Unobserved | Not pushed per explicit caller instruction |

## Outcome

* Outcome: Conformant
* Outcome rationale: `P01-T01` surgically resolves the PR #1761 hosted `src-api` `set(held)` assertion failure in `src/api/tests/test_ai_consumption_api.py`, verifies `chat_evaluation` parity and `"disabled"` enablement under both metering holds, and passes all targeted `unittest`, `ruff`, and `mypy` checks with zero defects.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up (`RV-001`) | Coordinator push + hosted CI observation on PR #1761; repository owner Issue #164 post-merge governance gates |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: 112 unit tests (`test_ai_consumption_api.py`, `test_ai_tasks.py`), `ruff check src tests`, `ruff format --check src tests` (195 files), and `mypy` (`tests/test_ai_consumption_api.py` and full 221-file `src tests`) all passed locally; hosted CI unobserved pending coordinator push.
* Blockers: none
