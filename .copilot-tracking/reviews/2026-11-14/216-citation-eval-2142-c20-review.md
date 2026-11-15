<!-- markdownlint-disable-file -->
# Review Record: Child Hardening Pass 20 for Issue #216 (`216-citation-eval-2142-c20`)

* Task ID: `216-citation-eval-2142-c20`
* Parent Task ID: `216-citation-eval-2142-c19`
* Date: `2026-11-14`
* Execution Status: `Complete`
* Outcome: `Defects found`

## Compared Artifacts

* Research: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c20-research.md`
* Plan: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c20-plan.md`
* Phase Details: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c20-phase-details.md`
* Plan Critique: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c20-plan-critique.md`
* Changes Record: `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c20-changes.md`
* Prior Review: `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c19-review.md`

## Findings

### `RV-053` (Medium): `_OBLIGATION_OBJECT_RE` and `_MEETING_ADVERBS_RE` omit `&` and `/` separators (`"health & safety obligations"`, `"legal and/or statutory obligations"`)

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_OBLIGATION_OBJECT_RE`). `"Are we meeting our damp health & safety obligations?"` and `"Are we meeting our legal and/or statutory obligations for this damp home?"` miss because `&` and `/` are outside `[a-z0-9',-]+`.
* Impact: Common `&` and `and/or` compliance modifier separators bypass `_OBLIGATION_OBJECT_RE`.
* Recommended destination: `rpi-implement` (via child task `216-citation-eval-2142-c21`: allow `&` and `/` inside `_OBLIGATION_OBJECT_RE` modifier tokens and `_MEETING_ADVERBS_RE` conjunctions).

### `RV-054` (Low): Intransitive `"meeting tomorrow and discussing ... obligations"` crosses coordinated participial clauses inside `_OBLIGATION_OBJECT_RE`

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_OBLIGATION_PREPOSITION_GUARD_RE`, `_OBLIGATION_OBJECT_RE`). `"Is the team meeting tomorrow and discussing damp legal obligations?"` matches `tomorrow and discussing damp legal` as 5 modifier tokens before `obligations`.
* Impact: Intransitive appointment `"meeting"` followed by a temporal/locative adverb or coordinated discussion participle can false-refuse.
* Recommended destination: `rpi-implement` (via child task `216-citation-eval-2142-c21`: add intransitive temporal/locative post-`meeting` adverbs and discussion/agenda participles to `_OBLIGATION_PREPOSITION_GUARD_RE`).

## Validation Coverage

* `mypy` (`0` errors in `318` files), `ruff check .`, `ruff format --check .`, `22` Issue #216 tests, and `58` companion `src/core` tests all passed; zero `.copilot-tracking` references exist in the 4 `src/core` files.

## Routed Follow-Up

1. Child task `216-citation-eval-2142-c21`: close `RV-053` and `RV-054` in `src/core`.
