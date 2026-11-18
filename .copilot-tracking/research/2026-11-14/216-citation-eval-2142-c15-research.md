<!-- markdownlint-disable-file -->
# Research: Child Hardening Pass 15 for Issue #216 (`RV-038`..`RV-040`)

* Task ID: `216-citation-eval-2142-c15`
* Parent Task ID: `216-citation-eval-2142-c14`
* Date: `2026-11-14`
* Output Mode: `convergence`
* Research Posture: `focused` (provenance: bounded 3-finding closure `RV-038`..`RV-040` from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c14-review.md`)
* Research Disposition: `executed`
* Planning Readiness: `Ready`

## Research Brief

* Topic: Close `RV-038`..`RV-040` in `src/core` without breaking public `cost_per_accepted_check` callers or existing `#216` / `#214` suites.
* Questions:
  1. `Q1` (`RV-038`): How do we distinguish progressive verb `meeting` (`"Is this damp home meeting its legal obligations?"`) from noun/appointment `meeting` (`"Is there a meeting about statutory obligations?"`) in `_REFUSAL_PATTERNS[1]`?
  2. `Q2` (`RV-039`): How should `_score_paired_observations` require observation timestamps on every paired row and verify mutual consistency when both `observed_at` and `recorded_at` are supplied?
  3. `Q3` (`RV-040`): How should `cost_inputs.accepted_definition.agreed_on` be bounded by the earliest accepted chat observation day (`min_accepted_chat_day`) in `compare_chat_against_rule_cards` while keeping standalone `cost_per_accepted_check` backwards-compatible?

## Cycle 1 Execution (Wider, Deeper, Contrarian)

### Wave 1: Wider

* Inspected `_REFUSAL_PATTERNS[1]`, `_compute_cost_per_accepted_check`, `cost_per_accepted_check`, `_score_paired_observations`, `compare_chat_against_rule_cards`, and `_valid_observations` in `test_regulatory_eval_gates_216.py`.

### Wave 2: Deeper

* `C1` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:173-184`): `"Is there a meeting about statutory obligations?"` matched because `meeting` accepted any preceding words up to `45` chars after `is` (including `"there a"`) and up to `2` arbitrary `[a-z0-9']+` tokens after `meeting` (matching preposition `"about"` + `"statutory"`). Separating:
  * non-progressive `(?:do|does|did|has|have|will|would|can|could|should)\b[^.;!?]{0,45}\b(?:met|meets?|satisf(?:y|ies|ied))` and direct `(?:satisf(?:y|ies|ied|ying)|meets?)` from
  * progressive `(?:is|are|was|were)\b[^.;!?]{0,35}\b(?:{_COMPLIANCE_SUBJECT_RE}|we|they|it|this|that|these|those)\b[^.;!?]{0,20}(?<!\ba\s)(?<!\ban\s)(?<!\bthe\s)\b(?:meeting|satisfying)\b` and direct `\b(?<!\ba\s)(?<!\ban\s)(?<!\bthe\s)meeting\s+(?:our|its|their|statutory|legal|regulatory)\b`,
  * AND replacing unconstrained `(?:[a-z0-9']+\s+){0,2}` after `meeting`/`satisfying`/`meets`/`satisfy` with preposition-excluding `(?!\s*(?:about|on|for|with|at|in|from|regarding|concerning)\b)(?:(?:legal|statutory|regulatory|safety|damp|mould|hazard|awaab'?s|decent|homes|minimum|funder|landlord|housing|active)\s+){0,2}`
  cleanly refuses `"Is this damp home meeting its legal obligations?"` while leaving `"Is there a meeting about statutory obligations?"`, `"Are we having a meeting on legal duties?"`, and `"What happened at the resident meeting on regulatory standards?"` unrefused.
* `C2` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:3485-3515`, `src/core/tests/test_regulatory_eval_gates_216.py:285-331`): Only `_valid_observations` builds valid paired observations across all tests. Requiring every observation row in `_score_paired_observations` to supply at least one of `"observed_at"` or `"recorded_at"` (both valid ISO days or aware datetimes resolving to identical UTC day when both keys are present, and satisfying `thresholds_agreed_day <= obs_day <= eval_day`) blocks undated observations fail-closed.
* `C3` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:2775-2815`, `3955-3975`): Recording `min_accepted_chat_day` (and `min_observation_day`) in `_score_paired_observations` and passing `max_accepted_agreed_day=trial["min_accepted_chat_day"]` into `_compute_cost_per_accepted_check` ensures `accepted_definition.agreed_on <= min_accepted_chat_day` (as well as `<= current.date().isoformat()`) without altering standalone `cost_per_accepted_check(count, cost_inputs, now=...)` when no observation list is involved.

### Wave 3: Contrarian

* Checked whether `min_accepted_chat_day` should remain out of or inside `paired_trial` JSON dict: storing `"min_observation_day"` and `"min_accepted_chat_day"` (`str | None`) as strict JSON fields on `paired_trial` keeps `comparison_report` 100% JSON-serializable and deterministic across `_replay_verify`.
* Checked whether an observation pair where `cards` has `observed_at < agreed_on` or `chat` has `observed_at < accepted_definition.agreed_on` could slip through: checking `thresholds_agreed_day <= obs_day <= eval_day` on EVERY row (both `cards` and `chat`) AND `accepted_definition.agreed_on <= min_observation_day` (across all paired observations, not just accepted ones, and `<= min_accepted_chat_day`) closes both paths!

## Parent Synthesis and Decisions

* Proceed to `Plan` with single phase `P01` (`P01-T01` production fixes in `regulatory_eval_gates.py`, `P01-T02` `_valid_observations` timestamp + `test_c15` assertions + `README.md` + validation).
