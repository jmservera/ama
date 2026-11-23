# Issue 146 live research (2026-11-23)

Research disposition: executed. Planning Readiness: Ready.

Scope: synthetic demo, resource group `ama`, read-only Azure CLI (`az monitor metrics alert list`, `az monitor scheduled-query list`, `az resource list` for workbooks). Nothing was created, so nothing needs deleting. Prior notes: `docs/reference/research/issue-146-live5-monitoring-2026-11-22.md` and earlier.

## Live observations (2026-11-23 about 17:45 UTC)

* 13 metric alerts: enabled are Foundry throttle, SQL CPU, API 5xx and restarts (both prefixes). Disabled: job failed for `demo-audit`, `demo-orch`, `demo-load`; IoT routing orphaned/invalid/dropped and ingress throttle.
* 8 scheduled-query rules: enabled are Key Vault expiry and denied, ledger digest mismatch and verify-missing (both prefixes, severity 1). Disabled: `ai-limits`, `agent-tasks-poison`.
* One workbook resource exists. Every rule has one action group.
* No live `sql-dtu` or `job-live-receiver` rule: those are source-only (main already carries the Bicep).

## Gap found

Criterion 1 ("alerts cover job failures, poison, ledger digest, IoT") has no executable, repeatable check that classifies live inventory into those four classes and distinguishes installed-and-enabled from installed-but-disabled. Prior notes did this by hand each pass. Code can satisfy a repeatable offline classifier fed by CLI JSON, with unit tests. It cannot enable the rules (needs activation approval reference and, for poison, a verified signal and drill; out of demo authority: no drills).

## Unticked criteria

| Criterion | Provable by code or tooling | Disposition |
| --- | --- | --- |
| 1 Alerts for job, poison, ledger, IoT | Classification of coverage: yes. Firing: no | Build classifier; whole criterion stays unproven |
| 2 Workbook availability, errors, latency, cost | Render needs private-link workspace access | Unproven; workbook resource installed |
| 3 Runbook entry with owner | Test-enforced entries exist; named person is a human decision | Unproven |
| T2 Usage beside Azure cost | Proven for demo 2026-11-18 | Not re-run |

Selected: criterion 1 classifier, `infra/scripts/monitoring_live_inventory.py` plus `infra/tests/test_monitoring_live_inventory.py`.
