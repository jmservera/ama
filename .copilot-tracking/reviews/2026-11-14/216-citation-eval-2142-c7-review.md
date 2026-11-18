<!-- markdownlint-disable-file -->
# Review Log: Issue #216 Child Hardening Pass 7 (`216-citation-eval-2142-c7`)

## Metadata

* Task ID: 216-citation-eval-2142-c7
* Parent Task ID: 216-citation-eval-2142-c6
* Date: 2026-11-14
* Review Execution Status: Complete
* Review Outcome: Defects found

## Compared Artifacts

* Research: .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c7-research.md
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c7-plan.md
* Phase Details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c7-phase-details.md
* Plan Critique: .copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c7-plan-critique.md
* Implementation Changes: .copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c7-changes.md
* Prior Review: .copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c6-review.md

## Validation Evidence

* `python3 -m mypy`: `Success: no issues found in 318 source files`
* `python3 -m ruff check .`: `All checks passed!`
* `python3 -m ruff format --check .`: `265 files already formatted`
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `Ran 10 tests in 17.705s - OK`
* `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_regulatory_chat.py' -q`: `Ran 25 tests in 31.114s - OK`
* `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_gates.py' -q`: `Ran 31 tests in 0.122s - OK`
* `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_live_doc_links.py' -q`: `Ran 2 tests in 1.012s - OK`
* Independent read-only `rubber-duck` subagent review completed against `src/core` changed files and `c7` tracking records; verified zero `.copilot-tracking/` references in `src/core`.

## Plan and Critique Reconciliation

* All `P01`, `P01-T01`, and `P01-T02` markers in `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c7-plan.md` are checked and reconciled with `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c7-changes.md`.
* Prior findings `RV-001` (core boundary via `RegulatoryChat.surface`), `RV-003`, `RV-005`, and `RV-007` are resolved; `RV-002`, `RV-004`, `RV-006`, and `PC-004`..`PC-007` revealed deeper edge cases documented below as `RV-008`..`RV-014`.
* Out-of-scope follow-up items (`src/api` route wiring and `src/agents` helper deduplication) remain explicitly separated from the `src/core` boundary.

## Findings

* `RV-008` (High, Blocking — Destination: `rpi-implement` via child task `216-citation-eval-2142-c8`):
  * Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_projected_provision_valid`, `_source_provenance_valid`, `_fact_provenance_valid`, `_card_provenance_valid`). Date syntax is checked, but temporal eligibility against `as_of` (rejecting future `2099` `effective`, `retrieved`, or `approved_on` dates on active answers), `@v{version}` alignment between `id` and `version`, and `exercise is True` on active synthetic provenance are not enforced.
* `RV-009` (High, Blocking — Destination: `rpi-implement` via child task `216-citation-eval-2142-c8`):
  * Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`evaluate_citation_and_refusal_gates`). Case grading checks `actual` against `expected` without validating `case["question"]` against `refuse(question)` or verifying that prompt-refused questions require `expected["kind"] == "refused"` with matching refusal reason.
* `RV-010` (High, Blocking — Destination: `rpi-implement` via child task `216-citation-eval-2142-c8`):
  * Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_validate_benefit_thresholds`, `_score_paired_observations`). Negative `min_completion_gain`/`min_comprehension_gain` or `max_elapsed_ratio > 1.0` combined with speed-only `agg_ratio < 1.0` can report `measured_value=True` despite severe completion/comprehension regressions (`-100%`). Enforce non-regression floors (`>= 0.0` completion and comprehension gain per role and aggregate, `<= 1.0` effort ratio per role and aggregate) alongside positive lift.
* `RV-011` (Medium — Destination: `rpi-implement` via child task `216-citation-eval-2142-c8`):
  * Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`observation_surface_digest`). Projecting through `_to_plain_json` converts invalid UTF-8 strings to `ascii(value)` before canonical hashing, colliding with literal `ascii(value)` strings. Preserve invalid UTF-8 strings for `["invalid_utf8_str", ascii(value)]` tagging during surface hashing while retaining sequence/mapping/datetime JSON equivalence.
* `RV-012` (Medium — Destination: `rpi-implement` via child task `216-citation-eval-2142-c8`):
  * Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`render_extractive_answer`, `_expected_from_bundle`). Malformed card mappings (`cards=[{}]`) or empty `cards=[]` on non-conflict answers still render `kind="answer"` instead of failing closed to `refused`.
* `RV-013` (Medium — Destination: `rpi-implement` via child task `216-citation-eval-2142-c8`):
  * Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_normalize_json_value`, `_is_strict_json_value`, `_to_plain_json`, `_verify_comparison_evidence`). Arbitrarily large integers (`10**5000`) exceed Python's 4300-digit `int_max_str_digits` decimal conversion limit in `str(value)`, `ascii(value)`, and `json.dumps(...)`, raising `ValueError` instead of failing closed to `cards_only`.
* `RV-014` (Medium — Destination: `rpi-implement` via child task `216-citation-eval-2142-c8`):
  * Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_build_gate_result`, `_verify_agreed_gates_report`). `_build_gate_result` checks `passed_count < total_count` unconditionally, rejecting runs such as `9/10` (`0.9`) even when an owner explicitly agrees `min_rates` of `0.8`, and `_verify_agreed_gates_report` short-circuits on individual imperfect turns before replaying `evaluate_citation_and_refusal_gates`.
* Follow-up (Out of Scope — Destination: distinct cross-package follow-up outside `src/core`):
  * Wiring `RegulatoryChat.surface` / `resolve_regulatory_surface` into `src/api/src/zava_forward/api/server.py` and deduplicating `src/agents` helpers remain outside the user-bounded `src/core` deliverable.
