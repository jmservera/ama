<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #216 Child Closure (`RV-001`..`RV-006`) in `src/core`

## Metadata

* Task ID: 216-citation-eval-2142-c1
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c1-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Single final-candidate critique for child task `216-citation-eval-2142-c1` verifying that `P01-T01` and `P01-T02` completely and cleanly resolve parent review defects `RV-001`..`RV-006` inside `src/core` without regressions or contradictions, while preserving `ALLOWED = {"core"}`, zero new test files, zero test removals, zero `pyproject.toml` relaxations, and clean `mypy`, `ruff`, and `unittest` checks.
* Research and evidence considered: .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c1-research.md; .copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-review.md; .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c1-plan.md; .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c1-phase-details.md; src/core/src/zava_forward/core/regulatory_eval_gates.py
* Decisions, dependencies, and acceptance criteria considered: `FR-1`..`FR-6`, `NFR`, `P01`, `P01-T01`, `P01-T02`, parent review findings `RV-001`..`RV-006`, and parent follow-up boundaries (keeping `src/agents`, `src/api`, and operational governance outside scope).
* Assessment boundary: Evaluates exact contract consistency across the child plan, phase details, child research, parent review, and `src/core/src/zava_forward/core/regulatory_eval_gates.py`. Does not read files outside the caller-supplied read boundary (`src/core/src/zava_forward/core/regulatory_chat.py` and `src/core/tests/test_regulatory_eval_gates_216.py`).

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| `FR-1` / `E1` / `RV-001` | Partial | `P01-T01` item 1 hardcodes `"No role-visible recorded home facts were projected for this purpose."` for empty `expected_facts`, contradicting `render_extractive_answer` in `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`str(bundle.get("unknown") or "No permitted structured home fact selected for this purpose.")`), and leaves `refused` sections and `answer` `unknown_or_conflict` open to appended unsupported claims (`PC-001`). |
| `FR-2` / `E2` / `RV-002` | Partial | `evaluated_outputs_sha256` binds `cases` and `actual` outputs, but `compare_chat_against_rule_cards` still copies `cit_check` and `ref_check` rates/outcomes into `beside_cost` even when `gates_report` fails schema or digest binding (`PC-005`). |
| `FR-3` / `E3` / `RV-003` | Covered | Counting `(chat_hazard_misses + cards_hazard_misses) > 0` across all observations as `failure_severity = "critical"` and appending a blocking reason in `compare_chat_against_rule_cards` cleanly resolves `RV-003`. |
| `FR-4` / `E4` / `RV-004` | Partial | Binding `agreement_gaps` to `LEGAL_GATE_OWNER` and `_validate_benefit_thresholds` to `COMPLIANCE_GATE_OWNER` closes arbitrary owner strings, but full-string `_canon_name(owner) != _canon_name(grader)` still permits `"Juan Manuel Servera"` or `COMPLIANCE_GATE_OWNER` to self-grade `LEGAL_GATE_OWNER` via parenthetical capacity variation (`PC-004`). |
| `FR-5` / `E5` / `RV-005` | Partial | Recomputing `deterministic_rule_cards(expected)` and checking exact per-card URL-encoded links and provisions resolves unioned/prefix parity, but unguarded subscript/attribute access and `str(expected_card['id'])` without `_nonblank_str` regress existing fail-closed handling on malformed `paired_cards` or `None` IDs (`PC-003`). |
| `FR-6` / `E6` / `RV-006` | Partial | Converting `in_tokens` and `out_tokens` via `_finite_float` after `_strict_int` prevents token overflow, but `total_cost / accepted_count` still raises `OverflowError` when `accepted_checks` is a huge integer such as `10**400` (`PC-002`). |
| `NFR` / `P01` / `P01-T01` / `P01-T02` | Partial | Scope, zero-new-file test strategy, and `mypy`/`ruff`/`unittest` verification commands are sound once `PC-001`..`PC-005` are tightened in `P01-T01` and `P01-T02`. |

## Verdict

* Verdict: Revise
* Rationale: `P01-T01` and `P01-T02` cover all six routed findings (`RV-001`..`RV-006`), cleanly resolve `RV-003`, and preserve `src/core` dependency and test-file boundaries, but contain one High internal contract contradiction in `RV-001` (`grade_chat_turn` vs `render_extractive_answer` empty-fact text plus remaining unguarded section text), two Medium fail-closed gaps in `RV-006` (`accepted_count` float division overflow and preserving `_strict_int` token type rejection) and `RV-005` (unguarded indexing/`str(None)` in `_score_structural_baseline`), and two Low tightening gaps in `RV-004` and `RV-002`. All five items are direct planner corrections requiring no user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `grade_chat_turn` empty-facts string contradicts `render_extractive_answer` and leaves refused/cadence sections open to appended prose

* Related IDs: `FR-1`, `E1`, `RV-001`, `P01`, `P01-T01`, `P01-T02`
* Evidence: src/core/src/zava_forward/core/regulatory_eval_gates.py; .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c1-phase-details.md; .copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-review.md
* Concern: `P01-T01` item 1 sets `expected_recorded_facts` when `expected_facts` is empty to `"No role-visible recorded home facts were projected for this purpose."` and ignores `expected.get("unknown")`, whereas `render_extractive_answer` in `src/core/src/zava_forward/core/regulatory_eval_gates.py` computes `str(bundle.get("unknown") or "No permitted structured home fact selected for this purpose.")`. In addition, `grade_chat_turn` still performs no exact check on `sections["what_sources_say"]` or `sections["recorded_home_facts"]` when `expected_kind == "refused"`, and uses a substring `in` check (when `expect_stale` is `True`) or no content check (when `expect_stale` is `False`) on `sections["unknown_or_conflict"]` for `answer` turns.
* Impact: Implementing `P01-T01` item 1 as written breaks consistency between `render_extractive_answer` and `grade_chat_turn` inside `regulatory_eval_gates.py` on empty-fact `answer` turns, while still allowing appended unsupported compliance claims in `unknown_or_conflict` or `refused` turn sections.
* Smallest useful change: Reconcile the canonical empty-fact fallback across `render_extractive_answer`, `RegulatoryChat`, and `grade_chat_turn` (respecting `_nonblank_str(expected.get("unknown"))` when present and sharing one canonical empty-fact constant), and require exact canonical strings for `refused` sections (`what_sources_say` and `recorded_home_facts`) and `answer` `sections["unknown_or_conflict"]` (`STALE_SNAPSHOT_NOTE` vs `FRESH_SNAPSHOT_NOTE`, aligned with `RegulatoryChat`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-1`, `P01-T01` item 1, and `P01-T02` specifying aligned canonical section strings across `render_extractive_answer`, `RegulatoryChat`, and `grade_chat_turn` for `answer` (with and without facts, fresh and stale) and `refused` turns, verified by unit assertions.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: `cost_per_accepted_check` still raises `OverflowError` on huge integer `accepted_checks` and must keep `_strict_int` token validation

* Related IDs: `FR-6`, `E6`, `RV-006`, `P01`, `P01-T01`, `P01-T02`
* Evidence: src/core/src/zava_forward/core/regulatory_eval_gates.py; .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c1-phase-details.md
* Concern: `P01-T01` item 6 converts `in_tokens` and `out_tokens` via `_finite_float` before float division, but leaves `unit_cost = total_cost / accepted_count` dividing a `float` by an arbitrary-precision `int` (`accepted_count = _strict_int(accepted_checks)`), which raises `OverflowError` when `accepted_checks = 10**400`. In addition, `P01-T01` should state explicitly that `in_tokens` and `out_tokens` keep `_strict_int` validation first so non-integer floats (such as `12.5`) continue to fail attributable-billing input validation rather than leaking to `authorise_model_run`.
* Impact: Huge integer `accepted_checks` inputs still raise an unhandled `OverflowError` instead of failing closed to `"Unknown"`, and replacing `_strict_int` with `_finite_float` on token inputs would alter float-rejection semantics and `missing_inputs` reporting.
* Smallest useful change: Specify in `P01-T01` item 6 and `P01-T02` that `in_tokens`, `out_tokens`, and `accepted_count` remain validated with `_strict_int` first and are then converted through `_finite_float` before float arithmetic, returning `"Unknown"` when any converted value is `None` or non-finite (testing both `input_tokens = 10**400` and `accepted_checks = 10**400`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-6`, `P01-T01` item 6, and `P01-T02` covering `_strict_int` + `_finite_float` conversion for `input_tokens`, `output_tokens`, and `accepted_checks`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `_score_structural_baseline` contract drops fail-closed type and non-blank ID guards

* Related IDs: `FR-5`, `E5`, `RV-005`, `P01`, `P01-T01`, `P01-T02`
* Evidence: src/core/src/zava_forward/core/regulatory_eval_gates.py; .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c1-phase-details.md
* Concern: Existing `_score_structural_baseline` guards `isinstance(card, Mapping)`, `isinstance(card_provs, list)`, and `isinstance(prov, Mapping)` so malformed `paired_cards` entries fail closed (`links_complete = False`) without raising exceptions. `P01-T01` item 5 writes `actual_card["id"]`, `actual_card["link"]`, `[(p.get("id"), p.get("link")) for p in actual_card["provisions"]]`, and `quote(str(expected_card['id']), safe='')` without `Mapping`/`list` guards or `_nonblank_str` ID checks.
* Impact: Malformed `paired_cards` payloads can raise `KeyError`, `TypeError`, or `AttributeError` instead of failing closed to `cards_only`, and `None` or blank IDs stringify to `"None"` or `""` (`/api/law/cards/None` or `/api/law/cards/`).
* Smallest useful change: Specify in `P01-T01` item 5 that `_score_structural_baseline` guards `isinstance(actual_card, Mapping)`, `isinstance(actual_card.get("provisions"), list)`, `all(isinstance(p, Mapping) for p in actual_card["provisions"])`, non-empty per-card `provisions`, and `_nonblank_str` on every expected/actual card and provision ID before constructing expected `/api/law/cards/{quote(card_id, safe='')}` and `/api/law/provisions/{quote(prov_id, safe='')}` URLs.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` item 5 preserving fail-closed `Mapping`/`list`/`_nonblank_str` validation alongside exact per-card provision and URL parity.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: `agreement_gaps` distinct-grader check allows same-person parenthetical capacity aliases

* Related IDs: `FR-4`, `E4`, `RV-004`, `P01`, `P01-T01`, `P01-T02`
* Evidence: src/core/src/zava_forward/core/regulatory_eval_gates.py; .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c1-phase-details.md
* Concern: Both `LEGAL_GATE_OWNER` and `COMPLIANCE_GATE_OWNER` in `src/core/src/zava_forward/core/regulatory_eval_gates.py` share the same person name (`"Juan Manuel Servera"`) qualified by different parenthetical capacities. Checking only `_canon_name(owner) != _canon_name(grader)` and optional IDs still permits `independent_grader = "Juan Manuel Servera"` or `independent_grader = COMPLIANCE_GATE_OWNER` to pass as distinct from `LEGAL_GATE_OWNER`.
* Impact: Weakens independent-grader separation on `OwnerGateAgreement` when the same named person is supplied without or with an alternate parenthetical capacity label.
* Smallest useful change: In `P01-T01` item 4 and `P01-T02`, also reject `independent_grader` when canonical base names before `"("` (`_canon_name(value.split("(", 1)[0])`) match and both are non-blank, in addition to full `_canon_name` and optional `owner_id` / `independent_grader_id` checks (and if an optional `compliance_owner` key is supplied on `agreement`, require it to match `COMPLIANCE_GATE_OWNER`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` item 4 and `P01-T02` rejecting same-person parenthetical capacity aliases as `independent_grader`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: Unbound or schema-invalid `gates_report` still populates `beside_cost` gate rates and outcomes

* Related IDs: `FR-2`, `E2`, `RV-002`, `P01`, `P01-T01`, `P01-T02`
* Evidence: src/core/src/zava_forward/core/regulatory_eval_gates.py; .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c1-phase-details.md
* Concern: In `compare_chat_against_rule_cards`, `cit_check` and `ref_check` are extracted from `gates_report.get("checks")` and echoed into `beside_cost` (`citation_validity_rate`, `citation_validity_outcome`, `refusal_accuracy_rate`, `refusal_accuracy_outcome`). If `P01-T01` item 2 only appends a reason on `evaluated_outputs_sha256` mismatch without gating `checks` on `gates_report.get("schema") == EVAL_SCHEMA` and a matching `evaluated_outputs_sha256`, `beside_cost` still reports stale `PASS` outcomes and `1.0` rates from an unbound report.
* Impact: Produces contradictory audit fields inside `compare_chat_against_rule_cards` (`measured_value = False` for unbound `gates_report` alongside `citation_validity_outcome = "Pass"` in `beside_cost`).
* Smallest useful change: In `P01-T01` item 2 and `P01-T02`, verify `isinstance(gates_report, Mapping) and gates_report.get("schema") == EVAL_SCHEMA and gates_report.get("evaluated_outputs_sha256") == evaluated_outputs_digest(cases)` before trusting `gates_report["checks"]`; when unbound, record a dedicated blocking reason and set `cit_check = None` and `ref_check = None` so `beside_cost` reports `None` rates and `UNKNOWN` outcomes (also recursively canonicalizing nested `Mapping`/`Sequence` values in `evaluated_outputs_digest`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` item 2 and `P01-T02` asserting both `measured_value is False` and `beside_cost` outcomes reset to `UNKNOWN` when `gates_report` is mutated/stale.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* `P01-T01` and `P01-T02` map one-to-one across all six parent review defects (`RV-001`..`RV-006`) without expanding file count or touching out-of-scope packages (`src/agents`, `src/api`, `pyproject.toml`).
* `RV-003` is cleanly closed by counting `hazard_missed is True` across `cards`, `chat`, and unpaired observations toward `failure_severity = "critical"` and blocking `measured_value`.
* Residual operational governance items (human threshold sign-off, external legal benchmark, and live staff trial with authorised spend) remain explicitly isolated in `Follow-Up Items`.

## Questions or Blocking Evidence Gaps

* None. No user decision or missing external evidence blocks final plan revision.

## Limitations

* Inspection strictly respected the caller-supplied five-file read boundary; `src/core/src/zava_forward/core/regulatory_chat.py` and `src/core/tests/test_regulatory_eval_gates_216.py` were not read directly during critique. When applying `PC-001` and `PC-004`, the planning parent / implementer should confirm exact section strings and existing test fixture owner fields against `regulatory_chat.py` and `test_regulatory_eval_gates_216.py`.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Revise `P01-T01` and `P01-T02` directly in `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c1-plan.md` and `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c1-phase-details.md` to incorporate `PC-001`..`PC-005`, record critique dispositions, and finalize for `rpi-implement` without another critique pass.
* User response required: no
