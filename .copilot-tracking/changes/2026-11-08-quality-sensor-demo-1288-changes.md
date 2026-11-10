---
title: Issue 1288 changes
description: Source and test changes delivered for the retained sensor read model, employee UI and Quality evidence grounding
ms.date: 2026-11-08
---

Plan: [plan](../plans/2026-11-08-quality-sensor-demo-1288-plan.md). Recorded 2026-11-08T19:30Z after implementation. Base `origin/main` `ecb28815b2f5dd354ba1d34046cf02784b49bdd2`. Source and local only.

## Added

* `src/core/src/zava_forward/core/sensor_view.py`: read-only bounded read model (`consent`, `reference_for`, `capture_source`, `citations`, `view`). Synthetic rows only, one home, at most 12 window readings and 4 before and 4 after, 6 hour sealed UTC window, units degC and %RH.
* `src/api/tests/test_quality_sensors.py`: real SQLite tests for states, bounds, side-effect freedom, before/after absence, role denial, same IDs and values in the captured (MOCK) model request, flag only for returned model output, dedupe across restart, seal stability.

## Changed

* `core/assistants.py`: quality-evidence registry, purpose and rules now include sensors (changes rule and registry hashes, so existing quality releases no longer match: intended); `capture(..., sensors=None)` adds the sensors source and `sensor:{reading_id}` citations; `eligible` uses them; `review_flag`; `snapshot` captures the source; `Assistants.sensors` authorizes through the existing quality-evidence roles, staff scope and revocation.
* `api/server.py`: `GET /api/cases/{id}/sensors` (403, 404, 400, 503 with manual route).
* `web/ops.js`, `web/app.js`: `sensorPanel` in the Quality and handover tab with native tables, plain-language freshness and absence text, manual route.
* `web/assistants.js`: "Review requested" block shown only when `review_flag` exists.
* `core/README.md`: component note.

## Divergences and amendments

* Plan said `Store.sensor_view`; delivered through `Assistants.sensors` to reuse its SQL connection and authorization. No store change.
* Before and after context is also capped at the sealed window end so the captured source is time-stable (found when a dedupe test failed; fixed before commit).
* Before/after reference is the first non-superseded quality record time, not an install date (no retained stage marker exists).

## Validation run

* `test_quality_sensors test_assistants test_assistant_release` from `src/api` in `/tmp/ama-1288-venv` (editable installs of this worktree): 187 tests OK, 62 skipped (SQL Server variants).
* `test_mvp` with the above in one run earlier: 208 OK, 62 skipped.
* `ruff check` and `ruff format --check` on the new Python files, `ruff check` on changed `assistants.py` and `server.py`: pass. `node --check` on the three changed JS files: pass.
* Browser (headless Chromium via Playwright, local seeded SQLite app, signed in as a Programme Manager, no lock contention, `/` 12G and `/mnt` 7.0G free): Quality tab shows two native tables, 10 reading rows with IDs, units, UTC times and a stale-freshness message. axe-core 4.14 on the rendered fragment (WCAG 2 A/AA/2.2 AA and best-practice): only `page-has-heading-one`, an artefact of testing a fragment. Not an assistive-technology acceptance claim. The review-flag block was not exercised in a browser.

## Not run

* `tools/rpi-checks.py --changed` (would reinstall projects and rebuild images; owner CI-FIRST scope excludes it here). SQL Server variants. Real model, Azure, Hub or device.
