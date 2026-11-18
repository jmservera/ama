<!-- markdownlint-disable-file -->
# Research Synthesis: Child Hardening Pass 18 for Issue #216 (`RV-047`..`RV-048`)

* Task ID: `216-citation-eval-2142-c18`
* Parent Task ID: `216-citation-eval-2142-c17`
* Date: `2026-11-14`
* Research Disposition: `executed`
* Planning Readiness: `Ready`

## Scope and Evidence

Targeted hardening inside `src/core` for the two findings surfaced during `c17` Review (`.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c17-review.md`):

1. `RV-047` (High — Mutable bundle passed into `self.render(...)` before grounding verification in `RegulatoryChat.ask()` and `RegulatoryChat.surface()`):
   * Passing `copy.deepcopy(snap)` to `self.render(copy.deepcopy(snap))` and deep-copying `reply` / `rendered` prevents any in-place mutation of `snap` by a renderer callback from altering the bundle inspected by `verify_reply_grounding(snap, reply)` or `resolve_regulatory_surface(snap, resolved_comparison, chat_reply=candidate_reply)`.
2. `RV-048` (Medium — Indirect `whether` compliance inquiries vs polite-prefaced WH-conditional questions in `_REFUSAL_PATTERNS[1]`):
   * In English syntax, `whether <subject> is/are/was/were meeting <obligation>` is always an indirect polar compliance inquiry (including `"What is the answer as to whether the team is meeting statutory obligations?"` and `"Tell us whether we are meeting our duties"`), whereas `if <subject> is/are/was/were meeting <obligation>` is an inquiry only after an inquiry verb/object (`tell me/us if`, `check if`, `confirm if`, `verify if`, `ask if`, `see if`, `know if`, `decide if`, `determine if`, `assess if`, `advise if`, `say if`, `state if`) and is otherwise a conditional antecedent (`"What happens if..."`, `"Could you explain what happens if..."`).
   * Restricting the declarative progressive pre-verb span so it cannot cross WH or conditional subordinators (`what|which|when|where|how|who|why|if|unless|whenever`) prevents `"Could you explain what happens if the team is meeting statutory obligations?"` from matching as a declarative assertion while preserving `"Our team is meeting statutory obligations."`.
