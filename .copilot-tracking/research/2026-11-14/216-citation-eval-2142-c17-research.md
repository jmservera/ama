<!-- markdownlint-disable-file -->
# Research Synthesis: Child Hardening Pass 17 for Issue #216 (`RV-044`..`RV-046`)

* Task ID: `216-citation-eval-2142-c17`
* Parent Task ID: `216-citation-eval-2142-c16`
* Date: `2026-11-14`
* Research Disposition: `executed`
* Planning Readiness: `Ready`

## Findings

1. **`RV-044` (`_OBLIGATION_OBJECT_RE` quantified `of` determiners)**:
   * Adding optional `(?:(?:all|any|each|every|some|both|most|every\s+one)\s+(?:of\s+)?)?` ahead of `(?:our\s+|the\s+|this\s+|these\s+|those\s+|its\s+|their\s+|my\s+|your\s+|a\s+|an\s+|any\s+|all\s+|every\s+)?` in `_OBLIGATION_OBJECT_RE` matches `"all of our statutory obligations"`, `"any of the legal duties"`, and `"each of these safety standards"`, while `(?!\s+{_OBLIGATION_PREPOSITION_GUARD_RE}\b)` directly after `meeting` continues to reject `"a meeting of the board"` or `"a meeting about statutory obligations"`.
2. **`RV-045` (Ship-gated `RegulatoryChat.ask()` canonical refusal and bundle-grounding verification)**:
   * Exposing `verify_reply_grounding(bundle, chat_reply) -> bool` in `regulatory_eval_gates.py` (reusing `grade_chat_turn(chat_reply, _expected_from_bundle(bundle))`) lets `RegulatoryChat.ask()` enforce canonical `refuse_question(raw_q) or refuse_question(masked)` on the retrieved bundle AND reject any ungrounded `self.render(snap)` output with `ChatForbidden` before persisting or returning the turn whenever `self.enforce_ship_gate` is `True`.
3. **`RV-046` (Informational conditional WH-questions)**:
   * Anchoring declarative progressive `meeting` to `(?:^|[.;!?]\s*)\s*(?!what\b|which\b|when\b|where\b|how\b|who\b|why\b)[^.;!?]{1,55}\b(?:is|are|was|were)\s+(?:not\s+|currently\s+|fully\s+|still\s+|already\s+)?meeting` and restricting subordinate `whether|if|that` to explicit compliance-inquiry verbs (`confirm|verify|certify|declare|state|say|check|tell\s+me|decide|know|advise|assess|determine|judge` + `(?:whether|if|that)\s+[^.;!?]{1,50}\b(?:is|are|was|were)\s+(?:not\s+|currently\s+|fully\s+|still\s+|already\s+)?meeting`) preserves `"Can you tell me whether the contractor is meeting safety standards?"` while allowing `"What happens if the team is meeting statutory obligations for this damp home?"`.
