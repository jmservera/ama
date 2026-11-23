---
title: Issue 2257 r2 changes
ms.date: 2026-11-23
---

Classification: documentation and evidence only; focused tier; no src change, so no FULL gate and no rpi-checks run.

## Changes

* Added `docs/reference/research/issue-2257-live-r2-2026-11-23.md` and `issue-2257-live-r2-2026-11-23/` (probe scripts, result JSON, screenshots, console window).
* Index row in `docs/reference/README.md`; entry in `docs/reference/log.md`.

## Per-criterion table

| Criterion | Proven or unproven | Evidence |
| --- | --- | --- |
| Map recovers from a dropped connection without reload | Proven live on 0000055 | recovery-proof-result.json, screenshots |
| Map recovers from a server-side overlay failure | Proven live (two logged overlay failures, map 200) | console-window.txt, probe-result-071740.json |
| Fresh-session failures gone | Unproven as a rate: 8 of 8 passed, 8 samples | probe-result-071740.json |
| Cause found | Largely proven; lock inferred from briefing 503 cause tag, driver message unlogged | console-window.txt |
| Billing, DPO/Legal, person-run AT | Not needed for the demo (owner decision 2026-11-18) | brief |
| Azure estate unchanged | Proven: read-only az and browser probes | this record |
