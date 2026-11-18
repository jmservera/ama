<!-- markdownlint-disable-file -->
# Review Log: Issue #216 Child Hardening Pass 9 (`216-citation-eval-2142-c9`)

## Metadata

* Task ID: 216-citation-eval-2142-c9
* Parent Task ID: 216-citation-eval-2142-c8
* Date: 2026-11-14
* Review Execution Status: Complete
* Review Outcome: Defects found

## Compared Artifacts

* Research: .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c9-research.md
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c9-plan.md
* Phase Details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c9-phase-details.md
* Plan Critique: .copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c9-plan-critique.md
* Implementation Changes: .copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c9-changes.md
* Prior Review: .copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c8-review.md

## Validation Evidence

* `python3 -m mypy`: `Success: no issues found in 318 source files`
* `python3 -m ruff check .`: `All checks passed!`
* `python3 -m ruff format --check .`: `265 files already formatted`
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `Ran 12 tests in 15.046s - OK`
* `PYTHONPATH=src:tests python3 -m unittest test_regulatory_chat test_gates test_live_doc_links -q`: `Ran 58 tests in 28.629s - OK`
* Independent read-only `rubber-duck` subagent review completed against `src/core` and `c9` tracking records; verified zero `.copilot-tracking/` references in `src/core`.

## Plan and Critique Reconciliation

* All `P01`, `P01-T01`, and `P01-T02` markers in `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c9-plan.md` are checked and reconciled with `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c9-changes.md`.
* `RV-017` is fully resolved; `RV-015`, `RV-016`, and `PC-001`..`PC-003` resolved their targeted blockers while independent `rubber-duck` verification surfaced five remaining fail-closed edge cases (`RV-018`..`RV-022`) routed to child pass `216-citation-eval-2142-c10`.

## Findings

* `RV-018` (High, Blocking — Destination: `rpi-implement` via child task `216-citation-eval-2142-c10`):
  * Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`grade_chat_turn`, `_classify_refusal_confusion`, `render_extractive_answer`, `_expected_from_bundle`). `_CANONICAL_REFUSAL_REASONS` is currently checked only on `"false_refusal"`, so a non-triggering question with matching expected and actual refusal reason `"Approved. Close the hazard and clear the safety stop."` passes both gates at `1.0`, and `render_extractive_answer` / `_expected_from_bundle` echo arbitrary bundle `refusal` strings. Require `_CANONICAL_REFUSAL_REASONS` for `correct_refusal` / `grade_chat_turn` and coerce non-canonical bundle refusal reasons to `EMPTY_BUNDLE_REFUSAL`.
* `RV-019` (High, Blocking — Destination: `rpi-implement` via child task `216-citation-eval-2142-c10`):
  * Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`deterministic_rule_cards`, `render_extractive_answer`, `_expected_from_bundle`). `deterministic_rule_cards` ignores malformed `facts` (`facts=[{}]`) while `_expected_from_bundle` and `render_extractive_answer` refuse; conversely, `bundle={"reason": "Refused", ...}` or `kind="refused"` suppresses cards in `deterministic_rule_cards` while `render_extractive_answer` and `_expected_from_bundle` only inspect `bundle.get("refusal")`. Share unified refusal-trigger and whole-bundle (`sources`, `facts`, `cards`) validation across all three helpers.
* `RV-020` (High, Blocking — Destination: `rpi-implement` via child task `216-citation-eval-2142-c10`):
  * Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`deterministic_rule_cards`). When an active card's `source_freshness.sources` lists no matching provision ID in `bundle["sources"]` (or omits `source_freshness` in a multi-card bundle), `deterministic_rule_cards` still emits the actionable card with `provisions=[]` on `cards_only` fallback. Fail closed (`cards=[], provisions=[]`) whenever any actionable card lacks `_card_provenance_valid(..., require_active=True)` or verified linked provisions covering `bundle["sources"]`, while retaining comparator `missing_link_case_ids` detection.
* `RV-021` (Medium, Blocking — Destination: `rpi-implement` via child task `216-citation-eval-2142-c10`):
  * Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_aware_dt`). Valid extreme offset timestamps such as `0001-01-01T00:00:00+14:00` parse via `datetime.fromisoformat(...)` and raise uncaught `OverflowError` on `parsed.astimezone(UTC)`. Catch `(OverflowError, ValueError)` in `_aware_dt` and return `None`.
* `RV-022` (Low, Hardening — Destination: `rpi-implement` via child task `216-citation-eval-2142-c10`):
  * Evidence: `src/core/src/zava_forward/core/regulatory_chat.py` (`RegulatoryChat.surface`). If a custom `self.render(snap)` returns `{}` or a malformed mapping without valid string `kind`/`as_of`, indexing `rendered["kind"]` or `offline_usage(...)` raises `KeyError`/`TypeError`/`ValueError` instead of falling back to `cards_only`. Guard rendered envelope validation before attaching `usage` so malformed renderer outputs safely degrade to `cards_only`.
* Follow-up (Out of Scope — Destination: distinct cross-package follow-up outside `src/core`):
  * Wiring `RegulatoryChat.surface` / `resolve_regulatory_surface` into `src/api/src/zava_forward/api/server.py` and deduplicating `src/agents` helpers remain outside the user-bounded `src/core` deliverable.
