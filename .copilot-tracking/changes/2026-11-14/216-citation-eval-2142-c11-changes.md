# Implementation Changes: Child Hardening Pass 11 for Issue #216 (`RV-023`..`RV-025`)

* Task ID: `216-citation-eval-2142-c11`
* Date: `2026-11-14`
* Plan: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c11-plan.md`
* Details: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c11-phase-details.md`
* Critique: `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c11-plan-critique.md`
* Status: `Completed`

## Summary

Completed `P01-T01` and `P01-T02` to resolve `RV-023`..`RV-025` and `PC-001`..`PC-004` in `src/core`.

## Task Log

* [x] `P01-T01`: Implemented exact per-card `provision_ids` emission and mid-loop refusal short-circuiting in `RegulatoryChat.bundle` (`src/core/src/zava_forward/core/regulatory_chat.py`), strict `provision_ids` provenance/subset/equality validation (`_card_provenance_valid`, `_active_cards_link_provisions`, `_conflict_collections_consistent`), unflagged version/ID contradiction guards (`_active_bundle_nonconflicting`) across `_inspect_bundle_surface` and `grade_chat_turn` (`citation_validity` and `answer_contract`), unconditional `expected` collection validation & emptiness on `refused`/`conflict` turns, and `expected` self-consistency checks in `_classify_refusal_confusion` and `_baseline_projection_matches` (`src/core/src/zava_forward/core/regulatory_eval_gates.py`), plus updated `src/core/README.md`.
* [x] `P01-T02`: Added `test_c11_exact_card_provision_ids_unflagged_version_conflicts_and_expected_refusal_guards` in `src/core/tests/test_regulatory_eval_gates_216.py` and verified all checks pass (`python3 -m mypy`: 0 issues in 318 source files; `python3 -m ruff check .`: passed; `python3 -m ruff format --check .`: passed; `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: 14/14 passed; companion suites `test_regulatory_chat`, `test_gates`, `test_live_doc_links`: 58/58 passed).

## Amendments and Divergences

* None. All four critique refinements (`PC-001`..`PC-004`) were incorporated into the finalized plan prior to implementation.
