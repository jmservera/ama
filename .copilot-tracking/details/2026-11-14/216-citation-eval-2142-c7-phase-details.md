<!-- markdownlint-disable-file -->
# Phase Details: Issue #216 Child Hardening Pass 7 (`216-citation-eval-2142-c7`)

## `P01`: Harden provenance, dataset-gap, surface-bound observation, baseline projection, and UTF-8 guards in `src/core`

### `P01-T01`

* `src/core/src/zava_forward/core/regulatory_eval_gates.py`:
  * Add `_is_utf8_str`, `_safe_quote`, and `_is_sha256_hex`; reject lone surrogates in `_is_strict_json_value`, `_nonblank_str`, `_valid_iso_day`, and `_aware_dt`, and encode non-UTF-8 strings via `ascii(...)` inside `_normalize_json_value` so digests never raise `UnicodeEncodeError`.
  * Guard `render_extractive_answer` against missing `id`/`text` keys on `sources` and `facts` (`sources=[{}]`), returning fail-closed refusal when active answer sources are malformed.
  * Add `_source_provenance_valid`, `_fact_provenance_valid`, and `_card_provenance_valid`; enforce them in `_source_matches`, `_fact_matches`, `grade_chat_turn`, and `_exact_card_links_match`.
  * Enforce full projection parity in `_exact_card_links_match` (`surface`, `as_of`, `conflict`, `workflow_only`, `cards`, `provisions`, and valid `recorded_home_facts` entries).
  * Enforce `graded` answer-turn presence, `adversarial` refused-turn presence, and strict UTF-8 string `prompts` covering `ADVERSARIAL_PROMPTS` in `evaluate_adversarial_prompts`, `evaluate_citation_and_refusal_gates`, and `_verify_agreed_gates_report`.
  * Export `observation_surface_digest(arm, surface)` and require every paired observation in `_score_paired_observations` / `compare_chat_against_rule_cards` to match an evaluated `case_id` and its `cards`/`chat` surface digest (`surface_sha256`).
* `src/core/src/zava_forward/core/regulatory_chat.py`:
  * Add `RegulatoryChat.surface(user, cid, question, *, comparison=None, tid=None)` using `resolve_regulatory_surface` so callers in `src/core` ship deterministic rule cards alone unless `comparison` proves measured value.

### `P01-T02`

* Update `src/core/README.md` to document `observation_surface_digest` and `RegulatoryChat.surface`.
* Update `_valid_observations` in `src/core/tests/test_regulatory_eval_gates_216.py` to bind `case_id` and `surface_sha256` to evaluated cases/surfaces, and add regressions for missing provenance (`{id, text, link}`), answer-only datasets, unbound observations, altered/held baseline cards, `sources=[{}]`, lone surrogates (`"\ud800"`), `prompts=[123]` / `[*ADVERSARIAL_PROMPTS, 123]`, and `RegulatoryChat.surface`.
