<!-- markdownlint-disable-file -->
# Implementation Changes: Issue #216 Child Hardening Pass 9 (`216-citation-eval-2142-c9`)

* Task ID: `216-citation-eval-2142-c9`
* Parent Task ID: `216-citation-eval-2142-c8`
* Date: `2026-11-14`
* Status: `Completed`
* Plan Artifact: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c9-plan.md`
* Phase Details Artifact: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c9-phase-details.md`
* Critique Artifact: `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c9-plan-critique.md`

## Scope and Readiness

* Declared scope: Full plan (`P01`: `P01-T01`, `P01-T02`) within `src/core`.
* Blockers: None.

## Completed Work by Plan Marker

### Phase 1 (`P01`) — Completed

* `P01-T01`: Completed in `src/core/src/zava_forward/core/regulatory_eval_gates.py` and `src/core/README.md` (`_CANONICAL_REFUSAL_REASONS`, `citation_validity`-aware `_classify_refusal_confusion`, `cit_blockers` + `ref_blockers` blocking any `unsafe_non_refusal` or `invalid_response` under sub-`1.0` `min_rates`, active `as_of`-current `deterministic_rule_cards` with `conflict_provisions` isolation and explicit-refusal / mixed-validity fail-closed gating, `_baseline_projection_matches` `conflict_provisions` parity, and bounded ASCII `@v` version parsing in `_id_version_matches`).
* `P01-T02`: Completed in `src/core/tests/test_regulatory_eval_gates_216.py` (aligned `conservative_refusal` `as_of` in `test_c8_provenance_refusal_nonregression_bigint_and_sub_one_gates` and added `test_c9_unsafe_refusal_blocker_active_fallback_cards_and_unicode_versions`).

## Amendments and Divergences

* None.

## Validation Evidence

* `python3 -m mypy`: `Success: no issues found in 318 source files`
* `python3 -m ruff check .`: `All checks passed!`
* `python3 -m ruff format --check .`: `265 files already formatted`
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `Ran 12 tests in 15.046s - OK`
* `PYTHONPATH="src:tests" python3 -m unittest test_regulatory_chat test_gates test_live_doc_links -q`: `Ran 58 tests in 28.629s - OK`
* Verified zero `.copilot-tracking/` strings across `src/`.

## Follow-Up Items

* Downstream `src/api` route wiring for `/api/law/chat` vs `/api/law/cards` remains tracked outside this `src/core`-scoped worktree slice of Issue #216.
