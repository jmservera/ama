---
title: Issue 2202 live changes, 2026-11-24
ms.date: 2026-11-24
---

## Changes

* Added `docs/reference/research/issue-2202-live-r68-2026-11-24.md` and its evidence folder (az state, probes, screenshots, tiles, coverage).
* Added an index row in `docs/reference/README.md` and an entry in `docs/reference/log.md`.
* No `src/` change: no defect found. Tier: focused (documentation and evidence). `rpi-checks.py --all` not run. Azure: read-only, nothing created or deleted.
* Divergence: evidence was gathered before this record was written; it changes no source file.

## Per-criterion table (Refs #2202; not closing)

| Criterion | Status | Evidence |
| --- | --- | --- |
| API, resident, simulator, receiver images rebuilt from main and rolled | Partly proven | New digests live on all four; digest-to-commit unprovable (registry firewall refuses this identity) |
| Revisions Running and Healthy | Proven | API 0000068, resident 0000030 Healthy 100%; agents Healthy ScaledToZero |
| ZF_CONTAINER_HARDENING enforced | Proven | `enforced` on three apps and both jobs |
| Rollback noted | Noted, not exercised | No drills authorised |
| Agents app difference explained | Proven | Idle by design (min replicas 0, no ingress) |
| Sensor charts | Proven | live-chart-probe.json |
| Map gauges | Proven | live-map-card-probe.json |
| Consent checkbox | Proven | probe-live-result.json |
| Chat routing | Proven | live_routing_probe.json (routing and refusal; allowance used, so no generative answer) |
| Half of homes with readings | Proven, 262 of 443 (59.1%) | coverage-result.json |
| Live receipt and log entry | Proven | research note and log entry |

Unproven: image provenance per digest, rollback drill, generative AI answers (owner actions SUS-1 and budget expiry).
