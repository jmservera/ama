# Implementation Changes: Child Hardening Pass 13 for Issue #216 (`216-citation-eval-2142-c13`)

* Task ID: `216-citation-eval-2142-c13`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c13-plan.md`
* Phase Details Path: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c13-phase-details.md`
* Declared Scope: Full plan (`P01`: `P01-T01`, `P01-T02`)
* Status: `Completed`

## Summary of Planned Execution

* Executed `P01-T01` in `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`RV-030`..`RV-033` + `PC-001`..`PC-004`).
* Executed `P01-T02` in `src/core/tests/test_regulatory_eval_gates_216.py` and `src/core/README.md`, then verified all `src/core` static analysis, formatting, Issue #216 tests, and companion test suites.

## Completed Tasks

* `P01-T01` (`src/core/src/zava_forward/core/regulatory_eval_gates.py`):
  * Added `_freshness_entry_valid` and wired `as_of_day` into `_active_bundle_nonconflicting` and `_card_provenance_valid` (`RV-030`, `PC-001`) so every constituent `source_freshness["sources"]` entry substantiates `"in_cadence"`, `"out_of_cadence"`, or `"unknown"` monitoring state with `_strict_int` `cadence_days` (`1..36600`), calendar `due_on == last_success + cadence_days`, `ref_day` inequalities, and aggregate rollup across rendering, card projection, and turn grading.
  * Expanded `_REFUSAL_PATTERNS[1]` with `_COMPLIANCE_SUBJECT_RE` and bounded single-clause ReDoS-safe regexes plus Unicode hyphen/dash classes (`RV-031`, `PC-004`) covering interrogative, declarative, compliance-treatment, obligation-satisfaction, and regulatory sign-off paraphrases without false-refusing factual provision/cadence queries.
  * Hardened `agreement_gaps` (`RV-032`, `PC-003`) to require dual-capacity sign-off from both `LEGAL_GATE_OWNER` (`owner`) and `COMPLIANCE_GATE_OWNER` (`compliance_owner` and/or `refusal_owner`), unconditional `independent_grader` distinctness whenever `grader is not None`, and complete distinct partner `*_id` sets (including matching `compliance_owner_id` and `refusal_owner_id` when both are supplied).
  * Factored `_compute_cost_per_accepted_check` (preserving `cost_per_accepted_check`'s exact 4-key return contract) and added `_extract_unit_cost_ceiling` inside `_validate_benefit_thresholds` and `compare_chat_against_rule_cards` (`RV-033`, `PC-002`) to require caller-supplied finite positive `max_ai_cost_per_accepted_check_gbp` (or `max_cost_per_accepted_check_gbp`, with zero hardcoded repository target per `BRD OD-51`) and fail closed to `cards_only` whenever exact unrounded or reported unit cost exceeds the ceiling.
* `P01-T02` (`src/core/tests/test_regulatory_eval_gates_216.py`, `src/core/README.md`):
  * Updated synthetic test fixtures (`_valid_agreement`, 3 `sub_one_*` inline agreements, `_valid_thresholds`, `multi_bundle`, and `unmapped_bundle`) and added `test_c13_substantiated_freshness_paraphrase_refusal_dual_owners_and_cost_ceiling`.
  * Updated the Issue #216 architecture and validation summary in `src/core/README.md`.

## Amendments and Divergences

* Minor compatible implementation-time refinements within `P01-T01` scope (no scope or requirement divergence):
  * Added explicit `compliance_owner_id == refusal_owner_id` parity check in `agreement_gaps` when both Compliance-owner ID aliases are simultaneously supplied.
  * Added bounded `confirm|certify|declare|treat|mark|deem|verify ... <subject> ... compliant|lawful` and `regulatory|compliance|legal|statutory sign-off` / `sign-off on <subject>` branches inside `_REFUSAL_PATTERNS[1]` so declarative/modal treatment and hyphenated sign-off prompts refuse cleanly under `_REFUSAL_PATTERNS[1]`.

## Validation Evidence

* `cd src/core && python3 -m mypy` -> `Success: no issues found in 318 source files`
* `cd src/core && python3 -m ruff check .` -> `All checks passed!`
* `cd src/core && python3 -m ruff format --check .` -> `265 files already formatted`
* `cd src/core && python3 -m unittest discover -s tests -p 'test_*216*.py' -v` -> `Ran 16 tests ... OK`
* `cd src/core && PYTHONPATH=src:tests python3 -m unittest tests/test_regulatory_chat.py tests/test_gates.py tests/test_live_doc_links.py` -> `Ran 58 tests ... OK`
* `.copilot-tracking` leak scan across `src/core` -> `0` matches

## Handoff to Review

* Ready for single-pass `Review` (`216-citation-eval-2142-c13-review.md`).
* Blockers: none. Remaining active `P01` work: none. Plan `## Follow-Up Items` remain outside `src/core` caller scope.
