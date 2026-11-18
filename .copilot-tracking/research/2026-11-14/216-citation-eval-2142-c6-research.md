<!-- markdownlint-disable-file -->
# RPI Research: Issue #216 Child Hardening Pass 6 (`RV-001`..`RV-003`)

* Task ID: 216-citation-eval-2142-c6
* Parent Task ID: 216-citation-eval-2142-c5
* Date: 2026-11-14
* Research disposition: reused
* Planning Readiness: Ready

## Reused Evidence

1. `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c5-review.md` (`RV-001`..`RV-003`):
   * `RV-001`: Non-empty `tuple` values in `recorded_home_facts` (and other `isinstance(..., list)` checks in `_exact_card_links_match`, `grade_chat_turn`, `_classify_refusal_confusion`) scored differently before vs after `_to_plain_json` conversion because scoring ran on raw inputs before projection.
   * `RV-002`: Malformed non-iterable fields (such as `expected["sources"] = object()` or non-sequence `cases` / `paired_cards` / `observations` / `prompts`) raised `TypeError` during scoring before strict JSON validation rejected them.
   * `RV-003`: Answer-branch `rows.append(...)` in `_score_structural_baseline` emitted raw `expected_kind` instead of `safe_expected_kind`, allowing custom objects with `__eq__("answer")` to break `json.dumps(..., allow_nan=False)` on failed comparison reports.
2. Architectural closure in `src/core/src/zava_forward/core/regulatory_eval_gates.py`:
   * Add `_is_nonstr_seq(value)` and `_seq(value)` across collection readers/graders so non-iterable inputs never raise `TypeError` and `tuple`/`list` sequences are scored identically everywhere.
   * Emit `safe_expected_kind` on both branches of `_score_structural_baseline`.
   * In `compare_chat_against_rule_cards`, validate strict JSON compatibility FIRST, project validated inputs via `_to_plain_json` BEFORE scoring, and execute a depth-1 `json.loads(json.dumps(comparison_report, allow_nan=False))` + `_verify_comparison_evidence` self-verification gate before ever returning `measured_value=True`.
