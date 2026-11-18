<!-- markdownlint-disable-file -->
# Plan Critique: Issue #216 Child Hardening Pass 7 (`216-citation-eval-2142-c7`)

* Task ID: 216-citation-eval-2142-c7
* Critique verdict: Revise (applied directly)

## Findings and Direct Dispositions

* `PC-001` (`recorded_home_facts` baseline parity): Applied directly. `_baseline_projection_matches` requires exact `_to_plain_json` equality on `surface`, `as_of`, `conflict`, `workflow_only`, `cards`, and `provisions`, while validating that `recorded_home_facts` is a sequence whose entries each match an expected home fact via `_fact_matches` (supporting both default `[]` and valid tuple/list home-fact projections).
* `PC-002` (Non-answer baseline parity and `conflict` derivation): Applied directly. `deterministic_rule_cards` derives `conflict = bool(bundle.get("conflict") or bundle.get("kind") == "conflict")`, and `_score_structural_baseline` validates `_baseline_projection_matches` across `answer`, `conflict`, and `refused` cases alike.
* `PC-003` (Pair-level `case_id` and arm-specific `surface_sha256` binding): Applied directly. `_score_paired_observations` buckets pairs by `(role, participant, case_id, task)` so both arms share `case_id`, and validates `surface_sha256 == observation_surface_digest(arm, surface)` against `_to_plain_json`-projected `paired_cards` and `cases[i]["actual"]`.
* `PC-004` (Projection-aware provenance validators): Applied directly. Separate `_source_provenance_valid` (full source citation with `text` and boolean `exercise`), `_projected_provision_valid` (projected provision without `text`/`exercise`), and `_card_provenance_valid` (supporting active `"approved"`/`"active"` statuses and optional boolean `exercise`) reconcile `LawStore` and synthetic multi-card fixtures.
* `PC-005` (Fail-closed malformed facts and non-Mapping entries): Applied directly. `render_extractive_answer` refuses fail-closed when `sources`, `facts`, or `cards` contain non-`Mapping` items or malformed `id`/`text` fields; `grade_chat_turn` rejects any non-`Mapping` element in expected or actual collections.
* `PC-006` (`RegulatoryChat.surface` admission, single snapshot, and import order): Applied directly. `RegulatoryChat.surface` enforces `self.admit(user)`, `case_id` existence, and question bounds, builds a single `bundle` snapshot, short-circuits to `cards_only` unless `_verify_comparison_evidence(comparison)` holds, and evaluates the candidate reply rendered from that identical snapshot without mutating `ask()`.
* `PC-007` (Collision-free invalid-UTF-8 tagging): Applied directly. `_normalize_json_value` tags valid UTF-8 strings as `["str", value]` and lone-surrogate strings as `["invalid_utf8_str", ascii(value)]` (with `ensure_ascii=True` in `_canon_json`), and `_is_strict_json_value` requires `_is_utf8_str` on both string values and mapping keys.
