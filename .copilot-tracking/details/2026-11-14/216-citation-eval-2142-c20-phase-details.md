<!-- markdownlint-disable-file -->
# Phase Details: Child Hardening Pass 20 for Issue #216 (`RV-051`..`RV-052`)

* Task ID: `216-citation-eval-2142-c20`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c20-plan.md`

## `P01-T01`: Coordinated Obligation Modifiers and Coordinated Adverbs

* In `src/core/src/zava_forward/core/regulatory_eval_gates.py`:
  * Expand `_OBLIGATION_PREPOSITION_GUARD_RE` with temporal/locative prepositions and clause/auxiliary guards so `{0,6}` tokens of `[a-z0-9',-]+` in `_OBLIGATION_OBJECT_RE` match coordinated modifiers (`"legal and statutory obligations"`, `"damp, mould, and building-safety standards"`) without crossing prepositions or clauses.
  * Update `_MEETING_ADVERBS_RE` to allow optional comma and coordinating `and|or|nor|but` across up to 4 adverbial units (`"adequately and consistently"`, `"not adequately or consistently"`), and widen `_NON_WH_COND_SPAN_RE` to `{1,10}` tokens.

## `P01-T02`: Regression Tests and Verification

* Add `test_c20_coordinated_obligation_modifiers_and_adverbs_refusal_precision` in `src/core/tests/test_regulatory_eval_gates_216.py` covering coordinated obligation modifiers, coordinated adverbs before `meeting`, and benign preposition/clause boundaries.
* Run `mypy`, `ruff check .`, `ruff format --check .`, `unittest discover -s tests -p 'test_*216*.py' -v`, and companion `src/core` tests.
