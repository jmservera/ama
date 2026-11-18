<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #216 Child Hardening Pass 3 (`RV-001`..`RV-003`)

## Metadata

* Task ID: 216-citation-eval-2142-c3
* Critique date: 2026-11-14
* Verdict: Revise (compatible findings applied directly)

## Findings

### PC-001 (Medium) - Capture `effective_now` and include `cases`, `paired_cards`, and `gates_report` in `verified_comparison_inputs` for full replay

* Detail: `compare_chat_against_rule_cards` uses `_score_paired_observations` and passes `now` to `cost_per_accepted_check`. Capturing `effective_now = now if now is not None else datetime.now(UTC)` once and storing `cases`, `paired_cards`, `gates_report`, `observations`, `benefit_thresholds`, `cost_inputs`, `rule_hazard_misses`, and serialized `effective_now` inside `verified_comparison_inputs` allows `_verify_comparison_evidence` in `resolve_regulatory_surface` to replay `_verify_agreed_gates_report`, `_score_structural_baseline`, `_score_paired_observations`, and `cost_per_accepted_check` deterministically without clock drift or trusting structural summary numbers.
* Disposition: Applied directly to `216-citation-eval-2142-c3-plan.md` and `216-citation-eval-2142-c3-phase-details.md`.

### PC-002 (Low) - Check `math.isnan` explicitly and check `GateResult` / `bool` before `int` in `_normalize_json_value`

* Detail: Explicitly branching on `math.isnan(value)` for non-finite floats and ensuring `bool` precedes `int` guarantees unambiguous tags across every Python scalar and dataclass.
* Disposition: Applied directly to `216-citation-eval-2142-c3-phase-details.md`.
