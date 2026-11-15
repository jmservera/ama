# RPI Review: Child Hardening Pass 12 for Issue #216 (`RV-026`..`RV-029`)

* Task ID: `216-citation-eval-2142-c12`
* Date: `2026-11-14`
* Review execution status: `Complete`
* Review outcome: `Defects found`

## Compared Artifacts

* Research: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c12-research.md`
* Plan: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c12-plan.md`
* Phase details: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c12-phase-details.md`
* Plan critique: `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c12-plan-critique.md`
* Changes record: `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c12-changes.md`
* Prior review: `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c11-review.md`

## Boundary and Reconciliation Verification

* Plan markers (`P01`, `P01-T01`, `P01-T02`), phase details, critique dispositions (`PC-001`..`PC-003`), changes evidence, follow-ups, and validation results are reconciled.
* Prior findings `RV-026`, `RV-027`, `RV-028`, and `RV-029` and critique items `PC-001`..`PC-003` are implemented and verified.
* Zero `.copilot-tracking/` references appear in `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, or `src/core/README.md`.

## Validation Evidence

* `python3 -m mypy` (`src/core`): `Success: no issues found in 318 source files`
* `python3 -m ruff check .` (`src/core`): `All checks passed!`
* `python3 -m ruff format --check .` (`src/core`): `265 files already formatted`
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v` (`src/core`): `Ran 15 tests in 51.250s — OK`
* Companion suites (`PYTHONPATH=src:tests`): `test_regulatory_chat.py` (`25/25 OK`), `test_gates.py` (`31/31 OK`), `test_live_doc_links.py` (`2/2 OK`)

## Findings

* `RV-030` [High] (`src/core/src/zava_forward/core/regulatory_eval_gates.py` — `_card_provenance_valid`): Constituent `source_freshness["sources"]` entries omitting `"status"` / `"due_on"` / `"last_success"` / `"cadence_days"` are still accepted on `"in_cadence"` and `"out_of_cadence"` cards, allowing synthetic cards to claim `"in_cadence"` without constituent monitoring evidence. Route: `rpi-implement` (via child task `216-citation-eval-2142-c13`).
* `RV-031` [High] (`src/core/src/zava_forward/core/regulatory_eval_gates.py` — `_REFUSAL_PATTERNS`; `src/core/src/zava_forward/core/regulatory_chat.py` — `RegulatoryChat.surface`): Compliance-judgment paraphrases such as `"Is this property compliant with the hazard law?"` evade `_REFUSAL_PATTERNS` while matching `classify_purpose` (`"hazard-awareness-clock"`), allowing `RegulatoryChat.surface` to return actionable rule cards or grounded chat on a compliance determination prompt. Route: `rpi-implement` (via child task `216-citation-eval-2142-c13`).
* `RV-032` [Medium] (`src/core/src/zava_forward/core/regulatory_eval_gates.py` — `agreement_gaps`): `GATE_OWNERS` assigns `citation_validity` to `LEGAL_GATE_OWNER` and `refusal_accuracy` to `COMPLIANCE_GATE_OWNER`, yet `agreement_gaps` treats `refusal_owner` / `compliance_owner` as optional rather than requiring explicit agreement from both designated gate-owner capacities before granting `owner_agreed`. Route: `rpi-implement` (via child task `216-citation-eval-2142-c13`).
* `RV-033` [Low] (`src/core/src/zava_forward/core/regulatory_eval_gates.py` — `_benefit_threshold_gaps`, `compare_chat_against_rule_cards`): Respecting Issue #216's OD-51 constraint ("BRD OD-51 is open; no price, budget or target is set here"), `benefit_thresholds` does not yet validate or enforce an optional owner-supplied `max_cost_per_accepted_check_gbp` ceiling against `cost_report["ai_cost_per_accepted_check"]` when an evaluation owner sets one. Route: `rpi-implement` (via child task `216-citation-eval-2142-c13`).

## Routed Follow-Up

1. Rank 1 (`216-citation-eval-2142-c13`, inside `src/core`): Require substantiated constituent freshness evidence (`status` on every constituent entry and `last_success`, `cadence_days`, `due_on` on `in_cadence`/`out_of_cadence` entries) (`RV-030`), expand compliance/breach/duty refusal paraphrase patterns (`RV-031`), require explicit `COMPLIANCE_GATE_OWNER` (`refusal_owner` or `compliance_owner`) alongside `LEGAL_GATE_OWNER` in `agreement_gaps` (`RV-032`), and enforce optional owner-supplied `max_cost_per_accepted_check_gbp` in `benefit_thresholds` without hardcoding an OD-51 target (`RV-033`).
2. Rank 2 (out of scope of `src/core` boundary): Wire `src/api` routes to `RegulatoryChat.surface` and deduplicate `src/agents` helpers in a separate cross-package task.
