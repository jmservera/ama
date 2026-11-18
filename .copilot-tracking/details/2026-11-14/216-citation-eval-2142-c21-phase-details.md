<!-- markdownlint-disable-file -->
# Phase Details: Child Hardening Pass 21 for Issue #216 (`RV-053`..`RV-054`)

* Task ID: `216-citation-eval-2142-c21`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c21-plan.md`

## `P01-T01`: `&` / `/` Separator Support and Intransitive Post-`meeting` Guards

* In `src/core/src/zava_forward/core/regulatory_eval_gates.py`:
  * Add temporal/locative post-`meeting` adverbs (`tomorrow|today|tonight|yesterday|soon|later|here|there|online|remotely|together|privately|regularly|weekly|monthly|daily|monday|tuesday|wednesday|thursday|friday|saturday|sunday`) and coordinated discussion/agenda participles (`discussing|reviewing|talking|chatting|speaking|presenting|debating|briefing|updating|considering|examining|exploring|looking|working|voting|deciding|agreeing`) to `_OBLIGATION_PREPOSITION_GUARD_RE`.
  * Allow `&` and `/` in `_OBLIGATION_OBJECT_RE` modifier tokens (`(?:[a-z0-9',/-]+|&)`) and `and(?:/or)?|&` in `_MEETING_ADVERBS_RE`.

## `P01-T02`: Regression Tests and Verification

* Expand `test_c20_coordinated_obligation_modifiers_and_adverbs_refusal_precision` in `src/core/tests/test_regulatory_eval_gates_216.py` with `"Are we meeting our damp health & safety obligations?"`, `"Are we meeting our legal and/or statutory obligations for this damp home?"`, and `"Is the team meeting tomorrow and discussing damp legal obligations?"`.
* Run `mypy`, `ruff check .`, `ruff format --check .`, `unittest discover -s tests -p 'test_*216*.py' -v`, and companion `src/core` tests.
