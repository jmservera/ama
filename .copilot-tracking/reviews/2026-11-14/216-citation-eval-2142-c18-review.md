<!-- markdownlint-disable-file -->
# Review Record: Child Hardening Pass 18 for Issue #216 (`216-citation-eval-2142-c18`)

* Task ID: `216-citation-eval-2142-c18`
* Parent Task ID: `216-citation-eval-2142-c17`
* Date: `2026-11-14`
* Execution Status: `Complete`
* Outcome: `Defects found`

## Compared Artifacts

* Research: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c18-research.md`
* Plan: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c18-plan.md`
* Phase Details: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c18-phase-details.md`
* Plan Critique: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c18-plan-critique.md`
* Changes Record: `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c18-changes.md`
* Prior Review: `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c17-review.md`

## Findings

### `RV-049` (Medium): Progressive `meeting` pattern lacks general `-ly` adverb support before `meeting` and its trailing gerund branch crosses `"what happens if"` after `"check"`

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_REFUSAL_PATTERNS[1]`). `"whether the team is adequately meeting statutory obligations"` misses because only five fixed adverbs were listed before `meeting`, while `"Please check what happens if the team is meeting statutory obligations."` false-refuses because the legacy gerund branch `check(?:ing)?(?:\s+whether|\s+if)?\b[^.;!?]{0,40}\bmeeting` crosses `"what happens if"`.
* Impact: General `-ly` adverbs before `meeting` can bypass indirect `whether` refusal, and `"Please check what happens if..."` false-refuses.
* Recommended destination: `rpi-implement` (via child task `216-citation-eval-2142-c19`: allow general adverbs `_MEETING_ADVERBS_RE` before `meeting`, forbid WH/conditional subordinators across all progressive pre-verb spans `_NON_WH_COND_SPAN_RE`, support optional `that` after `confirm`/`verify`/`certify`/`declare`/`state`/`say`, and restrict the direct gerund branch so it cannot span across `what happens if`).

### `RV-050` (Medium): Renderer bundle-mutation test in `test_regulatory_eval_gates_216.py` used an incomplete reply dict instead of `render_extractive_answer(mutated_snap)`

* Evidence: `src/core/tests/test_regulatory_eval_gates_216.py` (`test_c18_renderer_bundle_mutation_isolation_and_whether_vs_prefaced_wh_if_precision`). Returning a hand-built dict without `sections` fails `grade_chat_turn` even without `copy.deepcopy(snap)` isolation.
* Impact: Regression test would not catch removal of `copy.deepcopy(snap)` if a renderer mutates a supported `snap` in place and returns `render_extractive_answer(snap)`.
* Recommended destination: `rpi-implement` (via child task `216-citation-eval-2142-c19`: mutate a supported `snap` in place inside `_tampering_render` and return `render_extractive_answer(snap)` on a supported question so the test passes if and only if `copy.deepcopy(snap)` isolates verification in both `ask()` and `surface()`).

## Validation Coverage

* `mypy` (`0` errors in `318` files), `ruff check .`, `ruff format --check .`, `21` Issue #216 tests, and `58` companion `src/core` tests all passed; zero `.copilot-tracking` references exist in the 4 `src/core` files.

## Routed Follow-Up

1. Child task `216-citation-eval-2142-c19`: close `RV-049` and `RV-050` in `src/core`.
