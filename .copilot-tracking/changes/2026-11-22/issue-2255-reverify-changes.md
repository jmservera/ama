---
title: Issue 2255 changes record, live re-verification
date: 2026-11-22
---

# Changes

Tier: focused. No `src` change; read-only live probe on revision 0000054; no SQL write, deploy, Azure resource or push; `rpi-checks.py --all` not run.

## Files

* docs/reference/research/issue-2255-reverify-2026-11-22.md and folder (probe_clock.py, probe-rev54.json, screens/safety-queue-rev54.png).
* docs/reference/README.md index entry; docs/reference/log.md entry.

## Divergences

* Two early probe runs counted 1 clock because the queue had not finished rendering (and a changed briefing layout hid the old row-count pattern); the probe now waits for the last ranked row. A scratch API probe showed `hazard` is only a boolean in the list API, so the UI is the evidence; it was discarded.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Elapsed time shown against a target (22 of 22 hazard rows, 0 unknown) | Proven on 0000054 |
| Some clocks running with a target window (5 open, 17 overdue) | Proven |
| Named accountable owner still shown (23 rows) | Proven |
| Hazard service stays timing authority | Partly: seeded due times are synthetic reference values |
| Survives a new revision | Proven |
| Survives a dataset re-seed | Unproven: not tested, a re-seed drops the fields (backfill note) |
| Independent exact-head review, hosted CI, full local gate | Unproven here |
