<!-- markdownlint-disable-file -->
# Review Record: Child Hardening Pass 17 for Issue #216 (`216-citation-eval-2142-c17`)

* Task ID: `216-citation-eval-2142-c17`
* Parent Task ID: `216-citation-eval-2142-c16`
* Date: `2026-11-14`
* Execution Status: `Complete`
* Outcome: `Defects found`

## Compared Artifacts

* Research: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c17-research.md`
* Plan: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c17-plan.md`
* Phase Details: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c17-phase-details.md`
* Plan Critique: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c17-plan-critique.md`
* Changes Record: `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c17-changes.md`
* Prior Review: `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c16-review.md`

## Closure Verification

* `RV-044` (quantified `of` determiner phrases in `_OBLIGATION_OBJECT_RE`) is verified closed, and zero `.copilot-tracking` references exist across the 4 Issue #216 `src/core` files.
* Independent read-only `rubber-duck` review identified two remaining refinements (`RV-047`, `RV-048`) routed to child task `216-citation-eval-2142-c18`.

## Findings

### `RV-047` (High): `RegulatoryChat.ask()` and `RegulatoryChat.surface()` pass a mutable `snap` bundle directly to `self.render(snap)` before grounding verification

* Evidence: `src/core/src/zava_forward/core/regulatory_chat.py` (`ask`, `surface`). Calling `self.render(snap)` hands the live bundle reference to an injected renderer before `verify_reply_grounding(snap, reply)` or `resolve_regulatory_surface(snap, ...)` runs; a renderer that mutates `snap` in place (for example rewriting `snap["refusal"]` or `snap["sources"]`) can spoof bundle-grounding verification.
* Impact: In-place bundle mutation inside a buggy or adversarial `render` callback could bypass `verify_reply_grounding` / `resolve_regulatory_surface`.
* Recommended destination: `rpi-implement` (via child task `216-citation-eval-2142-c18`: pass `copy.deepcopy(snap)` into `self.render(...)` and copy `reply` in both `ask()` and `surface()` so verification always evaluates against an unmutated `snap`, and add regression tests for renderer bundle mutation).

### `RV-048` (Medium): Progressive `meeting` refusal pattern misses indirect `whether` compliance inquiries inside WH-questions and over-matches polite-prefaced informational `what happens if` questions

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_REFUSAL_PATTERNS[1]`). `"What is the answer as to whether the team is meeting statutory obligations?"` misses because `whether` required an immediately preceding inquiry verb, while `"Could you explain what happens if the team is meeting statutory obligations?"` false-refuses because `[^.;!?]{1,55}` in the clause-initial declarative branch crosses `"what happens if"`.
* Impact: Indirect `whether` compliance questions inside WH-clauses can slip past refusal, and polite-prefaced informational WH-conditionals can false-refuse.
* Recommended destination: `rpi-implement` (via child task `216-citation-eval-2142-c18`: forbid WH/conditional subordinators (`what|which|when|where|how|who|why|if|unless|whenever`) inside the declarative pre-verb span, match indirect polar `\bwhether\s+...meeting` compliance clauses regardless of outer WH framing, and require an inquiry verb/object before subordinate `(?:if|that)`).

## Validation Coverage

* `mypy` (`0` errors in `318` files), `ruff check .`, `ruff format --check .`, `20` Issue #216 tests, and `58` companion `src/core` tests all passed.

## Routed Follow-Up

1. Child task `216-citation-eval-2142-c18`: close `RV-047` and `RV-048` in `src/core`.
