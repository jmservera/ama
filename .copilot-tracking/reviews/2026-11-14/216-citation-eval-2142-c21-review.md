<!-- markdownlint-disable-file -->
# Review Record: Child Hardening Pass 21 for Issue #216 (`216-citation-eval-2142-c21`)

* Task ID: `216-citation-eval-2142-c21`
* Parent Task ID: `216-citation-eval-2142-c20`
* Date: `2026-11-14`
* Execution Status: `Complete`
* Outcome: `Defects found`

## Compared Artifacts

* Research: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c21-research.md`
* Plan: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c21-plan.md`
* Phase Details: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c21-phase-details.md`
* Plan Critique: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c21-plan-critique.md`
* Changes Record: `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c21-changes.md`
* Prior Review: `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c20-review.md`

## Scope Note on `src/api`

* Wiring `src/api/src/zava_forward/api/server.py` and `src/agents` to `RegulatoryChat.ship_gated(...)` lies outside the explicit user-bounded `src/core` task boundary and is preserved as ranked follow-up item #1; inside `src/core`, `RegulatoryChat.ship_gated(...)`, automatic `enforce_ship_gate` activation whenever `ship_gate_comparison` is supplied, `RegulatoryChat.surface(...)`, and `resolve_regulatory_surface(...)` enforce `"if no measured value, ship cards alone"`.

## Findings

### `RV-055` (Medium): `_OBLIGATION_PREPOSITION_GUARD_RE` conflates post-verb appointment time phrases with NP frequency adjectives (`"our weekly safety requirements"`) and misses deictic time phrases + coordinated `-ing` clauses (`"meeting this afternoon and planning safety obligations"`)

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_OBLIGATION_PREPOSITION_GUARD_RE`, `_OBLIGATION_OBJECT_RE`). Blocking `weekly|monthly|daily` at every NP modifier position blocks `"Are we meeting our weekly safety requirements?"`, while `"Is the team meeting this afternoon and planning safety obligations?"` slips past because `this afternoon` and `and planning` were not excluded.
* Impact: Frequency-qualified obligations (`weekly`/`monthly`/`daily` after a determiner) can miss refusal, while deictic appointment phrases (`this afternoon and planning...`) can false-refuse.
* Recommended destination: `rpi-implement` (via child task `216-citation-eval-2142-c22`: separate `_POST_MEETING_GUARD_RE`—checked immediately after the verb `meeting`, including deictic time phrases `(?:this|next|last|every)\s+(?:morning|afternoon|evening|night|week|month|quarter|year|...)` and bare temporal/locative adverbs—from `_NP_MODIFIER_GUARD_RE`—prepositions, subordinators, finite auxiliaries, and coordinated `-ing` verb phrases `(?:and|or)\s+(?!...)[a-z]+ing\b`—so frequency adjectives inside NPs refuse while appointment phrases stay allowed).

## Validation Coverage

* `mypy` (`0` errors in `318` files), `ruff check .`, `ruff format --check .`, `22` Issue #216 tests, and `58` companion `src/core` tests all passed; zero `.copilot-tracking` references exist in the 4 `src/core` files.

## Routed Follow-Up

1. Child task `216-citation-eval-2142-c22`: close `RV-055` in `src/core`.
