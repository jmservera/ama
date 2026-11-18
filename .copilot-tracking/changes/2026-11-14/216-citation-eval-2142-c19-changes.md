<!-- markdownlint-disable-file -->
# Changes Record: Child Hardening Pass 19 for Issue #216 (`RV-049`..`RV-050`)

* Task ID: `216-citation-eval-2142-c19`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c19-plan.md`
* Phase Details Path: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c19-phase-details.md`
* Critique Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c19-plan-critique.md`
* Status: `Completed`

## Summary

Completed `P01-T01` and `P01-T02` in `src/core` closing `RV-049` and `RV-050`:

### `P01-T01`: General Adverbs and Bounded Non-WH/Non-Conditional Spans (`RV-049`)

* Added `_MEETING_ADVERBS_RE` and `_NON_WH_COND_SPAN_RE` in `src/core/src/zava_forward/core/regulatory_eval_gates.py` and applied them across all progressive `meeting` branches in `_REFUSAL_PATTERNS[1]`, eliminating the wildcard `[^.;!?]{0,40}` gerund span so `"Please check what happens if the team is meeting statutory obligations."` and `"Is it clear what happens if..."` stay allowed while general `-ly` adverbs (`"adequately"`, `"properly"`) and optional-`that` confirmations refuse.

### `P01-T02`: Schema-Valid Bundle-Mutation Regression Proof (`RV-050`)

* Updated `test_c18_renderer_bundle_mutation_isolation_and_whether_vs_prefaced_wh_if_precision` in `src/core/tests/test_regulatory_eval_gates_216.py` so both `_tampering_render` (refusal spoofing) and `_source_swap_render` (provision-ID spoofing) mutate a supported `snap` in place and return `render_extractive_answer(snap)`, proving `copy.deepcopy(snap)` isolation in both `RegulatoryChat.ask()` (`ChatForbidden`, `0` persisted messages) and `RegulatoryChat.surface()` (`cards_only`, non-empty `rule_cards["cards"]`).
* Verified in `src/core`:
  * `python3 -m mypy`: `Success: no issues found in 318 source files`
  * `python3 -m ruff check .`: `All checks passed!`
  * `python3 -m ruff format --check .`: `265 files already formatted`
  * `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `Ran 21 tests ... OK`
  * `PYTHONPATH=src:tests python3 -m unittest tests/test_regulatory_chat.py tests/test_gates.py tests/test_live_doc_links.py`: `Ran 58 tests ... OK`

## Blockers and Remaining Work

* Blockers: None.
* Remaining active-plan work: None (`P01`, `P01-T01`, and `P01-T02` completed).
