<!-- markdownlint-disable-file -->
# Review Log: Issue #216 Child Hardening Pass 10 (`216-citation-eval-2142-c10`)

* Task ID: `216-citation-eval-2142-c10`
* Parent Task ID: `216-citation-eval-2142-c9`
* Date: `2026-11-14`
* Execution Status: `Complete`
* Outcome: `Defects found`

## Compared Artifacts

* Research: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c10-research.md`
* Plan: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c10-plan.md`
* Phase Details: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c10-phase-details.md`
* Plan Critique: `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c10-plan-critique.md`
* Changes Log: `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c10-changes.md`

## Verified Prior Findings (`RV-018`..`RV-022`)

* `RV-018` (`PC-001`, `PC-002`): Verified closed — `_canonical_refusal_reason` enforces exact unstripped `_is_utf8_str` membership in `_CANONICAL_REFUSAL_REASONS` across `grade_chat_turn`, `_classify_refusal_confusion`, `evaluate_adversarial_prompts`, and `evaluate_citation_and_refusal_gates`, and `render_extractive_answer` normalizes non-canonical bundle refusal text to `EMPTY_BUNDLE_REFUSAL`.
* `RV-019` (`PC-003`): Verified closed — `_inspect_bundle_surface` unifies explicit-refusal triggers and whole-bundle `sources`/`facts`/`cards` validation across `deterministic_rule_cards`, `render_extractive_answer`, and `_expected_from_bundle`.
* `RV-021` (`PC-004`): Verified closed — `_aware_dt` and `_usage_valid` catch `OverflowError` on UTC boundary timestamps (`0001-01-01T00:00:00+23:59`, `9999-12-31T23:59:59-23:59`).
* `RV-022` (`PC-004`): Verified closed — `RegulatoryChat.surface` guards `self.render(snap)` and `offline_usage(...)` without mutating `rendered` and degrades cleanly to `cards_only`.
* Subagent note disposition (`RegulatoryChat.ask`): Not a defect — `RegulatoryChat.ask` is the offline evaluation/turn-execution method tested by `test_regulatory_chat.py` and required to execute the graded/adversarial turns before `compare_chat_against_rule_cards` runs, whereas `RegulatoryChat.surface` / `resolve_regulatory_surface` are the Issue #216 shipping surface selectors (HTTP route wiring belongs to `src/api`, outside `src/core`). Pre-existing `.copilot-tracking` strings in `cutover_audit.py`, `test_cutover_audit.py`, and `test_live_doc_links.py` are repository audit/link-checker directory exclusions on `main`; zero `.copilot-tracking` strings exist in Issue #216 files.

## Findings

* `RV-023` (High — Defect, route: `rpi-implement`): Provision-specific card linkage in `RegulatoryChat.bundle` and `_active_cards_link_provisions` (`src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/src/zava_forward/core/regulatory_eval_gates.py`). `RegulatoryChat.bundle` omits `card["provisions"]` (`provision_ids`) from emitted card dicts and `_active_cards_link_provisions` matches provisions only by base `source_id`, so two active cards citing different provisions of the same source (e.g. `src@v1#0001` vs `src@v1#0002`) each receive both provision links instead of their own exact provision links.
* `RV-024` (High — Defect, route: `rpi-implement`): Unflagged version or duplicate-ID contradiction in `_inspect_bundle_surface` and `grade_chat_turn` (`src/core/src/zava_forward/core/regulatory_eval_gates.py`). When a bundle sets `conflict=False` (`kind="answer"`) while containing conflicting source versions for the same base `source_id` (e.g. `src@v1#0001` and `src@v2#0001`) or duplicate provision/card/fact IDs, active validation trusts `conflict=False` instead of failing closed.
* `RV-025` (Medium — Defect, route: `rpi-implement`): `grade_chat_turn` overwrites `expected_facts` and `expected_cards` with `[]` before validating `expected_kind == "refused"` (`src/core/src/zava_forward/core/regulatory_eval_gates.py`), allowing malformed or non-empty `expected["facts"]` / `expected["cards"]` on refused (and non-empty `expected["facts"]` on conflict) expectations to pass `grade_chat_turn`.

## Validation Coverage

* `cd src/core && python3 -m mypy`: `0` issues in `318` source files.
* `cd src/core && python3 -m ruff check .`: Passed.
* `cd src/core && python3 -m ruff format --check .`: `265` files formatted.
* `cd src/core && python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `13/13` tests passed.
* `cd src/core && PYTHONPATH="src:tests" python3 -m unittest test_regulatory_chat test_gates test_live_doc_links -q`: `58/58` tests passed.

## Routing Summary

* Route `RV-023`, `RV-024`, and `RV-025` to automatic child RPI task `216-citation-eval-2142-c11` (`rpi-implement` via full child RPI loop in `src/core`).
* Retain cross-package `src/api` route wiring and `src/agents` helper deduplication as out-of-scope follow-up items.
