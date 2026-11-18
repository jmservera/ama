<!-- markdownlint-disable-file -->
# RPI Phase Details: Regulatory Non-Advice, Duty-Satisfaction, and Future-Law Output Guard (#208)

## Metadata

* Task ID: issue-208-non-advice-guard
* Task slug: reg-208-non-advice-guard
* Related plan: .copilot-tracking/plans/2026-11-15/reg-208-non-advice-guard-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/reg-208-non-advice-guard-research.md, docs/adrs/0005-regulatory-compliance-assistant.md, docs/reference/regulatory/README.md

## Phase Index

| Phase ID | Name                                                                                   | Status | Detail sections                    |
|----------|----------------------------------------------------------------------------------------|--------|------------------------------------|
| P01      | Core Deterministic Regulatory Output Guard and Future-Law Support                      | complete | P01, P01-T01, P01-T02, P01-T03     |
| P02      | Agents and Core Assistant Output Guard Enforcement                                     | complete | P02, P02-T01, P02-T02, P02-T03     |
| P03      | API Regulatory Watch, Legal/Compliance View Enforcement, Workbench Telemetry, and Test | complete | P03, P03-T01, P03-T02, P03-T03     |

<!-- rpi:phase id=P01 -->
## P01: Core Deterministic Regulatory Output Guard and Future-Law Support

### Context

Research evidence (`C2`, `C3`, `C5`, `C8`, `C9`, `C15`) established that `src/core` owns `LawStore`, `SourceMonitor`, `RuleCards`, `RuleEngine`, `RegulatoryChat`, `ChatPanel`, and `Assistants`, and that `test_dependency_rule.py` permits `core` to import only `zava_forward.core`. Placing the deterministic non-advice / duty-satisfaction / future-law guard in `zava_forward.core.regulatory_output_guard` makes it reusable across `core`, `agents`, and `api` with zero circular or forbidden dependencies.

### Intent

Provide a fast, deterministic, zero-model output-validation guard and telemetry tracker in `src/core`, add `"future_phase"` source status support to `LawStore` and `RuleEngine`, and expose a guarded `SourceMonitor.watch_summary` builder producing cited watch items with human rule-activation state.

### Boundaries

* Included: `regulatory_output_guard.py`, `lawstore.py`, `rule_engine.py`, `source_monitor.py`, and `src/core/tests/test_regulatory_output_guard.py`.
* Excluded: HTTP routing (`P03`) and `src/agents` answer composer wiring (`P02`).

### Likely Targets

* src/core/src/zava_forward/core/regulatory_output_guard.py: New deterministic guard, advisory review-item rewriter, and thread-safe telemetry registry.
* src/core/src/zava_forward/core/lawstore.py: Add `"future_phase"` to `STATUSES` and `_caveats`.
* src/core/src/zava_forward/core/rule_engine.py: Treat `"future_phase"` as `"not applicable"` in `citation_eligibility`.
* src/core/src/zava_forward/core/source_monitor.py: Add `watch_summary` and `summarize_watch` helper guarded by `regulatory_output_guard`.
* src/core/tests/test_regulatory_output_guard.py: New unit test suite covering all core guard and watch-summary contracts.

### Dependencies

* none

### Validation Expectations

* `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_regulatory_output_guard.py" -v` inside `src/core`.
* `python3 -m ruff check` and `python3 -m mypy` inside `src/core`.

### Completion Evidence

* Passing unit tests in `src/core/tests/test_regulatory_output_guard.py` and existing `test_source_monitor.py` / `test_rule_engine.py` / `test_dependency_rule.py`.

### Unresolved Items

* none

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement `zava_forward.core.regulatory_output_guard` and telemetry registry

#### Context

Issue `#208` requires blocking or rewriting three classes of unsafe regulatory output claims:
1. `duty_satisfied`: stating a legal or statutory duty is satisfied/met/fulfilled/discharged or that a home/case/provider/action complies with the Act/Standard/Regulations/law or is legally compliant (`duty is satisfied`, `complies with the Act`, `legally compliant`, `statutory duty has been met`, `in compliance with section ...`).
2. `legal_advice`: giving legal advice or binding legal counsel/determinations (`this is legal advice`, `constitutes legal advice`, `our legal advice`, `you are legally required`, `you are legally exempt`, `legally obligates you`, `we advise you legally`).
3. `future_law_applied_as_active`: applying future/consultative law or uncommenced phases as active operational rules, either lexically (`applies future law as active`, `consultation applies as an active rule`, `future phase is active now`, `uncommenced phase applies as an active operational rule`, `proposed law is currently in force`) or contextually when source/card metadata indicates `status in ("consultation", "future_phase")`, `effective > as_of_day`, or `human_rule_activated is False` while the text or structured payload claims active operational rule enforcement (`active operational rule`, `applies now as an active rule`, `currently binding operational rule`, `active_operational_rule=True`, or `active_control=True`).

Contrarian evidence (`C9`, `C11`, `C17`, `C18`, `C20`) requires:
* NFKC normalization + stripping `Cf` format chars + homoglyph translation (`CONFUSABLES`) before lexical matching.
* Clause-level segmentation (`[.;!?\n]` plus contrast splits `, not `, `; not `, ` - not `, ` -- not `, ` but not `, ` rather than `) so local negations (`not`, `no`, `never`, `neither`, `cannot`, `can't`, `does not`, `do not`, `is not`, `are not`, `without`, `whether`, `if`, `not assessed`, `unassessed`, `not a finding`, `cannot decide`, `cannot confirm`) exempt genuine disclaimers in that clause without exempting affirmative violations in adjacent clauses (defeating disclaimer-stuffing).
* Optional `verbatim_quotes` exemption for bracketed/quoted verbatim statutory excerpts that come from verified active `in_force`/`guidance` provisions (`effective <= as_of_day` and `human_rule_activated=True`), while NEVER exempting quotes or summaries presented as active rules when `status in ("consultation", "future_phase")`, `effective > as_of_day`, or `human_rule_activated=False`.

#### Intent

Deliver `regulatory_output_guard.py` with:
* `GUARD_VERSION = "regulatory-non-advice-guard-v1"`
* `CATEGORIES = ("duty_satisfied", "legal_advice", "future_law_applied_as_active")`
* `ADVISORY_REVIEW_TEXT`: deterministic plain-language replacement framing the item as a dated reference / review item requiring named human legal or compliance review, never confirming duty satisfaction, giving legal advice, or activating future/consultative law.
* `GuardDecision` dataclass (`checked`, `passed`, `action`, `violations`, `reasons`, `rewritten_text`, `guard_version`) with `to_status_dict()` returning compact metadata (`checked`, `passed`, `action`, `violations`, `guard_version`) without `rewritten_text` so persisted chat turns never bloat `MAX_CONTENT` (`PC-001`).
* `inspect_regulatory_output(..., on_violation="rewrite" | "reject")` and `guard_regulatory_text(...)` (`PC-003`, `PC-004`): under unactivated/future/consultation metadata (`status in ("consultation", "future_phase")`, `effective > as_of_day`, or `human_rule_activated is False`), structured boolean flags (`active_operational_rule is True` or `active_control is True`) fail unconditionally with `future_law_applied_as_active`, whereas contextual active-rule prose patterns apply the same clause-scoped negation filter as lexical patterns so negated caveats (`"Uncommenced future phase, not an active operational rule."`, `"inactive pending human compliance review"`) pass cleanly.
* `GuardTelemetry` with thread-safe counters (`checked_total`, `passed_total`, `flagged_total`, `rewritten_total`, `rejected_total`, `by_category`, `record_decision(decision)`, `snapshot()`, and `reset()`), incrementing `rewritten_total` when `action == "rewritten"` and `rejected_total` when `action == "rejected"`.

#### Boundaries

* Included: `src/core/src/zava_forward/core/regulatory_output_guard.py`.
* Excluded: Model/LLM calls (strictly deterministic Python stdlib only).

#### Likely Targets

* src/core/src/zava_forward/core/regulatory_output_guard.py: Core guard module.

#### Dependencies

* none

#### Validation Expectations

* Unit tests verify `passed=True` on every existing codebase disclaimer (`LABEL`, `UNKNOWN`, `NOT_REVIEWED`, `REGULATORY_ANSWER`, `Consultation material, not a final rule.`) and `passed=False` with exact category attribution on affirmative claims, homoglyph bypasses, and disclaimer-stuffed strings.

#### Completion Evidence

* `regulatory_output_guard.py` passes `ruff check` and strict `mypy`.

#### Unresolved Items

* none

<!-- rpi:task id=P01-T02 -->
### P01-T02: Extend `LawStore`, `RuleEngine`, and `SourceMonitor.watch_summary` with guard enforcement

#### Context

`lawstore.STATUSES` (`C2`) currently lists `("in_force", "guidance", "consultation", "historical")`. Adding `"future_phase"` lets both `LawStore` and `SourceMonitor.observe` (`C3`, line 345) record uncommenced legislative phases explicitly (such as future Awaab's Law / Decent Homes phases), with `_caveats` emitting `"Uncommenced future phase, not an active operational rule."` and `rule_engine.citation_eligibility` (`C5`, line 236) returning `"not applicable"` whenever `status in ("consultation", "future_phase", "historical")` or `effective > day`.

`SourceMonitor` (`C3`) stores configurations, observations, candidate diffs (`reg_monitor_change`), and release events (`approved`, `regression`, `activated`, `rolled_back`), and opens `rule_card_review` items, yet currently lacks a read-side `watch_summary(today, telemetry=...)` method that assembles cited source watch entries, detected candidate changes, and open review items while passing every rendered summary through `regulatory_output_guard`.

#### Intent

* Update `lawstore.py` (`STATUSES` and `_caveats`) and `rule_engine.py` (`citation_eligibility`) for `"future_phase"`.
* Add `watch_summary(law, *, today, custom_summaries=None, telemetry=None)` in `source_monitor.py` (and `SourceMonitor.watch_summary(self, *, today, ...)`):
  * For each held source in `law.sources()["sources"]`, build a deterministic cited summary containing `source_id`, `title`, `version`, `provision_ids` (e.g. first/cited provision IDs), `status`, `source_effective` (`effective`), `retrieved` (`retrieved` date), `review_status`, `freshness` (`source_freshness`), `active_card_ids` (human-activated cards via `law.rules.is_active(cid, today)` whose `citation_eligibility == "active"`), `human_rule_activated` (`bool(active_card_ids)` and `status in ("in_force", "guidance")` and `(not effective or effective <= today)` and `review_status == "reviewed"`), `active_operational_rule` (`human_rule_activated`), and a cited `summary` string stating the provision ID, source/effective date, retrieval date, and human-activation status.
  * For each recorded `reg_monitor_change` and `rule_card_review`, build a review-item watch entry (`verified`, `status`, `candidate_status`, `candidate_effective`, `human_rule_activated=False`, `active_operational_rule=False`, `summary`) and validate its `summary` and note/interpretation fields through `regulatory_output_guard`.
  * Whenever any summary or injected/stored text claims duty satisfaction, gives legal advice, or applies unactivated/`consultation`/`future_phase`/future-dated material as an active operational rule, the guard flags the entry (`output_guard.passed = False`), forces `active_operational_rule = False`, replaces the unsafe summary with deterministic advisory review-item language preserving the dated source/provision citation, and records the telemetry event.

#### Boundaries

* Included: `lawstore.py`, `rule_engine.py`, `source_monitor.py`.
* Excluded: Mutating append-only ledger tables (`reg_source`, `reg_version`, `reg_provision`, `reg_monitor_*`).

#### Likely Targets

* src/core/src/zava_forward/core/lawstore.py: Add `"future_phase"` to `STATUSES` and `_caveats`.
* src/core/src/zava_forward/core/rule_engine.py: Include `"future_phase"` in `"not applicable"` status check.
* src/core/src/zava_forward/core/source_monitor.py: Add `watch_summary` function and `SourceMonitor.watch_summary` method with `output_guard` enforcement and telemetry summary.

#### Dependencies

* P01-T01

#### Validation Expectations

* Existing `test_source_monitor.py`, `test_rule_engine.py`, and `src/api/tests/test_lawstore.py` continue to pass, and `watch_summary` passes unit tests for clean cited summaries and all three violation categories.

#### Completion Evidence

* Guarded `watch_summary` payload contains `as_of`, `sources`, `changes`, `reviews`, and `output_guard` (status + telemetry).

#### Unresolved Items

* none

<!-- rpi:task id=P01-T03 -->
### P01-T03: Add comprehensive `src/core` unit tests for `regulatory_output_guard` and `watch_summary`

#### Context

Unit tests in `src/core/tests/test_regulatory_output_guard.py` must prove both isolated text/context guard behavior and `SourceMonitor.watch_summary` + `RuleEngine` behavior on `consultation`, `future_phase`, future `effective` dates, and unactivated vs human-activated rule cards.

#### Intent

Create `src/core/tests/test_regulatory_output_guard.py` testing:
1. Duty-satisfaction claims (`"The statutory duty is satisfied"`, `"This home complies with the Act"`, `"The landlord is legally compliant under section 10A"`, disclaimer-stuffed `"Not legal advice, but the duty is satisfied"`) -> flagged (`duty_satisfied`) and rewritten to advisory review-item text.
2. Legal-advice claims (`"Our legal advice is to delay works"`, `"You are legally exempt from phase 1"`, `"This constitutes legal advice"`, Cyrillic homoglyph `"l\u0435gal advice is that you must..."`) -> flagged (`legal_advice`) and rejected/rewritten.
3. Future/consultative law applied as active (`status="consultation"`, `status="future_phase"`, `effective="2027-10-01"` when `as_of="2026-10-16"`, or `human_rule_activated=False` claiming `"applies now as an active operational rule"` or `active_operational_rule=True`) -> flagged (`future_law_applied_as_active`), `active_operational_rule` forced `False`, and rewritten to advisory review-item language.
4. Legitimate cited summaries with provision ID, source/effective date, retrieval date, and human-activation status (plus all codebase disclaimers `LABEL`, `UNKNOWN`, `NOT_REVIEWED`, `REGULATORY_ANSWER`) -> pass cleanly (`passed=True`, `violations=[]`, text unchanged).

#### Boundaries

* Included: `src/core/tests/test_regulatory_output_guard.py`.
* Excluded: HTTP server tests (`P03-T02`).

#### Likely Targets

* src/core/tests/test_regulatory_output_guard.py: Core unit test file.

#### Dependencies

* P01-T01, P01-T02

#### Validation Expectations

* All tests in `src/core/tests/` pass with zero regressions.

#### Completion Evidence

* Green unittest run in `src/core`.

#### Unresolved Items

* none

<!-- rpi:phase id=P02 -->
## P02: Agents and Core Assistant Output Guard Enforcement

### Context

Research (`C6`, `C9`, `C10`, `C11`, `C17`, `C18`, `C19`) identified three assistant pipelines:
1. Extractive regulatory chat: `zava_forward.agents.regulatory_chat.answer(bundle)` rendered via `zava_forward.core.regulatory_chat.RegulatoryChat.ask`.
2. Employee case conversation chat: `zava_forward.core.chat_panel.ChatPanel._ask`.
3. Five structured evidence-proposal assistants: `zava_forward.core.assistants` (`validate_output` and `_output_violates_visibility`).

Contrarian evidence (`C17`, `C18`, `C19`) proved that valid `regulatory-chat-v1` responses must keep exact `cards` list items, `sections` keys, `citations`, and `usage` schemas so `evals/regulatory_chat_results.json`, `grade_chat_turn`, and `regulatory_usage.py` remain 100% compatible.

### Intent

Enforce `regulatory_output_guard` deterministically across all assistant response generators and validators in `src/agents` and `src/core`, and add focused `src/agents` unit tests.

### Boundaries

* Included: `src/agents/src/zava_forward/agents/regulatory_chat.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/src/zava_forward/core/chat_panel.py`, `src/core/src/zava_forward/core/assistants.py`, and `src/agents/tests/test_regulatory_non_advice_guard.py`.
* Excluded: Frozen eval dataset `src/agents/evals/regulatory_chat_results.json` (must NOT be modified; tests must pass against it unchanged).

### Likely Targets

* src/agents/src/zava_forward/agents/regulatory_chat.py: Enforce output guard in `answer(bundle)` and attach `output_guard` check summary.
* src/core/src/zava_forward/core/regulatory_chat.py: Enforce output guard on `self.render(...)` replies (supporting both `reply` and `answer` keys), rewrite/block unsafe claims into advisory review-item language, and expose `guard_status()`.
* src/core/src/zava_forward/core/chat_panel.py: Check `inspect_regulatory_output` on parsed model answers before emitting `"answer"`, withholding unsafe replies as `"withheld"`.
* src/core/src/zava_forward/core/assistants.py: Check `inspect_regulatory_output` in `_output_violates_visibility` and `validate_output` so unsafe model proposals fail validation / are withheld.
* src/agents/tests/test_regulatory_non_advice_guard.py: New unit test suite for agent regulatory responses.

### Dependencies

* P01

### Validation Expectations

* `PYTHONPATH=src:tests:../core/src python3 -m unittest discover -s tests -q` in `src/agents` (including `test_regulatory_answers.py` and `test_regulatory_gates.py`).
* `python3 -m ruff check` and `PYTHONPATH=../core/src python3 -m mypy` in `src/agents`.

### Completion Evidence

* Passing `src/agents` and `src/core` test suites with zero modifications to `evals/regulatory_chat_results.json`.

### Unresolved Items

* none

<!-- rpi:task id=P02-T01 -->
### P02-T01: Enforce output guard in `agents/regulatory_chat.py` and `core/regulatory_chat.py`

#### Context

In `agents/regulatory_chat.py:answer(bundle)` (`C11`, `PC-001`, `PC-002`), `bundle` carries `sources`, `facts`, `cards`, `as_of`, `conflict`, `refusal`, and optional `unknown`.
* Preserve existing `refusal`, `conflict`, and empty-source `unknown` branches first, validating their rendered prose lexically through `inspect_regulatory_output` (without recording telemetry yet, so frozen evals in `src/agents/evals/regulatory_chat_results.json` pass with `output_guard.passed=True`).
* On candidate `kind="answer"` turns, enforce contextual activation by requiring BOTH: (a) every cited source has `status in ("in_force", "guidance", "recorded-synthetic-demo")`, `review_status` not in `("not_reviewed", "historical")` when present, and `effective is None or effective <= as_of_day`; AND (b) `bundle["cards"]` is non-empty with no card marked inactive or unapproved (`status in ("draft", "retired", "rejected", "superseded")`, `active is False`, or `approved is False`). If either (a) or (b) fails, flag `future_law_applied_as_active`, demote the turn to advisory review-item guidance (`kind="refused"`, `citations=[]`, safe `sections` keeping all 5 `SECTION_KEYS`), and attach `output_guard = decision.to_status_dict()` (`passed=False`, `action="rewritten"`).
* Also validate non-quote prose across `unknown`, `safe_default`, `refusal`, `sections`, and combined `reply` (masking verbatim active quotes); if unsafe prose appears, flag `output_guard.passed=False` and rewrite unsafe fields to `ADVISORY_REVIEW_TEXT`.
* In `core/regulatory_chat.py:RegulatoryChat.ask` (`PC-001`), maintain one single telemetry-recording gate (`self.guard_telemetry`): if `self.render(bundle)` returned `output_guard` with `passed is False`, record that upstream failure decision once into `self.guard_telemetry` and preserve `output_guard` (`passed=False`) while still ensuring `reply`/`answer` and non-quote strings inside `sections` are sanitized; otherwise inspect `reply`/`answer` and non-quote `sections` strings once, rewrite any unsafe custom `render` strings to `ADVISORY_REVIEW_TEXT`, record the decision once, and store compact `output_guard` (`to_status_dict()`).

#### Intent

Wire `regulatory_output_guard` into `agents/regulatory_chat.py` and `core/regulatory_chat.py` (including a `RegulatoryChat.guard_status()` telemetry accessor).

#### Boundaries

* Included: `src/agents/src/zava_forward/agents/regulatory_chat.py`, `src/core/src/zava_forward/core/regulatory_chat.py`.
* Excluded: Changing `offline_usage` fields or mutating `card` dicts inside `bundle["cards"]`.

#### Likely Targets

* src/agents/src/zava_forward/agents/regulatory_chat.py: Guard check + `output_guard` field on returned envelope.
* src/core/src/zava_forward/core/regulatory_chat.py: Post-`self.render` guard enforcement + `guard_status()`.

#### Dependencies

* P01-T01

#### Validation Expectations

* `test_regulatory_answers.py`, `test_regulatory_gates.py`, `test_regulatory_eval_gates_216.py`, `test_regulatory_chat.py`, and `test_regulatory_privacy_audit_217.py` all pass cleanly.

#### Completion Evidence

* Both `agents` composer and `core` `RegulatoryChat.ask` block/rewrite unsafe outputs and attach `output_guard` metadata.

#### Unresolved Items

* none

<!-- rpi:task id=P02-T02 -->
### P02-T02: Enforce output guard in `core/chat_panel.py` and `core/assistants.py`

#### Context

`ChatPanel._ask` (`C9`, line 983, `PC-004`) already withholds model replies matching `ACTION_CLAIM`. Adding `not inspect_regulatory_output(parsed[0], on_violation="reject", telemetry=self.guard_telemetry).passed` to that exact gate ensures that if the conversational LLM generates `"Your statutory duty is satisfied"`, `"Here is legal advice: you are legally exempt"`, or `"Apply the consultation future phase as an active rule"`, `ChatPanel` deterministically withholds the reply (`kind="withheld"`, `text=WITHHELD`) and increments `rejected_total`.
Similarly, in `assistants.py` (`C10`, lines 141-155 and 732-775, `PC-004`), checking `inspect_regulatory_output(..., on_violation="reject", telemetry=self.guard_telemetry)` in `Assistants` / `validate_output` / `_output_violates_visibility` ensures none of the five structured assistants can persist or display prohibited regulatory claims and records `rejected_total` when rejecting/withholding.

#### Intent

Enforce `inspect_regulatory_output` in `chat_panel.py` and `assistants.py`.

#### Boundaries

* Included: `src/core/src/zava_forward/core/chat_panel.py`, `src/core/src/zava_forward/core/assistants.py`.
* Excluded: Altering deterministic `WORKFLOW_RULES` or `CONSENT_STATES` strings (verified safe under the guard).

#### Likely Targets

* src/core/src/zava_forward/core/chat_panel.py: Add `not inspect_regulatory_output(parsed[0]).passed` check alongside `ACTION_CLAIM`.
* src/core/src/zava_forward/core/assistants.py: Add `not inspect_regulatory_output(...).passed` check in `_output_violates_visibility` and `validate_output`.

#### Dependencies

* P01-T01

#### Validation Expectations

* Existing `test_chat_panel*.py` and `test_assistants*.py` suites in `src/core` and `src/api` pass, plus new unit assertions in `test_regulatory_output_guard.py`.

#### Completion Evidence

* Unsafe model replies in `ChatPanel` become `"withheld"` and unsafe `Assistants` outputs raise `ValueError` in `validate_output`.

#### Unresolved Items

* none

<!-- rpi:task id=P02-T03 -->
### P02-T03: Add `src/agents` unit tests proving agent-layer guard enforcement and frozen-eval stability

#### Context

`src/agents/tests/test_regulatory_non_advice_guard.py` directly exercises `zava_forward.agents.regulatory_chat.answer` across all four required test scenarios in Issue `#208`.

#### Intent

Create `src/agents/tests/test_regulatory_non_advice_guard.py` testing:
1. Bundle/card with unsafe `safe_default` or `unknown` claiming `"The statutory duty is satisfied and the home complies with the Act"` -> flagged (`duty_satisfied`), rewritten to advisory review-item language, `output_guard["passed"] is False`.
2. Bundle/card with text giving legal advice (`"Legal advice: you are legally exempt from enforcement"`) -> flagged (`legal_advice`), rejected/rewritten, `output_guard["passed"] is False`.
3. Bundles where cited source has `status="consultation"`, `status="future_phase"`, or `effective="2027-06-01"` (`> as_of`), or `cards=[]` / unapproved draft card -> flagged (`future_law_applied_as_active`), blocked from returning active `kind="answer"`, replaced with advisory review-item refusal/guidance.
4. Legitimate cited bundle with active human-approved card, `status="in_force"`, `effective="2025-10-27"`, `retrieved="2026-09-19"`, and provision ID -> returns `kind="answer"`, `output_guard["passed"] is True`, `output_guard["violations"] == []`, preserving exact excerpts and mandatory disclaimers.

#### Boundaries

* Included: `src/agents/tests/test_regulatory_non_advice_guard.py`.
* Excluded: Modifying `src/agents/evals/regulatory_chat_results.json`.

#### Likely Targets

* src/agents/tests/test_regulatory_non_advice_guard.py: Agent-layer non-advice guard test suite.

#### Dependencies

* P02-T01

#### Validation Expectations

* `src/agents` unittest suite passes 100%.

#### Completion Evidence

* Green unittest + `mypy` + `ruff` in `src/agents`.

#### Unresolved Items

* none

<!-- rpi:phase id=P03 -->
## P03: API Regulatory Watch, Legal/Compliance View Enforcement, Workbench Telemetry, and Validation

### Context

Research (`C12`, `C13`, `C14`, `C16`) showed `server.py` exposes `/api/law/sources*`, `/api/law/provisions/*`, `/api/law/search`, `/api/law/cards*`, `/api/law/alerts*`, `/api/chat/regulatory/*`, and `/api/me`, and `plain_language.py` adds `plain_summary` to `/api/chat/regulatory/threads/{id}/ask`. We need `GET /api/law/watch` exposing the guarded regulatory watch payload + telemetry, guard enforcement on legal/compliance views and `plain_summary`, workbench telemetry in `/api/chat/regulatory/status` and `/api/me`, registration in `test_role_endpoint_inventory.py`, and end-to-end HTTP integration tests.

### Intent

Expose the regulatory watch API and workbench guard telemetry, enforce the deterministic guard across all HTTP regulatory/compliance views and assistant endpoints, validate all three packages + `rename-zava-tests.py`, and commit cleanly on `feat/reg-208-non-advice-guard`.

### Boundaries

* Included: `src/api/src/zava_forward/api/plain_language.py`, `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_role_endpoint_inventory.py`, `src/api/tests/test_regulatory_watch_guard_api.py`, and `.copilot-tracking/` implementation/review artifacts.
* Excluded: `src/api/src/zava_forward/api/web/*` files, `infra/`, and pushing to `main`.

### Likely Targets

* src/api/src/zava_forward/api/plain_language.py: Guard `plain_summary` through `guard_regulatory_text`.
* src/api/src/zava_forward/api/server.py: Add `App.output_guard` (`GuardTelemetry`), `App.source_monitor()`, `GET /api/law/watch`, guard checks + `output_guard` metadata on `/api/law/*`, `/api/chat/regulatory/status`, `/api/chat/regulatory/threads/{id}/ask`, and `/api/me`.
* src/api/tests/test_role_endpoint_inventory.py: Add `"/api/law/watch"` to `GET_ENDPOINTS`.
* src/api/tests/test_regulatory_watch_guard_api.py: End-to-end loopback HTTP integration tests proving all 4 Issue `#208` criteria and telemetry reporting.

### Dependencies

* P01, P02

### Validation Expectations

* `ruff check` and `mypy` in `src/core`, `src/agents`, and `src/api` (with `PYTHONPATH=../core/src:../agents/src` for `api` and `PYTHONPATH=../core/src` for `agents`).
* Full `unittest discover` in `src/core`, `src/agents`, and `src/api`.
* `python3 tools/rename-zava-tests.py` from repository root.

### Completion Evidence

* All focused-tier tests, linters, type-checks, and rename checks pass; changes artifact and post-implementation review artifact are recorded and committed on `feat/reg-208-non-advice-guard`.

### Unresolved Items

* none

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add `GET /api/law/watch`, guard legal/compliance and `plain_language` responses, and expose workbench telemetry in `server.py`

#### Context

In `server.py` (`PC-001`, `PC-003`, `PC-004`):
* `App.__init__` initializes `self.guard_telemetry = GuardTelemetry()` and passes it to `RegulatoryChat`, `ChatPanel`, `Assistants`, and `SourceMonitor` watch helpers so every regulatory rewrite or rejection in that `App` instance records unified, inspectable telemetry (`rewritten_total` and `rejected_total`) without cross-test pollution.
* `GET /api/law/watch`:
  * Checks `projection.allowed(u, "law")` -> `403` if denied (matching `/api/law/sources` and `/api/law/cards` so Contractors and Mystery roles are blocked per `test_role_endpoint_inventory.py`).
  * Checks `app.law is None` -> `503 {"error": "The law store is not loaded."}` (matching `/api/law/sources` when `law=None`, which is how `RoleEndpointInventory` initializes `App(cls.store)` without `law`!).
  * Under `with app.law_lock:`, calls `watch_summary(app.law, today=datetime.now(UTC).date().isoformat(), telemetry=app.guard_telemetry)` and returns `200` JSON containing `label`, `as_of`, `sources`, `changes`, `reviews`, and `output_guard` (status + telemetry snapshot).
* Legal/compliance views and exports (`/api/law/sources`, `/api/law/sources.csv`, `/api/law/sources/{id}`, `/api/law/provisions/{id}`, `/api/law/search`, `_rulecards` for `/api/law/cards*`, and `_rule_alerts` for `/api/law/alerts*`):
  * Guard inside the shared source-list serializer feeding BOTH `/api/law/sources` and `/api/law/sources.csv`, inside `/api/law/sources/{id}`, `/api/law/provisions/{id}`, and `/api/law/search`, and inside `_rulecards` and `_rule_alerts` so every subroute and export is covered identically.
  * In `_rulecards`, pass each card's actual activation flag (`is_active = law.rules.is_active(cid, today)` and `active_operational_rule = declared_active`) so inactive draft cards pass cleanly unless their prose affirmatively asserts active operational force or compliance/legal advice (`PC-003`), while returning `(guarded_card, status)` and attaching merged `output_guard` on the `/api/law/cards*` envelope so individual card dicts keep exact `law.rules.history` key parity (`test_auth.py`).
* Assistant & workbench status views:
  * `plain_language.py`: pass `plain_summary` through `guard_regulatory_text` (and merge into `output_guard` via `merge_guard_statuses`).
  * `GET /api/chat/regulatory/status` and `GET /api/chat/status`: include `"output_guard": app.guard_telemetry.snapshot()`.
  * `POST /api/chat/regulatory/threads/{id}/ask`: do NOT re-check `reply` (already guarded and recorded once in `RegulatoryChat.ask`, `PC-001`); guard `plain_summary` when added and merge any `plain_summary` failure into the turn's `output_guard` without clobbering an upstream `passed=False`.
  * `GET /api/me`: include top-level `"regulatory_output_guard": app.guard_telemetry.snapshot()` when `projection.allowed(u, "law")` is true while preserving the exact four-key `me["services"]` dictionary (`test_expected_denials.py`), so Contractor/Mystery payloads receive zero internal compliance telemetry while workbench staff roles see live guard health and counters.

#### Intent

Deliver complete HTTP API enforcement and workbench telemetry exposure in `plain_language.py` and `server.py`.

#### Boundaries

* Included: `src/api/src/zava_forward/api/plain_language.py`, `src/api/src/zava_forward/api/server.py`.
* Excluded: Front-end JS changes.

#### Likely Targets

* src/api/src/zava_forward/api/plain_language.py: Guard plain-language summary text.
* src/api/src/zava_forward/api/server.py: Add `/api/law/watch`, guard `/api/law/*` and `/api/chat/regulatory/*`, and expose telemetry on `/api/law/watch`, `/api/chat/regulatory/status`, and `/api/me`.

#### Dependencies

* P01, P02

#### Validation Expectations

* Existing `test_lawstore.py`, `test_rulecards.py`, `test_rule_alerts.py`, `test_regulatory_chat_api.py`, and `test_role_endpoint_inventory.py` pass without regression.

#### Completion Evidence

* `GET /api/law/watch`, `/api/law/*`, `/api/chat/regulatory/*`, and `/api/me` return deterministic `output_guard` status and telemetry.

#### Unresolved Items

* none

<!-- rpi:task id=P03-T02 -->
### P03-T02: Register `/api/law/watch` in `test_role_endpoint_inventory.py` and add `test_regulatory_watch_guard_api.py`

#### Context

`test_role_endpoint_inventory.py` (`C16`) requires every `/api/...` route in `server.py` to appear in `GET_ENDPOINTS` or `POST_ENDPOINTS`. Adding `"/api/law/watch"` to `GET_ENDPOINTS` automatically tests all staff roles, `Contractor`, and `Mystery` against `/api/law/watch` for status codes and canary non-leakage.
In addition, `src/api/tests/test_regulatory_watch_guard_api.py` will run a real loopback `ThreadingHTTPServer` against `App` with `LawStore` and `SourceMonitor` to prove all Issue `#208` requirements end-to-end over HTTP.

#### Intent

* Add `"/api/law/watch"` to `GET_ENDPOINTS` in `src/api/tests/test_role_endpoint_inventory.py`.
* Create `src/api/tests/test_regulatory_watch_guard_api.py` proving over HTTP:
  1. Legitimate cited regulatory watch summaries (`GET /api/law/watch`), compliance views (`GET /api/law/sources`, `GET /api/law/cards`), and regulatory chat answers (`POST /api/chat/regulatory/threads/{id}/ask`) citing source date, retrieval date, provision ID, and human-activation status pass cleanly (`output_guard.passed is True`, `violations == []`).
  2. Outputs claiming a statutory duty is satisfied (e.g., in a review assessment interpretation, card summary, or rendered chat reply) are flagged (`duty_satisfied`) and replaced with advisory review-item language, never serving the compliance verdict to the client.
  3. Outputs giving legal advice (`"This constitutes legal advice: you are legally exempt..."`) are flagged (`legal_advice`) and replaced/rejected.
  4. Outputs or watch/card items applying `consultation`, `future_phase`, or future `effective` date sources without human rule activation as active operational rules are flagged (`future_law_applied_as_active`), have `active_operational_rule` forced `False`, and are rewritten/blocked.
  5. Guard telemetry (`checked_total`, `passed_total`, `flagged_total`, `rewritten_total`, `by_category`) is exposed and consistent across `GET /api/law/watch`, `GET /api/chat/regulatory/status`, and `GET /api/me` (and withheld from `Contractor`).

#### Boundaries

* Included: `src/api/tests/test_role_endpoint_inventory.py`, `src/api/tests/test_regulatory_watch_guard_api.py`.
* Excluded: Browser Playwright checks (not modified or needed since `web/` is untouched).

#### Likely Targets

* src/api/tests/test_role_endpoint_inventory.py: Add `"/api/law/watch"`.
* src/api/tests/test_regulatory_watch_guard_api.py: New HTTP API integration suite.

#### Dependencies

* P03-T01

#### Validation Expectations

* `test_role_endpoint_inventory.py` and `test_regulatory_watch_guard_api.py` pass 100%.

#### Completion Evidence

* Green HTTP integration proofs for all 4 acceptance scenarios and telemetry counters.

#### Unresolved Items

* none

<!-- rpi:task id=P03-T03 -->
### P03-T03: Run focused validation suite across `src/core`, `src/agents`, `src/api`, and `rename-zava-tests.py`

#### Context

Focused-tier validation requires matching `.github/workflows/src-ci.yml` locally for every modified package (`src/core`, `src/agents`, `src/api`) plus running `python3 tools/rename-zava-tests.py`.

#### Intent

Run and record:
* `src/core`: `python3 -m ruff check`, `python3 -m mypy`, `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q`
* `src/agents`: `python3 -m ruff check`, `PYTHONPATH=../core/src python3 -m mypy`, `PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest discover -s tests -q`
* `src/api`: `python3 -m ruff check`, `PYTHONPATH=../core/src:../agents/src python3 -m mypy`, `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q`
* Root: `python3 tools/rename-zava-tests.py`

#### Boundaries

* Included: Local focused validation and recording exact command outputs in `.copilot-tracking/changes/2026-11-15/reg-208-non-advice-guard-changes.md`.
* Excluded: Full external receipt gate (task prompt explicitly specifies `Validation tier: Focused`).

#### Likely Targets

* .copilot-tracking/changes/2026-11-15/reg-208-non-advice-guard-changes.md: Implementation and validation evidence log.

#### Dependencies

* P03-T01, P03-T02

#### Validation Expectations

* Exit code `0` across every command above.

#### Completion Evidence

* Recorded command results in `.copilot-tracking/changes/2026-11-15/reg-208-non-advice-guard-changes.md`.

#### Unresolved Items

* none
