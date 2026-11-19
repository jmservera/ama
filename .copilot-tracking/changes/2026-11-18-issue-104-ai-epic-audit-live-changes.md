---
title: Issue 104 audit changes
description: Changes record with per-criterion proven or unproven table
ms.date: 2026-11-18
---

## Files

* Added docs/reference/research/issue-104-epic-audit-live-2026-11-18.md.
* Edited docs/reference/README.md (index row) and docs/reference/log.md (entry).
* Evidence: .copilot-tracking/evidence/2026-11-18/issue-104-live/ (probe script, scrubbed JSON, filtered az output, screenshot).

## Classification and validation

Tier FOCUSED, docs-only; no src, SQL, infra or workflow change. Commands: `az containerapp show` (read-only); Playwright GET probe (6 calls, HTTP 200, first login attempt timed out then succeeded); from src/agents `python3 -m unittest tests.test_epic104_bounded_ai_invariants -q` (27 tests, OK; observed, raw output not retained); link check of the new note (no missing targets); no em dashes. Not run: mypy and ruff (no Python source changed), `rpi-checks.py --all` (prohibited), sloptrim detector (not installed). Hosted CI and independent review outstanding. Nothing ticked in any issue.

## Per-criterion table (epic 104 and children)

| Item | Proven for demo | Unproven and why |
| --- | --- | --- |
| #104 c1 stabilization #440 | No | #440 open; owner pivot/defer decisions absent |
| #104 c2 children closed or deferred | No | #107 #108 #164 #216 open, no deferral recorded |
| #104 c3 AI never approves/executes/ranks/mutates | Yes (consistent, live + 27 tests observed, raw output not retained) | already ticked |
| #104 tokenomics c1 (#432) | Yes (Unknown stated, #432 closed) | already ticked |
| #104 tokenomics c2 limits and owned alert | Yes (live alert, tasks disabled) | already ticked |
| #107 independent SQL worker/race/restart | Partly (local MSSQL, SQLite proxy) | no MSSQL old-image test; no Azure SQL (no drills) |
| #107 approved record, delivered-build proof | Denial side only | no approver (OQ-017) |
| #108 model/version/quota | Partly | subscription quota route empty |
| #108 frozen held-out split | Partly | independence, thresholds approval |
| #108 humans block seeded errors | No | needs people |
| #108 effort/cost comparison | No | needs measured effort, Finance |
| #108 hashes/protocol/outcomes | Partly | no reviewer protocol or outcome |
| #108 finite authority, attestation | Partly | payload approval, attestation absent |
| #108 delivered-build proof | Partly | no cited generative output; release denied |
| #108 one-lever routing/caching | Offline only | no live lever run |
| #164 thresholds, accountable reviewer | Partly | thresholds proposed, reviewer unknown |
| #164 results bound to versions | Partly | 0 chat model calls |
| #164 human exercises | No | needs people |
| #164 payload/authority/consent | Partly | approvals absent |
| #216 gates measured | Partly | 7 model answers; 13 prompts not model-tested; production ownership |
