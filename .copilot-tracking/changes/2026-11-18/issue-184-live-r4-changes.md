---
title: Issue 184 live audit changes
ms.date: 2026-11-18
---

## Changes

Refs #184. Documentation only; no source, workflow or Azure change. Tier: focused. Files: `docs/reference/research/issue-184-live-r4-2026-11-18.md`, its output folder, `docs/reference/README.md`, `docs/reference/log.md` and these tracking artifacts.

## Per-criterion result

| Criterion | Status | Basis |
| --- | --- | --- |
| All child stories closed or deferred | Unproven | #185 and #189 open, no owner deferral |
| Simulator never connects to, discovers or represents installed real devices | Already ticked; no regression | `SYN-` IDs and label in earlier live events; 135 tests pass |
| No device key or connection string in source, logs or telemetry | Already ticked; whole-log scope limited | Pattern scan matches test fixtures only; earlier job output 0 key matches |
| #185 credentials issued and stored without appearing in source or logs | Partly proven (demo) | Hub-generated keys, none in retained output; repository X.509 sink not exercised |
| #185 teardown removes all simulated identities | Proven (demo) | Run 3: 3 of 3 deleted; hub count 0 now |
| #189 run has an owner, a time limit and a budget alert | Partly proven | Budget alert live (USD 25, 80 and 100 percent); owner and expiry in source and tests only |

Production-only or owner items: closing or deferring #185 and #189, tier and credential-owner decisions, subscription-scope budget visibility.

## Validation

* `python3 -m unittest tests.test_live_control tests.test_live_simulator tests.test_simulator_admin` from `src/api`: 135 tests OK.
* Live outputs retained under `docs/reference/research/issue-184-live-r4-2026-11-18/`.
* Not run: mypy, ruff, `rpi-checks.py` (no executable change); hosted CI not observed.
* Azure: read-only; nothing created, nothing to delete. A transient device count of 3 on the shared hub was not mine and read 0 on recheck.
