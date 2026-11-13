# Plan: #107 identity-field allow-list readiness (1143)

Refs #107. Tracking-only, no `src/` edits, no test runs.

## Phases

* [x] Research: correction history, source and compatibility
* [ ] Critique: independent `rubber-duck` on count and design
* [ ] Implement: write ledger, matrix and READY/HELD determination in the changes file
* [ ] Review: independent `code-review`, then clean local commit

## Proposed failing-first design (specification only)

* New test in `src/core/tests` (existing assistants test module): `shape_result` given a result with `provider`, `deployment` and `model` containing a sentinel such as `"sk-SENTINEL leaked\nline"` or an over-pattern string must yield `None` or a fixed sentinel-free value, while the accepted values (`azure-openai`, test deployments, `test-model`, `unattested`) are preserved byte-for-byte.
* Critique-driven additions: a sentinel without whitespace (for example `sk-SENTINEL0123456789`) must also be rejected, so a charset pattern alone is insufficient; the policy must be an explicit allow-list (trusted provider/deployment from `runtime_binding`/configured `ai` object plus released `serving_model` values) or the field is replaced by a fixed placeholder. Also test non-str, str-subclass, missing and length-boundary (120, 121, 512, 513) values.
* Boundary decision to record before implementation: `ai.py:200` passes the raw model to consumption, which applies `bounded_model` at `ai_consumption.py:772`. Fixing only `shape_result` leaves that ledger path; the failing-first set must cover both consumers or state the narrower scope.
* Minimal fix when later authorized: one allow-list helper beside `bounded_model` used by `shape_result` and the consumption path. Rejected: charset-only pattern.
* Compatibility gate before any source edit: trace producers and callers of `shape_result`, then run existing core/agents/api suites; passing suites alone do not prove `offline-extractive; zero model calls` or production-configured identities cannot reach it.

## Readiness rule

READY only if the spent correction count is established and below five. Otherwise HELD for source edit.
