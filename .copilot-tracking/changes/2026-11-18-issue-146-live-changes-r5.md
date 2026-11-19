# Changes: issue 146 live closure (2026-11-18)

Tier: FOCUSED (documentation and evidence only; no src, infra, workflow or dependency change). Refs #146; no closing keyword.

Files
* docs/reference/research/issue-146-live3-monitoring-closure-2026-11-18.md (new)
* docs/reference/research/issue-146-live3-evidence-2026-11-18/ (new raw output, Playwright script; two screenshots deleted because they showed names)
* docs/reference/README.md (index row), docs/reference/log.md (entry)

Live actions: read-only az inventory; Playwright sign-in as the employee test account; deleted three tmp146 metric alerts and one tmp146 job left by the earlier stalled worker (post-cleanup list shows none).

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| C1 Alerts: job failures, poison queue, ledger digest, IoT | Unproven as a whole (digest proven) | Digest alert installed and fired Sev1. Job: Total shape fired, source Maximum shape did not on two fresh failures; no permanent rule. Poison: not installed, signal unreadable (private query). IoT: signal present, no alert |
| C2 Dashboard or workbook: availability, errors, latency, cost vs budget | Unproven | No workbook installed; private-link query prevents render |
| C3 Runbook entry with an owner per alert | Unproven | Entries exist; owners are proposed roles, no named appointment |
| T2 AI usage by capability beside Azure cost, variance visible | Proven for demo except the Azure cost record | Playwright shows usage by capability and "unreconciled"; Azure cost not shown (billing reconciliation out of scope) |
| Four ticked criteria | Not re-opened | |

Validation: `python3 -m unittest` over ten infra monitoring test modules: 61 tests OK (infra/ cwd). Credential literal scan of retained text/JSON: 0 matches. Not run: rpi-checks.py --all, src mypy/ruff (no src change). Hosted CI and independent review outstanding.

Follow-ups (ranked): 1 change source job-failure alert aggregation Maximum to Total and retest (FULL tier); 2 verify StorageQueueLogs for the poison candidate; 3 name owners.
