<!-- markdownlint-disable-file -->
# Research: Child Hardening Pass 14 for Issue #216 (`RV-034`..`RV-037`)

* Task ID: `216-citation-eval-2142-c14`
* Parent Task ID: `216-citation-eval-2142-c13`
* Date: `2026-11-14`
* Output Mode: `convergence`
* Research Posture: `focused` (provenance: bounded `src/core` defect set `RV-034`..`RV-037` from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c13-review.md`)
* Research Disposition: `executed`
* Planning Readiness: `Ready`

## Research Brief

* Topic: Close `RV-034`..`RV-037` in `src/core` for Issue #216 citation validity, refusal accuracy, and paired rule-card comparison gates.
* Scope: `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md`.
* Non-Goals: Edits outside `src/core` (`src/api`, `src/agents`), breaking `#214` `RegulatoryChat.ask()` unit tests when `enforce_ship_gate=False`, or setting any hardcoded price/budget target while `BRD OD-51` is open.
* Initial Questions:
  1. `Q1` (`RV-034`): How do progressive/participle and modal compliance questions (`"Is this damp home meeting its legal obligations?"`) bypass `_REFUSAL_PATTERNS[1]`, and how do we expand coverage without ReDoS or false refusals?
  2. `Q2` (`RV-035`): What exact `source_freshness["label"]` strings does `source_monitor.card_freshness` produce for `"in_cadence"`, `"out_of_cadence"`, and `"unknown"`, and where must 3-way parity be enforced?
  3. `Q3` (`RV-036`): How should `agreed_on` temporal ordering and non-synthetic paired-observation guards be enforced across `agreement_gaps`, `_validate_benefit_thresholds`, `_compute_cost_per_accepted_check`, and `_score_paired_observations`?
  4. `Q4` (`RV-037`): Why did rounded unit-cost comparison reject valid exact sub-ceiling costs, and how can `RegulatoryChat` expose opt-in instance-level ship-gating on `ask()` and `surface()` without breaking `#214` tests?

## Extension Registry and Participation

* Repository instructions (`.github/copilot-instructions.md`): Selected (enforces `src/core` tests, `mypy`, `ruff`, no `.copilot-tracking/` leaks in `src/core`).
* Specialist subagents: Inline execution selected for all three waves because all target code lives in 4 already-indexed `src/core` files (`<300` relevant lines).

## Cycle 1 Execution (Wider, Deeper, Contrarian)

### Wave 1: Wider

* Scanned `source_monitor.py`, `regulatory_eval_gates.py`, `regulatory_chat.py`, `test_regulatory_chat.py`, and `test_regulatory_eval_gates_216.py` to map every call site touching refusal patterns, freshness labels, `agreed_on` dates, paired-trial observation scoring, unit-cost ceiling checks, and `RegulatoryChat` entry points.

### Wave 2: Deeper

* `C1` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:143-181`): `_REFUSAL_PATTERNS[1]`'s obligation-satisfaction branch matches `(?:do|does|did|has|have)\b[^.;!?]{0,40}\b(?:met|meet|satisfy|satisfied)` + obligation nouns, omitting auxiliary `is|are|was|were|will|would|can|could|should` and progressive participles `meeting` / `satisfying`, and the subject-adjective branch matches only `is|are` (omitting `was|were|will|would|can|could|should` + `be`).
* `C2` (`src/core/src/zava_forward/core/source_monitor.py:117-124`, `src/core/src/zava_forward/core/regulatory_eval_gates.py:856-910`, `1475-1520`): `source_monitor.card_freshness` emits exact canonical labels (`"out_of_cadence"`: `"Source out of monitoring cadence; ask the named owner."`, `"unknown"`: `"Source monitoring cadence unknown; ask the named owner."`, `"in_cadence"`: `"Within monitoring cadence; not proof of legal currentness."`), whereas `_card_provenance_valid` only checked `(fresh_label == OUT_OF_CADENCE_LABEL) == (fresh_status == "out_of_cadence")` and `_active_bundle_nonconflicting` omitted label parity.
* `C3` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:2195-2210`, `2545-2555`, `2790-2805`, `3335-3430`, `3985-4015`): `agreed_on` in `agreement_gaps`, `_validate_benefit_thresholds`, and `_compute_cost_per_accepted_check` (`accepted_definition.agreed_on`) only checked `_valid_iso_day`, accepting `"9999-12-31"`; `_score_paired_observations` also accepted observation rows flagged `"synthetic": True` / `"simulated": True` or lacking pre-agreement / post-evaluation bounds on optional `observed_at` / `recorded_at`.
* `C4` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:4054-4065`): `within_unit_ceiling` checked both `exact_unit_cost <= agreed_unit_ceiling` and `reported_unit_cost <= agreed_unit_ceiling`, causing exact unit cost `0.0080006` (`round(..., 6) == 0.008001`) to fail under ceiling `0.0080007`.
* `C5` (`src/core/src/zava_forward/core/regulatory_chat.py:55-65`, `362-375`, `462-503`): `RegulatoryChat.__init__` can accept keyword-only `*, ship_gate_comparison: Mapping[str, Any] | None = None, enforce_ship_gate: bool = False`, defaulting `surface()`'s `comparison` to `self.ship_gate_comparison` when `comparison is None` and enforcing `_verify_comparison_evidence(self.ship_gate_comparison)` at the top of `ask()` when `enforce_ship_gate=True` (raising `ChatForbidden` when unverified), preserving existing `#214` behavior when `enforce_ship_gate=False`.
* `C6` (`src/core/tests/test_regulatory_eval_gates_216.py:894-925`, `1178-1190`, `3005-3015`): Inline test fixtures `multi_bundle`, `unmapped_bundle`, and `valid_unknown_bundle` use non-canonical shorthand freshness labels and must use `IN_CADENCE_LABEL` and `UNKNOWN_CADENCE_LABEL` once 3-way label parity is enforced.

### Wave 3: Contrarian

* Tested whether requiring `observed_at` on every paired observation row would break existing callers: existing `_valid_observations` and unit tests omit `observed_at`, so `observed_at` / `recorded_at` should be validated strictly whenever present (`agreed_on <= obs_day <= eval_day`), while `thresholds["agreed_on"] <= eval_day`, `accepted_definition["agreed_on"] <= eval_day`, and `agreement["agreed_on"] <= min_case_as_of_day` (and `<= eval_day` in `compare_chat_against_rule_cards`) unconditionally block post-dated agreements such as `"9999-12-31"` even when `observed_at` is omitted.
* Tested whether unconditionally blocking `RegulatoryChat.ask()` without `enforce_ship_gate=True` would break `#214` regression tests: `src/core/tests/test_regulatory_chat.py` has 25 tests calling `RegulatoryChat(...).ask(...)` directly without a comparison report, confirming `enforce_ship_gate: bool = False` (opt-in on `ask()`, always fail-closed on `surface()`) is the exact non-breaking design inside `src/core`.

## Parent Synthesis and Decisions

* Selected converged approach:
  1. Expand `_REFUSAL_PATTERNS[1]` with progressive participles (`meeting`, `satisfying`) and full modal/auxiliary sets (`C1`).
  2. Export `IN_CADENCE_LABEL` and `UNKNOWN_CADENCE_LABEL` alongside `OUT_OF_CADENCE_LABEL` and enforce exact 3-way `_FRESHNESS_LABELS` parity in `_card_provenance_valid` and `_active_bundle_nonconflicting` (`C2`, `C6`).
  3. Bound `agreed_on` against `min_case_as_of_day` / `eval_day` across `agreement_gaps`, `_validate_benefit_thresholds`, `_compute_cost_per_accepted_check`, and `compare_chat_against_rule_cards`, validate optional `observed_at` / `recorded_at` on observation rows, and reject observation rows marked `synthetic` / `simulated` (`C3`).
  4. Compare `exact_unit_cost <= agreed_unit_ceiling` directly without the false-negative rounded check (`C4`), and add keyword-only `ship_gate_comparison` + `enforce_ship_gate` to `RegulatoryChat` (`C5`).
* Further research needed: None (`Planning Readiness: Ready`).
