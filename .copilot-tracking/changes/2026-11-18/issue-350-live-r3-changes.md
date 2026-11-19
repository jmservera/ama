---
title: Issue 350 live parity r3, changes
ms.date: 2026-11-18
---

Refs #350. Docs and retained evidence only; no source change; tier FOCUSED (no src edit, so no FULL gate and no rpi-checks run).

Files added: docs/reference/research/deployed-parity-live-r3-2026-11-18.md and its folder (9 raw outputs, 4 screenshots, 12 staff screenshots showing personal names or addresses not retained, 7 scripts); index row in docs/reference/README.md; log entry in docs/reference/log.md. Dated RPI artifacts under .copilot-tracking/{research,plans,changes,reviews}/2026-11-18/.

Divergence: the brief's state path `.copilot-tracking/rpi-sessions/2026-11-18/issue-350-live-state.json` already held the tracked run 1 state; it was overwritten with the r3 state. The run 1 content stays in git history (commit before this one). Run 1 and run 2 artifacts are untouched.

Validation: documentation link and diff review (links to the 4 retained screenshots and raw files checked by listing); secret scan of raw outputs for password text (none); local session files deleted; no Azure resource created or changed, nothing to delete. mypy, ruff and unit tests not applicable (no code change).

## Per-criterion result (live demo, 2026-11-18 14:04 to 14:10 UTC)

| # | Criterion | Proven | Unproven, and why |
| --- | --- | --- | --- |
| 1 | Browser-mode API 401, page redirect kept | Page redirect kept; native curl 401 | Browser-UA JSON API returns 302 on all 8 protected API paths (fails); needs platform-principal design with #349, edge change not authorised |
| 2 | Staff prerequisite, dated rows, 16 assets | One staff session; 13 routes and law viewer render; 16 assets return 200 (8 match repo) | No writes or other roles; 8 assets older than head; aftercare 403 |
| 3 | Synthetic baseline | 443 open, 537 completed, 30 visits, finance, funding, handoffs readable | Restoration authority unrecorded; sensor and contractor cases invisible (403); ranking unsigned |
| 4 | Models, five assistants, release | Deployment Succeeded; five assistants, nine tasks; 87 persisted RAI records | Bounded release absent (human-owned); active release suspension SUS-1; no live draft or restart proof |
| 5 | Map provider and agreement | OSM tiles 33 x 200; stats, chart, map, list, CSV agree at 443; closed CSV 537 | Licensed provider is an owner decision; sensor agreement 403; own-queue CSV 133 vs list 16 |
| 6 | Own-user photo | None | 503; token store disabled; consent and edge change not authorised |
| 7 | Law store | Fail-safe 503 behaviour and viewer state | Store unset; seeding is human-owned data change |
| 8 | Ledger, document, digest, jobs | Ledger intact 1,943; continuity valid; Event Hub Active | digests_checked 0; no upload durability proof; all jobs Manual, no schedule |
| 9 | Time capture gated | Case work independent | /api/time/status 500 ProgrammingError, no gated explanation; source fix needs FULL tier |
| 10 | Per-role results | Programme Manager reads and exports; resident showcase, no staff API | Other roles, consent, finance and grant actions, chat dialogue, recovery |

No criterion is fully proven; none is ticked.
