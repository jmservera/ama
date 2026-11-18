<!-- markdownlint-disable-file -->
# Review: Regulatory Non-Advice, Duty-Satisfaction, and Future-Law Output Guard (#208)

## Scope and Evidence

* Task ID: issue-208-non-advice-guard
* Review date: 2026-11-15
* Review scope: full task (`P01`, `P02`, `P03`)
* Assessed boundary: Issue `#208` acceptance criterion `- [ ] No output states that a duty is satisfied, gives legal advice or applies future law as active` across `src/core/`, `src/agents/`, and `src/api/`, workbench/watch telemetry exposure, unit and HTTP integration proofs, and focused-tier validation.
* Plan: .copilot-tracking/plans/2026-11-15/reg-208-non-advice-guard-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/reg-208-non-advice-guard-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/reg-208-non-advice-guard-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/reg-208-non-advice-guard-research.md, `git diff` across `src/core`, `src/agents`, and `src/api`, and focused validation runs (`ruff check`, `ruff format --check`, `mypy`, `unittest`, `node --check`, `tools/rename-zava-tests.py`).

## Opening Review State

* Interpreted review goal: Verify once, with read-only source authority, that the completed `P01`–`P03` implementation deterministically prevents duty-satisfaction verdicts, legal advice, and unactivated/consultative/future-law operational rules across regulatory watch summaries, assistant responses, and legal/compliance views, exposes shared telemetry, preserves existing schemas/evals, and passes focused validation.
* Review scope: full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; research, plan, phase details, single-pass plan critique (`PC-001`–`PC-004`), and changes record are complete and reconciled.
* Acceptance basis: Issue `#208` non-advice/future-law acceptance criteria, synthesized functional/non-functional requirements (`FR-1`..`FR-6`, `NFR-1`..`NFR-4`), acceptance criteria (`AC-1`..`AC-7`), and resolved plan critique findings (`PC-001`..`PC-004`).
* First comparison boundary: Compare `P01`, `P02`, and `P03` plan/detail targets and critique dispositions against actual `src/core`, `src/agents`, and `src/api` changes and test proofs.
* Active read-only boundaries: Write only `.copilot-tracking/reviews/logs/2026-11-15/reg-208-non-advice-guard-review.md` within `rpi-review`; do not mutate source code, research, plan, details, critique, or changes records during review.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Assessed 2026-11-15 across all three phases (`P01`, `P02`, `P03`), nine tasks (`P01-T01`..`P03-T03`), four critique dispositions (`PC-001`..`PC-004`), three implementation-time detail alignments, and full focused-tier validation logs.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`, `P01-T03`) | Core Guard, Watch Summary, and Unit Proofs | Reconciled | All planned core modules (`regulatory_output_guard.py`, `lawstore.py`, `rule_engine.py`, `source_monitor.py`) and `test_regulatory_output_guard.py` match plan and detail markers. |
| `P02` (`P02-T01`, `P02-T02`, `P02-T03`) | Agents and Core Assistant Output Guard Enforcement | Reconciled | `agents/regulatory_chat.py`, `core/regulatory_chat.py`, `core/chat_panel.py`, `core/assistants.py`, and `test_regulatory_non_advice_guard.py` match plan and `PC-001`/`PC-002`/`PC-004` dispositions. |
| `P03` (`P03-T01`, `P03-T02`, `P03-T03`) | API Regulatory Watch, Legal/Compliance View Enforcement, Telemetry, and Validation | Reconciled | `plain_language.py`, `server.py`, `test_role_endpoint_inventory.py`, `test_regulatory_watch_guard_api.py`, and focused validation table match plan markers and recorded current-state alignments. |
| `Follow-Up Items` | Optional interactive regulatory watch UI tab in `src/api/src/zava_forward/api/web/law.js` | Reconciled | Preserved outside active `Pxx` scope in both plan and changes record. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01` (`P01-T01`, `P01-T02`, `P01-T03`) | `src/core/src/zava_forward/core/regulatory_output_guard.py`, `src/core/src/zava_forward/core/lawstore.py`, `src/core/src/zava_forward/core/rule_engine.py`, `src/core/src/zava_forward/core/source_monitor.py`, `src/core/tests/test_regulatory_output_guard.py` | Added zero-model deterministic guard (`duty_satisfied`, `legal_advice`, `future_law_applied_as_active`), NFKC/`Cf`/homoglyph normalization, pre-span vs in-span clause negation, `GuardTelemetry`, `"future_phase"` source lifecycle, and guarded `SourceMonitor.watch_summary`. | Unit tests verify all 4 `#208` scenarios, evasion resistance, disclaimer safety, and `watch_summary` telemetry. | `ruff check`, `ruff format --check`, strict `mypy` (355 files), and `test_regulatory_output_guard` + core suites passed. | Reconciled and conformant |
| `P02` (`P02-T01`, `P02-T02`, `P02-T03`) | `src/agents/src/zava_forward/agents/regulatory_chat.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/src/zava_forward/core/chat_panel.py`, `src/core/src/zava_forward/core/assistants.py`, `src/agents/tests/test_regulatory_non_advice_guard.py` | Enforced active source + human-approved card preconditions in `agents/regulatory_chat.answer`, single-gate telemetry and section sanitization in `RegulatoryChat.ask`/`surface`, and `on_violation="reject"` withholding in `ChatPanel` and `Assistants`. | Frozen evals (`evals/regulatory_chat_results.json`) remain untouched and green; unsafe turns/proposals are rewritten or rejected. | `ruff check`, `ruff format --check`, strict `mypy` (67 files), and all 536 `src/agents` tests passed. | Reconciled and conformant |
| `P03` (`P03-T01`, `P03-T02`, `P03-T03`) | `src/api/src/zava_forward/api/plain_language.py`, `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_role_endpoint_inventory.py`, `src/api/tests/test_regulatory_watch_guard_api.py` | Added `GET /api/law/watch`, guarded `/api/law/*` JSON/CSV serializers and `plain_language.apply` without clobbering upstream failures, wired shared `App.guard_telemetry` across status/me payloads, registered `/api/law/watch` in role inventory, and added loopback HTTP proofs. | All 6 end-to-end HTTP test methods in `test_regulatory_watch_guard_api.py` and full role-matrix inventory passed. | `ruff check`, `ruff format --check`, `mypy` (298 files), `src/api` suites, `node --check`, and `rename-zava-tests.py` passed. | Reconciled and conformant |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P03-T01` (`GET /api/me` telemetry placement) | Placed `regulatory_output_guard` at top level of `/api/me` (role-gated by `projection.allowed(u, "law")`) instead of adding `"regulatory_watch"` inside `me["services"]`. | `src/api/tests/test_expected_denials.py` asserts exact 4-key equality on `me["services"]`; no user decision needed (preserves approved telemetry intent and existing API contract). | Updated `P03-T01` in `.copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md` and `## Implementation-Time Plan and Detail Updates` in `changes.md`. | Not needed (immediately relevant current-state update preserving `FR-5` and `AC-6`). | Reconciled |
| `P03-T01` (`_guard_rulecard_dict` envelope vs item schema) | Returned `(guarded_card, status)` from `_guard_rulecard_dict` so card fields are sanitized while `output_guard` lives on the `/api/law/cards*` envelope rather than inside each card dict. | `src/api/tests/test_auth.py` (`RuleHttpTests.test_running_local_app_full_lifecycle_and_retained_versions`) compares card dicts directly to `law.rules.history(...)`; no user decision needed. | Updated `P03-T01` in `phase-details.md` and `changes.md`, and verified `test_auth.RuleHttpTests` + `test_regulatory_watch_guard_api` pass. | Not needed (`PC-003` and `PC-004` remain satisfied). | Reconciled |
| `P02-T02` (`Assistants.complete` positional signature) | Kept `Assistants.complete(self, task, envelope, output, failure=None)` positional signature unchanged and deduplicated telemetry via `threading.local()`. | `src/api/tests/test_assistants.py` (`DurabilityTests.test_uncertain_claim_and_completion_ack_lookup_not_reinference`) wraps `complete` with `def lost_complete(*args):`; no user decision needed. | Recorded in `changes.md` and verified `test_assistants.DurabilityTests` + `test_regulatory_watch_guard_api` pass. | Not needed (`PC-004` `rejected_total` telemetry remains satisfied). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four single-pass plan critique findings (`PC-001` post-rewrite clobbering/double-counting/section sanitization, `PC-002` `refusal`/`conflict`/`unknown` eval-branch ordering, `PC-003` boolean `active_operational_rule` precedence vs clause-scoped negation, and `PC-004` `/api/law/sources.csv`, `_rule_alerts`, and `rejected_total` wiring) were resolved before implementation and verified in code and HTTP tests.
* Material revisions: None occurred during implementation; all three implementation-time discoveries were backwards-compatible schema/signature alignments preserving approved requirements.
* Dependent-work pause assessment: No dependent-work pause was needed because no significant or divergent decision arose.
* Justification assessment: Fully supported by unit and HTTP integration test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Optional interactive regulatory watch UI tab in `src/api/src/zava_forward/api/web/law.js` | Issue `#208` scopes deterministic non-advice/future-law output guarding and watch/workbench API telemetry rather than a new browser tab redesign. | Future UX / Compliance workbench issue owner if visual diff browsing is requested. | Open distinct follow-up; excluded from active `Pxx` scope as planned. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Explicit-path `ruff format` reformatted four `pyproject.toml`-excluded legacy modules (Resolved in Follow-Up)

* Related scope: `P03-T03`
* Evidence: `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_role_endpoint_inventory.py`, `src/core/src/zava_forward/core/lawstore.py`, and `src/core/src/zava_forward/core/assistants.py` are listed in `[tool.ruff.format].exclude` in `src/api/pyproject.toml` and `src/core/pyproject.toml`, and passing explicit file paths to `ruff format` initially formatted untouched lines alongside the `#208` edits.
* Impact: Non-functional diff-size expansion that increased merge-conflict surface when rebasing across long-lived branches.
* Destination: follow-up (selected and resolved)
* Resolution evidence: Restored the original unformatted baseline on untouched lines of all four `[tool.ruff.format].exclude` files (`ast.dump` verified identical), rebased `feat/reg-208-non-advice-guard` cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`04e5da42e1ae0b172245a4ca85ff4d2b6232a8f2`), and passed directory-mode `ruff check .`, `ruff format --check .`, `mypy` (`src/core` 363 files, `src/agents` 67 files, `src/api` 301 files), `test_regulatory_output_guard`, `test_regulatory_non_advice_guard`, `test_regulatory_watch_guard_api`, `test_role_endpoint_inventory`, and `tools/rename-zava-tests.py`.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | follow-up (resolved) | Completed on rebased `feat/reg-208-non-advice-guard` onto `04e5da42e1ae0b172245a4ca85ff4d2b6232a8f2` | Restored untouched lines on `[tool.ruff.format].exclude` modules and verified directory-mode CI parity. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Plan follow-up: Optional interactive regulatory watch UI panel in `src/api/src/zava_forward/api/web/law.js` consuming `GET /api/law/watch`.

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy` | `src/core` (355 source files) | Passed | `All checks passed!`, `302 files already formatted`, `Success: no issues found in 355 source files`. |
| `python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=../core/src python3 -m mypy` | `src/agents` (67 source files) | Passed | `All checks passed!`, `63 files already formatted`, `Success: no issues found in 67 source files`. |
| `python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=../core/src:../agents/src python3 -m mypy` | `src/api` (298 source files) | Passed | `All checks passed!`, `214 files already formatted`, `Success: no issues found in 298 source files`. |
| `src/core` unit tests (`test_regulatory_output_guard`, `test_source_monitor`, `test_rule_engine`, `test_regulatory_chat`, `test_regulatory_eval_gates_216`, `test_regulatory_privacy_audit_217`, `test_dependency_rule`, plus subprocess suites) | `src/core/tests` | Passed | 134 targeted regulatory/core tests + 45 subprocess bundle/demo/fabric tests passed (`OK`); 3,579/3,579 non-Azure-SDK core tests passed (`test_device_registry_azure.py` skipped/unavailable without optional `azure-iot-hub` extra in host Python). |
| `PYTHONPATH=../core/tests python -m unittest discover -s tests -q` | `src/agents/tests` | Passed | `Ran 536 tests in 151.076s — OK` (100% pass including `test_regulatory_non_advice_guard.py` and frozen `evals/regulatory_chat_results.json`). |
| `src/api` unit & HTTP integration tests (`test_regulatory_watch_guard_api`, `test_lawstore`, `test_rule_alerts`, `test_regulatory_chat_api`, `test_expected_denials`, `test_role_endpoint_inventory`, `test_auth.RuleHttpTests`, `test_assistants.DurabilityTests` + full `discover`) | `src/api/tests` | Passed | All 6 HTTP integration tests in `test_regulatory_watch_guard_api.py` and 117 combined regulatory/auth/durability/inventory tests passed (`OK`); full 3,774-test discovery verified zero remaining regressions. |
| `for f in src/api/src/zava_forward/api/web/*.js; do node --check "$f"; done` | `src/api/src/zava_forward/api/web/*.js` | Passed | `node --check OK` across all workbench JS modules. |
| `python3 tools/rename-zava-tests.py` | Repository root migration check | Passed | `Ran 25 tests in 0.526s — OK`. |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every Issue `#208` acceptance criterion and caller requirement is deterministically enforced and proven by automated unit, agent, and loopback HTTP integration tests across `src/core`, `src/agents`, and `src/api`, with shared telemetry exposed in watch/status/workbench payloads, zero frozen-eval or contract regressions, and zero defects.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up (optional `web/law.js` watch UI tab; `RV-001` resolved on rebase onto `04e5da42e1ae0b172245a4ca85ff4d2b6232a8f2`) | Future UX issue owner |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Passed across `src/core`, `src/agents`, `src/api` (`ruff check`, `ruff format --check`, `mypy`, unit and HTTP integration suites), `node --check`, and `tools/rename-zava-tests.py`
* Blockers: none
