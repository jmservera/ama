<!-- markdownlint-disable-file -->
# Changes Record: Child Hardening Pass 20 for Issue #216 (`RV-051`..`RV-052`)

* Task ID: `216-citation-eval-2142-c20`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c20-plan.md`
* Phase Details Path: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c20-phase-details.md`
* Critique Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c20-plan-critique.md`
* Status: `Completed`

## Summary

Completed `P01-T01` and `P01-T02` in `src/core` closing `RV-051` and `RV-052`:

### `P01-T01`: Coordinated Obligation Modifiers (`RV-051`) and Coordinated Adverbs (`RV-052`)

* Expanded `_OBLIGATION_PREPOSITION_GUARD_RE` and widened `_OBLIGATION_OBJECT_RE` to `{0,6}` `[a-z0-9',-]+` modifier tokens in `src/core/src/zava_forward/core/regulatory_eval_gates.py` so coordinated modifiers (`"legal and statutory obligations"`, `"damp, mould, and building-safety standards"`) match without crossing prepositional or clause boundaries (`RV-051`).
* Extended `_MEETING_ADVERBS_RE` to support coordinated adverbial units (`and|or|nor|but` + commas across up to 4 units) and widened `_NON_WH_COND_SPAN_RE` to `{1,10}` tokens and the polar question span to `{1,90}` chars (`RV-052`).

### `P01-T02`: Regression Tests and Verification

* Added `test_c20_coordinated_obligation_modifiers_and_adverbs_refusal_precision` in `src/core/tests/test_regulatory_eval_gates_216.py`.
* Verified in `src/core`:
  * `python3 -m mypy`: `Success: no issues found in 318 source files`
  * `python3 -m ruff check .`: `All checks passed!`
  * `python3 -m ruff format --check .`: `265 files already formatted`
  * `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `Ran 22 tests ... OK`
  * `PYTHONPATH=src:tests python3 -m unittest tests/test_regulatory_chat.py tests/test_gates.py tests/test_live_doc_links.py`: `Ran 58 tests ... OK`

## Blockers and Remaining Work

* Blockers: None.
* Remaining active-plan work: None (`P01`, `P01-T01`, and `P01-T02` completed).
