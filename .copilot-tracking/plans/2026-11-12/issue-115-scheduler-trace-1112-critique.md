# Issue 115 scheduler trace plan critique (2026-11-12, 1112)

* Execution: one independent pass (rubber-duck subagent, read-only, final candidate). Verdict: proceed with changes. Gap confirmed real.
* Disposition of findings (all compatible, applied directly, none conflicts with a confirmed decision):
  1. Keep the existing `DocumentStoreError` branch and its "unavailable" wording (test line 119); add a separate generic branch emitting only the exception type name. Applied.
  2. Include `open_digest_store` (can raise `ValueError`) and `open_store` in the boundary; keep exit 2 for an absent URL. Applied.
  3. Test publish failure and verify failure separately, with a secret sentinel in the exception message that must not appear in output. Applied.
* Residual (not fixed, recorded): `SystemExit` from SQL configuration or schema checks passes through without an immediate marker; `--reconcile` keeps its own markers; catching `Exception` removes the traceback from console output.
* Marker-binding Bicep test judged justified, not duplicative of `test_ledger_alerts_use_azure_monitor_resource_specific_console_schema`.
