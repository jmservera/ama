<!-- markdownlint-disable-file -->
# Implementation Plan: Issue #216 Child Hardening Pass 8 (`216-citation-eval-2142-c8`)

* Task ID: `216-citation-eval-2142-c8`
* Parent Task ID: `216-citation-eval-2142-c7`
* Date: `2026-11-14`
* Status: `Finalized`
* Planning Readiness: `Ready`

## Executive Summary

Child task `216-citation-eval-2142-c8` closes all seven concrete in-scope `src/core` findings (`RV-008`..`RV-014`) surfaced by the `c7` independent review of Issue #216 (`regulatory_eval_gates.py`), incorporating all five direct planner corrections (`PC-001`..`PC-005`) from the single final-candidate critique. Phase `P01` tightens active temporal/version/`exercise=True` provenance validation against `as_of` across provisions, sources, facts, and cards, binds every evaluation case's `question` to both `refuse_question(question)` and `refuse(question)` while requiring prompt-triggered adversarial refused turns, enforces non-regression `>= 0.0` gain and `<= 1.0` elapsed-ratio floors in threshold validation, paired scoring, and `positive_lift`, eliminates UTF-16 lone-surrogate digest collisions in `observation_surface_digest(arm, surface)` without raising `ValueError`, fails closed to `refused` (`EMPTY_BUNDLE_REFUSAL`) when non-conflict bundles lack renderable rule cards, bounds `_strict_int` and replaces unbounded decimal conversions with `_int_token` / `_safe_ascii` so `10**5000` payloads never raise `ValueError`, and aligns `_build_gate_result` and `_verify_agreed_gates_report` when owner-agreed `min_rates < 1.0` while preserving zero tolerance for `unsafe_non_refusal` and missed adversarial prompts. No unresolved blockers exist.

## Sources

* `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c7-review.md`
* `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c8-research.md`
* `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* `src/core/src/zava_forward/core/regulatory_chat.py`
* `src/core/tests/test_regulatory_eval_gates_216.py`
* `src/core/README.md`

## User Decisions and Requirements

* Deliver the two locally verifiable acceptance criteria of Issue #216 strictly within `src/core`:
  * Citation validity and refusal accuracy gates set with owners and measured on a graded and adversarial set.
  * Paired comparison reports value of chat over deterministic cards with links; if no measured value, ship cards alone.
* Maintain all four `.copilot-tracking/` artifact families (`research/`, `plans/`, `changes/`, `reviews/`).
* Verify in `src/core` using bare `mypy`: `cd /home/azureuser/source/ama-demo-wt/feat-216-citation-eval-2142/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*216*.py' -v`.
* Commit cleanly on `feat/ai-216-citation-eval-2142` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing (`git status --short` empty), and keep `.copilot-tracking/` paths out of `src/` and commit messages.

## Goals

* Enforce active temporal (`<= as_of_day`), `@v{version}`, and `exercise=True` provenance rules across answer turns, baseline projections, and extractive bundle rendering (`RV-008`, `RV-012`).
* Bind case-level `question` prompts to `refuse(question)` and require at least one prompt-triggered refused turn in the `adversarial` bucket (`RV-009`).
* Enforce non-regression floors (`completion_gain >= 0.0`, `comprehension_gain >= 0.0`, `elapsed_ratio <= 1.0`) in both threshold validation and paired observation scoring (`RV-010`).
* Make `observation_surface_digest` collision-free on lone UTF-16 surrogates (`RV-011`) and make all canonical JSON, digest, string, and shipping helpers exception-safe on arbitrary-precision integers (`10**5000`) (`RV-013`).
* Support owner-agreed `min_rates < 1.0` consistently across `evaluate_citation_and_refusal_gates` and `_verify_agreed_gates_report` (`RV-014`).

## Scope and Non-Goals

* Scope:
  * `src/core/src/zava_forward/core/regulatory_eval_gates.py`
  * `src/core/tests/test_regulatory_eval_gates_216.py`
  * `src/core/README.md`
* Non-Goals:
  * Edits outside `src/core` (`src/api`, `src/agents`, `infra/`, `tools/`).
  * Running `pip install -e .` or `git push`.

## Functional Requirements

* `FR-01` (`RV-008`, `PC-002`): `_projected_provision_valid`, `_source_provenance_valid`, `_fact_provenance_valid`, and `_card_provenance_valid` (threaded via `_source_matches` and `_fact_matches`) validate `@v{version}` alignment on provisions (`<stem>@v<ver>[#<frag>]` matching `version`) and cards (`<stem>@v<ver>` without `#`, matching `card["version"]` when present) while preserving `{cid}/{path}@{digest}` fact IDs; when `require_active=True` (`expected_kind == "answer"`), they validate `effective <= as_of_day`, `_extract_day(retrieved) <= as_of_day` (plus aware timestamp `<= as_of` when both are aware), `approved_on <= as_of_day`, `src.get("exercise") is True`, `fact.get("exercise") is True`, `prov.get("exercise", True) is True`, and `card.get("exercise", True) is True`.
* `FR-02` (`RV-009`, `PC-003`): `evaluate_citation_and_refusal_gates` requires a non-blank UTF-8 `case["question"]`, checks both canonical `refuse_question(question)` and `refuse(question)`, requires any case triggering a refusal obligation to expect and produce `kind == "refused"` with that exact reason (using only the 5 canonical `confusion_counts` labels: `"unsafe_non_refusal"` on non-refused or citation-leaking outcomes and `"invalid_response"` on non-leaking reason mismatches), and requires at least one prompt-triggered refused turn in `adversarial`.
* `FR-03` (`RV-010`, `PC-005`): `_validate_benefit_thresholds` requires `0.0 <= min_completion_gain <= 1.0`, `0.0 <= min_comprehension_gain <= 1.0`, and `0.0 < max_elapsed_ratio <= 1.0`; `_score_paired_observations` enforces non-regression (`>= 0.0` gains and `<= 1.0` elapsed ratio per role and in aggregate) in both `role_gaps` and `positive_lift` alongside configured thresholds and strict aggregate lift.
* `FR-04` (`RV-011`, `PC-004`): `observation_surface_digest(arm, surface)` projects structural containers via unhashable-key-safe `_project_for_surface_digest` without pre-converting lone UTF-16 surrogates to `ascii(value)` and without raising `ValueError` on `_is_strict_json_value`, so `_canon_json` tags lone surrogates as `["invalid_utf8_str", ...]` distinct from valid UTF-8 `["str", ...]`.
* `FR-05` (`RV-012`, `PC-002`): `render_extractive_answer` and `_expected_from_bundle` fail closed to `kind="refused"` (`EMPTY_BUNDLE_REFUSAL`) when non-conflict bundles have empty `cards` or any unrenderable card (`_card_renderable`), or when `sources`/`facts` fail provenance checks, while preserving `unmapped_bundle` (`source_freshness=None`) link-parity diagnostics.
* `FR-06` (`RV-013`, `PC-004`): `_strict_int` enforces `value.bit_length() <= _MAX_JSON_INT_BITS` (`8192`), and `_int_token` / `_safe_ascii` replace unbounded decimal `str()`/`ascii()`/`{...!a}` conversions so `10**5000` payloads never raise `ValueError` across `_canon_json`, `_is_strict_json_value`, `_to_plain_json`, `observation_surface_digest`, `compare_chat_against_rule_cards`, `resolve_regulatory_surface`, and `RegulatoryChat.surface`.
* `FR-07` (`RV-014`, `PC-001`): `_build_gate_result` checks `(passed_count == total_count) if target_rate >= 1.0 else (rate >= target_rate)` while `refusal_accuracy` continues to block unconditionally when `confusion_counts["unsafe_non_refusal"] > 0` or `prompt_report["missed"] > 0`, and `_verify_agreed_gates_report` delegates rate pass/fail enforcement to the full `evaluate_citation_and_refusal_gates` replay rather than pre-rejecting imperfect individual turns.

## Non-Functional Requirements

* `NFR-01`: Strict `mypy`, `ruff check .`, and `ruff format --check .` cleanliness across `src/core`.
* `NFR-02`: Test Governance lock:
  * Test owner: `src/core/tests/test_regulatory_eval_gates_216.py`
  * Exact removals: `none`
  * Maximum test-method additions: `<= 2` new test methods in `test_regulatory_eval_gates_216.py`
  * Canonical targets: `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/README.md`
  * Generated targets: `none`
  * Semantic vs regression coverage: existing 10 tests cover core end-to-end semantics; new focused assertions verify `RV-008`..`RV-014` regressions (`future dates / version mismatch / exercise=False`, `adversarial question paired with answer`, `negative thresholds & speed-only regression`, `surrogate vs literal ascii digest collision`, `cards=[{}] / cards=[] refusal`, `10**5000 fail-closed surface`, and `min_rates=0.8` with `9/10` pass).

## Acceptance Criteria

* `AC-01`: Future `effective`/`retrieved`/`approved_on` dates (`> as_of`), `@v{version}` mismatches, and `exercise=False` on active answer provenance fail `grade_chat_turn` and baseline projection checks (`RV-008`).
* `AC-02`: Cases whose `question` triggers `refuse(question)` cannot pass when `expected["kind"] != "refused"`, and `adversarial` sets lacking a prompt-triggered refused turn fail `evaluate_citation_and_refusal_gates` (`RV-009`).
* `AC-03`: Negative gain thresholds, `max_elapsed_ratio > 1.0`, or faster-but-less-accurate paired chat runs fail comparison and ship `cards_only` (`RV-010`).
* `AC-04`: `observation_surface_digest("chat", {"x": "\ud800"}) != observation_surface_digest("chat", {"x": ascii("\ud800")})` without raising `ValueError`, while tuple/list JSON round-trips produce identical digests (`RV-011`, `PC-004`).
* `AC-05`: `render_extractive_answer` and `_expected_from_bundle` fail closed to `kind="refused"` (`EMPTY_BUNDLE_REFUSAL`) on `cards=[]` or `cards=[{}]` while keeping `unmapped_bundle` link-parity detection intact (`RV-012`, `PC-002`).
* `AC-06`: `10**5000` payloads anywhere in comparison/agreement/observation/`rule_hazard_misses`/`reasons` inputs fail closed to `cards_only` in `resolve_regulatory_surface` and `RegulatoryChat.surface` without raising `ValueError` (`RV-013`, `PC-004`).
* `AC-07`: Owner-agreed `min_rates` of `0.8` accept a `9/10` (`0.9`) dataset with a conservative `false_refusal` on a `conflict` turn in both `evaluate_citation_and_refusal_gates` and `compare_chat_against_rule_cards`, while rejecting `9/10` with an `unsafe_non_refusal` to `cards_only` (`RV-014`, `PC-001`).
* `AC-08`: `mypy`, `ruff check .`, `ruff format --check .`, `test_regulatory_eval_gates_216.py`, `test_regulatory_chat.py`, `test_gates.py`, and `test_live_doc_links.py` all pass cleanly.

## Phase Checklist

<!-- P01 -->
### [x] Phase 1 (`P01`): Harden Provenance, Refusal Binding, Non-Regression Floors, Digests, Big-Int Safety, and Sub-1.0 Gate Replay

<!-- P01-T01 -->
* [x] `P01-T01`: Implement `RV-008`..`RV-014` fixes in `src/core/src/zava_forward/core/regulatory_eval_gates.py` and update `src/core/README.md` if needed.

<!-- P01-T02 -->
* [x] `P01-T02`: Add focused regression coverage for `RV-008`..`RV-014` in `src/core/tests/test_regulatory_eval_gates_216.py` and run `mypy`, `ruff`, and `unittest` validation suites.

## Critique Disposition

* Critique artifact: `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c8-plan-critique.md` (Execution: `Complete`, Verdict: `Revise`, single pass completed).
* `PC-001` [High] (`direct_planner_correction` — Applied): Updated `FR-07`, `AC-07`, `P01-T01`, and `P01-T02` so `refusal_accuracy` always blocks when `confusion_counts["unsafe_non_refusal"] > 0` or `prompt_report["missed"] > 0` even under `target_rate < 1.0`, and scoped the `9/10` (`0.9 >= 0.8`) positive ship scenario to a conservative `false_refusal` on an `expected["kind"] == "conflict"` case alongside a negative `unsafe_non_refusal` test.
* `PC-002` [High] (`direct_planner_correction` — Applied): Updated `FR-01`, `FR-05`, and `P01-T01` to parse `fact["retrieved"]` via `_extract_day` (plus aware timestamp comparison against `as_of`), keep `{cid}/{path}@{digest}` fact IDs without `@v`, allow omitted `"exercise"` in `_projected_provision_valid` (`prov.get("exercise", True) is True`) while enforcing `src.get("exercise") is True` and checking expected sources/facts in `_baseline_projection_matches`, thread `as_of` through `_source_matches`/`_fact_matches`, and use `EMPTY_BUNDLE_REFUSAL`.
* `PC-003` [High] (`direct_planner_correction` — Applied): Updated `FR-02` and `P01-T01` to preserve the 5 canonical `confusion_counts` keys (`"unsafe_non_refusal"` / `"invalid_response"`), check both canonical `refuse_question(question)` and `refuse(question)` on case questions, and include `"refused"` in the `adversarial_prompt_refused_turns < 1` gap message.
* `PC-004` [High] (`direct_planner_correction` — Applied): Updated `FR-04`, `FR-06`, `AC-04`, `AC-06`, and `P01-T01` to use `observation_surface_digest(arm, surface)` without raising `ValueError` on `_is_strict_json_value`, handle unhashable mapping keys in `_project_for_surface_digest`, bound `_strict_int` to `_MAX_JSON_INT_BITS = 8192`, map oversized ints in `_to_plain_json`, and replace all remaining `ascii(...)`, `{...!a}`, and `resolve_regulatory_surface` `str(item)` sites with `_safe_ascii(...)`.
* `PC-005` [Medium] (`direct_planner_correction` — Applied): Updated `FR-03` and `P01-T01` so `paired_trial["positive_lift"]` itself requires per-role and aggregate non-regression (`>= 0.0` gains using exact integer hit deltas and `<= 1.0` finite ratios) in addition to strict aggregate lift.

## Follow-Up Items

* Downstream `src/api` endpoint wiring for `/api/law/chat` vs `/api/law/cards` remains tracked outside this `src/core`-scoped worktree slice of Issue #216.

## Handoff

* Changes record target: `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c8-changes.md`
