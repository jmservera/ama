---
title: Issue 108 live demo changes
description: Changes record with per-criterion proven/unproven table for issue 108
ms.date: 2026-11-18
---

Refs #108. Documentation and evidence only; no source change; tier FOCUSED (documentation link and diff review plus the targeted harness tests). `rpi-checks.py --all` not run.

## Files

* `docs/reference/research/issue-108-live-demo-evidence-2026-11-18.md` (new research note)
* `.copilot-tracking/evidence/2026-11-18/issue-108-live/` (probe script, endpoint JSON, screenshot, Azure CLI outputs)
* `docs/reference/README.md` (index row), `docs/reference/log.md` (entry)
* `.copilot-tracking/` research, plans, details, challenges, changes, reviews, session state

## Per-criterion table (unticked criteria)

| # | Criterion | Result |
| --- | --- | --- |
| 1 | Model names, versions, quotas confirmed in region | Proven for deployments and rate limits; subscription quota unproven (empty usages route) |
| 2 | Frozen independently labelled held-out split | Partly proven; independence unproven |
| 3 | Competent humans detect and block seeded errors | Unproven (needs people) |
| 4 | Effort and cost comparison, Finance validation | Unproven |
| 5 | Hashes, seed, denominators, serving version, protocol, outcomes | Partly proven; no reviewer protocol or outcome |
| 6 | Authorisation, payload handling, attestation, consent | Partly proven; payload approval and attestation unresolved |
| 7 | Real AI/SQL/Azure proof (CON-009/AC-057) | Partly proven; restart SQL checks and registered cited task unproven |
| 8 | One routing or caching lever vs baseline | Offline mechanism only; no live lever measured |

Nothing is newly tickable. Production-only items stay deferred (#1905-#1908).

## Residue

No Azure resource created. Focused harness tests: 115 OK from `src/agents`.
