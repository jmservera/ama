# Changes: issue 146 live monitoring proof (2026-11-18)

Tier: FOCUSED. Documentation-only repository change; no `src/` or `infra/` file edited, so FULL is not triggered. `rpi-checks.py --all` was not run.

Files: `docs/reference/research/issue-146-live-monitoring-evidence-2026-11-18.md` (new), `docs/reference/README.md`, `docs/reference/log.md`.
Live Azure actions (resource group `ama`): throwaway `tmp146-*` job-failure and IoT metric alerts, scheduled-query test alert (fired 08:28:37Z) and workbook, all deleted; verified none remain.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Alerts cover job failures, poison queue, ledger digest, IoT ingestion | Partly proven | Ledger digest alert installed and firing; job-failure and IoT rules created against real signals then deleted; poison queue unproven (no queue logs, private network) |
| Dashboard or workbook shows availability, errors, latency, cost against budget | Partly proven | Workbook deployed to the demo and deleted; rendering unproven because workspace query is private-link only |
| Each alert has a runbook entry with an owner | Partly proven | 20 runbook entries with proposed owner roles, tests pass; named humans not appointed |
| Tokenomics: AI usage by capability beside cost, variance visible | Unproven live | Panels exist in the deployed workbook; cannot render or query; no cost export |

Test alert fired; email delivery not independently observed. Adverse observation: the live Sev1 ledger digest mismatch alert fired at 2026-11-18T08:18:52Z.

## Validation

* `cd infra && python3 -m unittest tests.test_monitoring_alert_coverage tests.test_ai_alert_runbook_ownership tests.test_monitoring_workbook_sla_budget tests.test_diagnostic_log_privacy`: 21 tests OK.
* mypy, ruff, src suites: not applicable (no code changed).
* Hosted CI: not observed; nothing pushed.

Witness note: implement-start reported the README/log edits predated it (the evidence note was authored during research).
