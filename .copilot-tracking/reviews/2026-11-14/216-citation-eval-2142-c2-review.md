<!-- markdownlint-disable-file -->
# RPI Review: Issue #216 Child Hardening Pass 2 (`RV-001`..`RV-007`)

## Metadata

* Task ID: 216-citation-eval-2142-c2
* Review date: 2026-11-14
* Execution status: Complete
* Outcome: Defects found

## Compared Artifacts

* Research: .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c2-research.md
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c2-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c2-plan-critique.md
* Changes record: .copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c2-changes.md
* Prior parent review: .copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c1-review.md

## Boundary and Reconciliation Assessment

* All seven defects from `216-citation-eval-2142-c1-review.md` (`RV-001`, `RV-003` bundle-reply check, `RV-004`, `RV-005`, `RV-006`) and `PC-001` runtime non-Mapping bundle checks were implemented and verified across `mypy`, `ruff`, and 9 `test_*216*.py` tests.
* Independent `rubber-duck` review identified three remaining tamper/collision edge cases on adversarial prompt recomputation, fabricated `comparison` dicts at `resolve_regulatory_surface`, and untagged non-finite float digest collisions in `_normalize_json_value`.

## Findings

### RV-001 (High) - `_verify_agreed_gates_report` trusts reported `adversarial_prompts` counts without recomputing `evaluate_adversarial_prompts`

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_verify_agreed_gates_report`). If a report was produced with a failing prompt or overridden `refuse` callback, mutating `adversarial_prompts["missed"] = 0` / `refused = total`, flipping gate outcomes, and recomputing `report_integrity_sha256` is not caught unless `evaluate_adversarial_prompts(raw_prompts)` is recomputed directly against canonical `refuse_question` and `ADVERSARIAL_PROMPTS` coverage is enforced.
* Destination: `rpi-implement` (child task `216-citation-eval-2142-c3`)

### RV-002 (High) - `resolve_regulatory_surface` checks four top-level `comparison` flags without verifying underlying comparison evidence

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`resolve_regulatory_surface`). Passing a fabricated 4-key dictionary (`{"schema": COMPARISON_SCHEMA, "measured_value": True, "cards_alone": False, "ship_mode": "chat_with_cards"}`) bypasses structural benchmark, paired-trial lift, critical hazard-miss, beside-cost, and `comparison_integrity_sha256` verification.
* Destination: `rpi-implement` (child task `216-citation-eval-2142-c3`)

### RV-003 (Medium) - `_normalize_json_value` maps `float("nan")` and `{"__nonfinite_float__": "nan"}` to identical canonical JSON

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_normalize_json_value`). Because ordinary mappings are serialized untagged while non-finite floats serialize to `{"__nonfinite_float__": ...}`, distinct Python inputs collide under `_canon_json`. Tagged structural encoding eliminates all cross-type collisions.
* Destination: `rpi-implement` (child task `216-citation-eval-2142-c3`)

## Validation Coverage

* `python3 -m mypy`: PASS (318 source files)
* `python3 -m ruff check .` and `python3 -m ruff format --check .`: PASS (265 files)
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: PASS (9 tests)
* `test_dependency_rule.py` (2 tests), `test_live_doc_links.py` (2 tests), `test_regulatory_chat.py` (25 tests), `test_gates.py` (31 tests): PASS

## Plan Follow-Up Assessment

* `src/agents` helper deduplication and out-of-band human threshold/trial governance remain distinct non-defect follow-ups outside `src/core` scope.

## Routing Summary

* Route `RV-001`..`RV-003` to child RPI hardening loop `216-citation-eval-2142-c3` in `src/core`.
