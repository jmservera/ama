---
title: Issue 1288 live changes
ms.date: 2026-11-22
---

Tier: focused; no `src` change (FULL not triggered; `rpi-checks.py --all` not run). Refs #1288. Changes record persisted before edits.

## Changes

* Added `docs/reference/research/issue-1288-live-r9-quality-sensor-evidence-2026-11-22.md`.
* Added a pointer to `docs/reference/README.md` and an entry to `docs/reference/log.md`.
* Added evidence `.copilot-tracking/evidence/2026-11-22/issue-1288-live9/` (focused tests, scrubbed probe JSON and script, two screenshots).
* Added RPI research, critique, plan, details, changes, review and state records.

## Validation

* Main current: `HEAD..origin/main` empty.
* `src/api` focused tests: 92 OK, 9 skipped.
* Live read-only probe and Playwright screenshots; no Azure change; no secrets recorded.
* Link check of the new note: all targets exist.

## Per-criterion table (unticked criteria)

| Criterion | Status | Evidence or reason |
| --- | --- | --- |
| 3 Snapshot consumes identical UI reading IDs | Proven locally (mock provider); unproven live | 92 tests; no live model request |
| 4 Release-admitted durable, deduplicated, bounded proactive flag | Unproven | Release record missing (OQ-017); forecast endpoint 503/504 during window |
| 5 Employee sees finding, cited IDs, time, model, unapproved status | Proven locally; unproven live | No live model output exists |
| 6 Explicit missing, stale, unavailable states with human route | Proven locally; missing and unavailable seen live | 5 of 12 `consent-withheld`; stale not seen this window |
| 7 Focused SQL, API, browser tests correlate UI and snapshot | Proven as local engineering evidence | Fixture and mock provider; earlier SQL and browser runs stand |
| 8 Finite live walkthrough with actual model consumption and flag | Unproven | Model leg blocked: no approved release record, and none may be fabricated |

Divergences: none. Remaining work: named release owner approval, forecast 503/504 diagnosis.
