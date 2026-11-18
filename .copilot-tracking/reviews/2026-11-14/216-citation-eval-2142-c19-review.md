<!-- markdownlint-disable-file -->
# Review Record: Child Hardening Pass 19 for Issue #216 (`216-citation-eval-2142-c19`)

* Task ID: `216-citation-eval-2142-c19`
* Parent Task ID: `216-citation-eval-2142-c18`
* Date: `2026-11-14`
* Execution Status: `Complete`
* Outcome: `Defects found`

## Compared Artifacts

* Research: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c19-research.md`
* Plan: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c19-plan.md`
* Phase Details: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c19-phase-details.md`
* Plan Critique: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c19-plan-critique.md`
* Changes Record: `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c19-changes.md`
* Prior Review: `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c18-review.md`

## Closure Verification

* `RV-044`..`RV-050` are verified closed, including schema-valid bundle-mutation isolation across `RegulatoryChat.ask()` and `RegulatoryChat.surface()`, and zero `.copilot-tracking` references exist across the 4 `src/core` files.
* Independent read-only `rubber-duck` review identified two coordinated-modifier refusal gaps (`RV-051`, `RV-052`) routed to child task `216-citation-eval-2142-c20`.

## Findings

### `RV-051` (Medium): `_OBLIGATION_OBJECT_RE` caps pre-noun modifiers at 2 tokens (`{0,2}`), missing coordinated modifiers such as `"legal and statutory obligations"`

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_OBLIGATION_OBJECT_RE`). `"Are we meeting all of our legal and statutory obligations?"` has 3 modifier tokens (`legal`, `and`, `statutory`) before `obligations`, exceeding `{0,2}`.
* Impact: Multi-word or coordinated obligation modifiers (`"legal and statutory"`, `"damp, mould, and building-safety"`) bypass `_OBLIGATION_OBJECT_RE`.
* Recommended destination: `rpi-implement` (via child task `216-citation-eval-2142-c20`: widen `_OBLIGATION_OBJECT_RE` modifier slot to `{0,6}` over `[a-z0-9',-]+` while guarding out prepositions, clause subordinators, and finite auxiliaries in `_OBLIGATION_PREPOSITION_GUARD_RE`).

### `RV-052` (Medium): `_MEETING_ADVERBS_RE` omits coordinating conjunctions (`and`/`or`) and punctuation between adverbs before `meeting`

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_MEETING_ADVERBS_RE`). `"Please confirm whether the team is adequately and consistently meeting statutory obligations."` misses because `and` between `adequately` and `consistently` is not matched by `_MEETING_ADVERBS_RE`.
* Impact: Coordinated adverbial phrases (`"adequately and consistently"`, `"not adequately or consistently"`) before `meeting` bypass progressive compliance refusal.
* Recommended destination: `rpi-implement` (via child task `216-citation-eval-2142-c20`: extend `_MEETING_ADVERBS_RE` to allow optional comma and coordinating `and|or|nor|but` across up to 4 adverbial units, and widen `_NON_WH_COND_SPAN_RE` to `{1,10}` tokens for coordinated subjects).

## Validation Coverage

* `mypy` (`0` errors in `318` files), `ruff check .`, `ruff format --check .`, `21` Issue #216 tests, and `58` companion `src/core` tests all passed.

## Routed Follow-Up

1. Child task `216-citation-eval-2142-c20`: close `RV-051` and `RV-052` in `src/core`.
