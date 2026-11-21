# Changes: issue 2205 (2026-11-21)

Status: implementation complete. Tier FULL (src change); targeted tests only, no `rpi-checks.py --all`; the coordinator runs gates.

## Files

* `src/core/src/zava_forward/core/assistants.py`: `quality_scope()` and a `quality_scope` key in both `registry()` returns (read-only, no behaviour change to enforcement).
* `src/api/tests/test_assistants.py`: `test_effective_scope_is_listed_for_the_operator_without_a_model_call`.
* `src/api/README.md`, `docs/capstone/demo/runbook.md`: scope listing, preflight record, status row.
* `docs/reference/research/issue-2205-live-2026-11-21.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

* `test_assistants` 140 tests OK (60 skipped, no SQL); `test_assistant_release`, `test_assistant_panel_a11y_159`, `test_ai_tasks` 153 tests OK.
* `src/api` mypy clean; `src/core` mypy 3 errors, identical on the unmodified tree (missing OpenTelemetry stubs). ruff check passed.
* No web UI files changed, so no Playwright proof applies. Azure access was read-only (`az containerapp show`); no writes, no model calls, no throwaway resources.

## Per-criterion table

| Criterion | Proven or unproven | Evidence |
| --- | --- | --- |
| Effective scope lists only the demo cohort | Proven in source and tests; unproven live | New registry test; live app has no `ZF_ASSIST_QUALITY_DEMO_HOMES` and setting it is an Azure write |
| Trigger is operator-only, no per-reading calls | Proven in source and tests; unproven live | Existing scan and permit tests, `provider.calls == 0`; live assistant authority absent |
| Scope recorded before the demo; model-call authority referenced | Unproven | Runbook preflight names the record; needs configured live app and current owner authority |

No issue box ticked.
