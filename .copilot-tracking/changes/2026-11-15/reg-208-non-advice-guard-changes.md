<!-- markdownlint-disable-file -->
# RPI Changes: Regulatory Non-Advice, Duty-Satisfaction, and Future-Law Output Guard (#208)

## Metadata

* Task ID: issue-208-non-advice-guard
* Related plan: .copilot-tracking/plans/2026-11-15/reg-208-non-advice-guard-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01` (`P01-T01`, `P01-T02`, `P01-T03`), `P02` (`P02-T01`, `P02-T02`, `P02-T03`), `P03` (`P03-T01`, `P03-T02`, `P03-T03`)
* All remaining active-plan markers: none
* Status basis: Completed all three phases (`P01`, `P02`, `P03`) across `src/core`, `src/agents`, and `src/api` with focused validation (`ruff check`, `ruff format --check`, `mypy`, unit and HTTP integration tests, `node --check`, and `tools/rename-zava-tests.py`) passing cleanly.

## Execution Summary

Implemented the canonical deterministic regulatory output guard (`zava_forward.core.regulatory_output_guard`), `"future_phase"` lifecycle support in `LawStore` and `RuleEngine`, and guarded `SourceMonitor.watch_summary` (`P01`); wired enforcement across `agents/regulatory_chat.py`, `core/regulatory_chat.py`, `core/chat_panel.py`, and `core/assistants.py` (`P02`); exposed `GET /api/law/watch`, guarded all `/api/law/*` JSON/CSV serializers and `plain_language.apply`, exposed shared `GuardTelemetry` across `/api/law/watch`, `/api/chat/regulatory/status`, `/api/chat/status`, and staff `/api/me`, registered `/api/law/watch` in `test_role_endpoint_inventory.py`, added end-to-end HTTP proofs in `test_regulatory_watch_guard_api.py`, and passed focused validation across `src/core`, `src/agents`, `src/api`, and `tools/rename-zava-tests.py` (`P03`).

## Completed Work

### Core Guard, Watch Summary, and Unit Proofs (`P01`, `P01-T01`, `P01-T02`, `P01-T03`)

* Created `src/core/src/zava_forward/core/regulatory_output_guard.py` implementing deterministic zero-model inspection (`duty_satisfied_claim`, `legal_advice_given`, `future_law_applied_as_active`), Unicode NFKC/`Cf`/homoglyph normalization, clause-scoped negation distinguishing pre-span (`without`, `whether`, `if`) from in-span negation so `"applies as an active rule without human rule activation"` still fails while negated caveats pass, compact `GuardDecision.to_status_dict()`, `advisory_review_summary()`, and thread-safe `GuardTelemetry`.
* Updated `src/core/src/zava_forward/core/lawstore.py`, `src/core/src/zava_forward/core/rule_engine.py`, and `src/core/src/zava_forward/core/source_monitor.py` to support `"future_phase"` and `SourceMonitor.watch_summary(...)`.
* Created `src/core/tests/test_regulatory_output_guard.py` verifying all four Issue `#208` scenarios, homoglyph/disclaimer-stuffing evasion resistance, canonical refusal compatibility, `"future_phase"` citation ineligibility, and guarded `watch_summary` payloads.

### Agents and Core Assistant Output Guard Enforcement (`P02`, `P02-T01`, `P02-T02`, `P02-T03`)

* Updated `src/agents/src/zava_forward/agents/regulatory_chat.py` (`P02-T01`) to require both active commenced source status and at least one active/approved rule card before emitting `kind == "answer"`, demoting consultative, future-phase, future-dated, or unactivated answers to `kind == "unknown"` with explicit review-item reason, validating all non-quote prose across `reply` and `sections`, and attaching compact `output_guard`.
* Updated `src/core/src/zava_forward/core/regulatory_chat.py` (`P02-T01`) to act as the single telemetry-recording gate in `RegulatoryChat.ask` and `RegulatoryChat.surface` without double-counting or clobbering upstream `output_guard.passed=False` (`PC-001`), stripping exact verbatim quoted source/fact spans before guarding rendered `reply` and non-quote `sections` (`PC-002`).
* Updated `src/core/src/zava_forward/core/chat_panel.py` and `src/core/src/zava_forward/core/assistants.py` (`P02-T02`) to run `on_violation="reject"`, withholding unsafe replies/proposals and incrementing `rejected_total` in `guard_telemetry` (`PC-004`).
* Created `src/agents/tests/test_regulatory_non_advice_guard.py` and extended `src/core/tests/test_regulatory_output_guard.py` (`P02-T03`), proving legitimate cited answers pass cleanly (`test_regulatory_answers` and `test_regulatory_eval_gates_216` remain 100% green), consultative/future/unactivated answers demote to `unknown`, and unsafe duty-satisfied/legal-advice prose is rewritten/rejected.

### API Regulatory Watch, Legal/Compliance View Enforcement, Telemetry, and Validation (`P03`, `P03-T01`, `P03-T02`, `P03-T03`)

* Updated `src/api/src/zava_forward/api/plain_language.py` (`P03-T01`) to guard `plain_summary` via `guard_regulatory_text` and merge guard status through `merge_guard_statuses` without clobbering upstream `output_guard.passed=False` (`PC-001`).
* Updated `src/api/src/zava_forward/api/server.py` (`P03-T01`) to initialize shared `App.guard_telemetry = GuardTelemetry()` across `Assistants`, `ChatPanel`, `RegulatoryChat`, and `/api/law/*` handlers; serve `GET /api/law/watch` (with optional `?as_of=YYYY-MM-DD`, role-gated by `projection.allowed(user, "law")`, returning `503` when `law` is unloaded); enforce deterministic guarding across `/api/law/sources`, `/api/law/sources.csv`, `/api/law/sources/{id}`, `/api/law/provisions/{id}`, `/api/law/search`, `_rulecards` (`/api/law/cards*`, preserving exact per-card key parity while emitting merged `output_guard` on the envelope), and `_rule_alerts` (`/api/law/alerts*` and `/api/law/checks/*`); and expose shared guard telemetry on `/api/law/watch`, `/api/chat/regulatory/status`, `/api/chat/status`, and top-level `regulatory_output_guard` on `/api/me` for staff roles allowed `"law"`.
* Updated `src/api/tests/test_role_endpoint_inventory.py` (`P03-T02`) to include `"/api/law/watch"` in `GET_ENDPOINTS`, and created `src/api/tests/test_regulatory_watch_guard_api.py` (`P03-T02`) proving over loopback HTTP all four Issue `#208` acceptance scenarios (`duty_satisfied`, `legal_advice`, `future_law_applied_as_active`, and clean cited summaries), JSON/CSV parity, draft-vs-misactivated rule cards, `plain_language=True` violation preservation, and unified telemetry counters including `rejected_total`.
* Executed full focused validation (`P03-T03`) across `src/core`, `src/agents`, `src/api`, `web/*.js`, and `tools/rename-zava-tests.py`.

### Post-Review Follow-Up: Diff-Churn Minimization and Rebase (`RV-001`)

* Restored the original unformatted baseline on untouched lines of the four `[tool.ruff.format].exclude` files (`src/api/src/zava_forward/api/server.py`, `src/api/tests/test_role_endpoint_inventory.py`, `src/core/src/zava_forward/core/lawstore.py`, and `src/core/src/zava_forward/core/assistants.py`), preserving only semantic `#208` additions (`ast.dump` verified identical) and eliminating ~2,300 lines of unrelated formatting churn.
* Rebased `feat/reg-208-non-advice-guard` cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`04e5da42e1ae0b172245a4ca85ff4d2b6232a8f2`) with zero conflicts.
* Re-verified directory-mode `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `mypy` across `src/core` (363 files), `src/agents` (67 files), and `src/api` (301 files), plus `test_regulatory_output_guard`, `test_regulatory_non_advice_guard`, `test_regulatory_watch_guard_api`, `test_role_endpoint_inventory`, and `tools/rename-zava-tests.py`.

## Implementation-Time Plan and Detail Updates

* Immediately relevant current-state updates (`P03-T01` in `.copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md` and `P02-T02` in `assistants.py`):
  * `GET /api/me` exposes `regulatory_output_guard` at top level (gated by `projection.allowed(u, "law")`) without adding keys to `me["services"]`, preserving `test_expected_denials.py`'s exact 4-key `me["services"]` assertion.
  * `_guard_rulecard_dict` sanitizes card fields in place and returns `(card, guard_status)` so `_rulecards` emits merged `output_guard` on the `/api/law/cards*` response envelope without adding extra keys onto individual card dicts, preserving `test_auth.py`'s `law.rules.history(...)` comparison.
  * `Assistants.complete` retains its exact 4-argument positional signature `(self, task, envelope, output, failure=None)` and deduplicates telemetry via `threading.local()` when called from `Assistants.execute`, preserving `test_assistants.py` positional `lost_complete(*args)` wrappers.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `ruff check .` + `ruff format --check .` + `mypy` | `src/core` (355 files), `src/agents` (67 files), `src/api` (298 files) | Passed | Exit 0 across all three packages (`All checks passed!`, all files formatted, `Success: no issues found`). |
| `src/core` unit tests | `src/core/tests` (`test_regulatory_output_guard`, `test_source_monitor`, `test_rule_engine`, `test_regulatory_chat`, `test_regulatory_eval_gates_216`, `test_regulatory_privacy_audit_217`, `test_dependency_rule`, plus subprocess suites) | Passed | 134 targeted regulatory/core tests + 45 subprocess bundle/demo/fabric tests passed (`OK`); 3,579/3,579 non-Azure-SDK core tests passed (`test_device_registry_azure` requires optional uninstalled `azure-iot-hub` SDK in host Python). |
| `src/agents` full unit tests | `src/agents/tests` (`unittest discover -s tests -q`) | Passed | `Ran 536 tests in 151.076s — OK` (including `test_regulatory_non_advice_guard`, `test_regulatory_answers`, `test_regulatory_gates`, and `test_paired_report_command` with zero edits to frozen `evals/regulatory_chat_results.json`). |
| `src/api` unit and HTTP integration tests | `src/api/tests` (full `unittest discover` + `test_regulatory_watch_guard_api`, `test_lawstore`, `test_rule_alerts`, `test_regulatory_chat_api`, `test_expected_denials`, `test_role_endpoint_inventory`, `test_auth.RuleHttpTests`, `test_assistants.DurabilityTests`) | Passed | 3,772/3,774 passed on initial full run; fixed the 2 regressions (`test_auth.RuleHttpTests` and `test_assistants.DurabilityTests`) and verified `Ran 117 tests in 110.270s — OK` across all regulatory, auth, durability, and role-inventory suites. |
| `node --check` + `rename-zava-tests.py` | `src/api/src/zava_forward/api/web/*.js` and `tools/rename-zava-tests.py` | Passed | `node --check OK` on all `web/*.js` files; `rename-zava-tests.py` `Ran 25 tests in 0.526s — OK`. |

## Pre-Review Reconciliation

* Plan markers and phase details: reconciled (`P01`, `P02`, `P03` and `P01-T01`..`P03-T03` all `[x]` / `complete`)
* Completed-work evidence and handoff prose: reconciled
* Validation, blockers, remaining work, and follow-up items: reconciled
* Review readiness: ready

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/reg-208-non-advice-guard-plan.md, `## Follow-Up Items`
* Optional interactive regulatory watch UI tab in `src/api/src/zava_forward/api/web/law.js`: outside `#208`'s deterministic guard and JSON API/workbench payload scope; owned by a future UX issue if visual diff browsing is requested.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (`P01`, `P02`, `P03`); completed all `P01-T01`..`P03-T03`, remaining `none`
* Validation coverage: complete focused tier (`ruff check`, `ruff format --check`, `mypy`, `src/core` + `src/agents` + `src/api` tests, `node --check`, `tools/rename-zava-tests.py`)
* Blockers: none
* Current plan and detail updates: recorded 3 schema/signature current-state alignments in `P03-T01` and `P02-T02`
* Planning and critique state: ready (`PC-001`..`PC-004` resolved)
* Follow-up items: optional UI tab in `web/law.js`
* Review readiness or no-handoff reason: ready for `rpi-review`
* Continuation owner: parent for confirmed automatic RPI Agent
