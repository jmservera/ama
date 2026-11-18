<!-- markdownlint-disable-file -->
# RPI Review: Issue #216 Child Hardening Pass 6 (`216-citation-eval-2142-c6`)

## Metadata

* Task ID: 216-citation-eval-2142-c6
* Review date: 2026-11-14
* Execution status: Complete
* Outcome: Defects found

## Compared Artifacts

* Research: .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c6-research.md
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c6-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c6-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c6-plan-critique.md
* Changes record: .copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c6-changes.md
* Prior parent review: .copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c5-review.md

## Boundary and Reconciliation Assessment

* All three `c5` review items (`RV-001`..`RV-003`) are resolved and regression-tested.
* Independent `rubber-duck` review identified six remaining `src/core` hardening gaps (`RV-002`..`RV-007`) and one cross-package `src/api` integration item (`RV-001`, outside the user-bounded `src/core` delivery scope; we will also add a `RegulatoryChat.surface(...)` helper in `src/core` that defaults to `cards_only` while routing `src/api/server.py` wiring as a distinct out-of-scope follow-up).

## Findings

### RV-001 (Medium) - HTTP endpoint wiring in `src/api` calls `ask` directly without selector gating

* Evidence: `src/api/src/zava_forward/api/server.py` calls `RegulatoryChat.ask` directly; `src/api` is outside the user-bounded `src/core` delivery scope for this task, while `src/core`'s `RegulatoryChat` can additionally expose a gated `surface(...)` helper backed by `resolve_regulatory_surface` (defaulting to `cards_only`).
* Destination: Distinct follow-up item (`src/api` route integration); `src/core` `RegulatoryChat.surface(...)` helper routed to `rpi-implement` (`216-citation-eval-2142-c7`)

### RV-002 (High) - Missing source, fact, or card provenance fields can match `None == None` in `grade_chat_turn`

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_source_matches`, `_fact_matches`, `grade_chat_turn`). Comparing fields via `.get(key)` without requiring valid non-blank active provenance (`status`, `version`, `effective`, `retrieved`, `hash`, `review_status`, `completeness`, `exercise`, and active card metadata) allows stripped dicts with `{id, text, link}` to pass `citation_validity`.
* Destination: `rpi-implement` (child task `216-citation-eval-2142-c7`)

### RV-003 (High) - Refusal accuracy gate can pass on an answer-only dataset without a tested refusal chat turn

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`evaluate_citation_and_refusal_gates`, `_verify_agreed_gates_report`). `dataset_gaps` checks non-empty `graded` and `adversarial` buckets without requiring at least one supported answer turn in `graded` and at least one refused turn in `adversarial`.
* Destination: `rpi-implement` (child task `216-citation-eval-2142-c7`)

### RV-004 (High) - Paired observations are not cryptographically bound to evaluated case IDs and surface versions

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_score_paired_observations`, `compare_chat_against_rule_cards`). Arbitrary `task` strings can establish measured lift without binding each paired observation to an evaluated `case_id` and its `cards`/`chat` surface digest (`observation_surface_digest`).
* Destination: `rpi-implement` (child task `216-citation-eval-2142-c7`)

### RV-005 (High) - Altered baseline rule cards (`status="held"` or modified `safe_default`) pass `_exact_card_links_match`

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_exact_card_links_match`). Checking only `id` and `link` allows modified card status, actions, freshness, or provision metadata in `paired_cards` to pass structural comparison.
* Destination: `rpi-implement` (child task `216-citation-eval-2142-c7`)

### RV-006 (Medium) - Malformed source dicts (`sources=[{}]`) raise `KeyError` and lone UTF-16 surrogates raise `UnicodeEncodeError`

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`render_extractive_answer`, `_source_matches`, `_canon_json`). Direct indexing `src["id"]` raises `KeyError` on `{}` and `quote(...)` / `.encode("utf-8")` raises `UnicodeEncodeError` on lone surrogates (`"\ud800"`).
* Destination: `rpi-implement` (child task `216-citation-eval-2142-c7`)

### RV-007 (Medium) - Non-string elements in `prompts` (`prompts=[123]` or `[*ADVERSARIAL_PROMPTS, 123]`) do not record a `dataset_gaps` entry

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`evaluate_adversarial_prompts`, `evaluate_citation_and_refusal_gates`). Filtering `prompts` to `str` silently drops non-string elements instead of recording a dataset gap and failing both gates.
* Destination: `rpi-implement` (child task `216-citation-eval-2142-c7`)

## Validation Coverage

* `python3 -m mypy`: PASS (318 source files)
* `python3 -m ruff check .` and `python3 -m ruff format --check .`: PASS (265 files)
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: PASS (9 tests)

## Plan Follow-Up Assessment

* Cross-package `src/api` route integration (`RV-001`) and `src/agents` helper deduplication remain distinct follow-ups outside `src/core`.

## Routing Summary

* Route `RV-002`..`RV-007` plus `RegulatoryChat.surface(...)` in `src/core` to child RPI hardening loop `216-citation-eval-2142-c7`.
