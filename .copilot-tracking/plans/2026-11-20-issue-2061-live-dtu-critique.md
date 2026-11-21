# Critique: issue 2061 live deploy plan (2026-11-20)

Executed once by an independent read-only reviewer. Verdict: Revise; all five findings are compatible with the owner decisions and are applied directly.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | Plan stops only on Delete; Updates may drift auth, retention, access | Applied: the full what-if is read for every Modify on SQL, Key Vault, storage and IoT Hub; consequential changes are recorded and judged before deploy. |
| 2 | DTU SKU compatibility with ledger, zone and backup redundancy unproven | Applied: live DB properties captured first; compiled S0 request compared with them; what-if must show no change to ledger, redundancy or collation. |
| 3 | `routingReady=true` before the sender role exists | Applied: two stages. Stage 1 `iotHubRoutingReady=false` creates the `eh-` namespace and role; verify role propagation; stage 2 `true` moves the route. The brief telemetry gap is accepted for the demo and recorded. |
| 4 | Private connectivity unverified | Applied: gate stage 2 and the old-namespace deletion on the new private endpoint state, DNS and receiver reads from the target environment. |
| 5 | Rollback incomplete for the IoT route and the old namespace | Applied: live route, endpoint and SQL properties are saved to the evidence directory before deploy; `evhns-cutover-test-demo` is deleted last, only after telemetry flows; its buffered messages are not needed (synthetic, 1-day retention). |
