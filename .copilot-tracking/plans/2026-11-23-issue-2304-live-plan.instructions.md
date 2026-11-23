---
applyTo: '.copilot-tracking/changes/2026-11-23-issue-2304-live-changes.md'
---

# Plan: issue 2304 forecast statement count

Research: `.copilot-tracking/research/2026-11-23-issue-2304-live-research.md`. Critique: `.copilot-tracking/plans/2026-11-23-issue-2304-critique.md`. Details: `.copilot-tracking/details/2026-11-23-issue-2304-live-details.md`.

* [x] Phase 1: profile (SQLite counting connection, live baseline probe)
* [ ] Phase 2: add `forecast_reads.py`, wire into `Assistants.forecast`, map `ForecastTimeout` in the API
* [ ] Phase 3: regression tests (flat statement count, named unavailable state), run existing assistant tests, ruff and mypy
* [ ] Phase 4: deploy to the demo and re-check live elapsed time; research note with per-criterion table
* [ ] Phase 5: review, commit locally, never push
