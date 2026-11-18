---
title: Issue 119 live audit r2 changes
ms.date: 2026-11-18
---

## Status

Implementation complete. No source file under `src/` or `infra/` changed; docs-only, FOCUSED tier. `rpi-checks.py --all` was not run, per the brief.

## Files changed

* `docs/reference/research/issue-119-live-r2-map-evidence-2026-11-18.md` (new): live observations, vendor re-read, criteria table, production-only items, adverse evidence.
* `docs/reference/research/ux/map-tile-provider-options.md`: dated update section; earlier text unchanged.
* `docs/reference/README.md`, `docs/reference/log.md`: index row and log entry.
* `.copilot-tracking/evidence/2026-11-18/issue-119-live-r2/`: probes, JSON and screenshots.
* `.copilot-tracking/{research,plans,details,critique,changes,reviews}/2026-11-18/issue-119-live-r2-*.md` and the session state file.

## Per-criterion table

| Criterion | Proven for the demo | Unproven or production-only |
| --- | --- | --- |
| Provider licence, cost, coverage and processor terms recorded | Demo provider (public OSM): ODbL licence, attribution shown, no charge and no SLA under the policy, global coverage, tile request contents; vendor pages for Azure Maps, OS, MapTiler and OSM re-read and recorded | No licensed provider chosen; paid Azure Maps rate, OS plan prices, MapTiler commercial terms and every processor agreement unread or absent; selection and contracting are production decisions |
| Screen reader test of the list alternative | Engineering proxies only: accessibility tree, keyboard path, list works with tiles blocked | No screen reader was run (not needed for the demo per owner decision 2026-11-18); real assistive-technology acceptance is production-only |

## Validation

Checks run: link resolution script, literal credential scan, `git status` showing no `src/` or `infra/` change. Not applicable: unit tests, mypy, ruff, web checks, `rpi-checks.py`. Sloptrim detector unavailable. Details in the review record.

