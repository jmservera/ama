<!-- markdownlint-disable-file -->
# Implementation Plan: Child Hardening Pass 14 for Issue #216 (`RV-034`..`RV-037`)

* Task ID: `216-citation-eval-2142-c14`
* Parent Task ID: `216-citation-eval-2142-c13`
* Date: `2026-11-14`
* Status: `Approved`

## Executive Summary

Close the four remaining `src/core` findings (`RV-034`..`RV-037`) from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c13-review.md` so Issue #216's citation validity, refusal accuracy, and paired rule-card comparison gates are airtight within `src/core`:

1. Expand `_REFUSAL_PATTERNS[1]` in `regulatory_eval_gates.py` to refuse progressive/participle obligation-satisfaction questions (such as `"Is this damp home meeting its legal obligations?"`) and full modal/auxiliary subject-compliance questions (`is|are|was|were|will|would|can|could|should`) without ReDoS or false refusals (`RV-034`).
2. Export `IN_CADENCE_LABEL` and `UNKNOWN_CADENCE_LABEL` alongside `OUT_OF_CADENCE_LABEL` and enforce exact 3-way `source_freshness["label"]` parity with `source_monitor.card_freshness` in both `_card_provenance_valid` and `_active_bundle_nonconflicting` (`RV-035`).
3. Enforce pre-evaluation temporal bounds on `agreed_on` across `agreement_gaps` (`<= min_case_as_of_day` in `evaluate_citation_and_refusal_gates` and `<= eval_day` in `compare_chat_against_rule_cards`), `_validate_benefit_thresholds` (`<= eval_day`), and `_compute_cost_per_accepted_check` (`accepted_definition.agreed_on <= eval_day`), reject paired observations flagged as synthetic/simulated/exercise, validate optional observation `observed_at` / `recorded_at` timestamps (`thresholds_agreed_on <= obs_day <= eval_day`), and include explicit `evidence_scope` metadata in `compare_chat_against_rule_cards` (`RV-036`).
4. Compare exact unrounded `exact_unit_cost <= agreed_unit_ceiling` in `compare_chat_against_rule_cards` and add opt-in keyword-only `ship_gate_comparison` and `enforce_ship_gate: bool = False` to `RegulatoryChat` so `ask()` fails closed with `ChatForbidden` when `enforce_ship_gate=True` and comparison evidence is unverified while `surface()` automatically uses `self.ship_gate_comparison` unless overridden (`RV-037`).

## Sources

* `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c14-research.md`
* `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c13-review.md`
* `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* `src/core/src/zava_forward/core/regulatory_chat.py`
* `src/core/src/zava_forward/core/source_monitor.py`
* `src/core/tests/test_regulatory_eval_gates_216.py`
* `src/core/README.md`

## User Decisions and Requirements

* Deliver the remaining locally verifiable acceptance criteria for Issue #216 strictly inside `src/core`:
  1. Citation validity and refusal accuracy gates set with owners and measured on a graded and adversarial set.
  2. Paired comparison reports value of chat over deterministic cards with links; if no measured value, ship cards alone.
* Preserve `BRD OD-51` (open unit-cost/budget target): keep `benefit_thresholds=None` by default and never invent a hardcoded GBP ceiling in production defaults.
* Preserve backwards compatibility for existing `#214` unit tests in `src/core/tests/test_regulatory_chat.py`.
* Validate in `src/core` using bare `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`, and commit cleanly without pushing.

## Goals

* Eliminate progressive/modal compliance refusal bypasses in `_REFUSAL_PATTERNS[1]` (`RV-034`).
* Guarantee 3-way canonical freshness label parity across `"in_cadence"`, `"out_of_cadence"`, and `"unknown"` (`RV-035`).
* Block post-dated `agreed_on` records and synthetic/out-of-window paired trial rows fail-closed (`RV-036`).
* Eliminate 6-decimal rounding false negatives at the unit-cost ceiling boundary and support instance-bound `RegulatoryChat` ship gating across both `ask()` and `surface()` (`RV-037`).

## Scope and Non-Goals

* Scope:
  * `src/core/src/zava_forward/core/regulatory_eval_gates.py`
  * `src/core/src/zava_forward/core/regulatory_chat.py`
  * `src/core/tests/test_regulatory_eval_gates_216.py`
  * `src/core/README.md`
* Non-Goals:
  * Modifying `src/api` or `src/agents` (outside the caller's `src/core` boundary; tracked in `## Follow-Up Items`).
  * Removing existing tests (`none` removals; max `1` new test method in `test_regulatory_eval_gates_216.py` plus aligning 3 synthetic inline label fixtures to canonical `source_monitor` strings).

## Functional Requirements

* `FR-1` (`RV-034`): `_REFUSAL_PATTERNS[1]` must refuse obligation-satisfaction questions framed with auxiliary `do|does|did|has|have|is|are|was|were|will|would|can|could|should` and base/inflected/progressive verbs `met|meets?|meeting|satisf(?:y|ies|ied|ying)` (including `"Is this damp home meeting its legal obligations?"`) as well as modal subject-compliance questions (`is|are|was|were|will|would|can|could|should` + subject + `(?:be\s+)?(?:compliant|lawful)`), without refusing extractive factual provision/deadline/card-status questions.
* `FR-2` (`RV-035`): Define `IN_CADENCE_LABEL = "Within monitoring cadence; not proof of legal currentness."`, `UNKNOWN_CADENCE_LABEL = "Source monitoring cadence unknown; ask the named owner."`, and `_FRESHNESS_LABELS`, and require `freshness.get("label") == _FRESHNESS_LABELS[fresh_status]` in both `_card_provenance_valid` and `_active_bundle_nonconflicting`.
* `FR-3` (`RV-036`):
  * `agreement_gaps` accepts optional `max_agreed_on: str | None = None` and rejects agreements whose `agreed_on > max_agreed_on`; `evaluate_citation_and_refusal_gates` passes the earliest valid UTC day across evaluated cases' `expected["as_of"]` / `actual["as_of"]`, and `compare_chat_against_rule_cards` additionally rejects `verified_agreement["agreed_on"] > eval_day`.
  * `_validate_benefit_thresholds` accepts optional `eval_day: str | None = None` and rejects `benefit_thresholds["agreed_on"] > eval_day`.
  * `_compute_cost_per_accepted_check` rejects `accepted_definition["agreed_on"] > current.date().isoformat()` when `current` is valid.
  * `_score_paired_observations` rejects any observation row with `"synthetic": True`, `"simulated": True`, non-`bool` `"synthetic"`/`"simulated"` when present, or `"evidence_class"` in `{"synthetic", "simulated", "exercise"}` (or non-string/blank `"evidence_class"` when present), validates optional `"observed_at"` / `"recorded_at"` (`thresholds_agreed_on <= obs_day <= eval_day` when valid thresholds and `eval_day` are available), and `compare_chat_against_rule_cards` includes `"evidence_scope": "offline_workflow_evaluation_not_live_release_approval"` (hashed in `comparison_report_integrity_digest` and verified in `_verify_comparison_evidence`).
* `FR-4` (`RV-037`):
  * `compare_chat_against_rule_cards` evaluates `within_unit_ceiling = exact_unit_cost <= agreed_unit_ceiling` using exact unrounded float arithmetic.
  * `RegulatoryChat.__init__` accepts keyword-only `*, ship_gate_comparison: Mapping[str, Any] | None = None, enforce_ship_gate: bool = False` (rejecting non-`bool` `enforce_ship_gate` with `TypeError`), `start()` and `ask()` raise `ChatForbidden` via `_require_ship_gate()` before creating threads, rendering, or mutating thread state when `self.enforce_ship_gate` is `True` and `not _verify_comparison_evidence(self.ship_gate_comparison)`, and `surface(..., *, comparison=_UNSET)` resolves `effective_comparison = self.ship_gate_comparison if comparison is _UNSET else comparison` and forwards `effective_comparison` to both `_verify_comparison_evidence` and `resolve_regulatory_surface`.

## Non-Functional Requirements

* `NFR-1`: All regex additions in `_REFUSAL_PATTERNS[1]` use bounded negated character classes (`[^.;!?]{0,45}`) with linear worst-case runtime (no nested unbounded quantifiers).
* `NFR-2`: Zero `mypy` errors across all `src/core` files, clean `ruff check .` and `ruff format --check .`, zero `.copilot-tracking/` path mentions in `src/core`, and 100% pass rate on `test_regulatory_eval_gates_216.py` plus companion `src/core` suites (`test_regulatory_chat.py`, `test_gates.py`, `test_live_doc_links.py`).

## Acceptance Criteria

* `AC-1`: `"Is this damp home meeting its legal obligations?"` and `"Would this home be compliant under Awaab's Law?"` return the compliance-determination refusal from `refuse_question`, while all graded extractive questions in `build_regulatory_eval_cases` remain unrefused.
* `AC-2`: Cards with `"status": "unknown"` and `IN_CADENCE_LABEL` (or any non-canonical freshness label) fail `_card_provenance_valid` and `_active_bundle_nonconflicting`.
* `AC-3`: Post-dated `agreed_on` (`"9999-12-31"`) in `agreement`, `benefit_thresholds`, or `cost_inputs.accepted_definition`, synthetic-flagged observations (`"synthetic": True` or `"evidence_class": "synthetic"`), and pre-agreement / post-evaluation observation `observed_at` timestamps all fail closed (`UNKNOWN`/`FAIL` gates or `recommendation == "ship_cards_only"`, `cards_alone is True`).
* `AC-4`: Exact unit cost `0.0080006` under `max_ai_cost_per_accepted_check_gbp = 0.0080007` passes the unit-cost ceiling check, and `RegulatoryChat(..., ship_gate_comparison=..., enforce_ship_gate=True)` blocks `start()` and `ask()` with `ChatForbidden` when `ship_gate_comparison` recommends `"ship_cards_only"` while allowing `start()`/`ask()` and returning `"extractive_chat_with_rule_cards"` on `surface()` when `ship_gate_comparison` is verified `"ship_chat_with_cards"`.

## Critique Disposition

* Critique artifact: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c14-plan-critique.md` (`Complete`, `Revise` -> applied in one batch, finalized without repeating critique).
* `PC-001` (`Medium`, `planner`): Applied directly — `_require_ship_gate()` guards both `RegulatoryChat.start()` and `RegulatoryChat.ask()` when `enforce_ship_gate=True`, and `RegulatoryChat.surface()` uses a module-private `_UNSET` sentinel and passes `effective_comparison` to both `_verify_comparison_evidence` and `resolve_regulatory_surface`.
* `PC-002` (`Medium`, `planner`): Applied directly — `_min_case_as_of_day(cases)` feeds `max_agreed_on` in both `evaluate_citation_and_refusal_gates` and `_verify_agreed_gates_report`.
* `PC-003` (`Low`, `planner`): Applied directly — `AC-3` and `AC-4` use the exact `recommendation == "ship_cards_only"` (`cards_alone is True`) vocabulary.

## Phase Checklist

<!-- P01 -->
### Phase 1: Close `RV-034`..`RV-037` in `src/core` and Verify

* [x] `P01`: Implement `RV-034`..`RV-037` across `regulatory_eval_gates.py`, `regulatory_chat.py`, `test_regulatory_eval_gates_216.py`, and `src/core/README.md`, and pass full `src/core` static and unit validation.
  <!-- P01-T01 -->
  * [x] `P01-T01`: Implement progressive/modal refusal coverage (`RV-034`), 3-way canonical freshness label parity (`RV-035`), pre-evaluation `agreed_on` + non-synthetic observation guards (`RV-036`), and exact unit-cost ceiling comparison (`RV-037`) in `src/core/src/zava_forward/core/regulatory_eval_gates.py`, plus opt-in `ship_gate_comparison` / `enforce_ship_gate` in `src/core/src/zava_forward/core/regulatory_chat.py`.
  <!-- P01-T02 -->
  * [x] `P01-T02`: Align the 3 synthetic inline freshness labels and add `test_c14_progressive_refusal_canonical_freshness_labels_preagreed_timing_and_ship_gate` in `src/core/tests/test_regulatory_eval_gates_216.py`, update `src/core/README.md`, and run `mypy`, `ruff check .`, `ruff format --check .`, Issue #216 tests, and companion `src/core` tests.

## Follow-Up Items

* Wire `src/api/src/zava_forward/api/server.py` and `src/agents/src/zava_forward/agents/regulatory_chat.py` to pass verified `ship_gate_comparison` / `enforce_ship_gate=True` once a multi-package integration branch outside `src/core` is requested.
* Replace caller-supplied `max_ai_cost_per_accepted_check_gbp` fixture values with ratified finance policy figures once `BRD OD-51` is closed by Zava North Homes Finance and Compliance owners.
