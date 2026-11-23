---
title: Issue 1288 live changes
ms.date: 2026-11-23
---

Docs and evidence only; no `src` file changed (focused tier). Nothing created or changed in Azure.

* Added `docs/reference/research/issue-1288-live-r10-quality-sensor-evidence-2026-11-23.md`.
* Updated `docs/reference/README.md` and `docs/reference/log.md`.
* Evidence: `.copilot-tracking/evidence/2026-11-23/issue-1288-live10/`.
* No amendments or divergences from the plan.

## Per-criterion result (revisions 0000054 and 0000026, HEAD `b11b8259bd`)

| Criterion | Result |
| --- | --- |
| 1 Read model (ticked) | Seen live again: 12 readings, stable IDs, units, UTC, provenance |
| 2 UI values and context (ticked) | Seen live: Home sensors panel screenshot |
| 3 Quality AI snapshot uses identical readings | Proven locally (92 tests, mock provider); unproven live |
| 4 Release-admitted proactive deduplicated flag | Unproven: release record missing (OQ-017) |
| 5 Finding, cited IDs, model, unapproved status visible | Proven locally; unproven live (no model output) |
| 6 Explicit missing, stale, unavailable states | Proven locally; seen live (`consent-withheld`, `not-configured`); stale not seen |
| 7 Focused tests correlate UI and snapshot | Proven as local engineering evidence |
| 8 Finite live walkthrough with actual model | Unproven: model leg blocked by release admission |
| 9 Human acceptance controls intact (ticked) | Unchanged; no source change |

Owner-gated: criteria 4 and 8 need a named release owner to approve a finite release record.
