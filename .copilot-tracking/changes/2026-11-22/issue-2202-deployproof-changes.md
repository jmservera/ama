---
title: Issue 2202 deploy proof changes record
date: 2026-11-22
---

# Changes

Tier: focused (documentation plus live read-only probes; no `src` change; no Azure change; nothing pushed). `rpi-checks.py --all` not run.

## Files

* docs/reference/research/issue-2202-deployproof-2026-11-22.md and its folder (probes, JSON, 11 screenshots)
* docs/reference/README.md (index entry), docs/reference/log.md (entry)
* .copilot-tracking research, critique, plan, details, changes, review and state files

## Divergences

* The 2255 backfill tool was not run: the earlier live backfill is still present.
* The brief's resident AI poll across the hourly window was stopped once the 2245 note showed the ledger expiry as the probable cause; no ledger or suspension change was made.

## Per-criterion table

| Item | Status |
| --- | --- |
| 1. Hazard target clock and named owner (2255/76) | Proven (22 hazard cases plus 1 safeguarding case show clocks and owners) |
| 2a. Generative answer, employee chat (2245) | Unproven: open all-scope suspension from 2026-11-18; disclosure fix proven |
| 2b. Generative answer, resident app (2243) | Unproven: "AI usage limit was reached"; ledger expiry probable cause, not read directly |
| 3. Resident chart text and markers (2253) | Proven |
| 4. Safety count tile, map, list, API (2254) | Proven (23 everywhere) |
| 5. Handoff waiting shows untimed offers (2256) | Proven (4 rows) |
| 6. Map loads with readings | Proven (443 markers in 3.3 s; fresh 58) |
| Independent review, hosted CI, full gate | Unproven here (not applicable to a docs-only focused tier) |
