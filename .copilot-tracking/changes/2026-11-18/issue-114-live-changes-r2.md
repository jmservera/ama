---
title: Changes for issue 114 live re-verification
ms.date: 2026-11-18
---

Planned: add `docs/reference/research/issue-114-live-reverify-2026-11-18.md`, index entry, log entry. No source changes.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Per-year audit and ledger digest verification proven by test before reliance | Proven by tests on main (62 OK); unproven on the deployed demo image | Image lacks `verify_ledger_before_reliance`; roll is a deployment change not authorised here; live data holds one year |
| Measured load, latency and cost against PRD targets | Already ticked; not re-run | Prior note sql-ledger-live-2026-11-18.md |
| Backup, restore and deletion re-application (DH-005) | Already ticked; not re-run | Prior note |

Done: added the research note, index row in `docs/reference/README.md`, log entry. Validation: 62 tests OK (command in note); links reviewed; diff reviewed.

Correction: the first writes overwrote earlier tracked same-named artifacts; they were restored from git and this run's artifacts use the `-r2` suffix. The state file at the mandated path replaces the earlier tracked state (its prior content stays in git history).
