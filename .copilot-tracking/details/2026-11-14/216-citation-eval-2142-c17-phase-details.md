<!-- markdownlint-disable-file -->
# Phase Details: Child Hardening Pass 17 for Issue #216 (`RV-044`..`RV-046`)

* Task ID: `216-citation-eval-2142-c17`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c17-plan.md`

<!-- P01 -->
## Phase 1: Close `RV-044`..`RV-046` in `src/core` and Verify

<!-- P01-T01 -->
### `P01-T01`: Update `regulatory_eval_gates.py` and `regulatory_chat.py`

* `regulatory_eval_gates.py`:
  * Add `(?:(?:all|any|each|every|some|both|most|every\s+one)\s+(?:of\s+)?)?` ahead of the determiner group in `_OBLIGATION_OBJECT_RE` (`RV-044`).
  * Restrict subordinate `(?:whether|if|that)` progressive `meeting` to follow compliance-inquiry verbs (`confirm|verify|certify|declare|state|say|check|tell\s+me|decide|know|advise|assess|determine|judge`) so WH-conditionals like `"What happens if the team is meeting statutory obligations..."` are not refused (`RV-046`).
  * Export `verify_reply_grounding(bundle: Mapping[str, Any], chat_reply: Mapping[str, Any]) -> bool` and reuse it inside `resolve_regulatory_surface` (`RV-045`).
* `regulatory_chat.py`:
  * In `RegulatoryChat.ask()`: when `self.enforce_ship_gate` is `True`, apply `canonical_refusal = refuse_question(raw_q) or refuse_question(masked)` before rendering and require `isinstance(reply, dict) and verify_reply_grounding(snap, reply)` (raising `ChatForbidden` before persisting or mutating thread state if grounding fails).

<!-- P01-T02 -->
### `P01-T02`: Add `test_c17`, Update `src/core/README.md`, and Verify

* Add `test_c17_quantified_obligation_refusal_wh_conditional_precision_and_ask_grounding_gate` (`none` removals; max `1` new test method).
