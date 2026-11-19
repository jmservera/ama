---
title: Issue 111 live2 research
ms.date: 2026-11-18
---

Task: issue-111-live2. Refs #111. Synthetic demo, desktop only, FOCUSED tier (no src change).
Unticked criterion: R1 to R3 complete before a derived measure is used beyond an exercise rule.
Prior note on main: docs/reference/research/issue-111-sensor-analysis-live-evidence-2026-11-18.md (raw output not retained).
Research disposition: executed (re-run tests, signed-in demo walk, raw output retained).
Planning Readiness: Ready.

## Findings

* Core sensor tests re-run with raw output retained: 22 tests OK (1 expected failure); 91 tests OK (22 skipped, MSSQL-dependent). See docs/reference/research/issue-111-live2-raw/.
* Staff Playwright sign-in succeeded; `/api/cases/{id}/sensors` for one demo case returned `retained-reading-view-v2`, synthetic readings, `calibrated: false`, freshness `stale`, repeat call byte-identical; `sensor-drafts` returned `{"state":"disabled"}` (no SENSOR_REVIEW_DUE task created).
* Criterion 3 (R1 to R3) stays unproven: R2 needs named reviewer and Asset sign-off, R3 agreed limits, R1 official standards texts unread.
* Credential hygiene incident: a probe command printed the one-line staff credential file to the session transcript. Not stored in artifacts; owner should consider rotating the test user password.
