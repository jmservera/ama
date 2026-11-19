---
title: Issue 119 live audit r2 plan
ms.date: 2026-11-18
---

## Goal

Per-criterion audit of issue 119 against the repository and the live synthetic demo, with production-only items separated. Docs-only; no `src` change, so the FOCUSED tier applies and `rpi-checks.py --all` is not run.

## Decisions

* Owner decisions of 2026-11-18 apply: demo, desktop only; no billing reconciliation, DPO or Legal approval, or person-run assistive-technology testing for the demo.
* Earlier `issue-119-live` artifacts stay unchanged; this run writes `issue-119-live-r2` files.
* Critique runs once on this plan; compatible findings are applied directly.

## Phases

1. [x] Research: live config read, Playwright re-probe, vendor page re-read (`.copilot-tracking/research/2026-11-18/issue-119-live-r2-research.md`).
2. [x] Plan and critique: this file, details file, critique file.
3. [x] Implement: write `docs/reference/research/issue-119-live-r2-map-evidence-2026-11-18.md` with the per-criterion table; add dated update to `docs/reference/research/ux/map-tile-provider-options.md`; update `docs/reference/README.md` index and append `docs/reference/log.md`; write the changes record.
4. [x] Review: one review, markdown link and diff review, secret scan, sloptrim detector on prose.
5. [x] Commit locally; no push.

Details: `.copilot-tracking/details/2026-11-18/issue-119-live-r2-details.md`.
