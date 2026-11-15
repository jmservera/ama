<!-- markdownlint-disable-file -->
# Review Record: Child Hardening Pass 14 for Issue #216 (`RV-034`..`RV-037`)

* Task ID: `216-citation-eval-2142-c14`
* Parent Task ID: `216-citation-eval-2142-c13`
* Date: `2026-11-14`
* Execution Status: `Complete`
* Outcome: `Defects found`

## Compared Artifacts

* `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c14-research.md`
* `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c14-plan.md`
* `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c14-phase-details.md`
* `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c14-plan-critique.md`
* `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c14-changes.md`
* `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* `src/core/src/zava_forward/core/regulatory_chat.py`
* `src/core/tests/test_regulatory_eval_gates_216.py`
* `src/core/README.md`

## Closure Verification for `c13` Routed Findings

* `RV-034` (Progressive/modal compliance refusal coverage): Closed for obligation-satisfaction and modal subject-compliance questions (`test_c14` verified), with one noun-vs-verb refinement noted below (`RV-038`).
* `RV-035` (Exact 3-way canonical `source_monitor` freshness label parity): Closed across `_card_provenance_valid` and `_active_bundle_nonconflicting`.
* `RV-036` (Pre-evaluation `agreed_on` temporal ordering + non-synthetic observation guards + `evidence_scope`): Partially closed; undated observations and `accepted_definition.agreed_on` ordering relative to observation dates require mandatory observation timestamps (`RV-039`, `RV-040`).
* `RV-037` (Exact unrounded unit-cost ceiling check + opt-in `RegulatoryChat` instance ship-gate binding on `start()`, `ask()`, and `surface()`): Closed.

## Validation Evidence

* `cd src/core && python3 -m mypy`: `Success: no issues found in 318 source files`
* `cd src/core && python3 -m ruff check .`: `All checks passed!`
* `cd src/core && python3 -m ruff format --check .`: `265 files already formatted`
* `cd src/core && python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `Ran 17 tests in 29.881s — OK`
* `cd src/core && PYTHONPATH=src:tests python3 -m unittest tests/test_regulatory_chat.py tests/test_gates.py tests/test_live_doc_links.py`: `Ran 58 tests in 56.716s — OK`

## Findings

### `RV-038` (Medium): Appointment/noun `"meeting"` in `"Is there a meeting about statutory obligations?"` triggers false compliance refusal

* Boundary: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_REFUSAL_PATTERNS[1]`)
* Evidence: `_REFUSAL_PATTERNS[1]` allows `is|are|was|were` + arbitrary tokens up to `45` chars + `meeting` + two arbitrary `[a-z0-9']+` tokens (`about statutory`) + `obligations`, falsely refusing factual appointment questions such as `"Is there a meeting about statutory obligations?"`.
* Impact: False refusal on benign factual questions mentioning a `"meeting"` as a noun followed by a preposition (`about`, `on`, `for`, `regarding`).
* Destination: `rpi-implement` in child task `216-citation-eval-2142-c15` (restrict progressive `meeting`/`satisfying` to compliance subjects or direct determiner/compliance-adjective objects, excluding noun articles `a`/`an`/`the` before `meeting` and prepositions `about|on|for|with|at|in|regarding|concerning` after `meeting`).

### `RV-039` (High): Undated paired observations bypass pre-trial `agreed_on <= observed_at <= eval_day` verification

* Boundary: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_score_paired_observations`) and `src/core/tests/test_regulatory_eval_gates_216.py` (`_valid_observations`)
* Evidence: `_score_paired_observations` validates `observed_at` / `recorded_at` only when present, allowing undated observation rows to establish `measured_value = True` without proving the paired trial took place on or after `benefit_thresholds["agreed_on"]` and on or before `eval_day`.
* Impact: Undated observations cannot prove pre-trial threshold agreement ordering.
* Destination: `rpi-implement` in child task `216-citation-eval-2142-c15` (require every paired observation row to carry a valid `observed_at` or `recorded_at` timestamp — consistent when both are present — within `[benefit_thresholds.agreed_on, eval_day]`, and populate `"observed_at"` in `_valid_observations`).

### `RV-040` (Medium): `cost_inputs.accepted_definition.agreed_on` is checked against `now` (`eval_day`) but not against the earliest accepted observation timestamp

* Boundary: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_score_paired_observations`, `_compute_cost_per_accepted_check`, `compare_chat_against_rule_cards`)
* Evidence: `_compute_cost_per_accepted_check` checks `accepted_definition.agreed_on <= current.date().isoformat()`, so an `accepted_definition` dated `"2026-10-16"` could authorize cost calculation for accepted chat observations recorded earlier on `"2026-10-10"` when evaluated on `"2026-10-16"`.
* Impact: Post-hoc `accepted_definition` could be agreed after accepted trial checks were already recorded.
* Destination: `rpi-implement` in child task `216-citation-eval-2142-c15` (record `min_accepted_chat_day` in `_score_paired_observations` and enforce `accepted_definition.agreed_on <= min_accepted_chat_day` as well as `<= eval_day` in `_compute_cost_per_accepted_check` / `compare_chat_against_rule_cards`).

## Plan Follow-Up Assessment

* Cross-package wiring in `src/api` and `src/agents` and future ratification of `BRD OD-51` finance policy figures remain valid external follow-up items outside `src/core` and are not active-scope defects.
