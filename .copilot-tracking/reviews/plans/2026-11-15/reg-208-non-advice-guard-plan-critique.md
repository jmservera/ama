<!-- markdownlint-disable-file -->
# RPI Plan Critique: Regulatory Non-Advice, Duty-Satisfaction, and Future-Law Output Guard (#208)

## Metadata

* Task ID: issue-208-non-advice-guard
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/reg-208-non-advice-guard-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Prove Issue `#208` criterion (`No output states that a duty is satisfied, gives legal advice or applies future law as active`) across `src/core/`, `src/agents/`, and `src/api/`; implement an explicit, deterministic zero-model output-validation guard across regulatory watch summaries, assistant responses, and legal/compliance views blocking or rewriting duty-satisfaction claims, legal-advice claims, and unactivated `consultation` / `future_phase` / future-dated sources applied as active operational rules; expose guard telemetry and check status in the regulatory watch API and workbench payloads; prove all four required test scenarios via unit and loopback HTTP integration tests; and validate under the focused tier (`ruff check`, `mypy`, `unittest` across `src/core`, `src/agents`, `src/api`, plus `python3 tools/rename-zava-tests.py`).
* Research and evidence considered: .copilot-tracking/research/2026-11-15/reg-208-non-advice-guard-research.md (`C1`-`C20`), .copilot-tracking/plans/2026-11-15/reg-208-non-advice-guard-plan.md, .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md, docs/adrs/0005-regulatory-compliance-assistant.md, docs/reference/regulatory/README.md.
* Decisions, dependencies, and acceptance criteria considered: Canonical guard placement in `zava_forward.core.regulatory_output_guard` to satisfy `test_dependency_rule.py` (`C15`); `GET /api/law/watch` registration in `src/api/tests/test_role_endpoint_inventory.py` (`C16`) with `projection.allowed(user, "law")` and `503` when `app.law is None`; preservation of `src/agents/evals/regulatory_chat_results.json` (`C17`), `grade_chat_turn` `cards`/`sections` schema invariants (`C18`), and `offline_usage` metering (`C19`); test budget lock (zero test removals, at most 3 new test files plus 1 route entry in `test_role_endpoint_inventory.py`); commit on `feat/reg-208-non-advice-guard` without pushing to `main`.
* Assessment boundary: Evaluates completeness, internal consistency, architectural invariants, telemetry fidelity, and testability of the candidate plan and phase details strictly from supplied artifacts and cited repository authority documents, without modifying plan sources or performing open-ended codebase research.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Requirement 1 (Issue `#208` criterion across `core`, `agents`, `api`) | Partial | Architecture spans all three packages (`C15`), but `PC-001`, `PC-002`, and `PC-004` identify cross-layer overwrite, card-predicate, and export/subroute gaps that require direct planner tightening. |
| Requirement 2 (Deterministic 3-category guard + advisory rewrite/reject) | Partial | Unicode/homoglyph folding and clause-scoped disclaimer rules are well grounded (`C9`, `C20`), but `PC-002` and `PC-003` identify boolean/contextual activation edge cases on unactivated `in_force`/`guidance` sources, negated caveats, and draft cards. |
| Requirement 3 (Watch/workbench telemetry + 4 unit/API test scenarios) | Partial | All 4 scenarios are mapped to `P01-T03`, `P02-T03`, and `P03-T02`, but post-rewrite re-checking (`PC-001`) and unwired `rejected_total` counters (`PC-004`) would skew HTTP `output_guard` status and telemetry assertions. |
| Requirement 4 (Focused validation tier + branch boundary) | Covered | `P03-T03` specifies per-package `ruff check`, `mypy` with accurate `PYTHONPATH`, `unittest discover` across `src/core`, `src/agents`, `src/api`, and `python3 tools/rename-zava-tests.py` on `feat/reg-208-non-advice-guard`. |
| Research `C1`-`C20` invariants | Partial | `C15` (dependency rule), `C16` (endpoint inventory), and `C19` (usage metering) are covered; `C6` (`MAX_CONTENT`), `C12` (`/api/law/sources.csv`, `/api/law/alerts*`), and `C17`/`C18` (`sections` and refusal/conflict/gap stability) need the refinements in `PC-001`, `PC-002`, and `PC-004`. |
| `P01` (`P01-T01`, `P01-T02`, `P01-T03`) | Partial | Strong core design (`regulatory_output_guard.py`, `"future_phase"`, `SourceMonitor.watch_summary`); needs compact status serialization (`PC-001`), explicit boolean-vs-clause-negation precedence (`PC-003`), and `on_violation` action semantics (`PC-004`). |
| `P02` (`P02-T01`, `P02-T02`, `P02-T03`) | Partial | Covers `agents/regulatory_chat.py`, `core/regulatory_chat.py`, `chat_panel.py`, and `assistants.py`, but needs single-record telemetry/status preservation and `sections` sanitization (`PC-001`), reconciled source/card activation logic (`PC-002`), and `rejected_total` telemetry recording (`PC-004`). |
| `P03` (`P03-T01`, `P03-T02`, `P03-T03`) | Partial | Covers `GET /api/law/watch`, `/api/chat/regulatory/status`, `/api/me`, `plain_language.py`, `test_role_endpoint_inventory.py`, and focused validation, but needs non-clobbering chat route status merge (`PC-001`), draft-card activation context (`PC-003`), and `/api/law/sources.csv` + `_rule_alerts` coverage (`PC-004`). |

## Verdict

* Verdict: Revise
* Rationale: The 3-phase architecture (`zava_forward.core.regulatory_output_guard` wired into `LawStore`, `RuleEngine`, `SourceMonitor`, `agents`/`core` assistants, and `server.py`) is well structured and satisfies package dependency and endpoint-inventory constraints, but four concrete specification defects (`PC-001` through `PC-004`) would cause post-rewrite `output_guard` status clobbering and telemetry miscounts, bypasses or frozen-eval regressions on `answer(bundle)` card activation checks, false positives on negated caveats and draft cards, and missed `/api/law/sources.csv` / `/api/law/alerts*` / `rejected_total` coverage if implemented literally. All four findings are direct planner corrections requiring no user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Multi-layer re-validation of already-rewritten chat replies clobbers `output_guard.passed`, drops or double-counts telemetry, and leaves custom `sections` unsanitized

* Related IDs: Requirement 2, Requirement 3, Research C6, C11, C13, C18, P01-T01, P02-T01, P03-T01, P03-T02
* Evidence: .copilot-tracking/plans/2026-11-15/reg-208-non-advice-guard-plan.md, .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md, .copilot-tracking/research/2026-11-15/reg-208-non-advice-guard-research.md
* Concern: `P02-T01` specifies that `agents/regulatory_chat.py:answer(bundle)` rewrites unsafe prose or unactivated `consultation`/`future_phase` bundles to `ADVISORY_REVIEW_TEXT` and attaches `output_guard` (`passed=False`), then `core/regulatory_chat.py:RegulatoryChat.ask` validates `reply`/`answer` after `self.render(bundle)`, and `P03-T01` validates `reply` and `plain_summary` again in `POST /api/chat/regulatory/threads/{id}/ask` with `app.guard_telemetry`. Because `answer(bundle)` does not hold `app.guard_telemetry` and emits an already-sanitized `reply` (`ADVISORY_REVIEW_TEXT`), re-running the guard downstream on `reply` evaluates `passed=True` -- failing to record `flagged_total` / `rewritten_total` / `by_category` in `app.guard_telemetry`, overwriting `output_guard.passed` from `False` to `True` (while double-counting `checked_total` on clean turns), and leaving nested `sections` prose unsanitized when a custom `render` callback injects unsafe text consumed by `plain_language.py` or thread history reads. In addition, storing `GuardDecision.rewritten_text` inside persisted per-turn `output_guard` dicts duplicates the reply body and risks exceeding `RegulatoryChat` `MAX_CONTENT` (`C6`).
* Impact: HTTP integration tests in `P03-T02` asserting `output_guard.passed is False` and consistent telemetry increments across `/api/chat/regulatory/threads/{id}/ask`, `/api/chat/regulatory/status`, `/api/law/watch`, and `/api/me` will fail or miscount, custom `render` callbacks can leak prohibited claims inside `sections`, and near-limit turns risk `MAX_CONTENT` overflow.
* Smallest useful change: Specify in `P01-T01`, `P02-T01`, and `P03-T01` that: (1) `GuardDecision` provides a compact envelope dict helper (`checked`, `passed`, `action`, `violations`, `guard_version`, omitting `rewritten_text`); (2) `RegulatoryChat.ask` is the single telemetry-recording gate for chat turns -- if `self.render(bundle)` already returned `output_guard` with `passed is False`, `RegulatoryChat.ask` records that upstream violation decision into `self.guard_telemetry` once and preserves `passed=False` while still ensuring `reply`/`answer` and non-quote string fields inside `sections` are sanitized (preserving `SECTION_KEYS` and `cards`), whereas if `render` did not flag the turn, `RegulatoryChat.ask` inspects `reply`/`answer` and non-quote `sections` strings once; and (3) `POST /api/chat/regulatory/threads/{id}/ask` guards only `plain_summary` when added and merges any `plain_summary` failure into the turn's `output_guard` without re-checking `reply` or clobbering a prior `passed=False`.
* Action owner: planning parent
* Exact resolving evidence: Updated `P01-T01`, `P02-T01`, and `P03-T01` detail sections in .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md (and matching task expectations in .copilot-tracking/plans/2026-11-15/reg-208-non-advice-guard-plan.md) defining compact `output_guard` status serialization, upstream failure preservation, `sections` prose sanitization, and single-count telemetry recording across `answer`, `RegulatoryChat.ask`, and `server.py`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Contradictory source/card activation predicate and branch ordering in `P02-T01` either exempts unactivated `in_force`/`guidance` answers or regresses frozen non-answer evaluations

* Related IDs: Requirement 1, Requirement 2, Requirement 3, Research C6, C11, C17, C18, P02-T01, P02-T03
* Evidence: .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md, .copilot-tracking/research/2026-11-15/reg-208-non-advice-guard-research.md
* Concern: In `P02-T01`, the first bullet flags `future_law_applied_as_active` when `bundle["cards"]` lacks an active approved card `"when conflict is False and status is not a synthetic test fixture 'recorded-synthetic-demo' / 'in_force' / 'guidance'"`, while the second bullet states that missing or draft cards (`status="draft"` / `cards=[]` on an `"answer"`) must be caught alongside `"consultation"`, `"future_phase"`, and future `effective > as_of_day`. Literally exempting `"in_force"` and `"guidance"` from the active-card check permits unactivated `in_force`/`guidance` provisions (`cards=[]` or `status="draft"`) to emit `kind="answer"` without human rule activation, breaking `P02-T03` scenario 3. Conversely, running the active-source/card check before `answer(bundle)`'s existing `refusal`, `conflict`, and empty-source `unknown` branches would rewrite frozen non-answer replies (`cards=[]` or conflicting sources) in `src/agents/evals/regulatory_chat_results.json` (`C17`, `C18`).
* Impact: Literal implementation either lets unactivated `in_force`/`guidance` provisions bypass human rule-activation enforcement in `agents/regulatory_chat.py` or breaks `test_regulatory_answers.py` and `test_regulatory_gates.py` against `src/agents/evals/regulatory_chat_results.json`.
* Smallest useful change: Reconcile `P02-T01` in .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md into one exact rule: preserve existing `refusal`, `conflict`, and empty-source `unknown` branches first (validating their rendered prose lexically through `regulatory_output_guard` so frozen evals pass with `output_guard.passed=True`), and apply the contextual activation gate to candidate `kind="answer"` turns by requiring BOTH (a) every cited source has `status in ("in_force", "guidance", "recorded-synthetic-demo")`, `review_status` not `"not_reviewed"`/`"historical"` when present, and `effective is None or effective <= as_of_day`, AND (b) `bundle["cards"]` is non-empty with no card marked inactive or unapproved (`status in ("draft", "retired", "rejected", "superseded")`, `active is False`, or `approved is False`).
* Action owner: planning parent
* Exact resolving evidence: Updated `P02-T01` specification in .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md removing the `"in_force"`/`"guidance"` card-check exemption and explicitly ordering `refusal`/`conflict`/`unknown` branches ahead of candidate `kind="answer"` activation gating.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Contextual `future_law_applied_as_active` matching risks false positives on negated `"future_phase"` caveats, seeded `not_reviewed`/`consultation` watch items, and inactive draft cards

* Related IDs: Requirement 2, Requirement 3, Research C2, C4, C5, C12, P01-T01, P01-T02, P03-T01
* Evidence: .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md, .copilot-tracking/research/2026-11-15/reg-208-non-advice-guard-research.md, docs/reference/regulatory/README.md
* Concern: `P01-T01` triggers contextual `future_law_applied_as_active` whenever metadata has `status in ("consultation", "future_phase")`, `effective > as_of_day`, or `human_rule_activated is False` while text matches phrases such as `"active operational rule"` or structured flags set `active_operational_rule=True` / `active_control=True`. However, `P01-T02`'s own `"future_phase"` caveat (`"Uncommenced future phase, not an active operational rule."`), `ADVISORY_REVIEW_TEXT`, legitimate cited watch summaries for seeded `consultation` and `not_reviewed` snapshots (`docs/reference/regulatory/README.md`), and inactive draft rule cards returned by `GET /api/law/cards*` (`P03-T01`) all evaluate under `human_rule_activated=False` and include negated `"not an active operational rule"` or inactive-status wording. Unless `P01-T01` and `P03-T01` explicitly apply clause-scoped negation to contextual active-rule text patterns (while keeping boolean `active_operational_rule is True` / `active_control is True` unconditionally forbidden under unactivated metadata) and pass each card's actual activation flag on `/api/law/cards*`, legitimate cited non-active items will self-trigger `future_law_applied_as_active`.
* Impact: Legitimate cited watch and compliance summaries for held `consultation`, `future_phase`, `not_reviewed`, or draft-card records would false-positive in `/api/law/watch`, `/api/law/sources`, and `/api/law/cards*`, violating Requirement 3 Scenario 4.
* Smallest useful change: Clarify in `P01-T01`, `P01-T02`, and `P03-T01` that under unactivated/future/consultation metadata (`status in ("consultation", "future_phase")`, `effective > as_of_day`, or `human_rule_activated is False`): (1) structured boolean flags (`active_operational_rule is True` or `active_control is True`) unconditionally fail with `future_law_applied_as_active`; (2) contextual active-rule text patterns apply the same clause-scoped negation filter as lexical patterns so negated statements (`"not an active operational rule"`, `"inactive pending human compliance review"`) pass cleanly; and (3) `/api/law/cards*` passes `active_operational_rule=law.rules.is_active(card_id, today)` (or the card's active control flag) so inactive draft cards pass unless their text affirmatively asserts active operational force.
* Action owner: planning parent
* Exact resolving evidence: Updated `P01-T01`, `P01-T02`, and `P03-T01` rules in .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md distinguishing unconditional boolean-flag enforcement from clause-negated contextual prose and draft-card inspection.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: `/api/law/sources.csv` export, `/api/law/alerts*` subroutes, and `rejected_total` telemetry wiring (`ChatPanel` / `Assistants`) are omitted across `P02-T02` and `P03-T01`

* Related IDs: Requirement 1, Requirement 2, Requirement 3, Research C9, C10, C12, C14, P01-T01, P02-T02, P03-T01
* Evidence: .copilot-tracking/plans/2026-11-15/reg-208-non-advice-guard-plan.md, .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md, .copilot-tracking/research/2026-11-15/reg-208-non-advice-guard-research.md, docs/adrs/0005-regulatory-compliance-assistant.md
* Concern: First, Research `C12` identifies `/api/law/sources.csv` and `/api/law/alerts*` (`_rule_alerts` helper) as active legal/compliance endpoints in `server.py`, and `docs/adrs/0005-regulatory-compliance-assistant.md` mandates identical non-compliance/authority boundaries in exports as in views, yet `P03-T01` lists `/api/law/sources`, `/api/law/sources/{id}`, and `/api/law/alerts` without covering `/api/law/sources.csv` or guarding inside the shared `_rule_alerts` / `_rulecards` builders serving all `/api/law/alerts*` and `/api/law/cards*` routes. Second, the plan's Functional Requirements require `rejected_total` alongside `rewritten_total` in workbench telemetry, but `P02-T02` calls `inspect_regulatory_output(...)` in `ChatPanel._ask` and `assistants.py` without specifying `action="rejected"` recording or `App.guard_telemetry` wiring in `P03-T01`.
* Impact: CSV source exports or case-scoped `/api/law/alerts*` endpoints could bypass the output guard, and `rejected_total` in `/api/law/watch`, `/api/chat/regulatory/status`, and `/api/me` would stay `0` even when `ChatPanel` or `Assistants` withhold/reject unsafe legal-advice or duty-satisfaction outputs.
* Smallest useful change: Update `P01-T01`, `P02-T02`, and `P03-T01` so that: (1) `server.py` enforces `regulatory_output_guard` inside the shared source-list serializer (feeding both `/api/law/sources` and `/api/law/sources.csv`) and inside `_rule_alerts` and `_rulecards` (covering all `/api/law/alerts*` and `/api/law/cards*` endpoints); and (2) `inspect_regulatory_output` / `guard_regulatory_text` accepts `on_violation="rewrite" | "reject"`, with `ChatPanel` and `Assistants` recording `action="rejected"` on optional `guard_telemetry` wired from `App.__init__` (and tested in `P01-T03` / `P03-T02`).
* Action owner: planning parent
* Exact resolving evidence: Updated `P01-T01`, `P02-T02`, and `P03-T01` specifications in .copilot-tracking/plans/2026-11-15/reg-208-non-advice-guard-plan.md and .copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md covering `/api/law/sources.csv`, shared `_rule_alerts`/`_rulecards` helpers, and `on_violation="reject"` telemetry wiring into `App.guard_telemetry`.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Placing the zero-model deterministic guard in `zava_forward.core.regulatory_output_guard` cleanly respects unidirectional package boundaries (`core -> agents -> api`) enforced by `test_dependency_rule.py` (`C15`).
* Contrarian handling of Unicode NFKC, `Cf` format-character stripping, homoglyph folding (`C9`), verbatim active-quote preservation (`C17`), `grade_chat_turn` envelope compatibility (`C18`), and `test_role_endpoint_inventory.py` (`C16`, including `law is None` -> `503` and `Contractor`/`Mystery` -> `403`) directly addresses the codebase's sharpest regression traps.
* Extending `lawstore.STATUSES`, `LawStore._caveats`, and `rule_engine.citation_eligibility` with `"future_phase"` aligns data-layer eligibility with output-layer enforcement.
* Residual risk (explicitly scoped and acceptable): Interactive browser UI rendering of `/api/law/watch` in `src/api/src/zava_forward/api/web/law.js` is deferred as a non-goal because Issue `#208` targets deterministic output validation and JSON API/workbench payload telemetry; existing `web/` files remain untouched.

## Questions or Blocking Evidence Gaps

* None. All four findings are fully resolved by existing codebase evidence (`C1`-`C20`), `docs/adrs/0005-regulatory-compliance-assistant.md`, and confirmed user requirements.

## Limitations

* This critique assessed the supplied research artifact, candidate plan, candidate phase details, and cited repository authority documents (`docs/adrs/0005-regulatory-compliance-assistant.md`, `docs/reference/regulatory/README.md`) without reading live `src/` Python source files directly or running test suites, per the `rpi-plan-critique` read boundary.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: Apply direct planner revisions for `PC-001`, `PC-002`, `PC-003`, and `PC-004` in `.copilot-tracking/plans/2026-11-15/reg-208-non-advice-guard-plan.md` and `.copilot-tracking/details/2026-11-15/reg-208-non-advice-guard-phase-details.md`, record dispositions in `Critique Disposition`, and finalize directly for `rpi-implement` without another critique pass.
* User response required: no
