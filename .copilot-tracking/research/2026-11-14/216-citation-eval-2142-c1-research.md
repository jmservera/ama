<!-- markdownlint-disable-file -->
# RPI Research: Issue #216 Child Closure (`RV-001`..`RV-006`) in `src/core`

## Metadata

* Task ID: 216-citation-eval-2142-c1
* Parent task: 216-citation-eval-2142
* Date: 2026-11-14
* Research disposition: reused
* Planning Readiness: Ready

## Evidence Summary

Existing parent research (`.copilot-tracking/research/2026-11-14/216-citation-eval-2142-research.md`), parent implementation changes (`.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-changes.md`), and the parent review artifact (`.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-review.md`) establish complete, deterministic evidence for closing all six routed defects (`RV-001`..`RV-006`) inside `src/core`:

* `E1` (`RV-001`): `grade_chat_turn` in `src/core/src/zava_forward/core/regulatory_eval_gates.py` currently uses substring `in` checks on `sections["what_sources_say"]` and `sections["recorded_home_facts"]`, permitting appended unsupported compliance claims. Comparing against canonical extractive text (`"; ".join(f'[{s["id"]}] "{s["text"]}"' ...)` and `"; ".join(f"[{f['id']}] {f['text']}" ...)` or `"No role-visible recorded home facts were projected for this purpose."`) closes `RV-001`.
* `E2` (`RV-002`): `evaluate_citation_and_refusal_gates` does not emit a digest binding `evaluated_cases` together with their `actual` responses. Emitting `evaluated_outputs_sha256` from `evaluate_citation_and_refusal_gates` and verifying `gates_report.get("evaluated_outputs_sha256") == evaluated_outputs_digest(evaluated_cases)` inside `compare_chat_against_rule_cards` closes stale-report reuse.
* `E3` (`RV-003`): `compare_chat_against_rule_cards` only counts `chat`-arm hazard misses toward `failure_severity = "critical"`. Counting any `hazard_missed is True` across `chat`, `cards`, or unpaired trial observations (`observed_hazard_misses > 0`) as `failure_severity = "critical"` and requiring `observed_hazard_misses == 0` closes `RV-003`.
* `E4` (`RV-004`): `agreement_gaps` validates `owner` only as non-blank and distinct from `independent_grader`. Requiring `_canon_name(owner) == _canon_name(LEGAL_GATE_OWNER)` binds threshold agreements to the named gate owner (`GATE_OWNERS["citation_validity"]` / `GATE_OWNERS["refusal_accuracy"]`).
* `E5` (`RV-005`): `compare_chat_against_rule_cards` checks URL prefixes (`startswith`) and unioned provision IDs. Checking exact URL-encoded `/api/law/cards/{quote(card_id, safe='')}` and `/api/law/provisions/{quote(prov_id, safe='')}` links and exact per-card `[p["id"] for p in card["provisions"]]` parity against `deterministic_rule_cards(expected_bundle)` closes `RV-005`.
* `E6` (`RV-006`): `cost_per_accepted_check` divides arbitrary-precision Python ints directly by `1_000_000.0`, raising `OverflowError` on `10**400`. Converting `input_tokens` and `output_tokens` via `_finite_float` first and returning `"Unknown"` on `None` or non-finite totals closes `RV-006`.
