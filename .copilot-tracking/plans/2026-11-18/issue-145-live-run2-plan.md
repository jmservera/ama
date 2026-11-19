---
title: Issue 145 live run 2 plan
ms.date: 2026-11-18
---

# Plan: re-verify and close out #145 criteria (Refs #145)

* Tier: FOCUSED. No `src/` edit; documentation and tracking only. No `rpi-checks.py --all`.
* [x] Phase 1: read-only Azure checks (databases, jobs, backup and retention policy, earliest restore, blob protection).
* [x] Phase 2: code check for restore reconciliation of release, suspension and allowance state.
* [x] Phase 3: write the research note with the per-criterion table; update index and log.
* [x] Phase 4: link check, diff review, commit locally.
* Boundaries: no restore, no seeding, no database or Key Vault change, no push.
