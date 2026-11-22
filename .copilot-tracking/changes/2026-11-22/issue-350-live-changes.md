---
title: Issue 350 live changes (2026-11-22)
---

Refs #350. Tier FOCUSED (documentation and evidence only; no src change; no Azure change, nothing to delete). Hosted CI and independent exact-head review remain outstanding; no local gate was run.

## Changes

* Added docs/reference/research/issue-350-live-r5-2026-11-22.md, its raw/ evidence (edge, non-secret Azure state, redacted API shapes, blob listing, two screenshots) and scripts/probe.py.
* Updated docs/reference/README.md (index row) and docs/reference/log.md (entry).

## Per-criterion proven/unproven table

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Anonymous API 401 for browser requests, redirect kept | Unproven, failing (browser UA 302; needs FULL-tier edge change) |
| 2 | All dated rows and 16 assets via public app, authorised roles | Partly proven (one role, reads only) |
| 3 | Representative continuing synthetic baseline | Partly proven (980 cases present; provenance and sensor/document cases unseen) |
| 4 | Model deployment, release authority, five assistants, tasks | Partly proven (release authority and live model call unproven) |
| 5 | Licensed map provider; map/list/chart/CSV/sensor agreement | Partly proven (443 agree; licence, CSV, sensor unproven) |
| 6 | Delegated photo tokens | Unproven (photo off, correct fallback) |
| 7 | Versioned law store configured and seeded | Partly proven (configured, 4 cards, 0 sources; unseeded) |
| 8 | Ledger, document, digest durability, scheduled jobs | Partly proven (chain intact, digests present, jobs succeed; immutability, documents unproven) |
| 9 | Time capture gated | Proven for the demo |
| 10 | Per-role workflow, consent, finance, chat, export, law, recovery results | Unproven |

No box is ticked; the owner ticks after review.
