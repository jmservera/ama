<!-- markdownlint-disable-file -->
# Review: Issue #164 Chat Multi-Turn Revocation, Refusal Preservation, and Separate Held-Out Evaluation

## Scope and Evidence

* Task ID: issue-164-chat-eval-revocation
* Review date: 2026-11-15
* Review scope: Full task (`P01` through `P04`)
* Assessed boundary: Remaining local-testable RAI multi-turn, mid-thread revocation, human-workflow refusal preservation, version-bound held-out freeze, and separate multi-turn vs single-turn reporting criteria for Issue #164 across `src/core`, `src/agents`, and `src/api`, validated under the focused tier without live task enablement (`state="disabled"`).
* Plan: .copilot-tracking/plans/2026-11-15/issue-164-chat-eval-revocation-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-164-chat-eval-revocation-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/issue-164-chat-eval-revocation-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-164-chat-eval-revocation-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/issue-164-chat-eval-revocation-research.md (`C1`–`C17`), Git diff across `src/core`, `src/agents`, and `src/api`, and focused `unittest`, `mypy`, and `ruff` runs across all three packages.

## Opening Review State

* Interpreted review goal: Verify once with evidence that full-plan implementation (`P01`–`P04`) conforms to all Issue #164 local-testable multi-turn revocation, refusal-routing, held-out freeze, package-isolation, and separate reporting requirements while preserving live `disabled` gates and test-ownership caps.
* Review scope: Full task (`P01`, `P02`, `P03`, `P04`)
* Evidence readiness: Ready — plan markers, phase details, plan critique (`PC-001`–`PC-004`), changes record, source diffs, and focused validation results are complete and reconciled.
* Acceptance basis: Plan `## Functional Requirements`, `## Non-Functional Requirements`, `## Acceptance Criteria`, `## Test Ownership and Evidence Matrix`, and `## Critique Disposition` (`PC-001`–`PC-004`).
* First comparison boundary: Plan-to-change marker reconciliation and `ALLOWED = {"core"}` boundary compliance in `src/core`, bounded to the local-testable increment without live provider calls or owner threshold sign-off.
* Active read-only boundaries: Write access limited strictly to `.copilot-tracking/reviews/logs/2026-11-15/issue-164-chat-eval-revocation-review.md` (and parent RPI state transition after Review returns).
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass assessment on 2026-11-15 across all four phases (`P01`–`P04`), 10 changed/created source and test files under `src/`, and 533 executed unit tests plus `mypy` and `ruff` checks across `src/core`, `src/agents`, and `src/api`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `P01: Core RegulatoryChat Hardening and zava_forward.core.ai_eval Contract` | Reconciled | Both markers `[x]`; `regulatory_chat.py` and `ai_eval.py` match plan and `PC-001`/`PC-003`/`PC-004` dispositions. |
| `P02` (`P02-T01`) | `P02: Agents Multi-Turn Golden Coverage and Held-Out Expected-Outcome Freeze` | Reconciled | Marker `[x]`; `chat_eval.py`, `chat_golden.json`, and `chat_heldout.py` match `PC-002` and `PC-003` dispositions. |
| `P03` (`P03-T01`) | `P03: Separate Chat Multi-Turn Reporting in /api/ai/report` | Reconciled | Marker `[x]`; `/api/ai/report` emits top-level `chat_evaluation` alongside unchanged single-turn `evaluation` and `live`. |
| `P04` (`P04-T01`, `P04-T02`) | `P04: Deterministic Regression Suites and Focused Validation` | Reconciled | Markers `[x]`; test additions (`14 <= 22`, `3 <= 3`, `3 <= 4`, `2 <= 4`, zero removals) and focused validation commands match the locked matrix. |
| `Follow-Up Items` | `Follow-Up Items` (owner-gated held-out labelling, reviewer timing measurement, live budget/model run, and threshold approval) | Reconciled | Preserved outside active `Pxx`/`Pxx-Txx` completion claims while `enablement.state` stays `"disabled"`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/regulatory_chat.py` | Added `_question_refusal` (`self.refuse` precedence + `out_of_scope` fallback evaluated before special-category redaction in `ask()`), post-`detail` `ai_consent_state` checks in `bundle()` and `foundry_query()`, transactional re-check in `ask()`, and `ChatForbidden` block in `doubt()`. | Diff inspection and unit proofs in `test_regulatory_chat.py` and `test_ai_eval.py`. | `test_regulatory_chat.py` (28 tests JSON + SQLite), `mypy`, `ruff` Passed. | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/ai_eval.py` | Created pure-`core` multi-turn `PanelSession` and `RegulatorySession` harness, 8 built-in scenarios, closed-set `expected_outcome_problems`, `expected_outcomes_digest`, `heldout_freeze_problems`, `score_heldout`, 4-part `REVIEW_EFFORT_INPUTS`, `chat_enablement_state` (`disabled`), and `separate_evaluation_report`. | Zero imports outside `zava_forward.core`; `run_core_suite()` passes 8/8 scenarios. | `test_ai_eval.py` (14 tests), `test_dependency_rule.py` (2 tests), `mypy` (`strict = true`), `ruff` Passed. | Reconciled |
| `P02-T01` | `src/agents/src/zava_forward/agents/chat_eval.py`, `src/agents/evals/chat_golden.json`, `src/agents/src/zava_forward/agents/chat_heldout.py` | Added non-destructive `revoke_source` and `set_ai_consent` to `Run.apply`, `WORKFLOW_RULES` union in `_comparison`, golden source/AI-consent revocation and multi-turn ambiguity scenarios, and frozen `expected_outcome_problems` + `expected_outcomes_sha256` + `enablement` in `chat_heldout`. | Preserved `component_probes == 5` and all existing golden invariants while rejecting vacuous `expect={}` held-out turns. | `src/agents` `test_chat_*.py` (118 tests), `mypy`, `ruff` Passed. | Reconciled |
| `P03-T01` | `src/api/src/zava_forward/api/server.py` | Added separate `"chat_evaluation": chat_eval.run_eval()` sibling in `/api/ai/report` without altering single-turn `"evaluation"` or `"live"`. | Endpoint tests confirm single-turn metrics remain unchanged even when `chat_evaluation` fails, and live tasks stay disabled. | `src/api` `test_ai_tasks.py` (71 tests), `test_regulatory_chat_api.py` (13 tests), `test_chat_*.py` (151 tests), `mypy`, `ruff` Passed. | Reconciled |
| `P04-T01`, `P04-T02` | `src/core/tests/test_ai_eval.py`, `src/core/tests/test_regulatory_chat.py`, `src/agents/tests/test_chat_heldout.py`, `src/api/tests/test_ai_tasks.py` | Added 14 + 3 + 3 + 2 deterministic unit and endpoint regression tests covering Criteria 1, 2, and 3 including negative/failure-injection checks. | All counts within locked matrix caps and zero existing tests removed. | 533 focused tests + `mypy` (621 files) + `ruff` Passed. | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` (`RegulatoryChat.ask` pre-redaction refusal check) | Evaluated `_question_refusal(clean_q)` before `redact(clean_q)` while still persisting `masked` in `chat_repo`, preventing `chat_privacy.redact` from replacing `"Diagnose"` with `"[special_category removed]"` and bypassing `out_of_scope` `"diagnose"` refusal routing. | Triggered by deterministic `P04-T01` multi-turn refusal tests; local engineering judgment requiring no user decision because it enforces approved refusal-preservation requirements without altering privacy storage guarantees. | Recorded under `## Implementation-Time Plan and Detail Updates` in `.copilot-tracking/changes/2026-11-15/issue-164-chat-eval-revocation-changes.md`. | Not needed (`PC-001`–`PC-004` already resolved; no scope/architecture divergence). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four critique findings (`PC-001` post-`detail` `ai_consent_state` ordering + transactional `ask()` re-check + `self.refuse` precedence; `PC-002` non-destructive `revoke_source` + `WORKFLOW_RULES` union + golden invariants; `PC-003` strict closed-set `expected_outcome_problems` + canonical 4-item `REVIEW_EFFORT_INPUTS`; `PC-004` per-package `mypy`/`ruff` with `Any`-typed untyped `core` collaborators and zero `pyproject.toml` edits) were applied and verified by tests.
* Material revisions: None — no scope, architecture, or acceptance-criteria divergence arose during implementation.
* Dependent-work pause assessment: No pause required; phases executed strictly in dependency order (`P01` -> `P02` -> `P03` -> `P04`).
* Justification assessment: Supported by deterministic unit, static-type, lint, and package-boundary evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Owner-approved chat quality thresholds, named accountable reviewer appointment, independently labelled non-implementer held-out dataset execution, budget-authorized serving-model evaluation, and competent-human review effectiveness exercises under Issue #164 | Requires human owner governance sign-off, independent non-implementer labelling, and paid live model budget outside offline local-testable verification; `chat-case-conversation` must remain `disabled` until approved. | Repository owner / named accountable reviewer governance workflow for Issue #164. | Open distinct follow-up route (non-defect governance gate; `enablement.state == "disabled"` verified). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Execute post-merge non-implementer held-out dataset, reviewer timing measurement, and owner threshold sign-off before enabling live chat

* Related scope: `Follow-Up Items` (outside active `P01`–`P04` local-testable scope)
* Evidence: .copilot-tracking/plans/2026-11-15/issue-164-chat-eval-revocation-plan.md (`## Follow-Up Items`), `src/core/src/zava_forward/core/ai_eval.py` (`chat_enablement_state`), and `src/agents/src/zava_forward/agents/chat_eval.py` (`enablement_decision`) truthfully report `review_effort.status == "not measured"` (4 missing inputs) and `enablement.state == "disabled"`.
* Impact: Prevents premature live activation of `chat-case-conversation` until human effectiveness, reviewer effort vs case-card comparator, independent held-out labelling, and owner threshold sign-off are completed.
* Destination: `follow_up`
* Smallest useful next action: Keep `chat-case-conversation` `disabled` when merging this deterministic gate increment and schedule the owner-gated held-out and human-effectiveness exercise when live model evaluation is requested.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `follow_up` | Repository owner / Issue #164 governance gate | Non-blocking post-merge human governance and live-evaluation prerequisite explicitly out of scope for offline local-testable increment |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Post-merge Issue #164 human governance prerequisites (`RV-001`): non-implementer held-out scenario labelling, measured 4-part reviewer effort against the manual case-card comparator, budget-authorized serving-model run, and owner threshold approval before changing `chat-case-conversation` from `disabled`.

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none (`P01`–`P04` complete)

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m unittest discover -s tests -p "test_*ai_eval*.py" -q` | `src/core` | Passed | 14 tests OK |
| `python3 -m unittest discover -s tests -p "test_regulatory_chat.py" -q`, `test_chat_*.py`, `test_dependency_rule.py` | `src/core` | Passed | 28 + 136 + 2 tests OK (`ALLOWED = {"core"}` verified) |
| `python3 -m mypy src tests`, `python3 -m ruff check .`, `python3 -m ruff format --check .` | `src/core` | Passed | `mypy` (`strict = true`) 0 issues in 334 files; `ruff` clean across 281 formatted files |
| `PYTHONPATH=../core/tests python3 -m unittest discover -s tests -p "test_chat_*.py" -q` | `src/agents` | Passed | 118 tests OK |
| `python3 -m mypy src tests`, `python3 -m ruff check .`, `python3 -m ruff format --check .` | `src/agents` | Passed | `mypy` 0 issues in 66 files; `ruff` clean across 62 formatted files |
| `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_ai_tasks.py" -q`, `test_regulatory_chat_api.py`, `test_chat_*.py` | `src/api` | Passed | 71 + 13 + 151 (1 skipped) tests OK |
| `python3 -m mypy src tests`, `python3 -m ruff check .`, `python3 -m ruff format --check .` | `src/api` | Passed | `mypy` 0 issues in 221 files; `ruff` clean across 196 formatted files |
| `python3 tools/rpi-checks.py --all` | Repository | Skipped | Explicitly skipped per caller instructions specifying the focused validation tier |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every planned task (`P01-T01` through `P04-T02`), acceptance criterion, critique disposition (`PC-001`–`PC-004`), package-isolation invariant (`ALLOWED = {"core"}`), test-ownership bound, and focused validation check passed with zero open implementation defects, decision gaps, or evidence gaps. Post-merge owner governance gates (`RV-001`) are truthfully enforced in code (`enablement.state == "disabled"`, `review_effort.status == "not measured"`) and routed as distinct follow-up work.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up (`RV-001`) | Repository owner / Issue #164 post-merge governance exercise while keeping `chat-case-conversation` `disabled` |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: 533 focused unit/endpoint tests passed across `src/core` (180), `src/agents` (118), and `src/api` (235), plus `mypy` (621 source/test files) and `ruff check` / `ruff format --check` across all three packages; `tools/rpi-checks.py --all` skipped per caller instruction.
* Blockers: none
