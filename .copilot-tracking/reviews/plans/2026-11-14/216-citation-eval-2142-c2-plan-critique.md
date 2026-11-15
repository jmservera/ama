<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #216 Child Hardening Pass 2 (`216-citation-eval-2142-c2`)

## Metadata

* Task ID: 216-citation-eval-2142-c2
* Critique date: 2026-11-14
* Execution status: Complete
* Verdict: Revise

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Low]: `_canon_json` with `allow_nan=False` would raise `ValueError` on `math.nan` / `math.inf` inside untrusted case or report inputs, and `resolve_regulatory_surface` should guard non-`Mapping` `bundle`

* Scope: `P01-T01`
* Evidence: `P01-T01` specifies `json.dumps(..., allow_nan=False)` after recursive `Mapping`/`Sequence` normalization without normalizing non-finite floats (`math.nan`, `math.inf`, `-math.inf`) or non-JSON objects (`GateResult`), and `resolve_regulatory_surface` accepts `bundle: Mapping[str, Any]` at runtime where an untrusted caller could pass a non-`Mapping`.
* Direct planner resolution: Normalize non-finite `float` values to `{"__nonfinite_float__": repr(value)}` inside `_normalize_json_value`, pass `default=repr` to `json.dumps(..., allow_nan=False)`, and guard `isinstance(bundle, Mapping)` in `deterministic_rule_cards` and `resolve_regulatory_surface`.
