# Research: issue 2205 restrict AI quality analysis to demo homes (2026-11-21)

Research disposition: executed. Planning Readiness: Ready. Refs #2205 #134 #184.

## Findings

* Source already enforces the scope when `ZF_ASSIST_QUALITY_DEMO_HOMES` holds exactly five unique home ids (`src/core/src/zava_forward/core/assistants.py`: `Limits.__init__`, `quality_scope_denial`, scan skip, `_permit_block`, execute path). Invalid or empty values refuse Quality for every case. Unset means every case (legacy).
* The background scan skips Quality when the scope is set or invalid; proactive Quality work is not enqueued, claimed or permitted. No per-reading call path exists: readings arrive via the simulator, which never invokes the model.
* Offline tests exist in `src/api/tests/test_assistants.py` (scan, manual admit/refuse, invalid, existing task, legacy). They do not assert that the scope is visible to an operator, so "effective scope lists only the demo cohort" has no inspectable record.
* Live state (read-only Azure CLI, resource group ama, 2026-11-21): `ca-cutover-test-demo-api` revision 0000039 has no `ZF_ASSIST_*` variables, so the scope is unset and the assistant authority is absent (assistants disabled: authority, allowance and expiry are required). `job-live-simulator` has no scope variable either.

## Gap and decision

Add a read-only `quality_scope` block to the assistants registry so the effective scope can be recorded before the demo, plus tests and a runbook preflight command. Setting the variable on the live app is an Azure write and out of scope; it stays unproven live.

## Criteria status before work

| Criterion | Status |
| --- | --- |
| Effective scope lists only the demo cohort | Source enforced; no inspectable listing; live unset |
| Operator-only trigger, no per-reading calls | Source proven by tests; live not configured |
| Scope recorded before demo; model-call authority referenced | Not recorded |
