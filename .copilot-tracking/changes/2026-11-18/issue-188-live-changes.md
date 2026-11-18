---
title: Issue 188 live proof changes
ms.date: 2026-11-18
---

Refs #188. Validation tier: focused (no `src/` change; `rpi-checks.py --all` not run).

## Per-criterion result

| Criterion | Status | Evidence |
| --- | --- | --- |
| Live and backfill series queryable together per home | Proven (demo weather schema) | 24 rows per home, one schema, unique ordered slots; 36 backfill ACCEPTED, 36 live via Hub, 0 failed |
| No discontinuity at handover | Proven (engineering bounds) | Join steps inside 2.82 degC / 10.02 percent; official verifier `passed: true` |
| Idempotent re-run | Proven | Replay receipts 36/36 backfill, 36/36 Hub; `idempotent: true`; snapshot sha256 unchanged |
| Production X.509 receiver and `api-consumer` on live Azure | Unproven | Basic demo namespace has only `$Default`; production path needs X.509 and Standard tier |
| Indoor-schema backfill joined to a live stream | Unproven | Indoor backfill home has no live stream; verifier refuses mixed schemas |

Full record: [docs/reference/research/issue-188-live-backfill-evidence-2026-11-18.md](../../../docs/reference/research/issue-188-live-backfill-evidence-2026-11-18.md).

## Files

* Added the research note above; updated `docs/reference/README.md` and `docs/reference/log.md`.
* Added dated research, plan, details, critique, changes and review artifacts and the session state.

## Azure actions

* Created `job-188-probe`, two temporary role assignments and three SAS devices; all removed (job and roles deleted, devices deleted by the driver). IoT hub still has public access Disabled and local auth disabled.
* Residue: 72 synthetic ledger rows in `sensor_reading` (ledger, not deletable).
* Divergence: first verify run failed `INSUFFICIENT_HANDOVER_SAMPLES` (handover on first slot); the driver was corrected to the window midpoint.
