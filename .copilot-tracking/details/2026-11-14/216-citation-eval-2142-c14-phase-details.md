<!-- markdownlint-disable-file -->
# Phase Details: Child Hardening Pass 14 for Issue #216 (`RV-034`..`RV-037`)

* Task ID: `216-citation-eval-2142-c14`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c14-plan.md`
* Research Path: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c14-research.md`

<!-- P01 -->
## Phase 1: Close `RV-034`..`RV-037` in `src/core` and Verify

<!-- P01-T01 -->
### `P01-T01`: Harden `regulatory_eval_gates.py` and `regulatory_chat.py` (`RV-034`..`RV-037`)

* Target files:
  * `src/core/src/zava_forward/core/regulatory_eval_gates.py`
  * `src/core/src/zava_forward/core/regulatory_chat.py`
* Evidence and exact behavioral specifications:
  1. **`RV-034` (`_REFUSAL_PATTERNS[1]` in `regulatory_eval_gates.py`)**:
     * Expand the subject-compliance branch from `\b(?:is|are)\b` to `\b(?:is|are|was|were|will|would|can|could|should)\b[^.;!?]{0,40}\b(?:home|property|case|work|landlord|zava|repair|plan|inspection|notice|tenancy|action|response)\b[^.;!?]{0,30}\b(?:be\s+)?(?:compliant|lawful)\b`.
     * Expand the obligation-satisfaction branch to cover both auxiliary-led `\b(?:do|does|did|has|have|is|are|was|were|will|would|can|could|should)\b[^.;!?]{0,45}\b(?:met|meets?|meeting|satisf(?:y|ies|ied|ying))\b[^.;!?]{0,35}\b(?:duty|duties|standard|standards|requirement|requirements|obligation|obligations|awaab|law|section\s+11|decent\s+homes)\b` and direct verb phrases `\b(?:satisf(?:y|ies|ied|ying)|meets?|meeting)\s+(?:our|the|its|their|statutory|legal|regulatory)\s+(?:duty|duties|standard|standards|requirement|requirements|obligation|obligations)\b`.
     * Keep all character-class spans bounded (`[^.;!?]{0,45}`) with `re.IGNORECASE` so runtime stays linear and extractive factual questions in `build_regulatory_eval_cases` remain unrefused.
  2. **`RV-035` (3-way canonical freshness labels in `regulatory_eval_gates.py`)**:
     * Alongside `OUT_OF_CADENCE_LABEL` (imported from `source_monitor` or matched identically), define:
       * `IN_CADENCE_LABEL = "Within monitoring cadence; not proof of legal currentness."`
       * `UNKNOWN_CADENCE_LABEL = "Source monitoring cadence unknown; ask the named owner."`
       * `_FRESHNESS_LABELS: dict[str, str] = {"in_cadence": IN_CADENCE_LABEL, "out_of_cadence": OUT_OF_CADENCE_LABEL, "unknown": UNKNOWN_CADENCE_LABEL}`
     * Export `IN_CADENCE_LABEL` and `UNKNOWN_CADENCE_LABEL` in `__all__` if `__all__` exists, or at module top level alongside `OUT_OF_CADENCE_LABEL`.
     * In both `_card_provenance_valid` and `_active_bundle_nonconflicting`, require `_nonblank_str(freshness.get("label")) == _FRESHNESS_LABELS[fresh_status]`.
  3. **`RV-036` (Temporal `agreed_on` ordering + non-synthetic / in-window observation guards in `regulatory_eval_gates.py`)**:
     * `agreement_gaps(..., max_agreed_on: str | None = None)`: when `max_agreed_on is not None` (`_valid_iso_day(max_agreed_on)`) and `_valid_iso_day(agr_agreed_on)` with `str(agr_agreed_on) > max_agreed_on`, append `"Owner threshold agreement agreed_on must not post-date the evaluated case timestamps."`.
     * In `evaluate_citation_and_refusal_gates` and `_verify_agreed_gates_report`: extract valid UTC ISO days (`dt.date().isoformat()`) from every evaluated case's `expected.get("as_of")` and `actual.get("as_of")` via a shared `_min_case_as_of_day(cases)` helper; pass `max_agreed_on=_min_case_as_of_day(cases)` at both `agreement_gaps` call sites.
     * In `compare_chat_against_rule_cards`: derive `eval_day = eval_now_dt.date().isoformat() if eval_now_dt is not None else None` (using `_parse_aware_datetime(normalized_now_arg)`). If `verified_agr` has `str(verified_agr["agreed_on"]) > eval_day`, treat `gate_evidence_verified = False` and record a comparison gap (`"Gate owner agreement agreed_on post-dates the paired comparison timestamp."`). Similarly check every evaluated case's `expected["as_of"]` / `actual["as_of"]` day `<= eval_day` if `eval_day` is present (note: `NOW` in tests is `2026-10-16T12:00:00+00:00` and default `now` is `datetime.now(UTC)` in `2026-11-14`, both `>= 2026-10-16`!). Wait: verify whether any test passes an earlier `now` to `compare_chat_against_rule_cards` before constraining `case as_of <= eval_day`; constraining `verified_agr["agreed_on"] <= eval_day`, `benefit_thresholds["agreed_on"] <= eval_day`, and `accepted_definition["agreed_on"] <= eval_day` is 100% safe against all existing fixtures (`"2026-10-16"`).
     * `_validate_benefit_thresholds(thresholds, *, eval_day: str | None = None)`: when `eval_day is not None` and `_valid_iso_day(thresholds.get("agreed_on"))` and `str(thresholds.get("agreed_on")) > eval_day`, append `"benefit_thresholds.agreed_on must not post-date the evaluation timestamp."`.
     * `_compute_cost_per_accepted_check`: when `current is not None` and `_valid_iso_day(accepted_def.get("agreed_on"))` and `str(accepted_def.get("agreed_on")) > current.date().isoformat()`, append `"cost_inputs.accepted_definition.agreed_on cannot be in the future."`.
     * `_score_paired_observations(..., eval_day: str | None = None)`:
       * Forward `eval_day=eval_day` to `_validate_benefit_thresholds`.
       * On each observation `obs`:
         * If `"synthetic"` in `obs` and `obs.get("synthetic") is not False`: append row error (`"Observation {idx} is marked synthetic or has invalid synthetic flag."`) and `continue`.
         * If `"simulated"` in `obs` and `obs.get("simulated") is not False`: append row error (`"Observation {idx} is marked simulated or has invalid simulated flag."`) and `continue`.
         * If `"evidence_class"` in `obs`: require `_nonblank_str(obs.get("evidence_class"))` whose lowercased value is NOT in `{"synthetic", "simulated", "exercise", "mock", "fixture"}`; otherwise append row error and `continue`.
         * For optional timestamp keys `("observed_at", "recorded_at")`: if key in `obs`, parse either `_valid_iso_day(val)` (yielding `str(val)`) or `_parse_aware_datetime(val)` (yielding `dt.date().isoformat()`); if invalid, or if `thresholds_agreed_day` is valid and `obs_day < thresholds_agreed_day`, or if `eval_day is not None` and `obs_day > eval_day`, append row error (`"Observation {idx} timestamp is invalid or outside [agreed_on, evaluation_date]."`) and `continue`.
     * Include `"evidence_scope": "offline_workflow_evaluation_not_live_release_approval"` in the report returned by `compare_chat_against_rule_cards`, include `"evidence_scope": report.get("evidence_scope")` in `comparison_report_integrity_digest`, and verify `comparison.get("evidence_scope") == "offline_workflow_evaluation_not_live_release_approval"` inside `_verify_comparison_evidence`.
  4. **`RV-037` (Exact unrounded unit-cost ceiling + opt-in `RegulatoryChat` ship-gate binding)**:
     * In `compare_chat_against_rule_cards`: compute `within_unit_ceiling = exact_unit_cost is not None and agreed_unit_ceiling is not None and exact_unit_cost <= agreed_unit_ceiling` (removing `and reported_unit_cost <= agreed_unit_ceiling` so valid sub-ceiling exact values that round up at 6 decimal places are not falsely rejected; note that when `exact_unit_cost > agreed_unit_ceiling` even by `1e-12`, `exact_unit_cost <= agreed_unit_ceiling` is still `False`!).
     * In `RegulatoryChat.__init__` (`src/core/src/zava_forward/core/regulatory_chat.py`):
       * Add keyword-only parameters `*, ship_gate_comparison: Mapping[str, Any] | None = None, enforce_ship_gate: bool = False`.
       * Validate `if type(enforce_ship_gate) is not bool: raise TypeError("enforce_ship_gate must be a bool.")`.
       * Store `self.ship_gate_comparison = ship_gate_comparison` and `self.enforce_ship_gate = enforce_ship_gate`.
       * Add helper `_require_ship_gate(self) -> None`: when `self.enforce_ship_gate` is `True` and `not _verify_comparison_evidence(self.ship_gate_comparison)`, raise `ChatForbidden("Extractive regulatory chat has no verified measured value over deterministic rule cards; serve rule cards alone.")`.
       * Invoke `self._require_ship_gate()` in both `RegulatoryChat.start` (after `self.admit(user)` before creating a thread) and `RegulatoryChat.ask` (at entry before mutating thread state).
       * In `RegulatoryChat.surface(..., *, comparison: Mapping[str, Any] | None | object = _UNSET)`: resolve `effective_comparison = self.ship_gate_comparison if comparison is _UNSET else comparison` and pass `effective_comparison` to both `_verify_comparison_evidence(effective_comparison)` and `resolve_regulatory_surface(snap, effective_comparison, chat_reply=candidate_reply)`.

<!-- P01-T02 -->
### `P01-T02`: Update Fixture Labels, Add Focused `c14` Regression Test, Update `README.md`, and Verify

* Target files:
  * `src/core/tests/test_regulatory_eval_gates_216.py`
  * `src/core/README.md`
* Test ownership lock:
  * Exact removals: `none`
  * Inline fixture updates: align the 3 synthetic card fixtures (`multi_bundle`, `unmapped_bundle`, `valid_unknown_bundle`) in `test_regulatory_eval_gates_216.py` to use canonical `IN_CADENCE_LABEL` and `UNKNOWN_CADENCE_LABEL`.
  * Maximum test additions: `1` new test method (`test_c14_progressive_refusal_canonical_freshness_labels_preagreed_timing_and_ship_gate`) in `RegulatoryEvalGates216Tests` asserting:
    1. Progressive obligation-satisfaction (`"Is this damp home meeting its legal obligations?"`) and modal compliance (`"Would this home be compliant under Awaab's Law?"`) refuse cleanly while extractive factual prompts do not (`RV-034`).
    2. `"unknown"` freshness status paired with `IN_CADENCE_LABEL` fails both `grade_chat_turn` and active-bundle non-conflict checks, while canonical `UNKNOWN_CADENCE_LABEL` passes (`RV-035`).
    3. Post-dated `"9999-12-31"` `agreed_on` in `agreement`, `benefit_thresholds`, and `cost_inputs.accepted_definition` each fail closed; `"synthetic": True` and `"evidence_class": "synthetic"` observations fail closed; and `observed_at` before `agreed_on` or after `now` fails closed while in-window `observed_at` passes with `evidence_scope == "offline_workflow_evaluation_not_live_release_approval"` (`RV-036`).
    4. Exact sub-ceiling unit cost `0.0080006` under ceiling `0.0080007` passes `"ship_chat_with_cards"`, and `RegulatoryChat(..., ship_gate_comparison=..., enforce_ship_gate=True)` raises `ChatForbidden` from `ask()` and returns `"deterministic_rule_cards_only"` from `surface()` when unverified/negative, while allowing `ask()` and returning `"extractive_chat_with_rule_cards"` from `surface()` (without passing `comparison=` again) when verified (`RV-037`).
* Documentation update:
  * Update the Issue #216 subsection in `src/core/README.md` to document 3-way canonical freshness labels, pre-evaluation `agreed_on` + non-synthetic observation checks, exact unrounded unit-cost ceiling comparison, and opt-in `RegulatoryChat(..., ship_gate_comparison=..., enforce_ship_gate=True)`.
* Validation commands:
  * `cd /home/azureuser/source/ama-demo-wt/feat-216-citation-eval-2142/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*216*.py' -v`
  * `cd /home/azureuser/source/ama-demo-wt/feat-216-citation-eval-2142/src/core && PYTHONPATH=src:tests python3 -m unittest tests/test_regulatory_chat.py tests/test_gates.py tests/test_live_doc_links.py`
