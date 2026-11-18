<!-- markdownlint-disable-file -->
# Research: Issue #216 Child Hardening Pass 8 (`216-citation-eval-2142-c8`)

## Research Brief

* Topic: Close `c7` review findings `RV-008`..`RV-014` in `src/core` for Issue #216 citation-validity, refusal-accuracy, and paired rule-card shipping gates.
* Purpose: Achieve zero remaining in-scope `src/core` defects across provenance temporal/version/exercise bounds, question-to-refusal binding, non-regression paired benefit floors, collision-free observation surface digests, malformed-card refusal handling, arbitrary-precision integer safety, and sub-`1.0` owner-agreed `min_rates`.
* Audience / Use: Planning, implementation, and review for child RPI task `216-citation-eval-2142-c8`.
* Scope: `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md` (with `src/core/src/zava_forward/core/regulatory_chat.py` verified).
* Non-goals: Cross-package changes in `src/api` or `src/agents`, `pip install -e .`, or `git push`.
* Output mode: `convergence`
* Research posture: `focused` (bounded internal hardening task with exact file/symbol evidence supplied by `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c7-review.md`).
* Research disposition: `reused`
* Planning Readiness: `Ready`

## Extension Provenance

* Repository instructions (`.github/copilot-instructions.md`): Applied (`src/core` test commands, Markdown conventions, no `.copilot-tracking/` references in `src/`).
* Skills: `rpi-research` (selected), `rpi-plan` (downstream), `rpi-implement` (downstream), `rpi-review` (downstream).
* Specialists: Inline codebase verification (no independent research lane needed because `c7-review.md` pinpoints all 7 symbols in `regulatory_eval_gates.py`).

## Cycle 1 (Wider, Deeper, Contrarian)

### Wider Wave

* Examined all 7 findings (`RV-008`..`RV-014`) in `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c7-review.md` alongside `regulatory_eval_gates.py`, `regulatory_chat.py`, and `test_regulatory_eval_gates_216.py`.

### Deeper Wave (Codebase Evidence)

* `C1` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:778-880`): `_projected_provision_valid`, `_source_provenance_valid`, `_fact_provenance_valid`, and `_card_provenance_valid` check ISO syntax and `@v` substring presence, but do not check temporal bounds (`effective <= as_of_day`, `retrieved <= as_of_day`, `approved_on <= as_of_day`), `@v{version}` alignment between `id` and `version`, or `exercise is True` on active provenance (`RV-008`).
* `C2` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:1435-1565`): `evaluate_citation_and_refusal_gates` evaluates standalone `prompts` with `refuse`, but does not check each case's `question` against `refuse(question)` or require at least one prompt-triggered refused turn in `adversarial` (`RV-009`).
* `C3` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:2195-2445`): `_validate_benefit_thresholds` allows negative `min_completion_gain`/`min_comprehension_gain` and `max_elapsed_ratio > 1.0`, while `_score_paired_observations` allows `agg_ratio < 1.0` alone to satisfy `positive_lift` even when completion and comprehension regress (`-100%`) (`RV-010`).
* `C4` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:1915-1935`): `observation_surface_digest` projects through `_to_plain_json`, converting lone UTF-16 surrogates to `ascii(value)` prior to `_canon_json` and colliding with literal `ascii(value)` strings (`RV-011`).
* `C5` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:604-715`, `2590-2645`, and `src/core/tests/test_regulatory_eval_gates_216.py:1145-1228`): `render_extractive_answer` and `_expected_from_bundle` render `kind="answer"` when `cards=[]` or `cards=[{}]`.Note that `unmapped_bundle` in `test_regulatory_eval_gates_216.py` uses complete card metadata (`id`, `link`, `status`, `effective`, `approved_by`, `approved_on`, `safe_default`, `clock`) with `source_freshness=None` to exercise `missing_link_case_ids`; checking renderable card metadata (`_card_renderable`) rejects `cards=[]` and `cards=[{}]` while preserving `unmapped_bundle` link-parity diagnostics (`RV-012`).
* `C6` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:375-470`, `1118`, `1305-1325`, `2990-3060`): Python 3.12 raises `ValueError` when converting integers above 4300 decimal digits (`10**5000`) via `str()`, `ascii()`, or `json.dumps()`. Using bounded bit-length (`<= 8192` bits) for strict JSON ints and `to_bytes(...).hex()` tokens (`_int_token`) plus exception-safe `_safe_ascii` prevents `ValueError` across all digests, projections, f-strings, and `resolve_regulatory_surface` / `RegulatoryChat.surface` (`RV-013`).
* `C7` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:1360-1375`, `2530-2585`): `_build_gate_result` checks `passed_count < total_count` unconditionally and `_verify_agreed_gates_report` short-circuits on single failed turns before replaying `evaluate_citation_and_refusal_gates`, blocking valid runs against owner-agreed `min_rates < 1.0` (e.g., `9/10` vs `0.8`) (`RV-014`).

### Contrarian Wave

* Tested whether requiring `_card_provenance_valid` (including `source_freshness`) inside `render_extractive_answer` would mask `missing_link_case_ids` in `unmapped_bundle` (`C5`): confirmed it would turn `unmapped_bundle` into `refused` rather than testing unmapped card links. Separating `_card_renderable` (requiring active `id`/`@v`, `/api/law/cards/...` `link`, `status`, `effective <= as_of`, `approved_by`, `approved_on <= as_of`, `safe_default`, `clock`) from `_card_provenance_valid` (which additionally requires `source_freshness` mapping in `grade_chat_turn` and `_baseline_projection_matches`) resolves `RV-012` without losing `missing_link_case_ids` coverage.
* Tested whether allowing `min_rates < 1.0` (`RV-014`) could ship chat when chat grounding regresses below rule cards: confirmed `compare_chat_against_rule_cards` independently enforces `structural["grounding_lift"] >= 0.0` (`C7`), so rule-card superiority remains fail-closed while `evaluate_citation_and_refusal_gates` and `_verify_agreed_gates_report` honor owner-agreed `min_rates` consistently, provided `unsafe_non_refusal == 0`? Wait: if an owner sets `refusal_accuracy: 0.8` and 9/10 pass (e.g., 1 `false_refusal`), `rate = 0.9 >= 0.8` passes cleanly; we should still evaluate `rate_met = (passed_count == total_count) if target_rate >= 1.0 else (rate >= target_rate)` consistently in `_build_gate_result` and `re_gates` replay!

## Parent Synthesis and Decisions

* Selected recommendation: Implement cohesive `src/core` fixes for `RV-008`..`RV-014` in `regulatory_eval_gates.py`, add targeted regression assertions in `test_regulatory_eval_gates_216.py`, and update `src/core/README.md` if public invariants tighten.
* Rejected alternatives: Silently clamping negative thresholds (`RV-010`) or catching broad exceptions to hide bugs instead of bounded `_int_token` / `_safe_ascii` (`RV-013`).
* Unresolved blockers: None.
* Research disposition: `reused`
* Planning Readiness: `Ready`
