<!-- markdownlint-disable-file -->
# Changes Record: Child Hardening Pass 22 for Issue #216 (`RV-055`)

* Task ID: `216-citation-eval-2142-c22`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c22-plan.md`
* Phase Details Path: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c22-phase-details.md`
* Critique Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c22-plan-critique.md`
* Status: `Completed`

## Summary

Completed `P01-T01` and `P01-T02` in `src/core` closing `RV-055`:

### `P01-T01`: Structural Separation of Post-Verb Appointment Guards and NP Modifier Guards (`RV-055`)

* Separated `_NP_MODIFIER_GUARD_RE` (prepositions, clause subordinators, finite auxiliaries, non-possessive bare temporal nouns, and general coordinated `-ing` participial verb phrases excluding allowed domain `-ing` noun/adjective modifiers in `_ALLOWED_ING_NP_MODIFIERS_RE`) from `_POST_MEETING_GUARD_RE` (extending `_NP_MODIFIER_GUARD_RE` immediately after `meeting` with locative/manner appointment adverbs, non-possessive deictic temporal phrases `(?:this|next|last|every|each)\s+(?:morning|afternoon|evening|...)`, and bare frequency adverbs followed by a coordination or prepositional boundary) in `src/core/src/zava_forward/core/regulatory_eval_gates.py`.
* Applied `(?!\s+{_POST_MEETING_GUARD_RE})` at the start of `_OBLIGATION_OBJECT_RE` and `(?!{_NP_MODIFIER_GUARD_RE})` inside the `{0,6}` NP modifier loop so frequency/possessive obligation NPs (`"our weekly safety requirements"`, `"weekly safety requirements"`, `"this year's statutory obligations"`) refuse while intransitive appointment phrases (`"meeting this afternoon and planning safety obligations"`, `"meeting weekly and discussing safety requirements"`) stay allowed.

### `P01-T02`: Regression Tests and Verification

* Expanded `test_c20_coordinated_obligation_modifiers_and_adverbs_refusal_precision` in `src/core/tests/test_regulatory_eval_gates_216.py` covering `"Are we meeting our weekly safety requirements?"`, `"Are we meeting weekly safety requirements?"`, `"Are we meeting this year's statutory obligations?"`, `"Is the team meeting this afternoon and planning safety obligations?"`, and `"Are we meeting weekly and discussing safety requirements?"`.
* Verified in `src/core` and repository root:
  * `python3 -m mypy`: `Success: no issues found in 318 source files`
  * `python3 -m ruff check src tests`: `All checks passed!`
  * `python3 -m ruff format --check src tests`: `264 files already formatted`
  * `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `Ran 22 tests ... OK`
  * `PYTHONPATH=src:tests python3 -m unittest tests/test_regulatory_chat.py tests/test_gates.py tests/test_live_doc_links.py -q`: `Ran 58 tests ... OK`
  * `python3 tools/rename-zava-tests.py`: `Ran 25 tests ... OK`

## Blockers and Remaining Work

* Blockers: None.
* Remaining active-plan work: None (`P01`, `P01-T01`, and `P01-T02` completed).

## Follow-Up Items

* Wire `src/api` and `src/agents` to `RegulatoryChat.ship_gated(...)` in a separate multi-package PR outside `src/core`.
* Populate ratified finance policy values once `BRD OD-51` is closed.
