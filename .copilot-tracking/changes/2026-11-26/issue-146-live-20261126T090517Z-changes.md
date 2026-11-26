# Changes, Refs #146

## Files
* infra/main.test.bicepparam: candidate alert gates true with dated reference.
* infra/tests/test_monitoring_alert_coverage.py: DemoParameterActivationTests.
* docs/reference/research/issue-146-live9-monitoring-2026-11-26.md: live evidence.
* docs/reference/log.md, docs/reference/README.md: entries.

## Live changes (resource group ama)
Enabled 3 job, 4 IoT, poison and AI-limit rules; created alert-job-live-receiver-failed; workbook now 14 items. No throwaway resources created.

## Validation
Infra monitoring tests (33) pass; `az bicep build infra/main.bicep` succeeds. Focused tier; no src change; rpi-checks --all not run. Hosted CI not observed (nothing pushed).

## Per-criterion table
| Criterion | Status |
| --- | --- |
| Alerts cover job failures, poison queue, ledger digest, IoT | Proven installed and enabled (demo); poison and IoT firing unproven (write blocked by policy, no transport fault provoked) |
| Workbook shows availability, errors, latency, cost vs budget | Partly proven: 14-item workbook deployed live; availability Insufficient (no availability test); cost Unknown/Unreconciled by owner decision; Portal render not captured |
| Each alert has runbook and owner | Unproven: roles proposed, no person named; four legacy alerts lack descriptions |
| Tokenomics dashboard usage beside cost with variance | Proven for demo (tile deployed live) |
