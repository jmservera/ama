<!-- markdownlint-disable-file -->
# Review Record: Child Hardening Pass 16 for Issue #216 (`216-citation-eval-2142-c16`)

* Task ID: `216-citation-eval-2142-c16`
* Parent Task ID: `216-citation-eval-2142-c15`
* Date: `2026-11-14`
* Execution Status: `Complete`
* Outcome: `Defects found`

## Compared Artifacts

* Research: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c16-research.md`
* Plan: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c16-plan.md`
* Phase Details: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c16-phase-details.md`
* Plan Critique: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c16-plan-critique.md`
* Changes Record: `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c16-changes.md`
* Prior Review: `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c15-review.md`

## Closure Verification

* `RV-042` (exact UTC-instant `_aware_dt` observation bounds) and `RV-043` (`_UnsetType` automatic `enforce_ship_gate` + `RegulatoryChat.ship_gated`) are verified closed; zero `.copilot-tracking` references exist in any of the 4 Issue #216 files.
* Independent read-only `rubber-duck` verification surfaced three remaining refinements (`RV-044`..`RV-046`) routed to child task `216-citation-eval-2142-c17`.

## Findings

### `RV-044` (High): `_OBLIGATION_OBJECT_RE` misses quantified `of` determiner phrases such as `"all of our statutory obligations"`

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_OBLIGATION_OBJECT_RE`). `"Are we meeting all of our statutory obligations for this damp home?"` is missed because `of` is blocked by `_OBLIGATION_PREPOSITION_GUARD_RE` inside modifiers after `all`.
* Impact: Quantified determiner phrases (`all of our`, `any of the`, `each of these`, `every one of its`) bypass obligation-satisfaction refusal.
* Recommended destination: `rpi-implement` (via child task `216-citation-eval-2142-c17`: allow optional quantifier `(?:(?:all|any|each|every|some|both|most|every\s+one)\s+(?:of\s+)?)?` before the determiner slot in `_OBLIGATION_OBJECT_RE` while retaining `(?!\s+{_OBLIGATION_PREPOSITION_GUARD_RE}\b)` directly after the verb).

### `RV-045` (High): Ship-gated `RegulatoryChat.ask()` does not enforce canonical `refuse_question` or `verify_reply_grounding` before persisting/returning a rendered reply

* Evidence: `src/core/src/zava_forward/core/regulatory_chat.py` (`ask`). While `surface()` enforces canonical `refuse_question` and `resolve_regulatory_surface` (`grade_chat_turn` against `_expected_from_bundle`), `ask()` under `self.enforce_ship_gate == True` trusts `self.refuse` and `self.render` without checking `verify_reply_grounding(snap, reply)`.
* Impact: Under `enforce_ship_gate == True`, an injected buggy or ungrounded renderer could persist and return an ungrounded reply on `ask()` even though `surface()` rejects it.
* Recommended destination: `rpi-implement` (via child task `216-citation-eval-2142-c17`: expose `verify_reply_grounding(bundle, chat_reply)` in `regulatory_eval_gates.py` and, when `self.enforce_ship_gate` is `True` in `RegulatoryChat.ask()`, enforce canonical `refuse_question` on `snap` and raise `ChatForbidden` before persistence if `verify_reply_grounding(snap, reply)` fails).

### `RV-046` (Low): Subordinate `\b(?:whether|if|that)\s+` inside WH-clauses falsely refuses informational conditional questions

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_REFUSAL_PATTERNS[1]`). `"What happens if the team is meeting statutory obligations for this damp home?"` matches the unanchored `\b(?:whether|if|that)\s+` branch despite starting with `"What"`.
* Impact: Informational conditional WH-questions false-refuse unless subordinate `whether|if|that` is tied to compliance-inquiry verbs (`tell me`, `confirm`, `verify`, `check`, `decide`, `know`, `ask`, `advise`, `say`, `state`) rather than bare WH-conditionals.
* Recommended destination: `rpi-implement` (via child task `216-citation-eval-2142-c17`: anchor declarative progressive `meeting` to non-WH clause starts and handle subordinate `whether|if|that` via explicit compliance-inquiry verbs).

## Validation Coverage

* `mypy` (`0` errors in `318` files), `ruff check .`, `ruff format --check .`, `19` Issue #216 tests, and `58` companion `src/core` tests all passed.

## Routed Follow-Up

1. Child task `216-citation-eval-2142-c17`: close `RV-044`..`RV-046` in `src/core`.
