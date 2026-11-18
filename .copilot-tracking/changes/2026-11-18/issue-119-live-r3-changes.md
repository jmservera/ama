---
title: Issue 119 live r3 changes
ms.date: 2026-11-18
---

Tier FOCUSED (docs and evidence only; no src, SQL, infra or security change; no rpi-checks run). Base c94c4f0fa.

## Changes

* Removed five named-resident/officer PNGs under `.copilot-tracking/evidence/2026-11-18/issue-119-live/` (map-list-open, keyboard-focus-list, keyboard-opened-case, tiles-blocked-list-works, landing-no-map).
* Edited `docs/reference/research/issue-119-live-map-evidence-2026-11-18.md`: removed links, added removal note.
* Appended `docs/reference/log.md`.

## Validation

* Grep for the removed file names under `docs/`: no remaining links.
* Visual review of all six first-run PNGs; `map-desktop-1366.png` and r2 copies show no names and stay.
* Independent review also redacted person names from link text in `probe2.json` and `probe3.json` (issue-119-live) and `probe2.json` (issue-119-live-r2), replaced by `[name removed]`; JSON still parses and counts are unchanged. The removed screenshots stay in Git history of earlier commits.

## Issue 119 criteria (no new live run; carried from the prior note)

| Criterion | Status | Basis |
| --- | --- | --- |
| Provider licence, cost, coverage and processor terms recorded | Partly proven (demo OSM provider recorded); unproven for a licensed production provider | `docs/reference/research/issue-119-live-map-evidence-2026-11-18.md`; no licensed provider chosen, no price or processor agreement |
| Screen reader test of the list alternative | Unproven | Person-run assistive-technology testing out of demo scope (owner 2026-11-18); engineering proxies only (a11y tree, keyboard, tile-failure) |

Neither box is ticked.
