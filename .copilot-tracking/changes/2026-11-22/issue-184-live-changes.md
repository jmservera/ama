---
title: Issue 184 live changes (2026-11-22)
---

Planned changes: add `docs/reference/research/issue-184-live-chain-2026-11-22.md`, a `docs/reference/README.md` index row and a `docs/reference/log.md` entry. No src change; focused tier. No Azure resource created or changed.

## Per-criterion table

Added the research note `docs/reference/research/issue-184-live-chain-2026-11-22.md`, an index paragraph and a log entry. No src change; no Azure change. Checks run: read only Azure CLI, Log Analytics, Playwright probe; documentation link and diff review.

| Criterion | Verdict | Basis |
| --- | --- | --- |
| All child stories closed or deferred | Proven | #185 to #189 closed |
| Simulator never connects to or represents installed real devices | Proven for live traffic | 288 of 288 `SYN-` devices over 6 hours |
| No device key or connection string in source, logs or telemetry | Proven for last 6 hours of logs and current source; telemetry content not inspected | 0 pattern matches |
| Simulator to Hub to receiver to SQL to employee map | Proven for the demo; SQL hop inferred | Hub ingress equals egress; receiver Succeeded; case sensors fresh; map 443 items |
| Resident view shows live readings | Unproven | Test account declined consent; history ends 03:30Z; consent change is a write |
