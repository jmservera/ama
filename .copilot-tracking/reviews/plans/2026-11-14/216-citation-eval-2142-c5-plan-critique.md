<!-- markdownlint-disable-file -->
# Plan Critique: Issue #216 Child Hardening Pass 5 (`216-citation-eval-2142-c5`)

* Task ID: 216-citation-eval-2142-c5
* Critique date: 2026-11-14
* Execution status: Complete
* Verdict: Revise

## Findings

* `PC-001` (High, Blocking): Primitive subclasses (`str`/`int`/`float` subclasses) can override `__str__` or equality and alter meaning or collide keys during normalization. Require exact base types (`value is None`, `type(value) in (bool, int, str)`, `type(value) is float and math.isfinite(value)`, and `type(k) is str` for mapping keys) in `_is_strict_json_value` and `_normalize_json_value`.
  * Disposition: Applied directly to `216-citation-eval-2142-c5-plan.md` and `216-citation-eval-2142-c5-phase-details.md`.
* `PC-002` (High, Blocking): Project `normalized_cost_inputs` (with aware `datetime` `authority.expires_at` converted to `.isoformat()`), not raw `cost_inputs`, into `verified_comparison_inputs["cost_inputs"]`.
  * Disposition: Applied directly to `216-citation-eval-2142-c5-plan.md` and `216-citation-eval-2142-c5-phase-details.md`.
* `PC-003` (Medium, Blocking): Sanitize fallback `beside_cost` rate and outcome fields (`_finite_float` for rates and `_nonblank_str(...) or UNKNOWN` for outcomes) so failed comparison reports with unverified `NaN` or non-JSON `checks` remain strictly serializable with `json.dumps(..., allow_nan=False)`.
  * Disposition: Applied directly to `216-citation-eval-2142-c5-plan.md` and `216-citation-eval-2142-c5-phase-details.md`.
