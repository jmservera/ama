# Implementation Changes: Child Hardening Pass 12 for Issue #216 (`RV-026`..`RV-029`)

* Task ID: `216-citation-eval-2142-c12`
* Date: `2026-11-14`
* Plan: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c12-plan.md`
* Phase details: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c12-phase-details.md`
* Declared scope: Full plan (`P01`: `P01-T01`, `P01-T02`)
* Execution status: `Complete`

## Phase 1 (`P01`): Card-Signature Conflict, Freshness Aggregate Parity, and Surface Refusal Enforcement

### Task `P01-T01`: Implement `RV-026`..`RV-028` and `PC-001`..`PC-002` in `regulatory_eval_gates.py`, `regulatory_chat.py`, and `src/core/README.md`

* Status: `Complete`
* Changes:
  * `src/core/src/zava_forward/core/regulatory_eval_gates.py`:
    * Added `OUT_OF_CADENCE_LABEL` and `_FRESHNESS_STATUSES = ("in_cadence", "out_of_cadence", "unknown")`.
    * Hardened `_active_bundle_nonconflicting` (`RV-026`, `RV-027`, `PC-001`, `PC-002`) with `Mapping`, `_nonblank_str` (`type(v) is str`), `_is_nonstr_seq`, and `None | _is_utf8_str` guards before hashing `(safe_default, clock)` or constituent `(status, due_on, last_success)` tuples; rejected divergent active-card `(safe_default, clock)` signatures, cross-card constituent freshness disagreements, and enum `src["currentness"]` contradictions.
    * Hardened `_card_renderable`, `_card_provenance_valid`, `_source_matches`, and `grade_chat_turn` (`RV-027`, `PC-002`) to enforce valid freshness enum statuses, nonblank `label` with exact `out_of_cadence` biconditional, optional `as_of` day agreement, unconditional constituent `sources` validation, uniform constituent `status` rollup matching `card_freshness`, `due_on=None` -> `unknown` parity, `last_success + timedelta(days=cadence_days)` parity with `OverflowError` guard, `"currentness"` equality in `_source_matches`, `cards_prov_ok` gating on `cards_ok` (`answer_contract`), and strict boolean / omitted-key `expect_out_of_cadence` parity across both `citation_validity` and `answer_contract`.
  * `src/core/src/zava_forward/core/regulatory_chat.py`:
    * Imported `refuse_question` and enforced `canonical_refusal = refuse_question(raw_q) or refuse_question(masked)` directly inside `RegulatoryChat.surface` (`RV-028`) while preserving injectable `self.refuse` seams in `RegulatoryChat.ask` and `RegulatoryChat.bundle`.
  * `src/core/README.md`:
    * Documented `RegulatoryChat.surface` canonical `refuse_question` enforcement, `source_freshness` aggregate/constituent/currentness parity, and active-card `(safe_default, clock)` signature agreement.

### Task `P01-T02`: Apply `RV-029` & `PC-003` fixture updates, add `test_c12` regression test, and validate

* Status: `Complete`
* Changes:
  * `src/core/tests/test_regulatory_eval_gates_216.py`:
    * Aligned `multi_bundle`'s two synthetic cards on `"safe_default": "Escalate to named human owner."` and set `v2_source["link"] = "/api/law/provisions/synthetic%40v2%230001"` in `test_c11` (`RV-029`).
    * Added `test_c12_card_signature_conflict_freshness_consistency_and_surface_refusal_policy` covering `RV-026`..`RV-028` and `PC-001`..`PC-003` (including both `comparison=None` and verified `comparison=positive_cmp` refusal assertions on `RegulatoryChat.surface`).

## Implementation-Time Updates and Follow-Ups

* Local implementation judgment: Gated `cards_ok` in `grade_chat_turn` on `cards_prov_ok` so invalid card provenance fails `answer_contract` alongside `citation_validity`.
* Follow-up items (unchanged, outside `src/core` boundary): Cross-package `src/api` route wiring to `RegulatoryChat.surface` and `src/agents` helper deduplication.
* Blockers / remaining work: `none` (`P01`, `P01-T01`, and `P01-T02` complete).

## Validation State

* `python3 -m mypy` in `src/core`: `Success: no issues found in 318 source files`
* `python3 -m ruff check .` in `src/core`: `All checks passed!`
* `python3 -m ruff format --check .` in `src/core`: `265 files already formatted`
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v` in `src/core`: `Ran 15 tests in 51.250s — OK`
* Companion regressions (`PYTHONPATH=src:tests`): `test_regulatory_chat.py` (`25/25 OK`), `test_gates.py` (`31/31 OK`), `test_live_doc_links.py` (`2/2 OK`)
