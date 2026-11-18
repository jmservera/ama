<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #164 Chat Multi-Turn Revocation, Refusal Preservation, and Separate Held-Out Evaluation

## Metadata

* Task ID: issue-164-chat-eval-revocation
* Task slug: issue-164-chat-eval-revocation
* Related plan: .copilot-tracking/plans/2026-11-15/issue-164-chat-eval-revocation-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-164-chat-eval-revocation-research.md (`C1`–`C17`), docs/prds/zava-forward-retrofit-programme-demonstrator.md, GitHub Issue #164

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Core `RegulatoryChat` Hardening and `zava_forward.core.ai_eval` Contract | ready | P01, P01-T01, P01-T02 |
| P02 | Agents Multi-Turn Golden Coverage and Held-Out Expected-Outcome Freeze | ready | P02, P02-T01 |
| P03 | Separate Chat Multi-Turn Reporting in `/api/ai/report` | ready | P03, P03-T01 |
| P04 | Deterministic Regression Suites and Focused Validation | ready | P04, P04-T01, P04-T02 |

<!-- rpi:phase id=P01 -->
## P01: Core `RegulatoryChat` Hardening and `zava_forward.core.ai_eval` Contract

### Context

`src/core` owns `ChatPanel`, `ChatIsolation`, `RegulatoryChat`, `ai_registry`, and `ai_tasks`, and `src/core/tests/test_dependency_rule.py` enforces `ALLOWED = {"core"}` (`C1`). Currently `src/core/src/zava_forward/core/ai_eval.py` is absent (`C2`), and `RegulatoryChat` relies solely on a caller-supplied `refuse` callback for out-of-scope prompts while omitting `ai_consent_state` checks on mid-thread resident AI-consent withdrawal (`C7`, `C16`).

### Intent

Make `RegulatoryChat` enforce mid-thread resident AI-consent withdrawal and fallback `out_of_scope` workflow routing directly in `core`, and implement `src/core/src/zava_forward/core/ai_eval.py` as a pure-`core` multi-turn chat evaluation, version-bound held-out freeze, and separate multi-turn vs single-turn reporting module.

### Boundaries

* Included: `src/core/src/zava_forward/core/regulatory_chat.py` and `src/core/src/zava_forward/core/ai_eval.py`.
* Excluded: Any import of `zava_forward.agents` or `zava_forward.api` inside `src/core`; any live provider call or task enablement change.

### Likely Targets

* `src/core/src/zava_forward/core/regulatory_chat.py`: Add `_refusal` helper combining `consent_guidance(self.iso.ai_consent_state(cid))`, `self.refuse(question)`, and fallback `REFUSED + out_of_scope(question)[1]`, plus AI-consent withdrawal guard in `doubt`.
* `src/core/src/zava_forward/core/ai_eval.py`: Pure-`core` multi-turn `ChatPanel` + `RegulatoryChat` scenario harness, held-out expected-outcome + 6-binding freeze validator, and separate chat multi-turn vs single-turn evaluation report builder.

### Dependencies

* None.

### Validation Expectations

* `DependencyRuleTests` in `src/core/tests/test_dependency_rule.py` passes with zero non-`core` imports.
* `mypy` and `ruff` pass on `src/core/src/zava_forward/core/regulatory_chat.py` and `src/core/src/zava_forward/core/ai_eval.py`.

### Completion Evidence

* `RegulatoryChat` blocks withdrawn/non-`Given` recorded `ai_data_use_consent` across `bundle`, `foundry_query`, and `doubt`, and refuses `approve`/`decide`/`consent`/`diagnose`/`contact` requests with human workflow routes even when `self.refuse` returns `None`.
* `zava_forward.core.ai_eval.run_eval()` executes all deterministic multi-turn revocation, grounding, ambiguity, abstention, and refusal/non-manufacture scenarios cleanly with `enablement["state"] == "disabled"`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Harden `RegulatoryChat` mid-thread AI-consent revocation and fallback `out_of_scope` routing

#### Context

In `RegulatoryChat` (`C7`, `C16`, `C17`), `ChatIsolation.ai_consent_state(cid)` returns `None` when `ai_data_use_consent` is unset on a case (`C6`), so checking `consent_guidance(self.iso.ai_consent_state(cid))` preserves every legacy test fixture while failing closed when resident AI/data-use consent is `"Withdrawn"`, `"Declined"`, `"Pending"`, or `"Not requested"`. Checking `self.refuse(question)` before falling back to `REFUSED + out_of_scope(question)[1]` preserves `REASONS["legal"]` in `agents/tests/regulatory_gate_fixture.py` (`C17`) while ensuring `core.regulatory_chat` never answers out-of-scope action requests when `self.refuse` is permissive (`C16`).

#### Intent

Ensure `RegulatoryChat` clears prior-turn authority on mid-thread AI-consent withdrawal and preserves `out_of_scope` refusal + human workflow routes at the core boundary.

#### Boundaries

* Included: Pre-`detail` `_question_refusal(self, question: str) -> str | None` (`self.refuse(question)` first, fallback `REFUSED + out_of_scope(question)[1]`), post-`detail` `consent_guidance(self.iso.ai_consent_state(cid))` in `bundle` and `foundry_query`, transactional `ai_consent_state` re-check inside `ask()`'s `repo.txn()`, and `consent_guidance` `ChatForbidden` guard in `doubt` (pre-lock and inside `repo.txn()`).
* Excluded: Changing `agents.regulatory_chat.refusal` string constants expected by `regulatory_gate_fixture.py`.

#### Likely Targets

* `src/core/src/zava_forward/core/regulatory_chat.py`: Import `REFUSED`, `consent_guidance`, `out_of_scope` from `zava_forward.core.chat_panel`; wire `_refusal` and `doubt` consent check.

#### Dependencies

* None.

#### Validation Expectations

* Existing `test_regulatory_chat.py` and `agents/tests/test_regulatory_gates.py` pass unchanged, and new mid-thread AI-consent revocation + `out_of_scope` fallback tests pass.

#### Completion Evidence

* `bundle` and `foundry_query` return refusal/unpermitted payloads with manual consent or workflow routes when AI consent is revoked mid-thread or an out-of-scope action is asked; `doubt` raises `ChatForbidden` when AI consent is revoked after Turn 1.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Create pure-`core` `src/core/src/zava_forward/core/ai_eval.py`

#### Context

`src/core` needs `zava_forward.core.ai_eval` (`C2`) without importing `zava_forward.agents` (`C1`). All underlying chat, isolation, regulatory, lawstore, rulecard, and registry primitives live in `zava_forward.core` (`C3`–`C8`).

#### Intent

Deliver a self-contained, pure-`core` evaluation and verification module covering multi-turn `ChatPanel` and `RegulatoryChat` revocation/grounding/ambiguity/refusal scenarios, version-bound held-out freeze checks (including frozen per-turn expected outcomes), 4-part review-effort reporting, separate multi-turn vs single-turn reporting, and `disabled` enablement gating.

#### Boundaries

* Included:
  * `REQUIRED_BINDINGS = ("task", "model", "prompt_version", "policy_version", "source_version", "memory_version")`, `bindings(raw)`, `expected_outcomes_digest(spec)`, `expected_outcome_problems(spec)`, `leaks(heldout, development)`, `freeze_problems(...)`, and `run_heldout(...)`.
  * Deterministic `ScriptedChatModel`, multi-turn `ChatPanel` runner (supporting `set`, `revoke_source`, `set_ai_consent`, `set_role`, `remove_staff`, `remove_case`, `remember`), and multi-turn `RegulatoryChat` runner (supporting `hold_card`, `retire_card`, `supersede_source`, `add_conflicting_card`, `set_ai_consent`, `set_role`) with built-in `CORE_SCENARIOS` proving Criteria 1 and 2.
  * `REVIEW_EFFORT_INPUTS`, `review_effort(observations)`, `chat_specific(results)`, `enablement_decision(report, thresholds=None, heldout=None)` (rejecting missing/blank/system/agent `approved_by` and always keeping `state="disabled"` while live evidence gates remain unmet), `separate_evaluation_report(single_turn_report, chat_report)`, and `run_eval(spec=None)`.
* Excluded: Network calls, provider SDKs, `agents`/`api` imports, or live task activation.

#### Likely Targets

* `src/core/src/zava_forward/core/ai_eval.py`: New pure-`core` module.

#### Dependencies

* P01-T01 (`RegulatoryChat` consent/refusal hardening).

#### Validation Expectations

* `python3 -m unittest discover -s tests -p "test_*ai_eval*.py" -q` and `test_dependency_rule.py` in `src/core` pass; `mypy` passes with strict typing.

#### Completion Evidence

* `zava_forward.core.ai_eval.run_eval()` passes all deterministic multi-turn scenarios with zero open critical gaps and `enablement["state"] == "disabled"`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Agents Multi-Turn Golden Coverage and Held-Out Expected-Outcome Freeze

### Context

`agents.chat_eval` and `evals/chat_golden.json` lacked mid-thread source-field deletion, mid-thread `ai_data_use_consent` revocation, and explicit multi-turn ambiguity abstention scenarios (`C9`, `C12`), while `agents.chat_heldout.freeze_problems` did not verify per-turn frozen expected outcomes (`C10`, `C11`).

### Intent

Align `agents.chat_eval`, `evals/chat_golden.json`, and `agents.chat_heldout` with the hardened `core.ai_eval` expected-outcome freeze and multi-turn revocation/ambiguity contracts.

### Boundaries

* Included: `src/agents/src/zava_forward/agents/chat_eval.py`, `src/agents/evals/chat_golden.json`, `src/agents/src/zava_forward/agents/chat_heldout.py`.
* Excluded: Breaking existing `test_chat_eval.py`, `test_chat_eval_revocation_effort.py`, `test_chat_heldout.py`, or `test_epic104_bounded_ai_invariants.py` contracts.

### Likely Targets

* `src/agents/src/zava_forward/agents/chat_eval.py`: Add `revoke_source` (clearing optional/nested scalar fields to `""` without popping required `Store.detail()` keys) and `set_ai_consent` (setting `resident.ai_data_use_consent`) to `Run.apply`; union `chat_panel.WORKFLOW_RULES` in `_comparison` so `workflow/ai-consent-boundary` citations count as card/workflow-answerable; include `permission-source-and-ai-consent-revoked-mid-thread` in `REVOCATION_SCENARIOS` while keeping `memory-poisoning` scenario count at 5.
* `src/agents/evals/chat_golden.json`: Add `permission-source-and-ai-consent-revoked-mid-thread` and `grounding-ambiguous-request-abstains-without-guessing`.
* `src/agents/src/zava_forward/agents/chat_heldout.py`: Delegate/enforce per-turn frozen expected-outcome checks (`expected_outcome_problems` and optional `expected_outcomes_sha256` from `zava_forward.core.ai_eval`) in `freeze_problems`, and include `chat_specific`, `review_effort`, and `enablement` (`state="disabled"`) in `run_heldout`.

### Dependencies

* P01.

### Validation Expectations

* All existing and new `test_chat_*.py` and `test_epic104_bounded_ai_invariants.py` suites in `src/agents` pass.

### Completion Evidence

* `chat_heldout.run_heldout` blocks any held-out scenario missing frozen per-turn expected outcomes before execution and reports `chat_specific`, `review_effort`, and `enablement["state"] == "disabled"` when scored.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Extend `agents.chat_eval`, `evals/chat_golden.json`, and `agents.chat_heldout`

#### Context

See P02 context (`C9`–`C12`).

#### Intent

Ensure `agents` golden and held-out harnesses exercise mid-thread source-field/AI-consent revocation, ambiguity abstention, frozen expected outcomes, and separate chat reporting.

#### Boundaries

* Included: `Run._apply` ops (`revoke_source`, `set_ai_consent`), 2 multi-turn scenarios in `chat_golden.json`, expected-outcome freeze validation and separate reporting fields in `chat_heldout.py`.
* Excluded: Modifying single-turn `agents.ai_eval` metrics.

#### Likely Targets

* `src/agents/src/zava_forward/agents/chat_eval.py`
* `src/agents/evals/chat_golden.json`
* `src/agents/src/zava_forward/agents/chat_heldout.py`

#### Dependencies

* P01-T02.

#### Validation Expectations

* `python3 -m unittest discover -s tests -p "test_chat_*.py" -q` in `src/agents` passes.

#### Completion Evidence

* Golden evaluation passes with the expanded multi-turn revocation and ambiguity scenarios, and `chat_heldout` rejects vacuous/unfrozen `expect` dicts.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Separate Chat Multi-Turn Reporting in `/api/ai/report`

### Context

`/api/ai/report` in `src/api/src/zava_forward/api/server.py` currently returns `evaluation: ai_eval.run_eval()` (single-turn task evaluation only, where `chat-case-conversation` is marked unevaluated) without a separate multi-turn chat evaluation sibling (`C13`, `C15`).

### Intent

Expose multi-turn `chat_evaluation` as a distinct sibling key on `/api/ai/report` so chat-specific failures, complete review effort, and `disabled` enablement status are reported separately from single-turn task results.

### Boundaries

* Included: `src/api/src/zava_forward/api/server.py` `/api/ai/report` response dict.
* Excluded: Merging multi-turn chat counts or pass flags into single-turn `evaluation`, or changing manager-only RBAC (`MANAGER_ROLES`) on `/api/ai/report`.

### Likely Targets

* `src/api/src/zava_forward/api/server.py`: Import `chat_eval` from `zava_forward.agents` alongside `ai_eval` in `/api/ai/report` and include `"chat_evaluation": chat_eval.run_eval()` as a separate top-level field.

### Dependencies

* P01, P02.

### Validation Expectations

* `Endpoints.test_report_is_manager_only` and new separate-reporting tests in `src/api/tests/test_ai_tasks.py` pass.

### Completion Evidence

* `/api/ai/report` returns both `"evaluation"` (single-turn) and `"chat_evaluation"` (multi-turn conversation with `chat_specific`, `review_effort`, and `enablement.state == "disabled"`), keeping their denominators and failure structures separate.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add separate `chat_evaluation` sibling to `/api/ai/report` in `src/api/src/zava_forward/api/server.py`

#### Context

See P03 context (`C13`, `C14`, `C15`).

#### Intent

Deliver API-level separate multi-turn vs single-turn evaluation reporting without altering single-turn `evaluation` consumers.

#### Boundaries

* Included: `/api/ai/report` handler in `src/api/src/zava_forward/api/server.py`.
* Excluded: Non-report HTTP endpoints.

#### Likely Targets

* `src/api/src/zava_forward/api/server.py`

#### Dependencies

* P02-T01.

#### Validation Expectations

* `cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_ai_tasks.py" -q` passes.

#### Completion Evidence

* HTTP `GET /api/ai/report` as manager returns `200` with distinct `evaluation` and `chat_evaluation` payloads and `chat_evaluation["enablement"]["state"] == "disabled"`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P04 -->
## P04: Deterministic Regression Suites and Focused Validation

### Context

Every claim in Scope items 1, 2, and 3 must be backed by deterministic unit tests that fail if the underlying runtime or evaluation guard is weakened, and must pass the caller's focused validation commands (`C1`, `C2`, `C11`, `C14`).

### Intent

Author focused, high-signal regression tests in `src/core/tests/test_ai_eval.py`, `src/core/tests/test_regulatory_chat.py`, `src/agents/tests/test_chat_heldout.py`, and `src/api/tests/test_ai_tasks.py`, and execute all focused checks (`unittest`, `mypy`, `ruff`).

### Boundaries

* Included: `src/core/tests/test_ai_eval.py`, `src/core/tests/test_regulatory_chat.py`, `src/agents/tests/test_chat_heldout.py`, `src/api/tests/test_ai_tasks.py`.
* Excluded: `tools/rpi-checks.py --all` (explicitly prohibited by caller prompt).

### Likely Targets

* `src/core/tests/test_ai_eval.py` (new)
* `src/core/tests/test_regulatory_chat.py`
* `src/agents/tests/test_chat_heldout.py`
* `src/api/tests/test_ai_tasks.py`

### Dependencies

* P01, P02, P03.

### Validation Expectations

* `cd src/core && python3 -m unittest discover -s tests -p "test_*ai_eval*.py" -q`
* `cd src/core && python3 -m unittest discover -s tests -p "test_regulatory_chat.py" -q && python3 -m unittest discover -s tests -p "test_chat_panel.py" -q && python3 -m unittest discover -s tests -p "test_dependency_rule.py" -q`
* `cd src/agents && PYTHONPATH=../core/tests python3 -m unittest discover -s tests -p "test_chat_*.py" -q && PYTHONPATH=../core/tests python3 -m unittest discover -s tests -p "test_regulatory_gates.py" -q`
* `cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_ai_tasks.py" -q`
* `cd src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .`
* `cd src/agents && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .`
* `cd src/api && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .`

### Completion Evidence

* Zero failures across all targeted unit suites, `mypy`, and `ruff`.

### Unresolved Items

* None.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Create `src/core/tests/test_ai_eval.py` and extend `src/core/tests/test_regulatory_chat.py`

#### Context

`src/core/tests/test_ai_eval.py` is directly selected by `python3 -m unittest discover -s tests -p "test_*ai_eval*.py" -q` in `src/core` (`C2`).

#### Intent

Prove Criteria 1, 2, and 3 deterministically in `src/core`, including failure-injection proofs showing each gate fails closed when a revocation, refusal, expected-outcome freeze, version binding, or owner-approval check is violated.

#### Boundaries

* Included: `src/core/tests/test_ai_eval.py` and targeted additions to `src/core/tests/test_regulatory_chat.py`.
* Excluded: Non-`core` imports (`ALLOWED = {"core"}`).

#### Likely Targets

* `src/core/tests/test_ai_eval.py`
* `src/core/tests/test_regulatory_chat.py`

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* `python3 -m unittest discover -s tests -p "test_*ai_eval*.py" -q`, `test_regulatory_chat.py`, and `test_dependency_rule.py` in `src/core` exit `0`.

#### Completion Evidence

* Unit tests pass and cover mid-thread permission/source/card/consent revocation, unsupported claims with valid citations, stale/conflicting sources, ambiguity, abstention, multi-turn `approve`/`decide`/`consent`/`diagnose`/`contact` refusal routes, memory/history non-manufacture, frozen held-out expected outcomes & 6 bindings, separate reporting, 4-part review effort, and `disabled` live enablement.

#### Unresolved Items

* None.

<!-- rpi:task id=P04-T02 -->
### P04-T02: Extend `src/agents/tests/test_chat_heldout.py` and `src/api/tests/test_ai_tasks.py` and run focused checks

#### Context

`test_chat_heldout.py` and `test_ai_tasks.py` validate the held-out gate in `agents` and `/api/ai/report` in `api` (`C11`, `C13`, `C14`).

#### Intent

Verify held-out expected-outcome freeze and separate `chat_evaluation` HTTP reporting end-to-end, then run all focused tier checks (`unittest`, `mypy`, `ruff`).

#### Boundaries

* Included: `src/agents/tests/test_chat_heldout.py`, `src/api/tests/test_ai_tasks.py`, and focused validation commands.
* Excluded: `tools/rpi-checks.py --all`.

#### Likely Targets

* `src/agents/tests/test_chat_heldout.py`
* `src/api/tests/test_ai_tasks.py`

#### Dependencies

* P02-T01, P03-T01, P04-T01.

#### Validation Expectations

* All focused `unittest`, `mypy`, `ruff check .`, and `ruff format --check .` runs exit `0`.

#### Completion Evidence

* Recorded command exit statuses in `.copilot-tracking/changes/2026-11-15/issue-164-chat-eval-revocation-changes.md`.

#### Unresolved Items

* None.
