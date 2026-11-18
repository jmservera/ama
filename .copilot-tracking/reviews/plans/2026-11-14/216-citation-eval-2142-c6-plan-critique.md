<!-- markdownlint-disable-file -->
# Plan Critique: Issue #216 Child Hardening Pass 6 (`216-citation-eval-2142-c6`)

* Task ID: 216-citation-eval-2142-c6
* Critique date: 2026-11-14
* Execution status: Complete
* Verdict: Revise

## Findings

* `PC-001` (High, Blocking): Guard all `prompts` conversions (`case_set_digest` and `evaluate_citation_and_refusal_gates`) against non-iterable `prompts` (`prompts=object()`) and record a dataset gap when `prompts` is not a sequence of strings.
  * Disposition: Applied directly to `216-citation-eval-2142-c6-plan.md` and `216-citation-eval-2142-c6-phase-details.md`.
* `PC-002` (High, Blocking): Guard non-`Mapping` elements inside `cases` (such as `[None]`) in `case_set_digest`, `evaluated_outputs_digest`, and `evaluate_citation_and_refusal_gates` so no entrypoint raises `AttributeError`.
  * Disposition: Applied directly to `216-citation-eval-2142-c6-plan.md` and `216-citation-eval-2142-c6-phase-details.md`.
* `PC-003` (High, Blocking): Require exact `type(v) is str` in `_nonblank_str`, `set_name`, `arm`, `expected_kind`, and `actual_kind` before dictionary/set membership so unhashable `str` subclasses cannot raise `TypeError`.
  * Disposition: Applied directly to `216-citation-eval-2142-c6-plan.md` and `216-citation-eval-2142-c6-phase-details.md`.
* `PC-004` (High, Blocking): Normalize `citations` and `cards` sequences to plain lists/dicts inside `grade_chat_turn` and `_exact_card_links_match` so equivalent `tuple` and `list` values score identically across both answer and refusal turns.
  * Disposition: Applied directly to `216-citation-eval-2142-c6-plan.md` and `216-citation-eval-2142-c6-phase-details.md`.
* `PC-005` (Medium, Blocking): Normalize valid aware `datetime` `now` values via `.isoformat()` while keeping `now is None or (isinstance(now, datetime) and _aware_dt(now) is not None) or type(now) is str` valid, and test `datetime` vs ISO `str` replay parity.
  * Disposition: Applied directly to `216-citation-eval-2142-c6-plan.md` and `216-citation-eval-2142-c6-phase-details.md`.
