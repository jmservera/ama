# Phase Details: Child Hardening Pass 13 for Issue #216 (`216-citation-eval-2142-c13`)

* Task ID: `216-citation-eval-2142-c13`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c13-plan.md`
* Research Path: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c13-research.md`

<!-- P01 -->
## Phase P01: Harden Provenance Substantiation, Refusal Paraphrases, Dual-Owner Agreement, and Unit-Cost Ceiling (`src/core`)

* Dependencies: Prior `c12` implementation on branch `feat/ai-216-citation-eval-2142`; findings `RV-030`..`RV-033` in `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c12-review.md`.
* Write Boundary: `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md`.

<!-- P01-T01 -->
### Task P01-T01: Implement `RV-030`..`RV-033` in `src/core/src/zava_forward/core/regulatory_eval_gates.py`

* Evidence: `C1`..`C6` in `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c13-research.md`; critique dispositions `PC-001`..`PC-004` in `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c13-plan-critique.md`.
* Required Behavior:
  1. `RV-030` + `PC-001` (`_card_provenance_valid` and `_active_bundle_nonconflicting(..., *, as_of_day: str | None = None)`):
     * Update `_active_bundle_nonconflicting` to accept `*, as_of_day: str | None = None` and pass `as_of_day=as_of_day` from `_inspect_bundle_surface` and `grade_chat_turn` (keep `clock = _nonblank_str(card.get("clock"))` strictly for `(safe_default, clock)` workflow signature consistency).
     * Extract a shared constituent-entry validator helper `_freshness_entry_valid(entry, *, fresh_as_of_day, as_of_day, require_active) -> tuple[str, str, str | None, int | None, str | None] | None` returning `(sid, est, ls_val, cd_int, due_val)` on valid entries or `None` on invalid entries:
       * Require `sid` to be a non-blank trimmed UTF-8 string and `"status"` to be present with `est = _nonblank_str(entry.get("status"))` in `_FRESHNESS_STATUSES`.
       * Validate optional `entry["as_of"]` day (`entry_as_of_day = _extract_day(entry.get("as_of"))`, matching `fresh_as_of_day` when present and matching `as_of_day` when `require_active and as_of_day is not None`). Set `ref_day = as_of_day if (require_active and as_of_day is not None) else (as_of_day or entry_as_of_day or fresh_as_of_day)`.
       * When `est in ("in_cadence", "out_of_cadence")`: require `"last_success"`, `"cadence_days"`, and `"due_on"` in `entry`; require `_valid_iso_day(ls_val)` and `_valid_iso_day(due_val)` (`isinstance(..., str)` and `due_val > ls_val`), `cd_int = _strict_int(entry.get("cadence_days"))` in `1..36600` (rejecting `bool`), and `(date.fromisoformat(ls_val) + timedelta(days=cd_int)).isoformat() == due_val` (catching `OverflowError`). Whenever `ref_day is not None`, require `ls_val <= ref_day`, `ref_day < due_val` when `est == "in_cadence"`, and `ref_day >= due_val` when `est == "out_of_cadence"`.
       * When `est == "unknown"`: if `"due_on"` in `entry` and `entry.get("due_on") is not None`, return `None`; if `"last_success"` in `entry` and `entry.get("last_success") is not None`, return `None`; if `"cadence_days"` in `entry` and `entry.get("cadence_days") is not None`, require `cd_int = _strict_int(entry.get("cadence_days"))` in `1..36600` (else `cd_int = None`).
     * In both `_card_provenance_valid` and `_active_bundle_nonconflicting`, verify card-level `fresh_status` equals the exact constituent rollup (`"out_of_cadence"` if `"out_of_cadence"` in `entry_statuses`, else `"in_cadence"` if all `s == "in_cadence"`, else `"unknown"`), and in `_active_bundle_nonconflicting` compare `(est, ls_val, cd_int, due_val)` across cards sharing `sid` after `_strict_int` validation.
  2. `RV-031` + `PC-004` (`_REFUSAL_PATTERNS[1]`):
     * Use bounded single-clause `[^.;!?]{0,40}` spans (no `.*` chains), Unicode hyphen/dash support `[-\u2010-\u2015\u2212\s]*`, singular/plural subjects `(?:propert(?:y|ies)|homes?|dwellings?|flats?|houses?|buildings?|blocks?|cases?|tenanc(?:y|ies)|landlords?|repairs?|works?)`, and obligation-qualified `meet`/`satisfy` to match:
       * `\b(?:is|are)\b[^.;!?]{0,30}\b<subject>\b[^.;!?]{0,40}\b(?:compliant|in\s+compliance|non[-\u2010-\u2015\u2212\s]*compliant|lawful|unlawful)\b`
       * `\b<subject>\b[^.;!?]{0,30}\b(?:is|are)\s+(?:not\s+)?(?:legally\s+|statutorily\s+|fully\s+)?(?:compliant|in\s+compliance|non[-\u2010-\u2015\u2212\s]*compliant|lawful|unlawful)\b`
       * `\b(?:compl(?:y|ies|ied|ying)\s+with|complian(?:t|ce)\s+with|in\s+compliance\s+with|non[-\u2010-\u2015\u2212\s]*compliant|legally\s+compliant|confirm\s+compliance|certify\s+compliance|decide\s+breach|in\s+breach\b|breach(?:es|ed)?\s+(?:of\b|(?:the|our|this|its|awaab'?s)\b)|violat(?:e|es|ed|ing)\s+(?:the|our|this|its|awaab'?s)\b|violation\s+of\b|pass(?:es|ed)?\s+inspection)\b`
       * `\b(?:do|does|did|has|have|will|would|can)\s+(?:this|that|these|those|the|our|my|we|it)\b[^.;!?]{0,50}\b(?:comply|complied|pass\s+inspection|violate|violated|breach|breached)\b`
       * `\b(?:(?:do|does|did|has|have)\b[^.;!?]{0,40}\b(?:met|meet|satisfy|satisfied)|satisf(?:y|ies|ied)|meets?)\s+(?:our\s+|the\s+|this\s+|its\s+|a\s+|any\s+)?(?:[a-z0-9']+\s+){0,2}(?:duty|duties|obligation|law|act|standard|regulation|requirement)s?\b` (plus `\bdoes\s+this\s+satisfy\b` and `\bhave\s+we\s+met\s+our\s+(?:legal\s+)?duty\b`).
  3. `RV-032` + `PC-003` (`agreement_gaps`):
     * Require `owner` matching `LEGAL_GATE_OWNER` AND require at least one of `"compliance_owner"` or `"refusal_owner"` in `agreement`, with every present key in `("compliance_owner", "refusal_owner")` being a non-blank string matching `COMPLIANCE_GATE_OWNER`.
     * Whenever `grader is not None` (even if `owner is None`), check `grader` distinctness (`_canon_name` and non-empty `_base_person`) against `LEGAL_GATE_OWNER`, `COMPLIANCE_GATE_OWNER`, and every non-blank supplied owner string (`owner`, `compliance_owner`, `refusal_owner`).
     * Whenever any key in `("owner_id", "compliance_owner_id", "refusal_owner_id", "independent_grader_id")` is in `agreement`: require non-blank `"owner_id"`, non-blank `"independent_grader_id"`, non-blank `"compliance_owner_id"` if `"compliance_owner"` is in `agreement`, non-blank `"refusal_owner_id"` if `"refusal_owner"` is in `agreement`, at least one non-blank Compliance owner ID (`compliance_owner_id` or `refusal_owner_id`), and reject any blank/non-string value on any present `*_id` key; require `_canon_name(grader_id)` to be distinct from every supplied non-blank owner ID (`owner_id`, `compliance_owner_id`, `refusal_owner_id`) while allowing `owner_id` to match `compliance_owner_id` / `refusal_owner_id`.
  4. `RV-033` + `PC-002` (`_validate_benefit_thresholds`, `_compute_cost_per_accepted_check`, and `compare_chat_against_rule_cards`):
     * Add helper `_extract_unit_cost_ceiling(thresholds: Mapping[str, Any] | None) -> tuple[float | None, list[str]]` checking `"max_ai_cost_per_accepted_check_gbp"` and `"max_cost_per_accepted_check_gbp"`: require at least one present, require every present key to pass `_finite_float` with `val > 0.0` (rejecting `bool`, `<= 0`, `NaN`/`Inf`), and if both keys are present require `val_a == val_b`; wire into `_validate_benefit_thresholds` while keeping `benefit_thresholds=None` default (`BRD OD-51`).
     * Factor `_compute_cost_per_accepted_check(accepted_checks, cost_inputs, *, now) -> tuple[dict[str, Any], float | None]` returning `(public_4_key_report, exact_unit_cost)` so `cost_per_accepted_check` keeps its exact 4-key return dict unchanged while `compare_chat_against_rule_cards` checks `exact_unit_cost > max_unit_cost or float(cost_report["ai_cost_per_accepted_check"]) > max_unit_cost`.
     * Set `agreed_ceiling = float(max_unit_cost) if (trial["thresholds_valid"] and max_unit_cost is not None) else None` and `within_ceiling = (exact_unit_cost <= agreed_ceiling and float(cost_report["ai_cost_per_accepted_check"]) <= agreed_ceiling) if (agreed_ceiling is not None and exact_unit_cost is not None) else None`, emitting `"max_ai_cost_per_accepted_check_gbp": agreed_ceiling` and `"within_unit_cost_ceiling": within_ceiling` in `beside_cost`.
* Completion Expectation: Zero `mypy` or `ruff` findings; existing contracts and replay verification (`_replay_verify`) remain intact.

<!-- P01-T02 -->
### Task P01-T02: Update fixtures, add `test_c13_*` regressions in `src/core/tests/test_regulatory_eval_gates_216.py`, update `src/core/README.md`, and run `src/core` validation

* Test Ownership Lock:
  * Canonical test target: `src/core/tests/test_regulatory_eval_gates_216.py`
  * Generated targets: `none`
  * Exact test removals: `none`
  * Maximum test additions: `1` new test method (`test_c13_substantiated_freshness_paraphrase_refusal_dual_owners_and_cost_ceiling`)
  * Existing fixture updates in `src/core/tests/test_regulatory_eval_gates_216.py`:
    1. `_valid_agreement` and the 3 `sub_one_*` inline agreements (`sub_one_agr`, `malformed_agr`, `sub_one_corrupt_agr`): include `"compliance_owner": COMPLIANCE_GATE_OWNER`.
    2. `_valid_thresholds`: include `"max_ai_cost_per_accepted_check_gbp": 0.05`.
    3. `multi_bundle` and `unmapped_bundle`: populate complete `"in_cadence"` constituent metadata (`"status": "in_cadence"`, `"last_success": "2026-10-10"`, `"cadence_days": 14`, `"due_on": "2026-10-24"`).
  * Semantic vs regression coverage in `test_c13_substantiated_freshness_paraphrase_refusal_dual_owners_and_cost_ceiling`:
    1. Semantic + regression (`RV-030`, `PC-001`): verify `"in_cadence"` and `"out_of_cadence"` cards omitting constituent `"status"`, `"last_success"`, `"cadence_days"`, or `"due_on"`, spoofing `cadence_days=True`, carrying `"unknown"` with non-`None` `"due_on"`, or mismatching cross-card `cadence_days` fail `grade_chat_turn` and `_active_bundle_nonconflicting`.
    2. Semantic + regression (`RV-031`, `PC-004`): verify interrogative, plural, declarative, and Unicode-hyphen compliance-judgment paraphrases (`"Is this property compliant with the hazard law?"`, `"Do these works comply with the standard?"`, `"Tell me whether this property is compliant."`, `"Is this home non\u2011compliant?"`, `"Check whether this repair satisfies Awaab's Law."`, `"Is the landlord in breach of the damp duty?"`) are refused by `refuse_question` and `RegulatoryChat.surface` under both `comparison=None` and `comparison=positive_cmp`, while benign workflow/provision questions (`"Which reviewer does the officer meet?"`, `"What do the approved hazard provisions record for this home?"`) are not false-refused.
    3. Semantic + regression (`RV-032`, `PC-003`): verify an agreement omitting both `compliance_owner` and `refusal_owner`, mismatching either, omitting `compliance_owner_id` when `owner_id`/`independent_grader_id` are supplied, or colliding `compliance_owner_id` with `independent_grader_id` records `agreement_gaps`, stays `threshold_status == "provisional_not_agreed"`, and blocks `chat_with_cards`, while valid dual-owner IDs (`owner_id == compliance_owner_id != independent_grader_id`) pass.
    4. Semantic + regression (`RV-033`, `PC-002`): verify `benefit_thresholds` omitting unit-cost ceiling, passing `<= 0` / `bool`, or passing conflicting `max_ai_cost_per_accepted_check_gbp` vs `max_cost_per_accepted_check_gbp` fails validation (`beside_cost["max_ai_cost_per_accepted_check_gbp"] is None`), verify `max_cost_per_accepted_check_gbp` alias works when sole ceiling, verify exact unrounded unit-cost boundary (`0.0080004` > `0.008` even if rounded would match, or ceiling `0.001` < `0.008`) produces `measured_value == False` and `ship_mode == "cards_only"`, and verify `benefit_thresholds=None` preserves `BRD OD-51` no-default-target behavior.
* Documentation and Validation Evidence:
  * Update the Issue #216 bullet in `src/core/README.md` to document substantiated constituent freshness fields, compliance-judgment paraphrase refusal enforcement, dual-capacity gate-owner sign-off (`LEGAL_GATE_OWNER` + `COMPLIANCE_GATE_OWNER`), and owner-supplied `max_ai_cost_per_accepted_check_gbp` gating.
  * Run in `src/core`:
    * `python3 -m mypy`
    * `python3 -m ruff check .`
    * `python3 -m ruff format --check .`
    * `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`
    * `PYTHONPATH=src:tests python3 -m unittest tests/test_regulatory_chat.py tests/test_gates.py tests/test_live_doc_links.py`
