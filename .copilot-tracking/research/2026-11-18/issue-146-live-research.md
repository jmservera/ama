# Issue 146 live monitoring research (2026-11-18)

Research disposition: executed. Planning Readiness: Ready.

Scope: unticked criteria of #146 on the synthetic demo in resource group `ama`.
Starting inventory (read-only `az` queries): metric alerts for Foundry throttle, SQL CPU, API 5xx and API restarts; scheduled-query alerts for ledger digest mismatch, ledger verify missing and two Key Vault alerts; action group `ag-cutover-test-ops`; budget 300 (category Cost). No job-failure, poison-queue or IoT alert, and no workbook, existed.
Evidence is recorded in `docs/reference/research/issue-146-live-monitoring-evidence-2026-11-18.md`.
