<!-- markdownlint-disable-file -->
# Phase Details: Child Hardening Pass 16 for Issue #216 (`RV-041`..`RV-043`)

* Task ID: `216-citation-eval-2142-c16`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c16-plan.md`
* Research Path: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c16-research.md`

<!-- P01 -->
## Phase 1: Close `RV-041`..`RV-043` in `src/core` and Verify

<!-- P01-T01 -->
### `P01-T01`: Update `regulatory_eval_gates.py` and `regulatory_chat.py`

* `src/core/src/zava_forward/core/regulatory_eval_gates.py`:
  * Expand `_COMPLIANCE_SUBJECT_RE` to include `housing\s+associations?|associations?|organi[sz]ations?|providers?|contractors?|programmes?|services?|teams?|plans?|polic(?:y|ies)|processes?|approaches?|assessments?|inspections?|responses?|actions?|schedules?`.
  * Generalize progressive `meeting` in `_REFUSAL_PATTERNS[1]` so any non-`there` yes/no `is|are|was|were ... meeting` + `_OBLIGATION_OBJECT_RE` (without appointment verbs or noun articles/prepositions before `meeting`), any non-WH declarative/subordinate `... is|are|was|were [adverb]? meeting` + `_OBLIGATION_OBJECT_RE`, and compliance-assertion verbs + `meeting` + `_OBLIGATION_OBJECT_RE` refuse.
  * Pass `eval_now=parsed_now` to `_score_paired_observations`, parse `observed_at` and `recorded_at` via `_aware_dt` (rejecting bare date-only strings), enforce `obs_dt <= eval_now` and `rec_dt <= eval_now`, enforce `obs_dt <= rec_dt` and identical UTC dates when both keys are supplied, and check `obs_day >= thresholds_agreed_day`.
* `src/core/src/zava_forward/core/regulatory_chat.py`:
  * Use `ship_gate_comparison: Mapping[str, Any] | None | object = _UNSET` and `enforce_ship_gate: bool | None = None` in `RegulatoryChat.__init__`; raise `TypeError` if `enforce_ship_gate is not None and type(enforce_ship_gate) is not bool` or if `ship_gate_comparison is not _UNSET and ship_gate_comparison is not None and not isinstance(ship_gate_comparison, Mapping)`.
  * Set `self._enforce_ship_gate = (ship_gate_comparison is not _UNSET) if enforce_ship_gate is None else enforce_ship_gate` and `self._ship_gate_comparison = None if ship_gate_comparison is _UNSET else ship_gate_comparison`.
  * Add `@classmethod def ship_gated(cls, ..., *, ship_gate_comparison: Mapping[str, Any] | None = None) -> RegulatoryChat` calling `cls(..., ship_gate_comparison=ship_gate_comparison, enforce_ship_gate=True)`.

<!-- P01-T02 -->
### `P01-T02`: Add `test_c16`, Update `src/core/README.md`, and Run Verification

* Add `test_c16_general_subject_meeting_refusal_instant_observation_bounds_and_auto_ship_gate` in `src/core/tests/test_regulatory_eval_gates_216.py` (`none` removals; max `1` new test method).
* Update `src/core/README.md` to document UTC-instant observation bounds, automatic `enforce_ship_gate` activation when `ship_gate_comparison` is supplied, and `RegulatoryChat.ship_gated`.
