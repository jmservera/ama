# Changes: issue 146 live monitoring evidence (2026-11-18)

Tier: FOCUSED, documentation only (no src, infra, SQL or workflow change). Azure use: read-only list, show and metrics queries; no resource created, so no cleanup.

Files: docs/reference/research/monitoring-coverage-live-146-2026-11-18.md (new), docs/reference/README.md (index line), docs/reference/log.md (append entry).

| Criterion | Status |
| --- | --- |
| Alerts: ledger digest verification | Proven installed (2 rules, enabled, ag-cutover-test-ops); fire proven in #115 note |
| Alerts: job failures | Unproven; not installed (Failed series exists, failed runs seen) |
| Alerts: poison queue | Unproven; not installed; queue has no diagnostic setting |
| Alerts: IoT Hub ingestion | Unproven; not installed (metrics flowing) |
| Dashboard or workbook: availability, errors, latency, cost vs budget | Unproven; none installed |
| Runbook entry with owner per alert | Entries proven in source; owners are proposed roles only |
| Tokenomics dashboard beside Azure cost with variance | Unproven; none installed, reconciliation out of scope |

Validation: relative link check and git diff review (below). Not run: unit tests, mypy, ruff, rpi-checks (no code change).
