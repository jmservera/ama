---
title: Issue 144 live3 changes
ms.date: 2026-11-18
---

Refs #144. Tier: focused (documentation only, no src change; FULL tier not triggered).

## Files

* docs/reference/research/issue-144-hosting-proof-live-2026-11-18.md and its raw folder (new).
* docs/reference/README.md, docs/reference/log.md (index and log).

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Worker and job images real, versioned, deployed through the pipeline | Partly proven; pipeline clause unproven (no `src-deploy.yml` runs, protected runners and OIDC outside demo authorisation) |
| Scale rules, probes, limits, rollback (ticked) | Re-observed; rollback not exercised |
| Container hardening enforced in the deployed app | Unproven; non-root proven only |
| Load test without production claim (ticked) | Re-observed at demo scale (1,752 requests, p95 27.8 s cold start) |
| Single-replica and restart with audit persistence (ticked) | Not re-run (drills excluded) |
| Tokenomics drivers (ticked) | Re-observed; cost Unknown |

Cleanup: `/tmp/zz144` removed in-session; no Azure resource created. Local helper scripts in /tmp removed.
