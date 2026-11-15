<!-- markdownlint-disable-file -->
# Research: Issue #216 Child Hardening Pass 7 (`216-citation-eval-2142-c7`)

## Metadata

* Task ID: 216-citation-eval-2142-c7
* Parent Task ID: 216-citation-eval-2142-c6
* Date: 2026-11-14
* Research disposition: reused
* Planning Readiness: Ready

## Evidence Summary

Reused directly from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c6-review.md` and direct inspection of `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, and `src/core/tests/regulatory_fixture.py`:

1. **`RV-001` (Core surface selector integration)**: `src/api/server.py` is outside the user-bounded `src/core` scope, while `RegulatoryChat` in `src/core/src/zava_forward/core/regulatory_chat.py` can expose `surface(user, cid, question, *, comparison=None, tid=None)` backed by `resolve_regulatory_surface`, defaulting to `cards_only` without invoking `ask` unless `comparison` proves measured value.
2. **`RV-002` (Citation, fact, and card provenance validation)**: `_source_matches` and `_fact_matches` compared `.get(key)` values without verifying active non-blank provenance (`status`, positive integer `version`, ISO dates `effective` and `retrieved`, 64-hex SHA-256 `hash`, `review_status`, `completeness`, boolean `exercise`, and active rule-card metadata).
3. **`RV-003` (Refusal-turn dataset coverage)**: `evaluate_citation_and_refusal_gates` and `_verify_agreed_gates_report` must require at least one supported `answer` turn in `graded` and at least one `refused` chat turn in `adversarial` (plus canonical `ADVERSARIAL_PROMPTS` coverage).
4. **`RV-004` (Case- and surface-bound paired observations)**: Paired observations must bind `case_id` to an evaluated case in `cases` and bind `surface_sha256` to `observation_surface_digest(arm, surface)` (`paired_entry["rule_cards"]` for `"cards"` and `case["actual"]` for `"chat"`), ensuring unrelated or stale observations fail closed.
5. **`RV-005` (Complete deterministic baseline card projection parity)**: `_exact_card_links_match` must verify full `_to_plain_json` projection equality for `surface`, `as_of`, `conflict`, `workflow_only`, `cards`, and `provisions` against `deterministic_rule_cards(expected)`, plus active card and active provision provenance.
6. **`RV-006` (Safe malformed-source rendering and lone-surrogate UTF-8 guards)**: `_is_utf8_str` and `_safe_quote` prevent `UnicodeEncodeError` in `quote(...)`, `_canon_json`, and `json.dumps`, while `render_extractive_answer` validates non-blank `id`/`text` via `.get(...)` instead of raising `KeyError` on `sources=[{}]`.
7. **`RV-007` (Strict prompt sequence element validation)**: Non-string, blank, or non-UTF-8 prompt elements (`prompts=[123]` or `[*ADVERSARIAL_PROMPTS, 123]`) or missing canonical `ADVERSARIAL_PROMPTS` must record explicit `dataset_gaps` entries and count as missed in `evaluate_adversarial_prompts`.
