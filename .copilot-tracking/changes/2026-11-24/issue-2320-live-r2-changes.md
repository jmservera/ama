---
title: Issue 2320 live re-check on revision 0000061, changes
ms.date: 2026-11-24
---

No src change. Tier: focused (documentation and evidence only). Hosted CI for the exact head and independent review remain required; `rpi-checks.py --all` was not run.

Files added or changed:

* docs/reference/research/issue-2320-live-r2-2026-11-24.md and docs/reference/research/issue-2320-live-r2-2026-11-24/ (probe script, two JSON runs, screenshot)
* docs/reference/README.md (index entry), docs/reference/log.md (append)
* `.copilot-tracking/` RPI artifacts for this run

Validation: probe JSON checked by the script for the absence of the sign-in values; no secrets recorded.

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| #2320 profile where the briefing spends time | Proven | earlier note, live drop 11 to 14 s to 0.12 s |
| #2320 within 5 s or named state, no 503 on a quiet system | Partly proven: 12 of 12 under 0.16 s, no 503; "quiet" unproven (shared traffic), first GET after a change still writes | probe-r61 runs 1 and 2 |
| #2320 test proves read path avoids the write lock | Proven for repeat GET under a denial (merged test); first GET after change unproven | merged test, live timing |
| #2320 live re-check with elapsed times | Proven for briefing; forecast still 503 | research note |
| #145 backup redundancy and retention match #121 | Unproven, production-only (Local, 14 days, no approved decision) | az sql db show |
| #145 allowance closed after restore | Unproven live (restore drill not authorised) | none |
| #2245 chat call cap holds | Proven live (`call-budget-limit`, workflow-only reply) | container log 12:33:32 |
| #2245 "Model calls: 1", clear rule-based wording | Unproven (allowance spent; wording unchanged) | probe asks |
| AI-hold notice, retention endpoint | Proven | screenshot, probe |
| Forecast endpoint | Disproven (503 after 13 to 17 s) | probe, log |

No issue boxes ticked (the repository ticks after merge); #2320 criteria 1 and 4 are candidates.
