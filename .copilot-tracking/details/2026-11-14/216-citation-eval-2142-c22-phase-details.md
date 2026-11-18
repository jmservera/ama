<!-- markdownlint-disable-file -->
# Phase Details: Child Hardening Pass 22 for Issue #216 (`RV-055`)

* Task ID: `216-citation-eval-2142-c22`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c22-plan.md`

## `P01-T01`: Structural Separation of Post-Verb Appointment Guards and NP Modifier Guards

* In `src/core/src/zava_forward/core/regulatory_eval_gates.py`:
  * Define `_NP_MODIFIER_GUARD_RE` covering prepositions, clause subordinators, finite auxiliaries, bare temporal nouns (`tomorrow|today|tonight|yesterday|monday..sunday|morning|afternoon|evening`), and general coordinated `-ing` participles `(?:and|or)\s+(?!(?:building|housing|heating|lighting|plumbing|wiring|roofing|cladding|ventilation|funding|reporting|monitoring|licensing|letting|renting|living|working|operating|standing|existing|ongoing|pending|binding|governing|remaining)(?:[-\s]|,))[a-z]+ing\b`.
  * Define `_POST_MEETING_GUARD_RE` extending `_NP_MODIFIER_GUARD_RE` with deictic appointment phrases `(?:this|next|last|every|each)\s+(?:morning|afternoon|evening|night|week|weekend|month|quarter|year|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b`, locative/manner appointment adverbs (`soon|later|here|there|online|remotely|together|privately|regularly`), and bare frequency adverbs when followed by a clause/coordination boundary `(?:weekly|monthly|daily|annually)\s+(?:and|or|at|in|on|to|for|with|about|regarding|before|after)\b`.
  * Use `(?!\s+{_POST_MEETING_GUARD_RE})` at the start of `_OBLIGATION_OBJECT_RE` and `(?!{_NP_MODIFIER_GUARD_RE})` inside the `{0,6}` modifier loop.

## `P01-T02`: Regression Tests and Verification

* Expand `test_c20_coordinated_obligation_modifiers_and_adverbs_refusal_precision` in `src/core/tests/test_regulatory_eval_gates_216.py` with `"Are we meeting our weekly safety requirements?"`, `"Are we meeting weekly safety requirements?"`, `"Is the team meeting this afternoon and planning safety obligations?"`, and `"Are we meeting weekly and discussing safety requirements?"`.
* Run `mypy`, `ruff check .`, `ruff format --check .`, `unittest discover -s tests -p 'test_*216*.py' -v`, and companion `src/core` tests.
