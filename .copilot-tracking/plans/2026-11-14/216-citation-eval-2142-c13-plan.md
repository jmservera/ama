# Implementation Plan: Child Hardening Pass 13 for Issue #216 (`RV-030`..`RV-033`)

* Task ID: `216-citation-eval-2142-c13`
* Parent Task ID: `216-citation-eval-2142-c12`
* Date: `2026-11-14`
* Status: `Finalized`
* Changes Record Path: `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c13-changes.md`

## Executive Summary

This finalized plan delivers child hardening pass 13 (`216-citation-eval-2142-c13`) inside `src/core` to close all four findings (`RV-030`..`RV-033`) from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c12-review.md` and incorporate all four single-pass critique refinements (`PC-001`..`PC-004`):

1. Substantiated constituent freshness evidence (`RV-030`, `PC-001`): `_card_provenance_valid` and `_active_bundle_nonconflicting(..., *, as_of_day: str | None = None)` require every constituent entry in `source_freshness["sources"]` to carry `"status"` in `{"in_cadence", "out_of_cadence", "unknown"}`, require `"in_cadence"` and `"out_of_cadence"` constituent entries to carry valid ISO day `"last_success"`, `_strict_int` `"cadence_days"` (`1..36600`, rejecting `bool`), and `"due_on"` equal to `(date.fromisoformat(last_success) + timedelta(days=cadence_days)).isoformat()` (checked against `ref_day = as_of_day or entry_as_of_day or fresh_as_of_day`, never against `card["clock"]` SLA text), and reject `"unknown"` constituent entries claiming non-`None` `"last_success"` or `"due_on"`.
2. Compliance-judgment paraphrase refusal coverage (`RV-031`, `PC-004`): `_REFUSAL_PATTERNS[1]` uses bounded ReDoS-safe single-clause spans (`[^.;!?]{0,40}`) with Unicode hyphen/dash coverage (`\u2010`..`\u2015`, `\u2212`) to reject interrogative and declarative compliance, breach, legality, obligation-qualified `meet`/`satisfy`, and inspection-pass determinations across singular/plural subjects (`property`, `home`, `building`, `dwelling`, `flat`, `block`, `case`, `tenancy`, `landlord`, `repair`, `works?`) across `refuse_question`, `RegulatoryChat.bundle`, and `RegulatoryChat.surface` without false-refusing the 13 `DEFAULT_EVAL_CASES` or 25 `test_regulatory_chat.py` tests.
3. Dual-capacity gate-owner agreement (`RV-032`, `PC-003`): `agreement_gaps` requires explicit sign-off from both designated gate-owner capacities in `GATE_OWNERS` (`owner` matching `LEGAL_GATE_OWNER` for `citation_validity` and `compliance_owner` and/or `refusal_owner` matching `COMPLIANCE_GATE_OWNER` for `refusal_accuracy`), enforces unconditional `independent_grader` distinctness whenever `grader is not None`, and requires complete non-blank Legal + Compliance partner owner IDs distinct from `independent_grader_id` whenever any `*_id` key is supplied (leaving `threshold_status == "provisional_not_agreed"` on failure).
4. Owner-supplied unit-cost ceiling enforcement (`RV-033`, `PC-002`, preserving `BRD OD-51`): `_validate_benefit_thresholds` requires caller-supplied `max_ai_cost_per_accepted_check_gbp` and/or `max_cost_per_accepted_check_gbp` to be finite positive non-`bool` floats (rejecting conflicts if both keys are present, while keeping `benefit_thresholds=None` by default with zero hardcoded repository target per `BRD OD-51`), and `compare_chat_against_rule_cards` compares exact unrounded unit cost (as well as rounded `ai_cost_per_accepted_check`) against the ceiling, gating `beside_cost["max_ai_cost_per_accepted_check_gbp"]` and `beside_cost["within_unit_cost_ceiling"]` on `trial["thresholds_valid"]`.

## Sources and Evidence

* `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c13-research.md` (`C1`..`C8`)
* `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c12-review.md` (`RV-030`..`RV-033`)
* `src/core/src/zava_forward/core/source_monitor.py`
* `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* `src/core/src/zava_forward/core/regulatory_chat.py`
* `src/core/tests/test_regulatory_eval_gates_216.py`
* `src/core/README.md`

## User Decisions and Requirements

* Deliver all remaining locally verifiable Issue #216 acceptance criteria strictly inside `src/core` on branch `feat/ai-216-citation-eval-2142`.
* Citation validity and refusal accuracy gates must be set with named owners (`LEGAL_GATE_OWNER` and `COMPLIANCE_GATE_OWNER`) and measured on a graded and adversarial set.
* Paired comparison must report value of chat over deterministic rule cards with links beside AI cost per accepted check (or `"Unknown"` with missing inputs named) while respecting Issue #216 `BRD OD-51` ("no price, budget or target is set here, and a missing price source means cost is Unknown"); if no measured value at its cost, ship cards alone.
* Verify in `src/core` using bare `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*216*.py' -v`.
* Keep `.copilot-tracking/` references out of `src/core` code, tests, docs, and commit messages; commit cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` and do not push.

## Goals

* Substantiate `"in_cadence"` and `"out_of_cadence"` rule-card provenance with complete constituent monitoring fields matching `source_monitor.source_freshness` (`RV-030`).
* Refuse compliance, breach, legality, and statutory-duty determination paraphrases across `refuse_question`, `RegulatoryChat.bundle`, and `RegulatoryChat.surface` without false-refusing factual provision/cadence queries (`RV-031`).
* Require explicit `LEGAL_GATE_OWNER` and `COMPLIANCE_GATE_OWNER` sign-off in `agreement_gaps` before granting `threshold_status == "owner_agreed"` (`RV-032`).
* Require caller-supplied `benefit_thresholds.max_ai_cost_per_accepted_check_gbp` (with zero hardcoded default target in `src/core` per `BRD OD-51`) and fail closed to `cards_only` when known `ai_cost_per_accepted_check` exceeds it (`RV-033`).

## Scope and Non-Goals

* Scope:
  * `src/core/src/zava_forward/core/regulatory_eval_gates.py`
  * `src/core/tests/test_regulatory_eval_gates_216.py`
  * `src/core/README.md`
* Non-Goals:
  * Modifying `src/api`, `src/agents`, `src/orchestrator`, `src/importer`, `docs/`, or `tools/`.
  * Inventing or hardcoding a repository-wide tokenomics price, budget, or cost target while `BRD OD-51` is open.
  * Pushing commits or opening pull requests.

## Functional Requirements

* `FR-01` (`RV-030`, `PC-001`): In `_card_provenance_valid` and `_active_bundle_nonconflicting(..., *, as_of_day: str | None = None)` (wired from `_inspect_bundle_surface` and `grade_chat_turn`, distinct from `card["clock"]` SLA text), every constituent entry in `card["source_freshness"]["sources"]` must include `"status"` in `_FRESHNESS_STATUSES`. When constituent `"status"` is `"in_cadence"` or `"out_of_cadence"`, the entry must include valid ISO day `"last_success"`, `_strict_int` `"cadence_days"` in `1..36600` (rejecting `bool`), and valid ISO day `"due_on"` equal to `(date.fromisoformat(last_success) + timedelta(days=cadence_days)).isoformat()` (with `last_success <= ref_day` and `ref_day < due_val` for `"in_cadence"` / `ref_day >= due_val` for `"out_of_cadence"` whenever `ref_day = as_of_day if as_of_day is not None else (entry_as_of_day or fresh_as_of_day)` is a valid ISO day). When constituent `"status"` is `"unknown"`, `"last_success"` and `"due_on"` must be `None` if present, and `"cadence_days"` if present and non-`None` must pass `_strict_int` in `1..36600`. Cross-card constituent tuples `(est, ls_val, cd_int_or_none, due_val)` are compared only after `_strict_int` / `_is_utf8_str` validation.
* `FR-02` (`RV-031`, `PC-004`): In `_REFUSAL_PATTERNS[1]`, use bounded ReDoS-safe single-clause spans (`[^.;!?]{0,40}`, no `.*` chains) and Unicode hyphen/dash classes (`[-\u2010-\u2015\u2212\s]+`) to refuse interrogative and declarative compliance, breach/violation, legality, inspection-pass, and obligation-qualified `meet`/`satisfy` determinations across singular/plural subjects without false-refusing the 13 `DEFAULT_EVAL_CASES` or 25 `test_regulatory_chat.py` tests.
* `FR-03` (`RV-032`, `PC-003`): In `agreement_gaps`, require `owner` matching `LEGAL_GATE_OWNER` AND require at least one of `compliance_owner` or `refusal_owner` to be present and non-blank, with every supplied key in `("compliance_owner", "refusal_owner")` matching `COMPLIANCE_GATE_OWNER`. Evaluate `independent_grader` `_canon_name` and `_base_person` distinctness unconditionally whenever `grader is not None` against `LEGAL_GATE_OWNER`, `COMPLIANCE_GATE_OWNER`, and every supplied non-blank owner string. Whenever any key in `("owner_id", "compliance_owner_id", "refusal_owner_id", "independent_grader_id")` is present, require non-blank `"owner_id"`, non-blank `"independent_grader_id"`, and non-blank partner Compliance-owner ID(s) (`"compliance_owner_id"` when `"compliance_owner"` is present, `"refusal_owner_id"` when `"refusal_owner"` is present, and at least one non-blank Compliance owner ID overall, rejecting any blank/non-string present `*_id` key), requiring `_canon_name(grader_id)` to be distinct from every supplied owner ID while permitting `owner_id` to equal `compliance_owner_id` / `refusal_owner_id`.
* `FR-04` (`RV-033`, `PC-002`): In `_validate_benefit_thresholds`, accept `max_ai_cost_per_accepted_check_gbp` and/or `max_cost_per_accepted_check_gbp` (requiring at least one present, requiring every supplied key in `("max_ai_cost_per_accepted_check_gbp", "max_cost_per_accepted_check_gbp")` to be a finite positive non-`bool` float `> 0.0`, and rejecting mismatching values when both keys are present), keeping `benefit_thresholds=None` by default so zero price, budget, or target is hardcoded in `src/core` (`BRD OD-51`). Share an internal exact-unit-cost helper with `cost_per_accepted_check` (preserving `cost_per_accepted_check`'s public 4-key return contract) so `compare_chat_against_rule_cards` fails closed (`measured_value = False`, `ship_mode = "cards_only"`) whenever exact unrounded unit cost or rounded `ai_cost_per_accepted_check` exceeds `max_unit_cost`, and emit unrounded `float(max_unit_cost)` in `beside_cost["max_ai_cost_per_accepted_check_gbp"]` plus `beside_cost["within_unit_cost_ceiling"]` only when `trial["thresholds_valid"]` is `True` (`None` otherwise).
* `FR-05`: Update existing synthetic fixtures in `src/core/tests/test_regulatory_eval_gates_216.py` (`_valid_agreement`, the 3 `sub_one_*` inline agreements, `_valid_thresholds`, `multi_bundle`, and `unmapped_bundle`), add focused regression test `test_c13_substantiated_freshness_paraphrase_refusal_dual_owners_and_cost_ceiling` (maximum 1 test method addition; exact test removals: `none`), and update `src/core/README.md`.

## Non-Functional Requirements

* `NFR-01`: Strict type-safety under bare `python3 -m mypy` (`0` errors across all 318 source files) and clean `ruff check .` / `ruff format --check .`.
* `NFR-02`: Fail-closed behavior on non-UTF-8 strings, booleans masquerading as ints/floats (`isinstance(True, int)` rejected via `_strict_int` / `_finite_float`), `NaN`/`Inf`, and calendar overflow.
* `NFR-03`: Zero `.copilot-tracking/` path leaks in `src/core`.

## Acceptance Criteria

* `AC-01`: `_card_provenance_valid` and `_active_bundle_nonconflicting` reject `"in_cadence"` and `"out_of_cadence"` cards whose constituent `sources` omit `"status"`, `"last_success"`, `"cadence_days"`, or `"due_on"` (or spoof `cadence_days=True`), while accepting real `source_monitor` `"unknown"`, `"in_cadence"`, and `"out_of_cadence"` outputs.
* `AC-02`: `refuse_question` and `RegulatoryChat.surface` (under both `comparison=None` and `comparison=positive_cmp`) refuse interrogative, plural, declarative, and Unicode-hyphen compliance/breach/duty paraphrases (including `"Is this property compliant with the hazard law?"`) while preserving all 13 `DEFAULT_EVAL_CASES` and all 25 `test_regulatory_chat.py` tests.
* `AC-03`: `agreement_gaps` rejects agreements missing `compliance_owner` / `refusal_owner` or missing partner `compliance_owner_id` / `refusal_owner_id` when `*_id` keys are supplied (leaving `threshold_status == "provisional_not_agreed"` and blocking `PASS` / `chat_with_cards`) and accepts agreements naming both `LEGAL_GATE_OWNER` and `COMPLIANCE_GATE_OWNER` with a distinct `independent_grader`.
* `AC-04`: `compare_chat_against_rule_cards` validates `max_ai_cost_per_accepted_check_gbp` and `max_cost_per_accepted_check_gbp` (including conflicting dual keys and exact unrounded unit cost), gates `beside_cost["max_ai_cost_per_accepted_check_gbp"]` on `trial["thresholds_valid"]`, and ships `cards_only` when unit cost exceeds the owner ceiling while setting zero hardcoded cost target in `src/core` defaults.
* `AC-05`: Bare `mypy`, `ruff check .`, `ruff format --check .`, `unittest discover -s tests -p 'test_*216*.py' -v`, and companion suites (`test_regulatory_chat.py`, `test_gates.py`, `test_live_doc_links.py`) pass cleanly.

## Critique Disposition

* Critique Artifact: `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c13-plan-critique.md` (`Complete`, single-pass verdict `Revise`)
* `PC-001` (`Critical`, `direct_planner_correction`): Applied directly in `FR-01`, `AC-01`, `P01-T01`, and `P01-T02`. Wired `as_of_day: str | None = None` into `_active_bundle_nonconflicting` (keeping `card["clock"]` strictly for SLA signature equality), added `_strict_int` validation on `cadence_days` before cross-card tuple comparison, and enforced `ref_day` date inequalities across active and self-dated cards.
* `PC-002` (`High`, `direct_planner_correction`): Applied directly in `FR-04`, `AC-04`, `P01-T01`, and `P01-T02`. Supported both `max_ai_cost_per_accepted_check_gbp` and `max_cost_per_accepted_check_gbp` (rejecting conflicts if both appear), compared exact unrounded `total_cost / accepted_f` via a shared internal helper, preserved unrounded `float(max_unit_cost)` without `round(..., 6)` zero-collapse, and gated `beside_cost["max_ai_cost_per_accepted_check_gbp"]` + `beside_cost["within_unit_cost_ceiling"]` on `trial["thresholds_valid"]`.
* `PC-003` (`High`, `direct_planner_correction`): Applied directly in `FR-03`, `AC-03`, `P01-T01`, and `P01-T02`. Corrected `"provisional_target"` to `"provisional_not_agreed"`, made `independent_grader` distinctness unconditional whenever `grader is not None`, and required complete partner Legal + Compliance `*_id` sets whenever any `*_id` key is supplied.
* `PC-004` (`Medium`, `direct_planner_correction`): Applied directly in `FR-02`, `AC-02`, `P01-T01`, and `P01-T02`. Specified bounded ReDoS-safe single-clause spans, plural/declarative/inflected compliance and breach forms, Unicode dash support, obligation-qualified `meet`, and corrected `DEFAULT_EVAL_CASES` count to 13.

## Phase Checklist

<!-- P01 -->
### [x] Phase P01: Harden Provenance Substantiation, Refusal Paraphrases, Dual-Owner Agreement, and Unit-Cost Ceiling (`src/core`)

<!-- P01-T01 -->
* [x] Task P01-T01: Implement `RV-030`..`RV-033` in `src/core/src/zava_forward/core/regulatory_eval_gates.py`

<!-- P01-T02 -->
* [x] Task P01-T02: Update fixtures, add `test_c13_*` regressions in `src/core/tests/test_regulatory_eval_gates_216.py`, update `src/core/README.md`, and run `src/core` validation

## Follow-Up Items

* Cross-package follow-up outside `src/core` caller scope: wire `src/api` HTTP endpoints directly to `RegulatoryChat.surface` and consolidate duplicated helper code in `src/agents` in a separate multi-package issue/PR.
