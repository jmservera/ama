<!-- markdownlint-disable-file -->
# Phase Details: Child Hardening Pass 15 for Issue #216 (`RV-038`..`RV-040`)

* Task ID: `216-citation-eval-2142-c15`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c15-plan.md`
* Research Path: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c15-research.md`

<!-- P01 -->
## Phase 1: Close `RV-038`..`RV-040` in `src/core` and Verify

<!-- P01-T01 -->
### `P01-T01`: Harden `regulatory_eval_gates.py` (`RV-038`..`RV-040`)

* Target file: `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* Exact behavioral rules:
  1. **`RV-038` (`_REFUSAL_PATTERNS[1]`)**:
     * Keep non-progressive `(?:(?:do|does|did|has|have|will|would|can|could|should)\b[^.;!?]{0,45}\b(?:met|meets?|satisf(?:y|ies|ied))|satisf(?:y|ies|ied|ying)|meets?)` matched against `(?:our\s+|the\s+|this\s+|its\s+|their\s+|a\s+|any\s+)?(?:[a-z0-9']+\s+){0,2}(?:duty|duties|obligation|obligations|law|laws|act|standard|standards|regulation|regulations|requirement|requirements)\b`.
     * Separate progressive `satisfying` (`\b(?:is|are|was|were)\b[^.;!?]{0,45}\bsatisfying\b`) and progressive `meeting`:
       * Require progressive `meeting` either after `\b(?:is|are|was|were)\b[^.;!?]{0,35}\b(?:{_COMPLIANCE_SUBJECT_RE}|we|they|it|this|that|these|those)\b[^.;!?]{0,20}` with negative lookbehind `(?<!\ba\s)(?<!\ban\s)(?<!\bthe\s)(?<!\bany\s)(?<!\bour\s)(?<!\btheir\s)(?<!\bnext\s)(?<!\bstaff\s)(?<!\bteam\s)(?<!\bresident\s)` AND negative verb-context guard (no `\b(?:having|hold(?:ing)?|schedul(?:e|ed|ing)|attend(?:ing)?|book(?:ed|ing)?|arrang(?:e|ed|ing))\b` between `is|are|was|were` and `meeting`), OR direct `\b(?<!\ba\s)(?<!\ban\s)(?<!\bthe\s)meeting\s+(?:our|its|their|the|statutory|legal|regulatory)\b`,
       * Followed immediately by a direct determiner/adjective compliance object (blocking prepositions `(?!\s+(?:about|on|for|with|at|in|to|from|by|regarding|concerning)\b)`): `\s+(?:our\s+|the\s+|this\s+|its\s+|their\s+|all\s+|every\s+)?(?:(?:legal|statutory|regulatory|safety|damp|mould|hazard|awaab'?s|decent|homes|minimum|funder|housing|applicable)\s+){0,2}(?:duty|duties|obligation|obligations|law|laws|act|standard|standards|regulation|regulations|requirement|requirements)\b`.
  2. **`RV-039` (Mandatory paired observation timestamps in `_score_paired_observations`)**:
     * Every observation row must contain `"observed_at"` or `"recorded_at"`.
     * Parse every present key in `("observed_at", "recorded_at")` via `_extract_day`; if missing both, if either fails `_extract_day`, if both are present with unequal UTC days, if `thresholds_agreed_day is not None and obs_day < thresholds_agreed_day`, or if `eval_day is not None and obs_day > eval_day`, append a row error and skip the row.
     * Track `valid_obs_days: list[str]` across valid paired rows and `accepted_chat_days: list[str]` across valid paired `"chat"` rows with `accepted is True`; expose `"min_observation_day": min(valid_obs_days) if valid_obs_days else None` and `"min_accepted_chat_day": min(accepted_chat_days) if accepted_chat_days else None` in `paired_trial`.
  3. **`RV-040` (Pre-observation `agreed_on` bound for `accepted_definition` and `verified_agreement`)**:
     * Add `*, max_agreed_day: str | None = None` to `_compute_cost_per_accepted_check`: require `accepted_agreed_day <= current.date().isoformat()` AND (`max_agreed_day is None or str(accepted_agreed_day) <= max_agreed_day`).
     * In `compare_chat_against_rule_cards`, compute `earliest_trial_day = trial.get("min_accepted_chat_day") or trial.get("min_observation_day")` (or `min` of non-None `min_observation_day` and `min_accepted_chat_day`), pass `max_agreed_day=earliest_trial_day` to `_compute_cost_per_accepted_check`, and also verify `verified_agr["agreed_on"] <= earliest_trial_day` when `earliest_trial_day is not None`.

<!-- P01-T02 -->
### `P01-T02`: Update `_valid_observations`, Add `test_c15`, Update `README.md`, and Verify

* Target files: `src/core/tests/test_regulatory_eval_gates_216.py`, `src/core/README.md`
* Test ownership lock: `none` removals; populate `"observed_at": NOW.isoformat()` in `_valid_observations`; max `1` new test method `test_c15_meeting_noun_precision_mandatory_observation_dates_and_accepted_def_ordering`.
