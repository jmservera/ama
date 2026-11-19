# RPI Review: Child Hardening Pass 11 for Issue #216 (`RV-023`..`RV-025`)

* Task ID: `216-citation-eval-2142-c11`
* Date: `2026-11-14`
* Execution Status: `Complete`
* Outcome: `Defects found`

## Compared Artifacts

* Research: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c11-research.md`
* Plan: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c11-plan.md`
* Phase Details: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c11-phase-details.md`
* Plan Critique: `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c11-plan-critique.md`
* Changes Record: `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c11-changes.md`

## Closure Verification (`RV-023`..`RV-025` & `PC-001`..`PC-004`)

* `RV-023` + `PC-001` + `PC-004` — Resolved: `RegulatoryChat.bundle` emits `"provision_ids"` per card and clears `sources`/`facts`/`cards`/`conflict` immediately on mid-loop refusals; `_card_provenance_valid`, `_active_cards_link_provisions`, `_conflict_collections_consistent`, and `grade_chat_turn` validate exact per-card `provision_ids` linkage and reject ambiguous multi-provision fallback.
* `RV-024` + `PC-003` — Resolved: `_active_bundle_nonconflicting` rejects unflagged `conflict=False` version contradictions and duplicate source/fact/card IDs across `_inspect_bundle_surface` and both `citation_validity` and `answer_contract` in `grade_chat_turn`.
* `RV-025` + `PC-002` + `PC-004` — Resolved: `grade_chat_turn` validates `expected` collections unconditionally without pre-zeroing and enforces emptiness on `refused`/`conflict` turns; `_classify_refusal_confusion` and `_baseline_projection_matches` verify `expected` self-consistency before allowing `"false_refusal"` or non-answer baseline parity.
* Confirmed zero `.copilot-tracking` references in `regulatory_chat.py`, `regulatory_eval_gates.py`, `test_regulatory_eval_gates_216.py`, and `src/core/README.md`.

## Findings

* `RV-026` (High, route to child RPI loop `216-citation-eval-2142-c12`): `_active_bundle_nonconflicting` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:680`) checks duplicate/version IDs across active cards without checking `len({(card.get("safe_default"), card.get("clock")) for card in cards}) <= 1`, whereas `RegulatoryChat.bundle` (`src/core/src/zava_forward/core/regulatory_chat.py:312`) marks divergent `(safe_default, clock)` signatures as `conflict = True`. Two active cards with conflicting `(safe_default, clock)` in an in-memory `conflict=False` bundle could therefore project and grade as a supported answer.
* `RV-027` (High, route to child RPI loop `216-citation-eval-2142-c12`): `_card_provenance_valid` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:1298`) checks `_nonblank_str(freshness.get("status"))` without validating aggregate `source_freshness["status"]` (and its mandatory `out_of_cadence` label) against constituent `source_freshness["sources"]` statuses/due dates and bundle source `currentness`, and `grade_chat_turn` allows `expect_out_of_cadence=False` even when a card has `status == "out_of_cadence"` if `STALE_SNAPSHOT_NOTE` was forged away.
* `RV-028` (High, route to child RPI loop `216-citation-eval-2142-c12`): `RegulatoryChat.surface` (`src/core/src/zava_forward/core/regulatory_chat.py:468`) delegates refusal detection solely to `self.bundle` (`self.refuse`), whereas `compare_chat_against_rule_cards` replays `ADVERSARIAL_PROMPTS` against `refuse_question`. If a permissive `self.refuse` callback misses a canonically prohibited question, `surface` could return actionable `rule_cards` or grounded `chat` instead of enforcing `refuse_question` on the actual question.
* `RV-029` (Low, route to child RPI loop `216-citation-eval-2142-c12`): In `test_c11_exact_card_provision_ids_unflagged_version_conflicts_and_expected_refusal_guards` (`src/core/tests/test_regulatory_eval_gates_216.py:2492`), `v2_source` updates `id` and `version` without updating `v2_source["link"]` to `/api/law/provisions/synthetic%40v2%230001`, so `_source_provenance_valid` also rejects `v2_source` rather than isolating `_active_bundle_nonconflicting`.

## Validation Evidence

* `python3 -m mypy`: Passed (`0 issues found in 318 source files`).
* `python3 -m ruff check .` and `python3 -m ruff format --check .`: Passed.
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: Passed (`14/14` tests).
* Companion `src/core` suites (`test_regulatory_chat`, `test_gates`, `test_live_doc_links`): Passed (`58/58` tests).
