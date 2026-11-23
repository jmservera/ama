---
title: Issue 2255 live run 4 changes
ms.date: 2026-11-23
---

## Changes

* Added `docs/reference/research/issue-2255-live-r4-2026-11-23.md` and its evidence folder (probe script, JSON, page text, screenshot).
* Indexed it in `docs/reference/README.md` and appended `docs/reference/log.md`.
* No source, infra or Azure change. Tier: focused (no src change); `rpi-checks.py --all` not run.

## Per-criterion proven/unproven table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Elapsed time shown against a target, not "unknown" | Proven on revision 0000055 | 22 of 22 hazard rows, 0 unknown |
| Some clocks running with a target window | Proven | 5 open with due time, 17 overdue |
| Named accountable owner still shown | Proven | owner text on every hazard row |
| Hazard service stays timing authority | Partly proven | page text names the service as authority; seeded times are synthetic |
| Survives a dataset re-seed | Unproven, owner-gated | generator outside repository; destructive re-seed not authorised |
| Independent review, hosted CI, full local gate | Unproven here | no src change; coordinator runs gates |
