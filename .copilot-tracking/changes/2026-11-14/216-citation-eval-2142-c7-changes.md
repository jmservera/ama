<!-- markdownlint-disable-file -->
# Implementation Changes: Issue #216 Child Hardening Pass 7 (`216-citation-eval-2142-c7`)

* Task ID: 216-citation-eval-2142-c7
* Plan reference: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c7-plan.md
* Execution status: Complete

## `P01`: Harden provenance, dataset-gap, surface-bound observation, baseline projection, and UTF-8 guards in `src/core`

### `P01-T01`: Core provenance, dataset-gap, surface-binding, UTF-8, and `RegulatoryChat.surface` guards

* Updated `src/core/src/zava_forward/core/regulatory_eval_gates.py`:
  * Added `_is_utf8_str` (`TypeGuard[str]`), `_safe_quote`, `_is_sha256_hex`, collision-free `["invalid_utf8_str", ascii(value)]` digest normalization, UTF-8 mapping-key checks in `_is_strict_json_value`, and `ascii(...)` / `!a` fallbacks across `_to_plain_json`, `_normalize_json_value`, `evaluate_adversarial_prompts`, `evaluate_citation_and_refusal_gates`, and `_score_structural_baseline` so lone UTF-16 surrogates never raise `UnicodeEncodeError` and remain UTF-8 JSON-serializable (`RV-006`, `PC-007`).
  * Hardened `render_extractive_answer` and `_expected_from_bundle` to fail closed with `refused` when `sources`, `facts`, or `cards` contain non-`Mapping` entries or incomplete `id`/`text` fields (`sources=[{}]`, `facts=[{}]`) (`RV-006`, `PC-005`).
  * Added `_version_valid`, `_projected_provision_valid`, `_source_provenance_valid`, `_fact_provenance_valid`, and `_card_provenance_valid` in `grade_chat_turn` and `_baseline_projection_matches` so stripped `{id, text, link}` fixtures fail closed while valid `LawStore` and synthetic multi-card fixtures pass (`RV-002`, `PC-004`).
  * Derived `conflict` consistently across `bundle` and `expected` (`bool(bundle.get("conflict") or bundle.get("kind") == "conflict")`) and checked full `_baseline_projection_matches` parity (including optional expected `recorded_home_facts` and active/non-answer card and provision provenance) across `answer`, `conflict`, and `refused` turns (`RV-005`, `PC-001`, `PC-002`).
  * Enforced `dataset_gaps` in `evaluate_citation_and_refusal_gates` and `_verify_agreed_gates_report` when `prompts` contains non-string, blank, or invalid UTF-8 entries, when `graded` lacks at least one `answer` turn, or when `adversarial` lacks at least one `refused` turn (`RV-003`, `RV-007`).
  * Added `observation_surface_digest(arm, surface)` and bound paired staff observations by `(role, participant, case_id, task)` with exact arm-specific `surface_sha256` digests against evaluated `paired_cards` and `cases` (`RV-004`, `PC-003`).
* Updated `src/core/src/zava_forward/core/regulatory_chat.py`:
  * Added admitted, single-snapshot `RegulatoryChat.surface(user, cid, question, *, comparison=None)` backed by `_verify_comparison_evidence` and `resolve_regulatory_surface`, defaulting to `cards_only` (`cards_alone=True`, `chat=None`) without modifying `ask` or persisting chat turns (`RV-001` core boundary, `PC-006`).

### `P01-T02`: Documentation, surface-bound test fixtures, regressions, and `src/core` validation

* Updated `src/core/README.md` (`### Owned citation/refusal evaluation gates and rule-card ship comparator (#216)`) to document `observation_surface_digest` and `RegulatoryChat.surface`.
* Updated `src/core/tests/test_regulatory_eval_gates_216.py`:
  * Bound `_valid_observations(cases, paired_cards)` to evaluated `case_id`s and `observation_surface_digest` digests across all test callers.
  * Added `test_provenance_surface_binding_surrogate_and_chat_surface_regressions` covering `RegulatoryChat.surface` admission + default `cards_only` + verified `chat_with_cards`, stripped source/fact/card provenance, answer-only dataset gaps, unbound/cross-case paired observations, held/tampered baseline projections across answer and refused turns, malformed `sources=[{}]` and `facts=[{}]`, lone UTF-16 surrogates (`\ud800`) and collision-free digest + strict UTF-8 JSON round-trip, and non-string elements in `prompts`.

## Validation

* `python3 -m mypy`: `Success: no issues found in 318 source files`
* `python3 -m ruff check .`: `All checks passed!`
* `python3 -m ruff format --check .`: `265 files already formatted`
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `Ran 10 tests in 17.705s - OK`
* `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_regulatory_chat.py' -q`: `Ran 25 tests in 31.114s - OK`
* `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_gates.py' -q`: `Ran 31 tests in 0.122s - OK`
* `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_live_doc_links.py' -q`: `Ran 2 tests in 1.012s - OK`
* Bidirectional module import checks (`regulatory_eval_gates` <-> `regulatory_chat`): `OK`

## Blockers and Remaining Work

* Blockers: None.
* Remaining in-scope work: None (`P01`, `P01-T01`, and `P01-T02` complete).
* Follow-up items: Cross-package `src/api` HTTP route wiring and `src/agents` helper deduplication remain outside the user-bounded `src/core` scope.
