<!-- markdownlint-disable-file -->
# Changes Record: Issue #216 Child Hardening Pass 8 (`216-citation-eval-2142-c8`)

* Task ID: `216-citation-eval-2142-c8`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c8-plan.md`
* Phase Details Path: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c8-phase-details.md`
* Declared Scope: Full plan (`P01`: `P01-T01`, `P01-T02`)
* Execution Status: `Complete`

## Phase `P01` Execution Evidence

### `P01-T01` — Provenance, Refusal Binding, Non-Regression Floors, Digests, Big-Int Safety, and Sub-1.0 Gate Replay

* Status: `Completed`
* Files Updated:
  * `src/core/src/zava_forward/core/regulatory_eval_gates.py`:
    * Enforced `_MAX_JSON_INT_BITS = 8192`, `_int_token`, `_safe_ascii`, unhashable-key-safe `_canon_json`, bounded `_strict_int`, and oversized-int mapping in `_to_plain_json` (`RV-013`, `PC-004`).
    * Hardened `_source_provenance_valid`, `_fact_provenance_valid`, `_projected_provision_valid`, `_card_renderable`, `_card_provenance_valid`, `_source_matches`, `_fact_matches`, `grade_chat_turn`, `_baseline_projection_matches`, `render_extractive_answer`, `deterministic_rule_cards`, and `_expected_from_bundle` to verify `as_of` temporal currentness (`effective`, `retrieved`, `approved_on`), `@v{version}` alignment, `exercise=True`, and card renderability (`RV-008`, `RV-012`, `PC-002`).
    * Enforced prompt-to-expected refusal consistency and `adversarial_prompt_refused_turns >= 1` in `evaluate_citation_and_refusal_gates` (`RV-009`, `PC-003`).
    * Enforced non-regressing `benefit_thresholds` (`min_*_gain in [0, 1]`, `max_elapsed_ratio in (0, 1]`) and exact integer hit-delta per-role/aggregate non-regression in `_score_paired_observations` (`RV-010`, `PC-005`).
    * Updated `observation_surface_digest` via `_normalize_surface_value` so lone surrogates never collide with `ascii(...)` literals while sequence/mapping/aware-`datetime` JSON projections remain equivalent (`RV-011`, `PC-004`).
    * Fixed sub-`1.0` owner-agreed `min_rates` evaluation in `_build_gate_result` and `_verify_agreed_gates_report` while always blocking `unsafe_non_refusal > 0` or `missed > 0` standalone adversarial prompts (`RV-014`, `PC-001`).
  * `src/core/README.md`: Updated the Issue #216 subsection to document `as_of` currentness, prompt-triggered adversarial refusals, non-regressing paired-trial bounds, and `unsafe_non_refusal` blocking under owner-agreed `min_rates`.

### `P01-T02` — Regression Test Coverage and `src/core` Verification

* Status: `Completed`
* Files Updated:
  * `src/core/tests/test_regulatory_eval_gates_216.py`: Added 1 focused regression test method (`test_c8_provenance_refusal_nonregression_bigint_and_sub_one_gates`, within the `<= 2` addition ceiling) verifying `AC-01`..`AC-07` across `RV-008`..`RV-014` and `PC-001`..`PC-005`.

## Discoveries and Plan Updates

* Local judgment (`P01-T01`): Added `_normalize_surface_value` in `observation_surface_digest` and `_source_provenance_valid`/`_card_renderable` filtering in `deterministic_rule_cards` so aware-`datetime` surface digests match ISO timestamps (`RV-011`) and malformed `cards=[{}]` / `sources=[{}]` never project `id: None, link: None` entries (`RV-012`). Preserves approved intent with zero scope expansion.
* Blockers: `None`
* Remaining Active-Plan Work: `None` (`P01`, `P01-T01`, and `P01-T02` completed)
* Follow-Up Items: Downstream `src/api` route wiring for `/api/law/chat` vs `/api/law/cards` remains tracked outside this `src/core`-scoped worktree slice.

## Validation Evidence

* `cd src/core && python3 -m mypy`: `Success: no issues found in 318 source files`
* `cd src/core && python3 -m ruff check .`: `All checks passed!`
* `cd src/core && python3 -m ruff format --check .`: `265 files already formatted`
* `cd src/core && python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `Ran 11 tests in 16.242s - OK`
* `cd src/core && PYTHONPATH="src:tests" python3 -m unittest test_regulatory_chat test_gates test_live_doc_links -q`: `Ran 58 tests in 34.328s - OK`
* Verified zero `.copilot-tracking/` references in `src/`.
