<!-- markdownlint-disable-file -->
# Research: Issue #216 Child Hardening Pass 10 (`216-citation-eval-2142-c10`)

## Research Brief

* Topic: Resolve remaining in-scope `src/core` review findings (`RV-018`..`RV-022`) from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c9-review.md`.
* Scope: `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md`.
* Non-goals: `src/api` route wiring and `src/agents` helper deduplication (outside user-bounded `src/core` scope).
* Posture: `focused` (caller-bounded internal review findings with exact source targets).
* Output mode: `convergence`.
* Research disposition: `reused` (verified directly against `c9-review.md` and `src/core` lines).
* Planning Readiness: `Ready`.

## Cycle 1 — Wider, Deeper, and Contrarian Synthesis

### Wider & Deeper Codebase Evidence

* `C1` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:1353`, `1432`, `692`, `3120` — `RV-018`): `grade_chat_turn` and `_classify_refusal_confusion` require `_CANONICAL_REFUSAL_REASONS` only on `"false_refusal"`, allowing matching expected/actual `"Approved..."` refusal reasons on a non-triggering prompt to score `correct_refusal` and pass both gates at `1.0`, while `render_extractive_answer` and `_expected_from_bundle` echo arbitrary non-canonical `bundle["refusal"]` strings.
* `C2` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:824`, `649`, `3080` — `RV-019`): `deterministic_rule_cards` ignores `facts` validation (`facts=[{}]`) whereas `render_extractive_answer` and `_expected_from_bundle` refuse; conversely, `deterministic_rule_cards` treats `reason="Refused"` and `kind="refused"` as explicit refusals whereas `render_extractive_answer` and `_expected_from_bundle` only inspect `bundle.get("refusal")`.
* `C3` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:873`, `src/core/src/zava_forward/core/source_monitor.py:100` — `RV-020`): `deterministic_rule_cards` emits actionable cards with `provisions=[]` when `card["source_freshness"]["sources"]` lists no matching provision in `bundle["sources"]` or omits `source_freshness` in a multi-card bundle. `card_freshness` always populates `source_freshness["sources"]` with `source_id` entries for valid provisions (`source_id=None` on missing provision).
* `C4` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:587`, `1171` — `RV-021`): `_aware_dt` calls `parsed.astimezone(UTC)` and `_usage_valid` calls `offline_usage(...)` without catching `OverflowError` on valid extreme offset timestamps such as `0001-01-01T00:00:00+14:00` or `9999-12-31T23:59:59-14:00`.
* `C5` (`src/core/src/zava_forward/core/regulatory_chat.py:463` — `RV-022`): `RegulatoryChat.surface` indexes `rendered["kind"]` and `rendered["as_of"]` and calls `offline_usage(...)` directly on `self.render(snap)`, raising `KeyError`/`TypeError`/`ValueError`/`OverflowError` if a custom renderer returns `{}` or malformed fields instead of falling back to `cards_only`.

### Contrarian Check

* Requiring every actionable card on a non-conflict bundle to pass `_card_provenance_valid(..., require_active=True)` with non-empty `source_freshness["sources"]` whose `source_id`s all resolve to active `bundle["sources"]` (and whose union covers all `bundle["sources"]`) could break existing synthetic test fixtures if any active test bundle omitted `source_freshness["sources"]`. Verified across all 30 `source_freshness` occurrences in `src/core`: every valid active test bundle (`RegulatoryChat.bundle` via `card_freshness` and `multi_bundle`) populates `source_freshness["sources"]`, and `unmapped_bundle` (`test_regulatory_eval_gates_216.py:1142`) keeps `expected["kind"] == "answer"` so `_baseline_projection_matches(..., require_active_answer=True)` continues to flag `"graded-unmapped-card"` in `missing_link_case_ids` when `expected_surface["cards"] == []`.

## Selected Recommendation & Decisions

* Extract one shared bundle-inspection helper `_inspect_bundle_surface(bundle)` used by `deterministic_rule_cards`, `render_extractive_answer`, and `_expected_from_bundle` to enforce identical explicit-refusal detection (`refusal`, `reason`, `kind == "refused"`, or unknown `kind`), canonical refusal reason coercion (`_CANONICAL_REFUSAL_REASONS` else `EMPTY_BUNDLE_REFUSAL`), whole-bundle `sources`/`facts`/`cards` validation, and full active card-to-provision link coverage on non-conflict surfaces.
* Enforce `_CANONICAL_REFUSAL_REASONS` in `grade_chat_turn` and `_classify_refusal_confusion` on `expected_kind == "refused"` as well as `actual_kind == "refused"`.
* Catch `OverflowError` in `_aware_dt` and `_usage_valid`, and guard `RegulatoryChat.surface` rendered-envelope handling so malformed renderer outputs safely fall back to `cards_only`.
